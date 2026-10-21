# 00 — Método de engenharia criptográfica

Uma solução começa por propriedades e ameaça, segue por construção padronizada,
implementação, gestão de chave e operação, e termina em evidência. A revisão
pergunta “quais garantias sob quais hipóteses?”, não apenas “qual algoritmo?”.

Crie um cryptographic design record: dados e longevidade, adversário, primitivas
e parâmetros, formato, chaves, confiança, falhas, telemetria, recuperação,
dependências e plano de migração. Toda decisão tem dono e data de revisão.

## Regra

Primitiva própria só é aceitável como exercício marcado. Produção usa protocolo
padronizado, biblioteca mantida e revisão especializada.
