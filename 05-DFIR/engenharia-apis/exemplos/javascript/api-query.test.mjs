import assert from "node:assert/strict";
import test from "node:test";
import { buildQuery } from "./api-query.mjs";

test("monta consulta canonica", () => {
  assert.equal(
    buildQuery(20, "abc_123", "active"),
    "GET /v1/items?limit=20&after=abc_123&status=active",
  );
});

test("rejeita valores invalidos", () => {
  assert.throws(() => buildQuery(0));
  assert.throws(() => buildQuery(1, "bad=token"));
  assert.throws(() => buildQuery(1, "a".repeat(513)));
  assert.throws(() => buildQuery(1, null, "all"));
});
