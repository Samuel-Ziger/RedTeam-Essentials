# 07 — Scheduler, EEVDF, RT e deadline

## Objetivos

- explicar runnable, runqueue, preempção e migração;
- distinguir classes fair, real-time e deadline;
- interpretar afinidade, nice, latência e utilização;
- medir antes de alterar prioridades.

## O problema de escalonamento

Cada CPU lógica executa uma tarefa por vez. O scheduler escolhe entre tarefas
runnable, equilibra carga, respeita classes e tenta manter afinidade de cache.
Uma tarefa dormindo por I/O não compete na runqueue enquanto espera.

No caminho fair moderno, a transição do Linux para EEVDF começou na versão 6.6.
O algoritmo acompanha
**lag** em relação ao serviço justo, determina elegibilidade e escolhe o menor
deadline virtual. Isso permite considerar peso e pedido de fatia sem prometer
deadline de tempo real.

Não trate todo kernel como idêntico: confira versão, patches da distribuição e
documentação do checkout.

## Classes

| Classe | Uso | Risco |
|--------|-----|-------|
| `SCHED_OTHER` | trabalho geral fair | latência varia com carga |
| `SCHED_BATCH` | CPU-bound pouco interativo | favorece throughput |
| `SCHED_IDLE` | trabalho somente ocioso | pode sofrer forte atraso |
| `SCHED_FIFO/RR` | tempo real por prioridade | pode impedir progresso do sistema |
| `SCHED_DEADLINE` | runtime/period/deadline | admissão e configuração exigem rigor |

Prioridade real-time incorreta pode bloquear inclusive a administração da VM.
Experimentos RT são classe C, com watchdog e limite de duração.

## Observação

```bash
ps -eLo pid,tid,psr,cls,rtprio,pri,ni,stat,comm
chrt -p "$$"
taskset -pc "$$"
cat /proc/self/sched
cat /proc/schedstat 2>/dev/null | head
```

`nice` muda peso relativo na classe fair, não reserva uma porcentagem fixa. A
afinidade limita CPUs elegíveis; ela pode melhorar locality ou criar sobrecarga.

## Latência versus throughput

O tempo de resposta combina espera runnable, execução e bloqueios. CPU a 100%
não demonstra sozinha contenção: uma carga batch pode usar CPU ociosa sem
atrasar trabalho crítico. Meça `task-clock`, context switches, migrations,
runqueue latency e percentis da aplicação.

## Modelo fair moderno

Na classe fair, peso determina participação relativa quando existe competição;
não é reserva de CPU. No modelo EEVDF, o scheduler acompanha quanto serviço a
tarefa recebeu em relação ao ideal. Lag positivo indica que ela está atrás;
somente entidades elegíveis concorrem, e a de menor deadline virtual tende a ser
escolhida. Pedidos de fatia menores podem favorecer responsividade, mas aumentam
trocas e não convertem a tarefa em real-time.

Ao analisar um resultado, separe três tempos: execução efetiva na CPU, espera
runnable e bloqueio voluntário. Uma aplicação pode ter baixa utilização média e
p99 ruim por despertar atrás de outra tarefa, por migrar e perder locality ou
por esperar lock. `perf sched`, tracepoints `sched_switch`/`sched_wakeup` e
estatísticas da própria aplicação respondem perguntas diferentes.

## RT e deadline como contratos

`SCHED_FIFO` executa até bloquear, ceder ou ser preemptado por prioridade RT
maior; `SCHED_RR` adiciona quantum entre tarefas da mesma prioridade.
`SCHED_DEADLINE` expressa runtime, deadline e period e faz controle de admissão.
Configurações impossíveis devem ser rejeitadas; configurações possíveis ainda
precisam respeitar custos de kernel, IRQ e bloqueios.

Antes de elevar prioridade, identifique todas as dependências. Uma tarefa RT que
espera mutex mantido por tarefa comum pode sofrer inversão; priority inheritance
ajuda apenas quando a primitiva e o caminho oferecem essa semântica. Mantenha CPU
de administração e watchdog fora do conjunto do teste.

## Falhas comuns

- interpretar nice como porcentagem fixa;
- medir somente CPU total e ignorar espera runnable;
- fixar afinidade e criar uma fila artificial;
- usar prioridade RT para esconder bloqueio ou I/O lento;
- comparar kernels sem registrar versão, config e política ativa.

## Prática A/C

1. Execute duas cargas idênticas com nice diferente.
2. Compare tempo, `perf stat` e `/proc/PID/sched`.
3. Repita com afinidade na mesma CPU e em CPUs separadas.
4. Explique cache, fairness e ruído.
5. Apenas na VM, use RT por poucos segundos com um limite externo.

## Exercícios

1. Produza uma linha do tempo com wakeup, espera runnable, execução, bloqueio e
   conclusão; calcule cada parcela.
2. Compare duas cargas fair com pesos diferentes, primeiro isoladas e depois em
   competição, e explique quando a diferença aparece.
3. Desenhe um caso de inversão de prioridade e marque exatamente onde PI muda o
   resultado.
4. Analise 20 ms de latência com 2 ms de CPU e proponha evidência para distinguir
   runqueue, lock, timer, reclaim e I/O local.

## Checklist de domínio

- [ ] Distingo utilização, espera runnable, bloqueio e latência fim a fim.
- [ ] Explico lag, elegibilidade e deadline virtual sem prometer tempo real.
- [ ] Sei quando afinidade ajuda e quando cria contenção.
- [ ] Nunca testo RT sem watchdog, console e CPU de recuperação.
- [ ] Escolho uma evidência capaz de separar hipóteses concorrentes.

Fonte: [scheduler EEVDF](https://docs.kernel.org/scheduler/sched-eevdf.html).
