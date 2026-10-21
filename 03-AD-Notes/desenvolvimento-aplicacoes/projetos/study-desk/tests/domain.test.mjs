import assert from "node:assert/strict";
import test from "node:test";

import {
  MAX_DOCUMENT_CODE_UNITS,
  ValidationError,
  createSession,
  exportDocument,
  initialState,
  parseDocument,
  reducer,
  summarize,
  visibleSessions,
} from "../src/domain.mjs";

const fixedDate = new Date("2026-09-30T12:00:00.000Z");

function session(id = "s1", title = "Grafos", minutes = 45) {
  return createSession(
    { title, minutes },
    { id: () => id, now: () => fixedDate },
  );
}

test("cria sessao normalizada", () => {
  assert.deepEqual(session(), {
    id: "s1",
    title: "Grafos",
    minutes: 45,
    createdAt: fixedDate.toISOString(),
  });
});

test("converte minutos numericos do formulario", () => {
  assert.equal(
    createSession(
      { title: "API", minutes: "30" },
      { id: () => "s2", now: () => fixedDate },
    ).minutes,
    30,
  );
});

test("rejeita campos invalidos em conjunto", () => {
  assert.throws(
    () => createSession({ title: " ", minutes: "1.5" }),
    (error) =>
      error instanceof ValidationError &&
      Object.keys(error.fields).sort().join(",") === "minutes,title",
  );
});

test("limite de titulo segue unidades de codigo UTF-16", () => {
  assert.equal(session("emoji-40", "😀".repeat(40)).title, "😀".repeat(40));
  assert.throws(
    () => session("emoji-41", "😀".repeat(41)),
    (error) => error instanceof ValidationError && Boolean(error.fields.title),
  );
});

test("reducer adiciona e exclui sem alterar estado anterior", () => {
  const before = initialState();
  const added = reducer(before, { type: "SESSION_ADDED", session: session() });
  const removed = reducer(added, { type: "SESSION_DELETED", id: "s1" });

  assert.equal(before.sessions.length, 0);
  assert.equal(added.sessions.length, 1);
  assert.equal(removed.sessions.length, 0);
});

test("filtra sem diferenciar maiusculas e acentos preservados", () => {
  const state = reducer(initialState([session("1", "Álgebra")]), {
    type: "FILTER_CHANGED",
    query: "álG",
  });

  assert.equal(visibleSessions(state).length, 1);
});

test("resume quantidade e minutos", () => {
  assert.deepEqual(summarize([session("1", "A", 20), session("2", "B", 40)]), {
    count: 2,
    totalMinutes: 60,
  });
});

test("exporta e importa documento equivalente", () => {
  const documentValue = exportDocument([session()], () => fixedDate);
  const parsed = parseDocument(JSON.stringify(documentValue));

  assert.deepEqual(parsed.sessions, documentValue.sessions);
  assert.equal(parsed.schemaVersion, 1);
});

test("rejeita versao futura sem alterar dados", () => {
  const documentValue = {
    ...exportDocument([session()], () => fixedDate),
    schemaVersion: 2,
  };

  assert.throws(() => parseDocument(JSON.stringify(documentValue)), /nao suportada/);
});

test("rejeita campo desconhecido", () => {
  const documentValue = {
    ...exportDocument([session()], () => fixedDate),
    trusted: true,
  };

  assert.throws(() => parseDocument(JSON.stringify(documentValue)), /campos/);
});

test("rejeita IDs duplicados", () => {
  const documentValue = {
    schemaVersion: 1,
    exportedAt: fixedDate.toISOString(),
    sessions: [session(), session()],
  };

  assert.throws(() => parseDocument(JSON.stringify(documentValue)), /duplicados/);
});

test("valida ID e relogio injetados antes de criar sessao", () => {
  assert.throws(
    () =>
      createSession(
        { title: "API", minutes: 20 },
        { id: () => "id inseguro", now: () => fixedDate },
      ),
    /id invalido/,
  );
  assert.throws(
    () =>
      createSession(
        { title: "API", minutes: 20 },
        { id: () => "safe-id", now: () => new Date("invalida") },
      ),
    /data invalida/,
  );
});

test("rejeita caracteres de controle no titulo", () => {
  assert.throws(
    () => createSession({ title: "linha\nnova", minutes: 20 }),
    (error) => error instanceof ValidationError && Boolean(error.fields.title),
  );
});

test("rejeita instante ambiguo ou data impossivel", () => {
  const base = exportDocument([session()], () => fixedDate);
  assert.throws(
    () => parseDocument(JSON.stringify({ ...base, exportedAt: "2026-09-30 12:00:00" })),
    /UTC canonico/,
  );
  assert.throws(
    () => parseDocument(JSON.stringify({ ...base, exportedAt: "2026-02-30T12:00:00.000Z" })),
    /UTC valido/,
  );
});

test("rejeita documento acima do limite antes do parse", () => {
  assert.throws(() => parseDocument("x".repeat(MAX_DOCUMENT_CODE_UNITS + 1)), /excede/);
});

test("exportacao tambem rejeita duplicatas", () => {
  assert.throws(() => exportDocument([session(), session()], () => fixedDate), /duplicados/);
});

test("estado rejeita tema e eventos fora do contrato", () => {
  assert.throws(() => initialState([], "sepia"), /tema invalido/);
  const before = initialState([session()]);
  assert.throws(() => reducer(before, { type: "SESSION_ADDED", session: session() }), /duplicada/);
  assert.throws(() => reducer(before, { type: "SESSOIN_ADDED" }), /desconhecido/);
  assert.equal(before.sessions.length, 1);
});

test("filtro limitado preserva estado anterior na falha", () => {
  const before = initialState([session()]);
  assert.throws(
    () => reducer(before, { type: "FILTER_CHANGED", query: "x".repeat(201) }),
    /no maximo/,
  );
  assert.equal(before.query, "");
});

test("documento aceito e profundamente imutavel nas colecoes", () => {
  const parsed = parseDocument(JSON.stringify(exportDocument([session()], () => fixedDate)));

  assert.equal(Object.isFrozen(parsed), true);
  assert.equal(Object.isFrozen(parsed.sessions), true);
  assert.equal(Object.isFrozen(parsed.sessions[0]), true);
});
