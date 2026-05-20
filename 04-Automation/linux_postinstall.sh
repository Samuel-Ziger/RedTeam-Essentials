#!/usr/bin/env bash
# ============================================================================
# linux_postinstall.sh - Configuracao pos-instalacao para distros pentest
#
# Suporta Debian/Ubuntu/Kali/Parrot. Faz update, instala stack do operador,
# cria estrutura ~/Pentest, baixa wordlists basicas (SecLists), configura
# aliases.
#
# Opcoes:
#   --dry-run           Apenas mostra o que faria.
#   --skip-update       Pula apt update/upgrade.
#   --skip-wordlists    Pula download do SecLists.
#   --extra "pkg1 pkg2" Instala pacotes adicionais.
#   -h | --help         Ajuda.
#
# Exemplo:
#   sudo ./linux_postinstall.sh --extra "ghidra radare2"
#
# Autor:   Samuel Ziger - RedTeam Essentials
# Versao:  2.0.0
# Licenca: MIT
# ============================================================================
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=../lib/bash/rte_common.sh
source "$SCRIPT_DIR/../lib/bash/rte_common.sh"
rte::install_traps

SKIP_UPDATE=0
SKIP_WORDLISTS=0
EXTRA_PKGS=""
while [[ $# -gt 0 ]]; do
    case "$1" in
        --dry-run)        RTE_DRYRUN=1 ;;
        --skip-update)    SKIP_UPDATE=1 ;;
        --skip-wordlists) SKIP_WORDLISTS=1 ;;
        --extra)          EXTRA_PKGS="$2"; shift ;;
        -h|--help)
            grep -E '^# ' "$0" | sed 's/^# //'
            exit 0
            ;;
        *) rte::fatal "Argumento desconhecido: $1" ;;
    esac
    shift
done

rte::banner "Linux Post-Install" "2.0.0"
rte::require_root
rte::require_cmd apt

DISTRO="$(. /etc/os-release && echo "${ID,,}")"
PRETTY="$(. /etc/os-release && echo "$PRETTY_NAME")"
rte::info "Distro detectada: $PRETTY ($DISTRO)"
case "$DISTRO" in
    kali|parrot|debian|ubuntu|pop) ;;
    *) rte::warn "Distro $DISTRO nao testada. Prosseguindo por sua conta e risco." ;;
esac

if (( SKIP_UPDATE == 0 )); then
    rte::info "Atualizando indice de pacotes..."
    rte::run apt-get update -y
    rte::info "Aplicando upgrade..."
    DEBIAN_FRONTEND=noninteractive rte::run apt-get upgrade -y
fi

ESSENTIALS=(
    git vim tmux zsh curl wget jq xclip build-essential
    python3 python3-pip python3-venv golang-go default-jdk
    nmap netcat-openbsd socat tcpdump dnsutils whois traceroute
    hydra john hashcat sqlmap nikto whatweb dirb gobuster
    docker.io docker-compose
    binwalk foremost exiftool
)
rte::info "Instalando pacotes essenciais (${#ESSENTIALS[@]} pkgs)..."
DEBIAN_FRONTEND=noninteractive rte::run apt-get install -y --no-install-recommends "${ESSENTIALS[@]}"

if [[ "$DISTRO" == "kali" || "$DISTRO" == "parrot" ]]; then
    KALI_EXTRAS=(metasploit-framework burpsuite zaproxy bloodhound impacket-scripts crackmapexec responder)
    rte::info "Instalando extras de pentest ${DISTRO^}..."
    DEBIAN_FRONTEND=noninteractive rte::run apt-get install -y --no-install-recommends "${KALI_EXTRAS[@]}" || \
        rte::warn "Alguns extras nao puderam ser instalados (podem nao estar no repo)."
fi

if [[ -n "$EXTRA_PKGS" ]]; then
    rte::info "Instalando extras: $EXTRA_PKGS"
    # shellcheck disable=SC2086
    DEBIAN_FRONTEND=noninteractive rte::run apt-get install -y --no-install-recommends $EXTRA_PKGS
fi

USER_HOME="$(getent passwd "${SUDO_USER:-$USER}" | cut -d: -f6)"
PENTEST="$USER_HOME/Pentest"
rte::info "Criando estrutura em $PENTEST"
for d in Tools Scripts Wordlists Exploits Notes Labs Reports Logs Evidence; do
    rte::run mkdir -p "$PENTEST/$d"
done
rte::run chown -R "${SUDO_USER:-$USER}:${SUDO_USER:-$USER}" "$PENTEST" || true

if (( SKIP_WORDLISTS == 0 )); then
    if [[ -d /usr/share/seclists ]]; then
        rte::info "SecLists ja instalada em /usr/share/seclists"
    else
        rte::info "Clonando SecLists em $PENTEST/Wordlists/SecLists"
        rte::run git clone --depth 1 https://github.com/danielmiessler/SecLists.git \
            "$PENTEST/Wordlists/SecLists" || rte::warn "Falha ao clonar SecLists."
    fi
fi

RCFILE="$USER_HOME/.bashrc"
if [[ -f "$USER_HOME/.zshrc" ]]; then
    RCFILE="$USER_HOME/.zshrc"
fi

if ! grep -q "RTE_ALIASES_START" "$RCFILE" 2>/dev/null; then
    rte::info "Instalando aliases em $RCFILE"
    if [[ "$RTE_DRYRUN" == "1" ]]; then
        rte::warn "[DRY-RUN] aliases pulados"
    else
        cat >> "$RCFILE" <<'RTE_ALIAS_BLOCK'

# >>> RTE_ALIASES_START >>>
alias ll='ls -lah'
alias myip='curl -s ifconfig.me; echo'
alias ports='ss -tulpn'
alias serve='python3 -m http.server 8000'
alias nmapfast='nmap -T4 -F'
alias nmapfull='nmap -sV -sC -p- --min-rate=1000'
# <<< RTE_ALIASES_END <<<
RTE_ALIAS_BLOCK
    fi
fi

rte::info "Limpando cache do apt..."
rte::run apt-get autoremove -y
rte::run apt-get autoclean -y

rte::success "Configuracao concluida."
rte::info "Aplique aliases com: source $RCFILE"
rte::info "Estrutura em: $PENTEST"
