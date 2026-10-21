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
usage_failure() {
  local label="$1" stdout="$BUILD/usage.stdout" stderr="$BUILD/usage.stderr" status
  shift
  : >"$stdout"; : >"$stderr"
  set +e
  "$@" >"$stdout" 2>"$stderr"
  status=$?
  set -e
  [[ "$status" -eq 2 ]] || { printf '%s retornou %d, esperado 2\n' "$label" "$status" >&2; return 1; }
  [[ ! -s "$stdout" ]] || { printf '%s escreveu em stdout na falha\n' "$label" >&2; return 1; }
  [[ -s "$stderr" ]] || { printf '%s nao explicou a falha em stderr\n' "$label" >&2; return 1; }
}

if command -v python3 >/dev/null; then
  export PYTHONPYCACHEPREFIX="$BUILD/pycache"
  (cd "$ROOT/exemplos/python" && python3 -m unittest discover -v)
  PYTHONPATH="$ROOT/projetos/fileflow/src" python3 -m unittest discover -s "$ROOT/projetos/fileflow/tests" -v
  output="$(python3 "$ROOT/exemplos/python/batch_plan.py" --items z,a,z --format json)"
  check "$output" '"count":2'
  usage_failure "Python" python3 "$ROOT/exemplos/python/batch_plan.py" --items ../x
  PYTHONPATH="$ROOT/projetos/fileflow/src" python3 -m fileflow.cli --help >/dev/null
  PYTHONPATH="$ROOT/projetos/fileflow/src" python3 -m fileflow.cli --version >/dev/null
  pass "Python e FileFlow"
else skip "Python 3 ausente"; fi

if command -v javac >/dev/null && command -v java >/dev/null; then
  mkdir -p "$BUILD/java"
  javac -Xlint:all -Werror -d "$BUILD/java" "$ROOT/exemplos/java/BatchPlan.java"
  output="$(java -cp "$BUILD/java" BatchPlan --items z,a,z)"; check "$output" "count=2 items=a,z"
  usage_failure "Java" java -cp "$BUILD/java" BatchPlan --items ../x
  pass "Java"
else skip "JDK ausente"; fi

if command -v cc >/dev/null; then
  cc -std=c17 -Wall -Wextra -Wpedantic -Werror "$ROOT/exemplos/c/batch_plan.c" -o "$BUILD/batch_plan"
  output="$("$BUILD/batch_plan" --items z,a,z)"; check "$output" "count=2 items=a,z"
  usage_failure "C17" "$BUILD/batch_plan" --items ../x
  pass "C17"
else skip "compilador C ausente"; fi

if command -v node >/dev/null; then
  node --test "$ROOT/exemplos/javascript/batch-plan.test.mjs"
  output="$(node "$ROOT/exemplos/javascript/batch-plan.mjs" --items z,a,z)"; check "$output" "count=2 items=a,z"
  usage_failure "JavaScript" node "$ROOT/exemplos/javascript/batch-plan.mjs" --items ../x
  pass "JavaScript"
else skip "Node.js ausente"; fi

if command -v dotnet >/dev/null; then
  major="$(dotnet --version | cut -d. -f1)"
  if [[ "$major" =~ ^[0-9]+$ ]] && ((major >= 10)); then
    output="$(dotnet run --project "$ROOT/exemplos/csharp/BatchPlan.csproj" --configuration Release --artifacts-path "$BUILD/dotnet" -- --items z,a,z)"
    check "$output" "count=2 items=a,z"
    usage_failure "C#" dotnet run --project "$ROOT/exemplos/csharp/BatchPlan.csproj" --configuration Release --no-restore --artifacts-path "$BUILD/dotnet" -- --items ../x
    pass "C#"
  else skip ".NET 10+ necessario; encontrado $(dotnet --version)"; fi
else skip ".NET SDK ausente"; fi

if command -v ruff >/dev/null; then
  ruff check "$ROOT/exemplos/python" "$ROOT/projetos/fileflow/src" "$ROOT/projetos/fileflow/tests"
  ruff format --check "$ROOT/exemplos/python" "$ROOT/projetos/fileflow/src" "$ROOT/projetos/fileflow/tests"
  pass "Ruff"
else skip "Ruff ausente"; fi
printf '\nResultado: %d passaram; %d ignoradas por falta de toolchain.\n' "$passed" "$skipped"
