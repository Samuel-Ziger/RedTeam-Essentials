# Laboratório 01 — Contrato HTTP executável

## Pré-requisitos

- [Mapa das APIs](../00-mapa-das-apis.md)
- [Semântica HTTP](../01-http-semantica.md)
- [Estilos](../02-estilos-e-decisoes.md)
- [Design REST](../03-design-rest.md)
- [Representações](../04-representacoes-validacao.md)
- [Problem Details](../05-erros-problem-details.md)

## Missão

Modele uma coleção fictícia de itens sem persistência externa. O laboratório
avalia o contrato, não o framework. Você pode estender o Contract Lab.

## Requisitos

Implemente:

- POST /v1/items com 201, Location e schema fechado;
- GET /v1/items/{id} com ETag e cache privado;
- GET de coleção com limite 1–100 e ordem total;
- PATCH parcial com If-Match e 412;
- Problem Details RFC 9457 com code/requestId;
- 400/401/403/404/409/412/415/422 coerentes;
- request ID válido em toda resposta.

Defina máquina active → archived; archived não volta. Identidade ainda pode ser
sintética, mas o limite do laboratório precisa estar destacado.

## Casos obrigatórios

1. criação e leitura;
2. campo extra e title curto;
3. Content-Type errado;
4. identidade ausente;
5. update válido;
6. ETag antiga;
7. transição proibida;
8. GET com If-None-Match;
9. item inexistente;
10. request ID externo inválido substituído.

## Evidências

- proposta de uma página;
- tabela operação × método × status × idempotência;
- schemas Create/Patch/View;
- catálogo de problems;
- testes automatizados;
- captura textual das trocas HTTP.

## Gate

Outra pessoa deve prever método, status, corpo, headers e efeito de repetição
sem abrir o código. **Aprovado:** todos os casos passam, nenhum erro vaza stack e
PATCH concorrente não perde mudança.

## Extensão

Implemente negociação JSON/CSV somente na coleção e explique Vary/cache. A
extensão não compensa gate básico incompleto.

