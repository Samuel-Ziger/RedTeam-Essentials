import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import test from "node:test";

const html = await readFile(new URL("../index.html", import.meta.url), "utf8");
const app = await readFile(new URL("../src/app.mjs", import.meta.url), "utf8");

test("documento declara idioma, viewport e titulo", () => {
  assert.match(html, /<html lang="pt-BR">/);
  assert.match(html, /name="viewport"/);
  assert.match(html, /<title>Study Desk<\/title>/);
});

test("formulario associa rotulos e controles", () => {
  for (const id of ["title", "minutes", "filter", "import-input"]) {
    assert.match(html, new RegExp(`(?:for|id)="${id}"`));
  }
  assert.match(
    html,
    /<label class="file-button">[\s\S]*?<input id="import-input"[\s\S]*?<\/label>/,
  );
});

test("possui atalho, main e regiao de status", () => {
  assert.match(html, /class="skip-link"/);
  assert.match(html, /<main[^>]+id="main-content"/);
  assert.match(html, /role="status"/);
  assert.match(html, /aria-atomic="true"/);
});

test("nao possui handlers ou scripts inline", () => {
  assert.doesNotMatch(html, /\son[a-z]+=/i);
  assert.doesNotMatch(html, /<script(?![^>]+src=)/i);
});

test("declara politica local de conteudo e referencia", () => {
  assert.match(html, /Content-Security-Policy/);
  assert.match(html, /default-src 'self'/);
  assert.match(html, /name="referrer" content="no-referrer"/);
});

test("limites de formulario refletem o dominio", () => {
  assert.match(html, /id="title"[^>]+maxlength="80"/);
  assert.match(html, /id="minutes"[^>]+min="1"[^>]+max="1440"/);
  assert.match(html, /id="filter"[^>]+maxlength="200"/);
});

test("conteudo importado nunca e interpretado como HTML", () => {
  assert.doesNotMatch(app, /\.innerHTML\s*=|insertAdjacentHTML|document\.write|\beval\s*\(/);
  assert.match(app, /strong\.textContent = session\.title/);
});

test("acesso inicial ao storage possui degradacao em memoria", () => {
  assert.match(app, /try \{\s+storage = window\.localStorage;/);
  assert.match(app, /storage = new MemoryStorage\(\)/);
  assert.doesNotMatch(app, /new LocalSessionRepository\(localStorage\)/);
  assert.match(app, /Alteração mantida apenas nesta aba/);
});

test("exclusao move foco para destino logico apos render", () => {
  assert.match(app, /const visibleIndex = visibleSessions\(state\)\.findIndex/);
  assert.match(app, /const restoredButton = remainingButtons\.find/);
  assert.match(app, /remainingButtons\[Math\.min\(visibleIndex,/);
  assert.match(
    app,
    /\(restoredButton \?\? adjacentButton \?\? elements\.filter\)\.focus\(\)/,
  );
});
