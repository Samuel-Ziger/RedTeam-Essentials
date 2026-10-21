# 17 — Formatos versionados e agilidade

Formato criptográfico é protocolo duradouro. Inclua magic/version, suite fixa,
key ID, nonce, AAD e comprimentos limitados. Canonicalize uma única vez e
autentique todo campo que influencia interpretação.

Agilidade não é aceitar qualquer algoritmo enviado pelo cliente. É possuir
inventário, política allowlist, leitores para versões necessárias, escritor
único atual e plano de migração testado. Algoritmo desconhecido falha fechado;
downgrade nunca é fallback silencioso.

## Prática

Desenhe a matriz leitor/escritor durante migração v1→v2 e o ponto de rollback.
