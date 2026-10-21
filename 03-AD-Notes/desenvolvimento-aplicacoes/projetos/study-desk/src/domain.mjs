export const SCHEMA_VERSION = 1;
export const MAX_SESSIONS = 10_000;
export const MAX_DOCUMENT_BYTES = 5_000_000;
export const MAX_DOCUMENT_CODE_UNITS = 5_000_000;
export const MAX_TITLE_CODE_UNITS = 80;
export const MAX_FILTER_CODE_UNITS = 200;

const SAFE_ID = /^[A-Za-z0-9][A-Za-z0-9._-]{0,119}$/;
const CONTROL_CHARACTER = /[\u0000-\u001f\u007f-\u009f]/u;
const CANONICAL_INSTANT = /^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}Z$/;
const THEMES = new Set(["light", "dark"]);

export class ValidationError extends Error {
  constructor(fields) {
    super("dados invalidos");
    this.name = "ValidationError";
    this.fields = Object.freeze({ ...fields });
  }
}

function exactKeys(value, expected, context) {
  if (value === null || typeof value !== "object" || Array.isArray(value)) {
    throw new Error(`${context} deve ser um objeto`);
  }
  const actual = Object.keys(value).sort();
  const wanted = [...expected].sort();
  if (actual.length !== wanted.length || actual.some((key, index) => key !== wanted[index])) {
    throw new Error(`${context} possui campos ausentes ou desconhecidos`);
  }
}

function parseMinutes(value) {
  if (typeof value === "string" && /^\d+$/.test(value.trim())) {
    return Number(value);
  }
  return value;
}

function canonicalInstant(value, field) {
  if (typeof value !== "string" || !CANONICAL_INSTANT.test(value)) {
    throw new Error(`${field} deve ser um instante UTC canonico`);
  }
  const milliseconds = Date.parse(value);
  if (!Number.isFinite(milliseconds) || new Date(milliseconds).toISOString() !== value) {
    throw new Error(`${field} deve ser um instante UTC valido`);
  }
  return value;
}

function instantFromClock(clock, field) {
  const value = clock();
  if (!(value instanceof Date) || !Number.isFinite(value.getTime())) {
    throw new Error(`${field} retornou uma data invalida`);
  }
  return value.toISOString();
}

function validateTheme(theme) {
  if (!THEMES.has(theme)) throw new Error(`tema invalido: ${theme}`);
  return theme;
}

export function createSession(input, dependencies = {}) {
  const title = typeof input?.title === "string" ? input.title.trim() : "";
  const minutes = parseMinutes(input?.minutes);
  const fields = {};

  if (
    title.length === 0 ||
    title.length > MAX_TITLE_CODE_UNITS ||
    CONTROL_CHARACTER.test(title)
  ) {
    fields.title = `Informe um assunto entre 1 e ${MAX_TITLE_CODE_UNITS} posições de texto, sem controles.`;
  }
  if (!Number.isInteger(minutes) || minutes < 1 || minutes > 1440) {
    fields.minutes = "Informe minutos inteiros entre 1 e 1440.";
  }
  if (Object.keys(fields).length > 0) throw new ValidationError(fields);

  const now = dependencies.now ?? (() => new Date());
  const id = dependencies.id ?? (() => crypto.randomUUID());
  return validateSession({
    id: id(),
    title,
    minutes,
    createdAt: instantFromClock(now, "now"),
  });
}

export function validateSession(value, index = 0) {
  exactKeys(value, ["id", "title", "minutes", "createdAt"], `sessions[${index}]`);
  if (typeof value.id !== "string" || !SAFE_ID.test(value.id)) {
    throw new Error(`sessions[${index}].id invalido`);
  }
  if (
    typeof value.title !== "string" ||
    value.title.trim() !== value.title ||
    value.title.length === 0 ||
    value.title.length > MAX_TITLE_CODE_UNITS ||
    CONTROL_CHARACTER.test(value.title)
  ) {
    throw new Error(`sessions[${index}].title invalido`);
  }
  if (!Number.isInteger(value.minutes) || value.minutes < 1 || value.minutes > 1440) {
    throw new Error(`sessions[${index}].minutes invalido`);
  }
  canonicalInstant(value.createdAt, `sessions[${index}].createdAt`);
  return Object.freeze({ ...value });
}

export function validateSessions(values) {
  if (!Array.isArray(values) || values.length > MAX_SESSIONS) {
    throw new Error(`sessions deve ser uma lista com no maximo ${MAX_SESSIONS} itens`);
  }
  const sessions = values.map(validateSession);
  const ids = new Set(sessions.map((session) => session.id));
  if (ids.size !== sessions.length) throw new Error("ids de sessao duplicados");
  return Object.freeze(sessions);
}

export function parseDocument(text) {
  if (typeof text !== "string") throw new TypeError("documento deve ser texto JSON");
  if (text.length > MAX_DOCUMENT_CODE_UNITS) {
    throw new Error(`documento excede ${MAX_DOCUMENT_CODE_UNITS} unidades UTF-16`);
  }

  let value;
  try {
    value = JSON.parse(text);
  } catch (error) {
    throw new Error(`JSON invalido: ${error.message}`, { cause: error });
  }
  exactKeys(value, ["schemaVersion", "exportedAt", "sessions"], "documento");
  if (value.schemaVersion !== SCHEMA_VERSION) {
    throw new Error(`schemaVersion nao suportada: ${value.schemaVersion}`);
  }
  canonicalInstant(value.exportedAt, "exportedAt");
  return Object.freeze({
    schemaVersion: SCHEMA_VERSION,
    exportedAt: value.exportedAt,
    sessions: validateSessions(value.sessions),
  });
}

export function exportDocument(sessions, now = () => new Date()) {
  return Object.freeze({
    schemaVersion: SCHEMA_VERSION,
    exportedAt: instantFromClock(now, "relogio de exportacao"),
    sessions: validateSessions(sessions),
  });
}

export function initialState(sessions = [], theme = "light") {
  return Object.freeze({
    sessions: validateSessions(sessions),
    query: "",
    theme: validateTheme(theme),
  });
}

export function reducer(state, event) {
  if (event === null || typeof event !== "object" || typeof event.type !== "string") {
    throw new Error("evento deve possuir um tipo");
  }

  switch (event.type) {
    case "SESSION_ADDED": {
      const session = validateSession(event.session);
      if (state.sessions.some((item) => item.id === session.id)) {
        throw new Error(`sessao duplicada: ${session.id}`);
      }
      return Object.freeze({
        ...state,
        sessions: validateSessions([session, ...state.sessions]),
      });
    }
    case "SESSION_DELETED":
      if (typeof event.id !== "string" || !SAFE_ID.test(event.id)) {
        throw new Error("SESSION_DELETED exige ID valido");
      }
      return Object.freeze({
        ...state,
        sessions: Object.freeze(state.sessions.filter((item) => item.id !== event.id)),
      });
    case "SESSIONS_REPLACED":
      return Object.freeze({ ...state, sessions: validateSessions(event.sessions) });
    case "FILTER_CHANGED":
      if (
        typeof event.query !== "string" ||
        event.query.length > MAX_FILTER_CODE_UNITS ||
        CONTROL_CHARACTER.test(event.query)
      ) {
        throw new Error(`filtro deve ter no maximo ${MAX_FILTER_CODE_UNITS} unidades UTF-16`);
      }
      return Object.freeze({ ...state, query: event.query });
    case "THEME_CHANGED":
      return Object.freeze({ ...state, theme: validateTheme(event.theme) });
    default:
      throw new Error(`evento desconhecido: ${event.type}`);
  }
}

export function visibleSessions(state) {
  const query = state.query.trim().toLocaleLowerCase("pt-BR");
  if (!query) return state.sessions;
  return state.sessions.filter((session) =>
    session.title.toLocaleLowerCase("pt-BR").includes(query),
  );
}

export function summarize(sessions) {
  return Object.freeze({
    count: sessions.length,
    totalMinutes: sessions.reduce((total, session) => total + session.minutes, 0),
  });
}
