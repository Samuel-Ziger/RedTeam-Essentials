import test from 'node:test'
import assert from 'node:assert/strict'
import { readFileSync } from 'node:fs'

const css = readFileSync(new URL('../styles.css', import.meta.url), 'utf8')
const sidebar = readFileSync(new URL('../components/Sidebar.jsx', import.meta.url), 'utf8')

function declarations(selector) {
  const marker = `${selector} {`
  const start = css.indexOf(marker)
  assert.notEqual(start, -1, `regra ${selector} deve existir`)
  const end = css.indexOf('}', start)
  assert.notEqual(end, -1, `regra ${selector} deve ser fechada`)
  return css.slice(start + marker.length, end)
}

function hasDeclaration(rule, property, value) {
  const escapedProperty = property.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')
  const escapedValue = value.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')
  assert.match(rule, new RegExp(`${escapedProperty}:\\s*${escapedValue}\\s*;`))
}

test('mantem o shell limitado a viewport para criar uma area rolavel', () => {
  hasDeclaration(declarations('body'), 'overflow', 'hidden')

  const shell = declarations('.app-shell')
  hasDeclaration(shell, 'height', '100dvh')
  hasDeclaration(shell, 'min-height', '0')
  hasDeclaration(shell, 'overflow', 'hidden')
})

test('conteudo principal rola com mouse, teclado e toque sem crescer alem do shell', () => {
  const workspace = declarations('.workspace')
  hasDeclaration(workspace, 'height', '100%')
  hasDeclaration(workspace, 'min-height', '0')
  hasDeclaration(workspace, 'overflow', 'hidden')

  const content = declarations('.content-scroll')
  hasDeclaration(content, 'flex', '1 1 auto')
  hasDeclaration(content, 'min-height', '0')
  hasDeclaration(content, 'overflow-y', 'auto')
  hasDeclaration(content, 'touch-action', 'pan-y pinch-zoom')
})

test('arvore lateral preserva rolagem propria em navegacao touch', () => {
  const tree = declarations('.curriculum-tree')
  hasDeclaration(tree, 'min-height', '0')
  hasDeclaration(tree, 'overflow-y', 'auto')
  hasDeclaration(tree, 'touch-action', 'pan-y')
})

test('remove limites da viewport durante impressao', () => {
  const print = css.slice(css.indexOf('@media print'))
  assert.match(print, /html, body, #root \{ height: auto; min-height: 0; \}/)
  assert.match(print, /body \{ overflow: visible; \}/)
  assert.match(print, /\.app-shell \{ display: block; height: auto; overflow: visible; \}/)
  assert.match(print, /\.workspace \{ height: auto; overflow: visible; \}/)
})

test('item curricular ativo e revelado dentro da arvore lateral', () => {
  assert.match(sidebar, /tree\.contains\(target\)/)
  assert.match(sidebar, /target\.scrollIntoView\(\{ behavior: 'auto', block: 'nearest', inline: 'nearest' \}\)/)
})
