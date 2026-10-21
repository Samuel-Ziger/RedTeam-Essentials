import { useCallback, useEffect, useState } from 'react'

import {
  createEmptyProgress,
  loadProgress,
  recordScroll,
  recordVisit,
  saveProgress,
  setDocumentCompleted,
  setLabCompleted,
} from '../lib/progress.js'

export function useProgress() {
  const [progress, setProgress] = useState(() =>
    typeof window === 'undefined' ? createEmptyProgress() : loadProgress(window.localStorage),
  )

  useEffect(() => {
    saveProgress(window.localStorage, progress)
  }, [progress])

  const markDocument = useCallback((documentId, completed) => {
    setProgress((current) => setDocumentCompleted(current, documentId, completed))
  }, [])

  const markLab = useCallback((labId, completed) => {
    setProgress((current) => setLabCompleted(current, labId, completed))
  }, [])

  const visit = useCallback((document, context) => {
    setProgress((current) => {
      if (current.lastDocument?.id === document?.id) return current
      return recordVisit(current, document, context)
    })
  }, [])

  const saveScroll = useCallback((documentId, position) => {
    setProgress((current) => {
      if (Math.abs((current.scrollPositions[documentId] || 0) - position) < 8) return current
      return recordScroll(current, documentId, position)
    })
  }, [])

  const reset = useCallback(() => setProgress(createEmptyProgress()), [])

  return { progress, markDocument, markLab, visit, saveScroll, reset }
}
