import assert from "node:assert/strict";
import { after, before, test } from "node:test";
import { spawn } from "node:child_process";
import { createInterface } from "node:readline";
import { fileURLToPath } from "node:url";

import { ApiProblem, getJson } from "./api_client.mjs";

const mockPath = fileURLToPath(new URL("../mock_api.py", import.meta.url));
let server;
let baseUrl;

before(async () => {
  server = spawn("python3", [mockPath], {
    stdio: ["ignore", "pipe", "inherit"],
  });
  const lines = createInterface({ input: server.stdout });
  const port = await new Promise((resolve, reject) => {
    const onExit = (code) => reject(new Error(`mock API encerrou com código ${code}`));
    server.once("exit", onExit);
    lines.once("line", (line) => {
      server.off("exit", onExit);
      resolve(Number(line));
    });
  });
  assert.ok(Number.isInteger(port) && port > 0);
  baseUrl = `http://127.0.0.1:${port}`;
});

after(async () => {
  if (server === undefined || server.exitCode !== null) return;
  server.kill("SIGTERM");
  await new Promise((resolve) => server.once("exit", resolve));
});

test("decodifica sucesso e request ID", async () => {
  const response = await getJson(baseUrl, "/health/live");
  assert.equal(response.status, 200);
  assert.equal(response.requestId, "mock-request-001");
  assert.deepEqual(response.body, { status: "ok" });
});

test("preserva Problem Details em status não 2xx", async () => {
  await assert.rejects(
    getJson(baseUrl, "/problem"),
    (error) =>
      error instanceof ApiProblem &&
      error.status === 409 &&
      error.body.detail === "conflito de teste",
  );
});

test("rejeita JSON inválido e valor raiz que não é objeto", async () => {
  await assert.rejects(getJson(baseUrl, "/invalid-json"), /JSON válido/);
  await assert.rejects(getJson(baseUrl, "/array"), /objeto JSON/);
});

test("interrompe resposta declarada acima de 1 MB", async () => {
  await assert.rejects(getJson(baseUrl, "/too-large"), /limite de 1 MB/);
});

test("não segue redirect silenciosamente", async () => {
  await assert.rejects(getJson(baseUrl, "/redirect"));
});
