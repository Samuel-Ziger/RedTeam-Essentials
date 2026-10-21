import { useCallback, useEffect, useState } from 'react'

import { normalizeCatalog } from '../lib/catalog.js'

export function useCatalog() {
  const [state, setState] = useState({ status: 'loading', catalog: null, error: null })
  const [attempt, setAttempt] = useState(0)

  useEffect(() => {
    const controller = new AbortController()
    setState((current) => ({ ...current, status: 'loading', error: null }))

    fetch('/generated/catalog.json', { cache: 'no-store', signal: controller.signal })
      .then((response) => {
        if (!response.ok) throw new Error(`Catálogo indisponível (HTTP ${response.status})`)
        return response.json()
      })
      .then((payload) => {
        const catalog = normalizeCatalog(payload)
        if (!catalog.documents.length) {
          throw new Error('O catálogo foi carregado, mas não possui documentos.')
        }
        setState({ status: 'ready', catalog, error: null })
      })
      .catch((error) => {
        if (error.name !== 'AbortError') {
          setState({ status: 'error', catalog: null, error })
        }
      })

    return () => controller.abort()
  }, [attempt])

  const retry = useCallback(() => setAttempt((value) => value + 1), [])
  return { ...state, retry }
}
