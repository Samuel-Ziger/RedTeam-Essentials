const FALLBACK_TRACK = {
  id: 'formacao-completa',
  order: 0,
  title: 'Formação completa',
  description: 'Todos os módulos disponíveis neste repositório.',
}

const TYPE_LABELS = {
  overview: 'Visão geral',
  chapter: 'Capítulo',
  lab: 'Laboratório',
  reference: 'Referência',
  supplement: 'Material extra',
}

const RESOURCE_KIND_LABELS = {
  code: 'Código',
  config: 'Configuração',
  data: 'Dados',
  image: 'Imagem',
  markdown: 'Documento',
  text: 'Texto',
}

export const LIBRARY_SECTIONS = [
  { id: 'formation', title: 'Formação', shortTitle: 'Formação' },
  { id: 'security', title: 'Acervo de Segurança', shortTitle: 'Acervo' },
  { id: 'practice', title: 'Labs e Projetos', shortTitle: 'Prática' },
  { id: 'tools', title: 'Ferramentas e Código', shortTitle: 'Código' },
  { id: 'documentation', title: 'Documentação', shortTitle: 'Documentação' },
]

const LEGACY_COLLECTION_TITLES = {
  '00': 'Fundamentos legados',
  '01': 'Reconhecimento',
  '02': 'OSINT',
  '03': 'Active Directory',
  '04': 'Automação',
  '05': 'DFIR e resposta a incidentes',
  '06': 'Cheatsheets',
  '07': 'Web Application Security',
  '08': 'Cloud Red Team',
  '09': 'C2 e evasão',
  '10': 'Containers e Kubernetes',
  '11': 'Python Tools',
  '12': 'Java Tools',
  '13': 'Initial Access',
  '14': 'Post-Exploitation',
  '15': 'Identidade híbrida',
  '16': 'CI/CD e Supply Chain',
  '17': 'macOS Security',
  '18': 'Mobile Security',
  '19': 'Wireless Security',
  '20': 'Offensive Labs',
  '21': 'Network Pivoting',
  '22': 'Secure Code Review',
  '23': 'Threat Intelligence e Emulation',
  '24': 'Lateral Movement',
  '25': 'Cursos em português',
  '26': 'Ofensivo e Defensivo',
}

function list(value) {
  if (Array.isArray(value)) return value
  if (value === undefined || value === null || value === '') return []
  return [value]
}

function text(value, fallback = '') {
  if (typeof value === 'string' && value.trim()) return value.trim()
  if (typeof value === 'number') return String(value)
  return fallback
}

function number(value, fallback = 0) {
  const parsed = Number(value)
  return Number.isFinite(parsed) ? parsed : fallback
}

function hourRange(value) {
  const source = value && typeof value === 'object' && !Array.isArray(value) ? value : null
  const single = Math.max(0, number(source ? undefined : value))
  const rawMin = Math.max(0, number(source?.min, number(source?.max, single)))
  const rawMax = Math.max(0, number(source?.max, rawMin))
  return rawMin <= rawMax
    ? { min: rawMin, max: rawMax }
    : { min: rawMax, max: rawMin }
}

function sumHourRanges(modules) {
  return (modules || []).reduce((total, module) => ({
    min: total.min + hourRange(module?.estimatedHours).min,
    max: total.max + hourRange(module?.estimatedHours).max,
  }), { min: 0, max: 0 })
}

function boolean(value, fallback = false) {
  if (typeof value === 'boolean') return value
  if (value === 'true' || value === 1) return true
  if (value === 'false' || value === 0) return false
  return fallback
}

function searchable(value) {
  return text(value).normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase()
}

function slug(value, fallback = 'item') {
  const normalized = text(value, fallback)
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '')
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-|-$/g, '')
  return normalized || fallback
}

function refId(value) {
  if (typeof value === 'string' || typeof value === 'number') return String(value)
  return text(value?.id || value?.documentId || value?.path || value?.sourcePath)
}

function unique(values) {
  return [...new Set(values.filter(Boolean))]
}

function byOrder(a, b) {
  return (a.order ?? 0) - (b.order ?? 0) || a.title.localeCompare(b.title, 'pt-BR')
}

function inferType(raw) {
  const explicit = text(raw?.type).toLowerCase()
  if (TYPE_LABELS[explicit]) return explicit
  const path = text(raw?.sourcePath || raw?.path).toLowerCase()
  if (/\b(lab|laboratorio|laboratório)s?\b/.test(path)) return 'lab'
  if (/refer|bibliograf|recurso/.test(path)) return 'reference'
  if (/readme\.md$/.test(path)) return 'overview'
  return 'chapter'
}

function normalizeMemberships(raw) {
  const memberships = list(raw?.memberships ?? raw?.collectionIds ?? raw?.collections ?? raw?.courseIds)
  return unique([
    ...memberships.flatMap((membership) => {
    if (typeof membership === 'string' || typeof membership === 'number') return [String(membership)]
    if (!membership || typeof membership !== 'object') return []
    return [
      membership.id,
      membership.collectionId,
      membership.courseId,
      membership.sectionId,
      membership.legacySectionId,
      membership.projectId,
      membership.moduleId,
    ].map(refId)
    }),
    refId(raw?.collectionId),
    refId(raw?.courseId),
    refId(raw?.legacySectionId),
    refId(raw?.projectId),
  ])
}

function inferOrigin(raw, type = '') {
  const explicit = text(raw?.origin || raw?.sourceGroup).toLowerCase()
  if (explicit) return explicit
  if (raw?.legacy === true) return 'legacy'
  const memberships = normalizeMemberships(raw).join(' ').toLowerCase()
  if (/legacy|legado|acervo|security/.test(memberships)) return 'legacy'
  const path = text(raw?.sourcePath || raw?.path)
  const parts = path.split('/').filter(Boolean)
  if (!/^\d{2}-/.test(parts[0] || '')) return 'documentation'
  const relative = parts.slice(1)
  if (relative.length === 1 && !['overview', 'lab'].includes(type)) return 'legacy'
  if (/^(?:docker-lab|labs)$/i.test(relative[0] || '')) return 'legacy'
  return 'formation'
}

function inferRole(raw, type) {
  const explicit = text(raw?.role).toLowerCase()
  if (explicit) return explicit
  return {
    chapter: 'lesson',
    lab: 'lab',
    overview: 'overview',
    reference: 'reference',
    supplement: 'supplement',
  }[type] || 'content'
}

function inferRequired(raw, type, origin, role) {
  if (raw && Object.prototype.hasOwnProperty.call(raw, 'required')) {
    return boolean(raw.required)
  }
  return origin === 'formation' && (type === 'chapter' || role === 'lesson')
}

function normalizePrerequisites(raw) {
  return unique(
    list(raw?.prerequisites ?? raw?.requiredDocuments ?? raw?.requires ?? raw?.unlockAfter)
      .map(refId),
  )
}

function normalizeDocument(raw, index, moduleId = '') {
  const source = typeof raw === 'object' && raw !== null ? raw : { id: raw }
  const sourcePath = text(source.sourcePath || source.path || source.file)
  const id = text(source.id || source.documentId, sourcePath || `document-${index + 1}`)
  const title = text(
    source.title || source.name,
    sourcePath.split('/').pop()?.replace(/\.md$/i, '').replace(/[-_]/g, ' ') || `Documento ${index + 1}`,
  )
  const content = typeof source.content === 'string' ? source.content : ''
  const type = inferType(source)
  const origin = inferOrigin(source, type)
  const role = inferRole(source, type)

  return {
    id,
    order: number(source.globalOrder ?? source.order, index),
    moduleId: text(source.module || source.moduleId, moduleId),
    trackId: text(source.trackId || source.track),
    type,
    typeLabel: TYPE_LABELS[type] || 'Conteúdo',
    itemType: 'document',
    role,
    origin,
    category: text(source.category),
    courseId: text(source.courseId),
    legacySectionId: text(source.legacySectionId),
    projectId: text(source.projectId),
    required: inferRequired(source, type, origin, role),
    title,
    description: text(source.description || source.summary),
    sourcePath,
    contentUrl: text(source.contentUrl || source.url || source.contentPath),
    content,
    words: number(source.words || source.wordCount),
    readingMinutes: Math.max(1, number(source.readingMinutes || source.minutes, Math.ceil(number(source.words) / 210) || 1)),
    prerequisites: normalizePrerequisites(source),
    chapterNumber: source.chapterNumber ?? null,
    labNumber: source.labNumber ?? null,
    coursePath: text(source.coursePath),
    memberships: normalizeMemberships(source),
    resourceIds: unique(list(source.resourceIds ?? source.assetIds).map(refId)),
    searchText: text(source.searchText || source.searchIndex),
    librarySection: text(source.librarySection || source.section),
  }
}

function inferResourceKind(sourcePath, explicit) {
  const known = text(explicit).toLowerCase()
  if (RESOURCE_KIND_LABELS[known]) return known
  const extension = sourcePath.split('.').pop()?.toLowerCase()
  if (['png', 'jpg', 'jpeg', 'gif', 'webp', 'avif', 'svg', 'ico'].includes(extension)) return 'image'
  if (['md', 'markdown', 'rst'].includes(extension)) return 'markdown'
  if (['json', 'jsonl', 'csv', 'tsv', 'sql'].includes(extension)) return 'data'
  if (['conf', 'cfg', 'ini', 'toml', 'yaml', 'yml', 'xml', 'env', 'service'].includes(extension)) return 'config'
  if (['txt', 'log'].includes(extension)) return 'text'
  return 'code'
}

function inferLanguage(sourcePath, explicit) {
  if (text(explicit)) return text(explicit).toLowerCase()
  const name = sourcePath.split('/').pop()?.toLowerCase() || ''
  if (name === 'dockerfile') return 'dockerfile'
  if (name === 'makefile') return 'makefile'
  const extension = name.split('.').pop()
  return {
    bash: 'shell', c: 'c', cc: 'cpp', conf: 'config', cpp: 'cpp', cs: 'csharp',
    css: 'css', csv: 'csv', go: 'go', h: 'c', hpp: 'cpp', html: 'html',
    ini: 'ini', java: 'java', js: 'javascript', json: 'json', jsonl: 'json',
    jsx: 'jsx', kt: 'kotlin', md: 'markdown', mjs: 'javascript', ps1: 'powershell',
    py: 'python', rb: 'ruby', rs: 'rust', sh: 'shell', sql: 'sql', toml: 'toml',
    ts: 'typescript', tsx: 'tsx', xml: 'xml', yaml: 'yaml', yml: 'yaml', zsh: 'shell',
  }[extension] || extension || 'text'
}

function normalizeResource(raw, index) {
  const source = typeof raw === 'object' && raw !== null ? raw : { id: raw }
  const sourcePath = text(source.sourcePath || source.path || source.file)
  const id = text(source.id || source.resourceId || source.assetId, sourcePath || `resource-${index + 1}`)
  const kind = inferResourceKind(sourcePath, source.kind || source.type)
  const title = text(
    source.title || source.name,
    sourcePath.split('/').pop()?.replace(/[-_]/g, ' ') || `Arquivo ${index + 1}`,
  )
  return {
    id,
    order: number(source.order, index),
    itemType: 'resource',
    title,
    description: text(source.description || source.summary),
    sourcePath,
    contentUrl: text(source.contentUrl || source.url || source.contentPath),
    kind,
    kindLabel: RESOURCE_KIND_LABELS[kind] || 'Arquivo',
    language: inferLanguage(sourcePath, source.language),
    bytes: Math.max(0, number(source.bytes || source.size)),
    moduleId: text(source.moduleId || source.module),
    origin: inferOrigin(source, kind === 'markdown' ? 'reference' : ''),
    category: text(source.category),
    courseId: text(source.courseId),
    legacySectionId: text(source.legacySectionId),
    projectId: text(source.projectId),
    memberships: normalizeMemberships(source),
    relatedDocumentIds: unique(
      list(source.relatedDocumentIds ?? source.referencedBy ?? source.documentIds).map(refId),
    ),
    aliasOfDocumentId: text(source.aliasOfDocumentId),
    searchText: text(source.searchText || source.searchIndex),
    librarySection: text(source.librarySection || source.section),
  }
}

function normalizeGroup(raw, index, groupType) {
  const source = typeof raw === 'object' && raw !== null ? raw : { id: raw }
  const id = text(source.id || source.collectionId || source.courseId, `${groupType}-${index + 1}`)
  const grouping = `${id} ${text(source.kind)} ${text(source.category)}`
  const inferredSection = canonicalSection(grouping)
  const inferredOrigin = groupType === 'legacy' || inferredSection === 'security' ? 'legacy' : 'formation'
  return {
    id,
    order: number(source.order, index),
    groupType,
    title: text(source.title || source.name, `Coleção ${index + 1}`),
    description: text(source.description || source.summary),
    origin: text(source.origin, inferredOrigin),
    librarySection: text(source.librarySection || source.section, inferredSection),
    moduleIds: unique([
      ...list(source.moduleIds ?? source.modules).map(refId),
      refId(source.moduleId),
    ]),
    documentIds: unique(list(source.documentIds ?? source.documents).map(refId)),
    resourceIds: unique(list(source.resourceIds ?? source.assets ?? source.assetIds).map(refId)),
  }
}

function implicitGroups(modules, resources) {
  const groups = []
  modules.forEach((module) => {
    const buckets = new Map()
    const items = [...module.documents, ...resources.filter((resource) => resource.moduleId === module.id)]
    items.forEach((item) => {
      const relative = item.sourcePath.startsWith(`${module.path}/`)
        ? item.sourcePath.slice(module.path.length + 1)
        : item.sourcePath
      const parts = relative.split('/').filter(Boolean)
      const key = parts.length > 1 ? parts[0] : 'visao-geral'
      const bucket = buckets.get(key) || { documents: [], resources: [], origins: [] }
      if (item.itemType === 'resource') bucket.resources.push(item.id)
      else bucket.documents.push(item.id)
      bucket.origins.push(item.origin)
      buckets.set(key, bucket)
    })
    ;[...buckets.entries()].forEach(([key, bucket], index) => {
      const origin = bucket.origins.filter((value) => value === 'legacy').length > bucket.origins.length / 2
        ? 'legacy'
        : 'formation'
      groups.push({
        id: `folder-${module.id}-${slug(key)}`,
        order: module.order * 100 + index,
        groupType: origin === 'legacy' ? 'legacy' : 'course',
        title: key === 'visao-geral'
          ? (LEGACY_COLLECTION_TITLES[module.id] || `Visão geral · ${module.title}`)
          : key.replace(/[-_]/g, ' ').replace(/\b\w/g, (character) => character.toUpperCase()),
        description: `Materiais locais em ${module.path}/${key === 'visao-geral' ? '' : key}`,
        origin,
        librarySection: '',
        moduleIds: [module.id],
        documentIds: bucket.documents,
        resourceIds: bucket.resources,
      })
    })
  })
  return groups
}

function mergeDocument(primary, fallback) {
  if (!primary) return fallback
  if (!fallback) return primary
  return {
    ...fallback,
    ...primary,
    prerequisites: unique([...(fallback.prerequisites || []), ...(primary.prerequisites || [])]),
  }
}

/**
 * Converte tanto o schema gerado pela aplicação quanto formatos antigos
 * embutidos em trilhas para um modelo único, imutável e simples para a UI.
 */
export function normalizeCatalog(input) {
  const raw = input && typeof input === 'object' ? input : {}
  const topDocuments = list(raw.documents || raw.docs || raw.lessons)
  const documentMap = new Map()

  topDocuments.forEach((document, index) => {
    const normalized = normalizeDocument(document, index)
    documentMap.set(normalized.id, normalized)
    if (normalized.sourcePath) documentMap.set(normalized.sourcePath, normalized)
  })

  const rawTracks = list(raw.tracks || raw.paths || raw.learningPaths)
  const topModules = list(raw.modules || raw.sections)
  const embeddedModules = rawTracks.flatMap((track) =>
    list(track?.modules).filter((module) => module && typeof module === 'object'),
  )
  const moduleSources = [...topModules, ...embeddedModules]
  const moduleMap = new Map()

  moduleSources.forEach((moduleValue, moduleIndex) => {
    const source = typeof moduleValue === 'object' && moduleValue !== null
      ? moduleValue
      : { id: moduleValue }
    const id = text(source.id || source.moduleId, slug(source.title || source.name, `module-${moduleIndex + 1}`))
    if (moduleMap.has(id)) return

    const inlineDocuments = list(source.documents || source.chapters || source.lessons || source.files)
    inlineDocuments.forEach((documentValue, documentIndex) => {
      const reference = refId(documentValue)
      const known = documentMap.get(reference)
      const inline = typeof documentValue === 'object'
        ? normalizeDocument(documentValue, documentIndex, id)
        : null
      const normalized = mergeDocument(inline, known)
      if (normalized) {
        const withModule = { ...normalized, moduleId: normalized.moduleId || id }
        documentMap.set(withModule.id, withModule)
        if (withModule.sourcePath) documentMap.set(withModule.sourcePath, withModule)
      }
    })

    const requestedIds = unique([
      ...list(source.documentIds).map(refId),
      ...list(source.documents).map(refId),
      ...list(source.chapterIds).map(refId),
      ...list(source.labIds).map(refId),
      ...list(source.referenceIds).map(refId),
    ])
    const inferredDocuments = [...new Map([...documentMap.values()].map((doc) => [doc.id, doc])).values()]
      .filter((doc) => doc.moduleId === id)
    const requestedDocuments = requestedIds.map((documentId) => documentMap.get(documentId)).filter(Boolean)
    const documents = [...new Map([...requestedDocuments, ...inferredDocuments].map((doc) => [doc.id, doc])).values()]
      .map((doc) => ({ ...doc, moduleId: doc.moduleId || id }))
      .sort(byOrder)

    documents.forEach((doc) => documentMap.set(doc.id, doc))

    moduleMap.set(id, {
      id,
      order: number(source.order, moduleIndex),
      trackId: text(source.trackId || source.track),
      path: text(source.path),
      title: text(source.title || source.name, `Módulo ${id}`),
      description: text(source.description || source.summary),
      status: text(source.status, 'active'),
      maturity: text(source.maturity),
      estimatedHours: hourRange(source.estimatedHours ?? source.hours),
      prerequisiteModuleIds: unique(list(source.prerequisiteModuleIds || source.prerequisites).map(refId)),
      resourceIds: unique(list(source.resourceIds ?? source.assetIds ?? source.assets).map(refId)),
      documents,
      labs: documents.filter((document) => document.type === 'lab'),
      stats: source.stats && typeof source.stats === 'object' ? source.stats : {},
    })
  })

  // Documentos sem módulo conhecido continuam acessíveis em uma biblioteca.
  const allDistinctDocuments = [...new Map([...documentMap.values()].map((doc) => [doc.id, doc])).values()]
  const orphanDocuments = allDistinctDocuments.filter((document) => !moduleMap.has(document.moduleId))
  if (orphanDocuments.length) {
    const id = 'biblioteca-geral'
    moduleMap.set(id, {
      id,
      order: moduleMap.size,
      trackId: '',
      path: '',
      title: 'Biblioteca geral',
      description: 'Materiais que ainda não foram associados a um módulo.',
      status: 'active',
      maturity: '',
      estimatedHours: { min: 0, max: 0 },
      prerequisiteModuleIds: [],
      resourceIds: [],
      documents: orphanDocuments.sort(byOrder),
      labs: orphanDocuments.filter((document) => document.type === 'lab'),
      stats: {},
    })
  }

  const modules = [...moduleMap.values()].sort(byOrder)
  const normalizedTracks = (rawTracks.length ? rawTracks : [FALLBACK_TRACK]).map((trackValue, trackIndex) => {
    const source = typeof trackValue === 'object' && trackValue !== null
      ? trackValue
      : { id: trackValue }
    const id = text(source.id || source.trackId, slug(source.title || source.name, `track-${trackIndex + 1}`))
    const references = unique([
      ...list(source.moduleIds).map(refId),
      ...list(source.modules).map(refId),
    ])
    let trackModules = references.map((moduleId) => moduleMap.get(moduleId)).filter(Boolean)
    if (!trackModules.length) {
      trackModules = modules.filter((module) => module.trackId === id)
    }
    if (!trackModules.length && rawTracks.length === 1) trackModules = modules
    const documents = trackModules.flatMap((module) => module.documents)

    return {
      id,
      order: number(source.order, trackIndex),
      title: text(source.title || source.name, `Trilha ${trackIndex + 1}`),
      description: text(source.description || source.summary),
      modules: trackModules.sort(byOrder),
      documents,
      labs: documents.filter((document) => document.type === 'lab'),
      stats: {
        modules: trackModules.length,
        documents: documents.length,
        labs: documents.filter((document) => document.type === 'lab').length,
        readingMinutes: documents.reduce((total, document) => total + document.readingMinutes, 0),
        estimatedHours: sumHourRanges(trackModules),
      },
    }
  }).sort(byOrder)

  const assignedModuleIds = new Set(normalizedTracks.flatMap((track) => track.modules.map((module) => module.id)))
  const unassignedModules = modules.filter((module) => !assignedModuleIds.has(module.id))
  if (unassignedModules.length) {
    const documents = unassignedModules.flatMap((module) => module.documents)
    normalizedTracks.push({
      ...FALLBACK_TRACK,
      id: normalizedTracks.length ? 'outros-modulos' : FALLBACK_TRACK.id,
      title: normalizedTracks.length ? 'Outros módulos' : FALLBACK_TRACK.title,
      modules: unassignedModules,
      documents,
      labs: documents.filter((document) => document.type === 'lab'),
      stats: {
        modules: unassignedModules.length,
        documents: documents.length,
        labs: documents.filter((document) => document.type === 'lab').length,
        readingMinutes: documents.reduce((total, document) => total + document.readingMinutes, 0),
        estimatedHours: sumHourRanges(unassignedModules),
      },
    })
  }

  const documents = [...new Map(modules.flatMap((module) => module.documents).map((doc) => [doc.id, doc])).values()]
    .sort(byOrder)
  const labs = documents.filter((document) => document.type === 'lab')

  const resourceSource = Array.isArray(raw.resources) ? raw.resources : list(raw.assets)
  const resources = resourceSource.map(normalizeResource).map((resource) => {
    if (resource.moduleId && moduleMap.has(resource.moduleId)) return resource
    const owner = modules.find((module) =>
      module.resourceIds.includes(resource.id)
      || (module.path && resource.sourcePath.startsWith(`${module.path}/`)),
    )
    const fallbackLibrary = modules.find((module) => module.id === 'biblioteca-geral')
    return owner
      ? { ...resource, moduleId: owner.id }
      : fallbackLibrary && !resource.moduleId
        ? { ...resource, moduleId: fallbackLibrary.id }
        : resource
  }).sort(byOrder)
  const visibleResources = resources.filter((resource) => !resource.aliasOfDocumentId)
  modules.forEach((module) => {
    module.resources = visibleResources.filter((resource) => resource.moduleId === module.id)
    module.resourceIds = unique([...module.resourceIds, ...module.resources.map((resource) => resource.id)])
  })

  const courses = list(raw.courses).map((group, index) => normalizeGroup(group, index, 'course'))
  const legacySections = list(raw.legacySections)
    .map((group, index) => normalizeGroup(group, index, 'legacy'))
  const projects = list(raw.projects)
    .map((group, index) => normalizeGroup(group, index, 'project'))
  const explicitCollections = list(raw.collections)
    .map((group, index) => normalizeGroup(group, index, 'collection'))
  const explicitGroups = [...courses, ...legacySections, ...projects, ...explicitCollections]
  const groups = explicitGroups.length ? explicitGroups : implicitGroups(modules, resources)
  const collections = explicitCollections.length ? explicitCollections : groups

  return {
    schemaVersion: number(raw.schemaVersion, 1),
    generatedAt: text(raw.generatedAt),
    title: text(raw.title, 'RedTeam Essentials'),
    description: text(raw.description, 'Formação prática do zero ao avançado.'),
    tracks: normalizedTracks,
    modules,
    documents,
    labs,
    resources,
    visibleResources,
    collections,
    courses,
    legacySections,
    projects,
    groups,
    stats: {
      tracks: normalizedTracks.length,
      modules: modules.length,
      documents: documents.length,
      labs: labs.length,
      resources: resources.length,
      readingMinutes: documents.reduce((total, document) => total + document.readingMinutes, 0),
      ...(raw.stats && typeof raw.stats === 'object' ? raw.stats : {}),
      estimatedHours: sumHourRanges(modules),
      visibleResources: visibleResources.length,
      libraryItems: documents.length + visibleResources.length,
      coverage: raw.stats?.coverage && typeof raw.stats.coverage === 'object'
        ? raw.stats.coverage
        : { documents: documents.length, resources: resources.length },
    },
  }
}

export function documentContext(catalog, documentId) {
  const document = catalog.documents.find((item) => item.id === documentId)
  if (!document) return null
  const module = catalog.modules.find((item) => item.id === document.moduleId)
  const track = catalog.tracks.find((item) => item.modules.some((candidate) => candidate.id === module?.id))
  const allModuleDocuments = module?.documents || []
  const scopedModuleDocuments = document.courseId
    ? allModuleDocuments.filter((item) => item.courseId === document.courseId)
    : document.legacySectionId
      ? allModuleDocuments.filter((item) => item.legacySectionId === document.legacySectionId)
      : allModuleDocuments.filter((item) => item.origin === document.origin)
  const formationDocuments = catalog.modules
    .filter((candidate) => /^\d{2}$/.test(candidate.id))
    .sort((first, second) => Number(first.id) - Number(second.id))
    .flatMap((candidate) => candidate.documents.filter(isFormationItem))
  const navigationDocuments = isFormationItem(document)
    ? [...new Map(formationDocuments.map((item) => [item.id, item])).values()]
    : scopedModuleDocuments
  const index = navigationDocuments.findIndex((item) => item.id === document.id)
  return {
    document,
    module,
    track,
    previous: index > 0 ? navigationDocuments[index - 1] : null,
    next: index >= 0 && index < navigationDocuments.length - 1 ? navigationDocuments[index + 1] : null,
  }
}

export function collectionContext(catalog, collectionId) {
  const collection = (catalog.groups || []).find((item) => item.id === collectionId)
  if (!collection) return null
  const requestedDocuments = new Set(collection.documentIds || [])
  const requestedResources = new Set(collection.resourceIds || [])
  const documents = catalog.documents.filter((document) =>
    requestedDocuments.has(document.id) || document.memberships.includes(collection.id),
  )
  const resources = catalog.resources.filter((resource) =>
    !resource.aliasOfDocumentId
    && (requestedResources.has(resource.id) || resource.memberships.includes(collection.id)),
  )
  const modules = catalog.modules.filter((module) =>
    collection.moduleIds.includes(module.id)
    || documents.some((document) => document.moduleId === module.id)
    || resources.some((resource) => resource.moduleId === module.id),
  )
  return { collection, documents, resources, modules }
}

export function itemContext(catalog, item) {
  const module = catalog?.modules?.find((candidate) => candidate.id === item?.moduleId) || null
  const legacySection = catalog?.legacySections?.find((candidate) =>
    candidate.id === item?.legacySectionId || item?.memberships?.includes(candidate.id),
  ) || null
  const project = catalog?.projects?.find((candidate) =>
    candidate.id === item?.projectId || item?.memberships?.includes(candidate.id),
  ) || null
  const course = catalog?.courses?.find((candidate) =>
    candidate.id === item?.courseId || item?.memberships?.includes(candidate.id),
  ) || null
  const primary = legacySection || project || course || module
  return {
    primary,
    module,
    legacySection,
    project,
    course,
    primaryTitle: primary?.title || 'Documentação geral',
    moduleTitle: module ? `${module.id} · ${module.title}` : '',
  }
}

export function isFormationItem(item) {
  const origin = searchable(item?.origin || 'formation')
  return ['formation', 'formacao', 'curriculum', 'course', 'training', 'current'].includes(origin)
}

function canonicalSection(value) {
  const normalized = searchable(value)
  if (/formacao|formation|training|course/.test(normalized)) return 'formation'
  if (/security|seguranca|legacy|legado|acervo/.test(normalized)) return 'security'
  if (/lab|practice|pratica|project|projeto/.test(normalized)) return 'practice'
  if (/tool|ferramenta|code|codigo|asset/.test(normalized)) return 'tools'
  if (/doc|guide|guia|governance/.test(normalized)) return 'documentation'
  return ''
}

export function librarySectionsFor(item) {
  if (!item) return []
  const sections = new Set()
  const explicit = canonicalSection(item.librarySection)
  if (explicit) sections.add(explicit)

  const origin = searchable(item.origin)
  const role = searchable(item.role)
  const category = searchable(item.category)
  const memberships = searchable((item.memberships || []).join(' '))
  const classification = `${origin} ${role} ${category} ${memberships}`
  if (/legacy|legado|security|seguranca|acervo/.test(classification)) sections.add('security')
  if (
    item.type === 'lab'
    || /lab|exercise|exercicio|project|projeto|challenge|desafio/.test(classification)
  ) sections.add('practice')

  if (item.itemType === 'resource') {
    if (['code', 'config', 'data', 'text'].includes(item.kind)) sections.add('tools')
    if (item.kind === 'markdown' || /doc|guide|guia/.test(origin)) sections.add('documentation')
  } else if (/global|documentation|documentacao|governance|guide|guia/.test(classification)) {
    sections.add('documentation')
  }

  if (!sections.size || (item.itemType === 'document' && origin === 'formation')) sections.add('formation')
  return [...sections]
}

export function librarySectionFor(item) {
  const sections = librarySectionsFor(item)
  return sections.includes('formation') ? 'formation' : sections[0] || 'documentation'
}

export function libraryItems(catalog) {
  return [
    ...(catalog?.documents || []),
    ...(catalog?.visibleResources || catalog?.resources?.filter((resource) => !resource.aliasOfDocumentId) || []),
  ]
}

export function itemsForSection(catalog, sectionId) {
  return libraryItems(catalog).filter((item) => librarySectionsFor(item).includes(sectionId))
}

export function searchLibrary(catalog, query, filters = {}) {
  const needle = searchable(query)
  const tokens = needle.split(/\s+/).filter(Boolean)
  const groups = catalog?.groups || []
  const results = libraryItems(catalog).map((item) => {
    const module = catalog.modules.find((candidate) => candidate.id === item.moduleId)
    const itemGroups = groups.filter((group) =>
      item.memberships?.includes(group.id)
      || group.documentIds?.includes(item.id)
      || group.resourceIds?.includes(item.id),
    )
    const haystack = searchable([
      item.title,
      item.description,
      item.sourcePath,
      item.typeLabel,
      item.kindLabel,
      item.language,
      item.role,
      item.origin,
      item.searchText,
      module?.title,
      ...itemGroups.map((group) => group.title),
    ].join(' '))
    const words = haystack.split(/[^a-z0-9+#.]+/).filter(Boolean)
    const matches = tokens.filter((token) =>
      token.length <= 3
        ? words.some((word) => word === token || word.startsWith(token))
        : haystack.includes(token),
    ).length
    const normalizedTitle = searchable(item.title)
    const titleWords = normalizedTitle.split(/[^a-z0-9+#.]+/).filter(Boolean)
    const exactTitle = needle && (
      needle.length <= 3
        ? titleWords.some((word) => word === needle || word.startsWith(needle))
        : normalizedTitle.includes(needle)
    ) ? 4 : 0
    return {
      item,
      document: item.itemType === 'document' ? item : null,
      resource: item.itemType === 'resource' ? item : null,
      module,
      groups: itemGroups,
      sections: librarySectionsFor(item),
      score: matches + exactTitle,
    }
  }).filter((result) => !tokens.length || result.score >= tokens.length)

  const queryMatched = filters.includeEmpty || tokens.length ? results : []
  const facets = {
    documents: queryMatched.filter(({ item }) => item.itemType === 'document').length,
    resources: queryMatched.filter(({ item }) => item.itemType === 'resource').length,
    sections: Object.fromEntries(LIBRARY_SECTIONS.map(({ id }) => [
      id,
      queryMatched.filter((result) => result.sections.includes(id)).length,
    ])),
    origins: {},
    kinds: {},
  }
  queryMatched.forEach(({ item }) => {
    const origin = item.origin || 'unknown'
    const kind = item.itemType === 'resource' ? item.kind : item.type
    facets.origins[origin] = (facets.origins[origin] || 0) + 1
    facets.kinds[kind] = (facets.kinds[kind] || 0) + 1
  })

  const filtered = queryMatched.filter(({ item, sections }) => {
    if (filters.itemType && filters.itemType !== 'all' && item.itemType !== filters.itemType) return false
    if (filters.section && !sections.includes(filters.section)) return false
    if (filters.moduleId && item.moduleId !== filters.moduleId) return false
    if (filters.origin && item.origin !== filters.origin) return false
    const kind = item.itemType === 'resource' ? item.kind : item.type
    if (filters.kind && kind !== filters.kind) return false
    return true
  }).sort((a, b) =>
    b.score - a.score
    || (a.item.itemType === b.item.itemType ? 0 : a.item.itemType === 'document' ? -1 : 1)
    || byOrder(a.item, b.item),
  )

  return { results: filtered, total: filtered.length, facets }
}

export function searchCatalog(catalog, query, limit = Number.POSITIVE_INFINITY) {
  const found = searchLibrary(catalog, query, { itemType: 'document' }).results
  return found.slice(0, limit).map((result) => ({
    document: result.document,
    module: result.module,
    score: result.score,
  }))
}

function resolveLocalPath(currentItem, href) {
  if (!href || /^(?:[a-z]+:|#|\/\/)/i.test(href)) return null
  let cleanHref
  try {
    cleanHref = decodeURIComponent(href.split('#')[0].split('?')[0])
  } catch {
    return null
  }
  const directoryLink = cleanHref.endsWith('/')

  const currentParts = (currentItem?.sourcePath || '').split('/')
  currentParts.pop()
  const joined = [...currentParts, ...cleanHref.split('/')]
  const normalized = []
  for (const part of joined) {
    if (!part || part === '.') continue
    if (part === '..') {
      if (!normalized.length) return null
      normalized.pop()
    }
    else normalized.push(part)
  }
  return `${normalized.join('/')}${directoryLink ? '/README.md' : ''}`
}

export function resolveLocalDocument(catalog, currentDocument, href) {
  const target = resolveLocalPath(currentDocument, href)
  if (!target || (!href.endsWith('/') && !target.toLowerCase().endsWith('.md'))) return null
  return catalog.documents.find((document) => document.sourcePath === target) || null
}

export function resolveLocalResource(catalog, currentItem, href) {
  const target = resolveLocalPath(currentItem, href)
  if (!target) return null
  return catalog.resources.find((resource) => resource.sourcePath === target) || null
}

export function resolveLocalItem(catalog, currentItem, href) {
  return resolveLocalDocument(catalog, currentItem, href)
    || resolveLocalResource(catalog, currentItem, href)
    || null
}

export { RESOURCE_KIND_LABELS, TYPE_LABELS }
