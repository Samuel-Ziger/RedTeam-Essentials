# 16 — Disco, arquivo, backup e recuperação

Full-disk encryption protege mídia desligada; não protege dados de processo
comprometido após desbloqueio. Criptografia de arquivo/objeto separa chaves e
contextos, mas vaza metadados conforme formato. Backups precisam de chave e
procedimento de restauração independente do sistema perdido.

Defina RPO/RTO, cópias imutáveis, escrow autorizado, rotação, teste de restore e
destruição. Perder chave é perder dados; guardar chave junto ao único backup
anula resiliência. Não invente criptografia de disco: use BitLocker, FileVault,
LUKS ou solução suportada.

## Prática

Faça teste de restauração com cópia sintética e operador que não conhece o
ambiente original.
