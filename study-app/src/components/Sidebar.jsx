import React, { useEffect, useMemo, useRef, useState } from 'react'

import { isFormationItem } from '../lib/catalog.js'
import { completionBreakdown, isDocumentCompleted } from '../lib/progress.js'
import { Icon } from './Icons.jsx'

export function Sidebar({ catalog, progress, route, navigate, open, onClose }) {
  const treeRef = useRef(null)
  const activeModuleRef = useRef(null)
  const activeDocumentRef = useRef(null)
  const activeDocument = route.view === 'learn'
    ? catalog.documents.find((document) => document.id === route.id)
    : null
  const activeResource = route.view === 'resource'
    ? catalog.resources.find((resource) => resource.id === route.id)
    : null
  const activeModule = route.view === 'module'
    ? catalog.modules.find((module) => module.id === route.id)
    : activeDocument
    ? catalog.modules.find((module) => module.id === activeDocument.moduleId)
    : activeResource
      ? catalog.modules.find((module) => module.id === activeResource.moduleId)
    : null
  const [openModules, setOpenModules] = useState(() => new Set())

  useEffect(() => {
    if (activeModule?.id) setOpenModules((current) => new Set([...current, activeModule.id]))
  }, [activeModule?.id])

  useEffect(() => {
    let innerFrame
    const outerFrame = requestAnimationFrame(() => {
      innerFrame = requestAnimationFrame(() => {
        const tree = treeRef.current
        const target = activeDocumentRef.current || activeModuleRef.current
        if (!tree || !target || !tree.contains(target)) return
        target.scrollIntoView({ behavior: 'auto', block: 'nearest', inline: 'nearest' })
      })
    })
    return () => {
      cancelAnimationFrame(outerFrame)
      if (innerFrame) cancelAnimationFrame(innerFrame)
    }
  }, [activeDocument?.id, activeModule?.id])

  const overall = useMemo(() => completionBreakdown(catalog.documents, progress).required, [catalog.documents, progress])
  const formationModules = useMemo(() => catalog.modules
    .filter((module) => /^\d{2}$/.test(module.id) && module.documents.some(isFormationItem))
    .sort((first, second) => Number(first.id) - Number(second.id)), [catalog.modules])
  const firstModuleId = formationModules[0]?.id || '00'
  const lastModuleId = formationModules.at(-1)?.id || firstModuleId
  const trackByModuleId = useMemo(() => new Map(catalog.tracks.flatMap((track) =>
    track.modules.map((module) => [module.id, track]),
  )), [catalog.tracks])

  function go(view, id) {
    navigate(view, id)
    onClose()
  }

  function toggle(setter, id) {
    setter((current) => {
      const next = new Set(current)
      if (next.has(id)) next.delete(id)
      else next.add(id)
      return next
    })
  }

  return (
    <>
      <div className={`sidebar-backdrop${open ? ' is-visible' : ''}`} onClick={onClose} />
      <aside aria-label="Navegação do curso" className={`sidebar${open ? ' is-open' : ''}`}>
        <div className="brand-row">
          <button aria-label="Ir ao painel" className="brand" onClick={() => go('dashboard')} type="button">
            <span className="brand-mark"><Icon name="shield" size={20} /></span>
            <span><strong>RTE Study</strong><small>RedTeam Essentials</small></span>
          </button>
          <button aria-label="Fechar menu" className="icon-button sidebar-close" onClick={onClose} type="button">
            <Icon name="close" />
          </button>
        </div>

        <nav className="primary-nav">
          <button aria-current={route.view === 'dashboard' ? 'page' : undefined} onClick={() => go('dashboard')} type="button">
            <Icon name="dashboard" /><span>Painel</span>
          </button>
          <button aria-current={['library', 'collection', 'resource'].includes(route.view) ? 'page' : undefined} onClick={() => go('library', 'formation')} type="button">
            <Icon name="layers" /><span>Biblioteca</span>
            <em>{catalog.stats.libraryItems}</em>
          </button>
          <button aria-current={route.view === 'labs' ? 'page' : undefined} onClick={() => go('labs')} type="button">
            <Icon name="flask" /><span>Laboratórios</span>
            <em>{catalog.labs.length}</em>
          </button>
          <button aria-current={route.view === 'progress' ? 'page' : undefined} onClick={() => go('progress')} type="button">
            <Icon name="progress" /><span>Meu progresso</span>
            <em>{overall.percent}%</em>
          </button>
        </nav>

        <div className="sidebar-label">Jornada · módulos {firstModuleId}–{lastModuleId}</div>
        <p className="curriculum-hint">Acesse diretamente qualquer módulo ou abra seus conteúdos.</p>
        <nav aria-label={`Módulos ${firstModuleId} a ${lastModuleId}`} className="curriculum-tree" ref={treeRef}>
          {formationModules.map((module) => {
            const moduleOpen = openModules.has(module.id)
            const moduleProgress = completionBreakdown(module.documents, progress).required
            const formationDocuments = module.documents.filter(isFormationItem)
            const track = trackByModuleId.get(module.id)
            const moduleActive = activeModule?.id === module.id
            return (
              <section className={`tree-module sidebar-module${moduleActive ? ' is-active' : ''}`} key={module.id}>
                <div className="sidebar-module-row" ref={moduleActive ? activeModuleRef : null}>
                  <button
                    aria-current={moduleActive ? 'location' : undefined}
                    className="sidebar-module-link"
                    onClick={() => go('module', module.id)}
                    title={`Módulo ${module.id}: ${module.title}`}
                    type="button"
                  >
                    <span className="module-index">{module.id}</span>
                    <span className="sidebar-module-name">
                      <strong>{module.title}</strong>
                      <small>{track?.title || 'Formação'}</small>
                    </span>
                    <small aria-label={`${moduleProgress.completed} de ${moduleProgress.total} conteúdos concluídos`} className="sidebar-module-progress">
                      {moduleProgress.completed}/{moduleProgress.total}
                    </small>
                  </button>
                  <button
                    aria-controls={`sidebar-module-${module.id}`}
                    aria-expanded={moduleOpen}
                    aria-label={`${moduleOpen ? 'Recolher' : 'Abrir'} conteúdos do módulo ${module.id}`}
                    className="sidebar-module-expand"
                    onClick={() => toggle(setOpenModules, module.id)}
                    type="button"
                  >
                    <Icon name={moduleOpen ? 'chevronDown' : 'chevronRight'} size={14} />
                  </button>
                </div>
                {moduleOpen ? (
                  <div className="tree-documents" id={`sidebar-module-${module.id}`}>
                    {formationDocuments.map((document) => {
                      const complete = isDocumentCompleted(progress, document.id)
                      const active = route.view === 'learn' && route.id === document.id
                      return (
                        <button
                          aria-current={active ? 'page' : undefined}
                          className={active ? 'is-active' : ''}
                          key={document.id}
                          onClick={() => go('learn', document.id)}
                          ref={active ? activeDocumentRef : null}
                          title={document.title}
                          type="button"
                        >
                          <span className={`document-state${complete ? ' is-complete' : ''}`}>
                            {complete ? <Icon name="check" size={11} /> : null}
                          </span>
                          <span>{document.title}</span>
                          {document.type === 'lab' ? <Icon name="flask" size={13} /> : null}
                        </button>
                      )
                    })}
                  </div>
                ) : null}
              </section>
            )
          })}
        </nav>

        <div className="sidebar-footer">
          <span className="local-indicator"><i /> Dados salvos neste navegador</span>
          <small>Sem conta · sem sincronização externa</small>
        </div>
      </aside>
    </>
  )
}
