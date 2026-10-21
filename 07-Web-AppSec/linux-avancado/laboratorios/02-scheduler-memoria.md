# Lab 02 — Scheduler, memória e PSI

**Classe:** A/C. **Duração:** 12–18 h.

## Pré-requisitos e gate

Conclua o Lab 01 e os capítulos 07–12. Defina limites que deixem pelo menos
metade da RAM e uma CPU administrativa fora do experimento. Registre topologia,
governor ou frequência visível, kernel, vCPU, RAM, cgroup e virtualização.

## Hipóteses

1. Competidores na mesma CPU aumentam espera runnable.
2. Working set maior que o limite aumenta reclaim, faults e PSI de memória.
3. `MemoryHigh` produz degradação observável antes de `MemoryMax`.

## Desenho

Crie carga determinística de CPU e `page_faults` com 32, 128 e 256 MiB. Execute
baseline, competição na mesma CPU e CPUs distintas. Depois use scope systemd com
`MemoryHigh`/`MemoryMax` seguros para a VM.

Colete:

- tempo e resultado funcional;
- `perf stat` para task-clock, context-switches e migrations;
- `/proc/PID/sched` antes/depois;
- `memory.current`, `memory.events` e PSI;
- pelo menos dez repetições por condição.

Separe wall clock, task-clock, espera runnable e faults. Use uma janela comum
para PSI e métricas da aplicação; calcule deltas de `total`, não compare apenas
médias acumuladas. Randomize a ordem das condições e descarte warm-up somente
com regra definida antes.

## Fases

1. **Baseline:** uma carga, sem limite apertado e sem competidor.
2. **CPU:** duas cargas na mesma CPU e depois em CPUs elegíveis separadas.
3. **Peso:** nice ou CPUWeight diferente, isolado e sob competição.
4. **Memória:** working sets crescentes sem alterar cgroup.
5. **Proteção:** `MemoryHigh` abaixo de `MemoryMax`, com margem.
6. **Correlação:** trace curto apenas se contadores não separarem as hipóteses.

Não use RT, `drop_caches`, sysctl global ou OOM do host. Se `full` permanecer
alto após a carga, encerre o scope, preserve evidência e restaure a VM.

## Controles

- mesma entrada e binário;
- ordem A/B alternada;
- sem downloads, updates ou jobs concorrentes;
- snapshot/config preservados;
- aquecimento declarado.

## Análise exigida

Para cada hipótese, informe evidência favorável, evidência contrária e
confundidores. Nice não reserva percentual; demonstre a diferença entre execução
isolada e competição. MemAvailable baixo sem PSI pode representar cache saudável.
RSS, VSZ e PSS não são intercambiáveis.

Inclua pelo menos uma execução nula ou inesperada e explique como ela mudou o
modelo. Não remova outlier sem critério técnico e registro.

## Segurança

Limites devem deixar no mínimo metade da RAM da VM fora da carga. Não use
`SCHED_FIFO` neste lab. Interrompa se PSI full permanecer alto após encerrar.

## Entrega

CSV bruto, script de execução, mediana/p95/p99, gráfico e uma conclusão com
limitações da virtualização.

Acrescente código de saída, arquivo de ambiente, hashes e relatório que outra
pessoa possa recalcular. A aprovação exige distinguir runqueue de bloqueio, high
de max e correlação de causalidade.

## Perguntas para defesa

- Por que peso não muda uma tarefa isolada da mesma forma que sob competição?
- O que uma major fault demonstra e o que não demonstra?
- Qual camada do hypervisor continua fora da observação do guest?
- Que dado refutaria a hipótese de pressão de memória?
