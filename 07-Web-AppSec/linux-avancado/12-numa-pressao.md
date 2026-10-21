# 12 — NUMA, huge pages, PSI e DAMON

## Objetivos

- entender topologia NUMA e custo de acesso remoto;
- distinguir THP de HugeTLB;
- usar PSI para medir falta de progresso;
- conhecer DAMON sem aplicar tuning prematuro.

## NUMA

Em NUMA, CPUs e memória são agrupadas em nós com distâncias diferentes. Alocação
local tende a ser mais barata. First-touch significa que a CPU que primeiro
escreve pode influenciar onde a página é materializada. Afinar CPU sem política
de memória correspondente pode aumentar acessos remotos.

```bash
lscpu | grep -i numa
numactl --hardware 2>/dev/null || true
cat /sys/devices/system/node/online
cat /proc/self/numa_maps | head
```

Políticas incluem default/local, bind, preferred e interleave. `cpuset` restringe
recursos; mempolicy orienta alocação dentro do permitido. A restrição ancestral
vence uma preferência da tarefa.

## Huge pages

THP tenta promover automaticamente páginas, reduzindo TLB misses e page-table
overhead, mas pode adicionar compactação e latência. HugeTLB usa pools reservados
e semântica explícita. Verifique tamanho, modo e resultado real:

```bash
grep -E 'AnonHugePages|ShmemHugePages|HugePages|Hugepagesize' /proc/meminfo
cat /sys/kernel/mm/transparent_hugepage/enabled 2>/dev/null
grep -E 'AnonHugePages|KernelPageSize|MMUPageSize' /proc/self/smaps | head
```

## PSI

Pressure Stall Information mede a fração de tempo em que tarefas ficaram sem
progresso por CPU, memória ou I/O. `some` indica pelo menos uma tarefa afetada;
`full` indica todas as tarefas não ociosas afetadas simultaneamente no escopo.

```bash
cat /proc/pressure/cpu
cat /proc/pressure/memory
cat /proc/pressure/io
```

PSI complementa utilização. Memória 95% ocupada sem stalls pode estar saudável;
pressão crescente com latência indica falta de progresso.

## DAMON

DAMON amostra padrões de acesso com overhead controlável e pode alimentar
esquemas de operação. É ferramenta de observação e, opcionalmente, ação; comece
somente com monitoramento. Recursos dependem de config e versão.

## Localidade como hipótese

NUMA não é sinônimo de “mais rápido com bind”. Primeiro confirme a topologia e
as distâncias expostas pelo firmware ou hypervisor. Depois identifique onde
threads executam e onde páginas foram materializadas. First-touch distribui
memória conforme quem toca; inicialização serial pode concentrar páginas mesmo
quando o processamento posterior é paralelo.

Compare três políticas com a mesma carga: default, interleave e bind coerente de
CPU e memória. Colete throughput, latência, faults, migração de páginas e acessos
locais ou remotos quando a PMU permitir. Uma VM com um único nó não valida NUMA;
no máximo valida o procedimento e o fallback.

## Huge pages sem receita pronta

THP pode usar promotion e compaction em momentos que afetam cauda. HugeTLB
reserva pool explícito e pode desperdiçar capacidade. Meça TLB misses e páginas
realmente promovidas; apenas ler modo `always` ou `madvise` não prova uso.
Fragmentação, alinhamento, padrão de acesso e tamanho do working set determinam
se o benefício supera o custo.

## PSI como sinal de progresso

As médias `avg10`, `avg60` e `avg300` suavizam janelas diferentes; `total`
permite calcular deltas durante exatamente o experimento. CPU PSI indica tarefas
prontas sem CPU; memory PSI inclui stalls de reclaim e compaction; I/O PSI cobre
espera em I/O. `full` tem significado diferente por recurso e escopo, portanto
leia a documentação do kernel estudado.

DAMON amostra regiões e não registra cada acesso. Interprete resolução espacial,
intervalos e overhead antes de inferir hot/cold. Comece observando; esquemas de
reclaim são intervenção separada.

## Falhas comuns

- fixar CPU e esquecer política de memória;
- concluir NUMA dentro de guest com topologia artificial não documentada;
- afirmar uso de THP apenas pela configuração;
- comparar PSI acumulado sem delta de janela;
- ativar ação DAMON antes de validar a amostragem.

## Prática A/C

1. Meça uma carga com e sem first-touch paralelo.
2. Compare locality apenas se houver dois nós reais ou emulados.
3. Registre THP efetivamente usado, não apenas configurado.
4. Correlacione PSI com percentis de latência da carga.
5. Não altere sysctls no primeiro experimento.

## Exercícios

1. Desenhe CPUs, nós, distâncias, política e first-touch de uma carga paralela.
2. Calcule PSI a partir do delta de `total` e compare com p99 da aplicação na
   mesma janela.
3. Confirme THP em `smaps`, não apenas em sysfs, e registre custo de promoção.
4. Explique cenário com `MemAvailable` baixo e `memory full=0`, e outro com
   disponibilidade razoável mas stalls observáveis.

## Checklist de domínio

- [ ] Relaciono afinidade de CPU, first-touch e mempolicy.
- [ ] Distingo THP automático de pool HugeTLB.
- [ ] Interpreto PSI por recurso, escopo e janela.
- [ ] Uso DAMON como amostragem, não como verdade completa.
- [ ] Não faço tuning antes de medir controle e resultado real.

Fonte: [NUMA memory policy](https://docs.kernel.org/admin-guide/mm/numa_memory_policy.html).
