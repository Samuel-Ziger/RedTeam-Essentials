import test from "node:test";
import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";

import {
  MAX_TITLE_LENGTH,
  buildTasksQuery,
  pageRequiresRestart,
  prepareTitle,
  terminalPageIsIncomplete,
} from "./taskboard-core.mjs";

const webDirectory = new URL("./", import.meta.url);

test("normaliza espaços e conta pontos de código Unicode", () => {
  assert.deepEqual(prepareTitle("  Estudar\n  HTTP  "), {
    normalized: "Estudar HTTP",
    length: 12,
  });
  assert.equal(prepareTitle("😀".repeat(MAX_TITLE_LENGTH)).length, MAX_TITLE_LENGTH);
  assert.equal(prepareTitle("😀".repeat(MAX_TITLE_LENGTH + 1)).length, MAX_TITLE_LENGTH + 1);
});

test("primeira página omite revision e aplica o filtro", () => {
  const query = buildTasksQuery({ offset: 0, filter: "open", revision: 7 });
  assert.equal(query.get("limit"), "25");
  assert.equal(query.get("offset"), "0");
  assert.equal(query.get("done"), "false");
  assert.equal(query.has("revision"), false);
});

test("página seguinte fica ancorada na revision inicial", () => {
  const query = buildTasksQuery({ offset: 25, filter: "done", revision: 7 });
  assert.equal(query.get("offset"), "25");
  assert.equal(query.get("done"), "true");
  assert.equal(query.get("revision"), "7");
});

test("mudança compensatória de coleção reinicia a paginação", () => {
  const currentTasks = [{ id: 3 }, { id: 2 }];
  const currentPage = { total: 4, revision: 8 };
  const result = {
    tasks: [{ id: 1 }],
    page: { total: 4, revision: 10, offset: 2, hasMore: false },
  };
  assert.equal(pageRequiresRestart(currentTasks, currentPage, result, 2), true);
});

test("aceita página coerente e detecta término com item ausente", () => {
  const currentTasks = [{ id: 4 }, { id: 3 }];
  const currentPage = { total: 4, revision: 8 };
  const result = {
    tasks: [{ id: 2 }, { id: 1 }],
    page: { total: 4, revision: 8, offset: 2, hasMore: false },
  };
  assert.equal(pageRequiresRestart(currentTasks, currentPage, result, 2), false);
  assert.equal(terminalPageIsIncomplete(4, result.page), false);
  assert.equal(terminalPageIsIncomplete(3, result.page), true);
});

test("publica o módulo ES com MIME compatível com nosniff", async () => {
  const [nginxConfig, dockerfile] = await Promise.all([
    readFile(new URL("nginx.conf", webDirectory), "utf8"),
    readFile(new URL("Dockerfile", webDirectory), "utf8"),
  ]);

  assert.match(
    nginxConfig,
    /location\s*=\s*\/taskboard-core\.mjs\s*\{[^}]*default_type\s+application\/javascript;/su,
  );
  assert.match(
    dockerfile,
    /COPY[^\n]*\btaskboard-core\.mjs\b/u,
  );
});
