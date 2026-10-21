db = db.getSiblingDB("inventory");

if (!db.getCollectionNames().includes("audit_events")) {
  db.createCollection("audit_events", {
    validator: {
      $jsonSchema: {
        bsonType: "object",
        required: ["eventId", "aggregateId", "type", "occurredAt", "payload"],
        properties: {
          eventId: { bsonType: "string" },
          aggregateId: { bsonType: "string" },
          type: { bsonType: "string" },
          occurredAt: { bsonType: "date" },
          payload: { bsonType: "object" },
        },
      },
    },
  });
}

db.audit_events.createIndex({ eventId: 1 }, { unique: true });
db.audit_events.createIndex({ aggregateId: 1, occurredAt: -1, eventId: -1 });
