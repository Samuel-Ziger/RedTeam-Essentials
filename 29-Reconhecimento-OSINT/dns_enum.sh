#!/usr/bin/env bash
# ============================================================================
# dns_enum.sh - Enumeracao DNS passiva via dig + crt.sh
#
# Alternativa Linux do dns_enum.ps1. Coleta A, AAAA, MX, NS, TXT, SOA,
# CNAME e SRV, opcionalmente faz subdomain enum via Certificate Transparency
# e consulta WHOIS. Saida em JSON estruturado.
#
# Uso:
#   ./dns_enum.sh -d exemplo.com [--subs] [--whois] [-o out_dir] [--dry-run]
#
# Requisitos: bash 4+, dig (dnsutils), curl, jq.
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

# --- Parse args -------------------------------------------------------------
DOMAIN=""
OUTDIR="./output"
DO_SUBS=0
DO_WHOIS=0
DNS_SERVER=""

usage() {
    cat <<'EOF'
dns_enum.sh - Enumeracao DNS passiva

Opcoes:
  -d, --domain <fqdn>   Dominio alvo (obrigatorio)
  -o, --output  <dir>   Diretorio de saida (default ./output)
  -s, --server  <ip>    Usar servidor DNS especifico
      --subs            Enumerar subdominios via crt.sh
      --whois           Consultar WHOIS
      --dry-run         Apenas mostrar acoes
  -h, --help            Esta ajuda
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -d|--domain) DOMAIN="$2"; shift ;;
        -o|--output) OUTDIR="$2"; shift ;;
        -s|--server) DNS_SERVER="$2"; shift ;;
        --subs)      DO_SUBS=1 ;;
        --whois)     DO_WHOIS=1 ;;
        --dry-run)   RTE_DRYRUN=1 ;;
        -h|--help)   usage; exit 0 ;;
        *) rte::fatal "Argumento desconhecido: $1" ;;
    esac
    shift
done

rte::banner "DNS Enumeration" "2.0.0"

[[ -z "$DOMAIN" ]]                && rte::fatal "Use -d <dominio>"
rte::is_valid_domain "$DOMAIN"    || rte::fatal "Dominio invalido: $DOMAIN"
rte::require_cmd dig curl jq

mkdir -p "$OUTDIR"
STAMP="$(date +%Y%m%d_%H%M%S)"
OUTFILE="$OUTDIR/dns_enum_${DOMAIN}_${STAMP}.json"
SERVER_ARG=""
[[ -n "$DNS_SERVER" ]] && SERVER_ARG="@$DNS_SERVER"

# --- Funcao de query DIG ----------------------------------------------------
query_records() {
    local type="$1"
    rte::info "Consultando registros $type..."
    if [[ "$RTE_DRYRUN" == "1" ]]; then
        echo '[]'; return
    fi
    local out
    # shellcheck disable=SC2086
    out=$(dig +short +time=3 +tries=2 $SERVER_ARG "$type" "$DOMAIN" 2>/dev/null || true)
    if [[ -z "$out" ]]; then
        echo '[]'
    else
        jq -R -s --arg t "$type" 'split("\n") | map(select(length>0)) | map({type:$t, value:.})' <<<"$out"
    fi
}

# --- Subdominios via crt.sh -------------------------------------------------
query_subs() {
    if [[ "$RTE_DRYRUN" == "1" ]]; then
        echo '[]'; return
    fi
    rte::info "Consultando crt.sh ..."
    local raw
    raw=$(curl -s --max-time 30 -A "RTE-DNS-Enum/2.0" "https://crt.sh/?q=%25.${DOMAIN}&output=json" || echo "[]")
    if [[ -z "$raw" || "$raw" == *"<html"* ]]; then
        rte::warn "crt.sh sem resposta JSON"; echo '[]'; return
    fi
    jq -r --arg d "$DOMAIN" '
        .[] | .name_value | split("\n")[]
    ' <<<"$raw" 2>/dev/null \
        | sed 's/^\*\.//' \
        | tr '[:upper:]' '[:lower:]' \
        | grep -E "\.${DOMAIN}\$" \
        | sort -u \
        | jq -R . | jq -s .
}

# --- WHOIS ------------------------------------------------------------------
query_whois() {
    if [[ "$RTE_DRYRUN" == "1" ]]; then
        echo '""'; return
    fi
    if ! command -v whois >/dev/null 2>&1; then
        rte::warn "whois nao instalado, pulando."
        echo '""'; return
    fi
    rte::info "Consultando WHOIS..."
    local txt; txt="$(whois "$DOMAIN" 2>/dev/null | head -n 100 || true)"
    jq -R -s . <<<"$txt"
}

# --- Coleta principal -------------------------------------------------------
A=$(query_records A)
AAAA=$(query_records AAAA)
MX=$(query_records MX)
NS=$(query_records NS)
TXT=$(query_records TXT)
SOA=$(query_records SOA)
CNAME=$(query_records CNAME)
SRV=$(query_records SRV)

SUBS='[]'
[[ $DO_SUBS -eq 1 ]] && SUBS=$(query_subs)

WHOIS='""'
[[ $DO_WHOIS -eq 1 ]] && WHOIS=$(query_whois)

# --- Monta JSON final -------------------------------------------------------
if [[ "$RTE_DRYRUN" == "1" ]]; then
    rte::warn "[DRY-RUN] saida nao escrita."
    exit 0
fi

jq -n \
    --arg domain "$DOMAIN" \
    --arg ts "$(date -Iseconds)" \
    --arg dns "${DNS_SERVER:-system-default}" \
    --argjson A "$A" \
    --argjson AAAA "$AAAA" \
    --argjson MX "$MX" \
    --argjson NS "$NS" \
    --argjson TXT "$TXT" \
    --argjson SOA "$SOA" \
    --argjson CNAME "$CNAME" \
    --argjson SRV "$SRV" \
    --argjson subs "$SUBS" \
    --argjson whois "$WHOIS" \
    '{
        metadata: { tool:"dns_enum.sh", version:"2.0.0", target:$domain, timestamp:$ts, dns_server:$dns },
        records:  { A:$A, AAAA:$AAAA, MX:$MX, NS:$NS, TXT:$TXT, SOA:$SOA, CNAME:$CNAME, SRV:$SRV },
        subdomains: $subs,
        whois:    $whois,
        summary: {
            totalRecords:   ([$A,$AAAA,$MX,$NS,$TXT,$SOA,$CNAME,$SRV] | flatten | length),
            subdomainCount: ($subs | length)
        }
    }' > "$OUTFILE"

rte::success "Saida: $OUTFILE"
