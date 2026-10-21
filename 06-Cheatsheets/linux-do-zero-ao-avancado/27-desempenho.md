# 27 — Desempenho e planejamento de capacidade

## Objetivos

- definir carga, SLO, janela e baseline antes de otimizar;
- separar demanda, utilização, saturação, latência e erro por recurso;
- localizar gargalo com séries temporais e experimento controlado;
- planejar capacidade com margem, crescimento e cenário de falha.

## Desempenho é requisito medido

“Rápido” precisa de carga, percentil, prazo e recurso. Exemplos:

- p95 abaixo de 200 ms a 500 requisições/s;
- job conclui em 20 minutos com 4 GiB;
- fila não cresce durante pico de duas horas;
- boot até serviço pronto em 45 segundos.

Throughput e latência podem competir. Média esconde caudas. Otimização sem
baseline pode apenas mover gargalo.

## Método USE

Para cada recurso, examine:

- **utilization:** tempo/capacidade ocupada;
- **saturation:** fila ou trabalho que espera;
- **errors:** falhas, retries, drops e correções.

Recursos: CPUs, memória, interfaces, controladores, discos, filesystems, sockets
e limites de software. Nem toda ferramenta calcula utilização da mesma forma.

## Baseline reproduzível

Registre:

```bash
uname -a
lscpu
free -h
lsblk -o NAME,TYPE,SIZE,ROTA,SCHED,MODEL
ip -s link
sysctl kernel.sched_autogroup_enabled 2>/dev/null
```

Inclua configuração, versões, temperatura, governadores, virtualização,
dataset, cache frio/quente, duração e repetições.

## CPU

Perguntas: há fila executável? um core está saturado? tempo está em user,
kernel, IRQ ou steal? há throttling térmico/cgroup?

```bash
mpstat -P ALL 1 5 2>/dev/null
pidstat -u -w 1 5 2>/dev/null
cat /proc/loadavg
perf stat -- comando
```

Load deve ser interpretado com quantidade de CPUs e tarefas em `D`. CPU baixa
com latência alta pode indicar lock, I/O ou limite externo.

## Memória

Perguntas: existe PSI, reclaim, faults maiores, swap I/O, OOM ou crescimento de
PSS? O problema é cgroup ou host?

```bash
free -h
vmstat 1 5
cat /proc/pressure/memory
grep -E '^(Rss|Pss|Private)' /proc/PID/smaps_rollup
```

Não dimensione pela soma ingênua de RSS quando há compartilhamento.

## Armazenamento

Perguntas: latência vem do dispositivo, fila, filesystem, writeback ou
aplicação? O padrão é sequencial/aleatório, leitura/escrita, sync/async?

```bash
iostat -xz 1 5 2>/dev/null
pidstat -d 1 5 2>/dev/null
cat /proc/pressure/io
```

Benchmark de disco pode consumir espaço, desgaste e interferir em produção.
Use volume dedicado do lab, limite de tamanho, dados descartáveis e perfil que
represente a aplicação. `dd` mede um caso estreito e cache pode dominar.

## Desempenho de conectividade

Banda, RTT, perda, retransmissão, filas, DNS e capacidade entre hosts ficam
nos módulos 14 a 18. Aqui, registre apenas o SLO da aplicação, o listener local
e o limite do processo; não gere tráfego nem altere parâmetros de rede.

## Tuning em camadas

Ordem preferida:

1. corrigir trabalho desnecessário e algoritmo;
2. remover erro/retry e serialização acidental;
3. ajustar aplicação e banco;
4. configurar limites/filas coerentes;
5. ajustar kernel somente com hipótese e experimento;
6. aumentar capacidade quando demanda justifica.

Para cada mudança: uma variável, baseline, teste A/B, intervalo, rollback e
observação de efeitos colaterais. Persistir sysctl sem guardar o padrão
anterior torna incidentes futuros mais difíceis.

## Capacidade

Separe tendência de pico. Modele crescimento, sazonalidade, headroom, falha de
um nó, tempo de provisionamento e limite de dependências. Alertas preditivos por
tempo-até-esgotar podem ser melhores que percentual fixo, mas exigem dados
estáveis.

## Experimento final

Escolha um programa do curso:

1. defina workload e SLO;
2. execute aquecimento;
3. colete cinco repetições;
4. identifique gargalo por evidência;
5. altere uma coisa;
6. repita nas mesmas condições;
7. apresente mediana e percentis, não só melhor caso;
8. reverta se não houver melhora significativa.

## Exercícios

1. Defina um SLO simples para a unit didática e colete baseline ocioso e sob
   carga sintética limitada.
2. Formule hipótese de CPU, memória e armazenamento; indique métrica, mudança
   controlada e resultado que refutaria cada uma.
3. Compare média e percentis de uma amostra de latência e explique o que a
   média esconde.
4. Produza previsão simples de capacidade com crescimento, pico, margem e perda
   de uma instância; declare todas as suposições.

## Checklist de domínio

Consigo responder “o que está saturado e por quê?” com janela, carga, métrica e
experimento, sem confundir correlação com causa.
