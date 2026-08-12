#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/../.." && pwd)"
BUILD="$(mktemp -d)"
trap 'rm -rf "$BUILD"' EXIT

javac -Xlint:all -Werror -d "$BUILD" \
  "$ROOT/12-Java-Tools/src/main/java/io/redteam/essentials/PayloadGenerator.java"

list="$(java -cp "$BUILD" io.redteam.essentials.PayloadGenerator --list)"
for type in xss sqli cmdi ssti ssrf lfi xxe; do
  grep -Eq "^${type}[[:space:]]+[1-9][0-9]* payloads$" <<<"$list"
done

output="$(java -cp "$BUILD" io.redteam.essentials.PayloadGenerator --type xss --count 2 --encode b64)"
[[ "$(wc -l <<<"$output")" -eq 2 ]]
grep -Eq '^[A-Za-z0-9+/]+={0,2}$' <<<"$output"

if java -cp "$BUILD" io.redteam.essentials.PayloadGenerator --type inexistente >/dev/null 2>&1; then
  printf '[FALHA] tipo inválido deveria retornar erro.\n' >&2
  exit 1
fi
printf '[OK] testes Java offline concluídos.\n'

