# 13 — Curvas elípticas

ECC trabalha com grupos de pontos e oferece chaves menores para níveis de
segurança comparáveis a sistemas clássicos. Curva, codificação, validação de
ponto, hash, nonce de assinatura e protocolo determinam segurança.

Não misture ECDH e ECDSA sob a mesma chave nem aceite curvas arbitrárias.
Prefira APIs específicas como X25519 e Ed25519 quando o ecossistema permitir.
Interoperabilidade regulada pode exigir perfis NIST; documente a razão.

## Verificação

Por que “ECC-256” é insuficiente para identificar um formato e uma operação?
