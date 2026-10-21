# 11 — MM, page tables, allocators e reclaim

## Objetivos

- seguir um endereço virtual até a página física ou swap;
- explicar VMA, page tables, TLB e page fault;
- distinguir buddy, slab e alocações virtuais;
- interpretar reclaim, writeback, swap e OOM.

## Espaço virtual

O `mm_struct` representa o espaço de endereços de um processo. Regiões com
propriedades semelhantes são VMAs. Page tables traduzem endereços virtuais em
frames e carregam bits de permissão. A TLB cacheia traduções; mudá-las pode
exigir invalidação local ou entre CPUs.

```bash
cat /proc/self/maps
cat /proc/self/smaps_rollup
grep -E 'PageTables|AnonPages|Mapped|Slab' /proc/meminfo
```

Um page fault **minor** normalmente não espera armazenamento; um **major** exigiu
I/O. Fault não é necessariamente erro: demand paging e copy-on-write dependem
dele.

## Memória física

O buddy allocator gerencia blocos de páginas por ordem. SLUB/SLAB cria caches de
objetos do kernel. `kmalloc` oferece memória fisicamente contígua dentro de
limites; `vmalloc` oferece continuidade virtual com mapeamento de páginas que
podem ser dispersas. A escolha depende de tamanho, contexto e consumidor.

## Folios e page cache

Folio representa uma unidade de gerenciamento que pode conter mais de uma página
base e reduz overhead em operações maiores. Não assuma que todo folio tem ordem
zero nem que “página” em textos antigos corresponde exatamente à abstração
atual.

## Reclaim

Sob pressão, o kernel recupera page cache limpa, inicia writeback de páginas
sujas e pode mover memória anônima para swap. Reclaim direto faz a tarefa
solicitante trabalhar; `kswapd` atua em segundo plano. Thrashing ocorre quando
o working set não cabe e páginas retornam repetidamente.

```bash
vmstat 1
grep -E 'pgscan|pgsteal|pswp|oom' /proc/vmstat
cat /proc/pressure/memory
```

## Overcommit e OOM

Reserva virtual não equivale a memória física comprometida. Overcommit policy
decide admissão; alocação real pode falhar mais tarde. O OOM killer seleciona
uma vítima quando reclaim não permite progresso, respeitando cgroups e ajustes.

## Do endereço à página

Um acesso começa em endereço virtual gerado pela CPU. A TLB pode resolver a
tradução; em miss, hardware percorre page tables. Entrada ausente ou incompatível
com a permissão gera fault e transfere controle ao kernel. O handler localiza a
VMA, verifica acesso, materializa página anônima, lê arquivo, resolve COW ou
entrega sinal se o endereço não pertence a mapeamento válido.

RSS, PSS, VSZ e page-table bytes respondem perguntas diferentes. VSZ inclui
reservas ainda não materializadas; RSS conta páginas residentes do processo sem
dividir compartilhamento; PSS rateia páginas compartilhadas. Some métricas de
cgroup e sistema antes de concluir “vazamento” a partir de uma única coluna.

## Alocação e fragmentação

Buddy atende ordens de páginas fisicamente contíguas. Mesmo com muitos bytes
livres, uma ordem alta pode falhar por fragmentação. Compaction tenta formar
blocos; reclaim libera conteúdo recuperável. Slab caches reutilizam objetos e
podem reter memória para performance, portanto `Slab` alto não implica vazamento
sem crescimento, reclaimability e responsáveis.

Writeback e reclaim interagem: páginas sujas não podem ser descartadas antes de
persistir. Pressão pode fazer a própria tarefa entrar em direct reclaim, elevando
latência. Em cgroup, limite estreito muda o escopo de reclaim e OOM; sempre
correlacione `memory.events`, PSI e contadores de faults.

## Falhas comuns

- interpretar memória livre baixa como falta de memória;
- chamar todo page fault de erro;
- confundir reserva virtual com compromisso físico;
- atribuir major fault somente a swap;
- ajustar swappiness ou THP sem workload e baseline;
- analisar OOM sem o escopo global ou memcg.

## Prática A

Execute [`page_faults.c`](exemplos/c/page_faults.c) com tamanhos crescentes.
Compare faults antes/depois de tocar cada página, RSS, `smaps_rollup` e tempo.
Explique por que `malloc` bem-sucedido não comprova que todas as páginas existem.

## Exercícios

1. Compare VSZ, RSS e PSS antes de reservar, depois de reservar e depois de tocar
   um mapping grande.
2. Demonstre COW após `fork` medindo faults e PSS de pai e filho.
3. Relacione uma falha de ordem alta a fragmentação sem confundi-la com falta
   total de bytes.
4. Desenhe o caminho CPU → TLB → page tables → fault → alocação → retomada.

## Checklist de domínio

- [ ] Distingo VMA, page table, TLB, frame e mapping.
- [ ] Explico minor fault, major fault, demand paging e COW.
- [ ] Comparo buddy, slab, `kmalloc` e `vmalloc` pelo requisito.
- [ ] Relaciono reclaim, writeback, swap, PSI e OOM.
- [ ] Não uso `malloc` bem-sucedido como prova de residência física.

Fonte: [Memory Management](https://docs.kernel.org/mm/index.html).
