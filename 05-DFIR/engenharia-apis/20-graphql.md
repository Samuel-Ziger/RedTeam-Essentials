# 20 — GraphQL

GraphQL publica um schema tipado e permite ao cliente selecionar campos e
relações. Resolve necessidades de projeção, mas transfere parte do custo para
resolvers, autorização por campo, controle de complexidade e cache.

## Objetivos

- modelar schema, queries, mutations e subscriptions;
- evitar N+1 com batching;
- aplicar autorização em objetos e propriedades;
- limitar custo, profundidade e cardinalidade;
- entender nullability, erros parciais e evolução.

## 1. Schema e execução

~~~graphql
type Item {
  id: ID!
  title: String!
  owner: User!
}

type Query {
  item(id: ID!): Item
}

type Mutation {
  updateItem(input: UpdateItemInput!): UpdateItemPayload!
}
~~~

Schema é contrato. Resolver obtém dados de cada campo. A query define shape da
resposta; isso reduz overfetching, mas uma consulta curta pode gerar trabalho
grande por listas e relações.

A edição oficial de setembro de 2025 é a release estável mais recente da
especificação consultada; o working draft de 2026 não deve ser tratado
automaticamente como baseline de produção.

## 2. N+1 e batching

Listar 100 itens e buscar owner por item gera 101 chamadas. DataLoader agrupa
IDs e usa cache por requisição:

~~~text
items resolver -> 100 owner IDs
loader -> SELECT users WHERE id IN (...)
~~~

O cache não deve atravessar identidade/tenant sem chave correta. Batching precisa
preservar ordem e ausência. Meça queries por operação.

## 3. Autorização

Autorização ocorre em:

- operação/mutation;
- objeto retornado;
- campo sensível;
- conexão/lista;
- argumento e transição.

Filtrar apenas no resolver raiz falha quando o mesmo objeto aparece por outra
relação. Policy central pode ser chamada pelos resolvers. Evite descobrir campo
se sua existência já é sensível.

## 4. Custo e abuso

Limite:

- tamanho do documento;
- profundidade;
- quantidade de aliases e campos;
- page size de toda conexão;
- custo ponderado de resolvers;
- tempo e concorrência.

Profundidade sozinha não captura aliases repetidos. Calcule custo antes da
execução e também imponha limites em dados. Persisted operations permitem
allowlist e hash conhecido, especialmente em clientes próprios; ainda exigem
autorização.

## 5. Null e erros

Campos nullable podem ser null por ausência, negação ou erro. Em campo non-null,
erro propaga null até o próximo pai nullable. Um erro em parte da query pode
coexistir com data parcial.

Cliente precisa decidir se aceita parcial. extensions pode levar code e request
ID; não exponha stack. HTTP costuma retornar 200 quando execução GraphQL contém
erros de campo, portanto métricas precisam inspecionar resultado GraphQL, não só
status.

## 6. Mutations e idempotência

Mutation deve expressar intenção, input e payload. Use clientMutationId ou
idempotency key quando repetição puder duplicar efeito. Concorrência pode usar
expectedVersion. Não coloque dez ações opcionais numa mutation genérica.

Upload, download e operações longas podem ser melhores em HTTP dedicado/job,
com GraphQL retornando link/estado.

## 7. Evolução e cache

Adicionar tipo/campo é aditivo; remover exige depreciação e telemetria de uso de
campo. Mudar nullability é breaking em uma direção ou outra. Observe queries
persistidas e clientes antes de remover.

Cache HTTP tradicional é menos direto porque POST e documentos variados
compartilham URL. Use normalized client cache, persisted GET quando apropriado e
cache de resolver com identidade completa.

## Falhas comuns

| Falha | Resultado | Correção |
|---|---|---|
| resolver por linha | N+1 | batching |
| auth só na Query | campo/relação vaza | policy por objeto/campo |
| limite só de profundidade | aliases explodem custo | análise ponderada |
| olhar só HTTP 200 | erro invisível | métricas GraphQL |
| remover campo sem uso | cliente quebra | deprecation + telemetry |

## Exercícios

### Nível 1 — schema

Modele items, owners e mutation versionada. **Aceite:** nullability, paginação e
errors estão definidos.

### Nível 2 — N+1

Conte queries antes/depois de DataLoader. **Aceite:** resultado é igual e número
de queries não cresce linearmente.

### Nível 3 — custo/autorização

Teste aliases, profundidade e campo sensível. **Aceite:** custo é rejeitado antes
da execução e objeto autorizado não implica campo autorizado.

## Checklist

- [ ] Schema expressa domínio e nullability.
- [ ] Relações usam batching medido.
- [ ] Autorização alcança campos e caminhos alternativos.
- [ ] Custo limita aliases, listas e resolvers.
- [ ] Erros parciais são observáveis.
- [ ] Depreciação usa telemetria de campos.

