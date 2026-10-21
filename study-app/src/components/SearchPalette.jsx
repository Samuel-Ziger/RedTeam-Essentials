import React, { useEffect, useMemo, useRef, useState } from 'react'

import { itemContext, searchLibrary } from '../lib/catalog.js'
import { isDocumentCompleted } from '../lib/progress.js'
import { Icon } from './Icons.jsx'

export function SearchPalette({ catalog, progress, open, onClose, onSelect }) {
  const [query, setQuery] = useState('')
  const [selectedIndex, setSelectedIndex] = useState(0)
  const [itemType, setItemType] = useState('all')
  const [visibleCount, setVisibleCount] = useState(50)
  const inputRef = useRef(null)
  const resultRefs = useRef([])
  const search = useMemo(() => searchLibrary(catalog, query, { itemType }), [catalog, itemType, query])
  const results = search.results.slice(0, visibleCount)

  useEffect(() => {
    if (!open) return undefined
    setSelectedIndex(0)
    const frame = requestAnimationFrame(() => inputRef.current?.focus())
    const onKeyDown = (event) => {
      if (event.key === 'Escape') onClose()
    }
    window.addEventListener('keydown', onKeyDown)
    return () => {
      cancelAnimationFrame(frame)
      window.removeEventListener('keydown', onKeyDown)
    }
  }, [open, onClose])

  useEffect(() => {
    setSelectedIndex(0)
    setVisibleCount(50)
  }, [itemType, query])

  useEffect(() => {
    if (!open) return
    resultRefs.current[selectedIndex]?.scrollIntoView({
      block: 'nearest',
      inline: 'nearest',
    })
  }, [itemType, open, query, results.length, selectedIndex])

  if (!open) return null

  function choose(item) {
    onSelect(item)
    setQuery('')
    onClose()
  }

  function handleKeys(event) {
    if (event.key === 'ArrowDown') {
      event.preventDefault()
      setSelectedIndex((current) => Math.min(results.length - 1, current + 1))
    } else if (event.key === 'ArrowUp') {
      event.preventDefault()
      setSelectedIndex((current) => Math.max(0, current - 1))
    } else if (event.key === 'Enter' && results[selectedIndex]) {
      event.preventDefault()
      choose(results[selectedIndex].item)
    }
  }

  return (
    <div aria-label="Buscar no curso" aria-modal="true" className="search-overlay" role="dialog">
      <button aria-label="Fechar busca" className="search-backdrop" onClick={onClose} type="button" />
      <div className="search-palette">
        <div className="search-input-row">
          <Icon name="search" size={21} />
          <input
            aria-controls="search-results"
            aria-label="Buscar conteúdos, laboratórios, ferramentas e arquivos"
            onChange={(event) => setQuery(event.target.value)}
            onKeyDown={handleKeys}
            placeholder="Busque por assunto, código, módulo ou caminho..."
            ref={inputRef}
            type="search"
            value={query}
          />
          <kbd>esc</kbd>
        </div>
        {query ? (
          <div aria-label="Filtrar resultados da busca" className="search-facets">
            <button aria-pressed={itemType === 'all'} onClick={() => setItemType('all')} type="button">Tudo <span>{search.facets.documents + search.facets.resources}</span></button>
            <button aria-pressed={itemType === 'document'} onClick={() => setItemType('document')} type="button">Conteúdos <span>{search.facets.documents}</span></button>
            <button aria-pressed={itemType === 'resource'} onClick={() => setItemType('resource')} type="button">Arquivos <span>{search.facets.resources}</span></button>
          </div>
        ) : null}
        <div aria-label="Resultados da busca" aria-live="polite" className="search-results" id="search-results" role="listbox">
          {!query ? (
            <div className="search-empty">
              <span><Icon name="sparkles" size={24} /></span>
              <strong>Encontre qualquer item da biblioteca</strong>
              <p>Pesquise em conteúdos, materiais complementares, código, configurações e dados.</p>
            </div>
          ) : results.length ? (
            <>
              <div className="search-result-count">{search.total} resultado{search.total === 1 ? '' : 's'} · exibindo {results.length}</div>
              {results.map(({ item }, index) => {
                const context = itemContext(catalog, item)
                return <button
                  aria-selected={index === selectedIndex}
                  className={`search-result${index === selectedIndex ? ' is-selected' : ''}`}
                  key={`${item.itemType}-${item.id}`}
                  onClick={() => choose(item)}
                  onMouseEnter={() => setSelectedIndex(index)}
                  ref={(element) => { resultRefs.current[index] = element }}
                  role="option"
                  type="button"
                >
                  <span className={`result-icon result-icon--${item.itemType === 'resource' ? item.kind : item.type}`}>
                    <Icon name={item.itemType === 'resource' ? item.kind === 'code' ? 'code' : 'file' : item.type === 'lab' ? 'flask' : 'book'} size={18} />
                  </span>
                  <span>
                    <strong>{item.title}</strong>
                    <small>{context.primaryTitle} · {item.itemType === 'resource' ? item.kindLabel : item.typeLabel}</small>
                    <code>{item.sourcePath}</code>
                  </span>
                  {item.itemType === 'document' && isDocumentCompleted(progress, item.id) ? (
                    <span className="search-read"><Icon name="check" size={14} /> Lido</span>
                  ) : null}
                </button>
              })}
              {results.length < search.total ? (
                <button className="search-load-more" onClick={() => setVisibleCount((count) => count + 50)} type="button">
                  Mostrar mais {Math.min(50, search.total - results.length)} resultados
                </button>
              ) : null}
            </>
          ) : (
            <div className="search-empty">
              <span><Icon name="search" size={24} /></span>
              <strong>Nada encontrado</strong>
              <p>Tente termos mais curtos ou procure pelo nome de um módulo.</p>
            </div>
          )}
        </div>
        <footer className="search-footer">
          <span><kbd>↑</kbd><kbd>↓</kbd> navegar</span>
          <span><kbd>↵</kbd> abrir</span>
          <span><kbd>esc</kbd> fechar</span>
        </footer>
      </div>
    </div>
  )
}
