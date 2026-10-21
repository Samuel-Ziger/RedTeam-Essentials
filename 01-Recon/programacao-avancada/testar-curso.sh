#!/usr/bin/env bash
set -euo pipefail

REQUIRE_ALL=0

usage() {
  cat <<'EOF'
Uso: testar-curso.sh [--require-all]

Executa testes unitários, contratos HTTP, clientes nas cinco linguagens e
validação estática do ambiente Docker. Runtimes/dependências ausentes aparecem
como PULADO. Com --require-all, qualquer verificação pulada encerra com código 1.

Os testes de integração com bancos reais são deliberadamente separados:
  laboratorios/testar-laboratorios.sh
  projetos/inventory-api/smoke-test.sh   # com o Compose já iniciado
EOF
}

while (( $# > 0 )); do
  case "$1" in
    --require-all)
      REQUIRE_ALL=1
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      printf '[FALHA] opção desconhecida: %s\n' "$1" >&2
      usage >&2
      exit 2
      ;;
  esac
  shift
done

COURSE_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
API_DIR="$COURSE_DIR/projetos/inventory-api/api"
BUILD_DIR="$(mktemp -d)"
MOCK_PID=""
MOCK_READY=0
MOCK_PORT=""
SKIPPED_CHECKS=0

cleanup() {
  if [[ -n "$MOCK_PID" ]] && kill -0 "$MOCK_PID" 2>/dev/null; then
    kill "$MOCK_PID" 2>/dev/null || true
    wait "$MOCK_PID" 2>/dev/null || true
  fi
  rm -rf "$BUILD_DIR"
}
trap cleanup EXIT

export PYTHONPYCACHEPREFIX="$BUILD_DIR/pycache"

pass() { printf '[OK] %s\n' "$1"; }
fail() {
  printf '[FALHA] %s\n' "$1" >&2
  exit 1
}
skip() {
  SKIPPED_CHECKS=$((SKIPPED_CHECKS + 1))
  printf '[PULADO] %s\n' "$1"
}
require() {
  if ! command -v "$1" >/dev/null 2>&1; then
    skip "$1 não encontrado"
    return 1
  fi
}

check_python_version() {
  local version major minor
  version="$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')"
  IFS=. read -r major minor <<<"$version"
  if ! [[ "$major" =~ ^[0-9]+$ && "$minor" =~ ^[0-9]+$ ]]; then
    fail "não foi possível interpretar a versão do Python: $version"
  fi
  if (( major != 3 || minor < 12 )); then
    fail "Python 3.12+ necessário; instalado: $version"
  fi
  pass "Python $version compatível"
}

check_node_version() {
  local version major minor
  version="$(node --version)"
  version="${version#v}"
  IFS=. read -r major minor _ <<<"$version"
  if ! [[ "$major" =~ ^[0-9]+$ && "$minor" =~ ^[0-9]+$ ]]; then
    fail "não foi possível interpretar a versão do Node.js: $version"
  fi
  if (( major < 22 || major % 2 != 0 || (major == 22 && minor < 12) )); then
    fail "Node.js 22.12+ em linha par suportada necessário; instalado: $version"
  fi
  pass "Node.js $version compatível"
}

start_mock_api() {
  local attempts port_file
  port_file="$BUILD_DIR/mock-api.port"
  python3 "$COURSE_DIR/exemplos/mock_api.py" >"$port_file" \
    2>"$BUILD_DIR/mock-api.stderr" &
  MOCK_PID=$!
  for attempts in {1..100}; do
    if [[ -s "$port_file" ]]; then
      read -r MOCK_PORT <"$port_file"
      if [[ "$MOCK_PORT" =~ ^[0-9]+$ ]] && (( MOCK_PORT >= 1 && MOCK_PORT <= 65535 )); then
        export MOCK_PORT
        export INVENTORY_URL="http://127.0.0.1:$MOCK_PORT"
        MOCK_READY=1
        return
      fi
      fail "mock API publicou porta inválida: $MOCK_PORT"
    fi
    if ! kill -0 "$MOCK_PID" 2>/dev/null; then
      sed -n '1,40p' "$BUILD_DIR/mock-api.stderr" >&2
      fail 'mock API encerrou antes de publicar a porta'
    fi
    sleep 0.05
  done
  fail 'timeout ao iniciar mock API local'
}

if require python3; then
  check_python_version
  python3 -m unittest discover -s "$COURSE_DIR/exemplos/python" -p 'test_*.py'
  python3 -m compileall -q -x '(^|/)(\.venv|venv|node_modules)(/|$)' "$COURSE_DIR"
  pass 'cliente e testes Python'

  if python3 -c 'import fastapi, httpx2, psycopg, psycopg_pool, pydantic, pymongo, pytest' \
      >/dev/null 2>&1; then
    PYTHONPATH="$API_DIR/src" python3 -m pytest -q "$API_DIR/tests"
    pass 'testes unitários, casos de uso e contrato HTTP da Inventory API'
  else
    skip 'dependências da API; instale api/requirements-dev.txt em ambiente virtual'
  fi

  start_mock_api
  python_output="$(python3 "$COURSE_DIR/exemplos/python/api_client.py")"
  grep -q 'health=ok request_id=mock-request-001' <<<"$python_output"
  grep -q 'BOOK-001: Banco de Dados' <<<"$python_output"
  pass 'cliente Python contra contrato HTTP local'
fi

bash -n "$COURSE_DIR/testar-curso.sh"
bash -n "$COURSE_DIR/laboratorios/testar-laboratorios.sh"
bash -n "$COURSE_DIR/projetos/inventory-api/smoke-test.sh"
pass 'sintaxe Bash'

if command -v javac >/dev/null 2>&1; then
  javac_version="$(javac -version 2>&1 | awk '{print $2}')"
  javac_major="${javac_version%%.*}"
else
  javac_major=0
fi
if [[ "$javac_major" =~ ^[0-9]+$ ]] && (( javac_major >= 17 )); then
  javac -Xlint:all -Werror -d "$BUILD_DIR/java" \
    "$COURSE_DIR/exemplos/java/ApiClient.java"
  if (( MOCK_READY )); then
    java_output="$(INVENTORY_URL="$INVENTORY_URL" java -cp "$BUILD_DIR/java" ApiClient)"
    grep -q 'health=ok request_id=mock-request-001' <<<"$java_output"
    grep -q 'BOOK-001' <<<"$java_output"
    pass 'cliente Java 17+ compilado e executado'
  else
    pass 'cliente Java 17+ compilado; execução requer Python para o mock local'
  fi
else
  skip "javac 17+ necessário; instalado: $javac_major"
fi

if require cc; then
  cc -std=c17 -Wall -Wextra -Wpedantic -Werror \
    "$COURSE_DIR/exemplos/c/api_client.c" -o "$BUILD_DIR/api-client-c"
  if (( MOCK_READY )); then
    c_output="$(INVENTORY_HOST=127.0.0.1 INVENTORY_PORT="$MOCK_PORT" \
      "$BUILD_DIR/api-client-c")"
    grep -q 'HTTP/1.1 200' <<<"$c_output"
    grep -q '"status":"ok"' <<<"$c_output"
    if INVENTORY_HOST=example.com INVENTORY_PORT=80 \
        "$BUILD_DIR/api-client-c" >/dev/null 2>&1; then
      fail 'cliente C deveria recusar host fora de loopback'
    fi
    pass 'cliente C17 compilado e executado'
  else
    pass 'cliente C17 compilado; execução requer Python para o mock local'
  fi
fi

if require node; then
  check_node_version
  node --check "$COURSE_DIR/laboratorios/mongodb/001_setup.js"
  node --check "$COURSE_DIR/laboratorios/mongodb/002_queries.js"
  node --check "$COURSE_DIR/laboratorios/mongodb/003_assertions.js"
  node --check "$COURSE_DIR/projetos/inventory-api/db/mongo/001_indexes.js"
  if (( MOCK_READY )); then
    node --test "$COURSE_DIR/exemplos/javascript/api_client.test.mjs"
    js_output="$(INVENTORY_URL="$INVENTORY_URL" \
      node "$COURSE_DIR/exemplos/javascript/api_client.mjs")"
    grep -q 'health=ok request_id=mock-request-001' <<<"$js_output"
    grep -q 'BOOK-001: Banco de Dados' <<<"$js_output"
    pass 'cliente JavaScript e scripts MongoDB'
  else
    pass 'sintaxe JavaScript/MongoDB; testes HTTP requerem Python para o mock local'
  fi
fi

if require dotnet; then
  dotnet_version="$(dotnet --version)"
  dotnet_major="${dotnet_version%%.*}"
  if [[ "$dotnet_major" =~ ^[0-9]+$ ]] && (( dotnet_major >= 10 )); then
    dotnet build --nologo --configuration Release \
      --property:BaseOutputPath="$BUILD_DIR/dotnet/bin/" \
      --property:BaseIntermediateOutputPath="$BUILD_DIR/dotnet/obj/" \
      "$COURSE_DIR/exemplos/csharp/ApiClient.csproj"
    if (( MOCK_READY )); then
      csharp_output="$(INVENTORY_URL="$INVENTORY_URL" \
        dotnet "$BUILD_DIR/dotnet/bin/Release/net10.0/ApiClient.dll")"
      grep -q 'health=ok request_id=mock-request-001' <<<"$csharp_output"
      grep -q 'BOOK-001: Banco de Dados' <<<"$csharp_output"
      pass 'cliente C#/.NET 10 compilado e executado'
    else
      pass 'cliente C#/.NET 10 compilado; execução requer Python para o mock local'
    fi
  else
    skip ".NET 10+ necessário; instalado: $dotnet_version"
  fi
fi

if command -v docker >/dev/null 2>&1 && docker compose version >/dev/null 2>&1; then
  docker compose -f "$COURSE_DIR/laboratorios/compose.yaml" config --quiet
  docker compose -f "$COURSE_DIR/projetos/inventory-api/compose.yaml" config --quiet
  pass 'configurações Docker Compose'
else
  skip 'Docker Compose v2 não encontrado'
fi

if (( SKIPPED_CHECKS == 0 )); then
  pass 'curso avançado validado em todos os runtimes'
else
  printf '[PARCIAL] validações disponíveis concluídas; %d verificação(ões) pulada(s)\n' \
    "$SKIPPED_CHECKS"
  if (( REQUIRE_ALL )); then
    printf '[FALHA] --require-all exige que nenhuma verificação seja pulada\n' >&2
    exit 1
  fi
fi
