# 12 — Memória virtual, page cache, swap e OOM

## Objetivos

- relacionar endereço virtual, página, frame, fault e residência;
- distinguir VIRT, RSS, PSS, USS, cache recuperável e memória anônima;
- interpretar pressão, reclaim, swap e eventos OOM ao longo do tempo;
- testar uma hipótese de memória sem desestabilizar o host.

## O mapa mental correto

Cada processo enxerga um espaço de endereços virtual. Tabelas de páginas,
administradas pelo kernel com suporte da MMU, mapeiam páginas virtuais para
frames físicos ou indicam que a página ainda precisa ser materializada. Isso
oferece isolamento, compartilhamento controlado, mapeamento de arquivos e
alocação sob demanda.

```text
endereço virtual do processo
          ↓ page tables / MMU
RAM: página anônima | page cache | página compartilhada | estrutura do kernel
          ↕ reclaim                         ↕ swap (quando elegível)
```

## Layout de um processo

Um processo costuma mapear:

- segmentos do executável e bibliotecas;
- heap para alocações dinâmicas;
- stacks de threads;
- arquivos mapeados por `mmap`;
- regiões anônimas e compartilhadas;
- páginas auxiliares do kernel.

```bash
cat "/proc/$$/maps" | sed -n '1,25p'
pmap -x "$$" 2>/dev/null | tail -n 5
grep -E '^(Vm|Rss|Threads)' "/proc/$$/status"
```

Stack e heap são conceitos de runtime, não duas caixas que explicam toda a
memória de um processo.

## Reserva não é residência

- **VSZ/VIRT:** espaço virtual mapeado; pode incluir regiões nunca tocadas,
  arquivos e memória compartilhada.
- **RSS/RES:** páginas atualmente residentes atribuídas ao processo, com
  compartilhamento que pode ser contado repetidamente.
- **PSS:** divide páginas compartilhadas proporcionalmente e costuma estimar
  melhor o custo por processo.
- **USS:** páginas exclusivas do processo.

```bash
grep -E '^(Rss|Pss|Private|Shared)' "/proc/$$/smaps_rollup" 2>/dev/null
ps -o pid,vsz,rss,%mem,comm -p "$$"
```

Um `malloc()` bem-sucedido pode reservar endereço sem consumir imediatamente
toda a RAM. Ao tocar páginas, page faults materializam mapeamentos.

## Page faults

- minor fault: resolve sem buscar dados de um dispositivo de bloco, por exemplo
  page cache ou alocação anônima;
- major fault: requer I/O de armazenamento;
- copy-on-write: pai e filho compartilham páginas até uma escrita exigir cópia.

```bash
/usr/bin/time -v true 2>&1 | grep -i 'page fault'
pidstat -r 1 3 2>/dev/null || true
```

Fault não significa necessariamente erro; é parte normal da paginação.

## Como ler `free`

```bash
free -h
grep -E '^(MemTotal|MemFree|MemAvailable|Buffers|Cached|Swap)' /proc/meminfo
```

Linux usa RAM ociosa como cache de arquivos. Por isso `free` pequeno não prova
falta de memória. `MemAvailable` estima quanto pode ser fornecido a novas cargas
sem swapping significativo, considerando cache recuperável e outros fatores.
Cache usado produtivamente é memória bem aproveitada.

Não use `drop_caches` como “otimização” rotineira: ele destrói trabalho útil e
pode aumentar latência. Serve a experimentos controlados com entendimento.

## Memória anônima, arquivos e swap

Páginas limpas de arquivo podem ser descartadas e relidas. Páginas anônimas
modificadas não possuem arquivo de origem e, se elegíveis, podem ir para swap.
Swap amplia as opções de reclaim e absorve picos; não transforma disco em RAM
equivalente. Sem swap, pressão pode chegar ao OOM mais cedo.

```bash
swapon --show
vmstat 1 5
cat /proc/pressure/memory
```

Em `vmstat`, `si`/`so` mostram swap-in/out naquele intervalo. Uso de swap
acumulado não prova thrashing. Observe atividade, latência e PSI.

## Reclaim, LRU e pressão

Quando faltam páginas livres, o kernel recupera cache, escreve dados sujos e
pode mover memória anônima para swap. Pressure Stall Information (PSI) mede
tempo em que tarefas ficam atrasadas esperando recursos:

```bash
cat /proc/pressure/cpu
cat /proc/pressure/memory
cat /proc/pressure/io
```

Pressão sustentada, latência e eventos de reclaim contam mais que uma foto
isolada do percentual usado.

## OOM

Se reclaim não satisfaz uma alocação, o kernel pode acionar o OOM killer. A
seleção considera consumo, ajustes e contexto; em cgroup, o evento pode ficar
contido no grupo.

```bash
journalctl -k -g 'oom|Out of memory|Killed process' --since today 2>/dev/null
cat "/proc/$$/oom_score"
cat "/proc/$$/oom_score_adj"
```

Não altere `oom_score_adj` para tornar tudo imune: se nenhum processo elegível
puder ser encerrado, o sistema pode ficar irrecuperável. Corrija vazamento,
limites e capacidade.

## Overcommit

Linux pode aceitar compromissos virtuais maiores que RAM+swap conforme a
política em `vm.overcommit_memory`. Isso atende aplicações que reservam mais do
que usam, mas torna a aceitação da alocação diferente da garantia futura.

```bash
sysctl vm.overcommit_memory vm.overcommit_ratio
grep -E '^(CommitLimit|Committed_AS)' /proc/meminfo
```

Não mude valores globais sem medir a carga e entender a documentação da
versão do kernel.

## cgroup v2

Cgroups contabilizam e controlam grupos de processos. Arquivos importantes em
um cgroup v2 incluem `memory.current`, `memory.high`, `memory.max`,
`memory.events` e `memory.pressure`. `memory.high` pressiona/restringe;
`memory.max` é limite duro e pode levar a OOM dentro do cgroup.

```bash
stat -fc %T /sys/fs/cgroup
systemctl status "$(systemctl --user --no-pager --plain 2>/dev/null | head -n 1)" 2>/dev/null || true
cat /sys/fs/cgroup/memory.current 2>/dev/null || true
```

Use `systemd-run --user` em laboratório para escopos limitados, sem alterar a
raiz de cgroups manualmente.

## Slab, huge pages e NUMA

- slab/slub: caches de objetos do kernel;
- transparent huge pages: páginas maiores geridas automaticamente, com
  benefícios e custos dependentes da carga;
- hugetlb: huge pages reservadas explicitamente;
- NUMA: latência de memória depende do nó em máquinas multiprocessadas.

```bash
slabtop -o 2>/dev/null | head
grep -i huge /proc/meminfo
numactl --hardware 2>/dev/null || true
```

Não ajuste THP ou NUMA por receita genérica; compare uma carga representativa.

## Método de diagnóstico

1. defina sintoma: erro, latência, OOM ou swapping;
2. estabeleça intervalo e carga afetada;
3. examine `MemAvailable`, PSI, faults, swap I/O e eventos OOM;
4. identifique processo/cgroup por RSS, PSS e tendência;
5. diferencie cache recuperável, anônima, slab e memória bloqueada;
6. reproduza com limite seguro;
7. corrija aplicação, configuração ou capacidade;
8. confirme que a métrica e o sintoma melhoraram.

## Laboratório

Compile e execute `exemplos/c/memoria.c`. Compare `/proc/PID/maps`,
`smaps_rollup`, faults e RSS antes da alocação, depois da reserva e depois de
tocar as páginas. O programa limita a alocação e não tenta provocar OOM.

## Exercícios

1. Compile o exemplo de memória, execute com dois tamanhos e compare reserva,
   páginas tocadas, faults e RSS; não use um tamanho capaz de pressionar o host.
2. Observe uma aplicação durante cinco minutos e explique por que uma única
   fotografia de uso não revela tendência nem pressão sustentada.
3. Compare memória do processo em status, smaps rollup e cgroup; documente por
   que os números não precisam ser idênticos.
4. Construa uma árvore de decisão para lentidão, swapping ativo e evento OOM,
   incluindo a evidência que falsificaria cada hipótese.

## Checklist de domínio

Consigo explicar por que VIRT não é RAM, cache não é desperdício, swap usada
não prova problema e OOM deve ser investigado no contexto de processo/cgroup.
