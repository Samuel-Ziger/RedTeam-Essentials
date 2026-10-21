import test from 'node:test'
import assert from 'node:assert/strict'

import {
  completionBreakdown,
  completionFor,
  createEmptyProgress,
  firstAvailableDocument,
  labAvailability,
  loadProgress,
  moduleAvailability,
  nextRecommended,
  normalizeProgress,
  recordScroll,
  recordVisit,
  recentlyCompleted,
  saveProgress,
  setDocumentCompleted,
  setLabCompleted,
} from './progress.js'

const NOW = '2026-10-01T12:00:00.000Z'
const documents = [
  { id: 'intro', type: 'chapter', prerequisites: [] },
  { id: 'advanced', type: 'chapter', prerequisites: ['intro'] },
  { id: 'lab-1', type: 'lab', prerequisites: ['intro', 'advanced'] },
]
const catalog = { documents }

function gatedCatalog(size = 28) {
  const modules = Array.from({ length: size }, (_, index) => {
    const id = String(index).padStart(2, '0')
    const document = {
      id: `required-${id}`,
      moduleId: id,
      origin: 'formation',
      required: true,
      type: 'chapter',
      prerequisites: [],
    }
    return {
      id,
      prerequisiteModuleIds: index === 27
        ? Array.from({ length: 27 }, (_value, prerequisite) => String(prerequisite).padStart(2, '0'))
        : [],
      documents: [document],
    }
  })
  return { modules, documents: modules.flatMap((module) => module.documents) }
}

test('normaliza progresso legado sem reaproveitar referências mutáveis', () => {
  const legacy = { completed: ['intro'], labs: ['lab-antigo'], scroll: { intro: '42', invalid: -2 } }
  const normalized = normalizeProgress(legacy)
  assert.deepEqual(normalized.completedDocuments, { intro: null })
  assert.deepEqual(normalized.completedLabs, { 'lab-antigo': null })
  assert.deepEqual(normalized.scrollPositions, { intro: 42 })
  assert.notEqual(normalized, legacy)
})

test('marca e desmarca documento preservando o restante do estado', () => {
  const initial = createEmptyProgress()
  const completed = setDocumentCompleted(initial, 'intro', true, NOW)
  assert.equal(completed.completedDocuments.intro, NOW)
  assert.equal(completed.startedAt, NOW)
  assert.equal(initial.completedDocuments.intro, undefined)

  const reverted = setDocumentCompleted(completed, 'intro', false, NOW)
  assert.equal(reverted.completedDocuments.intro, undefined)
})

test('calcula progresso apenas para IDs únicos', () => {
  const progress = setDocumentCompleted(createEmptyProgress(), 'intro', true, NOW)
  assert.deepEqual(completionFor([documents[0], documents[0], documents[1]], progress), {
    completed: 1,
    total: 2,
    remaining: 1,
    percent: 50,
  })
})

test('separa progresso obrigatório da formação e exploração opcional', () => {
  const materials = [
    { id: 'required', origin: 'formation', required: true },
    { id: 'reference', origin: 'formation', required: false },
    { id: 'legacy', origin: 'legacy', required: false },
    { id: 'legacy-wrong-flag', origin: 'legacy', required: true },
  ]
  let progress = setDocumentCompleted(createEmptyProgress(), 'required', true, NOW)
  progress = setDocumentCompleted(progress, 'legacy', true, NOW)
  const breakdown = completionBreakdown(materials, progress)
  assert.deepEqual(breakdown.required, { completed: 1, total: 1, remaining: 0, percent: 100 })
  assert.deepEqual(breakdown.optional, { completed: 1, total: 3, remaining: 2, percent: 33 })
})

test('libera laboratório somente quando todos os pré-requisitos foram lidos', () => {
  let progress = setDocumentCompleted(createEmptyProgress(), 'intro', true, NOW)
  assert.deepEqual(labAvailability(documents[2], progress).missing, ['advanced'])
  assert.equal(labAvailability(documents[2], progress).unlocked, false)

  progress = setDocumentCompleted(progress, 'advanced', true, NOW)
  assert.equal(labAvailability(documents[2], progress).unlocked, true)
  progress = setLabCompleted(progress, 'lab-1', true, NOW)
  assert.equal(labAvailability(documents[2], progress).completed, true)
})

test('ler a instrução não conclui o laboratório no progresso curricular', () => {
  const lab = {
    id: 'lab-pratico',
    type: 'lab',
    role: 'lab_instruction',
    origin: 'formation',
    required: true,
  }
  const readOnly = setDocumentCompleted(createEmptyProgress(), lab.id, true, NOW)
  assert.equal(labAvailability(lab, readOnly).completed, false)
  assert.deepEqual(completionBreakdown([lab], readOnly).required, {
    completed: 0,
    total: 1,
    remaining: 1,
    percent: 0,
  })

  const practiced = setLabCompleted(readOnly, lab.id, true, NOW)
  assert.equal(labAvailability(lab, practiced).completed, true)
  assert.equal(completionBreakdown([lab], practiced).required.percent, 100)
})

test('retomada mantém lab lido até o checkpoint prático ser concluído', () => {
  const intro = { id: 'intro-retomada', type: 'chapter', origin: 'formation', required: true }
  const lab = {
    id: 'lab-retomada',
    type: 'lab',
    origin: 'formation',
    required: true,
    prerequisites: [intro.id],
  }
  const next = {
    id: 'depois-do-lab',
    type: 'chapter',
    origin: 'formation',
    required: true,
    prerequisites: [lab.id],
  }
  const curriculum = { documents: [intro, lab, next], modules: [] }
  let progress = setDocumentCompleted(createEmptyProgress(), intro.id, true, NOW)
  progress = setDocumentCompleted(progress, lab.id, true, '2026-10-01T12:01:00.000Z')

  assert.equal(firstAvailableDocument(curriculum.documents, curriculum, progress).id, lab.id)

  progress = setLabCompleted(progress, lab.id, true, '2026-10-01T12:02:00.000Z')
  assert.equal(firstAvailableDocument(curriculum.documents, curriculum, progress).id, next.id)
})

test('histórico separa leitura concluída de execução de laboratório', () => {
  const chapter = { id: 'capitulo-recente', type: 'chapter' }
  const lab = { id: 'lab-recente', type: 'lab' }
  const curriculum = { documents: [chapter, lab] }
  let progress = setDocumentCompleted(createEmptyProgress(), chapter.id, true, NOW)
  progress = setDocumentCompleted(progress, lab.id, true, '2026-10-01T12:01:00.000Z')

  assert.deepEqual(recentlyCompleted(curriculum, progress), [{
    document: chapter,
    completedAt: NOW,
    completionType: 'reading',
  }])

  progress = setLabCompleted(progress, lab.id, true, '2026-10-01T12:02:00.000Z')
  assert.deepEqual(recentlyCompleted(curriculum, progress).map((item) => [item.document.id, item.completionType]), [
    [lab.id, 'lab'],
    [chapter.id, 'reading'],
  ])
})

test('leitura de lab não libera dependência de documento nem de módulo', () => {
  const base = { id: 'base', moduleId: '00', type: 'chapter', origin: 'formation', required: true }
  const lab = {
    id: 'lab-base',
    moduleId: '00',
    type: 'lab',
    role: 'lab_instruction',
    origin: 'formation',
    required: true,
  }
  const dependent = {
    id: 'dependent',
    moduleId: '01',
    type: 'chapter',
    origin: 'formation',
    required: true,
    prerequisites: ['lab-base'],
  }
  const curriculum = {
    documents: [base, lab, dependent],
    modules: [
      { id: '00', prerequisiteModuleIds: [], documents: [base, lab] },
      { id: '01', prerequisiteModuleIds: ['00'], documents: [dependent] },
    ],
  }
  let progress = setDocumentCompleted(createEmptyProgress(), base.id, true, NOW)
  progress = setDocumentCompleted(progress, lab.id, true, NOW)

  assert.equal(moduleAvailability(curriculum.modules[1], curriculum, progress).unlocked, false)
  assert.deepEqual(labAvailability({ id: 'next-lab', prerequisites: ['lab-base'] }, progress, curriculum).missing, ['lab-base'])
  assert.equal(nextRecommended(curriculum, progress).id, lab.id)

  progress = setLabCompleted(progress, lab.id, true, NOW)
  assert.equal(moduleAvailability(curriculum.modules[1], curriculum, progress).unlocked, true)
  assert.deepEqual(labAvailability({ id: 'next-lab', prerequisites: ['lab-base'] }, progress, curriculum).missing, [])
  assert.equal(nextRecommended(curriculum, progress).id, dependent.id)
})

test('bloqueia o módulo 27 até concluir todos os módulos 00 a 26', () => {
  const curriculum = gatedCatalog()
  const advanced = curriculum.modules[27]
  const empty = moduleAvailability(advanced, curriculum, createEmptyProgress())
  assert.equal(empty.unlocked, false)
  assert.deepEqual(empty.missingModuleIds, Array.from({ length: 27 }, (_value, index) => String(index).padStart(2, '0')))

  let progress = createEmptyProgress()
  for (let index = 0; index < 27; index += 1) {
    progress = setDocumentCompleted(progress, `required-${String(index).padStart(2, '0')}`, true, NOW)
  }
  const ready = moduleAvailability(advanced, curriculum, progress)
  assert.equal(ready.unlocked, true)
  assert.equal(ready.completedPrerequisiteModules, 27)
})

test('fecha pré-requisitos transitivos antes de liberar um módulo', () => {
  const curriculum = gatedCatalog(3)
  curriculum.modules[1].prerequisiteModuleIds = ['00']
  curriculum.modules[2].prerequisiteModuleIds = ['01']
  let progress = setDocumentCompleted(createEmptyProgress(), 'required-01', true, NOW)

  const blocked = moduleAvailability(curriculum.modules[2], curriculum, progress)
  assert.deepEqual(blocked.prerequisiteModuleIds, ['00', '01'])
  assert.deepEqual(blocked.missingModuleIds, ['00'])

  progress = setDocumentCompleted(progress, 'required-00', true, NOW)
  assert.equal(moduleAvailability(curriculum.modules[2], curriculum, progress).unlocked, true)
})

test('laboratório respeita o gate do módulo quando recebe o catálogo', () => {
  const curriculum = gatedCatalog()
  const lab = { id: 'lab-27', moduleId: '27', prerequisites: [] }
  const empty = labAvailability(lab, createEmptyProgress(), curriculum)
  assert.equal(empty.unlocked, false)
  assert.equal(empty.missingModuleIds.length, 27)

  let progress = createEmptyProgress()
  for (let index = 0; index < 27; index += 1) {
    progress = setDocumentCompleted(progress, `required-${String(index).padStart(2, '0')}`, true, NOW)
  }
  assert.equal(labAvailability(lab, progress, curriculum).unlocked, true)
  assert.equal(labAvailability(lab, progress).unlocked, true, 'a assinatura antiga continua funcional')
})

test('registra último documento e posição de leitura', () => {
  let progress = recordVisit(createEmptyProgress(), { id: 'intro', moduleId: '00' }, { trackId: 'base' }, NOW)
  progress = recordScroll(progress, 'intro', 82.6, NOW)
  assert.equal(progress.lastDocument.id, 'intro')
  assert.equal(progress.lastDocument.trackId, 'base')
  assert.equal(progress.scrollPositions.intro, 83)
})

test('recomenda o próximo capítulo incompleto cujos requisitos foram atendidos', () => {
  const empty = createEmptyProgress()
  assert.equal(nextRecommended(catalog, empty).id, 'intro')
  const completed = setDocumentCompleted(empty, 'intro', true, NOW)
  assert.equal(nextRecommended(catalog, completed).id, 'advanced')
  const chaptersDone = setDocumentCompleted(completed, 'advanced', true, NOW)
  assert.equal(nextRecommended(catalog, chaptersDone).id, 'lab-1')
  const labOnlyRead = setDocumentCompleted(chaptersDone, 'lab-1', true, NOW)
  assert.equal(nextRecommended(catalog, labOnlyRead).id, 'lab-1')
  const labDone = setLabCompleted(labOnlyRead, 'lab-1', true, NOW)
  assert.equal(nextRecommended(catalog, labDone), null)
})

test('recomendação não atravessa o gate de um módulo', () => {
  const baseDocument = { id: 'base-required', moduleId: '00', type: 'chapter', origin: 'formation', required: true, prerequisites: [] }
  const advancedDocument = { id: 'advanced-required', moduleId: '27', type: 'chapter', origin: 'formation', required: true, prerequisites: [] }
  const curriculum = {
    documents: [advancedDocument, baseDocument],
    modules: [
      { id: '00', prerequisiteModuleIds: [], documents: [baseDocument] },
      { id: '27', prerequisiteModuleIds: ['00'], documents: [advancedDocument] },
    ],
  }

  assert.equal(nextRecommended(curriculum, createEmptyProgress()).id, 'base-required')
  const completed = setDocumentCompleted(createEmptyProgress(), 'base-required', true, NOW)
  assert.equal(nextRecommended(curriculum, completed).id, 'advanced-required')
})

test('recomenda apenas a formação obrigatória quando o schema informa origem e papel', () => {
  const catalogV2 = {
    documents: [
      { id: 'core', type: 'chapter', origin: 'formation', required: true, prerequisites: [] },
      { id: 'solution', type: 'reference', origin: 'formation', required: false, prerequisites: [] },
      { id: 'recon-legacy', type: 'chapter', origin: 'legacy', required: false, prerequisites: [] },
    ],
  }
  assert.equal(nextRecommended(catalogV2, createEmptyProgress()).id, 'core')
  const completed = setDocumentCompleted(createEmptyProgress(), 'core', true, NOW)
  assert.equal(nextRecommended(catalogV2, completed), null)
})

test('salva, carrega e se recupera de JSON inválido', () => {
  const values = new Map()
  const storage = {
    getItem: (key) => values.get(key) ?? null,
    setItem: (key, value) => values.set(key, value),
  }
  const progress = setDocumentCompleted(createEmptyProgress(), 'intro', true, NOW)
  assert.equal(saveProgress(storage, progress), true)
  assert.equal(loadProgress(storage).completedDocuments.intro, NOW)
  values.set('rte.study.progress.v1', '{')
  assert.deepEqual(loadProgress(storage), createEmptyProgress())
})
