import React, { useEffect, useMemo, useRef, useState } from 'react'

import {
  collectionContext,
  itemContext,
  itemsForSection,
  LIBRARY_SECTIONS,
  librarySectionsFor,
  searchLibrary,
} from '../lib/catalog.js'
import {
  completionBreakdown,
  isDocumentCompleted,
  moduleAvailability,
} from '../lib/progress.js'
import { Icon } from './Icons.jsx'
import { ProgressBar, ProgressRing } from './ProgressUI.jsx'

const PAGE_SIZE = 60

function formatBytes(bytes) {
  const value = Number(bytes) || 0
  if (value < 1024) return `${value} B`
  if (value < 1024 * 1024) return `${(value / 1024).toFixed(value < 10240 ? 1 : 0)} KB`
  return `${(value / (1024 * 1024)).toFixed(1)} MB`
}

function iconFor(item) {
  if (item.itemType === 'document') return item.type === 'lab' ? 'flask' : 'book'
  if (item.kind === 'code') return 'code'
  if (item.kind === 'image') return 'image'
  if (item.kind === 'data') return 'database'
  if (item.kind === 'config') return 'terminal'
  return 'file'
}

function itemLabel(item) {
  return item.itemType === 'document' ? item.typeLabel : item.kindLabel
}

function openItem(item, navigate) {
  navigate(item.itemType === 'resource' ? 'resource' : 'learn', item.id)
}

function ModuleGatePanel({ catalog, module, navigate, state }) {
  const pending = state.missingModuleIds
    .map((moduleId) => catalog.modules.find((candidate) => candidate.id === moduleId))
    .filter(Boolean)
  const visible = pending.slice(0, 8)
  const hiddenCount = Math.max(0, pending.length - visible.length)
  return (
    <section className="module-gate" role="status">
      <span className="module-gate-icon"><Icon name="lock" size={30} /></span>
      <span className="eyebrow">MÓDULO BLOQUEADO</span>
      <h2>Conclua a base curricular antes de iniciar</h2>
      <p>
        Você pode consultar este mapa, mas as leituras e atividades do módulo {module.id}
        {' '}serão liberadas quando os conteúdos obrigatórios dos {pending.length} módulo{pending.length === 1 ? '' : 's'} pendente{pending.length === 1 ? '' : 's'} forem concluídos.
      </p>
      <div className="module-gate-requirements" aria-label="Módulos pendentes">
        {visible.map((required) => (
          <button key={required.id} onClick={() => navigate('module', required.id)} type="button">
            <span>{required.id}</span><strong>{required.title}</strong><Icon name="chevronRight" size={16} />
          </button>
        ))}
      </div>
      {hiddenCount ? <small className="module-gate-more">E mais {hiddenCount} módulo{hiddenCount === 1 ? '' : 's'} pendente{hiddenCount === 1 ? '' : 's'}.</small> : null}
      {pending[0] ? (
        <button className="button button--primary" onClick={() => navigate('module', pending[0].id)} type="button">
          Continuar pelo módulo {pending[0].id} <Icon name="arrowRight" size={16} />
        </button>
      ) : null}
    </section>
  )
}

export function LibraryItemList({ catalog, items, modules, navigate, progress, emptyTitle = 'Nenhum material encontrado' }) {
  const [visibleCount, setVisibleCount] = useState(PAGE_SIZE)

  useEffect(() => setVisibleCount(PAGE_SIZE), [items])

  if (!items.length) {
    return (
      <div className="empty-panel library-empty">
        <span><Icon name="search" size={27} /></span>
        <h2>{emptyTitle}</h2>
        <p>Altere os filtros ou pesquise com termos mais curtos.</p>
      </div>
    )
  }

  const visible = items.slice(0, visibleCount)
  return (
    <>
      <div className="library-result-summary" aria-live="polite">
        Exibindo <strong>{visible.length}</strong> de <strong>{items.length}</strong> itens
      </div>
      <div className="library-items">
        {visible.map((item) => {
          const module = modules.find((candidate) => candidate.id === item.moduleId)
          const context = catalog ? itemContext(catalog, item) : { primaryTitle: module?.title, module: null }
          const showPhysicalModule = context.module && context.primary?.id !== context.module.id
          const completed = item.itemType === 'document' && isDocumentCompleted(progress, item.id)
          return (
            <button className="library-item" key={`${item.itemType}-${item.id}`} onClick={() => openItem(item, navigate)} type="button">
              <span className={`library-item-icon library-item-icon--${item.itemType === 'resource' ? item.kind : item.type}`}>
                <Icon name={iconFor(item)} size={19} />
              </span>
              <span className="library-item-main">
                <span className="library-item-title"><strong>{item.title}</strong>{completed ? <em><Icon name="check" size={12} /> Lido</em> : null}</span>
                <small>{context.primaryTitle}{showPhysicalModule ? ` · pasta do módulo ${context.module.id}` : ''}</small>
                <code>{item.sourcePath}</code>
              </span>
              <span className="library-item-meta">
                <span>{itemLabel(item)}</span>
                {item.itemType === 'resource' ? <small>{item.language || item.kind} · {formatBytes(item.bytes)}</small> : <small>{item.readingMinutes} min de leitura</small>}
                {item.itemType === 'document' ? <em className={item.required ? 'is-required' : ''}>{item.required ? 'Obrigatório' : 'Opcional'}</em> : null}
              </span>
              <Icon name="chevronRight" size={17} />
            </button>
          )
        })}
      </div>
      {visible.length < items.length ? (
        <button className="button button--secondary library-load-more" onClick={() => setVisibleCount((count) => count + PAGE_SIZE)} type="button">
          Mostrar mais {Math.min(PAGE_SIZE, items.length - visible.length)} itens
        </button>
      ) : null}
    </>
  )
}

function FilterBar({ query, setQuery, itemType, setItemType, moduleId, setModuleId, kind, setKind, origin, setOrigin, modules, items }) {
  const origins = [...new Set(items.map((item) => item.origin).filter(Boolean))].sort()
  const kinds = [...new Set(items.map((item) => item.itemType === 'resource' ? item.kind : item.type).filter(Boolean))].sort()
  return (
    <div className="library-filters">
      <label className="library-query">
        <span className="sr-only">Buscar nesta seção</span>
        <Icon name="search" size={18} />
        <input onChange={(event) => setQuery(event.target.value)} placeholder="Buscar título, caminho, linguagem ou tema..." type="search" value={query} />
      </label>
      <label><span className="sr-only">Tipo de item</span><select onChange={(event) => setItemType(event.target.value)} value={itemType}><option value="all">Conteúdo e arquivos</option><option value="document">Somente conteúdos</option><option value="resource">Somente arquivos</option></select></label>
      <label><span className="sr-only">Módulo</span><select onChange={(event) => setModuleId(event.target.value)} value={moduleId}><option value="">Todos os módulos</option>{modules.map((module) => <option key={module.id} value={module.id}>{module.id} · {module.title}</option>)}</select></label>
      <label><span className="sr-only">Formato</span><select onChange={(event) => setKind(event.target.value)} value={kind}><option value="">Todos os formatos</option>{kinds.map((value) => <option key={value} value={value}>{value}</option>)}</select></label>
      {origins.length > 1 ? <label><span className="sr-only">Origem</span><select onChange={(event) => setOrigin(event.target.value)} value={origin}><option value="">Todas as origens</option>{origins.map((value) => <option key={value} value={value}>{value}</option>)}</select></label> : null}
    </div>
  )
}

function useLibraryFilters(catalog, section, baseItems) {
  const [query, setQuery] = useState('')
  const [itemType, setItemType] = useState('all')
  const [moduleId, setModuleId] = useState('')
  const [kind, setKind] = useState('')
  const [origin, setOrigin] = useState('')

  useEffect(() => {
    setQuery('')
    setItemType('all')
    setModuleId('')
    setKind('')
    setOrigin('')
  }, [section])

  const allowed = useMemo(() => new Set(baseItems.map((item) => `${item.itemType}:${item.id}`)), [baseItems])
  const search = useMemo(() => searchLibrary(catalog, query, {
    includeEmpty: true,
    itemType,
    moduleId,
    kind,
    origin,
  }), [catalog, itemType, kind, moduleId, origin, query])
  const items = search.results.map((result) => result.item)
    .filter((item) => allowed.has(`${item.itemType}:${item.id}`))

  return {
    items,
    values: { query, itemType, moduleId, kind, origin },
    setters: { setQuery, setItemType, setModuleId, setKind, setOrigin },
  }
}

function groupsForSection(catalog, section) {
  return (catalog.groups || []).filter((group) => {
    const context = collectionContext(catalog, group.id)
    const items = [...(context?.documents || []), ...(context?.resources || [])]
    if (!items.length) return false
    return items.some((item) => librarySectionsFor(item).includes(section))
  })
}

export function LibraryView({ catalog, progress, navigate, sectionId }) {
  const activeSection = LIBRARY_SECTIONS.some((section) => section.id === sectionId) ? sectionId : 'formation'
  const section = LIBRARY_SECTIONS.find((item) => item.id === activeSection)
  const activeTabRef = useRef(null)
  const baseItems = useMemo(() => itemsForSection(catalog, activeSection), [activeSection, catalog])
  const filters = useLibraryFilters(catalog, activeSection, baseItems)
  const groups = useMemo(() => groupsForSection(catalog, activeSection), [activeSection, catalog])
  const sectionCounts = Object.fromEntries(LIBRARY_SECTIONS.map(({ id }) => [id, itemsForSection(catalog, id).length]))

  useEffect(() => {
    activeTabRef.current?.scrollIntoView({ block: 'nearest', inline: 'center' })
  }, [activeSection])

  return (
    <div className="page library-page">
      <header className="library-hero">
        <div><span className="eyebrow">CATÁLOGO COMPLETO</span><h1>Biblioteca</h1><p>Explore a formação, os materiais complementares, laboratórios e todos os arquivos de código sem perder a organização original.</p></div>
        <dl>
          <div><dt>Conteúdos</dt><dd>{catalog.documents.length}</dd></div>
          <div><dt>Arquivos</dt><dd>{catalog.visibleResources.length}</dd></div>
          <div><dt>Coleções</dt><dd>{catalog.groups.length}</dd></div>
        </dl>
      </header>

      <nav aria-label="Seções da biblioteca" className="library-tabs">
        {LIBRARY_SECTIONS.map((tab) => (
          <button aria-current={tab.id === activeSection ? 'page' : undefined} key={tab.id} onClick={() => navigate('library', tab.id)} ref={tab.id === activeSection ? activeTabRef : null} type="button">
            <span>{tab.title}</span><em>{sectionCounts[tab.id]}</em>
          </button>
        ))}
      </nav>

      <section className="library-section-heading">
        <div><span className="eyebrow">SEÇÃO ATUAL</span><h2>{section.title}</h2></div>
        <p>{baseItems.length} itens catalogados nesta seção.</p>
      </section>

      {groups.length ? (
        <section className="collection-strip" aria-label={`Coleções em ${section.title}`}>
          {groups.map((group) => {
            const context = collectionContext(catalog, group.id)
            const total = (context?.documents.length || 0) + (context?.resources.length || 0)
            return (
              <button key={group.id} onClick={() => navigate('collection', group.id)} title={group.title} type="button">
                <span><Icon name={group.origin === 'legacy' ? 'shield' : 'folder'} size={18} /></span>
                <span><strong>{group.title}</strong><small>{total} itens · {group.origin === 'legacy' ? 'Acervo legado' : 'Coleção'}</small></span>
                <Icon name="chevronRight" size={16} />
              </button>
            )
          })}
        </section>
      ) : null}

      <FilterBar {...filters.values} {...filters.setters} items={baseItems} modules={catalog.modules} />
      <LibraryItemList catalog={catalog} items={filters.items} modules={catalog.modules} navigate={navigate} progress={progress} />
    </div>
  )
}

export function ModuleView({ catalog, module, progress, navigate }) {
  const items = useMemo(() => [...module.documents, ...(module.resources || [])], [module])
  const filters = useLibraryFilters(catalog, `module-${module.id}`, items)
  const breakdown = completionBreakdown(module.documents, progress)
  const gate = moduleAvailability(module, catalog, progress)
  const track = catalog.tracks.find((candidate) => candidate.modules.some((item) => item.id === module.id))
  const groups = (catalog.groups || []).filter((group) => {
    const context = collectionContext(catalog, group.id)
    return context?.modules.some((candidate) => candidate.id === module.id)
  })

  return (
    <div className="page library-page">
      <div className="page-breadcrumbs"><button onClick={() => navigate('dashboard')} type="button">Início</button><Icon name="chevronRight" size={13} />{track ? <><button onClick={() => navigate('track', track.id)} type="button">{track.title}</button><Icon name="chevronRight" size={13} /></> : null}<span>Módulo {module.id}</span></div>
      <header className="module-library-hero">
        <span className="module-card-index">{module.id}</span>
        <div><span className="eyebrow">MÓDULO COMPLETO</span><h1>{module.title}</h1><p>{module.description}</p><div className="module-library-metrics"><span>{module.documents.length} conteúdos</span><span>{module.resources?.length || 0} arquivos</span><span>{module.labs.length} labs</span></div></div>
        <div><ProgressRing size="medium" value={breakdown.required.percent} /><small>Formação obrigatória<br />{breakdown.required.completed}/{breakdown.required.total}</small></div>
      </header>
      {!gate.unlocked ? (
        <ModuleGatePanel catalog={catalog} module={module} navigate={navigate} state={gate} />
      ) : (
        <>
          {groups.length ? <section className="collection-strip">{groups.map((group) => <button key={group.id} onClick={() => navigate('collection', group.id)} title={group.title} type="button"><span><Icon name="folder" size={18} /></span><span><strong>{group.title}</strong><small>{group.groupType === 'legacy' ? 'Acervo legado' : 'Coleção do módulo'}</small></span><Icon name="chevronRight" size={16} /></button>)}</section> : null}
          <FilterBar {...filters.values} {...filters.setters} items={items} modules={[module]} />
          <LibraryItemList catalog={catalog} items={filters.items} modules={catalog.modules} navigate={navigate} progress={progress} />
        </>
      )}
    </div>
  )
}

export function CollectionView({ catalog, context, progress, navigate }) {
  const { collection, documents, resources, modules } = context
  const items = useMemo(() => [...documents, ...resources], [documents, resources])
  const filters = useLibraryFilters(catalog, `collection-${collection.id}`, items)
  const breakdown = completionBreakdown(documents, progress)
  return (
    <div className="page library-page">
      <div className="page-breadcrumbs"><button onClick={() => navigate('library', collection.origin === 'legacy' ? 'security' : 'formation')} type="button">Biblioteca</button><Icon name="chevronRight" size={13} /><span>{collection.title}</span></div>
      <header className="collection-hero">
        <span><Icon name={collection.origin === 'legacy' ? 'shield' : 'folder'} size={29} /></span>
        <div><span className="eyebrow">{collection.origin === 'legacy' ? 'ACERVO DE SEGURANÇA' : 'COLEÇÃO'}</span><h1>{collection.title}</h1><p>{collection.description || 'Conteúdos e arquivos preservados em sua organização original.'}</p></div>
        <dl><div><dt>Conteúdos</dt><dd>{documents.length}</dd></div><div><dt>Arquivos</dt><dd>{resources.length}</dd></div><div><dt>Obrigatórios</dt><dd>{breakdown.required.total}</dd></div></dl>
      </header>
      <FilterBar {...filters.values} {...filters.setters} items={items} modules={modules.length ? modules : catalog.modules} />
      <LibraryItemList catalog={catalog} items={filters.items} modules={catalog.modules} navigate={navigate} progress={progress} />
    </div>
  )
}
