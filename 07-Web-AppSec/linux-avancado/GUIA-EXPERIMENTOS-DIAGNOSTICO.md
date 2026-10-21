# Guia de experimentos e diagnóstico de Linux avançado

Este guia conecta os capítulos quando um comportamento cruza scheduler, memória,
filesystem, bloco, driver e user space. Ele não oferece uma lista de “comandos
mágicos”. O objetivo é localizar a primeira camada divergente, testar uma
hipótese e preservar evidência suficiente para revisão.

## 1. Defina o contrato

Antes de instrumentar, escreva:

```text
esperado:
observado:
escopo e primeira ocorrência:
métrica, unidade e janela:
kernel/config/build:
workload e entrada:
mudança mais recente:
hipótese refutável:
controle negativo:
limite de risco e critério de parada:
reversão:
```

“Está lento” não separa CPU, espera runnable, fault, reclaim, lock ou I/O. Prefira:
“o p99 passou de 20 ms para 110 ms quando o working set excedeu
`MemoryHigh`; espero aumento de `high`, PSI e direct reclaim na mesma janela”.

## 2. Preserve antes de alterar

Colete UTC, duração monotônica, release, cmdline, config, virtualização, cgroup,
mount e hash do workload. Salve stdout, stderr e código de saída. Para crash,
preserve primeiro console, core/vmcore, executáveis, build IDs, módulos e símbolos.
Restart e recompilação podem destruir o estado mais útil.

Não publique core, vmcore, environment ou argumentos antes de procurar segredos.
Guarde dados brutos como somente leitura e produza gráficos a partir de cópias.

## 3. Escada de localização

Percorra da aplicação para baixo até encontrar a primeira divergência:

1. **Contrato da aplicação:** resultado, taxa, erro e duração.
2. **Tarefa:** estado, threads, syscalls, runqueue e sinais.
3. **Recursos:** cgroup, PSI, faults, descritores e limites.
4. **Memória:** VMA, RSS/PSS, reclaim, writeback e OOM.
5. **VFS/filesystem:** path walk, page cache, protocolo de `fsync`.
6. **Bloco:** fila, latência, merges, flush e device virtual.
7. **Driver/dispositivo:** completion, IRQ, DMA e erros.
8. **Plataforma:** NUMA, firmware, hypervisor e hardware.

Não pule diretamente para o kernel porque um syscall aparece no topo da stack. A
tarefa pode estar bloqueada legitimamente enquanto outra camada deixa de
progredir.

## 4. Escolha a ferramenta menos invasiva

Comece com contadores existentes em `/proc`, `/sys`, cgroup e logs. Depois use
`perf stat` para contagem, sampling para distribuição on-CPU, tracepoint para
eventos com contrato e somente então probe de função interna. eBPF local é útil
quando agregação no kernel reduz volume, mas exige verifier, privilégios e
teardown explícitos.

| Pergunta | Primeira evidência | Escalada |
|----------|--------------------|----------|
| faltou CPU? | task-clock, PSI CPU | sched wakeup/switch |
| faltou memória? | events, PSI, faults | reclaim/compaction tracepoints |
| esperou I/O? | latência da aplicação, diskstats | block issue/complete |
| travou em lock? | stacks de todas as threads | lockdep ou tracing dirigido |
| loader falhou? | ELF e `PT_INTERP` | trace de arquivos do processo próprio |
| kernel falhou? | primeira mensagem e taint | vmcore com símbolos exatos |

Uma ferramenta responde uma pergunta. Coleções enormes sem hipótese elevam
overhead e tornam falsos padrões mais prováveis.

## 5. CPU e scheduler

Separe wall clock de tempo na CPU. Uma tarefa com 2 ms de CPU e 20 ms fim a fim
passou 18 ms runnable ou bloqueada. Colete por thread; agregação do processo pode
esconder um worker saturado.

Ordem recomendada:

1. resultado funcional e timestamps internos;
2. `perf stat` com task-clock, switches e migrations;
3. estado e `/proc/PID/sched`;
4. trace curto de wakeup/switch somente se a hipótese permanecer.

Nice muda peso sob competição. Afinidade pode reduzir migração ou criar fila.
Política RT só entra em VM sacrificável com watchdog, console e CPU administrativa.

## 6. Memória

VSZ não é residência e memória ocupada não é pressão. Correlacione RSS/PSS,
minor/major faults, `memory.current`, eventos, PSI e comportamento do workload.
Page cache recuperável pode ser saudável; direct reclaim e PSI indicam perda de
progresso.

Quando houver OOM, determine primeiro se foi global ou memcg. Preserve a primeira
mensagem, limites ancestrais, `memory.events` e conjunto de tarefas. A vítima é
uma decisão do mecanismo, não necessariamente a causa do crescimento.

## 7. Arquivos e bloco

Uma escrita pode terminar na page cache antes de alcançar mídia. Para requisito
de durabilidade, documente `fsync` do arquivo, rename e `fsync` do diretório,
além do contrato de flush abaixo.

Meça latência da aplicação e do device na mesma janela. Dentro de VM, diskstats
descreve dispositivo virtual; o host ainda pode ter fila e cache próprios. Não
compare IOPS sem tamanho, mix, padrão, sync e queue depth.

Todo teste de filesystem, Device Mapper ou repair usa arquivo-imagem explícito.
Antes do cleanup, prove a árvore. Remova filesystem, volume, mapping e loop na
ordem inversa; nunca substitua o alvo por glob de `/dev`.

## 8. Tracing com orçamento

Registre estado anterior, clock, buffer, eventos e filtros. Desabilite antes de
configurar e antes de ler snapshot. Use `trap` para restauração. Defina:

- duração máxima;
- número esperado de eventos por segundo;
- memória de buffer;
- filtro de PID ou cgroup;
- campos necessários;
- contador de perda aceitável, normalmente zero no laboratório.

Tracepoints são preferíveis a kprobes quando expõem os dados necessários. Um
kprobe em função interna precisa ser revalidado após cada build. Sequência
temporal sustenta correlação; causalidade exige controle ou mecanismo adicional.

## 9. Crash e hang

Para user space, preserve build ID, core, bibliotecas e input. Crash exige fault
address e ownership; deadlock exige todas as stacks e grafo de espera; corrupção
exige encontrar a escrita anterior.

Para kernel, diferencie WARN, oops, panic, hung task, soft e hard lockup. Use a
primeira falha. Taint é contexto. vmcore só é interpretável com `vmlinux`,
config e módulos daquela build. Kdump não está pronto enquanto uma captura de
teste não tiver sido aberta e analisada.

## 10. Encerramento do diagnóstico

Uma investigação termina quando:

- a hipótese foi sustentada ou refutada por controle;
- a menor correção restaura o requisito;
- teste funcional e regressão passam;
- risco e limitações estão documentados;
- toda instrumentação e estado privilegiado foram removidos;
- os dados brutos continuam disponíveis por hash;
- outra pessoa consegue revisar o raciocínio.

Se o resultado não reproduzir, registre-o. Ocultar execução nula cria certeza
falsa e impede que o próximo experimento melhore o modelo.
