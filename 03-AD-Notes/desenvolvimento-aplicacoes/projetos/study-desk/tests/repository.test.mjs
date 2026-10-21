import assert from "node:assert/strict";
import test from "node:test";

import { createSession } from "../src/domain.mjs";
import {
  LocalSessionRepository,
  MemoryStorage,
  StorageError,
} from "../src/repository.mjs";

const fixedDate = new Date("2026-09-30T12:00:00.000Z");

function session() {
  return createSession(
    { title: "Interfaces", minutes: 25 },
    { id: () => "s1", now: () => fixedDate },
  );
}

test("repositorio vazio retorna lista vazia", () => {
  const repository = new LocalSessionRepository(new MemoryStorage());

  assert.deepEqual(repository.load(), []);
});

test("salva e carrega fotografia validada", () => {
  const repository = new LocalSessionRepository(new MemoryStorage(), {
    now: () => fixedDate,
  });
  repository.save([session()]);

  assert.deepEqual(repository.load(), [session()]);
});

test("clear remove o documento", () => {
  const repository = new LocalSessionRepository(new MemoryStorage(), {
    now: () => fixedDate,
  });
  repository.save([session()]);
  repository.clear();

  assert.deepEqual(repository.load(), []);
});

test("documento corrompido falha explicitamente", () => {
  const storage = new MemoryStorage();
  storage.setItem("study-desk:sessions:v1", "nao-json");
  const repository = new LocalSessionRepository(storage);

  assert.throws(() => repository.load(), /JSON invalido/);
});

test("construtor rejeita adapter incompleto", () => {
  assert.throws(() => new LocalSessionRepository({ getItem() {} }), /setItem/);
});

test("falhas do storage possuem operacao e causa", () => {
  const failure = new Error("quota ou permissao");
  const storage = {
    getItem() {
      throw failure;
    },
    setItem() {
      throw failure;
    },
    removeItem() {
      throw failure;
    },
  };
  const repository = new LocalSessionRepository(storage, { now: () => fixedDate });

  for (const [operation, action] of [
    ["ler", () => repository.load()],
    ["salvar", () => repository.save([session()])],
    ["excluir", () => repository.clear()],
  ]) {
    assert.throws(
      action,
      (error) =>
        error instanceof StorageError &&
        error.operation === operation &&
        error.cause === failure,
    );
  }
});

test("entrada invalida falha antes de escrever", () => {
  let writes = 0;
  const storage = {
    getItem: () => null,
    setItem: () => {
      writes += 1;
    },
    removeItem() {},
  };
  const repository = new LocalSessionRepository(storage, { now: () => fixedDate });

  assert.throws(() => repository.save([session(), session()]), /duplicados/);
  assert.equal(writes, 0);
});
