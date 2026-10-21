# 05 — Nomes, SAN, EKU e políticas

Para TLS, identidades DNS e IP ficam em Subject Alternative Name. Wildcard
possui regras limitadas e amplia impacto operacional. EKU restringe finalidade,
como serverAuth ou clientAuth; Key Usage restringe operações de chave.

Não coloque segredo, e-mail desnecessário ou dado pessoal no certificado: ele
pode aparecer em logs e transparência. Normalize nomes conforme biblioteca e
use identificadores de workload estáveis quando a infraestrutura os suporta.

## Verificação

Um certificado válido para `api.example.test` deve servir
`db.example.test`? Explique sem depender apenas do emissor.
