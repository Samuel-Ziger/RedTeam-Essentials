import test from 'node:test'
import assert from 'node:assert/strict'

import { markdownAnchor } from './markdown.js'

test('gera ancora estavel para titulos Markdown e fragmentos codificados', () => {
  assert.equal(markdownAnchor('🎯 Introdução ao Web Recon'), 'introducao-ao-web-recon')
  assert.equal(markdownAnchor('introdu%C3%A7%C3%A3o'), 'introducao')
  assert.equal(markdownAnchor('%E0%A4%A'), 'e0-a4-a')
})
