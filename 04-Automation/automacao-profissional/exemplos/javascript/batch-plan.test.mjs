import assert from "node:assert/strict";
import test from "node:test";
import { plan } from "./batch-plan.mjs";

test("deduplica e ordena", () => {
  assert.deepEqual(plan("build,test,build,deploy"), ["build", "deploy", "test"]);
});

test("rejeita ID inseguro", () => {
  assert.throws(() => plan("ok,../x"), /IDs/);
});

test("rejeita mais de 64 IDs", () => {
  assert.throws(() => plan(Array.from({ length: 65 }, (_, i) => `id${i}`).join(",")), /64/);
});

test("rejeita mais de 1023 bytes", () => {
  assert.throws(() => plan("a".repeat(1024)), /1023/);
});
