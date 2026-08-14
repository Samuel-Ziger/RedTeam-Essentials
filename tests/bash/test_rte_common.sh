#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/../.." && pwd)"
# shellcheck source=../../lib/bash/rte_common.sh
source "$ROOT/lib/bash/rte_common.sh"

failures=0
assert_success() { "$@" || { printf '[FALHA] esperava sucesso: %s\n' "$*" >&2; failures=$((failures + 1)); }; }
assert_failure() { if "$@"; then printf '[FALHA] esperava falha: %s\n' "$*" >&2; failures=$((failures + 1)); fi; }

assert_success rte::is_valid_domain example.com
assert_success rte::is_valid_domain api.lab.example.org
assert_failure rte::is_valid_domain localhost
assert_failure rte::is_valid_domain --invalid.example
assert_success rte::is_valid_ipv4 127.0.0.1
assert_success rte::is_valid_ipv4 255.255.255.255
assert_failure rte::is_valid_ipv4 256.0.0.1
assert_failure rte::is_valid_ipv4 1.2.3

RTE_DRYRUN=1
marker="$(mktemp)"
rm -f "$marker"
assert_success rte::run touch "$marker"
[[ ! -e "$marker" ]] || { printf '[FALHA] dry-run executou o comando\n' >&2; failures=$((failures + 1)); }

RTE_SKIP_AUTH=1
assert_success rte::confirm_authorization

log_dir="$(mktemp -d)"
rte::set_log_file "$log_dir/rte.log"
rte::info "teste offline"
grep -Fq 'teste offline' "$log_dir/rte.log" || failures=$((failures + 1))
rm -rf "$log_dir"

if (( failures > 0 )); then
  printf '%d teste(s) Bash falharam.\n' "$failures" >&2
  exit 1
fi
printf '[OK] testes Bash offline concluídos.\n'

