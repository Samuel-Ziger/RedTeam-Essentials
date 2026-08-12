#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
COMPOSE_FILE="${SCRIPT_DIR}/docker-compose.yml"
CONFIG_ONLY=false

if [[ "${1:-}" == "--config-only" ]]; then
  CONFIG_ONLY=true
elif [[ $# -gt 0 ]]; then
  printf 'Uso: %s [--config-only]\n' "$0" >&2
  exit 2
fi

failures=0
pass() { printf '[OK] %s\n' "$1"; }
fail() { printf '[FALHA] %s\n' "$1" >&2; failures=$((failures + 1)); }

if ! command -v docker >/dev/null 2>&1; then
  fail 'Docker nao encontrado no PATH.'
  exit 1
fi
if ! docker compose version >/dev/null 2>&1; then
  fail 'Plugin Docker Compose v2 indisponivel.'
  exit 1
fi
pass "$(docker compose version)"

if docker compose -f "$COMPOSE_FILE" config --quiet; then
  pass 'Configuracao Compose valida.'
else
  fail 'Configuracao Compose invalida.'
fi

if $CONFIG_ONLY; then
  exit "$failures"
fi

if ! docker info >/dev/null 2>&1; then
  fail 'Docker daemon inacessivel.'
  exit 1
fi

mapfile -t running < <(docker compose -f "$COMPOSE_FILE" ps --services --status running)
if (( ${#running[@]} == 0 )); then
  fail 'Nenhum servico em execucao.'
fi
for service in "${running[@]}"; do
  status="$(docker inspect --format '{{if .State.Health}}{{.State.Health.Status}}{{else}}sem-healthcheck{{end}}' "$(docker compose -f "$COMPOSE_FILE" ps -q "$service")")"
  if [[ "$status" == "healthy" ]]; then
    pass "Servico saudavel: $service"
  else
    fail "Servico $service com estado: $status"
  fi
done

declare -A endpoints=(
  [dvwa]='http://127.0.0.1:8081'
  [juiceshop]='http://127.0.0.1:8082'
  [bwapp]='http://127.0.0.1:8083'
  [webgoat]='http://127.0.0.1:8084'
  [vulnerable-wordpress]='http://127.0.0.1:8085'
  [nodegoat]='http://127.0.0.1:8086'
  [vampi]='http://127.0.0.1:8087'
)

if command -v curl >/dev/null 2>&1; then
  for service in "${running[@]}"; do
    [[ -n "${endpoints[$service]:-}" ]] || continue
    if curl --fail --silent --show-error --location --max-time 5 --output /dev/null "${endpoints[$service]}"; then
      pass "HTTP respondeu: $service (${endpoints[$service]})"
    else
      fail "HTTP sem resposta: $service (${endpoints[$service]})"
    fi
  done
else
  fail 'curl indisponivel; smoke tests HTTP nao executados.'
fi

exit "$failures"
