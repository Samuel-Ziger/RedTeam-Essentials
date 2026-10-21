#!/usr/bin/env bash
# Inicia a interface local de estudos sem expor o Vite na rede.

set -Eeuo pipefail

readonly ROOT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
readonly APP_DIR="${ROOT_DIR}/study-app"
readonly GENERATOR="${APP_DIR}/scripts/build_catalog.py"
readonly VALIDATOR="${ROOT_DIR}/scripts/validate_study_app.py"
readonly HOST="127.0.0.1"

PORT="${ESTUDO_PORT:-5173}"
START_TIMEOUT="${ESTUDO_START_TIMEOUT:-30}"
OPEN_BROWSER=1
CHECK_ONLY=0
SERVER_PID=""

usage() {
  cat <<'EOF'
Uso: bash estudo.sh [opcoes]

Inicia a aplicacao visual do RedTeam Essentials apenas no computador local.

Opcoes:
  --port PORTA  Porta local do Vite (padrao: 5173 ou $ESTUDO_PORT)
  --no-open     Nao abrir o navegador automaticamente
  --check       Verificar pre-requisitos e arquivos sem instalar ou iniciar
  -h, --help    Mostrar esta ajuda

Variaveis opcionais:
  ESTUDO_PORT             Porta local, equivalente a --port
  ESTUDO_START_TIMEOUT    Espera pelo servidor em segundos (padrao: 30)
EOF
}

fail() {
  printf '[ERRO] %s\n' "$*" >&2
  exit 1
}

is_integer_in_range() {
  local value="$1"
  local minimum="$2"
  local maximum="$3"
  [[ "${value}" =~ ^[0-9]+$ ]] &&
    ((10#${value} >= minimum && 10#${value} <= maximum))
}

while (($# > 0)); do
  case "$1" in
    --port)
      (($# >= 2)) || fail "--port exige um valor"
      PORT="$2"
      shift 2
      ;;
    --port=*)
      PORT="${1#*=}"
      shift
      ;;
    --no-open)
      OPEN_BROWSER=0
      shift
      ;;
    --check)
      CHECK_ONLY=1
      shift
      ;;
    -h | --help)
      usage
      exit 0
      ;;
    *)
      fail "opcao desconhecida: $1 (use --help)"
      ;;
  esac
done

is_integer_in_range "${PORT}" 1 65535 || fail "porta invalida: ${PORT}"
is_integer_in_range "${START_TIMEOUT}" 1 300 ||
  fail "ESTUDO_START_TIMEOUT deve estar entre 1 e 300 segundos"
PORT=$((10#${PORT}))
START_TIMEOUT=$((10#${START_TIMEOUT}))

require_command() {
  local command_name="$1"
  local install_hint="$2"
  command -v "${command_name}" >/dev/null 2>&1 ||
    fail "${command_name} nao encontrado. ${install_hint}"
}

check_node_version() {
  local version major minor supported=0
  version="$(node --version)"
  version="${version#v}"
  IFS=. read -r major minor _ <<<"${version}"
  if ! [[ "${major}" =~ ^[0-9]+$ && "${minor}" =~ ^[0-9]+$ ]]; then
    fail "nao foi possivel interpretar a versao do Node.js: ${version}"
  fi
  if ((major == 22 && minor >= 12)); then
    supported=1
  elif ((major > 22 && major % 2 == 0)); then
    supported=1
  fi
  ((supported == 1)) ||
    fail "Node.js suportado: 22.12+ ou linha par posterior ainda suportada; encontrado ${version}"
  printf '[OK] Node.js %s\n' "${version}"
}

check_environment() {
  local python_version
  require_command python3 "Instale Python 3 pelo gerenciador da sua distribuicao."
  require_command node "Instale Node.js 22.12+ ou uma linha par posterior ainda suportada."
  require_command npm "Instale o npm que acompanha o Node.js."
  check_node_version

  [[ -f "${APP_DIR}/package.json" ]] || fail "study-app/package.json nao encontrado"
  [[ -f "${APP_DIR}/package-lock.json" ]] || fail "study-app/package-lock.json nao encontrado"
  [[ -f "${GENERATOR}" ]] || fail "gerador de catalogo nao encontrado: ${GENERATOR}"
  [[ -f "${VALIDATOR}" ]] || fail "validador da aplicacao nao encontrado: ${VALIDATOR}"
  python_version="$(python3 --version 2>&1)"
  printf '[OK] %s e npm %s\n' "${python_version}" "$(npm --version)"
}

SERVER_PID=""
cleanup() {
  local exit_status=$?
  trap - EXIT
  if [[ -n "${SERVER_PID}" ]] && kill -0 "${SERVER_PID}" 2>/dev/null; then
    printf '\n[INFO] Encerrando o servidor local...\n'
    kill "${SERVER_PID}" 2>/dev/null || true
    wait "${SERVER_PID}" 2>/dev/null || true
  fi
  exit "${exit_status}"
}
trap cleanup EXIT
trap 'exit 130' INT
trap 'exit 143' TERM

open_browser() {
  local url="$1"
  local candidate
  for candidate in google-chrome-stable google-chrome chromium chromium-browser; do
    if command -v "${candidate}" >/dev/null 2>&1; then
      "${candidate}" "${url}" >/dev/null 2>&1 &
      printf '[OK] Navegador aberto com %s\n' "${candidate}"
      return 0
    fi
  done
  if command -v xdg-open >/dev/null 2>&1; then
    xdg-open "${url}" >/dev/null 2>&1 &
    printf '[OK] Navegador aberto com xdg-open\n'
    return 0
  fi
  if [[ "$(uname -s)" == "Darwin" ]] && command -v open >/dev/null 2>&1; then
    open -a "Google Chrome" "${url}" >/dev/null 2>&1 &
    printf '[OK] Navegador aberto com Google Chrome\n'
    return 0
  fi
  printf '[AVISO] Nao encontrei Chrome, Chromium ou xdg-open. Abra: %s\n' "${url}" >&2
}

wait_for_server() {
  local url="$1"
  local started_at="${SECONDS}"
  local server_status=0
  while ((SECONDS - started_at < START_TIMEOUT)); do
    if ! kill -0 "${SERVER_PID}" 2>/dev/null; then
      wait "${SERVER_PID}" || server_status=$?
      SERVER_PID=""
      fail "o Vite encerrou antes de responder (codigo ${server_status})"
    fi
    if python3 - "${url}" <<'PY' >/dev/null 2>&1
import sys
import urllib.request

try:
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
    with opener.open(sys.argv[1], timeout=0.5) as response:
        raise SystemExit(0 if 200 <= response.status < 400 else 1)
except Exception:
    raise SystemExit(1)
PY
    then
      return 0
    fi
    sleep 0.25
  done
  fail "o servidor nao respondeu em ${START_TIMEOUT}s: ${url}"
}

check_environment
python3 "${VALIDATOR}"

if ((CHECK_ONLY == 1)); then
  printf '[OK] Ambiente pronto. Nenhuma dependencia foi instalada e nenhum servidor foi iniciado.\n'
  exit 0
fi

printf '[INFO] Gerando o catalogo a partir dos Markdown do repositorio...\n'
python3 "${GENERATOR}" --repo-root "${ROOT_DIR}"
[[ -f "${APP_DIR}/public/generated/catalog.json" ]] ||
  fail "o gerador nao produziu public/generated/catalog.json"

needs_install=0
if [[ ! -d "${APP_DIR}/node_modules" ]]; then
  needs_install=1
elif ! (cd "${APP_DIR}" && npm ls --depth=0 --silent >/dev/null 2>&1); then
  printf '[AVISO] Dependencias locais ausentes ou divergentes do package.json.\n'
  needs_install=1
fi

if ((needs_install == 1)); then
  printf '[INFO] Instalando dependencias reproduziveis com npm ci...\n'
  (cd "${APP_DIR}" && npm ci --ignore-scripts)
else
  printf '[OK] Dependencias locais instaladas e consistentes.\n'
fi

[[ -x "${APP_DIR}/node_modules/.bin/vite" ]] ||
  fail "Vite ausente em node_modules; execute 'cd study-app && npm ci --ignore-scripts'"

readonly URL="http://${HOST}:${PORT}/"
printf '[INFO] Iniciando em %s (somente loopback)...\n' "${URL}"
(
  cd "${APP_DIR}"
  exec ./node_modules/.bin/vite --host "${HOST}" --port "${PORT}" --strictPort
) &
SERVER_PID=$!

wait_for_server "${URL}"
printf '[OK] Aplicacao pronta: %s\n' "${URL}"
if ((OPEN_BROWSER == 1)); then
  open_browser "${URL}"
fi
printf '[INFO] Pressione Ctrl+C para encerrar.\n'

server_status=0
wait "${SERVER_PID}" || server_status=$?
SERVER_PID=""
exit "${server_status}"
