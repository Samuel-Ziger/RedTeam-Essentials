import {
  MAX_DOCUMENT_BYTES,
  ValidationError,
  createSession,
  exportDocument,
  initialState,
  parseDocument,
  reducer,
  summarize,
  visibleSessions,
} from "./domain.mjs";
import { LocalSessionRepository, MemoryStorage } from "./repository.mjs";

const startupMessages = [];
let persistentStorage = true;
let storage;
try {
  storage = window.localStorage;
} catch (error) {
  persistentStorage = false;
  storage = new MemoryStorage();
  startupMessages.push(
    `O armazenamento persistente está bloqueado: ${error.message}. Alterações valerão apenas nesta aba.`,
  );
}

let savedTheme = null;
try {
  savedTheme = storage.getItem("study-desk:theme");
} catch (error) {
  persistentStorage = false;
  storage = new MemoryStorage();
  startupMessages.push(
    `O armazenamento persistente não pôde ser lido: ${error.message}. Alterações valerão apenas nesta aba.`,
  );
}
const initialTheme = savedTheme === "dark" ? "dark" : "light";
let repository = new LocalSessionRepository(storage);

const elements = {
  form: document.querySelector("#session-form"),
  title: document.querySelector("#title"),
  minutes: document.querySelector("#minutes"),
  titleError: document.querySelector("#title-error"),
  minutesError: document.querySelector("#minutes-error"),
  filter: document.querySelector("#filter"),
  list: document.querySelector("#session-list"),
  empty: document.querySelector("#empty-state"),
  summary: document.querySelector("#summary"),
  status: document.querySelector("#status"),
  exportButton: document.querySelector("#export-button"),
  importInput: document.querySelector("#import-input"),
  clearButton: document.querySelector("#clear-button"),
  themeToggle: document.querySelector("#theme-toggle"),
};

let state;
try {
  state = initialState(repository.load(), initialTheme);
} catch (error) {
  persistentStorage = false;
  storage = new MemoryStorage();
  repository = new LocalSessionRepository(storage);
  state = initialState([], initialTheme);
  startupMessages.push(
    `Os dados persistidos não puderam ser lidos e foram preservados: ${error.message}. Alterações valerão apenas nesta aba.`,
  );
}

const dateFormatter = new Intl.DateTimeFormat("pt-BR", {
  dateStyle: "short",
  timeStyle: "short",
});

function setStatus(message) {
  elements.status.textContent = message;
}

function durableStatus(message) {
  return persistentStorage
    ? message
    : `${message} Alteração mantida apenas nesta aba; exporte uma cópia antes de fechá-la.`;
}

function persist() {
  try {
    repository.save(state.sessions);
    return true;
  } catch (error) {
    setStatus(`Não foi possível salvar localmente: ${error.message}`);
    return false;
  }
}

function dispatch(event, options = {}) {
  const previous = state;
  state = reducer(state, event);
  if (options.persist && !persist()) {
    state = previous;
    render();
    return false;
  }
  render();
  return true;
}

function render() {
  const visible = visibleSessions(state);
  const totals = summarize(visible);
  elements.list.replaceChildren(...visible.map(sessionElement));
  elements.empty.hidden = visible.length > 0;
  elements.summary.textContent =
    totals.count === 0
      ? "Nenhuma sessão encontrada."
      : `${totals.count} ${totals.count === 1 ? "sessão" : "sessões"} · ${totals.totalMinutes} min`;
  document.documentElement.dataset.theme = state.theme;
  const dark = state.theme === "dark";
  elements.themeToggle.setAttribute("aria-pressed", String(dark));
  elements.themeToggle.textContent = dark ? "Usar tema claro" : "Usar tema escuro";
}

function sessionElement(session) {
  const item = document.createElement("li");
  item.className = "session-card";

  const content = document.createElement("div");
  const title = document.createElement("p");
  const strong = document.createElement("strong");
  strong.textContent = session.title;
  title.append(strong);

  const meta = document.createElement("p");
  meta.className = "session-meta";
  meta.textContent = `${session.minutes} min · ${dateFormatter.format(new Date(session.createdAt))}`;
  content.append(title, meta);

  const remove = document.createElement("button");
  remove.className = "danger";
  remove.type = "button";
  remove.dataset.deleteId = session.id;
  remove.textContent = "Excluir";
  remove.setAttribute("aria-label", `Excluir sessão ${session.title}`);
  item.append(content, remove);
  return item;
}

function clearErrors() {
  for (const [input, output] of [
    [elements.title, elements.titleError],
    [elements.minutes, elements.minutesError],
  ]) {
    input.removeAttribute("aria-invalid");
    output.textContent = "";
  }
}

function showErrors(fields) {
  const pairs = [
    ["title", elements.title, elements.titleError],
    ["minutes", elements.minutes, elements.minutesError],
  ];
  for (const [name, input, output] of pairs) {
    if (fields[name]) {
      input.setAttribute("aria-invalid", "true");
      output.textContent = fields[name];
    }
  }
  const firstInvalid = pairs.find(([name]) => fields[name]);
  firstInvalid?.[1].focus();
}

elements.form.addEventListener("submit", (event) => {
  event.preventDefault();
  clearErrors();
  try {
    const session = createSession({
      title: elements.title.value,
      minutes: elements.minutes.value,
    });
    if (dispatch({ type: "SESSION_ADDED", session }, { persist: true })) {
      elements.form.reset();
      elements.title.focus();
      setStatus(durableStatus(`Sessão ${session.title} registrada.`));
    }
  } catch (error) {
    if (error instanceof ValidationError) {
      showErrors(error.fields);
      setStatus("Revise os campos indicados.");
    } else {
      setStatus(`Não foi possível registrar: ${error.message}`);
    }
  }
});

elements.filter.addEventListener("input", () => {
  dispatch({ type: "FILTER_CHANGED", query: elements.filter.value });
});

elements.list.addEventListener("click", (event) => {
  const button = event.target.closest("button[data-delete-id]");
  if (!button) return;
  const session = state.sessions.find((item) => item.id === button.dataset.deleteId);
  if (!session) return;
  const visibleIndex = visibleSessions(state).findIndex((item) => item.id === session.id);
  if (!window.confirm(`Excluir a sessão ${session.title}?`)) return;

  const committed = dispatch(
    { type: "SESSION_DELETED", id: session.id },
    { persist: true },
  );
  const remainingButtons = [...elements.list.querySelectorAll("button[data-delete-id]")];
  const restoredButton = remainingButtons.find(
    (item) => item.dataset.deleteId === session.id,
  );
  const adjacentButton =
    remainingButtons[Math.min(visibleIndex, remainingButtons.length - 1)];
  (restoredButton ?? adjacentButton ?? elements.filter).focus();
  if (committed) {
    setStatus(durableStatus(`Sessão ${session.title} excluída.`));
  }
});

elements.themeToggle.addEventListener("click", () => {
  const theme = state.theme === "dark" ? "light" : "dark";
  dispatch({ type: "THEME_CHANGED", theme });
  try {
    storage.setItem("study-desk:theme", theme);
    if (!persistentStorage) {
      setStatus("O tema mudou apenas nesta aba.");
    }
  } catch (error) {
    setStatus(`O tema mudou apenas nesta sessão: ${error.message}`);
  }
});

elements.exportButton.addEventListener("click", () => {
  const blob = new Blob([JSON.stringify(exportDocument(state.sessions), null, 2)], {
    type: "application/json",
  });
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = "study-desk-export.json";
  link.click();
  setTimeout(() => URL.revokeObjectURL(url), 0);
  setStatus("Cópia JSON exportada.");
});

elements.importInput.addEventListener("change", async () => {
  const [file] = elements.importInput.files;
  if (!file) return;
  try {
    if (file.size > MAX_DOCUMENT_BYTES) throw new Error("o arquivo excede 5 MB");
    const documentValue = parseDocument(await file.text());
    const confirmed = window.confirm(
      `Substituir os dados atuais por ${documentValue.sessions.length} sessões importadas?`,
    );
    if (confirmed) {
      if (
        dispatch(
          { type: "SESSIONS_REPLACED", sessions: documentValue.sessions },
          { persist: true },
        )
      ) {
        setStatus(
          durableStatus(`${documentValue.sessions.length} sessões importadas.`),
        );
      }
    } else {
      setStatus("Importação cancelada; os dados não foram alterados.");
    }
  } catch (error) {
    setStatus(`Não foi possível importar: ${error.message}`);
  } finally {
    elements.importInput.value = "";
  }
});

elements.clearButton.addEventListener("click", () => {
  if (state.sessions.length === 0) {
    setStatus("Não há sessões para excluir.");
    return;
  }
  if (window.confirm("Excluir todas as sessões deste navegador?")) {
    if (dispatch({ type: "SESSIONS_REPLACED", sessions: [] }, { persist: true })) {
      setStatus(durableStatus("Todas as sessões foram excluídas."));
    }
  }
});

render();
if (startupMessages.length > 0) setStatus(startupMessages.join(" "));
