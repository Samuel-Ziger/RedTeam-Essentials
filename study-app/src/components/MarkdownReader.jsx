import React, { useEffect, useMemo, useState } from 'react'
import ReactMarkdown from 'react-markdown'
import rehypeSanitize from 'rehype-sanitize'
import remarkGfm from 'remark-gfm'

import { resolveLocalItem } from '../lib/catalog.js'
import { markdownAnchor } from '../lib/markdown.js'
import { Icon } from './Icons.jsx'

const contentCache = new Map()

function extractText(value) {
  if (typeof value === 'string' || typeof value === 'number') return String(value)
  if (Array.isArray(value)) return value.map(extractText).join('')
  if (value?.props?.children) return extractText(value.props.children)
  return ''
}

function safeContentUrl(document, href) {
  if (!href) return undefined
  if (/^(?:mailto:|tel:|#)/i.test(href)) return href
  try {
    const resolved = new URL(href, new URL(document.contentUrl, window.location.origin))
    if (!['http:', 'https:'].includes(resolved.protocol)) return undefined
    if (
      resolved.origin === window.location.origin
      && !resolved.pathname.startsWith('/generated/content/')
    ) return undefined
    return resolved.href
  } catch {
    return undefined
  }
}

function MarkdownHeading({ level, children, node: _node, ...props }) {
  const Tag = `h${level}`
  const anchor = markdownAnchor(extractText(children))
  return <Tag {...props} id={anchor ? `md-${anchor}` : undefined}>{children}</Tag>
}

function CodeBlock({ children }) {
  const [copied, setCopied] = useState(false)
  const code = extractText(children)

  async function copy() {
    try {
      await navigator.clipboard.writeText(code)
      setCopied(true)
      window.setTimeout(() => setCopied(false), 1600)
    } catch {
      setCopied(false)
    }
  }

  return (
    <div className="code-block">
      <button aria-label="Copiar código" onClick={copy} type="button">
        <Icon name={copied ? 'check' : 'copy'} size={15} />
        {copied ? 'Copiado' : 'Copiar'}
      </button>
      <pre>{children}</pre>
    </div>
  )
}

export function MarkdownReader({ catalog, document, onOpenItem, onOpenDocument, onReady }) {
  const [state, setState] = useState({ status: 'loading', content: '', error: null, documentId: document.id })
  const [attempt, setAttempt] = useState(0)

  useEffect(() => {
    const controller = new AbortController()
    if (document.content) {
      setState({ status: 'ready', content: document.content, error: null, documentId: document.id })
      return () => controller.abort()
    }

    const url = document.contentUrl
    if (!url) {
      setState({
        status: 'error',
        content: '',
        error: new Error('Este documento não possui um endereço de conteúdo no catálogo.'),
        documentId: document.id,
      })
      return () => controller.abort()
    }

    if (contentCache.has(url)) {
      setState({ status: 'ready', content: contentCache.get(url), error: null, documentId: document.id })
      return () => controller.abort()
    }

    setState({ status: 'loading', content: '', error: null, documentId: document.id })
    fetch(url, { cache: 'no-store', signal: controller.signal })
      .then((response) => {
        if (!response.ok) throw new Error(`Não foi possível abrir o arquivo (HTTP ${response.status}).`)
        return response.text()
      })
      .then((content) => {
        contentCache.set(url, content)
        setState({ status: 'ready', content, error: null, documentId: document.id })
      })
      .catch((error) => {
        if (error.name !== 'AbortError') {
          setState({ status: 'error', content: '', error, documentId: document.id })
        }
      })

    return () => controller.abort()
  }, [document.content, document.contentUrl, document.id, attempt])

  useEffect(() => {
    if (state.status === 'loading' || state.documentId !== document.id || !onReady) return undefined
    let innerFrame
    const outerFrame = requestAnimationFrame(() => {
      innerFrame = requestAnimationFrame(() => onReady(document.id))
    })
    return () => {
      cancelAnimationFrame(outerFrame)
      if (innerFrame) cancelAnimationFrame(innerFrame)
    }
  }, [document.id, onReady, state.documentId, state.status])

  const components = useMemo(() => ({
    pre: CodeBlock,
    a({ href, children, node: _node, ...props }) {
      if (href?.startsWith('#')) {
        const anchor = markdownAnchor(href.slice(1))
        return (
          <a
            href={href}
            onClick={(event) => {
              event.preventDefault()
              window.document.getElementById(`md-${anchor}`)?.scrollIntoView({
                behavior: 'smooth',
                block: 'start',
              })
            }}
            {...props}
          >
            {children}
          </a>
        )
      }
      const localItem = resolveLocalItem(catalog, document, href)
      if (localItem) {
        const route = localItem.itemType === 'resource' ? 'resource' : 'learn'
        return (
          <a
            href={`#/${route}/${encodeURIComponent(localItem.id)}`}
            onClick={(event) => {
              event.preventDefault()
              ;(onOpenItem || onOpenDocument)?.(localItem)
            }}
            {...props}
          >
            {children}
          </a>
        )
      }
      const external = /^(?:https?:)?\/\//i.test(href || '')
      const opensSeparate = external || Boolean(href && !href.startsWith('#') && !/^(?:mailto:|tel:)/i.test(href))
      return (
        <a
          href={safeContentUrl(document, href)}
          rel={opensSeparate ? 'noreferrer noopener' : undefined}
          target={opensSeparate ? '_blank' : undefined}
          {...props}
        >
          {children}
        </a>
      )
    },
    img({ src, alt, node: _node, ...props }) {
      return <img alt={alt || ''} loading="lazy" src={safeContentUrl(document, src)} {...props} />
    },
    input({ type, node: _node, ...props }) {
      return <input disabled={type === 'checkbox'} type={type} {...props} />
    },
    h1: (props) => <MarkdownHeading level={1} {...props} />,
    h2: (props) => <MarkdownHeading level={2} {...props} />,
    h3: (props) => <MarkdownHeading level={3} {...props} />,
    h4: (props) => <MarkdownHeading level={4} {...props} />,
    h5: (props) => <MarkdownHeading level={5} {...props} />,
    h6: (props) => <MarkdownHeading level={6} {...props} />,
  }), [catalog, document, onOpenDocument, onOpenItem])

  if (state.status === 'loading') {
    return (
      <div aria-label="Carregando documento" className="reader-loading" role="status">
        <span /><span /><span /><span /><span />
      </div>
    )
  }

  if (state.status === 'error') {
    return (
      <div className="inline-error" role="alert">
        <span><Icon name="book" size={24} /></span>
        <div>
          <strong>O conteúdo não pôde ser carregado</strong>
          <p>{state.error?.message}</p>
          <button className="button button--secondary" onClick={() => setAttempt((value) => value + 1)} type="button">
            <Icon name="refresh" size={16} /> Tentar novamente
          </button>
        </div>
      </div>
    )
  }

  return (
    <article className="markdown-body">
      <ReactMarkdown
        components={components}
        rehypePlugins={[rehypeSanitize]}
        remarkPlugins={[remarkGfm]}
      >
        {state.content}
      </ReactMarkdown>
    </article>
  )
}
