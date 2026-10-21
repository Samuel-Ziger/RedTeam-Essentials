import React, { useEffect, useMemo, useState } from 'react'

import { isFormationItem, itemContext } from '../lib/catalog.js'
import {
  completionBreakdown,
  firstAvailableDocument,
  isDocumentCompleted,
  isLearningItemCompleted,
  isRequirementCompleted,
  labAvailability,
  moduleAvailability,
  nextRecommended,
  recentlyCompleted,
} from '../lib/progress.js'
import { Icon } from './Icons.jsx'
import { MarkdownReader } from './MarkdownReader.jsx'
import { MetaDot, ProgressBar, ProgressRing } from './ProgressUI.jsx'

function formatDuration(minutes) {
  const value = Number(minutes) || 0
  if (value < 60) return `${value} min`
  const hours = Math.floor(value / 60)
  const remainder = value % 60
  return remainder ? `${hours}h ${remainder}min` : `${hours}h`
}

function formatHourRange(value) {
  const min = Math.max(0, Number(value?.min) || 0)
  const max = Math.max(min, Number(value?.max) || min)
  return min === max ? `${min} h` : `${min}–${max} h`
}

function sumEstimatedHours(modules) {
  return (modules || []).reduce((total, module) => ({
    min: total.min + (Number(module?.estimatedHours?.min) || 0),
    max: total.max + (Number(module?.estimatedHours?.max) || 0),
  }), { min: 0, max: 0 })
}

function formatDate(value) {
  if (!value) return ''
  try {
    return new Intl.DateTimeFormat('pt-BR', { day: '2-digit', month: 'short' }).format(new Date(value))
  } catch {
    return ''
  }
}

function moduleForDocument(catalog, document) {
  const moduleId = String(document?.moduleId || document?.module || '')
  return catalog?.modules?.find((module) => String(module.id) === moduleId) || null
}

function documentAvailability(document, catalog, progress) {
  if (!document) return { unlocked: false, missing: [], missingModuleIds: [] }
  const module = moduleForDocument(catalog, document)
  const moduleState = module
    ? moduleAvailability(module, catalog, progress)
    : { unlocked: true, missingModuleIds: [] }
  if (document.type === 'lab') {
    const labState = labAvailability(document, progress, catalog)
    return { ...labState, module, moduleState }
  }
  const missing = (document.prerequisites || []).filter((id) =>
    !isRequirementCompleted(progress, id, catalog),
  )
  return {
    unlocked: moduleState.unlocked && missing.length === 0,
    missing,
    missingModuleIds: moduleState.missingModuleIds,
    module,
    moduleState,
  }
}

function formationStats(documents) {
  const formation = documents.filter(isFormationItem)
  return {
    documents: formation.length,
    labs: formation.filter((document) => document.type === 'lab').length,
    readingMinutes: formation.reduce((total, document) => total + document.readingMinutes, 0),
  }
}

function EmptyPanel({ icon = 'book', title, children, action }) {
  return (
    <div className="empty-panel">
      <span><Icon name={icon} size={28} /></span>
      <h2>{title}</h2>
      <p>{children}</p>
      {action}
    </div>
  )
}

function LockedModule({ catalog, module, navigate, state }) {
  const pending = state.missingModuleIds
    .map((moduleId) => catalog.modules.find((candidate) => candidate.id === moduleId))
    .filter(Boolean)
  const visible = pending.slice(0, 8)
  const hiddenCount = Math.max(0, pending.length - visible.length)
  return (
    <section className="module-gate" role="status">
      <span className="module-gate-icon"><Icon name="lock" size={30} /></span>
      <span className="eyebrow">MÓDULO BLOQUEADO</span>
      <h2>Conclua a base curricular antes de avançar</h2>
      <p>
        O módulo {module.id} depende da conclusão de {state.totalPrerequisiteModules}
        {' '}módulo{state.totalPrerequisiteModules === 1 ? '' : 's'}. Ainda há {pending.length} pendente{pending.length === 1 ? '' : 's'}.
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

export function DashboardView({ catalog, progress, navigate }) {
  const [moduleFilter, setModuleFilter] = useState('all')
  const progressBreakdown = completionBreakdown(catalog.documents, progress)
  const overall = progressBreakdown.required
  const lastDocumentCandidate = progress.lastDocument
    ? catalog.documents.find((document) => document.id === progress.lastDocument.id)
    : null
  const lastDocument = lastDocumentCandidate
    && documentAvailability(lastDocumentCandidate, catalog, progress).unlocked
    ? lastDocumentCandidate
    : null
  const recommendation = nextRecommended(catalog, progress)
  const continueFromLast = lastDocument && !isLearningItemCompleted(progress, lastDocument)
  const continueDocument = continueFromLast ? lastDocument : recommendation
  const recent = recentlyCompleted(catalog, progress, 4)
  const formationTracks = catalog.tracks.filter((track) => track.documents.some(isFormationItem))
  const formationModules = catalog.modules
    .filter((module) => /^\d{2}$/.test(module.id) && module.documents.some(isFormationItem))
    .sort((first, second) => Number(first.id) - Number(second.id))
  const firstModuleId = formationModules[0]?.id || '00'
  const lastModuleId = formationModules.at(-1)?.id || firstModuleId
  const journeyRange = `${firstModuleId}–${lastModuleId}`
  const trackByModuleId = new Map(formationTracks.flatMap((track) =>
    track.modules.map((module) => [module.id, track]),
  ))
  const visibleModules = moduleFilter === 'all'
    ? formationModules
    : formationModules.filter((module) => trackByModuleId.get(module.id)?.id === moduleFilter)
  const currentModuleId = formationModules.find((module) => (
    moduleAvailability(module, catalog, progress).unlocked
    && completionBreakdown(module.documents, progress).required.remaining > 0
  ))?.id
  const availableLabs = catalog.labs
    .filter(isFormationItem)
    .filter((lab) => labAvailability(lab, progress, catalog).unlocked && !labAvailability(lab, progress, catalog).completed)
    .slice(0, 4)
  const completeFormation = formationStats(catalog.documents)
  const completeWorkload = sumEstimatedHours(formationModules)

  return (
    <div className="page page--dashboard">
      <section className="dashboard-hero">
        <div className="hero-copy">
          <span className="eyebrow"><i /> JORNADA {journeyRange} · AMBIENTE LOCAL</span>
          <h1>Avance módulo a módulo.<br /><span>Construa na prática.</span></h1>
          <p>
            Uma sequência única do módulo {firstModuleId} ao {lastModuleId}, com progresso, leituras e
            laboratórios conectados. A base 00–26 libera a especialização 27–40; as áreas
            temáticas continuam disponíveis como filtros.
          </p>
          <div className="hero-actions">
            {continueDocument ? (
              <button className="button button--primary" onClick={() => navigate('learn', continueDocument.id)} type="button">
                <Icon name="arrowRight" size={17} />
                {continueFromLast ? 'Continuar de onde parei' : 'Começar a estudar'}
              </button>
            ) : null}
            <button className="button button--ghost" onClick={() => navigate('progress')} type="button">
              Ver meu progresso
            </button>
            <button className="button button--ghost" onClick={() => navigate('library', 'formation')} type="button">
              <Icon name="layers" size={16} /> Biblioteca completa
            </button>
          </div>
        </div>
        <div className="hero-progress-card">
          <ProgressRing size="medium" value={overall.percent} />
          <div>
            <span>Seu progresso geral</span>
            <strong>{overall.completed} de {overall.total}</strong>
            <small>conteúdos concluídos</small>
          </div>
        </div>
        <div aria-hidden="true" className="hero-grid" />
      </section>

      <section aria-label="Resumo da formação" className="metric-grid">
        <div><span className="metric-icon"><Icon name="target" /></span><strong>{formationModules.length}</strong><small>módulos em sequência</small></div>
        <div><span className="metric-icon"><Icon name="book" /></span><strong>{overall.total}</strong><small>conteúdos obrigatórios</small></div>
        <div><span className="metric-icon"><Icon name="flask" /></span><strong>{completeFormation.labs}</strong><small>laboratórios da formação</small></div>
        <div><span className="metric-icon"><Icon name="clock" /></span><strong>{formatHourRange(completeWorkload)}</strong><small>de carga completa estimada</small></div>
      </section>

      <section aria-labelledby="module-journey-heading" className="section-block module-journey-section">
        <div className="section-heading">
          <div><span className="eyebrow">JORNADA PRINCIPAL</span><h2 id="module-journey-heading">Módulos {firstModuleId} a {lastModuleId}</h2></div>
          <p>Siga a ordem completa ou use uma área apenas para localizar o assunto que procura.</p>
        </div>

        <div className="journey-filter-row">
          <div aria-label="Filtrar módulos por área" className="journey-filters">
            <button
              aria-pressed={moduleFilter === 'all'}
              onClick={() => setModuleFilter('all')}
              type="button"
            >
              Todos <span>{formationModules.length}</span>
            </button>
            {formationTracks.map((track) => (
              <button
                aria-pressed={moduleFilter === track.id}
                key={track.id}
                onClick={() => setModuleFilter(track.id)}
                type="button"
              >
                {track.title} <span>{track.modules.filter((module) => /^\d{2}$/.test(module.id)).length}</span>
              </button>
            ))}
          </div>
          {moduleFilter !== 'all' ? (
            <button className="text-button journey-area-link" onClick={() => navigate('track', moduleFilter)} type="button">
              Abrir visão da área <Icon name="arrowRight" size={15} />
            </button>
          ) : null}
        </div>

        <p aria-live="polite" className="journey-result-count">
          Exibindo <strong>{visibleModules.length}</strong> de {formationModules.length} módulos na ordem curricular.
        </p>

        <ol className="module-journey-list" start={Number(visibleModules[0]?.id || 0) + 1}>
          {visibleModules.map((module) => {
            const current = completionBreakdown(module.documents, progress).required
            const gate = moduleAvailability(module, catalog, progress)
            const start = firstAvailableDocument(module.documents, catalog, progress)
            const stats = formationStats(module.documents)
            const track = trackByModuleId.get(module.id)
            const completed = current.total > 0 && current.remaining === 0
            const currentModule = module.id === currentModuleId
            const status = !gate.unlocked
              ? 'Bloqueado'
              : completed
              ? 'Conteúdos concluídos'
              : current.completed
                ? 'Em andamento'
                : currentModule
                  ? 'Comece aqui'
                  : 'Na sequência'
            return (
              <li aria-current={currentModule ? 'step' : undefined} className={`module-journey-item${completed ? ' is-complete' : ''}${currentModule ? ' is-current' : ''}${gate.unlocked ? '' : ' is-locked'}`} key={module.id}>
                <span aria-hidden="true" className="module-journey-marker">
                  <strong>{module.id}</strong><i />
                </span>
                <article className="module-journey-card">
                  <header>
                    <div>
                      <small>Módulo {module.id}{track ? ` · ${track.title}` : ''}</small>
                      <h3>{module.title}</h3>
                    </div>
                    <span className="module-journey-status">{status}</span>
                  </header>
                  <p>{module.description || `${stats.documents} materiais organizados para estudo.`}</p>
                  <div className="module-journey-meta">
                    <span><Icon name="book" size={14} /> {stats.documents} conteúdos</span>
                    <span><Icon name="flask" size={14} /> {stats.labs} lab{stats.labs === 1 ? '' : 's'}</span>
                    <span><Icon name="clock" size={14} /> {formatDuration(stats.readingMinutes)} de leitura</span>
                    <span><Icon name="target" size={14} /> {formatHourRange(module.estimatedHours)} de carga</span>
                    {!gate.unlocked ? <span><Icon name="lock" size={14} /> {gate.missingModuleIds.length} módulos pendentes</span> : null}
                  </div>
                  <div className="module-journey-progress">
                    <span>{current.completed} de {current.total} obrigatórios</span>
                    <strong>{current.percent}%</strong>
                  </div>
                  <ProgressBar label={`Progresso no módulo ${module.id}: ${module.title}`} value={current.percent} />
                  <div className="module-journey-actions">
                    <button className="button button--secondary" onClick={() => navigate('module', module.id)} type="button">
                      <Icon name={gate.unlocked ? 'folder' : 'lock'} size={15} /> {gate.unlocked ? 'Ver módulo' : 'Ver requisitos'}
                    </button>
                    {start ? (
                      <button className="text-button" onClick={() => navigate('learn', start.id)} type="button">
                        {completed ? 'Revisar' : current.completed ? 'Continuar' : 'Começar'} <Icon name="arrowRight" size={15} />
                      </button>
                    ) : null}
                  </div>
                </article>
              </li>
            )
          })}
        </ol>
      </section>

      <div className="dashboard-columns">
        <section className="panel">
          <div className="panel-heading"><div><span className="eyebrow">RETOME RAPIDAMENTE</span><h2>Atividade recente</h2></div></div>
          {lastDocument || recent.length ? (
            <div className="activity-list">
              {lastDocument ? (
                <button className="continue-row" onClick={() => navigate('learn', lastDocument.id)} type="button">
                  <span className="activity-icon"><Icon name="book" /></span>
                  <span><small>Última leitura</small><strong>{lastDocument.title}</strong><em>{lastDocument.typeLabel} · {lastDocument.readingMinutes} min de leitura</em></span>
                  <Icon name="arrowRight" size={18} />
                </button>
              ) : null}
              {recent.map(({ document, completedAt, completionType }) => (
                <button className="activity-row" key={document.id} onClick={() => navigate('learn', document.id)} type="button">
                  <span className="activity-check"><Icon name="check" size={14} /></span>
                  <span><strong>{document.title}</strong><small>{completionType === 'lab' ? 'Lab concluído' : 'Leitura concluída'} em {formatDate(completedAt)}</small></span>
                  <Icon name="chevronRight" size={16} />
                </button>
              ))}
            </div>
          ) : (
            <EmptyPanel title="Sua jornada começa aqui">Abra o primeiro conteúdo para registrar sua atividade.</EmptyPanel>
          )}
        </section>

        <section className="panel">
          <div className="panel-heading">
            <div><span className="eyebrow">HORA DE PRATICAR</span><h2>Labs disponíveis</h2></div>
            <button className="text-button" onClick={() => navigate('labs')} type="button">Ver todos</button>
          </div>
          {availableLabs.length ? (
            <div className="compact-lab-list">
              {availableLabs.map((lab) => (
                <button key={lab.id} onClick={() => navigate('learn', lab.id)} type="button">
                  <span><Icon name="flask" /></span>
                  <span><strong>{lab.title}</strong><small>{lab.readingMinutes} min de leitura do enunciado · Pronto para iniciar</small></span>
                  <Icon name="arrowRight" size={16} />
                </button>
              ))}
            </div>
          ) : (
            <EmptyPanel icon="lock" title="Continue estudando">Novos laboratórios aparecem quando seus capítulos obrigatórios forem concluídos.</EmptyPanel>
          )}
        </section>
      </div>
    </div>
  )
}

export function TrackView({ catalog, track, progress, navigate }) {
  const current = completionBreakdown(track.documents, progress).required
  const start = firstAvailableDocument(track.documents, catalog, progress)
  const trackFormation = formationStats(track.documents)
  return (
    <div className="page">
      <section className="track-hero">
        <div>
          <span className="eyebrow">ÁREA DA FORMAÇÃO</span>
          <h1>{track.title}</h1>
          <p>{track.description || 'Explore os módulos relacionados a esta área da formação.'}</p>
          {start ? (
            <button className="button button--primary" onClick={() => navigate('learn', start.id)} type="button">
              <Icon name="arrowRight" size={17} /> {current.completed ? 'Continuar nesta área' : 'Explorar esta área'}
            </button>
          ) : null}
        </div>
        <div className="track-hero-stats">
          <ProgressRing size="medium" value={current.percent} />
          <dl>
            <div><dt>{track.stats.modules === 1 ? 'Módulo' : 'Módulos'}</dt><dd>{track.stats.modules}</dd></div>
            <div><dt>Conteúdos</dt><dd>{trackFormation.documents}</dd></div>
            <div><dt>Laboratórios</dt><dd>{trackFormation.labs}</dd></div>
            <div><dt>Carga completa estimada</dt><dd>{formatHourRange(track.stats.estimatedHours)}</dd></div>
          </dl>
        </div>
      </section>

      <section className="section-block">
        <div className="section-heading"><div><span className="eyebrow">CURRÍCULO</span><h2>Módulos desta área</h2></div></div>
        <div className="module-list">
          {track.modules.map((module, index) => {
            const moduleProgress = completionBreakdown(module.documents, progress).required
            const gate = moduleAvailability(module, catalog, progress)
            const next = firstAvailableDocument(module.documents, catalog, progress)
            const moduleFormation = formationStats(module.documents)
            return (
              <article className={`module-card${gate.unlocked ? '' : ' is-locked'}`} key={module.id}>
                <span className="module-card-index">{module.id || String(index + 1).padStart(2, '0')}</span>
                <div className="module-card-main">
                  <div className="module-card-heading">
                  <div><small>Módulo {module.id || String(index + 1).padStart(2, '0')}</small><h3>{module.title}</h3></div>
                    <strong>{moduleProgress.percent}%</strong>
                  </div>
                  <p>{module.description || `${module.documents.length} materiais para estudar.`}</p>
                  <ProgressBar label={`Progresso em ${module.title}`} value={moduleProgress.percent} />
                  <div className="module-card-footer">
                    <span>{moduleProgress.completed}/{moduleProgress.total} conteúdos concluídos</span>
                    <span>{moduleFormation.documents} itens · {moduleFormation.labs} lab{moduleFormation.labs === 1 ? '' : 's'}</span>
                    <span>{formatHourRange(module.estimatedHours)} de carga estimada</span>
                    {!gate.unlocked ? <span><Icon name="lock" size={14} /> {gate.missingModuleIds.length} módulos pendentes</span> : null}
                    <button className="text-button" onClick={() => navigate('module', module.id)} type="button">
                      {gate.unlocked ? 'Ver tudo' : 'Ver requisitos'} <Icon name={gate.unlocked ? 'folder' : 'lock'} size={15} />
                    </button>
                    {next ? (
                      <button className="text-button" onClick={() => navigate('learn', next.id)} type="button">
                        {moduleProgress.completed ? 'Continuar' : 'Começar'} <Icon name="arrowRight" size={15} />
                      </button>
                    ) : null}
                  </div>
                </div>
              </article>
            )
          })}
        </div>
      </section>
    </div>
  )
}

export function LabsView({ catalog, progress, markDocument, markLab, navigate }) {
  const [filter, setFilter] = useState('all')
  const labs = useMemo(() => catalog.labs.map((lab) => ({
    lab,
    state: labAvailability(lab, progress, catalog),
    module: catalog.modules.find((module) => module.id === lab.moduleId),
  })), [catalog, progress])
  const counts = {
    all: labs.length,
    available: labs.filter(({ state }) => state.unlocked && !state.completed).length,
    locked: labs.filter(({ state }) => !state.unlocked).length,
    completed: labs.filter(({ state }) => state.completed).length,
  }
  const visible = labs.filter(({ state }) => {
    if (filter === 'available') return state.unlocked && !state.completed
    if (filter === 'locked') return !state.unlocked
    if (filter === 'completed') return state.completed
    return true
  })

  return (
    <div className="page">
      <header className="page-heading">
        <span className="eyebrow">PRÁTICA GUIADA</span>
        <h1>Laboratórios</h1>
        <p>Pratique quando a base necessária estiver concluída. Tudo permanece no seu ambiente local.</p>
      </header>
      <div aria-label="Filtrar laboratórios" className="filter-tabs" role="tablist">
        {[
          ['all', 'Todos'],
          ['available', 'Disponíveis'],
          ['locked', 'Bloqueados'],
          ['completed', 'Concluídos'],
        ].map(([id, label]) => (
          <button aria-selected={filter === id} key={id} onClick={() => setFilter(id)} role="tab" type="button">
            {label} <span>{counts[id]}</span>
          </button>
        ))}
      </div>
      {visible.length ? (
        <div className="labs-grid">
          {visible.map(({ lab, state, module }) => (
            <article className={`lab-card${state.unlocked ? '' : ' is-locked'}${state.completed ? ' is-completed' : ''}`} key={lab.id}>
              <div className="lab-card-icon"><Icon name={state.completed ? 'check' : state.unlocked ? 'unlock' : 'lock'} /></div>
              <div className="lab-card-status">
                {state.completed ? 'Concluído' : state.unlocked ? 'Disponível' : 'Bloqueado'}
              </div>
              <small>{module?.title || 'Laboratório'}</small>
              <h2>{lab.title}</h2>
              <p>{lab.description || 'Exercício prático acompanhado pelo material do curso.'}</p>
              <div className="lab-prerequisite-row">
                <span>{state.completedRequirements}/{state.totalRequirements} pré-requisitos</span>
                <span>{lab.readingMinutes} min de leitura do enunciado</span>
              </div>
              <ProgressBar
                label={`Pré-requisitos de ${lab.title}`}
                value={state.totalRequirements ? (state.completedRequirements / state.totalRequirements) * 100 : 100}
              />
              <div className="lab-card-actions">
                {state.unlocked ? (
                  <button className="button button--secondary" onClick={() => navigate('learn', lab.id)} type="button">
                    <Icon name="flask" size={16} /> {state.completed ? 'Revisar lab' : 'Iniciar lab'}
                  </button>
                ) : (
                  <button className="button button--muted" disabled type="button"><Icon name="lock" size={15} /> Continue estudando</button>
                )}
                {state.unlocked ? (
                  <button
                    aria-label={state.completed ? `Desmarcar ${lab.title}` : `Concluir ${lab.title}`}
                    className="icon-button"
                    onClick={() => {
                      const target = !state.completed
                      markLab(lab.id, target)
                      if (target) markDocument(lab.id, true)
                    }}
                    title={state.completed ? 'Desmarcar conclusão' : 'Marcar como concluído'}
                    type="button"
                  ><Icon name="check" /></button>
                ) : null}
              </div>
            </article>
          ))}
        </div>
      ) : (
        <EmptyPanel icon="flask" title="Nenhum laboratório neste filtro">Altere o filtro ou continue estudando para liberar novas práticas.</EmptyPanel>
      )}
    </div>
  )
}

export function ProgressView({ catalog, progress, onReset, navigate }) {
  const breakdown = completionBreakdown(catalog.documents, progress)
  const overall = breakdown.required
  const recent = recentlyCompleted(catalog, progress, 8)
  const completedLabs = catalog.labs.filter((lab) => isFormationItem(lab) && labAvailability(lab, progress, catalog).completed).length
  const formationTracks = catalog.tracks.filter((track) => track.documents.some(isFormationItem))
  const formationModules = catalog.modules.filter((module) => module.documents.some(isFormationItem))

  function reset() {
    if (window.confirm('Apagar todo o progresso salvo neste navegador? Esta ação não pode ser desfeita.')) onReset()
  }

  return (
    <div className="page">
      <header className="page-heading page-heading--row">
        <div><span className="eyebrow">VISÃO GERAL</span><h1>Meu progresso</h1><p>Acompanhe o que já estudou e escolha seu próximo passo.</p></div>
        <button className="button button--danger-ghost" onClick={reset} type="button">Reiniciar progresso</button>
      </header>
      <section className="progress-summary">
        <ProgressRing value={overall.percent} />
        <div className="progress-summary-copy">
          <span className="eyebrow">PROGRESSO DOS CONTEÚDOS</span>
          <h2>{overall.completed} conteúdos concluídos</h2>
          <p>{overall.remaining
            ? `Faltam ${overall.remaining} itens obrigatórios registrados no aplicativo.`
            : 'Todos os itens obrigatórios registrados no aplicativo foram concluídos. Confira também as entregas e os checklists de cada módulo.'}</p>
          <div className="summary-stats">
            <div><strong>{overall.total}</strong><span>obrigatórios</span></div>
            <div><strong>{breakdown.optional.completed}/{breakdown.optional.total}</strong><span>opcionais explorados</span></div>
            <div><strong>{completedLabs}</strong><span>labs concluídos</span></div>
          </div>
        </div>
      </section>

      <section className="optional-progress-card">
        <span><Icon name="layers" size={22} /></span>
        <div>
          <strong>Exploração opcional e acervo</strong>
          <p>{breakdown.optional.completed} de {breakdown.optional.total} referências, extras e materiais legados explorados.</p>
          <ProgressBar label="Progresso em materiais opcionais" value={breakdown.optional.percent} />
        </div>
        <strong>{breakdown.optional.percent}%</strong>
        <button className="text-button" onClick={() => navigate('library', 'security')} type="button">Explorar biblioteca <Icon name="arrowRight" size={15} /></button>
      </section>

      <section className="section-block">
        <div className="section-heading"><div><span className="eyebrow">POR ÁREA</span><h2>Progresso por assunto</h2></div></div>
        <div className="track-progress-list">
          {formationTracks.map((track, index) => {
            const value = completionBreakdown(track.documents, progress).required
            return (
              <button key={track.id} onClick={() => navigate('track', track.id)} style={{ '--track-index': index % 6 }} type="button">
                <span className="track-progress-number">{String(index + 1).padStart(2, '0')}</span>
                <span className="track-progress-main">
                  <span><strong>{track.title}</strong><small>{value.completed}/{value.total} conteúdos concluídos</small></span>
                  <ProgressBar label={`Progresso em ${track.title}`} value={value.percent} />
                </span>
                <strong>{value.percent}%</strong>
                <Icon name="chevronRight" size={17} />
              </button>
            )
          })}
        </div>
      </section>

      <div className="dashboard-columns progress-columns">
        <section className="panel">
          <div className="panel-heading"><div><span className="eyebrow">DETALHAMENTO</span><h2>Por módulo</h2></div></div>
          <div className="module-progress-grid">
            {formationModules.map((module) => {
              const value = completionBreakdown(module.documents, progress).required
              const gate = moduleAvailability(module, catalog, progress)
              const next = firstAvailableDocument(module.documents, catalog, progress)
              return (
                <button className={gate.unlocked ? '' : 'is-locked'} key={module.id} onClick={() => gate.unlocked && next ? navigate('learn', next.id) : navigate('module', module.id)} type="button">
                  <span>{module.id}</span><span><strong>{module.title}</strong><ProgressBar compact value={value.percent} /></span><em>{gate.unlocked ? `${value.percent}%` : <Icon name="lock" size={15} />}</em>
                </button>
              )
            })}
          </div>
        </section>
        <section className="panel">
          <div className="panel-heading"><div><span className="eyebrow">HISTÓRICO</span><h2>Conclusões recentes</h2></div></div>
          {recent.length ? (
            <div className="activity-list">
              {recent.map(({ document, completedAt, completionType }) => (
                <button className="activity-row" key={document.id} onClick={() => navigate('learn', document.id)} type="button">
                  <span className="activity-check"><Icon name="check" size={14} /></span>
                  <span><strong>{document.title}</strong><small>{formatDate(completedAt)} · {completionType === 'lab' ? 'Laboratório executado' : document.typeLabel}</small></span>
                  <Icon name="chevronRight" size={16} />
                </button>
              ))}
            </div>
          ) : <EmptyPanel title="Nenhuma conclusão ainda">Marque um conteúdo como lido e ele aparecerá aqui.</EmptyPanel>}
        </section>
      </div>
    </div>
  )
}

function LockedLab({ catalog, document, state, navigate }) {
  const missingDocuments = state.missing
    .map((id) => catalog.documents.find((item) => item.id === id))
    .filter(Boolean)
  const missingModules = state.missingModuleIds
    .map((id) => catalog.modules.find((item) => item.id === id))
    .filter(Boolean)
  const visibleModules = missingModules.slice(0, 8)
  const visibleDocuments = missingDocuments.slice(0, 8)
  const firstMissingModule = missingModules[0]
  return (
    <div className="locked-lab">
      <span><Icon name="lock" size={32} /></span>
      <span className="eyebrow">LABORATÓRIO BLOQUEADO</span>
      <h2>Prepare a base antes da prática</h2>
      <p>Conclua os módulos e leituras obrigatórias pendentes. O laboratório será liberado automaticamente.</p>
      {visibleModules.length ? (
        <div className="locked-requirements locked-requirements--modules">
          {visibleModules.map((required) => (
            <button key={required.id} onClick={() => navigate('module', required.id)} type="button">
              <span>{required.id}</span><strong>{required.title}</strong><Icon name="arrowRight" size={16} />
            </button>
          ))}
        </div>
      ) : null}
      <div className="locked-requirements">
        {visibleDocuments.map((required) => (
          <button key={required.id} onClick={() => navigate('learn', required.id)} type="button">
            <span><Icon name="book" size={16} /></span><strong>{required.title}</strong><Icon name="arrowRight" size={16} />
          </button>
        ))}
      </div>
      {missingModules.length > visibleModules.length || missingDocuments.length > visibleDocuments.length ? (
        <small className="module-gate-more">Outros requisitos permanecem resumidos para manter a navegação objetiva.</small>
      ) : null}
      {firstMissingModule || missingDocuments[0] ? (
        <button className="button button--primary" onClick={() => firstMissingModule ? navigate('module', firstMissingModule.id) : navigate('learn', missingDocuments[0].id)} type="button">
          {firstMissingModule ? `Continuar pelo módulo ${firstMissingModule.id}` : 'Estudar primeiro requisito'} <Icon name="arrowRight" size={16} />
        </button>
      ) : null}
    </div>
  )
}

export function ReaderView({ catalog, context, progress, markDocument, markLab, navigate, onContentReady }) {
  const { document, module, track, previous, next } = context
  const completed = isDocumentCompleted(progress, document.id)
  const moduleState = module
    ? moduleAvailability(module, catalog, progress)
    : { unlocked: true, missingModuleIds: [], totalPrerequisiteModules: 0 }
  const moduleLocked = Boolean(module && isFormationItem(document) && !moduleState.unlocked)
  const labState = document.type === 'lab' ? labAvailability(document, progress, catalog) : null
  const nextLocked = Boolean(next && !documentAvailability(next, catalog, progress).unlocked)
  const relatedResources = (document.resourceIds || [])
    .map((id) => catalog.resources.find((resource) => resource.id === id))
    .filter((resource) => resource && !resource.aliasOfDocumentId)
  const location = itemContext(catalog, document)
  const legacyCollection = location.legacySection
  const labLocked = Boolean(labState && !labState.unlocked)
  const contentLocked = moduleLocked || labLocked

  useEffect(() => {
    if (!contentLocked || !onContentReady) return undefined
    const frame = requestAnimationFrame(() => onContentReady(document.id))
    return () => cancelAnimationFrame(frame)
  }, [contentLocked, document.id, onContentReady])

  function toggleLab() {
    if (contentLocked || !labState) return
    const target = !labState.completed
    markLab(document.id, target)
    if (target) markDocument(document.id, true)
  }

  return (
    <div className="reader-page">
      <div className="reader-toolbar">
        <div className="breadcrumbs">
          <button onClick={() => navigate(legacyCollection ? 'library' : 'dashboard', legacyCollection ? 'security' : undefined)} type="button">{legacyCollection ? 'Biblioteca' : 'Início'}</button><Icon name="chevronRight" size={13} />
          {legacyCollection ? <><button onClick={() => navigate('collection', legacyCollection.id)} type="button">{legacyCollection.title}</button><Icon name="chevronRight" size={13} /></> : track ? <><button onClick={() => navigate('track', track.id)} type="button">{track.title}</button><Icon name="chevronRight" size={13} /></> : null}
          <span>{legacyCollection && module ? `Pasta ${module.id}` : module?.title || location.primaryTitle}</span>
        </div>
        <button
          aria-pressed={completed}
          className={`read-toggle${completed ? ' is-complete' : ''}${contentLocked ? ' is-locked' : ''}`}
          disabled={contentLocked}
          onClick={() => !contentLocked && markDocument(document.id, !completed)}
          type="button"
        >
          <span><Icon name={contentLocked ? 'lock' : 'check'} size={14} /></span>{contentLocked ? 'Bloqueado' : completed ? 'Lido' : 'Marcar como lido'}
        </button>
      </div>

      <div className="reader-container">
        <header className="reader-heading">
          <span className={`content-type content-type--${document.type}`}>{document.typeLabel}</span>
          <h1>{document.title}</h1>
          {document.description ? <p>{document.description}</p> : null}
          <div className="reader-meta">
            <span><Icon name="clock" size={15} /> {document.readingMinutes} min de leitura</span>
            <MetaDot />
            <span>{document.words.toLocaleString('pt-BR')} palavras</span>
            {location.primary ? <><MetaDot /><span>{location.primaryTitle}</span></> : null}
            {legacyCollection && module ? <><MetaDot /><span>Pasta física: módulo {module.id}</span></> : null}
          </div>
        </header>

        {moduleLocked ? (
          <LockedModule catalog={catalog} module={module} navigate={navigate} state={moduleState} />
        ) : labLocked ? (
          <LockedLab catalog={catalog} document={document} navigate={navigate} state={labState} />
        ) : (
          <>
            {document.type === 'lab' ? (
              <div className="lab-ready-banner">
                <span><Icon name="unlock" /></span>
                <div><strong>Laboratório liberado</strong><p>Você concluiu os conhecimentos necessários. Trabalhe somente no ambiente autorizado descrito no material.</p></div>
              </div>
            ) : null}
            <MarkdownReader
              catalog={catalog}
              document={document}
              onOpenItem={(target) => navigate(target.itemType === 'resource' ? 'resource' : 'learn', target.id)}
              onReady={onContentReady}
            />
            {relatedResources.length ? (
              <section className="related-materials">
                <span className="eyebrow">ARQUIVOS DESTE CONTEÚDO</span>
                <h2>Código, configurações e dados</h2>
                <div>{relatedResources.map((resource) => (
                  <button key={resource.id} onClick={() => navigate('resource', resource.id)} type="button">
                    <Icon name={resource.kind === 'code' ? 'code' : resource.kind === 'image' ? 'image' : 'file'} size={17} />
                    <span><strong>{resource.title}</strong><small>{resource.kindLabel} · {resource.language || resource.kind}</small></span>
                    <Icon name="arrowRight" size={16} />
                  </button>
                ))}</div>
              </section>
            ) : null}
            <section className="reader-completion">
              <span><Icon name={completed ? 'check' : 'sparkles'} size={23} /></span>
              <div>
                <strong>{document.type === 'lab'
                  ? completed ? 'Enunciado lido' : 'Terminou de ler o enunciado?'
                  : completed ? 'Conteúdo concluído' : 'Terminou esta leitura?'}</strong>
                <p>{document.type === 'lab'
                  ? completed
                    ? 'A leitura foi salva. O lab só conta como concluído depois do checkpoint prático abaixo.'
                    : 'Registre a leitura sem confundi-la com a execução do laboratório.'
                  : completed
                    ? 'Seu progresso foi salvo neste navegador.'
                    : 'Marque como lido para atualizar a trilha e liberar atividades.'}</p>
              </div>
              <button className={`button ${completed ? 'button--secondary' : 'button--primary'}`} onClick={() => markDocument(document.id, !completed)} type="button">
                <Icon name="check" size={16} /> {document.type === 'lab'
                  ? completed ? 'Desmarcar leitura' : 'Marcar enunciado como lido'
                  : completed ? 'Desmarcar' : 'Marcar como lido'}
              </button>
            </section>
            {labState ? (
              <section className="lab-finish-card">
                <div><span className="eyebrow">CHECKPOINT PRÁTICO</span><h2>{labState.completed ? 'Laboratório concluído' : 'Concluiu o laboratório?'}</h2><p>Registre a conclusão somente depois de executar e revisar os resultados.</p></div>
                <button className="button button--secondary" onClick={toggleLab} type="button"><Icon name="flask" size={16} /> {labState.completed ? 'Desmarcar lab' : 'Concluir laboratório'}</button>
              </section>
            ) : null}
          </>
        )}

        <nav aria-label="Navegação entre conteúdos" className="reader-pagination">
          {previous ? (
            <button onClick={() => navigate('learn', previous.id)} type="button">
              <Icon name="arrowLeft" /><span><small>Anterior</small><strong>{previous.title}</strong></span>
            </button>
          ) : <span />}
          {next ? (
            <button disabled={nextLocked} onClick={() => !nextLocked && navigate('learn', next.id)} type="button">
              <span><small>{nextLocked ? 'Conclua os requisitos' : 'Próximo'}</small><strong>{next.title}</strong></span><Icon name={nextLocked ? 'lock' : 'arrowRight'} />
            </button>
          ) : <span />}
        </nav>
        <div className="source-path">Fonte local: <code>{document.sourcePath}</code></div>
      </div>
    </div>
  )
}

export function NotFoundView({ navigate }) {
  return (
    <div className="page page--centered">
      <EmptyPanel
        action={<button className="button button--primary" onClick={() => navigate('dashboard')} type="button">Voltar ao painel</button>}
        icon="search"
        title="Conteúdo não encontrado"
      >
        O endereço pode ter mudado quando o catálogo foi atualizado.
      </EmptyPanel>
    </div>
  )
}
