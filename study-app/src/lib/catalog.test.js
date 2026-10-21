import test from 'node:test'
import assert from 'node:assert/strict'

import {
  collectionContext,
  documentContext,
  itemsForSection,
  libraryItems,
  normalizeCatalog,
  resolveLocalDocument,
  resolveLocalResource,
  searchCatalog,
  searchLibrary,
} from './catalog.js'

const generatedCatalog = {
  schemaVersion: 1,
  tracks: [
    { id: 'fundamentos', order: 1, title: 'Fundamentos', moduleIds: ['00'] },
  ],
  modules: [
    {
      id: '00',
      order: 1,
      trackId: 'fundamentos',
      title: 'Programação',
      estimatedHours: { min: 12, max: 20 },
      documentIds: ['doc-a', 'doc-b', 'lab-a'],
      chapterIds: ['doc-a', 'doc-b'],
      labIds: ['lab-a'],
    },
  ],
  documents: [
    {
      id: 'doc-a',
      order: 1,
      module: '00',
      type: 'chapter',
      title: 'Introdução ao Python',
      sourcePath: '00/curso/01-introducao.md',
      contentUrl: '/generated/content/00/curso/01-introducao.md',
      readingMinutes: 5,
      prerequisites: [],
    },
    {
      id: 'doc-b',
      order: 2,
      module: '00',
      type: 'chapter',
      title: 'Funções e testes',
      sourcePath: '00/curso/02-funcoes.md',
      prerequisites: ['doc-a'],
    },
    {
      id: 'lab-a',
      order: 3,
      module: '00',
      type: 'lab',
      title: 'Laboratório Python',
      sourcePath: '00/curso/laboratorios/lab.md',
      prerequisites: ['doc-a', 'doc-b'],
    },
  ],
}

test('normaliza o schema gerado e resolve referências globais', () => {
  const catalog = normalizeCatalog(generatedCatalog)
  assert.equal(catalog.tracks.length, 1)
  assert.equal(catalog.modules[0].documents.length, 3)
  assert.equal(catalog.modules[0].labs[0].id, 'lab-a')
  assert.equal(catalog.stats.labs, 1)
  assert.equal(catalog.tracks[0].stats.readingMinutes, 7)
  assert.deepEqual(catalog.modules[0].estimatedHours, { min: 12, max: 20 })
  assert.deepEqual(catalog.tracks[0].stats.estimatedHours, { min: 12, max: 20 })
  assert.deepEqual(catalog.stats.estimatedHours, { min: 12, max: 20 })
})

test('normaliza carga horária escalar como faixa fechada', () => {
  const input = {
    ...generatedCatalog,
    modules: [{ ...generatedCatalog.modules[0], estimatedHours: 8 }],
  }
  assert.deepEqual(normalizeCatalog(input).modules[0].estimatedHours, { min: 8, max: 8 })
})

test('aceita catálogo antigo com documentos embutidos', () => {
  const catalog = normalizeCatalog({
    tracks: [{
      title: 'Trilha local',
      modules: [{ title: 'Módulo local', documents: [{ title: 'Leia-me', content: '# Oi' }] }],
    }],
  })
  assert.equal(catalog.tracks[0].modules.length, 1)
  assert.equal(catalog.documents[0].content, '# Oi')
})

test('fornece contexto anterior e próximo dentro do módulo', () => {
  const catalog = normalizeCatalog(generatedCatalog)
  const context = documentContext(catalog, 'doc-b')
  assert.equal(context.previous.id, 'doc-a')
  assert.equal(context.next.id, 'lab-a')
  assert.equal(context.track.id, 'fundamentos')
})

test('continua a formação do fim de um módulo para o início do seguinte', () => {
  const input = {
    ...generatedCatalog,
    tracks: [{
      id: 'fundamentos',
      order: 1,
      title: 'Fundamentos',
      moduleIds: ['00', '01'],
    }],
    modules: [
      generatedCatalog.modules[0],
      {
        id: '01',
        order: 2,
        trackId: 'fundamentos',
        title: 'APIs',
        documentIds: ['doc-c'],
      },
    ],
    documents: [
      ...generatedCatalog.documents.map((document) => ({ ...document, origin: 'formation' })),
      {
        id: 'doc-c',
        order: 4,
        module: '01',
        type: 'chapter',
        title: 'Primeiro conteúdo de APIs',
        sourcePath: '01/curso/01-apis.md',
        origin: 'formation',
      },
    ],
  }
  const catalog = normalizeCatalog(input)

  assert.equal(documentContext(catalog, 'lab-a').next.id, 'doc-c')
  assert.equal(documentContext(catalog, 'doc-c').previous.id, 'lab-a')
})

test('navega dentro da mesma origem sem misturar formação e acervo legado', () => {
  const legacy = {
    id: 'legacy-a',
    order: 2,
    module: '00',
    type: 'supplement',
    title: 'Recon legado',
    sourcePath: '00/recon.md',
    origin: 'legacy',
  }
  const input = {
    ...generatedCatalog,
    modules: [{ ...generatedCatalog.modules[0], documentIds: ['doc-a', 'legacy-a', 'doc-b', 'lab-a'] }],
    documents: [...generatedCatalog.documents, legacy],
  }
  const catalog = normalizeCatalog(input)
  assert.equal(documentContext(catalog, 'doc-a').next.id, 'doc-b')
  assert.equal(documentContext(catalog, 'legacy-a').previous, null)
  assert.equal(documentContext(catalog, 'legacy-a').next, null)
})

test('busca sem diferenciar acentos e inclui contexto do módulo', () => {
  const catalog = normalizeCatalog(generatedCatalog)
  assert.equal(searchCatalog(catalog, 'introducao python')[0].document.id, 'doc-a')
  assert.equal(searchCatalog(catalog, 'programacao funcoes')[0].document.id, 'doc-b')
})

test('resolve link Markdown relativo sem permitir URLs externas', () => {
  const catalog = normalizeCatalog(generatedCatalog)
  const current = catalog.documents.find((document) => document.id === 'doc-b')
  const withDirectoryOverview = {
    ...catalog,
    documents: [
      ...catalog.documents,
      { id: 'guide', sourcePath: '00/curso/guias/README.md' },
    ],
  }
  assert.equal(resolveLocalDocument(catalog, current, './01-introducao.md').id, 'doc-a')
  assert.equal(resolveLocalDocument(withDirectoryOverview, current, './guias/').id, 'guide')
  assert.equal(resolveLocalDocument(catalog, current, 'https://example.org/file.md'), null)
  assert.equal(resolveLocalDocument(catalog, current, '%E0%A4%A'), null)
  assert.equal(resolveLocalDocument(catalog, current, '../../../01-introducao.md'), null)
})

test('normaliza recursos e coleções do schema v2 sem perder compatibilidade com assets', () => {
  const catalog = normalizeCatalog({
    ...generatedCatalog,
    schemaVersion: 2,
    documents: generatedCatalog.documents.map((document) => ({
      ...document,
      origin: 'formation',
      required: document.id === 'doc-a',
      role: document.type === 'lab' ? 'lab' : 'lesson',
      memberships: [{ collectionId: 'formacao-principal', courseId: 'curso-python', moduleId: '00' }],
      resourceIds: document.id === 'doc-a' ? ['source-python'] : [],
    })),
    resources: [{
      id: 'source-python',
      title: 'Exemplo Python',
      sourcePath: '00/curso/exemplos/main.py',
      contentUrl: '/generated/content/00/curso/exemplos/main.py',
      kind: 'code',
      language: 'python',
      moduleId: '00',
      memberships: [{ collectionId: 'laboratorios-projetos', courseId: 'curso-python', moduleId: '00' }],
      relatedDocumentIds: ['doc-a'],
    }],
    courses: [{
      id: 'curso-python',
      title: 'Curso Python',
      moduleIds: ['00'],
      documentIds: ['doc-a', 'doc-b'],
      resourceIds: ['source-python'],
    }],
  })
  assert.equal(catalog.schemaVersion, 2)
  assert.equal(catalog.resources[0].language, 'python')
  assert.deepEqual(catalog.resources[0].memberships, ['laboratorios-projetos', 'curso-python', '00'])
  assert.deepEqual(catalog.documents[0].resourceIds, ['source-python'])
  assert.equal(collectionContext(catalog, 'curso-python').resources[0].id, 'source-python')
  assert.equal(itemsForSection(catalog, 'tools').some((item) => item.id === 'source-python'), true)
  assert.equal(itemsForSection(catalog, 'practice').some((item) => item.id === 'source-python'), true)
  assert.equal(resolveLocalResource(catalog, catalog.documents[0], './exemplos/main.py').id, 'source-python')
})

test('busca global inclui documentos e recursos, expõe facets e não corta em 30', () => {
  const documents = Array.from({ length: 35 }, (_, index) => ({
    id: `python-${index}`,
    module: '00',
    type: 'chapter',
    title: `Python exemplo ${index}`,
    sourcePath: `00/curso/${index}.md`,
  }))
  const catalog = normalizeCatalog({
    tracks: [{ id: 'base', moduleIds: ['00'] }],
    modules: [{ id: '00', title: 'Base', documentIds: documents.map(({ id }) => id) }],
    documents,
    resources: [{ id: 'python-tool', title: 'Python runner', sourcePath: '00/curso/runner.py', kind: 'code' }],
  })
  assert.equal(searchCatalog(catalog, 'python').length, 35)
  const result = searchLibrary(catalog, 'python')
  assert.equal(result.total, 36)
  assert.equal(result.facets.documents, 35)
  assert.equal(result.facets.resources, 1)
})

test('mantém alias Markdown resolvível sem duplicá-lo na biblioteca ou busca', () => {
  const catalog = normalizeCatalog({
    tracks: [],
    modules: [],
    documents: [{
      id: 'global-guide',
      title: 'Guia global',
      sourcePath: 'GUIDE.md',
      contentUrl: '/generated/content/GUIDE.md',
      origin: 'global',
      required: false,
    }],
    resources: [{
      id: 'global-guide-alias',
      title: 'Guia global',
      sourcePath: 'GUIDE.md',
      contentUrl: '/generated/content/GUIDE.md',
      kind: 'markdown',
      aliasOfDocumentId: 'global-guide',
    }],
  })
  assert.equal(catalog.resources.length, 1)
  assert.equal(catalog.visibleResources.length, 0)
  assert.deepEqual(libraryItems(catalog).map(({ id }) => id), ['global-guide'])
  assert.equal(searchLibrary(catalog, 'guia').total, 1)
  assert.equal(resolveLocalResource(catalog, { sourcePath: 'folder/current.md' }, '../GUIDE.md').id, 'global-guide-alias')
})

test('expõe documentos globais na Documentação sem duplicá-los na Formação', () => {
  const globalDocuments = Array.from({ length: 19 }, (_, index) => ({
    id: `global-document-${index + 1}`,
    title: `Documento global ${index + 1}`,
    sourcePath: `docs/global-${index + 1}.md`,
    origin: 'global',
    category: 'documentation',
    role: 'global_document',
    required: false,
    memberships: [{ collectionId: 'documentacao-global' }],
  }))
  const catalog = normalizeCatalog({
    tracks: [],
    modules: [],
    documents: globalDocuments,
    collections: [{
      id: 'documentacao-global',
      title: 'Documentação global',
      kind: 'documentation',
      documentIds: globalDocuments.map(({ id }) => id),
    }],
  })

  const documentation = itemsForSection(catalog, 'documentation')
  const formation = itemsForSection(catalog, 'formation')
  const items = libraryItems(catalog)

  assert.equal(documentation.length, 19)
  assert.equal(formation.some((item) => item.origin === 'global'), false)
  assert.equal(items.length, 19)
  assert.equal(new Set(items.map((item) => `${item.itemType}:${item.id}`)).size, 19)
})
