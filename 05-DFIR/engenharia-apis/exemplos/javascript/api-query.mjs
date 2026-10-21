import { fileURLToPath } from "node:url";

const token = /^[A-Za-z0-9_-]+$/;

export function buildQuery(limit, after = null, status = null) {
  if (!Number.isInteger(limit) || limit < 1 || limit > 100) throw new Error("limit invalido");
  if (after !== null && (after.length > 512 || !token.test(after))) throw new Error("after invalido");
  if (status !== null && !["active", "archived"].includes(status)) throw new Error("status invalido");
  const parts = [`limit=${limit}`];
  if (after !== null) parts.push(`after=${after}`);
  if (status !== null) parts.push(`status=${status}`);
  return `GET /v1/items?${parts.join("&")}`;
}

if (fileURLToPath(import.meta.url) === process.argv[1]) {
  const values = new Map();
  try {
    const allowed = new Set(["--limit", "--after", "--status"]);
    for (let i = 2; i < process.argv.length; i += 2) {
      const option = process.argv[i];
      if (i + 1 >= process.argv.length) throw new Error("valor ausente");
      if (!allowed.has(option)) throw new Error("argumento desconhecido");
      if (values.has(option)) throw new Error("argumento repetido");
      values.set(option, process.argv[i + 1]);
    }
    console.log(buildQuery(Number(values.get("--limit")), values.get("--after"), values.get("--status")));
  } catch (error) {
    console.error(error.message);
    process.exitCode = 2;
  }
}
