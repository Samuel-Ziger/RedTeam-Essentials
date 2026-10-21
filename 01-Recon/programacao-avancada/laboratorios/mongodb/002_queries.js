db = db.getSiblingDB("course");

print("Histórico do agregado:");
db.audit_events
  .find(
    { aggregateId: "product-001" },
    { _id: 0, eventId: 1, type: 1, occurredAt: 1, payload: 1 },
  )
  .sort({ occurredAt: -1, eventId: -1 })
  .forEach((document) => printjson(document));

print("Resumo de movimentos:");
db.audit_events
  .aggregate([
    { $match: { type: "stock.adjusted" } },
    {
      $group: {
        _id: "$aggregateId",
        events: { $sum: 1 },
        net: { $sum: "$payload.delta" },
      },
    },
    { $sort: { events: -1, _id: 1 } },
  ])
  .forEach((document) => printjson(document));

print("Plano da consulta principal:");
printjson(
  db.audit_events
    .find({ aggregateId: "product-001" })
    .sort({ occurredAt: -1, eventId: -1 })
    .explain("executionStats"),
);
