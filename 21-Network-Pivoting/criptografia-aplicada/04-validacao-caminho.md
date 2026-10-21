# 04 — Construção e validação de caminho

O validador constrói caminho do leaf até uma âncora, verifica assinaturas,
validade, extensões críticas, constraints, políticas e uso. A ordem enviada pelo
servidor ajuda a construção, mas a raiz normalmente não precisa ser enviada.

Validade temporal depende de relógio correto. Cadeia válida não prova que o nome
pedido corresponde ao certificado; hostname e finalidade são verificações
adicionais. Bibliotecas de plataforma devem fazer validação, não código caseiro.

## Prática

Separe “parseou”, “assinatura bate”, “cadeia confiável”, “nome corresponde” e
“política permite” em cinco resultados diferentes.
