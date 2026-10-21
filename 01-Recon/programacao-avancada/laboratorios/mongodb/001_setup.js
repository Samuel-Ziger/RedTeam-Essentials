db = db.getSiblingDB("course");
db.audit_events.drop();

db.createCollection("audit_events", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["eventId", "aggregateId", "type", "occurredAt", "schemaVersion", "payload"],
      properties: {
        eventId: { bsonType: "string" },
        aggregateId: { bsonType: "string" },
        type: { bsonType: "string" },
        occurredAt: { bsonType: "date" },
        schemaVersion: { bsonType: "int", minimum: 1 },
        payload: { bsonType: "object" },
      },
    },
  },
});

db.audit_events.createIndex({ eventId: 1 }, { unique: true });
db.audit_events.createIndex({ aggregateId: 1, occurredAt: -1, eventId: -1 });

db.audit_events.insertMany([
  {
    eventId: "evt-001",
    aggregateId: "product-001",
    type: "product.created",
    occurredAt: ISODate("2026-09-28T10:00:00Z"),
    schemaVersion: NumberInt(1),
    payload: { sku: "BOOK-001", priceCents: 4500 },
  },
  {
    eventId: "evt-002",
    aggregateId: "product-001",
    type: "stock.adjusted",
    occurredAt: ISODate("2026-09-28T11:00:00Z"),
    schemaVersion: NumberInt(1),
    payload: { delta: 10, newStock: 10 },
  },
  {
    eventId: "evt-003",
    aggregateId: "product-001",
    type: "stock.adjusted",
    occurredAt: ISODate("2026-09-29T09:00:00Z"),
    schemaVersion: NumberInt(1),
    payload: { delta: -2, newStock: 8 },
  },
]);

printjson({ status: "ok", documents: db.audit_events.countDocuments({}) });
