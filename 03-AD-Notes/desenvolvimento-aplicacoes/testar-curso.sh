#!/usr/bin/env bash
set -Eeuo pipefail

COURSE_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BUILD_DIR="$(mktemp -d)"
trap 'rm -rf -- "$BUILD_DIR"' EXIT

passed=0
skipped=0

pass() {
  printf 'PASS  %s\n' "$1"
  passed=$((passed + 1))
}

skip() {
  printf 'SKIP  %s\n' "$1"
  skipped=$((skipped + 1))
}

assert_contains() {
  local value="$1"
  local expected="$2"
  if [[ "$value" != *"$expected"* ]]; then
    printf 'Esperado encontrar %q em %q\n' "$expected" "$value" >&2
    return 1
  fi
}

assert_failure_contract() {
  local expected_message="$1"
  shift
  local stdout_path="$BUILD_DIR/negative.stdout"
  local stderr_path="$BUILD_DIR/negative.stderr"
  local status

  if "$@" >"$stdout_path" 2>"$stderr_path"; then
    printf 'Esperava falha, mas o comando terminou com sucesso: %q\n' "$1" >&2
    return 1
  else
    status=$?
  fi
  if ((status != 2)); then
    printf 'Esperava codigo 2, recebeu %d: %q\n' "$status" "$1" >&2
    return 1
  fi
  if [[ -s "$stdout_path" ]]; then
    printf 'Falha de uso escreveu em stdout: %s\n' "$(<"$stdout_path")" >&2
    return 1
  fi
  assert_contains "$(<"$stderr_path")" "$expected_message"
}

assert_help_contract() {
  local stdout_path="$BUILD_DIR/help.stdout"
  local stderr_path="$BUILD_DIR/help.stderr"
  local help_output

  "$@" >"$stdout_path" 2>"$stderr_path"
  help_output="$(<"$stdout_path")"
  if [[ "${help_output,,}" != *"usage:"* ]]; then
    printf 'Ajuda nao contem linha de uso: %q\n' "$help_output" >&2
    return 1
  fi
  if [[ -s "$stderr_path" ]]; then
    printf 'Ajuda escreveu em stderr: %s\n' "$(<"$stderr_path")" >&2
    return 1
  fi
}

if command -v python3 >/dev/null 2>&1; then
  export PYTHONPYCACHEPREFIX="$BUILD_DIR/pycache"
  (
    cd "$COURSE_ROOT/exemplos/python"
    python3 -m unittest discover -v
  )
  output="$(APP_PROFILE=testing python3 "$COURSE_ROOT/exemplos/python/app_config.py" --format json)"
  assert_contains "$output" '"profile":"testing"'
  output="$(APP_PROFILE=testing python3 "$COURSE_ROOT/exemplos/python/app_config.py" --profile production)"
  assert_contains "$output" "profile=production source=cli"
  assert_failure_contract "APP_PROFILE invalido" env APP_PROFILE=unknown \
    python3 "$COURSE_ROOT/exemplos/python/app_config.py"
  assert_help_contract env APP_PROFILE=unknown \
    python3 "$COURSE_ROOT/exemplos/python/app_config.py" --help
  pass "Python: testes e contrato da aplicacao"
else
  skip "Python 3 nao encontrado"
fi

if command -v javac >/dev/null 2>&1 && command -v java >/dev/null 2>&1; then
  mkdir -p "$BUILD_DIR/java"
  javac -Xlint:all -Werror -d "$BUILD_DIR/java" "$COURSE_ROOT/exemplos/java/AppConfig.java"
  output="$(APP_PROFILE=testing java -cp "$BUILD_DIR/java" AppConfig --format json)"
  assert_contains "$output" '"source":"environment"'
  output="$(APP_PROFILE=testing java -cp "$BUILD_DIR/java" AppConfig --profile production)"
  assert_contains "$output" "profile=production source=cli"
  assert_failure_contract "profile invalido" env APP_PROFILE=unknown \
    java -cp "$BUILD_DIR/java" AppConfig
  assert_help_contract env APP_PROFILE=unknown java -cp "$BUILD_DIR/java" AppConfig --help
  pass "Java: compilacao estrita e precedencia"
else
  skip "JDK nao encontrado"
fi

if command -v cc >/dev/null 2>&1; then
  cc -std=c17 -Wall -Wextra -Wpedantic -Werror \
    "$COURSE_ROOT/exemplos/c/app_config.c" -o "$BUILD_DIR/app_config_c"
  output="$(APP_PROFILE=testing "$BUILD_DIR/app_config_c" --format json)"
  assert_contains "$output" '"source":"environment"'
  output="$(APP_PROFILE=testing "$BUILD_DIR/app_config_c" --profile production)"
  assert_contains "$output" "profile=production source=cli"
  assert_failure_contract "profile invalido" env APP_PROFILE=unknown "$BUILD_DIR/app_config_c"
  assert_help_contract env APP_PROFILE=unknown "$BUILD_DIR/app_config_c" --help
  pass "C17: compilacao estrita e precedencia"
else
  skip "compilador C nao encontrado"
fi

if command -v node >/dev/null 2>&1; then
  node --test "$COURSE_ROOT/exemplos/javascript/app-config.test.mjs"
  node --check "$COURSE_ROOT/projetos/study-desk/src/app.mjs"
  (
    cd "$COURSE_ROOT/projetos/study-desk"
    npm test
  )
  output="$(APP_PROFILE=testing node "$COURSE_ROOT/exemplos/javascript/app-config.mjs" --format json)"
  assert_contains "$output" '"source":"environment"'
  assert_failure_contract "APP_PROFILE invalido" env APP_PROFILE=unknown \
    node "$COURSE_ROOT/exemplos/javascript/app-config.mjs"
  assert_help_contract env APP_PROFILE=unknown \
    node "$COURSE_ROOT/exemplos/javascript/app-config.mjs" --help
  pass "JavaScript: contrato e Study Desk"
else
  skip "Node.js nao encontrado"
fi

if command -v dotnet >/dev/null 2>&1; then
  dotnet_major="$(dotnet --version | cut -d. -f1)"
  if [[ "$dotnet_major" =~ ^[0-9]+$ ]] && ((dotnet_major >= 10)); then
    output="$(APP_PROFILE=testing dotnet run \
      --project "$COURSE_ROOT/exemplos/csharp/AppConfig.csproj" \
      --configuration Release \
      --artifacts-path "$BUILD_DIR/dotnet" -- --format json)"
    assert_contains "$output" '"source":"environment"'
    output="$(APP_PROFILE=testing dotnet run \
      --project "$COURSE_ROOT/exemplos/csharp/AppConfig.csproj" \
      --configuration Release \
      --artifacts-path "$BUILD_DIR/dotnet" -- --profile production)"
    assert_contains "$output" "profile=production source=cli"
    assert_failure_contract "profile invalido" env APP_PROFILE=unknown dotnet run \
      --project "$COURSE_ROOT/exemplos/csharp/AppConfig.csproj" \
      --configuration Release --artifacts-path "$BUILD_DIR/dotnet"
    assert_help_contract env APP_PROFILE=unknown dotnet run \
      --project "$COURSE_ROOT/exemplos/csharp/AppConfig.csproj" \
      --configuration Release --artifacts-path "$BUILD_DIR/dotnet" -- --help
    pass "C#: build estrito e precedencia"
  else
    skip ".NET 10+ necessario; encontrado $(dotnet --version)"
  fi
else
  skip ".NET SDK nao encontrado"
fi

if command -v ruff >/dev/null 2>&1; then
  ruff check "$COURSE_ROOT/exemplos/python"
  ruff format --check "$COURSE_ROOT/exemplos/python"
  pass "Python: lint e formatacao"
else
  skip "Ruff nao encontrado"
fi

printf '\nResultado: %d verificacoes passaram; %d foram ignoradas por falta de toolchain.\n' \
  "$passed" "$skipped"
