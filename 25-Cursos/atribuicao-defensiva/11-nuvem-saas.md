# 11 — Nuvem e SaaS

Cloud control planes registram chamadas administrativas, principal, role,
recurso, região, origem, user-agent e resultado. Data plane e sistema operacional
podem exigir fontes adicionais.

## Identidade federada

Siga a cadeia IdP → token → role → chamada. Uma role assumida não é nome de
pessoa; preserve issuer, subject, session name e device/contexto. Tokens podem
ser roubados ou usados por automação.

## Integridade

Envie audit logs para conta/projeto separado, armazenamento com imutabilidade,
acesso restrito e alertas sobre alteração da trilha. Monitore regiões e serviços
que não estavam habilitados no baseline.

## SaaS

Retenção e campos variam por licença. Documente API de exportação, atraso,
timezone, paginação e limites. Preserve o export original e hash antes de
normalizar.

## Contenção

Revogue sessão/chave, reduza role, isole workload ou aplique SCP/policy conforme
impacto. Destruir instância antes de preservar evidência pode apagar contexto.

## Prática

Modele uma concessão administrativa com IdP, control plane e ticket aprovado.
Crie caso positivo e alteração legítima equivalente.

