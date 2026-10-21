#!/usr/bin/env bash
set -euo pipefail

REQUIRE_ALL=0

usage() {
  cat <<'EOF'
Uso: testar-curso.sh [--require-all]

Sem opções, executa todas as verificações disponíveis e informa runtimes
ausentes como PULADO. Com --require-all, qualquer verificação pulada faz o
processo terminar com código 1; use esse modo para concluir o módulo e na CI.
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

if (( REQUIRE_ALL )); then
  # A suíte HTTP usa skip em sandboxes que proíbem loopback. Para a conclusão
  # formal isso é evidência ausente, portanto deve falhar em vez de parecer OK.
  export RTE_REQUIRE_HTTP_TESTS=1
else
  unset RTE_REQUIRE_HTTP_TESTS
fi

COURSE_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
BUILD_DIR="$(mktemp -d)"
trap 'rm -rf "$BUILD_DIR"' EXIT
export PYTHONPYCACHEPREFIX="$BUILD_DIR/pycache"
SKIPPED_CHECKS=0

pass() { printf '[OK] %s\n' "$1"; }
fail() {
  printf '[FALHA] %s\n' "$1" >&2
  exit 1
}
skip() {
  SKIPPED_CHECKS=$((SKIPPED_CHECKS + 1))
  printf '[PULADO] %s\n' "$1"
}
expect_status() {
  local expected="$1"
  shift
  local actual
  if "$@" >/dev/null 2>&1; then
    actual=0
  else
    actual=$?
  fi
  if (( actual != expected )); then
    printf '[FALHA] esperado código %d, recebido %d: %s\n' "$expected" "$actual" "$*" >&2
    return 1
  fi
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

if require python3; then
  check_python_version
  python3 -m unittest discover -s "$COURSE_DIR/exemplos/python" -p 'test_*.py'
  python3 -m unittest discover -s "$COURSE_DIR/labs/starter-http" -p 'test_*.py'
  python3 -m unittest discover -s "$COURSE_DIR/projetos/taskboard/api" -p 'test_*.py'
  python3 -m compileall -q "$COURSE_DIR"
  pass 'Python, starter HTTP e API TaskBoard'
fi

if command -v javac >/dev/null 2>&1; then
  javac_version="$(javac -version 2>&1 | awk '{print $2}')"
  javac_major="${javac_version%%.*}"
else
  javac_major=0
fi
if [[ "$javac_major" =~ ^[0-9]+$ ]] && (( javac_major >= 17 )); then
  javac -Xlint:all -Werror -d "$BUILD_DIR/java" "$COURSE_DIR/exemplos/java/Fundamentos.java"
  java -cp "$BUILD_DIR/java" Fundamentos 10 8 4 | grep -q 'media=7.33'
  java -cp "$BUILD_DIR/java" Fundamentos 0 10 | grep -q 'media=5.00'
  expect_status 2 java -cp "$BUILD_DIR/java" Fundamentos
  expect_status 2 java -cp "$BUILD_DIR/java" Fundamentos 11
  expect_status 2 java -cp "$BUILD_DIR/java" Fundamentos texto
  expect_status 2 java -cp "$BUILD_DIR/java" Fundamentos NaN
  pass 'Java'
elif command -v java >/dev/null 2>&1; then
  java_major="$(java -version 2>&1 | awk -F '[".]' 'NR == 1 {print $2}')"
  if [[ "$java_major" =~ ^[0-9]+$ ]] && (( java_major >= 17 )); then
    java "$COURSE_DIR/exemplos/java/Fundamentos.java" 10 8 4 | grep -q 'media=7.33'
    java "$COURSE_DIR/exemplos/java/Fundamentos.java" 0 10 | grep -q 'media=5.00'
    expect_status 2 java "$COURSE_DIR/exemplos/java/Fundamentos.java"
    expect_status 2 java "$COURSE_DIR/exemplos/java/Fundamentos.java" 11
    expect_status 2 java "$COURSE_DIR/exemplos/java/Fundamentos.java" texto
    expect_status 2 java "$COURSE_DIR/exemplos/java/Fundamentos.java" NaN
    pass 'Java em source-file mode'
  else
    skip "Java 17+ necessário"
  fi
else
  skip 'Java 17+ não encontrado'
fi

if require cc; then
  cc -std=c17 -Wall -Wextra -Wpedantic -Werror \
  "$COURSE_DIR/exemplos/c/fundamentos.c" -lm -o "$BUILD_DIR/fundamentos-c"
  "$BUILD_DIR/fundamentos-c" 10 8 4 | grep -q 'media=7.33'
  "$BUILD_DIR/fundamentos-c" 0 10 | grep -q 'media=5.00'
  expect_status 2 "$BUILD_DIR/fundamentos-c"
  expect_status 2 "$BUILD_DIR/fundamentos-c" 11
  expect_status 2 "$BUILD_DIR/fundamentos-c" texto
  expect_status 2 "$BUILD_DIR/fundamentos-c" NaN
  pass 'C17'
fi

if require node; then
  check_node_version
  node --test "$COURSE_DIR/exemplos/javascript/fundamentos.test.mjs"
  node --test "$COURSE_DIR/projetos/taskboard/web/taskboard-core.test.mjs"
  node --check "$COURSE_DIR/projetos/taskboard/web/app.js"
  node "$COURSE_DIR/exemplos/javascript/fundamentos.mjs" 10 8 4 | grep -q '"average":7.33'
  node "$COURSE_DIR/exemplos/javascript/fundamentos.mjs" 0 10 | grep -q '"average":5'
  expect_status 2 node "$COURSE_DIR/exemplos/javascript/fundamentos.mjs"
  expect_status 2 node "$COURSE_DIR/exemplos/javascript/fundamentos.mjs" 11
  expect_status 2 node "$COURSE_DIR/exemplos/javascript/fundamentos.mjs" texto
  expect_status 2 node "$COURSE_DIR/exemplos/javascript/fundamentos.mjs" NaN
  pass 'JavaScript'
fi

if require dotnet; then
  dotnet_major="$(dotnet --version | cut -d. -f1)"
  if [[ "$dotnet_major" =~ ^[0-9]+$ ]] && (( dotnet_major >= 10 )); then
    dotnet run --project "$COURSE_DIR/exemplos/csharp/CursoFundamentos.csproj" -- 10 8 4 \
      | grep -q 'media=7.33'
    dotnet run --no-build \
      --project "$COURSE_DIR/exemplos/csharp/CursoFundamentos.csproj" -- 0 10 \
      | grep -q 'media=5.00'
    expect_status 2 dotnet run --no-build \
      --project "$COURSE_DIR/exemplos/csharp/CursoFundamentos.csproj" --
    expect_status 2 dotnet run --no-build \
      --project "$COURSE_DIR/exemplos/csharp/CursoFundamentos.csproj" -- 11
    expect_status 2 dotnet run --no-build \
      --project "$COURSE_DIR/exemplos/csharp/CursoFundamentos.csproj" -- texto
    expect_status 2 dotnet run --no-build \
      --project "$COURSE_DIR/exemplos/csharp/CursoFundamentos.csproj" -- NaN
    pass 'C#/.NET'
  else
    skip ".NET 10+ necessário; instalado: $(dotnet --version)"
  fi
fi

if command -v docker >/dev/null 2>&1 && docker compose version >/dev/null 2>&1; then
  docker compose -f "$COURSE_DIR/projetos/taskboard/compose.yaml" config --quiet
  pass 'configuração Docker Compose do TaskBoard'
else
  skip 'Docker Compose v2 não encontrado'
fi

if (( SKIPPED_CHECKS == 0 )); then
  pass 'curso validado em todos os runtimes'
else
  printf '[PARCIAL] validações disponíveis concluídas; %d verificação(ões) pulada(s)\n' \
    "$SKIPPED_CHECKS"
  if (( REQUIRE_ALL )); then
    printf '[FALHA] --require-all exige que nenhuma verificação seja pulada\n' >&2
    exit 1
  fi
fi
