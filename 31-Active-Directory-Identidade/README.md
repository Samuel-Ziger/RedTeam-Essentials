# 31 — Active Directory e identidade híbrida

O módulo aplica a base de Windows empresarial a diretórios, Kerberos,
relações de confiança e identidades híbridas. A análise ofensiva autorizada e
a validação defensiva compartilham o mesmo grafo de caminhos e controles.

## Contrato do módulo

| Campo | Definição |
|---|---|
| Público | Administração Windows, engenharia de identidade, SOC e Purple Team. |
| Pré-requisitos | Módulos `27`, `28` e `29`; Windows `08`–`11`. |
| Tempo estimado | 50–80 horas. |
| Ambiente | Floresta de laboratório isolada e identidades fictícias. |
| Foco | Inventário, delegação, caminhos de privilégio, detecção e remediação. |
| Evidência final | Grafo comentado, hipóteses validadas e plano de redução de risco. |
| Critério de conclusão | Caminhos prioritários explicados, mitigados e retestados no lab. |

## Conteúdo curricular

- [Active Directory e identidade híbrida](active-directory-identidade-hibrida/README.md)
- [Comandos de inventário AD](active-directory-identidade-hibrida/ad_enum_commands.md)
- [BloodHound: teoria e interpretação](active-directory-identidade-hibrida/bloodhound_teoria.md)
- [Kerberoasting: teoria e defesa](active-directory-identidade-hibrida/kerberoasting_teoria.md)
- [Cenários modernos de AD](active-directory-identidade-hibrida/modern-ad-attacks-2026.md)
- [Identidade híbrida](active-directory-identidade-hibrida/LEGADO-IDENTIDADE-HIBRIDA.md)

Próximo: [Módulo 32 — Segurança em nuvem](../32-Cloud-Security/README.md).
