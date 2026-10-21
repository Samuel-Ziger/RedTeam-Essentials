import { useCallback, useEffect, useState } from 'react'

function parseHash(hash) {
  const clean = (hash || '').replace(/^#\/?/, '')
  const [view = 'dashboard', ...rest] = clean.split('/')
  const known = new Set([
    'dashboard',
    'learn',
    'track',
    'module',
    'collection',
    'resource',
    'library',
    'labs',
    'progress',
  ])
  if (!known.has(view)) return { view: 'dashboard', id: null }
  let id = null
  try {
    id = rest.length ? decodeURIComponent(rest.join('/')) : null
  } catch {
    id = rest.join('/') || null
  }
  return { view, id }
}

export function routeHref(view, id) {
  return `#/${view}${id ? `/${encodeURIComponent(id)}` : ''}`
}

export function useHashRoute() {
  const [route, setRoute] = useState(() => parseHash(window.location.hash))
  const [navigationRevision, setNavigationRevision] = useState(0)

  useEffect(() => {
    if (!window.location.hash) window.history.replaceState(null, '', '#/dashboard')
    const onHashChange = () => {
      setRoute(parseHash(window.location.hash))
      setNavigationRevision((current) => current + 1)
    }
    window.addEventListener('hashchange', onHashChange)
    onHashChange()
    return () => window.removeEventListener('hashchange', onHashChange)
  }, [])

  const navigate = useCallback((view, id) => {
    const next = routeHref(view, id)
    if (window.location.hash === next) setNavigationRevision((current) => current + 1)
    else window.location.hash = next
  }, [])

  return { route, navigate, navigationRevision }
}
