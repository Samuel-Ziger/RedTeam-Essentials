import React, { useCallback, useEffect, useMemo, useRef, useState } from 'react'

import { Icon } from './components/Icons.jsx'
import { SearchPalette } from './components/SearchPalette.jsx'
import { Sidebar } from './components/Sidebar.jsx'
import { CollectionView, LibraryView, ModuleView } from './components/LibraryViews.jsx'
import { ResourceViewer } from './components/ResourceViewer.jsx'
import {
  DashboardView,
  LabsView,
  NotFoundView,
  ProgressView,
  ReaderView,
  TrackView,
} from './components/Views.jsx'
import { useCatalog } from './hooks/useCatalog.js'
import { useHashRoute } from './hooks/useHashRoute.js'
import { useProgress } from './hooks/useProgress.js'
import { collectionContext, documentContext } from './lib/catalog.js'
import { completionBreakdown, THEME_STORAGE_KEY } from './lib/progress.js'

function initialTheme() {
  try {
    const stored = window.localStorage.getItem(THEME_STORAGE_KEY)
    if (stored === 'light' || stored === 'dark') return stored
  } catch {
    // O tema continua funcional mesmo quando o navegador bloqueia o storage.
  }
  return window.matchMedia?.('(prefers-color-scheme: light)').matches ? 'light' : 'dark'
}

function LoadingScreen() {
  return (
    <div className="boot-screen" role="status">
      <div className="boot-logo"><Icon name="shield" size={30} /></div>
      <strong>Preparando seu ambiente de estudos</strong>
      <p>Organizando trilhas, materiais e laboratórios locais...</p>
      <span className="boot-loader"><i /><i /><i /></span>
    </div>
  )
}

function CatalogError({ error, retry }) {
  return (
    <div className="boot-screen boot-screen--error" role="alert">
      <div className="boot-logo"><Icon name="book" size={30} /></div>
      <strong>Não foi possível abrir a biblioteca</strong>
      <p>{error?.message || 'O catálogo local não foi encontrado.'}</p>
      <code>/generated/catalog.json</code>
      <button className="button button--primary" onClick={retry} type="button"><Icon name="refresh" size={16} /> Tentar novamente</button>
    </div>
  )
}

function routeTitle(route, catalog) {
  if (route.view === 'library') return 'Biblioteca completa'
  if (route.view === 'labs') return 'Laboratórios'
  if (route.view === 'progress') return 'Meu progresso'
  if (route.view === 'track') return catalog.tracks.find((track) => track.id === route.id)?.title || 'Área'
  if (route.view === 'module') return catalog.modules.find((module) => module.id === route.id)?.title || 'Módulo'
  if (route.view === 'collection') return catalog.groups.find((group) => group.id === route.id)?.title || 'Coleção'
  if (route.view === 'resource') return catalog.resources.find((resource) => resource.id === route.id)?.title || 'Arquivo'
  if (route.view === 'learn') return catalog.documents.find((document) => document.id === route.id)?.title || 'Leitura'
  return 'Painel de estudos'
}

function jumpToScrollPosition(element, top) {
  const previousBehavior = element.style.scrollBehavior
  element.style.scrollBehavior = 'auto'
  element.scrollTop = top
  if (previousBehavior) element.style.scrollBehavior = previousBehavior
  else element.style.removeProperty('scroll-behavior')
}

export default function App() {
  const { status, catalog, error, retry } = useCatalog()
  const { route, navigate, navigationRevision } = useHashRoute()
  const { progress, markDocument, markLab, visit, saveScroll, reset } = useProgress()
  const [theme, setTheme] = useState(initialTheme)
  const [sidebarOpen, setSidebarOpen] = useState(false)
  const [searchOpen, setSearchOpen] = useState(false)
  const scrollRef = useRef(null)
  const scrollTimer = useRef(null)
  const menuButtonRef = useRef(null)
  const activeScrollDocumentRef = useRef(null)
  const latestScrollPositionsRef = useRef(new Map())
  const restoreScrollRef = useRef(null)
  const restoreObserverRef = useRef(null)
  const restoreTimeoutRef = useRef(null)
  const restoreReleaseFrameRef = useRef(null)

  useEffect(() => {
    document.documentElement.dataset.theme = theme
    document.documentElement.style.colorScheme = theme
    try {
      window.localStorage.setItem(THEME_STORAGE_KEY, theme)
    } catch {
      // Navegação privada ou política do navegador pode negar persistência.
    }
    document.querySelector('meta[name="theme-color"]')?.setAttribute('content', theme === 'dark' ? '#09111f' : '#f3f6fb')
  }, [theme])

  useEffect(() => {
    const onKeyDown = (event) => {
      if ((event.ctrlKey || event.metaKey) && event.key.toLowerCase() === 'k') {
        event.preventDefault()
        setSearchOpen((open) => !open)
      }
    }
    window.addEventListener('keydown', onKeyDown)
    return () => window.removeEventListener('keydown', onKeyDown)
  }, [])

  const context = useMemo(() =>
    catalog && route.view === 'learn' && route.id ? documentContext(catalog, route.id) : null,
  [catalog, route.id, route.view])

  useEffect(() => {
    if (!context?.document) return
    visit(context.document, { moduleId: context.module?.id, trackId: context.track?.id })
  }, [context?.document?.id, context?.module?.id, context?.track?.id, visit])

  const clearRestoreWatch = useCallback(() => {
    restoreObserverRef.current?.disconnect()
    restoreObserverRef.current = null
    window.clearTimeout(restoreTimeoutRef.current)
    restoreTimeoutRef.current = null
    cancelAnimationFrame(restoreReleaseFrameRef.current)
    restoreReleaseFrameRef.current = null
  }, [])

  useEffect(() => {
    const element = scrollRef.current
    if (!element) return undefined
    window.clearTimeout(scrollTimer.current)
    clearRestoreWatch()
    const documentId = route.view === 'learn' ? route.id : null
    const remembered = documentId && latestScrollPositionsRef.current.has(documentId)
      ? latestScrollPositionsRef.current.get(documentId)
      : progress.scrollPositions[documentId] || 0
    const position = documentId ? remembered : 0
    if (documentId) latestScrollPositionsRef.current.set(documentId, position)
    activeScrollDocumentRef.current = documentId
    restoreScrollRef.current = documentId && position > 0
      ? { documentId, target: position }
      : null
    const frame = requestAnimationFrame(() => {
      // A troca de rota precisa ser imediata mesmo com rolagem suave no CSS.
      jumpToScrollPosition(element, position)
    })
    return () => {
      cancelAnimationFrame(frame)
      window.clearTimeout(scrollTimer.current)
      clearRestoreWatch()
      if (documentId) {
        const latest = latestScrollPositionsRef.current.get(documentId)
        if (Number.isFinite(latest)) saveScroll(documentId, latest)
      }
      if (activeScrollDocumentRef.current === documentId) activeScrollDocumentRef.current = null
      if (restoreScrollRef.current?.documentId === documentId) restoreScrollRef.current = null
    }
    // Restaura somente quando a rota muda, não a cada gravação de progresso.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [clearRestoreWatch, navigationRevision, route.id, route.view, saveScroll, status])

  const handleScroll = useCallback(() => {
    if (route.view !== 'learn' || !route.id || !scrollRef.current) return
    if (activeScrollDocumentRef.current !== route.id) return
    if (restoreScrollRef.current?.documentId === route.id) return
    window.clearTimeout(scrollTimer.current)
    const position = scrollRef.current.scrollTop
    latestScrollPositionsRef.current.set(route.id, position)
    scrollTimer.current = window.setTimeout(() => saveScroll(route.id, position), 250)
  }, [route.id, route.view, saveScroll])

  const handleReaderContentReady = useCallback((documentId) => {
    const restoration = restoreScrollRef.current
    const element = scrollRef.current
    if (!element || restoration?.documentId !== documentId || activeScrollDocumentRef.current !== documentId) return

    clearRestoreWatch()
    const finish = (position) => {
      latestScrollPositionsRef.current.set(documentId, position)
      restoreObserverRef.current?.disconnect()
      restoreObserverRef.current = null
      window.clearTimeout(restoreTimeoutRef.current)
      restoreTimeoutRef.current = null
      restoreReleaseFrameRef.current = requestAnimationFrame(() => {
        if (restoreScrollRef.current?.documentId === documentId) restoreScrollRef.current = null
        restoreReleaseFrameRef.current = null
      })
    }
    const apply = () => {
      if (restoreScrollRef.current?.documentId !== documentId) return true
      jumpToScrollPosition(element, restoration.target)
      if (Math.abs(element.scrollTop - restoration.target) <= 2) {
        finish(restoration.target)
        return true
      }
      return false
    }

    if (apply()) return
    const reader = element.querySelector('.reader-page')
    if (reader && typeof ResizeObserver !== 'undefined') {
      restoreObserverRef.current = new ResizeObserver(() => apply())
      restoreObserverRef.current.observe(reader)
    }
    restoreTimeoutRef.current = window.setTimeout(() => {
      if (restoreScrollRef.current?.documentId !== documentId) return
      jumpToScrollPosition(element, restoration.target)
      finish(element.scrollTop)
    }, 2000)
  }, [clearRestoreWatch])

  const handleReset = useCallback(() => {
    latestScrollPositionsRef.current.clear()
    reset()
  }, [reset])

  const handleSkipToContent = useCallback((event) => {
    event.preventDefault()
    const element = scrollRef.current
    if (!element) return
    jumpToScrollPosition(element, 0)
    element.focus({ preventScroll: true })
  }, [])

  const closeSidebar = useCallback(() => {
    setSidebarOpen(false)
    if (sidebarOpen) requestAnimationFrame(() => menuButtonRef.current?.focus())
  }, [sidebarOpen])

  useEffect(() => {
    if (!sidebarOpen) return undefined
    const onKeyDown = (event) => {
      if (event.key !== 'Escape') return
      event.preventDefault()
      closeSidebar()
    }
    window.addEventListener('keydown', onKeyDown)
    return () => window.removeEventListener('keydown', onKeyDown)
  }, [closeSidebar, sidebarOpen])

  useEffect(() => () => {
    window.clearTimeout(scrollTimer.current)
    clearRestoreWatch()
  }, [clearRestoreWatch])

  if (status === 'loading') return <LoadingScreen />
  if (status === 'error' || !catalog) return <CatalogError error={error} retry={retry} />

  const overall = completionBreakdown(catalog.documents, progress).required
  const title = routeTitle(route, catalog)

  let view
  if (route.view === 'dashboard') {
    view = <DashboardView catalog={catalog} navigate={navigate} progress={progress} />
  } else if (route.view === 'track') {
    const track = catalog.tracks.find((item) => item.id === route.id)
    view = track ? <TrackView catalog={catalog} navigate={navigate} progress={progress} track={track} /> : <NotFoundView navigate={navigate} />
  } else if (route.view === 'library') {
    view = <LibraryView catalog={catalog} navigate={navigate} progress={progress} sectionId={route.id} />
  } else if (route.view === 'module') {
    const module = catalog.modules.find((item) => item.id === route.id)
    view = module ? <ModuleView catalog={catalog} module={module} navigate={navigate} progress={progress} /> : <NotFoundView navigate={navigate} />
  } else if (route.view === 'collection') {
    const collection = collectionContext(catalog, route.id)
    view = collection ? <CollectionView catalog={catalog} context={collection} navigate={navigate} progress={progress} /> : <NotFoundView navigate={navigate} />
  } else if (route.view === 'resource') {
    const resource = catalog.resources.find((item) => item.id === route.id)
    view = resource ? <ResourceViewer catalog={catalog} navigate={navigate} progress={progress} resource={resource} /> : <NotFoundView navigate={navigate} />
  } else if (route.view === 'labs') {
    view = <LabsView catalog={catalog} markDocument={markDocument} markLab={markLab} navigate={navigate} progress={progress} />
  } else if (route.view === 'progress') {
    view = <ProgressView catalog={catalog} navigate={navigate} onReset={handleReset} progress={progress} />
  } else if (route.view === 'learn' && context) {
    view = (
      <ReaderView
        catalog={catalog}
        context={context}
        markDocument={markDocument}
        markLab={markLab}
        navigate={navigate}
        onContentReady={handleReaderContentReady}
        progress={progress}
      />
    )
  } else {
    view = <NotFoundView navigate={navigate} />
  }

  return (
    <div className="app-shell">
      <a className="skip-link" href="#main-content" onClick={handleSkipToContent}>Pular para o conteúdo</a>
      <Sidebar
        catalog={catalog}
        onClose={closeSidebar}
        open={sidebarOpen}
        navigate={navigate}
        progress={progress}
        route={route}
      />
      <div className="workspace">
        <header className="topbar">
          <button
            aria-expanded={sidebarOpen}
            aria-label="Abrir menu"
            className="icon-button mobile-menu"
            onClick={() => setSidebarOpen(true)}
            ref={menuButtonRef}
            type="button"
          >
            <Icon name="menu" />
          </button>
          <div className="topbar-title"><small>RedTeam Essentials</small><strong>{title}</strong></div>
          <button className="search-trigger" onClick={() => setSearchOpen(true)} type="button">
            <Icon name="search" size={18} /><span>Buscar em tudo</span><kbd>Ctrl K</kbd>
          </button>
          <div className="topbar-progress" title={`${overall.percent}% concluído`}>
            <span><i style={{ width: `${overall.percent}%` }} /></span><small>{overall.percent}%</small>
          </div>
          <button
            aria-label={theme === 'dark' ? 'Usar tema claro' : 'Usar tema escuro'}
            className="icon-button"
            onClick={() => setTheme((current) => current === 'dark' ? 'light' : 'dark')}
            type="button"
          >
            <Icon name={theme === 'dark' ? 'sun' : 'moon'} />
          </button>
        </header>
        <main className="content-scroll" id="main-content" onScroll={handleScroll} ref={scrollRef} tabIndex="-1">
          {view}
        </main>
      </div>
      <SearchPalette
        catalog={catalog}
        onClose={() => setSearchOpen(false)}
        onSelect={(item) => navigate(item.itemType === 'resource' ? 'resource' : 'learn', item.id)}
        open={searchOpen}
        progress={progress}
      />
    </div>
  )
}
