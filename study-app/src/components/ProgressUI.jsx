import React from 'react'

export function ProgressBar({ value, label, compact = false }) {
  const percent = Math.max(0, Math.min(100, Number(value) || 0))
  return (
    <div className={`progress-bar-wrap${compact ? ' is-compact' : ''}`}>
      {label ? <span className="sr-only">{label}: {percent}%</span> : null}
      <div
        aria-label={label}
        aria-valuemax="100"
        aria-valuemin="0"
        aria-valuenow={percent}
        className="progress-bar"
        role="progressbar"
      >
        <span style={{ width: `${percent}%` }} />
      </div>
    </div>
  )
}

export function ProgressRing({ value, size = 'large' }) {
  const percent = Math.max(0, Math.min(100, Number(value) || 0))
  return (
    <div
      aria-label={`${percent}% dos conteúdos concluídos`}
      className={`progress-ring progress-ring--${size}`}
      role="img"
      style={{ '--progress': `${percent * 3.6}deg` }}
    >
      <div>
        <strong>{percent}%</strong>
        <span>dos conteúdos</span>
      </div>
    </div>
  )
}

export function MetaDot() {
  return <span aria-hidden="true" className="meta-dot" />
}
