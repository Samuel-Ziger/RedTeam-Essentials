export const PROGRESS_STORAGE_KEY = 'rte.study.progress.v1'
export const THEME_STORAGE_KEY = 'rte.study.theme'
export const PROGRESS_VERSION = 1

export function createEmptyProgress() {
  return {
    version: PROGRESS_VERSION,
    completedDocuments: {},
    completedLabs: {},
    lastDocument: null,
    scrollPositions: {},
    startedAt: null,
    updatedAt: null,
  }
}

function object(value) {
  return value && typeof value === 'object' && !Array.isArray(value) ? value : {}
}

function completionMap(value) {
  if (Array.isArray(value)) {
    return Object.fromEntries(value.filter(Boolean).map((id) => [String(id), null]))
  }
  return Object.fromEntries(
    Object.entries(object(value)).filter(([id]) => typeof id === 'string' && id.length > 0),
  )
}

export function normalizeProgress(value) {
  const source = object(value)
  const completedDocuments = completionMap(source.completedDocuments ?? source.completed ?? source.read)
  const completedLabs = completionMap(source.completedLabs ?? source.labs)
  const scrollPositions = Object.fromEntries(
    Object.entries(object(source.scrollPositions ?? source.scroll))
      .filter(([, position]) => Number.isFinite(Number(position)) && Number(position) >= 0)
      .map(([id, position]) => [id, Number(position)]),
  )
  const last = object(source.lastDocument ?? source.lastRead)

  return {
    version: PROGRESS_VERSION,
    completedDocuments,
    completedLabs,
    lastDocument: typeof last.id === 'string'
      ? {
          id: last.id,
          moduleId: typeof last.moduleId === 'string' ? last.moduleId : '',
          trackId: typeof last.trackId === 'string' ? last.trackId : '',
          visitedAt: last.visitedAt ?? last.updatedAt ?? null,
        }
      : null,
    scrollPositions,
    startedAt: source.startedAt ?? null,
    updatedAt: source.updatedAt ?? null,
  }
}

function timestamp(now) {
  if (typeof now === 'string') return now
  if (now instanceof Date) return now.toISOString()
  return new Date().toISOString()
}

function touched(progress, now) {
  const time = timestamp(now)
  return {
    ...progress,
    startedAt: progress.startedAt || time,
    updatedAt: time,
  }
}

export function setDocumentCompleted(value, documentId, completed = true, now) {
  const progress = normalizeProgress(value)
  if (!documentId) return progress
  const completedDocuments = { ...progress.completedDocuments }
  if (completed) completedDocuments[documentId] = timestamp(now)
  else delete completedDocuments[documentId]
  return touched({ ...progress, completedDocuments }, now)
}

export function setLabCompleted(value, labId, completed = true, now) {
  const progress = normalizeProgress(value)
  if (!labId) return progress
  const completedLabs = { ...progress.completedLabs }
  if (completed) completedLabs[labId] = timestamp(now)
  else delete completedLabs[labId]
  return touched({ ...progress, completedLabs }, now)
}

export function recordVisit(value, document, context = {}, now) {
  const progress = normalizeProgress(value)
  if (!document?.id) return progress
  return touched({
    ...progress,
    lastDocument: {
      id: document.id,
      moduleId: document.moduleId || context.moduleId || '',
      trackId: document.trackId || context.trackId || '',
      visitedAt: timestamp(now),
    },
  }, now)
}

export function recordScroll(value, documentId, position, now) {
  const progress = normalizeProgress(value)
  if (!documentId || !Number.isFinite(Number(position))) return progress
  return touched({
    ...progress,
    scrollPositions: {
      ...progress.scrollPositions,
      [documentId]: Math.max(0, Math.round(Number(position))),
    },
  }, now)
}

export function isDocumentCompleted(progress, documentId) {
  return Object.prototype.hasOwnProperty.call(
    normalizeProgress(progress).completedDocuments,
    documentId,
  )
}

function isLabDocument(document) {
  return document?.type === 'lab' || document?.role === 'lab_instruction'
}

/**
 * Conclusão curricular difere de leitura: um lab só termina no checkpoint
 * prático (completedLabs), ainda que sua instrução já tenha sido lida.
 */
export function isLearningItemCompleted(value, document) {
  const progress = normalizeProgress(value)
  if (!document?.id) return false
  const completion = isLabDocument(document)
    ? progress.completedLabs
    : progress.completedDocuments
  return Object.prototype.hasOwnProperty.call(completion, document.id)
}

export function isRequirementCompleted(value, documentId, catalog = null) {
  const document = catalog?.documents?.find((candidate) => candidate.id === documentId)
  return document
    ? isLearningItemCompleted(value, document)
    : isDocumentCompleted(value, documentId)
}

export function completionFor(documents, value) {
  const uniqueDocuments = [...new Map(
    (documents || []).filter((document) => document?.id).map((document) => [document.id, document]),
  ).values()]
  const completed = uniqueDocuments.filter((document) => isLearningItemCompleted(value, document)).length
  return {
    completed,
    total: uniqueDocuments.length,
    remaining: Math.max(0, uniqueDocuments.length - completed),
    percent: uniqueDocuments.length ? Math.round((completed / uniqueDocuments.length) * 100) : 0,
  }
}

export function isRequiredFormationDocument(document) {
  const origin = String(document?.origin || 'formation').toLowerCase()
  const belongsToFormation = ['formation', 'formacao', 'curriculum', 'course', 'training', 'current'].includes(origin)
  return Boolean(document?.required) && belongsToFormation
}

export function completionBreakdown(documents, value) {
  const all = documents || []
  const requiredDocuments = all.filter(isRequiredFormationDocument)
  const optionalDocuments = all.filter((document) => !isRequiredFormationDocument(document))
  return {
    required: completionFor(requiredDocuments, value),
    optional: completionFor(optionalDocuments, value),
    all: completionFor(all, value),
  }
}

function documentsForModule(module, catalog) {
  if (!module) return []
  if (Array.isArray(module.documents) && module.documents.length) return module.documents
  const moduleId = String(module.id || module.moduleId || '')
  return (catalog?.documents || []).filter((document) =>
    String(document?.moduleId || document?.module || '') === moduleId,
  )
}

function prerequisiteClosure(module, catalog) {
  const modules = new Map((catalog?.modules || []).map((candidate) => [String(candidate.id), candidate]))
  const rootId = String(module?.id || module?.moduleId || '')
  const pending = [...new Set(module?.prerequisiteModuleIds || [])].map(String)
  const seen = new Set()

  while (pending.length) {
    const moduleId = pending.shift()
    if (!moduleId || moduleId === rootId || seen.has(moduleId)) continue
    seen.add(moduleId)
    const prerequisite = modules.get(moduleId)
    for (const dependency of prerequisite?.prerequisiteModuleIds || []) {
      const dependencyId = String(dependency)
      if (!seen.has(dependencyId)) pending.push(dependencyId)
    }
  }

  const order = new Map((catalog?.modules || []).map((candidate, index) => [String(candidate.id), index]))
  return [...seen].sort((first, second) => {
    const firstOrder = order.has(first) ? order.get(first) : Number.MAX_SAFE_INTEGER
    const secondOrder = order.has(second) ? order.get(second) : Number.MAX_SAFE_INTEGER
    return firstOrder - secondOrder || first.localeCompare(second, 'pt-BR', { numeric: true })
  })
}

export function moduleAvailability(module, catalog, value) {
  const progress = normalizeProgress(value)
  const moduleMap = new Map((catalog?.modules || []).map((candidate) => [String(candidate.id), candidate]))
  const prerequisiteModuleIds = prerequisiteClosure(module, catalog)
  const missingModuleIds = prerequisiteModuleIds.filter((moduleId) => {
    const prerequisite = moduleMap.get(moduleId)
    if (!prerequisite) return true
    const requiredDocuments = documentsForModule(prerequisite, catalog).filter(isRequiredFormationDocument)
    return requiredDocuments.some((document) => !isLearningItemCompleted(progress, document))
  })
  const missingSet = new Set(missingModuleIds)
  const completedModuleIds = prerequisiteModuleIds.filter((moduleId) => !missingSet.has(moduleId))

  return {
    unlocked: missingModuleIds.length === 0,
    prerequisiteModuleIds,
    missingModuleIds,
    completedModuleIds,
    completedPrerequisiteModules: completedModuleIds.length,
    totalPrerequisiteModules: prerequisiteModuleIds.length,
  }
}

export function labAvailability(lab, value, catalog = null) {
  const progress = normalizeProgress(value)
  const prerequisites = [...new Set(lab?.prerequisites || lab?.prerequisiteDocumentIds || [])]
  const missing = prerequisites.filter((id) => !isRequirementCompleted(progress, id, catalog))
  const moduleId = String(lab?.moduleId || lab?.module || '')
  const module = catalog?.modules?.find((candidate) => String(candidate.id) === moduleId)
  const moduleState = module
    ? moduleAvailability(module, catalog, progress)
    : {
        unlocked: true,
        prerequisiteModuleIds: [],
        missingModuleIds: [],
        completedPrerequisiteModules: 0,
        totalPrerequisiteModules: 0,
      }
  const completedDocumentPrerequisites = prerequisites.length - missing.length
  return {
    unlocked: missing.length === 0 && moduleState.unlocked,
    completed: Object.prototype.hasOwnProperty.call(progress.completedLabs, lab?.id),
    missing,
    missingModuleIds: moduleState.missingModuleIds,
    prerequisiteModuleIds: moduleState.prerequisiteModuleIds,
    completedPrerequisites: completedDocumentPrerequisites,
    totalPrerequisites: prerequisites.length,
    completedModulePrerequisites: moduleState.completedPrerequisiteModules,
    totalModulePrerequisites: moduleState.totalPrerequisiteModules,
    completedRequirements: completedDocumentPrerequisites + moduleState.completedPrerequisiteModules,
    totalRequirements: prerequisites.length + moduleState.totalPrerequisiteModules,
  }
}

function isFormationLearningItem(document) {
  const origin = String(document?.origin || 'formation').toLowerCase()
  return ['formation', 'formacao', 'curriculum', 'course', 'training', 'current'].includes(origin)
}

/**
 * Retorna o primeiro item curricular que pode ser estudado. A leitura do
 * enunciado de um lab não faz esse lab desaparecer da retomada: para fins de
 * aprendizagem, ele só termina quando completedLabs registra o checkpoint.
 */
export function firstAvailableDocument(documents, catalog, value) {
  const progress = normalizeProgress(value)
  const formation = (documents || []).filter(isFormationLearningItem)
  const required = formation.filter((document) => document.required)
  const ordered = [...required, ...formation.filter((document) => !document.required)]
  const available = ordered.filter((document) => {
    const moduleId = String(document?.moduleId || document?.module || '')
    const module = catalog?.modules?.find((candidate) => String(candidate.id) === moduleId)
    if (module && !moduleAvailability(module, catalog, progress).unlocked) return false
    if (isLabDocument(document)) return labAvailability(document, progress, catalog).unlocked
    return (document.prerequisites || []).every((id) => isRequirementCompleted(progress, id, catalog))
  })
  return available.find((document) => !isLearningItemCompleted(progress, document))
    || available[0]
    || null
}

export function nextRecommended(catalog, value) {
  const progress = normalizeProgress(value)
  const sourceDocuments = catalog?.documents || []
  const requiredDocuments = sourceDocuments.filter(isRequiredFormationDocument)
  const documents = requiredDocuments.length ? requiredDocuments : sourceDocuments
  if (!documents.length) return null

  const currentIndex = progress.lastDocument
    ? documents.findIndex((document) => document.id === progress.lastDocument.id)
    : -1
  const ordered = currentIndex >= 0
    ? [...documents.slice(currentIndex + 1), ...documents.slice(0, currentIndex + 1)]
    : documents

  return ordered.find((document) => {
    if (isLearningItemCompleted(progress, document)) return false
    const moduleId = String(document.moduleId || document.module || '')
    const module = catalog?.modules?.find((candidate) => String(candidate.id) === moduleId)
    if (module && !moduleAvailability(module, catalog, progress).unlocked) return false
    if (isLabDocument(document)) return labAvailability(document, progress, catalog).unlocked
    return (document.prerequisites || []).every((id) => isRequirementCompleted(progress, id, catalog))
  }) || null
}

export function recentlyCompleted(catalog, value, limit = 5) {
  const progress = normalizeProgress(value)
  const documentMap = new Map((catalog?.documents || []).map((document) => [document.id, document]))
  const completedReadings = Object.entries(progress.completedDocuments)
    .map(([id, completedAt]) => ({
      document: documentMap.get(id),
      completedAt,
      completionType: 'reading',
    }))
    .filter((item) => item.document && !isLabDocument(item.document))
  const completedLabs = Object.entries(progress.completedLabs)
    .map(([id, completedAt]) => ({
      document: documentMap.get(id),
      completedAt,
      completionType: 'lab',
    }))
    .filter((item) => item.document && isLabDocument(item.document))

  return [...completedReadings, ...completedLabs]
    .sort((a, b) => String(b.completedAt || '').localeCompare(String(a.completedAt || '')))
    .slice(0, limit)
}

export function loadProgress(storage) {
  try {
    const raw = storage?.getItem(PROGRESS_STORAGE_KEY)
    return raw ? normalizeProgress(JSON.parse(raw)) : createEmptyProgress()
  } catch {
    return createEmptyProgress()
  }
}

export function saveProgress(storage, progress) {
  try {
    storage?.setItem(PROGRESS_STORAGE_KEY, JSON.stringify(normalizeProgress(progress)))
    return true
  } catch {
    return false
  }
}
