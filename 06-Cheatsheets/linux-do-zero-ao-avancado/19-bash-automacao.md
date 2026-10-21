# 19 — Bash e automação robusta

## Objetivos

- preservar limites de argumentos, nomes e registros;
- validar entrada, dependências, pré-condições e códigos de saída;
- produzir automação idempotente com temporários e cleanup seguros;
- testar falhas, concorrência, interrupção e segunda execução.

## Quando usar Bash

Bash é excelente para compor ferramentas do sistema, preparar ambiente e
automatizar fluxos pequenos. Migre para Python ou outra linguagem quando dados
estruturados, concorrência, bibliotecas, testes complexos ou portabilidade fora
de Unix dominarem o problema.

## Esqueleto

```bash
#!/usr/bin/env bash
set -Eeuo pipefail

readonly PROGRAM_NAME="${0##*/}"

usage() {
    printf 'uso: %s DIRETORIO\n' "$PROGRAM_NAME" >&2
}

main() {
    if (( $# != 1 )); then
        usage
        return 2
    fi
    local directory=$1
    [[ -d $directory ]] || {
        printf 'erro: diretorio inexistente: %q\n' "$directory" >&2
        return 1
    }
    find "$directory" -maxdepth 1 -type f -print0
}

main "$@"
```

`errexit` possui exceções em condicionais, listas, substituições e versões;
não substitui tratar falhas esperadas. `nounset` também exige expansões com
default quando ausência é legítima.

## Variáveis e arrays

```bash
nome='arquivo com espaco.txt'
printf '%s\n' "$nome"

arquivos=("um.txt" "dois com espaco.txt")
for arquivo in "${arquivos[@]}"; do
    printf '%s\n' "$arquivo"
done
```

Nunca guarde uma lista de argumentos em string. Use array. Nunca use `eval`
para remontar entrada; mantenha dados como dados.

## Parâmetros

```bash
printf 'script=%s quantidade=%d primeiro=%s\n' "$0" "$#" "${1:-ausente}"
```

- `$@` entre aspas preserva cada argumento;
- `$*` entre aspas junta tudo pelo primeiro caractere de IFS;
- `${x:-padrao}` usa default se vazio/ausente;
- `${x:?mensagem}` exige valor;
- `${x#prefixo}`/`${x%sufixo}` removem padrões.

Use `getopts` para flags curtas portáveis ou parser cuidadoso para flags longas.

## Testes e condições

```bash
if [[ -f $arquivo && -r $arquivo ]]; then
    printf 'legivel: %s\n' "$arquivo"
fi

if (( tentativas >= 3 )); then
    return 1
fi
```

`[[ ... ]]` evita várias expansões perigosas e suporta regex Bash. `[ ... ]` é
o comando `test` e exige quoting cuidadoso. `(( ... ))` é contexto aritmético.

## Ler dados

```bash
while IFS= read -r linha || [[ -n $linha ]]; do
    printf '%s\n' "$linha"
done < arquivo.txt

while IFS= read -r -d '' caminho; do
    printf '%q\n' "$caminho"
done < <(find . -type f -print0)
```

Evite `for x in $(comando)`: substitution remove newlines finais e word
splitting/glob destroem limites.

## Temporários e cleanup

```bash
tmp_dir=$(mktemp -d)
cleanup() {
    local status=$?
    [[ -n ${tmp_dir:-} && -d $tmp_dir ]] && rm -rf -- "$tmp_dir"
    exit "$status"
}
trap cleanup EXIT
trap 'exit 130' INT
trap 'exit 143' TERM
```

`mktemp` evita corrida previsível. O cleanup valida o alvo. Handlers devem ser
simples; sinais chegam entre operações.

## Idempotência

Um script idempotente converge para o estado desejado:

```bash
install -d -m 0750 -- "$destino"
if ! cmp -s -- "$origem" "$destino/config"; then
    install -m 0640 -- "$origem" "$destino/config.novo"
    mv -f -- "$destino/config.novo" "$destino/config"
fi
```

Valide configuração antes do `mv`. O rename é atômico apenas dentro do mesmo
filesystem e não torna toda a operação transacional.

## Logging

Resultados máquina-legíveis vão para stdout; logs, para stderr ou syslog:

```bash
log() {
    printf '%s level=%s message=%q\n' \
        "$(date --iso-8601=seconds)" "$1" "$2" >&2
}

logger --tag curso-linux -- 'tarefa concluida'
```

Não registre segredos. Inclua timestamp, severidade, operação e correlação.

## Concorrência e locks

```bash
exec 9>"$XDG_RUNTIME_DIR/curso-linux.lock"
flock -n 9 || { printf '%s\n' 'ja esta em execucao' >&2; exit 1; }
```

Lock por arquivo precisa de local, ownership e ciclo de vida corretos. Em rede,
semântica pode variar. systemd também evita instâncias conforme o desenho da
unit.

## Qualidade

```bash
bash -n script.sh
shellcheck script.sh
bash -x script.sh   # pode revelar segredos; somente em dados sintéticos
```

Teste com caminhos vazios, espaços, newline, arquivo iniciado por `-`, permissão
negada, comando ausente, interrupção e segunda execução.

## Exercícios

1. Estenda um exemplo para aceitar opção de simulação e prove que ela não
   modifica o destino.
2. Teste nomes vazios, com espaço, newline e prefixo de hífen sem usar divisão
   de palavras ou avaliação dinâmica.
3. Execute duas instâncias concorrentes de um script com lock e explique quem
   é responsável por remover ou expirar o estado.
4. Injete falha antes e depois da troca final de arquivo; compare estado,
   código de saída, log e cleanup.

## Checklist de domínio

Consigo escrever script que valida entrada, preserva argumentos, trata falha,
limpa temporários, converge de novo e não depende do meu ambiente interativo.
