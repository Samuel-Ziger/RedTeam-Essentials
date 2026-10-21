export function markdownAnchor(value) {
  let decoded = String(value || '')
  try {
    decoded = decodeURIComponent(decoded)
  } catch {
    // Mantém o fragmento original quando a codificação estiver incompleta.
  }
  return decoded
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '')
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-|-$/g, '')
}
