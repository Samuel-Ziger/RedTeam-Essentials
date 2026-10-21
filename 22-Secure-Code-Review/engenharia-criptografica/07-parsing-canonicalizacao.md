# 07 — Parsing, canonicalização e formatos

Criptografia autentica bytes, enquanto aplicações interpretam estruturas.
Duplicidade de chaves JSON, Unicode, números, ordem, Base64 flexível e campos
ignorados podem fazer assinante e verificador entenderem coisas diferentes.

Defina gramática fechada, codificação, limites, normalização e canonicalização.
Rejeite duplicados e trailing data; autentique antes de usar campos. Para novos
protocolos, prefira serialização determinística padronizada.

## Prática

Crie corpus com campo duplicado, Unicode equivalente, Base64 inválido, inteiro
excessivo e bytes finais. Todos devem ter resultado inequívoco.
