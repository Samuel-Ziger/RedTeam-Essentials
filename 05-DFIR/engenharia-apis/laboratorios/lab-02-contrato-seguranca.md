# Laboratório 02 — Contrato evolutivo e seguro

## Pré-requisitos

- [Laboratório 01](lab-01-contrato-http.md)
- [Coleções](../06-colecoes-paginacao.md)
- [Idempotência e cache](../07-idempotencia-cache.md)
- [Evolução](../08-versionamento-evolucao.md)
- [Autenticação](../09-autenticacao.md)
- [Autorização](../10-autorizacao.md)
- [Segurança](../11-seguranca-owasp.md)
- [OpenAPI](../12-openapi-contract-first.md)

## Missão

Transforme a API em contrato publicável com dois tenants e políticas negativas
demonstráveis. A autenticação continua sintética local; autorização deve ser real
no caso de uso.

## Requisitos

- cursor opaco, assinado, versionado e ligado ao filtro;
- POST idempotente com digest canônico;
- mesma chave/corpo reproduz resultado; corpo diferente retorna 409;
- isolamento de leitura, escrita, coleção, cache e eventos;
- matriz reader/writer × operação × estado;
- limites de corpo, lista, cursor e frequência simulada;
- OpenAPI validado com examples, problems, headers e security;
- diff que detecta ao menos uma mudança incompatível;
- threat model baseado no OWASP API Security 2023.

## Casos obrigatórios

Teste cursor alterado, cursor de outro filtro, chave divergente, item do tenant B
usado por A, campo server-only, corpo/lote excessivo, resposta de erro sem segredo
e enum novo consumido por cliente antigo.

## Evidências

- OpenAPI-fonte e relatório de validação;
- matriz de autorização e testes gerados dela;
- risco → controle → teste → sinal → owner;
- ADR de estratégia de versão;
- plano expand/contract de um campo;
- resultado do breaking diff.

## Gate

Nenhum ID conhecido atravessa tenant, cursor adulterado nunca vira consulta
livre, chave idempotente não representa dois comandos e implementação/contrato
concordam. Mudança breaking falha antes de publicar.

## Extensão

Adicione uma fake de validação JWT completa. Não implemente servidor OAuth e não
use token real.

