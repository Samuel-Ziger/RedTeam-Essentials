# 13 — Terminal, zsh e composição de comandos

Terminal hospeda um shell; zsh interpreta palavras, expansões, redirecionamentos
e pipelines. Um comando bem escrito declara entradas, saídas e erro.

```zsh
printf '%s\n' "$PATH"
command -v plutil
find "$HOME/Documents/fixture" -type f -print
```

Use aspas em variáveis de caminho, `--` quando a ferramenta aceita, e verifique
código de saída. `>` substitui; `>>` acrescenta. Em pipeline, cada processo tem
status e pode falhar. Scripts do curso usam `set -euo pipefail` quando compatível.

Aliases são conveniência interativa; funções e scripts versionados são mais
auditáveis. Não modifique `PATH` para colocar diretórios graváveis antes de
binários do sistema.

## Prática

Liste arquivos de uma fixture, filtre por extensão, calcule SHA-256 e grave um
relatório. Repita com nome contendo espaço e hífen inicial sem quebrar quoting.
