import { exportDocument, parseDocument } from "./domain.mjs";

export class StorageError extends Error {
  constructor(operation, cause) {
    super(`falha ao ${operation} dados locais`, { cause });
    this.name = "StorageError";
    this.operation = operation;
  }
}

export class LocalSessionRepository {
  constructor(storage, options = {}) {
    for (const method of ["getItem", "setItem", "removeItem"]) {
      if (typeof storage?.[method] !== "function") {
        throw new TypeError(`storage deve implementar ${method}`);
      }
    }
    this.storage = storage;
    this.key = options.key ?? "study-desk:sessions:v1";
    this.now = options.now ?? (() => new Date());
  }

  load() {
    let serialized;
    try {
      serialized = this.storage.getItem(this.key);
    } catch (error) {
      throw new StorageError("ler", error);
    }
    if (serialized === null) return [];
    return [...parseDocument(serialized).sessions];
  }

  save(sessions) {
    const document = exportDocument(sessions, this.now);
    try {
      this.storage.setItem(this.key, JSON.stringify(document));
    } catch (error) {
      throw new StorageError("salvar", error);
    }
  }

  clear() {
    try {
      this.storage.removeItem(this.key);
    } catch (error) {
      throw new StorageError("excluir", error);
    }
  }
}

export class MemoryStorage {
  #values = new Map();

  getItem(key) {
    return this.#values.has(key) ? this.#values.get(key) : null;
  }

  setItem(key, value) {
    this.#values.set(key, String(value));
  }

  removeItem(key) {
    this.#values.delete(key);
  }
}
