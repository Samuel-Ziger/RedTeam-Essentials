# 09 — OUs, grupos, delegação e lifecycle

OU organiza administração e aplicação de política; não replique o organograma
sem necessidade. Groups representam função/acesso. Contas representam pessoas,
serviços ou dispositivos com owner e lifecycle.

## Modelo de grupo

Uma convenção como AGDLP expressa Accounts → Global groups → Domain Local
groups → Permissions. Em ambientes multi-domain, escopos e universal groups
exigem desenho. O princípio é separar identidade funcional de permissão técnica.

## Delegation

Delegue tarefas específicas no menor escopo: reset de senha de uma população,
gerenciamento de grupo determinado ou criação de objetos em OU. Evite usar
grupos altamente privilegiados para operação cotidiana.

## Lifecycle

Joiner/mover/leaver precisa de fonte autoritativa, aprovação, validade,
recertificação e desativação antes da exclusão. Contas inativas e grupos sem
owner são dívida de segurança.

## Exercício offline

Use `Test-RteEnterpriseModel.ps1` para validar fixture de identidades, grupos e
permissões. Corrija ciclos, membros desconhecidos e owners ausentes.

