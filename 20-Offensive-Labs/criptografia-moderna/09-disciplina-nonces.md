# 09 — Disciplina de nonces

“Aleatório” não é sinônimo de “nunca repete”. Uma estratégia precisa considerar
taxa, vida da chave, reinícios, múltiplos escritores, clones de VM e rollback.
Pode usar geração aleatória com orçamento de colisão ou contador persistente com
prefixo exclusivo, desde que o algoritmo aceite a estratégia.

Registre contagem e chave ativa, não cada plaintext. Rotacione antes do limite,
falhe fechado quando estado de contador se perde e impeça duas instâncias de
compartilharem a mesma faixa. Teste reinício e concorrência.

## Prática

Projete alocação de nonce para quatro workers e descreva o comportamento após
restauração de snapshot.
