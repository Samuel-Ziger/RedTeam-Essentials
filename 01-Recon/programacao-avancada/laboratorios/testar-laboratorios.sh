#!/usr/bin/env bash
set -euo pipefail

RUN_POSTGRES=1
RUN_MONGO=1

usage() {
  cat <<'EOF'
Uso: testar-laboratorios.sh [--postgres-only | --mongo-only]

Cria um projeto Docker Compose efêmero, executa setup, consultas e asserções e
remove contêineres, rede e volumes ao terminar. Nenhuma porta é publicada.
EOF
}

while (( $# > 0 )); do
  case "$1" in
    --postgres-only)
      RUN_POSTGRES=1
      RUN_MONGO=0
      ;;
    --mongo-only)
      RUN_POSTGRES=0
      RUN_MONGO=1
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

LAB_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_NAME="rte-m01-labs-$$"
COMPOSE=(docker compose --project-name "$PROJECT_NAME" --file "$LAB_DIR/compose.yaml")

fail() {
  printf '[FALHA] %s\n' "$1" >&2
  exit 1
}
pass() { printf '[OK] %s\n' "$1"; }

if ! command -v docker >/dev/null 2>&1 || ! docker compose version >/dev/null 2>&1; then
  fail 'Docker com Compose v2 é obrigatório'
fi

mongo_kernel_is_unsupported() {
  local release major minor patch
  release="$(uname -r)"
  IFS=. read -r major minor patch _ <<<"$release"
  patch="${patch%%[^0-9]*}"
  patch="${patch:-0}"
  if [[ "$major" =~ ^[0-9]+$ && "$minor" =~ ^[0-9]+$ && "$patch" =~ ^[0-9]+$ ]]; then
    (( major == 6 && minor >= 19 )) && return 0
    (( major == 7 && minor == 0 && patch <= 13 )) && return 0
  fi
  return 1
}

if (( RUN_MONGO )) && mongo_kernel_is_unsupported; then
  fail "MongoDB é incompatível com o kernel $(uname -r); use --postgres-only ou um host fora do intervalo 6.19–7.0.13"
fi

cleanup() {
  "${COMPOSE[@]}" down --volumes --remove-orphans >/dev/null 2>&1 || true
}
trap cleanup EXIT INT TERM

services=()
(( RUN_POSTGRES )) && services+=(postgres)
(( RUN_MONGO )) && services+=(mongo)
"${COMPOSE[@]}" config --quiet
"${COMPOSE[@]}" up --detach --wait "${services[@]}"

if (( RUN_POSTGRES )); then
  for script in 001_schema.sql 002_seed.sql 003_queries.sql 004_assertions.sql; do
    "${COMPOSE[@]}" exec --no-TTY postgres \
      psql --set=ON_ERROR_STOP=1 --username=course --dbname=course \
      --file="/course/$script"
  done
  pass 'PostgreSQL: schema, dados, consultas, constraints e resultados'
fi

if (( RUN_MONGO )); then
  for script in 001_setup.js 002_queries.js 003_assertions.js; do
    "${COMPOSE[@]}" exec --no-TTY mongo \
      mongosh --quiet --file="/course/$script"
  done
  pass 'MongoDB: validator, índices, consultas, agregação e resultados'
fi

pass 'laboratórios concluídos; recursos efêmeros serão removidos'
