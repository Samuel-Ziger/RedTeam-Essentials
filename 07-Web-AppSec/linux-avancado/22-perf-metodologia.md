# 22 — perf, PMU, flame graphs e metodologia

## Objetivos

- formular hipótese de desempenho antes de coletar;
- usar contadores, sampling e call graphs;
- interpretar multiplexing, skid e overhead;
- comunicar incerteza e distribuição.

## Pergunta antes da ferramenta

Comece por impacto observável: latência, throughput, CPU, memória ou I/O. Defina
uma hipótese que um dado possa negar. “Rodar perf para ver” gera muitos eventos e
pouca conclusão.

Método USE por recurso:

- utilization: fração ocupada;
- saturation: trabalho esperando;
- errors: falhas e retries.

Para aplicação, acrescente taxa, erros e duração. Este módulo usa apenas cargas
locais.

## `perf stat`

```bash
perf stat -r 5 -e task-clock,cycles,instructions,branches,branch-misses \
  -- ./workload
```

IPC é instruções por ciclo, não “eficiência universal”. Instruções distintas
têm custos diferentes; stalls, frequência e vetorização importam. Se eventos
excedem contadores físicos, a PMU multiplexa e escala resultados; confira tempo
ativo e incerteza.

## Sampling

```bash
perf record -g -- ./workload
perf report
```

Sampling responde onde amostras ocorreram, sujeito a frequência, unwind e skid.
Frame pointers, DWARF ou LBR mudam custo e qualidade do call graph. Símbolos e
debuginfo precisam corresponder ao binário.

## Flame graphs

Largura representa número de amostras, não tempo de uma chamada individual.
Altura é profundidade, não gravidade. Topo largo aponta onde CPU foi amostrada;
não mostra espera off-CPU sem coleta apropriada.

## Benchmark confiável

1. fixe entrada e versões;
2. aqueça quando o cenário real é quente;
3. randomize ordem A/B;
4. repita e guarde dados brutos;
5. observe thermal throttling e frequência;
6. apresente mediana, p95/p99 e dispersão;
7. valide que a otimização preserva correção.

## Contadores e atribuição

Eventos de hardware pertencem a uma microarquitetura e podem contar de forma
diferente entre CPUs. `cycles` varia com frequência e estados; `task-clock`
mede tempo agendado; wall clock inclui espera. Multiplexing ocorre quando há mais
eventos que contadores físicos: o kernel agenda grupos e escala valores. Registre
`time_enabled`, `time_running` ou percentual exibido e reduza a lista quando a
razão for baixa.

Contagem por processo, thread, CPU, cgroup e sistema responde perguntas distintas.
Herdar para filhos ou agregar CPUs pode esconder desbalanceamento. Comece no
escopo da métrica da aplicação e amplie somente se a hipótese exigir.

## Sampling sem falsa precisão

Sampling observa uma distribuição, não todas as ocorrências. Frequência alta
aumenta resolução e overhead. Skid desloca amostra do evento preciso; PEBS/IBS ou
outros mecanismos podem melhorar precisão quando suportados. Call graph incorreto
pode vir de frame pointers omitidos, unwind DWARF caro, stack limitada ou símbolos
divergentes.

Flame graph on-CPU não mostra por que a tarefa ficou fora da CPU. Para latência,
combine perfis on-CPU, off-CPU ou trace de scheduler com timestamps da aplicação.
Uma função larga pode ser vítima de chamadas caras abaixo dela; investigue stack
completa antes de otimizar o frame superior.

## Falhas comuns

- escolher evento disponível sem ligá-lo à hipótese;
- comparar contadores de CPUs ou kernels diferentes;
- ignorar multiplexing e frequência;
- tratar amostras como duração exata de cada chamada;
- otimizar benchmark quebrando resultado;
- publicar apenas a melhor repetição.

## Prática A

Compile uma carga com `-O0`, `-O2` e `-O3`. Compare tempo, instruções, ciclos e
resultado funcional. Use cinco repetições e explique variações sem escolher
apenas a melhor.

## Exercícios

1. Defina uma hipótese e escolha o menor conjunto de eventos que poderia
   refutá-la; explique por que cada evento participa.
2. Force multiplexing com muitos eventos, depois reduza o grupo e compare a
   confiança da medição.
3. Gere perfis com frame pointer e DWARF e avalie diferença de overhead e stacks.
4. Investigue caso com menos instruções e mais tempo separando frequência, stalls,
   espera e ruído.

## Checklist de domínio

- [ ] Começo por impacto, hipótese e controle, não pela ferramenta.
- [ ] Distingo wall clock, task-clock, cycles e instructions.
- [ ] Detecto multiplexing, skid, unwind incompleto e overhead.
- [ ] Interpreto flame graph como amostras on-CPU.
- [ ] Valido correção e apresento distribuição completa.

Fonte: [perf](https://perf.wiki.kernel.org/index.php/Main_Page).
