#!/usr/bin/env bash
# ============================================================================
# rte_common.sh - Biblioteca compartilhada dos scripts Bash do RedTeam-Essentials
#
# Uso (em qualquer script .sh):
#   #!/usr/bin/env bash
#   set -euo pipefail
#   SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
#   # shellcheck source=/dev/null
#   source "$SCRIPT_DIR/../lib/bash/rte_common.sh"
#
# Recursos:
#   * Logging colorido com niveis (DEBUG/INFO/WARN/ERROR/FATAL)
#   * Trap de cleanup e ERR
#   * Helpers de validacao (dominio, IP, root, comando)
#   * Confirmacao de autorizacao etica
#   * Funcoes utilitarias (require_cmd, run_cmd com --dry-run)
#
# Autor:   Samuel Ziger - RedTeam Essentials
# Versao:  2.0.0
# Licenca: MIT
# ============================================================================

# --- Cores -----------------------------------------------------------------
if [[ -t 1 ]]; then
    RTE_RED=$'\033[0;31m'
    RTE_GREEN=$'\033[0;32m'
    RTE_YELLOW=$'\033[1;33m'
    RTE_BLUE=$'\033[0;34m'
    RTE_CYAN=$'\033[0;36m'
    RTE_GRAY=$'\033[0;90m'
    RTE_BOLD=$'\033[1m'
    RTE_RST=$'\033[0m'
else
    RTE_RED='' RTE_GREEN='' RTE_YELLOW='' RTE_BLUE='' RTE_CYAN=''
    RTE_GRAY='' RTE_BOLD='' RTE_RST=''
fi

# --- Nivel de log ----------------------------------------------------------
declare -A RTE_LOG_LEVELS=( [DEBUG]=0 [INFO]=1 [WARN]=2 [ERROR]=3 [FATAL]=4 )
RTE_CURRENT_LEVEL="${RTE_LOG_LEVEL:-INFO}"
RTE_LOG_FILE="${RTE_LOG_FILE:-}"

rte::set_log_level() { RTE_CURRENT_LEVEL="${1:-INFO}"; }
rte::set_log_file()  {
    RTE_LOG_FILE="$1"
    mkdir -p "$(dirname "$RTE_LOG_FILE")"
}

rte::log() {
    local level="$1"; shift
    local msg="$*"
    local cur="${RTE_LOG_LEVELS[$RTE_CURRENT_LEVEL]:-1}"
    local lev="${RTE_LOG_LEVELS[$level]:-1}"
    (( lev < cur )) && return 0

    local color glyph
    case "$level" in
        DEBUG)   color="$RTE_GRAY";   glyph="[~]" ;;
        INFO)    color="$RTE_CYAN";   glyph="[*]" ;;
        SUCCESS) color="$RTE_GREEN";  glyph="[+]" ;;
        WARN)    color="$RTE_YELLOW"; glyph="[!]" ;;
        ERROR)   color="$RTE_RED";    glyph="[x]" ;;
        FATAL)   color="$RTE_RED";    glyph="[X]" ;;
        *)       color="$RTE_RST";    glyph="[?]" ;;
    esac

    local stamp; stamp="$(date +'%Y-%m-%d %H:%M:%S')"
    local line="${stamp} ${glyph} ${msg}"
    printf '%b%s%b\n' "$color" "$line" "$RTE_RST" >&2
    [[ -n "$RTE_LOG_FILE" ]] && printf '%s\n' "$line" >> "$RTE_LOG_FILE"
}

rte::debug()   { rte::log DEBUG   "$@"; }
rte::info()    { rte::log INFO    "$@"; }
rte::success() { rte::log SUCCESS "$@"; }
rte::warn()    { rte::log WARN    "$@"; }
rte::error()   { rte::log ERROR   "$@"; }
rte::fatal()   { rte::log FATAL   "$@"; exit 1; }

# --- Banner ----------------------------------------------------------------
rte::banner() {
    local title="${1:-RedTeam Essentials}"
    local version="${2:-2.0.0}"
    local bar; bar="$(printf '=%.0s' {1..64})"
    printf '%b\n%s\n RedTeam Essentials :: %-40s v%s\n%s\n AVISO: Uso apenas educacional/autorizado.\n%s%b\n\n' \
        "$RTE_CYAN" "$bar" "$title" "$version" "$bar" "$bar" "$RTE_RST"
}

# --- Validacoes ------------------------------------------------------------
rte::require_root() {
    if [[ $EUID -ne 0 ]]; then
        rte::fatal "Este script precisa ser executado como root (use sudo)."
    fi
}

rte::require_cmd() {
    local missing=()
    for c in "$@"; do
        command -v "$c" >/dev/null 2>&1 || missing+=("$c")
    done
    if (( ${#missing[@]} > 0 )); then
        rte::fatal "Comandos ausentes: ${missing[*]}"
    fi
}

rte::is_valid_domain() {
    local d="$1"
    [[ "$d" =~ ^([a-zA-Z0-9](-?[a-zA-Z0-9])*\.)+[a-zA-Z]{2,}$ ]]
}

rte::is_valid_ipv4() {
    local ip="$1"
    [[ "$ip" =~ ^([0-9]{1,3}\.){3}[0-9]{1,3}$ ]] || return 1
    IFS='.' read -r -a o <<<"$ip"
    for n in "${o[@]}"; do (( n <= 255 )) || return 1; done
    return 0
}

rte::confirm_authorization() {
    if [[ "${RTE_SKIP_AUTH:-0}" == "1" ]]; then
        rte::warn "Autorizacao pulada (RTE_SKIP_AUTH=1)."
        return 0
    fi
    printf '%b' "$RTE_YELLOW"
    printf 'Voce tem autorizacao por escrito para testar este alvo?\n'
    printf 'Digite AUTORIZADO para prosseguir: '
    printf '%b' "$RTE_RST"
    local ans
    read -r ans
    if [[ "$ans" != "AUTORIZADO" ]]; then
        rte::fatal "Autorizacao nao confirmada. Abortando."
    fi
    rte::success "Autorizacao confirmada."
}

# --- run_cmd com dry-run ---------------------------------------------------
RTE_DRYRUN="${RTE_DRYRUN:-0}"
rte::run() {
    if [[ "$RTE_DRYRUN" == "1" ]]; then
        rte::warn "[DRY-RUN] $*"
        return 0
    fi
    rte::debug "$ $*"
    "$@"
}

# --- Cleanup / trap --------------------------------------------------------
declare -a RTE_CLEANUP=()
rte::add_cleanup() { RTE_CLEANUP+=("$*"); }
rte::__run_cleanup() {
    local rc=$?
    for c in "${RTE_CLEANUP[@]}"; do
        rte::debug "cleanup: $c"
        eval "$c" || true
    done
    return $rc
}
rte::install_traps() {
    trap 'rte::__run_cleanup' EXIT
    trap 'rte::error "Erro na linha $LINENO (codigo $?)"; exit 1' ERR
    trap 'rte::warn "Interrompido pelo usuario."; exit 130' INT
}
