# Laboratório 02 — WAF, CRS e falso positivo

## Cenário

Uma rota de documentação recebe exemplos de código e aciona uma regra genérica.
Ao mesmo tempo, a rota de login precisa conservar proteção normal.

## Red

Crie quatro casos totalmente locais: documento simples, documento com exemplo
de código inofensivo, corpo acima do contrato e requisição com tipo incorreto.
Não procure formas de escapar da regra; demonstre apenas a colisão legítima.

## Blue

Registre ID, score, campo e rota. Proponha exclusão somente para o parâmetro de
exemplo na rota e método corretos. Mantenha limite de tamanho e tipo.

## Purple

Monte regressão com os quatro casos e um negativo relacionado. Rode antes,
depois e após rollback. A entrega deve explicar por que desabilitar a regra ou
permitir toda a rota seria excessivo.
