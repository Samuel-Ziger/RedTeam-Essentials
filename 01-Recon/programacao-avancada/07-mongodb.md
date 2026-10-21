# MongoDB em profundidade

MongoDB armazena documentos BSON em coleções. Seu ponto forte é representar um
agregado hierárquico lido e alterado junto. Flexibilidade não elimina modelagem:
tipos, tamanho, índices, validação, versão, atomicidade e evolução continuam
sendo decisões explícitas.

Os comandos usam `mongosh` e dados fictícios. Execute-os somente no
[laboratório MongoDB](referencias/GUIA-LAB-MONGODB.md).

## Objetivos

Ao concluir, você deverá conseguir:

- escolher tipos BSON sem confundir data, número e string;
- decidir entre embutir, referenciar e separar coleções;
- executar CRUD atômico com filtros condicionais;
- impor validação de schema no servidor;
- projetar e medir índices compostos, parciais, multikey e TTL;
- construir aggregation pipelines com grão e limite conhecidos;
- explicar atomicidade, transações e concerns;
- evoluir documentos por versão com migration idempotente;
- impedir filtros arbitrários e consultas sem limite.

## 1. BSON não é JSON textual

BSON possui tipos que JSON não distingue: `ObjectId`, `Date`, inteiros de 32
e 64 bits, `Decimal128`, binário, documentos e arrays.

```javascript
db.audit_events.insertOne({
  eventId: "evt-100",
  aggregateId: "product-100",
  type: "product.created",
  occurredAt: ISODate("2026-10-03T12:00:00Z"),
  schemaVersion: NumberInt(1),
  payload: {
    sku: "BOOK-100",
    priceCents: NumberLong(4500),
  },
});
```

`ISODate(...)` cria BSON Date; uma data entre aspas continua string. No
`mongosh`, use `NumberInt`, `NumberLong` ou `Decimal128` quando o tipo
importar. No driver, confirme como os tipos da linguagem são serializados.

`_id` é obrigatório e possui índice único automático. Um identificador de
domínio ainda pode precisar de unicidade:

```javascript
db.audit_events.createIndex({eventId: 1}, {unique: true});
```

`ObjectId` é identidade prática, não controle de acesso nem relógio global.
MongoDB também limita o tamanho de cada documento; confirme o valor na
documentação da versão. Arrays sem limite são um problema muito antes de atingir
o teto físico.

## 2. Embutir ou referenciar

Um pedido é um bom agregado:

```javascript
{
  _id: "order:o-123",
  schemaVersion: NumberInt(1),
  customerSnapshot: {
    id: "customer:c-9",
    displayName: "Cliente fictício",
  },
  items: [
    {
      sku: "BOOK-1",
      quantity: NumberInt(2),
      unitPriceCents: NumberLong(3500),
    },
  ],
  totalCents: NumberLong(7000),
  currency: "BRL",
  status: "paid",
  createdAt: ISODate("2026-10-03T12:00:00Z"),
}
```

Embutir quando os dados:

- pertencem ao mesmo agregado;
- são lidos e alterados juntos;
- possuem cardinalidade/tamanho limitados;
- precisam de atomicidade no mesmo documento;
- não possuem ciclo de vida independente.

Nome do cliente e preço unitário acima são snapshots históricos; não devem
acompanhar o cadastro e catálogo atuais.

Referenciar ou separar quando:

- o conjunto cresce sem limite;
- a entidade é compartilhada;
- há ciclo de vida, retenção ou permissão própria;
- consultas começam frequentemente pelo elemento;
- atualizar cópias exigiria fan-out;
- o documento ficaria grande ou disputado.

```javascript
{
  _id: "review:r-55",
  bookId: "book:b-10",
  memberId: "member:m-8",
  rating: NumberInt(5),
  createdAt: ISODate("2026-10-03T12:30:00Z"),
}
```

MongoDB não resolve essa referência automaticamente. A aplicação usa consultas
separadas, `$lookup` ou uma projeção. Modelagem documental escolhe quais joins
são pagos na escrita por duplicação e quais permanecem na leitura.

### Buckets com limite

Para muitas medidas pequenas, agrupar por janela pode reduzir overhead:

```javascript
{
  sensorId: "sensor:s-7",
  bucketStart: ISODate("2026-10-03T12:00:00Z"),
  count: NumberInt(2),
  measurements: [
    {offsetSeconds: NumberInt(3), value: 21.4},
    {offsetSeconds: NumberInt(18), value: 21.6},
  ],
}
```

Defina máximo de itens/tamanho, concorrência, atraso e fechamento. Avalie também
coleções time series suportadas pela versão antes de implementar buckets próprios.

## 3. CRUD correto

### Inserir e verificar

```javascript
const result = db.audit_events.insertOne({
  eventId: "evt-101",
  aggregateId: "product-100",
  type: "stock.adjusted",
  occurredAt: ISODate("2026-10-03T13:00:00Z"),
  schemaVersion: NumberInt(1),
  payload: {delta: NumberInt(5), newStock: NumberInt(5)},
});

printjson({acknowledged: result.acknowledged, insertedId: result.insertedId});
```

Duplicar `eventId` produz erro de chave única. A aplicação decide se é replay
da mesma intenção ou conflito diferente; não deve engolir qualquer duplicate key.

### Ler, projetar e ordenar

```javascript
db.audit_events
  .find(
    {aggregateId: "product-100"},
    {_id: 0, eventId: 1, type: 1, occurredAt: 1, payload: 1},
  )
  .sort({occurredAt: -1, eventId: -1})
  .limit(20);
```

Projete só o necessário. O desempate por `eventId` torna a ordem total. Para a
página seguinte:

```javascript
db.audit_events
  .find({
    aggregateId: "product-100",
    $or: [
      {occurredAt: {$lt: ISODate("2026-10-03T13:00:00Z")}},
      {
        occurredAt: ISODate("2026-10-03T13:00:00Z"),
        eventId: {$lt: "evt-101"},
      },
    ],
  })
  .sort({occurredAt: -1, eventId: -1})
  .limit(21);
```

O cursor da API codifica e valida os dois valores, filtros e versão do formato.

### Atualizar atomicamente

```javascript
const result = db.products.updateOne(
  {_id: "product-100", version: NumberInt(4)},
  {
    $set: {name: "Nome revisado", updatedAt: new Date()},
    $inc: {version: NumberInt(1)},
  },
);

printjson({matched: result.matchedCount, modified: result.modifiedCount});
```

O filtro implementa compare-and-set. Zero em `matchedCount` significa ausente
ou versão obsoleta. `modifiedCount` zero pode também significar que o valor já
era igual. Evite ler, alterar o objeto inteiro e chamar `replaceOne`: isso pode
apagar campos gravados concorrentemente e todos os campos omitidos.

Para estoque:

```javascript
const result = db.products.updateOne(
  {_id: "product-100", stock: {$gte: NumberInt(2)}},
  {
    $inc: {stock: NumberInt(-2), version: NumberInt(1)},
    $set: {updatedAt: new Date()},
  },
);
```

A condição e o incremento pertencem à mesma escrita atômica de documento.

### Array limitado

```javascript
db.products.updateOne(
  {_id: "product-100"},
  {
    $push: {
      recentChanges: {
        $each: [{at: new Date(), field: "name"}],
        $sort: {at: -1},
        $slice: 20,
      },
    },
  },
);
```

Isso mantém somente histórico recente; não substitui auditoria completa.

### Excluir com estado

```javascript
const result = db.temporary_exports.deleteOne({
  _id: "export:e-7",
  status: "expired",
});
```

Verifique `deletedCount`. Exclusão numa coleção não apaga automaticamente
cache, projeção ou backup.

## 4. Upsert e idempotência

```javascript
db.event_receipts.updateOne(
  {eventId: "evt-101"},
  {
    $setOnInsert: {
      eventId: "evt-101",
      firstSeenAt: new Date(),
      payloadHash: "sha256:exemplo-ficticio",
    },
    $set: {lastSeenAt: new Date()},
    $inc: {deliveryCount: NumberInt(1)},
  },
  {upsert: true},
);
```

Esse registro mede entregas, mas o efeito de domínio precisa ocorrer uma vez.
Idempotência exige índice único, associação da chave ao conteúdo/escopo e
retenção que cubra o replay. A mesma chave com payload diferente é conflito.
Sem índice único adequado, upserts concorrentes podem criar duplicatas.

## 5. Schema validation

```javascript
db.createCollection("audit_events", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: [
        "eventId",
        "aggregateId",
        "type",
        "occurredAt",
        "schemaVersion",
        "payload",
      ],
      additionalProperties: false,
      properties: {
        _id: {},
        eventId: {bsonType: "string", minLength: 1, maxLength: 80},
        aggregateId: {bsonType: "string", minLength: 1, maxLength: 120},
        type: {
          bsonType: "string",
          pattern: "^[a-z][a-z0-9]*(\\.[a-z][a-z0-9]*)+$",
        },
        occurredAt: {bsonType: "date"},
        schemaVersion: {bsonType: "int", minimum: 1},
        payload: {bsonType: "object"},
      },
    },
  },
  validationLevel: "strict",
  validationAction: "error",
});
```

Com `additionalProperties: false`, declare `_id`, pois ele existe em todos os
documentos. A validação de `payload` acima garante apenas que é objeto; cada
tipo/versão precisa de contrato específico na aplicação ou validator próprio.

Validação da aplicação melhora a resposta; validação no banco protege outros
escritores. Unicidade e concorrência continuam sob índices e filtros atômicos.

`collMod` pode alterar um validator existente. Antes de endurecer:

1. conte documentos incompatíveis;
2. migre em lotes retomáveis;
3. implante leitores compatíveis;
4. observe erros;
5. mude a ação/nível;
6. mantenha correção adiante ou rollback planejado.

Mudar o validator não converte documentos existentes.

## 6. Índices compostos

```javascript
db.audit_events.createIndex(
  {eventId: 1},
  {name: "event_id_unique", unique: true},
);

db.audit_events.createIndex(
  {aggregateId: 1, occurredAt: -1, eventId: -1},
  {name: "aggregate_history"},
);
```

O segundo combina igualdade por agregado, ordenação temporal e desempate. Uma
heurística é Equality, Sort, Range (ESR), mas distribuição e consultas reais
podem justificar outra ordem.

Um índice composto atende prefixos úteis; não atende igualmente uma busca global
somente por `occurredAt` ou `eventId`.

### Parcial

```javascript
db.jobs.createIndex(
  {availableAt: 1, _id: 1},
  {
    name: "pending_jobs",
    partialFilterExpression: {status: "pending"},
  },
);
```

A consulta deve conter condição compatível com o predicado.

### Multikey e `$elemMatch`

```javascript
db.books.createIndex({tags: 1});

db.orders.find({
  items: {
    $elemMatch: {
      sku: "BOOK-1",
      quantity: {$gte: NumberInt(2)},
    },
  },
});
```

Indexar array produz multikey index. Arrays grandes multiplicam entradas.
`$elemMatch` exige que as condições sejam verdadeiras no mesmo elemento; sem
ele, elementos diferentes poderiam satisfazer cada condição. Índices compostos
com múltiplos arrays possuem restrições específicas.

### TTL

```javascript
db.sessions.createIndex(
  {expiresAt: 1},
  {expireAfterSeconds: 0, name: "session_expiry"},
);
```

TTL é remoção assíncrona, não autorização nem cronômetro exato. A aplicação deve
rejeitar `expiresAt <= agora` mesmo antes da limpeza.

Cada índice custa memória, disco e escrita. Um índice único também protege
integridade e não deve ser removido apenas por baixa contagem de leitura.

## 7. Leia o plano

```javascript
db.audit_events
  .explain("executionStats")
  .find({aggregateId: "product-100"})
  .sort({occurredAt: -1, eventId: -1})
  .limit(20);
```

Observe:

- `nReturned`;
- `totalKeysExamined`;
- `totalDocsExamined`;
- `IXSCAN`, `COLLSCAN`, `FETCH` e `SORT`;
- bounds e filtro residual;
- tempo com cautela.

`docsExamined` muito maior que `nReturned` sugere baixa seletividade ou índice
incompleto. `SORT` mostra que a ordem não veio do índice. `COLLSCAN` pode ser
correto para coleção pequena ou consulta que lê quase tudo.

`hint` é ferramenta de diagnóstico, não correção padrão: força uma escolha que
pode piorar quando os dados mudarem.

## 8. Aggregation pipeline

```javascript
db.audit_events.aggregate([
  {
    $match: {
      type: "stock.adjusted",
      occurredAt: {
        $gte: ISODate("2026-10-01T00:00:00Z"),
        $lt: ISODate("2026-11-01T00:00:00Z"),
      },
    },
  },
  {
    $project: {
      _id: 0,
      aggregateId: 1,
      day: {
        $dateTrunc: {
          date: "$occurredAt",
          unit: "day",
          timezone: "UTC",
        },
      },
      delta: "$payload.delta",
    },
  },
  {
    $group: {
      _id: {aggregateId: "$aggregateId", day: "$day"},
      eventCount: {$sum: 1},
      net: {$sum: "$delta"},
    },
  },
  {$sort: {"_id.day": 1, "_id.aggregateId": 1}},
]);
```

Boas regras:

- filtre cedo quando a semântica permitir;
- remova payload grande;
- preserve tipos;
- limite arrays produzidos por `$push`;
- estime multiplicação de `$unwind` e `$lookup`;
- ordene apenas quando exigido;
- leia o plano da pipeline.

`$unwind` transforma cada elemento em documento intermediário. `$lookup`
combina coleções, mas uso frequente e amplo pode revelar fronteira de agregado
ruim. Garanta índice na junção e limite a cardinalidade. Permitir uso de disco
não conserta pipeline ilimitada.

## 9. Atomicidade e transações

Uma escrita de documento é atômica. Uma sequência de duas escritas não é. Para
regra entre documentos, escolha conscientemente:

- remodelar e embutir;
- filtro condicional/compensação;
- transação multidocumento;
- workflow assíncrono com estado;
- outra fonte canônica e projeção.

Transações exigem topologia compatível, como replica set ou cluster sharded
conforme a versão; standalone pode não suportá-las.

```javascript
const session = db.getMongo().startSession();
const sessionDb = session.getDatabase("course");

try {
  session.withTransaction(
    async () => {
      sessionDb.reservations.insertOne({
        _id: "reservation:r-10",
        productId: "product-100",
        quantity: NumberInt(2),
        createdAt: new Date(),
      });

      const inventory = sessionDb.products.updateOne(
        {_id: "product-100", stock: {$gte: NumberInt(2)}},
        {$inc: {stock: NumberInt(-2)}},
      );

      if (inventory.matchedCount !== 1) {
        throw new Error("reservation rejected");
      }
    },
    {
      readConcern: {level: "snapshot"},
      writeConcern: {w: "majority"},
      readPreference: {mode: "primary"},
    },
  );
} finally {
  session.endSession();
}
```

O helper `withTransaction` pode repetir o callback ou o commit em falhas
classificadas como transitórias. Portanto, o callback não pode produzir
HTTP/email ou outro efeito externo irreversível. Drivers têm APIs e políticas de
retry próprias. Transações custam recursos, podem abortar e não corrigem agregado
mal definido. Um commit com resposta perdida pode ter resultado incerto; IDs
idempotentes e a política documentada do driver são obrigatórios.

## 10. Concerns e preferência de leitura

- **write concern:** quando a escrita é reconhecida e por quantos membros;
- **read concern:** garantia de visibilidade/isolamento;
- **read preference:** quais membros podem atender a leitura.

Decida por operação:

- a escrita confirmada pode ser perdida em failover?
- leitura de secundária atrasada é aceitável?
- é necessário read-your-writes?
- qual latência/indisponibilidade é aceita?
- como o cliente reage a resultado incerto?

`majority` não é backup. Ler de secundária não garante menor latência nem dado
atual. Causal consistency em sessão preserva relações suportadas, mas não cria
transação global ou ordem total entre clientes.

## 11. Evolução de documentos

Uma migration inicial idempotente:

```javascript
db.audit_events.updateMany(
  {schemaVersion: {$exists: false}},
  {$set: {schemaVersion: NumberInt(1)}},
);
```

Fluxo profissional:

1. leitor entende v1 e v2;
2. novos escritores gravam v2;
3. backfill percorre lotes por `_id`, com checkpoint;
4. métricas contam pendências e inválidos;
5. validator passa a exigir v2;
6. compatibilidade v1 é removida após telemetria.

O lote precisa ser retomável e condicional à versão antiga. Não use offset
mutável nem carregue toda coleção na memória. Considere impacto em oplog,
replicação, índices, disco e cache.

Lazy migration ao ler distribui custo, mas deixa documentos antigos por tempo
indefinido e torna latência variável. Combine-a com convergência observável.

## 12. Change streams e projeções

Change streams observam mudanças em topologias compatíveis e fornecem resume
tokens. Um consumidor robusto:

- persiste o token depois de efeito idempotente;
- aceita evento repetido;
- monitora lag;
- trata token expirado/inválido;
- consegue reconstruir a projeção;
- versiona payload e reconcilia com a fonte.

Change stream não é fila de retenção infinita. A janela do oplog e os modos de
falha precisam estar no desenho.

## 13. Sharding

A shard key afeta distribuição, roteamento, hot spots, rebalancing, transações e
unicidade. Hash distribui, mas perde localidade de faixa. Range preserva faixa,
mas chaves monotônicas podem concentrar escrita. Chave composta equilibra
trade-offs ao custo de consultas mais complexas.

Antes de escolher:

- meça cardinalidade e frequência;
- modele tenant/chave celebridade;
- liste consultas direcionadas e scatter-gather;
- estime crescimento por shard;
- confirme restrições de índices/unique da versão;
- teste rebalanceamento e falha em ambiente controlado.

## 14. Backup e operação

Replicação também replica exclusão/corrupção. Backup exige RPO/RTO, cópia fora do
domínio de falha, criptografia, retenção e restore cronometrado. Depois do
restore, valide documentos, validators, índices e versão.

Observe:

- conexões e filas;
- working set e I/O;
- queries lentas, keys/docs examined;
- replication lag e janela do oplog;
- tamanho de coleção/índices;
- erros de validação/duplicate key;
- transações longas;
- distribuição de chunks quando aplicável.

## 15. Segurança: construa o filtro

Nunca faça:

```javascript
// Entrada poderia injetar operadores e consultas caras.
db.products.find(request.body.filter);
```

Construa uma allowlist:

```javascript
const filter = {};

if (typeof input.aggregateId !== "string" ||
    input.aggregateId.length < 1 ||
    input.aggregateId.length > 120) {
  throw new Error("aggregateId inválido");
}
filter.aggregateId = input.aggregateId;

const allowedTypes = new Set(["product.created", "stock.adjusted"]);
if (input.type !== undefined) {
  if (!allowedTypes.has(input.type)) {
    throw new Error("type inválido");
  }
  filter.type = input.type;
}

const documents = db.audit_events
  .find(filter, {_id: 0, eventId: 1, type: 1, occurredAt: 1})
  .sort({occurredAt: -1, eventId: -1})
  .limit(100)
  .toArray();
```

Também limite profundidade, arrays, regex, resultado e tempo; aplique tenant e
autorização no servidor; use TLS e menor privilégio; nunca registre connection
string, credencial ou documento sensível.

## 16. Erros recorrentes

- gravar data/número como string;
- criar array sem limite;
- embutir entidade que exige atualização global;
- usar `replaceOne` e apagar mudança concorrente;
- ignorar `matchedCount`;
- indexar toda propriedade;
- presumir que prefixo composto atende qualquer coluna;
- tratar TTL como expiração instantânea;
- usar `$lookup` amplo sem medir;
- usar transação para remendar agregado ruim;
- endurecer validator antes da migration;
- encaminhar filtro do cliente ao driver;
- chamar réplica de backup.

## 17. Exercícios progressivos

Execute primeiro os scripts
[de configuração](laboratorios/mongodb/001_setup.js) e
[de consultas](laboratorios/mongodb/002_queries.js).

### Nível 1 — tipos e CRUD

1. Insira evento com Date, `NumberInt` e `NumberLong`.
2. Tente inserir `occurredAt` como string e registre o erro.
3. Atualize produto com versão; demonstre conflito usando versão antiga.
4. Compare `$set` a `replaceOne` diante de campo concorrente.

### Nível 2 — modelo e índice

1. Modele pedido embutido e defina limite.
2. Modele avaliações referenciadas e justifique.
3. Compare keys/docs examined antes/depois do índice de histórico.
4. Faça paginação com empate em `occurredAt`.
5. Demonstre a semântica de `$elemMatch`.

### Nível 3 — agregação e evolução

1. Agregue ajustes por agregado e dia UTC.
2. Declare o grão após cada estágio.
3. Migre `schemaVersion` idempotentemente.
4. Planeje v1→v2 com leitor dual, backfill, métrica e validator final.

### Nível 4 — concorrência e operação

1. Execute updates concorrentes e preserve estoque não negativo.
2. Explique quando embutir elimina uma transação multidocumento.
3. Em replica set local, teste commit e abort.
4. Desenhe resposta a commit incerto com ID de intenção.
5. Defina concerns para histórico e saldo.
6. Restaure um backup fictício e valide índices/validator.

## Critério de conclusão

- [ ] Tipos BSON e unidades estão explícitos.
- [ ] Cada agregado possui dono e limite de crescimento.
- [ ] Updates são atômicos e suas contagens são verificadas.
- [ ] Validator, aplicação e índices protegem regras complementares.
- [ ] Cada índice corresponde a filtro/ordem medidos.
- [ ] Pipelines possuem grão, limite e plano.
- [ ] Sei quando embutir e quando usar transação.
- [ ] Concerns vêm de requisitos de falha.
- [ ] Migration é versionada, idempotente e observável.
- [ ] Nenhum filtro do cliente chega diretamente ao driver.
- [ ] Backup foi restaurado; réplica não foi chamada de backup.

Depois, conecte persistência ao caminho completo da requisição em
[Anatomia completa de uma API](08-anatomia-api.md).
