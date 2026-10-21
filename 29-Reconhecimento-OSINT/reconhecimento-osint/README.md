# Reconhecimento e OSINT

O percurso vai de fontes passivas a validações ativas estritamente autorizadas.
Para cada dado, registre fonte, momento da coleta, confiança e possível impacto.

## Sequência

| Fase | Leituras e ferramentas | Entrega |
|---|---|---|
| Pergunta | [Catálogo OSINT](../acervo/osint/osint-tools-list.md) | Requisitos de inteligência e fontes permitidas. |
| Coleta passiva | [Cheatsheet](../passive_recon_cheatsheet.md) | Evidências com proveniência. |
| Superfície web | [Notas web](../web_recon_notes.md) | Ativos e relações normalizados. |
| DNS autorizado | [Bash](../dns_enum.sh) e [PowerShell](../dns_enum.ps1) | Resultados equivalentes e auditáveis. |
| Automação | [OSINT em PowerShell](../acervo/osint/osint_automation.ps1) | Pipeline com rate limit, cache e tratamento de erro. |

## Critério de conclusão

Produza um inventário deduplicado, separe fatos de inferências, revise falsos
positivos e indique lacunas. Não colete dados pessoais sem necessidade e base
legal compatível com o exercício.
