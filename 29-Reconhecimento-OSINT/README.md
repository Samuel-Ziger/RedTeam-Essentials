# 29 — Reconhecimento avançado, OSINT e superfície de ataque

O módulo organiza reconhecimento passivo, enumeração autorizada e OSINT em
um fluxo orientado por hipóteses, escopo e qualidade da evidência.

## Contrato do módulo

| Campo | Definição |
|---|---|
| Público | Analistas de segurança, OSINT, exposição externa e Purple Team. |
| Pré-requisitos | Módulos `27` e `28`. |
| Tempo estimado | 32–48 horas. |
| Limite | Fontes públicas e ativos explicitamente autorizados. |
| Foco | Descoberta, validação, proveniência, correlação e priorização. |
| Ambiente | Fontes públicas permitidas, fixtures e domínios do próprio laboratório. |
| Evidência final | Inventário de superfície com fonte, confiança, timestamp e lacunas. |
| Critério de conclusão | Inventário deduplicado, revisado e acompanhado de limitações. |

## Conteúdo curricular

- [Reconhecimento e OSINT](reconhecimento-osint/README.md)
- [Cheatsheet de reconhecimento passivo](passive_recon_cheatsheet.md)
- [Notas de reconhecimento web](web_recon_notes.md)
- [Enumeração DNS em Bash](dns_enum.sh)
- [Enumeração DNS em PowerShell](dns_enum.ps1)
- [Acervo histórico de Recon](LEGADO-RECON.md)
- [Catálogo de fontes OSINT](acervo/osint/osint-tools-list.md)
- [Automação OSINT](acervo/osint/osint_automation.ps1)

O resultado não é uma lista bruta de achados: é um mapa explicável, com
falsos positivos revisados e separação clara entre fato e inferência.

Próximo: [Módulo 30 — Web, APIs e AppSec](../30-Web-API-AppSec/README.md).
