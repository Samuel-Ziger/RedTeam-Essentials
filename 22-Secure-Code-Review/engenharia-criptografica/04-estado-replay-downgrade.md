# 04 — Estado, replay, downgrade e binding

Autenticidade não garante frescor. Nonce, contador, janela, timestamp com relógio
confiável ou identificador idempotente podem detectar replay conforme sistema.
Estado precisa sobreviver a concorrência, reinício e rollback de snapshot.

Downgrade ocorre quando um atacante influencia versão/algoritmo para opção mais
fraca. Vincule negociação ao transcript, mantenha allowlist e não faça fallback
após erro genérico. Reflection e role confusion são evitados com papéis e
direções distintos na derivação e mensagens.

## Prática

Teste mensagem duplicada, fora de ordem, de outra direção e de versão anterior.
