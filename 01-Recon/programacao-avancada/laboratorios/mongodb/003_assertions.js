db = db.getSiblingDB("course");

assert.eq(3, db.audit_events.countDocuments({}), "quantidade inicial de eventos");
assert.eq(
  3,
  db.audit_events.countDocuments({ aggregateId: "product-001" }),
  "histórico do agregado",
);

const indexNames = db.audit_events.getIndexes().map((index) => index.name);
assert(indexNames.includes("eventId_1"), "índice único de eventId ausente");
assert(
  indexNames.includes("aggregateId_1_occurredAt_-1_eventId_-1"),
  "índice do histórico por agregado ausente",
);

let invalidRejected = false;
try {
  db.audit_events.insertOne({
    eventId: "invalid-event",
    aggregateId: "product-001",
    type: "invalid",
    occurredAt: "não é uma data BSON",
    schemaVersion: NumberInt(1),
    payload: {},
  });
} catch (error) {
  invalidRejected = true;
}
assert(invalidRejected, "validator deveria rejeitar occurredAt como string");
assert.eq(0, db.audit_events.countDocuments({ eventId: "invalid-event" }));

let duplicateRejected = false;
try {
  db.audit_events.insertOne({
    eventId: "evt-001",
    aggregateId: "other-product",
    type: "product.created",
    occurredAt: ISODate("2026-10-01T00:00:00Z"),
    schemaVersion: NumberInt(1),
    payload: {},
  });
} catch (error) {
  duplicateRejected = true;
}
assert(duplicateRejected, "índice único deveria rejeitar eventId repetido");

const [summary] = db.audit_events
  .aggregate([
    { $match: { aggregateId: "product-001", type: "stock.adjusted" } },
    {
      $group: {
        _id: "$aggregateId",
        events: { $sum: 1 },
        net: { $sum: "$payload.delta" },
      },
    },
  ])
  .toArray();

assert.eq(2, summary.events, "quantidade de ajustes");
assert.eq(8, summary.net, "saldo líquido dos ajustes");

const execution = db.audit_events
  .find({ aggregateId: "product-001" })
  .sort({ occurredAt: -1, eventId: -1 })
  .hint("aggregateId_1_occurredAt_-1_eventId_-1")
  .explain("executionStats");
assert.eq(3, execution.executionStats.nReturned, "documentos retornados pelo plano");
assert(
  execution.executionStats.totalKeysExamined <= 3,
  `consulta examinou ${execution.executionStats.totalKeysExamined} chaves para 3 eventos`,
);

printjson({ status: "ok", assertions: 10 });
