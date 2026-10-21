# 08 — Política BGP e segurança de rotas

Prefix filters e listas de AS autorizam o que entra/sai. Maximum-prefix limita
impacto de vazamento. Bogons/martians, seus próprios prefixos e default devem ser
tratados explicitamente. Communities padronizam ações operacionais.

RPKI associa prefixo, comprimento máximo e AS de origem em ROAs. Validação de
origem classifica Valid, Invalid ou NotFound; ela não valida todo AS_PATH.
Políticas de rejeição/preferência precisam de rollout e monitoramento.

GTSM/TTL security, autenticação de sessão quando suportada, ACL de controle,
CoPP e proteção de gestão reduzem superfície. Nenhum substitui filtros de rota.

## Mudança segura

Teste política com rotas sintéticas, use preview/diff, aplique a um peer canário,
monitore contagens e tenha rollback. Um erro de filtro pode retirar ou vazar
milhares de prefixos em segundos.
