#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/../.." && pwd)"
BUILD="$(mktemp -d)"
trap 'rm -rf "$BUILD"' EXIT
SOURCE="$ROOT/28-Engenharia-Ferramentas-Seguranca/acervo/java/src/main/java/io/redteam/essentials/PayloadGenerator.java"

javac_version="$(javac -version 2>&1 | awk '{print $2}')"
javac_major="${javac_version%%.*}"
java_version="$(java -version 2>&1 | awk -F '[".]' 'NR == 1 {print $2}')"

if [[ "$javac_major" =~ ^[0-9]+$ ]] && (( javac_major >= 17 )); then
  javac -Xlint:all -Werror -d "$BUILD" "$SOURCE"
  runner=(java -cp "$BUILD" io.redteam.essentials.PayloadGenerator)
elif [[ "$java_version" =~ ^[0-9]+$ ]] && (( java_version >= 17 )); then
  printf '[INFO] javac %s abaixo do requisito; usando source-file mode do Java %s.\n' \
    "$javac_version" "$java_version"
  runner=(java "$SOURCE")
else
  printf '[FALHA] Java 17+ necessario (javac=%s, java=%s).\n' \
    "$javac_version" "${java_version:-desconhecido}" >&2
  exit 1
fi

list="$("${runner[@]}" --list)"
for type in xss sqli cmdi ssti ssrf lfi xxe; do
  grep -Eq "^${type}[[:space:]]+[1-9][0-9]* payloads$" <<<"$list"
done

output="$("${runner[@]}" --type xss --count 2 --encode b64)"
[[ "$(wc -l <<<"$output")" -eq 2 ]]
grep -Eq '^[A-Za-z0-9+/]+={0,2}$' <<<"$output"

if "${runner[@]}" --type inexistente >/dev/null 2>&1; then
  printf '[FALHA] tipo inválido deveria retornar erro.\n' >&2
  exit 1
fi
for args in \
  '--type xss --count 0' \
  '--type xss --count nao-numero' \
  '--type xss --encode desconhecido' \
  '--type'; do
  # A expansao intencional simula argumentos separados para a CLI.
  # shellcheck disable=SC2086
  if "${runner[@]}" $args >/dev/null 2>&1; then
    printf '[FALHA] argumentos invalidos deveriam retornar erro: %s\n' "$args" >&2
    exit 1
  fi
done
printf '[OK] testes Java offline concluídos.\n'
