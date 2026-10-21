# 14 — OpenPGP, S/MIME e assinatura de artefatos

OpenPGP usa certificados/chaves e modelos de confiança próprios; S/MIME usa
X.509. Ambos exigem validar identidade, algoritmo, expiração e revogação. Cifrar
e-mail não esconde todos os metadados e endpoints continuam vendo plaintext.

Assinatura de artefato deve cobrir bytes reproduzíveis, identidade do emissor,
proveniência e política de verificação. Distribua chave pública por canal
autenticado; checksum publicado ao lado do arquivo não substitui assinatura.

## Prática

Desenhe verificação de release que falha fechado para assinatura ausente,
identidade inesperada e digest divergente.
