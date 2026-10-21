# 28 — Tempo real, latência e PREEMPT_RT

## Objetivos

- distinguir tempo real de “rápido”;
- decompor fontes de latência e jitter;
- usar políticas RT com limites de segurança;
- avaliar PREEMPT_RT, afinidade e prioridade herdada.

## Deadline é contrato

Sistema real-time é avaliado pela capacidade de cumprir deadlines, incluindo o
pior caso relevante. Uma média baixa com outlier de segundos falha para controle
crítico. Hard, firm e soft real-time diferem pela consequência de perder prazo.

## Fontes de latência

- tarefa de maior prioridade executando;
- seção não preemptível ou interrupção desabilitada;
- page fault e alocação;
- contenção de lock e inversão de prioridade;
- IRQ, workqueue e timer;
- C-states, mudança de frequência e firmware;
- SMI invisível ao kernel;
- pressão de memória ou I/O;
- ruído do hypervisor.

## Inversão de prioridade

Uma tarefa baixa segura lock, uma alta bloqueia nele e uma média preempta a
baixa: indiretamente a média atrasa a alta. Priority inheritance eleva
temporariamente o dono do lock. PI mutex resolve esse padrão, não dependências
arbitrárias ou I/O lento dentro da região crítica.

## PREEMPT_RT

RT torna mais partes do kernel preemptíveis, converte spinlocks selecionados e
threadiza interrupções. O resultado depende de drivers, hardware e configuração.
Uma plataforma precisa de teste de pior caso sob carga concorrente representativa.

## Ferramentas

```bash
cyclictest --help 2>/dev/null | head
chrt -m
cat /sys/kernel/realtime 2>/dev/null || true
```

Nunca execute um loop `SCHED_FIFO` infinito sem CPU de administração, limite,
watchdog e acesso ao console. Faça testes apenas na VM C.

## Desenho do experimento

1. meça baseline ocioso;
2. adicione CPU, memória e I/O locais separadamente;
3. combine apenas depois;
4. registre histograma e máximo, não só média;
5. capture trace ao cruzar threshold;
6. repita em bare metal de teste se a decisão for de hardware.

## Orçamento de latência

Decomponha o deadline: liberação do evento, wakeup, espera pela CPU, execução,
bloqueios, IRQ e entrega da saída. Reserve margem para variação. O requisito deve
dizer período, deadline, duração do teste, carga concorrente e consequência da
perda. “Menos de 100 µs em média” não limita o pior caso.

`cyclictest` mede latência de wakeup sob configuração específica; não prova o
tempo fim a fim da aplicação. Use histograma, máximo e contagem de violações.
Correlacione outlier com tracing limitado por threshold. A própria coleta altera
o sistema, então faça controle com e sem instrumentação.

## Preparação da tarefa

Evite faults previsíveis pré-alocando e tocando memória, considere `mlockall`
somente com limite e privilégio adequados e não aloque no caminho crítico. Defina
afinidade junto com posicionamento de IRQ e housekeeping; isolar uma CPU sem
considerar workers e timers pode apenas mover ruído.

Prioridades formam uma cadeia. A tarefa crítica não deve depender de serviço com
prioridade incapaz de progredir. Locks com PI ajudam inversão direta; comunicação,
filesystem e firmware podem continuar sem bound útil. PREEMPT_RT reduz seções
não preemptíveis, mas driver e hardware precisam de medição próprios.

## Falhas comuns

- usar média como garantia de deadline;
- rodar FIFO infinito na única CPU administrativa;
- atribuir outlier do guest ao kernel sem observar host;
- bloquear em I/O imprevisível no caminho crítico;
- ativar isolamento, C-states ou frequência todos ao mesmo tempo;
- medir sem workload concorrente representativo.

## Exercícios

1. Construa orçamento de 1 ms distribuído entre wakeup, runqueue, execução e
   bloqueios, incluindo margem.
2. Colete histograma baseline e sob uma carga local por tempo definido; relate
   todas as violações, não apenas média.
3. Modele inversão de prioridade com e sem PI e uma dependência que PI não
   consegue resolver.
4. Liste scheduler do host, vCPU, timer virtual e VM exits que impedem uma VM de
   provar deadline de bare metal.

## Checklist de domínio

- [ ] Defino real-time por deadline e consequência, não por velocidade média.
- [ ] Decomponho latência e preservo margem.
- [ ] Uso histograma, máximo e violações sob carga.
- [ ] Configuro RT somente com watchdog, console e CPU administrativa.
- [ ] Não generalizo resultado de VM para hardware real.

Fonte: [real-time preemption](https://docs.kernel.org/core-api/real-time/index.html).
