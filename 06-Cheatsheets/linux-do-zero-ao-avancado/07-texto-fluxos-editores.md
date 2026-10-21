# 07 — Fluxos, texto, regex e editores

## Objetivos

- controlar entrada, saída, erro e código de retorno em pipelines;
- selecionar ferramentas de texto sem confundir linhas com registros arbitrários;
- distinguir BRE, ERE e a gramática de formatos estruturados;
- editar e validar configurações sem perder a versão anterior.

## Os três fluxos padrão

Todo processo normalmente recebe descritores:

| FD | Nome | Uso |
|----|------|-----|
| 0 | stdin | entrada |
| 1 | stdout | resultado |
| 2 | stderr | diagnóstico |

```bash
comando >saida.txt 2>erro.txt
comando >>saida.txt 2>>erro.txt
comando >tudo.txt 2>&1
comando </caminho/entrada.txt
```

A ordem importa: redirecionamentos são avaliados da esquerda para a direita.
`2>&1` faz FD 2 apontar para o destino atual de FD 1.

## Pipelines

```bash
printf '%s\n' banana pera banana maca |
    sort |
    uniq -c |
    sort -nr
```

Um pipe conecta stdout de um processo ao stdin do seguinte. Por padrão, Bash
retorna o status do último comando; `set -o pipefail` torna falhas anteriores
visíveis. `tee` duplica um fluxo para arquivo e stdout:

```bash
printf '%s\n' alpha beta | tee resultado.txt | wc -l
```

## Ferramentas fundamentais

| Ferramenta | Pergunta que responde |
|------------|-----------------------|
| `cat` | qual é o fluxo completo? |
| `less` | como navegar sem carregar tudo na tela? |
| `head`/`tail` | como ver começo/fim? |
| `wc` | quantas linhas, palavras ou bytes? |
| `cut` | quais campos por delimitador/posição? |
| `sort`/`uniq` | como ordenar e agregar iguais adjacentes? |
| `tr` | como traduzir/remover caracteres? |
| `grep` | quais linhas correspondem? |
| `sed` | como transformar um fluxo por regras? |
| `awk` | como selecionar campos, calcular e relatar? |

Exemplo com dados sintéticos:

```bash
printf '%s\n' \
  '2026-09-30 INFO api iniciou' \
  '2026-09-30 ERROR banco indisponivel' \
  '2026-09-30 INFO api recuperou' |
awk '$2 == "ERROR" { erros++; print $0 } END { print "erros=" erros > "/dev/stderr" }'
```

## Expressões regulares

Regex descreve texto, não estrutura arbitrária. Em uma ERE:

- `^` e `$`: início e fim;
- `.`: qualquer caractere;
- `[0-9]`: classe;
- `*`, `+`, `?`: quantidade;
- `{m,n}`: intervalo de quantidade;
- `(...)`: grupo;
- `a|b`: alternativa.

```bash
printf '%s\n' INFO ERROR WARN ERROR42 |
grep -E '^(ERROR|WARN)$'
```

Use aspas simples ao passar regex fixa para evitar expansão da shell. BRE,
ERE e regex de linguagens diferem; não transfira sintaxe sem conferir.

## Delimitadores corretos

Linhas funcionam para texto cuja unidade não contém newline. Para nomes de
arquivo, use NUL:

```bash
find . -maxdepth 1 -type f -print0 |
while IFS= read -r -d '' caminho; do
    printf '%q\n' "$caminho"
done
```

JSON, YAML, XML e CSV possuem gramática, escaping e tipos. Use parsers como
`jq`, `yq` apropriado ou bibliotecas, não `grep` para reescrever estrutura.

## Editores

### Nano

Bom para a primeira edição. `Ctrl-O` grava, `Ctrl-X` sai, `Ctrl-W` procura.
Leia a barra inferior: `^` representa Ctrl.

### Vim

Vim é modal. `i` entra em inserção, `Esc` volta ao normal, `:w` grava, `:q`
sai, `/texto` procura, `u` desfaz. Aprenda o suficiente para recuperar uma
configuração quando for o editor disponível.

### Edição administrativa segura

Para sudoers, use `visudo`; para crontab, `crontab -e`. Ferramentas especializadas
validam sintaxe e usam troca controlada. Para outros arquivos, copie, valide e
substitua de forma atômica quando o serviço permitir.

## Codificação e fim de linha

```bash
file arquivo.txt
od -An -tx1 -N32 arquivo.txt
locale charmap
```

LF é o fim de linha comum em Linux; CRLF pode aparecer em arquivos Windows.
Não remova `\r` indiscriminadamente de arquivos binários.

## Exercícios

1. Gere um relatório de contagem por nível a partir de logs sintéticos.
2. Preserve stdout como CSV e envie resumo para stderr.
3. Explique por que `grep ERROR arquivo | wc -l` pode ocultar falha ao abrir o
   arquivo sem `pipefail`.
4. Edite o mesmo arquivo com Nano e Vim e compare backups/swap criados.

## Checklist de domínio

Consigo compor pipelines sem perder erros, escolher delimitador correto e usar
parser quando os dados possuem estrutura.
