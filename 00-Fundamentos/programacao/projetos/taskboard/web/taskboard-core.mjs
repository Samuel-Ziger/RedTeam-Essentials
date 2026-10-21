export const PAGE_SIZE = 25;
export const MAX_TITLE_LENGTH = 120;

export function prepareTitle(value) {
  const normalized = String(value ?? "").trim().replace(/\s+/gu, " ");
  return {
    normalized,
    length: [...normalized].length,
  };
}

export function buildTasksQuery({ offset, filter, revision }) {
  const query = new URLSearchParams({
    limit: String(PAGE_SIZE),
    offset: String(offset),
  });
  if (filter === "open") query.set("done", "false");
  if (filter === "done") query.set("done", "true");
  if (offset > 0) query.set("revision", String(revision));
  return query;
}

export function pageRequiresRestart(currentTasks, currentPage, result, expectedOffset) {
  const currentIds = new Set(currentTasks.map((task) => task.id));
  return (
    result.page.total !== currentPage.total ||
    result.page.revision !== currentPage.revision ||
    result.page.offset !== expectedOffset ||
    result.tasks.some((task) => currentIds.has(task.id))
  );
}

export function terminalPageIsIncomplete(mergedLength, page) {
  return !page.hasMore && mergedLength !== page.total;
}
