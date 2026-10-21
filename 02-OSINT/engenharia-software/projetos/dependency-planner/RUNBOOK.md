# Runbook local — Dependency Planner

## Verificação rápida

Na raiz do repositório:

```bash
bash 02-OSINT/engenharia-software/testar-curso.sh
```

Somente o projeto Python:

```bash
COURSE=02-OSINT/engenharia-software/projetos/dependency-planner
PYTHONPATH="$COURSE/src" python3 -m unittest discover -s "$COURSE/tests" -v
PYTHONPATH="$COURSE/src" python3 -m dependency_planner.cli \
  "$COURSE/fixtures/valid-project.json" --format json
```

Resultado válido retorna status `0`, escreve somente em `stdout` e inclui
`order`, `batches`, `critical_path` e `minimum_duration`. Erro esperado retorna
status `2`, deixa `stdout` vazio e escreve mensagem curta em `stderr`.

## Triagem

| Sintoma | Primeira verificação | Evidência |
|---|---|---|
| `No module named dependency_planner` | `PYTHONPATH` aponta para `src`? | comando/diretório |
| arquivo não encontrado | caminho relativo parte de qual diretório? | caminho absoluto temporário |
| `JSON invalido` | encoding, linha e coluna | fixture mínimo sanitizado |
| dependência desconhecida | ID existe exatamente, inclusive caixa/espaço? | item e referência |
| ciclo | caminho fecha no mesmo ID? | `A -> ... -> A` |
| ordem inesperada | propriedade ou desempate foi violado? | arestas + posições |
| lentidão | valores de `V`, `E` e forma do grafo | benchmark reproduzível |

Use o [guia de diagnóstico do curso](../../GUIA-DIAGNOSTICO.md) para investigação
completa.

## Recuperação e rollback

O programa é somente leitura e não mantém estado. Preserve o arquivo original,
reexecute a versão anterior do código e compare propriedades/saída. Não use
`git reset --hard` para recuperar uma mudança local; salve o diff ou trabalhe em
branch e reverta o commit específico.

## Escalonamento

Ao relatar defeito, inclua versão, runtime, comando, fixture mínimo, status,
canais de saída e primeira propriedade violada. Remova nomes/dados reais. Não
inclua arquivos completos quando um subgrafo pequeno reproduz a falha.

