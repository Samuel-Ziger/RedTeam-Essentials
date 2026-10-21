# Laboratório 03 — Resiliência, concorrência e documentos

## Objetivo

Adicionar controle de carga e uma saída de relatório sem transformar falhas
transitórias em tempestade ou dado em fórmula.

## Etapa A — retry policy

Crie policy com classificador, maxAttempts, deadline, full jitter, Retry-After e
cancelamento. Injete clock, RNG e sleeper. Escrita com resultado incerto deve
reconciliar antes de repetir.

## Etapa B — fila limitada

Implemente N workers e fila de capacidade M. Meça 1, 2, 4 e 8 workers contra fake
com latência/rate limit configuráveis. Registre throughput, p95, retries, 429, fila
e memória aproximada.

## Etapa C — falha e cancelamento

Teste fail-fast e best-effort. Cancele com itens na fila, em chamada e em commit.
Todo item termina succeeded, skipped, failed, uncertain ou cancelled.

## Etapa D — relatório CSV

Exporte IDs e outcomes com biblioteca CSV. Fixtures incluem aspas, newline, Unicode
e texto iniciado por =, +, - e @. Neutralize segundo o consumidor documentado e
faça round-trip.

## Aceite

- testes de retry não usam sleep real;
- nenhuma fila/task cresce sem limite;
- concorrência observada nunca excede N;
- limite de workers é defendido por medição;
- cancelamento não chama efeito confirmado de rollback;
- CSV preserva texto sem executar fórmula no consumidor suportado;
- relatório final é determinístico.

## Extensão

Gere documento a partir de template validado. Um placeholder ausente deve abortar
antes de publicar qualquer documento final.

