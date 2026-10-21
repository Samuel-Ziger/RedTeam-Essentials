import React, { useEffect, useMemo, useState } from 'react'
import ReactMarkdown from 'react-markdown'
import rehypeSanitize from 'rehype-sanitize'
import remarkGfm from 'remark-gfm'

import { itemContext, resolveLocalItem } from '../lib/catalog.js'
import { markdownAnchor } from '../lib/markdown.js'
import { moduleAvailability } from '../lib/progress.js'
import { Icon } from './Icons.jsx'

const resourceCache = new Map()

function extractText(value) {
  if (typeof value === 'string' || typeof value === 'number') return String(value)
  if (Array.isArray(value)) return value.map(extractText).join('')
  if (value?.props?.children) return extractText(value.props.children)
  return ''
}

function safeUrl(resource, href = resource?.contentUrl) {
  if (!href) return undefined
  if (/^(?:mailto:|tel:|#)/i.test(href)) return href
  try {
    const base = new URL(resource.contentUrl, window.location.origin)
    const resolved = new URL(href, base)
    if (!['http:', 'https:'].includes(resolved.protocol)) return undefined
    if (resolved.origin === window.location.origin && !resolved.pathname.startsWith('/generated/content/')) {
      return undefined
    }
    return resolved.href
  } catch {
    return undefined
  }
}

function displayBytes(bytes) {
  const value = Number(bytes) || 0
  if (value < 1024) return `${value} B`
  if (value < 1024 * 1024) return `${(value / 1024).toFixed(value < 10240 ? 1 : 0)} KB`
  return `${(value / (1024 * 1024)).toFixed(1)} MB`
}

function Heading({ level, children, node: _node, ...props }) {
  const Tag = `h${level}`
  const anchor = markdownAnchor(extractText(children))
  return <Tag {...props} id={anchor ? `resource-${anchor}` : undefined}>{children}</Tag>
}

function LockedResource({ catalog, module, navigate, state }) {
  const pending = state.missingModuleIds
    .map((moduleId) => catalog.modules.find((candidate) => candidate.id === moduleId))
    .filter(Boolean)
  const visible = pending.slice(0, 8)
  const hiddenCount = Math.max(0, pending.length - visible.length)
  return (
    <section className="module-gate" role="status">
      <span className="module-gate-icon"><Icon name="lock" size={30} /></span>
      <span className="eyebrow">ARQUIVO BLOQUEADO</span>
      <h2>Conclua a base curricular antes de usar este recurso</h2>
      <p>Este arquivo pertence ao módulo {module.id}. Ainda há {pending.length} módulo{pending.length === 1 ? '' : 's'} pendente{pending.length === 1 ? '' : 's'}.</p>
      <div className="module-gate-requirements" aria-label="Módulos pendentes">
        {visible.map((required) => (
          <button key={required.id} onClick={() => navigate('module', required.id)} type="button">
            <span>{required.id}</span><strong>{required.title}</strong><Icon name="chevronRight" size={16} />
          </button>
        ))}
      </div>
      {hiddenCount ? <small className="module-gate-more">E mais {hiddenCount} módulo{hiddenCount === 1 ? '' : 's'} pendente{hiddenCount === 1 ? '' : 's'}.</small> : null}
      {pending[0] ? <button className="button button--primary" onClick={() => navigate('module', pending[0].id)} type="button">Continuar pelo módulo {pending[0].id} <Icon name="arrowRight" size={16} /></button> : null}
    </section>
  )
}

export function ResourceViewer({ catalog, resource, navigate, progress }) {
  const isImage = resource.kind === 'image'
  const [state, setState] = useState({ status: isImage ? 'ready' : 'loading', content: '', error: null })
  const [copied, setCopied] = useState(false)
  const [attempt, setAttempt] = useState(0)
  const module = catalog.modules.find((item) => item.id === resource.moduleId)
  const moduleState = module
    ? moduleAvailability(module, catalog, progress)
    : { unlocked: true, missingModuleIds: [] }
  const moduleLocked = Boolean(module && resource.origin === 'formation' && !moduleState.unlocked)
  const context = itemContext(catalog, resource)
  const primaryIsCollection = context.primary && catalog.groups.some((group) => group.id === context.primary.id)
  const relatedDocuments = (resource.relatedDocumentIds || [])
    .map((id) => catalog.documents.find((document) => document.id === id))
    .filter(Boolean)

  useEffect(() => {
    if (moduleLocked) {
      setState({ status: 'blocked', content: '', error: null })
      return undefined
    }
    if (isImage) {
      setState({ status: 'ready', content: '', error: null })
      return undefined
    }
    const controller = new AbortController()
    const url = safeUrl(resource)
    if (!url) {
      setState({ status: 'error', content: '', error: new Error('Endereço local inválido.') })
      return () => controller.abort()
    }
    if (resourceCache.has(url)) {
      setState({ status: 'ready', content: resourceCache.get(url), error: null })
      return () => controller.abort()
    }
    setState({ status: 'loading', content: '', error: null })
    fetch(url, { cache: 'no-store', signal: controller.signal })
      .then((response) => {
        if (!response.ok) throw new Error(`Não foi possível abrir o arquivo (HTTP ${response.status}).`)
        return response.text()
      })
      .then((content) => {
        resourceCache.set(url, content)
        setState({ status: 'ready', content, error: null })
      })
      .catch((error) => {
        if (error.name !== 'AbortError') setState({ status: 'error', content: '', error })
      })
    return () => controller.abort()
  }, [attempt, isImage, moduleLocked, resource])

  const markdownComponents = useMemo(() => ({
    a({ href, children, node: _node, ...props }) {
      if (href?.startsWith('#')) {
        const anchor = markdownAnchor(href.slice(1))
        return (
          <a
            href={`#resource-${anchor}`}
            onClick={(event) => {
              event.preventDefault()
              window.document.getElementById(`resource-${anchor}`)?.scrollIntoView({ behavior: 'smooth', block: 'start' })
            }}
            {...props}
          >{children}</a>
        )
      }
      const local = resolveLocalItem(catalog, resource, href)
      if (local) {
        return (
          <a
            href={local.itemType === 'resource' ? `#/resource/${encodeURIComponent(local.id)}` : `#/learn/${encodeURIComponent(local.id)}`}
            onClick={(event) => {
              event.preventDefault()
              navigate(local.itemType === 'resource' ? 'resource' : 'learn', local.id)
            }}
            {...props}
          >{children}</a>
        )
      }
      const target = safeUrl(resource, href)
      const external = /^(?:https?:)?\/\//i.test(href || '')
      return <a href={target} rel={external ? 'noreferrer noopener' : undefined} target={external ? '_blank' : undefined} {...props}>{children}</a>
    },
    img({ src, alt, node: _node, ...props }) {
      return <img alt={alt || ''} loading="lazy" src={safeUrl(resource, src)} {...props} />
    },
    h1: (props) => <Heading level={1} {...props} />,
    h2: (props) => <Heading level={2} {...props} />,
    h3: (props) => <Heading level={3} {...props} />,
    h4: (props) => <Heading level={4} {...props} />,
    h5: (props) => <Heading level={5} {...props} />,
    h6: (props) => <Heading level={6} {...props} />,
  }), [catalog, navigate, resource])

  async function copy() {
    try {
      await navigator.clipboard.writeText(state.content)
      setCopied(true)
      window.setTimeout(() => setCopied(false), 1600)
    } catch {
      setCopied(false)
    }
  }

  return (
    <div className="resource-page">
      <div className="reader-toolbar">
        <div className="breadcrumbs">
          <button onClick={() => navigate('library', resource.origin === 'legacy' ? 'security' : 'tools')} type="button">Biblioteca</button>
          <Icon name="chevronRight" size={13} />
          {primaryIsCollection ? <><button onClick={() => navigate('collection', context.primary.id)} type="button">{context.primaryTitle}</button><Icon name="chevronRight" size={13} /></> : null}
          {module ? <><button onClick={() => navigate('module', module.id)} title={module.title} type="button">Pasta {module.id}</button><Icon name="chevronRight" size={13} /></> : null}
          <span>{resource.title}</span>
        </div>
        <div className="resource-toolbar-actions">
          {!moduleLocked && !isImage && state.status === 'ready' ? (
            <button className="read-toggle" onClick={copy} type="button"><Icon name={copied ? 'check' : 'copy'} size={15} /> {copied ? 'Copiado' : 'Copiar'}</button>
          ) : null}
          {!moduleLocked ? <a className="read-toggle" download href={safeUrl(resource)}><Icon name="download" size={15} /> Baixar</a> : null}
        </div>
      </div>

      <div className="resource-container">
        <header className="reader-heading resource-heading">
          <span className={`content-type resource-kind resource-kind--${resource.kind}`}>{resource.kindLabel}</span>
          <h1>{resource.title}</h1>
          {resource.description ? <p>{resource.description}</p> : null}
          <div className="reader-meta">
            <span><Icon name={resource.kind === 'code' ? 'code' : resource.kind === 'image' ? 'image' : 'file'} size={15} /> {resource.language || resource.kind}</span>
            <span>{displayBytes(resource.bytes)}</span>
            {context.primary ? <span>{context.primaryTitle}</span> : null}
            {module && context.primary?.id !== module.id ? <span>Pasta física: módulo {module.id}</span> : null}
          </div>
        </header>

        {moduleLocked ? <LockedResource catalog={catalog} module={module} navigate={navigate} state={moduleState} /> : null}
        {!moduleLocked && state.status === 'loading' ? (
          <div aria-label="Carregando arquivo" className="reader-loading" role="status"><span /><span /><span /><span /><span /></div>
        ) : null}
        {!moduleLocked && state.status === 'error' ? (
          <div className="inline-error" role="alert">
            <Icon name="file" size={24} />
            <div><strong>O arquivo não pôde ser carregado</strong><p>{state.error?.message}</p><button className="button button--secondary" onClick={() => setAttempt((value) => value + 1)} type="button"><Icon name="refresh" size={16} /> Tentar novamente</button></div>
          </div>
        ) : null}
        {!moduleLocked && state.status === 'ready' && isImage ? (
          <div className="resource-image"><img alt={resource.title} src={safeUrl(resource)} /></div>
        ) : null}
        {!moduleLocked && state.status === 'ready' && resource.kind === 'markdown' ? (
          <article className="markdown-body">
            <ReactMarkdown components={markdownComponents} rehypePlugins={[rehypeSanitize]} remarkPlugins={[remarkGfm]}>{state.content}</ReactMarkdown>
          </article>
        ) : null}
        {!moduleLocked && state.status === 'ready' && !isImage && resource.kind !== 'markdown' ? (
          <div className="resource-code" data-language={resource.language || resource.kind}>
            <div><span>{resource.language || resource.kind}</span><span>{state.content.split('\n').length} linhas</span></div>
            <pre><code>{state.content}</code></pre>
          </div>
        ) : null}

        {!moduleLocked && relatedDocuments.length ? (
          <section className="related-materials">
            <span className="eyebrow">MATERIAL RELACIONADO</span>
            <h2>Onde este arquivo é utilizado</h2>
            <div>{relatedDocuments.map((document) => (
              <button key={document.id} onClick={() => navigate('learn', document.id)} type="button"><Icon name="book" size={17} /><span><strong>{document.title}</strong><small>{document.typeLabel}</small></span><Icon name="arrowRight" size={16} /></button>
            ))}</div>
          </section>
        ) : null}
        <div className="source-path">Fonte local: <code>{resource.sourcePath}</code></div>
      </div>
    </div>
  )
}
