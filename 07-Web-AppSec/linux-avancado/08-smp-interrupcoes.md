# 08 — SMP, preempção, interrupções e timers

## Objetivos

- distinguir contexto de processo, hardirq, softirq e NMI;
- entender preempção, per-CPU data e migração;
- relacionar timers, clocks e tick;
- localizar latência causada por trabalho assíncrono local.

## Contextos de execução

Em contexto de processo, o código normalmente pode dormir quando permitido. Um
handler de hardirq deve ser curto e não pode bloquear como uma tarefa comum.
Trabalho adiado pode seguir por softirq, tasklet legado, workqueue ou thread de
IRQ. NMI tem restrições ainda maiores.

Pergunte sempre:

1. em qual contexto estou?
2. preempção e interrupções estão habilitadas?
3. posso dormir ou alocar com flags que dormem?
4. qual CPU possui o estado acessado?

## SMP e dados per-CPU

SMP permite execução concorrente real no kernel. Dados per-CPU evitam contenção,
mas exigem impedir migração enquanto um ponteiro per-CPU estiver em uso. Desligar
preempção ou usar APIs apropriadas não substitui proteção contra outra fonte de
concorrência, como uma interrupção na mesma CPU.

## Modelo de preempção

`CONFIG_PREEMPT_NONE`, voluntário, dinâmico e preemptivo oferecem trade-offs de
throughput e latência. PREEMPT_RT transforma diversos mecanismos e move mais
trabalho para contextos escalonáveis, mas não torna qualquer driver determinístico.

```bash
grep -E 'CONFIG_PREEMPT(_NONE|_VOLUNTARY|_DYNAMIC|=)' \
  /boot/config-"$(uname -r)" 2>/dev/null
cat /sys/kernel/realtime 2>/dev/null || true
```

## Interrupções

```bash
cat /proc/interrupts
cat /proc/softirqs
cat /proc/irq/default_smp_affinity
```

Este curso não analisa interrupções de rede. Escolha timer, armazenamento ou um
dispositivo local do laboratório.

## Tempo

O kernel combina clocksource, clock events e timers de alta resolução. Relógio
monotônico mede intervalos; tempo real pode saltar com ajustes. Para timeout,
prefira relógio monotônico. Jiffies continuam internos, mas user space não deve
assumir seu valor ou frequência.

## Entrada, adiamento e retorno

Uma interrupção interrompe o contexto atual, salva estado suficiente e entra por
um vetor da arquitetura. O handler reconhece a fonte e realiza o mínimo urgente;
trabalho restante segue em softirq, workqueue ou thread dedicada. A escolha
define se o código pode dormir, qual prioridade recebe e que tipo de proteção é
válido.

Workqueue não é apenas “thread depois”. O worker pool pode ser bound por CPU ou
unbound; flags, concurrency management e reclaim mudam garantias. Trabalho que
pode participar de reclaim precisa ser desenhado para evitar deadlock de memória.
Cancelamento também é protocolo: impedir nova fila, esperar item em execução e
liberar estado somente depois.

## Ordenação em SMP

Desabilitar preempção impede migração da tarefa atual, mas não impede hardirq,
NMI nem outra CPU. Desabilitar IRQ local não protege contra CPUs remotas. Por
isso cada dado precisa de uma lista explícita de contextos que o acessam e da
primitiva que cobre todos eles. Dados per-CPU reduzem compartilhamento, mas a
agregação ainda precisa de ordenação e snapshot coerente.

Timers são associados a uma base e disparam após o prazo, não necessariamente
no instante exato. Atraso inclui resolução, IRQ desabilitada, carga e política da
tarefa que consumirá o evento. Para medir intervalos, use clock monotônico e
registe clocksource; tempo civil pode ser ajustado.

## Falhas comuns

- chamar função que dorme em contexto atômico;
- manter IRQ desabilitada por seção longa;
- usar ponteiro per-CPU depois de permitir migração;
- liberar objeto enquanto work ou timer ainda o referencia;
- atribuir ao guest uma latência causada pelo hypervisor.

## Prática A

1. Registre `/proc/interrupts` duas vezes durante uma carga de disco local.
2. Calcule deltas por CPU.
3. Observe context switches e migrations com `perf stat`.
4. Correlacione um tracepoint de timer com a tarefa, sem alterar afinidades.
5. Documente limitações impostas pela virtualização.

## Exercícios

1. Classifique cinco APIs do kernel quanto a contexto permitido, capacidade de
   dormir e proteção exigida.
2. Desenhe o lifetime de um objeto referenciado por timer e workqueue, incluindo
   cancelamento síncrono no teardown.
3. Meça deltas de interrupções locais por CPU antes/durante uma carga e registre
   por que a correlação não prova causalidade.
4. Compare relógio monotônico e realtime durante um ajuste simulado de relógio.

## Checklist de domínio

- [ ] Distingo processo, hardirq, softirq, worker, IRQ thread e NMI.
- [ ] Sei quando uma operação pode dormir.
- [ ] Não confundo desabilitar preempção com exclusão entre CPUs.
- [ ] Projeto cancelamento antes de liberar objeto assíncrono.
- [ ] Explico por que dormir em hardirq impediria o progresso necessário.

Fonte: [locking no kernel](https://docs.kernel.org/locking/index.html).
