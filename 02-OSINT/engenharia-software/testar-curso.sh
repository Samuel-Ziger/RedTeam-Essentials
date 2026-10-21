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

if command -v python3 >/dev/null 2>&1; then
  export PYTHONPYCACHEPREFIX="$BUILD_DIR/pycache"
  python3 -m compileall -q "$COURSE_ROOT/exemplos/python"
  (
    cd "$COURSE_ROOT/exemplos/python"
    python3 -m unittest discover -v
  )
  PYTHONPATH="$COURSE_ROOT/projetos/dependency-planner/src" \
    python3 -m unittest discover \
      -s "$COURSE_ROOT/projetos/dependency-planner/tests" -v
  PYTHONPATH="$COURSE_ROOT/projetos/dependency-planner/src" \
    python3 -m dependency_planner.cli \
      "$COURSE_ROOT/projetos/dependency-planner/fixtures/valid-project.json" \
      --format json >"$BUILD_DIR/plan.json"
  python3 -m json.tool "$BUILD_DIR/plan.json" >/dev/null
  pass "Python: exemplo, projeto, testes e CLI"
else
  skip "Python 3 nao encontrado"
fi

if command -v javac >/dev/null 2>&1 && command -v java >/dev/null 2>&1; then
  mkdir -p "$BUILD_DIR/java"
  javac -Xlint:all -Werror -d "$BUILD_DIR/java" \
    "$COURSE_ROOT/exemplos/java/DependencyPlanner.java"
  java -cp "$BUILD_DIR/java" DependencyPlanner
  pass "Java: compilacao e cenarios executaveis"
else
  skip "JDK nao encontrado"
fi

if command -v cc >/dev/null 2>&1; then
  cc -std=c17 -Wall -Wextra -Wpedantic -Werror \
    "$COURSE_ROOT/exemplos/c/dependency_graph.c" \
    -o "$BUILD_DIR/dependency_graph"
  "$BUILD_DIR/dependency_graph"
  pass "C17: compilacao estrita e cenarios executaveis"
else
  skip "compilador C nao encontrado"
fi

if command -v node >/dev/null 2>&1; then
  node --test "$COURSE_ROOT/exemplos/javascript/dependencyGraph.test.mjs"
  pass "JavaScript: testes com node:test"
else
  skip "Node.js nao encontrado"
fi

if command -v dotnet >/dev/null 2>&1; then
  dotnet_major="$(dotnet --version | cut -d. -f1)"
  if [[ "$dotnet_major" =~ ^[0-9]+$ ]] && ((dotnet_major >= 10)); then
    dotnet run \
      --project "$COURSE_ROOT/exemplos/csharp/DependencyPlanner.csproj" \
      --configuration Release \
      --artifacts-path "$BUILD_DIR/dotnet"
    pass "C#: build estrito e cenarios executaveis"
  else
    skip ".NET 10+ necessario; encontrado $(dotnet --version)"
  fi
else
  skip ".NET SDK nao encontrado"
fi

if command -v ruff >/dev/null 2>&1; then
  ruff check \
    "$COURSE_ROOT/exemplos/python" \
    "$COURSE_ROOT/projetos/dependency-planner/src" \
    "$COURSE_ROOT/projetos/dependency-planner/tests"
  ruff format --check \
    "$COURSE_ROOT/exemplos/python" \
    "$COURSE_ROOT/projetos/dependency-planner/src" \
    "$COURSE_ROOT/projetos/dependency-planner/tests"
  pass "Python: lint e formatacao"
else
  skip "Ruff nao encontrado"
fi

printf '\nResultado: %d verificacoes passaram; %d foram ignoradas por falta de toolchain.\n' \
  "$passed" "$skipped"
