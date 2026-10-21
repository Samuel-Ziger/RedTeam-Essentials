#!/usr/bin/env bash
set -Eeuo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BUILD="$(mktemp -d)"
trap 'rm -rf -- "$BUILD"' EXIT
passed=0
skipped=0
pass() { printf 'PASS  %s\n' "$1"; passed=$((passed + 1)); }
skip() { printf 'SKIP  %s\n' "$1"; skipped=$((skipped + 1)); }
check() { [[ "$1" == *"$2"* ]] || { printf 'saida inesperada: %s\n' "$1" >&2; return 1; }; }
expect_usage_error() {
  local label="$1"
  local stdout
  local status
  shift
  set +e
  stdout="$("$@" 2>"$BUILD/usage-error.txt")"
  status=$?
  set -e
  [[ "$status" -eq 2 ]] || { printf '%s: codigo esperado 2, obtido %d\n' "$label" "$status" >&2; return 1; }
  [[ -z "$stdout" ]] || { printf '%s: stdout deveria estar vazio\n' "$label" >&2; return 1; }
  [[ -s "$BUILD/usage-error.txt" ]] || { printf '%s: stderr deveria conter diagnostico\n' "$label" >&2; return 1; }
}

if command -v python3 >/dev/null; then
  export PYTHONPYCACHEPREFIX="$BUILD/pycache"
  (cd "$ROOT/exemplos/python" && python3 -m unittest discover -v)
  output="$(python3 "$ROOT/exemplos/python/api_query.py" --limit 20 --after abc_123 --status active)"
  check "$output" "GET /v1/items?limit=20&after=abc_123&status=active"
  expect_usage_error "Python entrada invalida" python3 "$ROOT/exemplos/python/api_query.py" --limit nope
  expect_usage_error "Python argumento repetido" python3 "$ROOT/exemplos/python/api_query.py" --limit 1 --limit 2
  pass "Python: exemplo de contrato"
  if python3 -c 'import fastapi, httpx2, openapi_spec_validator, pytest, yaml' >/dev/null 2>&1; then
    (cd "$ROOT/projetos/contract-lab-api" && PYTHONPATH=. python3 -m pytest -q)
    pass "Contract Lab API"
  else
    skip "dependencias da Contract Lab API ausentes"
  fi
else skip "Python 3 ausente"; fi

if command -v javac >/dev/null && command -v java >/dev/null; then
  java_major="$(javac -version 2>&1 | awk '{print $2}' | cut -d. -f1)"
  if [[ "$java_major" =~ ^[0-9]+$ ]] && ((java_major >= 11)); then
    mkdir -p "$BUILD/java"
    javac -Xlint:all -Werror -d "$BUILD/java" "$ROOT/exemplos/java/ApiQuery.java"
    output="$(java -cp "$BUILD/java" ApiQuery --limit 20 --after abc_123 --status active)"
    check "$output" "GET /v1/items?limit=20&after=abc_123&status=active"
    expect_usage_error "Java entrada invalida" java -cp "$BUILD/java" ApiQuery --limit nope
    expect_usage_error "Java argumento repetido" java -cp "$BUILD/java" ApiQuery --limit 1 --limit 2
    pass "Java"
  else skip "JDK 11+ necessario; encontrado $(javac -version 2>&1)"; fi
else skip "JDK ausente"; fi

if command -v cc >/dev/null; then
  cc -std=c17 -Wall -Wextra -Wpedantic -Werror "$ROOT/exemplos/c/api_query.c" -o "$BUILD/api_query"
  output="$("$BUILD/api_query" --limit 20 --after abc_123 --status active)"
  check "$output" "GET /v1/items?limit=20&after=abc_123&status=active"
  expect_usage_error "C entrada invalida" "$BUILD/api_query" --limit nope
  expect_usage_error "C argumento repetido" "$BUILD/api_query" --limit 1 --limit 2
  pass "C17"
else skip "compilador C ausente"; fi

if command -v node >/dev/null; then
  node --test "$ROOT/exemplos/javascript/api-query.test.mjs"
  output="$(node "$ROOT/exemplos/javascript/api-query.mjs" --limit 20 --after abc_123 --status active)"
  check "$output" "GET /v1/items?limit=20&after=abc_123&status=active"
  expect_usage_error "JavaScript entrada invalida" node "$ROOT/exemplos/javascript/api-query.mjs" --limit nope
  expect_usage_error "JavaScript argumento repetido" node "$ROOT/exemplos/javascript/api-query.mjs" --limit 1 --limit 2
  pass "JavaScript"
else skip "Node.js ausente"; fi

if command -v dotnet >/dev/null; then
  dotnet_major="$(dotnet --version | cut -d. -f1)"
  if [[ "$dotnet_major" =~ ^[0-9]+$ ]] && ((dotnet_major >= 10)); then
    output="$(dotnet run --project "$ROOT/exemplos/csharp/ApiQuery.csproj" --configuration Release --artifacts-path "$BUILD/dotnet" -- --limit 20 --after abc_123 --status active)"
    check "$output" "GET /v1/items?limit=20&after=abc_123&status=active"
    expect_usage_error "C# entrada invalida" dotnet run --project "$ROOT/exemplos/csharp/ApiQuery.csproj" --configuration Release --artifacts-path "$BUILD/dotnet" -- --limit nope
    expect_usage_error "C# argumento repetido" dotnet run --project "$ROOT/exemplos/csharp/ApiQuery.csproj" --configuration Release --artifacts-path "$BUILD/dotnet" -- --limit 1 --limit 2
    pass "C#"
  else skip ".NET 10+ necessario; encontrado $(dotnet --version)"; fi
else skip ".NET SDK ausente"; fi

if command -v ruff >/dev/null; then
  ruff check "$ROOT/exemplos/python" "$ROOT/projetos/contract-lab-api"
  ruff format --check "$ROOT/exemplos/python" "$ROOT/projetos/contract-lab-api"
  pass "Ruff"
else skip "Ruff ausente"; fi

printf '\nResultado: %d passaram; %d ignoradas por falta de toolchain.\n' "$passed" "$skipped"
