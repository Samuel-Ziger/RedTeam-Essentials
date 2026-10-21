# 15 — Block layer, filas e writeback

## Objetivos

- seguir I/O do filesystem ao dispositivo;
- entender bio, request, blk-mq, filas e merge;
- diferenciar latência, throughput, IOPS e profundidade;
- interpretar scheduler sem aplicar receitas universais.

## Caminho conceitual

```text
aplicação → VFS/page cache → filesystem → bio → blk-mq → driver → device
                                     ↑ completion e erro ←
```

Um `bio` descreve regiões de memória e setores de uma operação. A block layer
combina, divide, enfileira e transforma trabalho em requests adequados ao driver.
blk-mq oferece filas de submissão por CPU/contexto e filas de hardware.

## Métricas

- IOPS: operações por segundo, dependente de tamanho e padrão;
- throughput: bytes por segundo;
- latência: distribuição de tempo por operação;
- queue depth: trabalho simultaneamente pendente;
- utilização: tempo ocupado segundo o ponto de observação.

Comparar IOPS sem tamanho, read/write mix, sequencialidade, sync e profundidade
não tem valor.

## I/O schedulers

`none`, `mq-deadline`, BFQ e Kyber podem existir conforme config e dispositivo.
NVMe rápido, HDD rotacional, desktop interativo e VM compartilham necessidades
diferentes. Leia o selecionado e disponíveis:

```bash
for queue in /sys/block/*/queue/scheduler; do
  printf '%s: ' "$queue"
  cat "$queue"
done
```

Não altere dispositivo do host. Faça comparação em disco virtual dedicado.

## Writeback e flush

Páginas sujas são escritas em lotes. Barriers/flushes comunicam ordenação e
persistência através da pilha, mas caches de dispositivo que mentem sobre flush
quebram o contrato. `fsync` concluído deve ser avaliado ponta a ponta.

Discard/TRIM informa blocos não usados. Pode ser periódico ou online; comportamento
e custo variam por camada, thin provisioning e virtualização.

## Observação

```bash
lsblk -o NAME,TYPE,SIZE,ROTA,SCHED,MOUNTPOINTS
cat /proc/diskstats
iostat -xz 1 2 2>/dev/null || true
```

Dentro de VM, a métrica vê dispositivo virtual. Correlacionar com host exigiria
outra coleta; não invente causalidade a partir de uma camada.

## Decompondo a latência

Latência observada pela aplicação inclui espera na page cache ou filesystem,
fila do bloco, serviço no dispositivo e completion até a tarefa voltar a rodar.
Um contador medido no device não inclui necessariamente todo o caminho. Alinhe
timestamps e escopo antes de comparar `fio`, `/proc/diskstats`, tracepoints e
latência da aplicação.

Little relaciona concorrência média, taxa e tempo no sistema quando o regime é
estável: mais queue depth mantém o dispositivo ocupado, mas cada operação pode
esperar mais. Throughput crescente com p99 degradado é um resultado esperado,
não contradição. Defina primeiro SLO de cauda ou objetivo de vazão.

## Requests, merges e limites

O filesystem produz bios; a block layer pode dividir ou combinar trabalho
conforme limites de segmento, tamanho e alinhamento. blk-mq mapeia software
queues para hardware contexts e tags limitam operações em voo. Scheduler vê
apenas a camada em que opera; um dispositivo virtual ou target Device Mapper
pode acrescentar outra fila abaixo.

Flush estabelece barreira de persistência quando todas as camadas honram o
contrato. FUA pode pedir persistência por comando. `sync` global, `fsync` de um
arquivo e I/O com `O_SYNC` têm escopos e custos distintos. Nunca use conclusão
rápida como prova de mídia não volátil.

## Falhas comuns

- citar IOPS sem tamanho, mix, padrão e queue depth;
- usar `util=100%` como diagnóstico universal;
- executar benchmark contra bloco do host;
- comparar cache quente de uma condição com frio de outra;
- mudar scheduler sem conhecer a camada de virtualização;
- medir média quando o contrato usa p99.

## Prática B

Use `fio` somente contra arquivo dentro de volume descartável, com limite de
tamanho, tempo e `--filename` explícito. Compare leitura sequencial e aleatória,
uma e várias filas. Arquive percentis completos, não apenas bandwidth.

## Exercícios

1. Desenhe o caminho de uma escrita síncrona e marque todos os pontos de fila.
2. Compare quatro queue depths mantendo bytes, duração e workload constantes;
   apresente throughput e p50/p95/p99.
3. Calcule uma verificação de Little com taxa e tempo médio, declarando por que
   regime instável quebra a aproximação.
4. Identifique quais métricas vêm do guest, do device virtual e do host.

## Checklist de domínio

- [ ] Distingo bio, request, software queue, hardware context e completion.
- [ ] Relato IOPS com tamanho, mix, padrão, sync e profundidade.
- [ ] Explico a troca entre throughput e latência de cauda.
- [ ] Não generalizo métrica do guest para o hardware.
- [ ] Avalio persistência através de todas as camadas.

Fonte: [block layer](https://docs.kernel.org/block/index.html).
