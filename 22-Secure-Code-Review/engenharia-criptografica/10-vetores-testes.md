# 10 — Vetores, testes negativos e interoperabilidade

Known-answer tests confirmam compatibilidade com padrão; round trip sozinho pode
validar dois erros simétricos. Inclua vetores oficiais, limites, chave/nonce
inválidos, alteração de cada campo, mensagem vazia e formatos malformados.

Teste interoperabilidade com implementação independente e fixe bytes canônicos.
Segredos de vetor são públicos e nunca reutilizados. Teste de regressão acompanha
cada incidente e versão de formato.

## Prática

Monte matriz entrada→resultado→propriedade e identifique o teste que falharia se
AAD deixasse de incluir key ID.
