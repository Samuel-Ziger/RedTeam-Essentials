# Lab 02 — Mach-O, dylib e carregamento seguro

## Procedimento

1. Rode os testes de `MachoSummary.py`, inclusive entradas truncadas.
2. Compile `librte_math.dylib` e `dylib_consumer` em diretório temporário.
3. Inspecione header, install name, dependências e símbolos exportados.
4. Execute e confirme `api_version=1` e `sum=42`.
5. Mova o par para outro diretório temporário e repita.
6. Remova a dylib e demonstre falha fechada.

## Limite

Somente a biblioteca compilada no lab é carregada. Não use injection, interpose,
hooking, variáveis `DYLD_*` ou binário de terceiro.
