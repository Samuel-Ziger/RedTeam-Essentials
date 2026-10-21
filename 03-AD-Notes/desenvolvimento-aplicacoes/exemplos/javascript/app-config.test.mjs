import assert from "node:assert/strict";
import test from "node:test";

import { resolveProfile } from "./app-config.mjs";

test("usa o padrao", () => {
  assert.deepEqual(resolveProfile(undefined, {}), {
    profile: "development",
    source: "default",
  });
});

test("ambiente substitui o padrao", () => {
  assert.deepEqual(resolveProfile(undefined, { APP_PROFILE: "testing" }), {
    profile: "testing",
    source: "environment",
  });
});

test("CLI substitui o ambiente", () => {
  assert.deepEqual(resolveProfile("production", { APP_PROFILE: "testing" }), {
    profile: "production",
    source: "cli",
  });
});

test("valor direto invalido da CLI e rejeitado", () => {
  assert.throws(() => resolveProfile("other", { APP_PROFILE: "testing" }), /invalido/);
});

test("ambiente invalido e rejeitado", () => {
  assert.throws(() => resolveProfile(undefined, { APP_PROFILE: "other" }), /invalido/);
});
