# Lab 04 — Automação e mudança segura

Crie pipeline conceitual schema -> lint -> render -> diff -> review -> lab ->
canário -> post-check. Injete erro de prefixo, segredo no diff, API parcialmente
indisponível e drift manual.

**Aceite:** pipeline falha antes da aplicação, segredos são redigidos, operação
é idempotente e rollback/confirmed commit não depende da sessão principal.
