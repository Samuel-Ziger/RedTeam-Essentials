import {
  MAX_TITLE_LENGTH,
  PAGE_SIZE,
  buildTasksQuery,
  pageRequiresRestart,
  prepareTitle,
  terminalPageIsIncomplete,
} from "./taskboard-core.mjs";

const REQUEST_TIMEOUT_MS = 8_000;

const elements = {
  form: document.querySelector("#task-form"),
  titleInput: document.querySelector("#task-title"),
  titleCount: document.querySelector("#title-count"),
  submitButton: document.querySelector("#submit-task"),
  taskList: document.querySelector("#tasks"),
  taskSummary: document.querySelector("#task-summary"),
  emptyState: document.querySelector("#empty-state"),
  message: document.querySelector("#message"),
  errorMessage: document.querySelector("#error-message"),
  refreshButton: document.querySelector("#refresh"),
  filter: document.querySelector("#task-filter"),
  loadMoreButton: document.querySelector("#load-more"),
};

const state = {
  tasks: [],
  page: { limit: PAGE_SIZE, offset: 0, total: 0, hasMore: false, revision: 0 },
  filter: "all",
  loaded: false,
  loadFailed: false,
  loading: false,
  activeLoad: null,
  loadGeneration: 0,
};

class ApiRequestError extends Error {
  constructor(message, { status = 0, code = "network_error", requestId = "" } = {}) {
    super(message);
    this.name = "ApiRequestError";
    this.status = status;
    this.code = code;
    this.requestId = requestId;
  }
}

function showStatus(text = "") {
  elements.message.textContent = text;
  elements.errorMessage.hidden = true;
  elements.errorMessage.textContent = "";
}

function showError(error) {
  elements.message.textContent = "";
  const reference = error?.requestId ? ` Referência: ${error.requestId}.` : "";
  elements.errorMessage.textContent = `${error?.message ?? "Erro inesperado."}${reference}`;
  elements.errorMessage.hidden = false;
}

async function api(path, options = {}) {
  const controller = new AbortController();
  const externalSignal = options.signal;
  let timedOut = false;

  const abortFromCaller = () => controller.abort();
  if (externalSignal?.aborted) {
    controller.abort();
  } else {
    externalSignal?.addEventListener("abort", abortFromCaller, { once: true });
  }
  const timeoutId = window.setTimeout(() => {
    timedOut = true;
    controller.abort();
  }, REQUEST_TIMEOUT_MS);

  const headers = new Headers(options.headers ?? {});
  headers.set("Accept", "application/json");
  if (options.body && !headers.has("Content-Type")) {
    headers.set("Content-Type", "application/json");
  }

  let response;
  let text;
  try {
    response = await fetch(path, {
      ...options,
      headers,
      signal: controller.signal,
      cache: "no-store",
      credentials: "same-origin",
    });
    // O timeout cobre também o download do corpo, não apenas os headers.
    text = await response.text();
  } catch (error) {
    if (controller.signal.aborted) {
      if (!timedOut) {
        const cancelled = new Error("Requisição cancelada");
        cancelled.name = "AbortError";
        throw cancelled;
      }
      throw new ApiRequestError("A API demorou mais de 8 segundos para responder.", {
        code: "request_timeout",
      });
    }
    throw new ApiRequestError("Não foi possível conectar à API.", {
      code: "network_error",
    });
  } finally {
    window.clearTimeout(timeoutId);
    externalSignal?.removeEventListener("abort", abortFromCaller);
  }

  const requestId = response.headers.get("X-Request-ID") ?? "";
  let payload = null;
  if (text) {
    try {
      payload = JSON.parse(text);
    } catch {
      throw new ApiRequestError("A API devolveu uma resposta que não é JSON válido.", {
        status: response.status,
        code: "invalid_response",
        requestId,
      });
    }
  }

  if (!response.ok) {
    const apiError = payload?.error;
    const message =
      typeof apiError === "object" && typeof apiError.message === "string"
        ? apiError.message
        : typeof apiError === "string"
          ? apiError
          : `A API respondeu HTTP ${response.status}.`;
    throw new ApiRequestError(message, {
      status: response.status,
      code: typeof apiError?.code === "string" ? apiError.code : "http_error",
      requestId: typeof apiError?.requestId === "string" ? apiError.requestId : requestId,
    });
  }
  return payload;
}

function validateTask(task) {
  const valid =
    task &&
    Number.isSafeInteger(task.id) &&
    task.id > 0 &&
    typeof task.title === "string" &&
    typeof task.done === "boolean" &&
    typeof task.createdAt === "string";
  if (!valid) {
    throw new ApiRequestError("A API devolveu uma tarefa fora do contrato esperado.", {
      code: "invalid_response",
    });
  }
  return task;
}

function validatePage(payload) {
  const page = payload?.page;
  if (
    !Array.isArray(payload?.tasks) ||
    !page ||
    !Number.isSafeInteger(page.limit) ||
    page.limit < 1 ||
    !Number.isSafeInteger(page.offset) ||
    page.offset < 0 ||
    !Number.isSafeInteger(page.total) ||
    page.total < 0 ||
    !Number.isSafeInteger(page.revision) ||
    page.revision < 0 ||
    typeof page.hasMore !== "boolean"
  ) {
    throw new ApiRequestError("A API devolveu uma página fora do contrato esperado.", {
      code: "invalid_response",
    });
  }
  return { tasks: payload.tasks.map(validateTask), page };
}

function formatCreatedAt(value) {
  const date = new Date(value);
  return Number.isNaN(date.getTime())
    ? "data indisponível"
    : new Intl.DateTimeFormat("pt-BR", {
        dateStyle: "short",
        timeStyle: "short",
      }).format(date);
}

function taskElement(task) {
  const item = document.createElement("li");
  item.className = `task${task.done ? " done" : ""}`;
  item.dataset.taskId = String(task.id);

  const checkbox = document.createElement("input");
  checkbox.type = "checkbox";
  checkbox.id = `task-${task.id}`;
  checkbox.checked = task.done;
  checkbox.dataset.action = "toggle";
  checkbox.setAttribute("aria-label", `${task.done ? "Reabrir" : "Concluir"} ${task.title}`);

  const content = document.createElement("div");
  content.className = "task-content";

  const label = document.createElement("label");
  label.htmlFor = checkbox.id;
  label.textContent = task.title;

  const metadata = document.createElement("div");
  metadata.className = "task-metadata";

  const badge = document.createElement("span");
  badge.className = "badge";
  badge.textContent = task.done ? "Concluída" : "Pendente";

  const separator = document.createTextNode(" · ");
  const createdAt = document.createElement("time");
  createdAt.dateTime = task.createdAt;
  createdAt.textContent = `criada em ${formatCreatedAt(task.createdAt)}`;
  metadata.append(badge, separator, createdAt);
  content.append(label, metadata);

  const remove = document.createElement("button");
  remove.type = "button";
  remove.className = "delete";
  remove.dataset.action = "delete";
  remove.textContent = "Remover";
  remove.setAttribute("aria-label", `Remover ${task.title}`);

  item.append(checkbox, content, remove);
  return item;
}

function renderTasks() {
  elements.taskList.replaceChildren(...state.tasks.map(taskElement));
  elements.taskList.setAttribute("aria-busy", String(state.loading));
  elements.emptyState.hidden = state.loading || !state.loaded || state.tasks.length > 0;
  elements.loadMoreButton.hidden = !state.loaded || !state.page.hasMore;
  elements.loadMoreButton.disabled = state.loading;

  const qualifier =
    state.filter === "open"
      ? " pendentes"
      : state.filter === "done"
        ? " concluídas"
        : "";
  elements.taskSummary.textContent = state.loaded
    ? `${state.tasks.length} de ${state.page.total} tarefa${state.page.total === 1 ? "" : "s"}${qualifier}`
    : state.loadFailed
      ? "Não foi possível carregar as tarefas."
      : "Carregando…";
}

function setListLoading(loading) {
  state.loading = loading;
  elements.taskList.setAttribute("aria-busy", String(loading));
  elements.refreshButton.disabled = loading;
  elements.loadMoreButton.disabled = loading;
  elements.refreshButton.textContent = loading ? "Carregando…" : "Atualizar";
}

function invalidateDataLoads() {
  state.loadGeneration += 1;
  const active = state.activeLoad;
  if (!active) return;
  state.activeLoad = null;
  active.abort();
  setListLoading(false);
}

function queryFor(offset) {
  return buildTasksQuery({
    offset,
    filter: state.filter,
    revision: state.page.revision,
  });
}

async function loadTasks({ append = false, announce = false } = {}) {
  state.activeLoad?.abort();
  const controller = new AbortController();
  state.activeLoad = controller;
  const loadGeneration = state.loadGeneration;
  const offset = append ? state.tasks.length : 0;
  if (!state.loaded) {
    state.loadFailed = false;
    elements.taskSummary.textContent = "Carregando…";
  }
  setListLoading(true);
  if (!state.loaded) showStatus("Carregando tarefas…");

  try {
    const payload = await api(`/api/tasks?${queryFor(offset)}`, {
      signal: controller.signal,
    });
    const result = validatePage(payload);
    if (controller !== state.activeLoad || loadGeneration !== state.loadGeneration) return false;

    if (append) {
      if (pageRequiresRestart(state.tasks, state.page, result, offset)) {
        // A API ancora páginas seguintes na revisão da primeira. Estas
        // verificações também defendem o cliente contra respostas defeituosas.
        return await loadTasks({ announce: true });
      }

      const byId = new Map(state.tasks.map((task) => [task.id, task]));
      for (const task of result.tasks) byId.set(task.id, task);
      const merged = [...byId.values()];
      if (terminalPageIsIncomplete(merged.length, result.page)) {
        return await loadTasks({ announce: true });
      }
      state.tasks = merged;
    } else {
      state.tasks = result.tasks;
    }
    state.page = result.page;
    state.loaded = true;
    state.loadFailed = false;
    showStatus(announce ? "Lista atualizada." : "");
    return true;
  } catch (error) {
    if (
      append &&
      error.code === "stale_page" &&
      controller === state.activeLoad &&
      loadGeneration === state.loadGeneration
    ) {
      return await loadTasks({ announce: true });
    }
    if (error.name !== "AbortError") {
      if (!state.loaded) state.loadFailed = true;
      showError(error);
    }
    return false;
  } finally {
    if (controller === state.activeLoad) {
      state.activeLoad = null;
      setListLoading(false);
      renderTasks();
    }
  }
}

function setTaskBusy(taskId, busy) {
  const item = elements.taskList.querySelector(`[data-task-id="${taskId}"]`);
  if (!item) return;
  item.setAttribute("aria-busy", String(busy));
  for (const control of item.querySelectorAll("button, input")) {
    control.disabled = busy;
  }
}

async function toggleTask(taskId, done) {
  const previous = state.tasks.find((task) => task.id === taskId);
  if (!previous) return;
  invalidateDataLoads();
  setTaskBusy(taskId, true);
  try {
    const updated = validateTask(
      await api(`/api/tasks/${taskId}`, {
        method: "PATCH",
        body: JSON.stringify({ done }),
      }),
    );
    invalidateDataLoads();
    state.tasks = state.tasks.map((task) => (task.id === taskId ? updated : task));
    renderTasks();
    const refreshed = await loadTasks();
    if (refreshed) showStatus(done ? "Tarefa concluída." : "Tarefa reaberta.");
    else {
      showError(
        new ApiRequestError(
          "A tarefa foi alterada, mas a lista não pôde ser sincronizada. Atualize-a.",
          { code: "refresh_failed" },
        ),
      );
    }
    elements.taskList.querySelector(`#task-${taskId}`)?.focus();
  } catch (error) {
    renderTasks();
    elements.taskList.querySelector(`#task-${taskId}`)?.focus();
    showError(error);
  } finally {
    setTaskBusy(taskId, false);
  }
}

async function removeTask(taskId) {
  const task = state.tasks.find((candidate) => candidate.id === taskId);
  if (!task) return;
  if (!window.confirm(`Remover a tarefa "${task.title}"?`)) return;

  invalidateDataLoads();
  setTaskBusy(taskId, true);
  try {
    await api(`/api/tasks/${taskId}`, { method: "DELETE" });
    invalidateDataLoads();
    state.tasks = state.tasks.filter((candidate) => candidate.id !== taskId);
    state.page = {
      ...state.page,
      total: Math.max(0, state.page.total - 1),
    };
    renderTasks();
    const refreshed = await loadTasks();
    elements.taskList.querySelector("button, input")?.focus();
    if (refreshed) showStatus("Tarefa removida.");
    else {
      showError(
        new ApiRequestError(
          "A tarefa foi removida, mas a lista não pôde ser sincronizada. Atualize-a.",
          { code: "refresh_failed" },
        ),
      );
    }
  } catch (error) {
    setTaskBusy(taskId, false);
    showError(error);
  }
}

elements.form.addEventListener("submit", async (event) => {
  event.preventDefault();
  const { normalized: title, length: titleLength } = prepareTitle(elements.titleInput.value);
  if (titleLength < 1 || titleLength > MAX_TITLE_LENGTH) {
    elements.titleInput.setCustomValidity(
      titleLength < 1
        ? "Digite um título com pelo menos um caractere."
        : "Use no máximo 120 caracteres após a normalização.",
    );
    elements.titleInput.reportValidity();
    return;
  }

  elements.submitButton.disabled = true;
  elements.submitButton.textContent = "Adicionando…";
  invalidateDataLoads();
  try {
    validateTask(
      await api("/api/tasks", {
        method: "POST",
        body: JSON.stringify({ title }),
      }),
    );
    invalidateDataLoads();
    elements.form.reset();
    elements.titleCount.value = "0/120";
    const refreshed = await loadTasks();
    elements.titleInput.focus();
    if (refreshed) showStatus("Tarefa adicionada.");
    else {
      showError(
        new ApiRequestError(
          "A tarefa foi criada, mas a lista não pôde ser sincronizada. Atualize-a antes de tentar novamente.",
          { code: "refresh_failed" },
        ),
      );
    }
  } catch (error) {
    showError(error);
  } finally {
    elements.submitButton.disabled = false;
    elements.submitButton.textContent = "Adicionar";
  }
});

elements.titleInput.addEventListener("input", () => {
  const { length } = prepareTitle(elements.titleInput.value);
  elements.titleInput.setCustomValidity(
    length > MAX_TITLE_LENGTH ? "Use no máximo 120 caracteres após a normalização." : "",
  );
  elements.titleCount.value = `${length}/120`;
});

elements.taskList.addEventListener("change", (event) => {
  const checkbox = event.target.closest('input[data-action="toggle"]');
  if (!checkbox) return;
  const item = checkbox.closest("[data-task-id]");
  const taskId = Number(item?.dataset.taskId);
  if (Number.isSafeInteger(taskId)) void toggleTask(taskId, checkbox.checked);
});

elements.taskList.addEventListener("click", (event) => {
  const button = event.target.closest('button[data-action="delete"]');
  if (!button) return;
  const item = button.closest("[data-task-id]");
  const taskId = Number(item?.dataset.taskId);
  if (Number.isSafeInteger(taskId)) void removeTask(taskId);
});

elements.refreshButton.addEventListener("click", () => void loadTasks({ announce: true }));
elements.loadMoreButton.addEventListener("click", () => void loadTasks({ append: true }));
elements.filter.addEventListener("change", () => {
  state.filter = elements.filter.value;
  state.loaded = false;
  state.loadFailed = false;
  state.tasks = [];
  renderTasks();
  void loadTasks();
});

window.addEventListener("offline", () => {
  showError(new ApiRequestError("O navegador está offline.", { code: "offline" }));
});
window.addEventListener("online", () => void loadTasks({ announce: true }));

renderTasks();
void loadTasks();
