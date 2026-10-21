#!/usr/bin/env bash
set -euo pipefail

BASE_URL="${BASE_URL:-http://127.0.0.1:8101}"
TEMP_DIR="$(mktemp -d)"
CURL=(curl --silent --show-error --connect-timeout 3 --max-time 15)
trap 'rm -rf "$TEMP_DIR"' EXIT

fail() {
  printf '[FALHA] %s\n' "$1" >&2
  exit 1
}

json_value() {
  python3 -c "import json,sys; print(json.load(sys.stdin)$1)"
}

header_value() {
  local name="$1" file="$2"
  awk -v wanted="${name,,}" '
    BEGIN { FS=": *" }
    tolower($1) == wanted {
      sub("\\r$", "", $2)
      print $2
    }
  ' "$file" | tail -n 1
}

assert_problem() {
  local expected_status="$1" expected_suffix="$2" body_file="$3" header_file="$4"
  local content_type
  content_type="$(header_value content-type "$header_file")"
  [[ "$content_type" == application/problem+json* ]] || \
    fail "erro $expected_status não retornou application/problem+json"
  python3 - "$expected_status" "$expected_suffix" "$body_file" <<'PY'
import json
import pathlib
import sys

expected_status = int(sys.argv[1])
expected_suffix = sys.argv[2]
document = json.loads(pathlib.Path(sys.argv[3]).read_text())
assert document["status"] == expected_status, document
assert document["type"].endswith(expected_suffix), document
assert document["requestId"], document
assert document["instance"].startswith("/"), document
PY
}

request_id="smoke-$(python3 -c 'import uuid; print(uuid.uuid4().hex)')"
sku="COURSE-${request_id:6:20}"
second_sku="EXTRA-${request_id:6:20}"
operation_id="$(python3 -c 'import uuid; print(uuid.uuid4())')"

gateway_status="$("${CURL[@]}" --output /dev/null --write-out '%{http_code}' \
  "$BASE_URL/gateway-health")"
[[ "$gateway_status" == 204 ]] || fail "gateway health retornou $gateway_status"

for endpoint in live ready; do
  "${CURL[@]}" --fail "$BASE_URL/health/$endpoint" |
    python3 -c 'import json,sys; assert json.load(sys.stdin) == {"status":"ok"}'
done

"${CURL[@]}" --fail \
  --dump-header "$TEMP_DIR/create.headers" \
  --output "$TEMP_DIR/create.json" \
  --request POST "$BASE_URL/api/v1/products" \
  --header 'Content-Type: application/json' \
  --header "X-Request-ID: $request_id" \
  --header "Idempotency-Key: $request_id" \
  --data "{\"sku\":\"$sku\",\"name\":\"Produto 100%_seguro smoke\",\"priceCents\":2500,\"initialStock\":2}"

product_id="$(json_value '["id"]' <"$TEMP_DIR/create.json")"
etag="$(header_value etag "$TEMP_DIR/create.headers")"
location="$(header_value location "$TEMP_DIR/create.headers")"
response_request_id="$(header_value x-request-id "$TEMP_DIR/create.headers")"
[[ -n "$product_id" && "$etag" == '"1"' ]] || fail 'criação não retornou ID/ETag esperado'
[[ "$location" == "/api/v1/products/$product_id" ]] || fail 'Location da criação é inválido'
[[ "$response_request_id" == "$request_id" ]] || fail 'request ID válido não foi preservado'

"${CURL[@]}" --fail \
  --dump-header "$TEMP_DIR/replay.headers" \
  --output "$TEMP_DIR/replay.json" \
  --request POST "$BASE_URL/api/v1/products" \
  --header 'Content-Type: application/json' \
  --header "Idempotency-Key: $request_id" \
  --data "{\"sku\":\"$sku\",\"name\":\"Produto 100%_seguro smoke\",\"priceCents\":2500,\"initialStock\":2}"
[[ "$(header_value idempotency-replayed "$TEMP_DIR/replay.headers")" == true ]] || \
  fail 'retry não foi identificado'
cmp --silent "$TEMP_DIR/create.json" "$TEMP_DIR/replay.json" || \
  fail 'retry alterou a resposta armazenada'

conflict_status="$("${CURL[@]}" \
  --dump-header "$TEMP_DIR/conflict.headers" \
  --output "$TEMP_DIR/conflict.json" --write-out '%{http_code}' \
  --request POST "$BASE_URL/api/v1/products" \
  --header 'Content-Type: application/json' \
  --header "Idempotency-Key: $request_id" \
  --data "{\"sku\":\"$sku-X\",\"name\":\"Outro corpo\",\"priceCents\":1}")"
[[ "$conflict_status" == 409 ]] || fail 'reutilização conflitante deveria retornar 409'
assert_problem 409 idempotency-conflict "$TEMP_DIR/conflict.json" "$TEMP_DIR/conflict.headers"

"${CURL[@]}" --fail \
  --dump-header "$TEMP_DIR/update.headers" \
  --output "$TEMP_DIR/update.json" \
  --request PATCH "$BASE_URL/api/v1/products/$product_id" \
  --header 'Content-Type: application/json' \
  --header "If-Match: $etag" \
  --data '{"name":"Produto atualizado"}'
etag="$(header_value etag "$TEMP_DIR/update.headers")"
[[ "$etag" == '"2"' ]] || fail 'update não incrementou versão'

"${CURL[@]}" --fail \
  --dump-header "$TEMP_DIR/movement.headers" \
  --output "$TEMP_DIR/movement.json" \
  --request POST "$BASE_URL/api/v1/products/$product_id/stock-movements" \
  --header 'Content-Type: application/json' \
  --header "If-Match: $etag" \
  --data "{\"operationId\":\"$operation_id\",\"delta\":3,\"reason\":\"entrada do smoke test\"}"
[[ "$(json_value '["resultingStock"]' <"$TEMP_DIR/movement.json")" == 5 ]] || \
  fail 'movimento não alterou estoque'
[[ "$(header_value etag "$TEMP_DIR/movement.headers")" == '"3"' ]] || \
  fail 'movimento não retornou a nova versão'

"${CURL[@]}" --fail \
  --dump-header "$TEMP_DIR/movement-replay.headers" \
  --output "$TEMP_DIR/movement-replay.json" \
  --request POST "$BASE_URL/api/v1/products/$product_id/stock-movements" \
  --header 'Content-Type: application/json' \
  --header 'If-Match: "2"' \
  --data "{\"operationId\":\"$operation_id\",\"delta\":3,\"reason\":\"entrada do smoke test\"}"
[[ "$(header_value idempotency-replayed "$TEMP_DIR/movement-replay.headers")" == true ]] || \
  fail 'replay do movimento não foi identificado'
cmp --silent "$TEMP_DIR/movement.json" "$TEMP_DIR/movement-replay.json" || \
  fail 'replay do movimento alterou o resultado'

operation_conflict_status="$("${CURL[@]}" \
  --dump-header "$TEMP_DIR/operation-conflict.headers" \
  --output "$TEMP_DIR/operation-conflict.json" --write-out '%{http_code}' \
  --request POST "$BASE_URL/api/v1/products/$product_id/stock-movements" \
  --header 'Content-Type: application/json' \
  --header 'If-Match: "3"' \
  --data "{\"operationId\":\"$operation_id\",\"delta\":3,\"reason\":\"entrada do smoke test\"}")"
[[ "$operation_conflict_status" == 409 ]] || fail 'operation ID com precondição diferente deveria retornar 409'
assert_problem 409 idempotency-conflict \
  "$TEMP_DIR/operation-conflict.json" "$TEMP_DIR/operation-conflict.headers"

stale_status="$("${CURL[@]}" \
  --dump-header "$TEMP_DIR/stale.headers" \
  --output "$TEMP_DIR/stale.json" --write-out '%{http_code}' \
  --request PATCH "$BASE_URL/api/v1/products/$product_id" \
  --header 'Content-Type: application/json' \
  --header 'If-Match: "1"' \
  --data '{"name":"alteração obsoleta"}')"
[[ "$stale_status" == 412 ]] || fail 'ETag obsoleto deveria retornar 412'
assert_problem 412 version-conflict "$TEMP_DIR/stale.json" "$TEMP_DIR/stale.headers"

missing_precondition_status="$("${CURL[@]}" \
  --dump-header "$TEMP_DIR/precondition.headers" \
  --output "$TEMP_DIR/precondition.json" --write-out '%{http_code}' \
  --request PATCH "$BASE_URL/api/v1/products/$product_id" \
  --header 'Content-Type: application/json' \
  --data '{"name":"sem precondição"}')"
[[ "$missing_precondition_status" == 428 ]] || fail 'If-Match ausente deveria retornar 428'
assert_problem 428 precondition-required \
  "$TEMP_DIR/precondition.json" "$TEMP_DIR/precondition.headers"

"${CURL[@]}" --fail --output "$TEMP_DIR/search.json" \
  "$BASE_URL/api/v1/products?limit=10&q=%25_"
python3 - "$sku" "$TEMP_DIR/search.json" <<'PY'
import json
import pathlib
import sys

sku = sys.argv[1]
page = json.loads(pathlib.Path(sys.argv[2]).read_text())
assert [item["sku"] for item in page["items"]] == [sku], page
PY

second_key="second-$request_id"
"${CURL[@]}" --fail --output "$TEMP_DIR/second.json" \
  --request POST "$BASE_URL/api/v1/products" \
  --header 'Content-Type: application/json' \
  --header "Idempotency-Key: $second_key" \
  --data "{\"sku\":\"$second_sku\",\"name\":\"Segundo produto\",\"priceCents\":100}"

"${CURL[@]}" --fail --output "$TEMP_DIR/page.json" \
  "$BASE_URL/api/v1/products?limit=1"
next_cursor="$(json_value '["nextCursor"]' <"$TEMP_DIR/page.json")"
[[ -n "$next_cursor" && "$next_cursor" != None ]] || fail 'primeira página não retornou cursor'
"${CURL[@]}" --fail --get --output "$TEMP_DIR/next-page.json" \
  --data-urlencode 'limit=1' --data-urlencode "after=$next_cursor" \
  "$BASE_URL/api/v1/products"
[[ "$(json_value '["items"].__len__()' <"$TEMP_DIR/next-page.json")" == 1 ]] || \
  fail 'segunda página deveria conter um produto'

events=0
for _ in {1..40}; do
  "${CURL[@]}" --fail "$BASE_URL/api/v1/products/$product_id/events" \
    >"$TEMP_DIR/events.json"
  events="$(json_value '.__len__()' <"$TEMP_DIR/events.json")"
  (( events >= 3 )) && break
  sleep 0.25
done
(( events >= 3 )) || fail 'outbox não convergiu para o MongoDB'

"${CURL[@]}" --fail "$BASE_URL/openapi.json" >"$TEMP_DIR/openapi.json"
python3 - "$TEMP_DIR/openapi.json" <<'PY'
import json
import pathlib
import sys

schema = json.loads(pathlib.Path(sys.argv[1]).read_text())
assert schema["info"]["version"] == "1.0.0"
assert "/api/v1/products" in schema["paths"]
assert "ProblemView" in schema["components"]["schemas"]
PY

"${CURL[@]}" --fail --dump-header "$TEMP_DIR/headers" --output /dev/null \
  "$BASE_URL/health/live"
[[ "$(header_value x-content-type-options "$TEMP_DIR/headers")" == nosniff ]] || \
  fail 'gateway não enviou X-Content-Type-Options'
[[ "$(header_value cache-control "$TEMP_DIR/headers")" == no-store ]] || \
  fail 'gateway não enviou Cache-Control esperado'
for unique_header in x-request-id x-content-type-options cache-control; do
  header_count="$(awk -v wanted="$unique_header" '
    BEGIN { count = 0 }
    tolower($0) ~ "^" wanted ":" { count += 1 }
    END { print count }
  ' "$TEMP_DIR/headers")"
  [[ "$header_count" == 1 ]] || fail "gateway enviou $header_count ocorrências de $unique_header"
done

printf '[OK] HTTP, Problem Details, idempotência, ETag, cursor, PostgreSQL, outbox e MongoDB validados\n'
