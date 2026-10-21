# Exemplos executáveis

## Mach-O

`MachoSummary.py` interpreta headers thin e fat/universal com validação de
limites. Ele não executa nem modifica o arquivo.

```bash
python3 MachoSummary.py CAMINHO --pretty
```

## Perfis e baseline

`ProfileAudit.py` inspeciona estrutura de `.mobileconfig` sem instalar. O
comparador de baseline trabalha somente com JSON sintético.

```bash
python3 ProfileAudit.py fixtures/training.mobileconfig --pretty
python3 Compare-RteMacBaseline.py \
  fixtures/desired-baseline.json fixtures/observed-baseline.json --pretty
```

## Dylib em C

A biblioteca exporta apenas soma e versão. O consumidor usa
`@loader_path/librte_math.dylib`, `RTLD_NOW | RTLD_LOCAL`, valida símbolos e não
aceita caminho externo.

```zsh
output=$(mktemp -d)
./dylib/build.zsh "$output"
"$output/dylib_consumer"
```

O exemplo não aborda injection, interposing, hooking ou binários de terceiros.
Execute testes portáteis com `python3 -m unittest discover -s tests -v`.
