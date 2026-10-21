# 01 — Definições e jogos de segurança

Definições como IND-CPA/IND-CCA e EUF-CMA formalizam o que um adversário pode
consultar e qual evento conta como vitória. Elas evitam argumentos vagos como
“parece aleatório” e permitem ligar uma construção a uma propriedade.

Uma prova é relativa ao modelo, hipótese e implementação ideal. Ela não cobre
chave em log, nonce repetido, parser ambíguo, endpoint comprometido ou canal
lateral fora do modelo. Engenharia mapeia cada lacuna a controles e testes.

## Prática

Para um envelope, escreva objetivo de confidencialidade, integridade e replay
como jogos informais com capacidade e condição de vitória.
