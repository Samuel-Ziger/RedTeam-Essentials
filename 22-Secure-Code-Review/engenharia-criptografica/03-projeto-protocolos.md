# 03 — Projeto de protocolos

Especifique atores, estados, mensagens, gramática, transcript, chaves, erros,
limites, timeouts e encerramento. Comece por protocolo conhecido; pequenas
mudanças podem invalidar análise existente. Separe negotiation data de dados
autenticados e defina quando cada entrada se torna confiável.

Inclua versionamento e extensibilidade sem ambiguidades. Campos desconhecidos
críticos falham; campos opcionais têm valor padrão inequívoco; comprimentos são
limitados antes da alocação. Estado inválido não “tenta continuar”.

## Prática

Escreva máquina de estados para um registro autenticado com INIT, ACTIVE,
ROTATING e CLOSED.
