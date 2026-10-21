# Guia de diagnóstico — dados, APIs e consistência

Diagnosticar um sistema orientado a dados significa localizar a primeira
fronteira em que o comportamento observado diverge do contrato. Trocar índice,
aumentar pool ou reiniciar serviço antes disso pode esconder a evidência e
introduzir um segundo defeito.

Este guia usa somente a Inventory API e dados sintéticos do laboratório.
Comandos de inspeção devem ser executados no diretório conferido do projeto.

## Regra principal

```text
sintoma -> linha do tempo -> camada -> hipótese -> menor prova -> correção -> regressão
```

Não comece pela correção. Primeiro escreva:

- request ou operação exata;
- resultado esperado;
- resultado observado;
- horário UTC;
- versões de aplicação e bancos;
- identificador de request/operação;
- primeira e última evidência confiáveis.

Uma mensagem como “a API está lenta” ainda não é um caso reproduzível. “O p95 de
`GET /products?limit=20` passou de 80 ms para 900 ms depois de o fixture crescer
de 1.000 para 100.000 produtos; tempo de pool permaneceu abaixo de 2 ms e o
plano mudou para sequential scan” já aponta uma fronteira investigável.

## O caminho de uma requisição

```text
cliente
  -> resolver/conectar
  -> gateway Nginx
  -> parser e middleware HTTP
  -> validação do DTO
  -> caso de uso
  -> espera pelo pool
  -> transação/consulta PostgreSQL
  -> commit + outbox
  -> serialização e resposta
  -> worker
  -> MongoDB
```

O mesmo erro aparente pode nascer em camadas diferentes. Um `503` pode ser
gateway sem upstream, readiness recusando dependência ou aplicação traduzindo
exaustão. Preserve status, headers, media type, corpo e request ID antes de
formular a hipótese.

## Passo 1 — prove o ambiente

No projeto integrador:

```bash
docker compose config --quiet
docker compose ps
docker compose images
docker compose top
```

Perguntas:

1. todos os serviços esperados existem?
2. estão `healthy`, apenas `running` ou reiniciando?
3. a imagem executada é a que acabou de ser construída?
4. somente o gateway publica porta em `127.0.0.1`?
5. volume e rede pertencem ao projeto correto?

Não use `docker system prune` como diagnóstico. Ele altera outros projetos e
remove evidência. Prefira comandos limitados ao Compose atual.

## Passo 2 — separe liveness de readiness

```bash
curl -i --max-time 5 http://127.0.0.1:8101/health/live
curl -i --max-time 5 http://127.0.0.1:8101/health/ready
```

Interpretação:

| Liveness | Readiness | Hipótese inicial |
|----------|-----------|-------------------|
| falha | falha | gateway/API ausente, porta errada ou processo travado |
| sucesso | falha | processo vivo, dependência/configuração indisponível |
| sucesso | sucesso | caminho básico funciona; reproduza a operação específica |
| falha | sucesso | contrato inconsistente ou cache/proxy incorreto; investigue imediatamente |

Readiness não deve executar trabalho caro nem modificar estado. Ela prova as
dependências mínimas necessárias para aceitar tráfego, dentro de um timeout
menor que o intervalo da probe.

## Passo 3 — capture o contrato HTTP

Use uma chave e dados fictícios exclusivos para reprodução:

```bash
curl --silent --show-error --include --max-time 10 \
  --request POST http://127.0.0.1:8101/api/v1/products \
  --header 'Content-Type: application/json' \
  --header 'Accept: application/json, application/problem+json' \
  --header 'Idempotency-Key: diag-product-001' \
  --data '{"sku":"DIAG-001","name":"Fixture de diagnóstico","priceCents":1000,"initialStock":1}'
```

Guarde somente:

- request sem segredo;
- status;
- `Content-Type`, `Location`, `ETag` e request ID;
- corpo sanitizado;
- duração e horário.

Classifique antes de abrir o código:

- `4xx`: o contrato recusou request, identidade, permissão ou estado atual;
- `5xx`: o servidor não conseguiu cumprir uma entrada potencialmente válida;
- timeout sem resposta: resultado pode ser desconhecido;
- corpo incompatível com `Content-Type`: defeito de protocolo/gateway;
- sucesso com estado errado: invariante, transação ou serialização.

Não use `curl -k` neste laboratório; ele é HTTP local. Em HTTPS real, ignorar
certificado remove justamente a propriedade que deveria ser diagnosticada.

## Passo 4 — correlacione logs

```bash
docker compose logs --since=10m --no-color gateway api
```

Filtre pelo request ID observado. Uma linha útil registra campos estruturados,
não corpo completo:

```text
timestamp, requestId, method, route, status, durationMs, errorCode
```

Evite registrar:

- `Authorization`, cookie ou connection string;
- idempotency key completa quando for tratada como segredo;
- corpo livre com dado pessoal;
- stack trace na resposta;
- uma linha por item de coleção grande.

Ausência de log também é evidência: se o gateway registra e a API não, a
falha está antes do handler ou na conexão ao upstream.

## Passo 5 — PostgreSQL: conexões, transações e locks

Verifique atividade no banco local:

```bash
docker compose exec postgres psql -U inventory -d inventory -P pager=off -c '
SELECT pid, state, wait_event_type, wait_event,
       age(clock_timestamp(), xact_start) AS transaction_age,
       left(query, 120) AS query
FROM pg_stat_activity
WHERE datname = current_database()
ORDER BY xact_start NULLS LAST;'
```

Interprete com cuidado:

- `active`: query executando ou aguardando evento;
- `idle`: conexão aberta sem transação ativa;
- `idle in transaction`: transação aberta sem executar, capaz de manter locks e
  snapshots;
- `wait_event_type = Lock`: existe espera, não necessariamente deadlock;
- transação longa: pode impedir limpeza de versões e ampliar contenção.

Liste locks não concedidos junto à query:

```bash
docker compose exec postgres psql -U inventory -d inventory -P pager=off -c '
SELECT a.pid, l.locktype, l.mode, l.granted,
       age(clock_timestamp(), a.query_start) AS query_age,
       left(a.query, 120) AS query
FROM pg_locks AS l
JOIN pg_stat_activity AS a ON a.pid = l.pid
WHERE NOT l.granted
ORDER BY a.query_start;'
```

Não encerre PID como primeira tentativa. Registre bloqueador, bloqueado, ordem
dos locks e transação que deveria ter terminado. No laboratório descartável,
cancelar pode fazer parte da recuperação depois de preservar a evidência.

## Passo 6 — planos e regressão de consulta

Comece sem executar mutação:

```sql
EXPLAIN (FORMAT JSON)
SELECT id, sku, name
FROM product
WHERE sku = 'DIAG-001';
```

Depois, para `SELECT` seguro com fixture local:

```sql
EXPLAIN (ANALYZE, BUFFERS, WAL, FORMAT JSON)
SELECT id, sku, name
FROM product
WHERE sku = 'DIAG-001';
```

Leia nesta ordem:

1. linhas estimadas versus reais;
2. loops;
3. método de scan e condições;
4. linhas removidas por filtro;
5. buffers hit/read/dirtied;
6. sort em memória ou disco;
7. tempo por nó e total;
8. variação entre execuções aquecidas e frias.

`EXPLAIN ANALYZE` executa a instrução. Para `UPDATE`/`DELETE`, use transação
descartável e rollback somente depois de entender efeitos, triggers e locks:

```sql
BEGIN;
EXPLAIN (ANALYZE, BUFFERS)
UPDATE product SET price_cents = price_cents WHERE false;
ROLLBACK;
```

Um índice não corrige estimativa ruim, semântica errada ou retorno excessivo.
Registre tamanho do fixture, `ANALYZE`, plano anterior e custo de escrita.

## Passo 7 — idempotência e concorrência

Para diagnosticar duplicação, separe três identidades:

- request ID: uma tentativa de transporte;
- idempotency key: várias tentativas da mesma intenção;
- ID do recurso/operação: efeito persistido no domínio.

Repita o mesmo POST com a mesma chave e corpo; depois mantenha a chave e mude o
corpo. O primeiro caso deve recuperar o resultado associado. O segundo deve
recusar conflito, não adotar silenciosamente a nova intenção.

Para lost update:

1. dois clientes fazem GET e recebem a mesma ETag;
2. o primeiro envia `If-Match` e confirma;
3. o segundo envia a ETag antiga;
4. a API rejeita a precondição;
5. o segundo relê e decide, em vez de sobrescrever automaticamente.

Se ambos confirmam, verifique se o `UPDATE` compara versão na mesma instrução e
se o código distingue zero linhas de sucesso.

## Passo 8 — outbox e MongoDB

O commit PostgreSQL e a projeção MongoDB não são simultâneos. Verifique a fonte:

```bash
docker compose exec postgres psql -U inventory -d inventory -P pager=off -c '
SELECT id, event_type, occurred_at, published_at,
       age(clock_timestamp(), occurred_at) AS age
FROM outbox_event
ORDER BY occurred_at DESC
LIMIT 20;'
```

Verifique a projeção:

```bash
docker compose exec mongo mongosh inventory --quiet --eval '
db.audit_events.find({}, {_id: 0, eventId: 1, eventType: 1, occurredAt: 1})
  .sort({occurredAt: -1}).limit(20).toArray()'
```

Estados relevantes:

| PostgreSQL | MongoDB | Interpretação |
|------------|---------|-------------------|
| sem evento | sem documento | transação não gerou outbox ou fez rollback |
| pendente | sem documento | worker ainda não publicou ou falhou |
| publicado | documento presente | convergência esperada |
| pendente | documento presente | publicação ocorreu e marcação falhou; deduplicação deve proteger retry |
| publicado | sem documento | inconsistência: remoção, banco errado ou marcação prematura |

Uma projeção pode estar atrasada sem a fonte estar errada. Meça o atraso e
defina quando ele viola o SLO.

## Matriz de sintomas

| Sintoma | Hipóteses iniciais | Primeira prova |
|---------|--------------------|----------------|
| `502/503` no gateway | API ausente, DNS interno, timeout | `compose ps`, logs das duas camadas |
| readiness falha | PostgreSQL/Mongo/config | corpo da probe e logs correlacionados |
| `422` inesperado | DTO, alias, tipo, limite | Problem Details e OpenAPI executada |
| `409` em retry igual | hash/canonicalização ou chave | registro idempotente e bytes normalizados |
| `412` no primeiro PATCH | ETag incorreta ou estado mudou | GET imediatamente anterior e versão no banco |
| latência sem CPU alta | lock, pool, I/O, dependência | wait events e tempo de pool |
| CPU alta no banco | plano, agregação, cardinalidade | query normalizada e plano real |
| outbox cresce | Mongo/worker/deduplicação | idade do evento e erro do worker |
| evento duplicado | consumidor sem unicidade | índice `eventId` e contagem por ID |
| dados somem após recriar | volume/migration/projeto errado | mounts e nome do projeto Compose |

A tabela gera hipóteses, não diagnósticos automáticos.

## O que não fazer

- reiniciar tudo antes de capturar estado;
- adicionar índice sem consulta e plano;
- aumentar pool sem medir espera e capacidade do banco;
- repetir POST após timeout sem semântica idempotente;
- usar `SELECT *` em evidência que pode conter dado sensível;
- habilitar log de corpo/token para “facilitar”;
- executar `EXPLAIN ANALYZE` de escrita em dado importante sem contenção;
- apagar volume para transformar inconsistência em ambiente vazio;
- corrigir apenas o sintoma manual sem criar teste de regressão.

## Registro de investigação

```markdown
## Caso

- horário UTC:
- versões/digests:
- request/operação:
- resultado esperado:
- resultado observado:
- request ID / operation ID:

## Linha do tempo

1. ...

## Hipóteses

| hipótese | evidência que confirmaria | evidência que rejeitaria |
|----------|---------------------------|--------------------------|
| ... | ... | ... |

## Menor reprodução

- fixture:
- comando:
- saída essencial:

## Causa

- fronteira que divergiu:
- mecanismo:
- por que os testes não detectaram:

## Correção e prova

- mudança:
- teste de regressão:
- sinais após a mudança:
- risco residual:
- cleanup:
```

## Critério de domínio

Você domina este guia quando consegue receber um sintoma, localizar a camada
sem reinício indiscriminado, produzir reprodução mínima, explicar o mecanismo e
converter a descoberta em teste e sinal operacional.
