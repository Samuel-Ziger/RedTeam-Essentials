#!/usr/bin/env node

import { pathToFileURL } from "node:url";

const MAX_RESPONSE_BYTES = 1_000_000;

export class ApiProblem extends Error {
  constructor(status, body) {
    super(`HTTP ${status}: ${body.detail ?? "resposta sem sucesso"}`);
    this.name = "ApiProblem";
    this.status = status;
    this.body = body;
  }
}

async function readLimitedUtf8(response) {
  const declaredLength = Number(response.headers.get("content-length") ?? 0);
  if (!Number.isSafeInteger(declaredLength) || declaredLength < 0) {
    throw new Error("Content-Length inválido na resposta");
  }
  if (declaredLength > MAX_RESPONSE_BYTES) {
    throw new Error("resposta maior que o limite de 1 MB");
  }
  if (response.body === null) {
    return "";
  }

  const reader = response.body.getReader();
  const chunks = [];
  let total = 0;
  try {
    for (;;) {
      const { done, value } = await reader.read();
      if (done) break;
      total += value.byteLength;
      if (total > MAX_RESPONSE_BYTES) {
        await reader.cancel("body limit exceeded");
        throw new Error("resposta maior que o limite de 1 MB");
      }
      chunks.push(value);
    }
  } finally {
    reader.releaseLock();
  }

  const bytes = new Uint8Array(total);
  let offset = 0;
  for (const chunk of chunks) {
    bytes.set(chunk, offset);
    offset += chunk.byteLength;
  }
  try {
    return new TextDecoder("utf-8", { fatal: true }).decode(bytes);
  } catch (error) {
    throw new Error("resposta não contém UTF-8 válido", { cause: error });
  }
}

export async function getJson(baseUrl, path, { timeoutMs = 3_000 } = {}) {
  const response = await fetch(`${baseUrl.replace(/\/$/, "")}${path}`, {
    headers: {
      Accept: "application/json",
      "User-Agent": "rte-javascript-client/1",
    },
    redirect: "error",
    signal: AbortSignal.timeout(timeoutMs),
  });

  const text = await readLimitedUtf8(response);

  let body;
  try {
    body = JSON.parse(text);
  } catch (error) {
    throw new Error("resposta não contém JSON válido", { cause: error });
  }
  if (body === null || Array.isArray(body) || typeof body !== "object") {
    throw new Error("o contrato esperava um objeto JSON");
  }
  if (!response.ok) {
    throw new ApiProblem(response.status, body);
  }
  return {
    body,
    requestId: response.headers.get("x-request-id"),
    status: response.status,
  };
}

function productSummary(value) {
  if (
    value === null ||
    Array.isArray(value) ||
    typeof value !== "object" ||
    typeof value.sku !== "string" ||
    typeof value.name !== "string" ||
    !Number.isSafeInteger(value.stock)
  ) {
    throw new Error("item de produto incompatível com o contrato");
  }
  return `- ${value.sku}: ${value.name} (estoque=${value.stock})`;
}

export async function main() {
  const baseUrl = process.env.INVENTORY_URL ?? "http://127.0.0.1:8101";
  const [health, page] = await Promise.all([
    getJson(baseUrl, "/health/live"),
    getJson(baseUrl, "/api/v1/products?limit=5"),
  ]);
  if (health.body.status !== "ok" || !Array.isArray(page.body.items)) {
    throw new Error("resposta incompatível com o contrato");
  }

  console.log(`health=${health.body.status} request_id=${health.requestId}`);
  console.log(
    `produtos=${page.body.items.length} proximo_cursor=${page.body.nextCursor}`,
  );
  for (const product of page.body.items) {
    console.log(productSummary(product));
  }
}

if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) {
  try {
    await main();
  } catch (error) {
    console.error(`erro: ${error.message}`);
    process.exitCode = 1;
  }
}
