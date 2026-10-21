# Design de APIs, HTTP e evolução de contratos

Design de API é design de um compromisso entre produtor e consumidores. Uma
rota elegante não compensa semântica ambígua; um schema completo não compensa
paginar de forma instável. O objetivo é tornar o comportamento previsível em
sucesso, concorrência, retry, evolução e falha.

## Objetivos de aprendizagem

Ao terminar, você deverá conseguir:

- escolher entre recursos REST, RPC e mensagens assíncronas;
- aplicar métodos, status, cache e precondições HTTP corretamente;
- projetar filtros, ordenação e paginação determinísticos;
- definir idempotência sob retry e concorrência;
- evoluir contratos com política de compatibilidade e depreciação;
- transformar decisões em um contrato OpenAPI testável.

## Comece pelo caso de uso, não pela rota

Antes de escrever `/v1/...`, responda:

1. quem chama e em nome de quem;
2. qual intenção ou informação precisa ser representada;
3. quais invariantes devem sobreviver à concorrência;
4. qual consistência o consumidor observa;
5. como o chamador repete a operação após timeout;
6. como o contrato poderá evoluir;
7. quais dados são sensíveis e quanto tempo existem.

Uma descrição útil é: “um operador autorizado cadastra um produto com SKU
único no próprio tenant; repetir a mesma intenção não cria outro produto”.

## REST, RPC e eventos

Não existe um estilo universal. Escolha pela semântica, interoperabilidade e
necessidade operacional.

| Estilo | Modelo | Bom encaixe | Cuidado principal |
|---|---|---|---|
| REST/HTTP | recursos e representações | CRUD, integração web, cache | não esconder ações em verbos genéricos |
| RPC | procedimentos tipados | chamadas internas e comandos ricos | acoplamento a métodos e tooling |
| evento/fila | fatos e processamento assíncrono | desacoplamento e fan-out | entrega, ordenação e observabilidade |
| webhook | callback HTTP orientado a evento | notificar sistema externo | assinatura, retry e endpoint lento |

Uma solução pode combinar estilos. O cliente cria uma exportação via HTTP,
recebe `202`, um worker processa a mensagem e um webhook notifica conclusão.
Isso não elimina contratos: cada fronteira possui o seu.

### Recurso ou comando?

CRUD direto funciona para estado simples:

```text
GET    /api/v1/products
POST   /api/v1/products
GET    /api/v1/products/{productId}
PATCH  /api/v1/products/{productId}
DELETE /api/v1/products/{productId}
```

Uma movimentação de estoque é melhor como recurso imutável do que como
`PATCH {"stock": 8}`, pois preserva intenção e auditoria:

```text
POST /api/v1/products/{productId}/stock-movements
GET  /api/v1/products/{productId}/stock-movements/{movementId}
```

Um comando explícito também pode ser adequado:

```text
POST /api/v1/orders/{orderId}:cancel
```

O ponto não é evitar verbos a qualquer custo; é impedir que uma atualização
genérica contorne transições e regras do domínio.

## Identificadores e URLs

- use identificador opaco e estável; não faça o cliente interpretar seus bits;
- não exponha segredo ou dado pessoal na URL;
- mantenha nomes previsíveis e consistentes;
- evite hierarquias que simulam toda a estrutura do banco;
- limite profundidade: sub-recursos expressam relação, não posse absoluta;
- trate URLs retornadas como opacas quando o cliente puder apenas segui-las.

IDs sequenciais não substituem autorização. UUIDs também não: dificuldade
de adivinhar um ID não concede permissão para lê-lo.

## Semântica dos métodos

| Método | Seguro | Idempotente | Uso comum |
|---|---:|---:|---|
| GET | sim | sim | obter representação |
| HEAD | sim | sim | obter os headers do GET |
| OPTIONS | sim | sim | capacidades/opções de comunicação |
| PUT | não | sim | criar/substituir estado no URI conhecido |
| DELETE | não | sim | solicitar remoção |
| POST | não | não por padrão | criar subordinado ou executar comando |
| PATCH | não | depende do formato | alterar parcialmente |

**Seguro** significa que a semântica pretendida não modifica estado do
recurso. Logs e métricas podem mudar. **Idempotente** significa que repetir a
mesma intenção produz o mesmo efeito pretendido; respostas podem diferir.

Um `DELETE` repetido pode retornar `204` na primeira vez e `404` depois sem
deixar de ser idempotente. Um `PATCH` que define `name` tende a ser idempotente;
um patch que incrementa `stock` não é.

## Status como parte do contrato

| Status | Uso contratual |
|---|---|
| 200 | sucesso com representação |
| 201 | recurso criado; normalmente acompanhado de `Location` |
| 202 | aceito para processamento ainda não concluído |
| 204 | sucesso sem body |
| 304 | representação em cache ainda válida |
| 400 | sintaxe ou framing inválido |
| 401 | credencial ausente/inválida; pode incluir `WWW-Authenticate` |
| 403 | identidade conhecida sem permissão |
| 404 | recurso ausente ou deliberadamente ocultado |
| 405 | método não permitido; inclua `Allow` |
| 409 | conflito com o estado atual ou unicidade |
| 412 | precondição como `If-Match` falhou |
| 415 | media type recebido não suportado |
| 422 | conteúdo entendido, mas semanticamente inválido |
| 428 | servidor exige requisição condicional |
| 429 | limite excedido; `Retry-After` quando aplicável |
| 500 | falha não prevista |
| 502 | gateway recebeu resposta inválida do upstream |
| 503 | serviço/dependência temporariamente indisponível |
| 504 | gateway excedeu o tempo do upstream |

Evite `200` com `{"success": false}`: intermediários, SDKs e métricas deixam
de compreender o resultado. Não use `500` para rejeição prevista do domínio.

## Erros com Problem Details

Uma resposta consistente pode usar `application/problem+json`:

```http
HTTP/1.1 409 Conflict
Content-Type: application/problem+json

{
  "type": "https://api.example.test/problems/duplicate-sku",
  "title": "SKU already exists",
  "status": 409,
  "detail": "The supplied SKU is already registered.",
  "instance": "/api/v1/products",
  "requestId": "3bb0a764bd9a",
  "errors": [{"field":"sku","code":"not_unique"}]
}
```

Clientes decidem por `type`, `status` e códigos estruturados, nunca analisando
o texto de `detail`. Não inclua SQL, stack trace, host interno ou existência de
objeto que a política decidiu ocultar.

## Representações e compatibilidade

Decida e documente:

- nomes e tipos dos campos;
- unidades (`priceCents`, não um `price` ambíguo);
- timezone e formato de data;
- diferença entre ausente, `null`, zero e vazio;
- enumerações abertas ou fechadas;
- precisão decimal;
- política para campos desconhecidos;
- máximo de coleções e strings.

Dinheiro não deve depender de ponto flutuante binário. Use inteiro na menor
unidade quando o domínio permitir ou tipo decimal com precisão definida.

## Filtros, projeção e ordenação

```http
GET /api/v1/products?category=books&sort=-createdAt,id&fields=id,name,priceCents
```

Todo campo e operador deve pertencer a uma allowlist. Defina:

- se filtros diferentes usam `AND` ou `OR`;
- como valores repetidos funcionam;
- se busca diferencia acentos ou caixa;
- quais combinações possuem índice;
- limite de complexidade e quantidade de filtros;
- desempate único e obrigatório na ordenação.

Nunca traduza diretamente um objeto do cliente para SQL, MongoDB ou nome de
campo. O servidor compila o DTO permitido para uma consulta parametrizada.

## Paginação correta

### Offset/limit

```http
GET /api/v1/products?limit=20&offset=40
```

É simples e permite saltar para uma página, mas offsets altos podem custar caro.
Inserções e remoções antes do offset causam repetição ou omissão.

### Cursor/keyset

```http
GET /api/v1/products?limit=20&after=eyJjcmVhdGVkQXQiOiIuLi4iLCJpZCI6Ii4uLiJ9
```

Para ordenação `(created_at DESC, id DESC)`, a próxima consulta equivale a:

```sql
SELECT id, name, created_at
FROM product
WHERE tenant_id = :tenant_id
  AND (created_at, id) < (:cursor_created_at, :cursor_id)
ORDER BY created_at DESC, id DESC
LIMIT :limit_plus_one;
```

Busque `limit + 1` para saber se existe próxima página e devolva apenas
`limit`. O cursor deve ser opaco para o consumidor, protegido contra alteração
quando isso importa e vinculado aos filtros/ordenação relevantes.

Um cursor não congela automaticamente o conjunto. Se a promessa for snapshot,
inclua uma revisão/limite temporal ou use mecanismo de snapshot do armazenamento
com custo e expiração documentados.

### Invariantes de paginação

- `1 <= limit <= limite_máximo`;
- ordenação total inclui chave única;
- cursor incompatível ou expirado falha de forma definida;
- `next` existe apenas se outra página foi comprovada;
- filtro/autorização não mudam silenciosamente entre páginas;
- dados de outro tenant nunca entram no cursor nem no resultado.

## Idempotência para comandos

Uma chave de idempotência transforma retries da mesma intenção em uma única
operação lógica. Defina escopo como `(tenant, operação, chave)` e associe a um
hash canônico da entrada relevante.

Fluxo concorrente:

```text
ausente -> processing -> completed
                    \-> failed_retryable ou failed_final
```

1. reserve a chave com constraint única;
2. grave hash, estado e expiração;
3. execute mudança e resultado na transação adequada;
4. retry com chave e hash iguais recebe resultado equivalente;
5. chave igual com hash diferente recebe `409`;
6. concorrente que encontra `processing` aguarda com limite ou recebe resposta
   documentada;
7. limpeza respeita o maior intervalo realista de retry.

Não use request ID como chave: cada tentativa pode possuir novo request ID,
enquanto a intenção idempotente permanece a mesma.

### O que entra no hash

Inclua campos semanticamente relevantes depois de canonicalização definida.
Não dependa da ordem textual de chaves JSON. Identidade/tenant e versão do
contrato pertencem ao escopo mesmo que não estejam no body.

## Concorrência otimista com ETag

Ao ler:

```http
HTTP/1.1 200 OK
ETag: "product-42-v7"
```

Ao alterar:

```http
PATCH /api/v1/products/42 HTTP/1.1
If-Match: "product-42-v7"
Content-Type: application/merge-patch+json

{"name":"Novo nome"}
```

Se a versão atual for outra, retorne `412 Precondition Failed`. Uma atualização
atômica pode ser:

```sql
UPDATE product
SET name = :name, version = version + 1
WHERE id = :id AND version = :expected_version
RETURNING id, name, version;
```

Zero linhas significa ausência ou conflito; faça a distinção conforme a
política de exposição. `If-None-Match` também permite cache/revalidação e
criação condicional em contratos que a suportam.

## Operações assíncronas

Se a tarefa não termina no tempo normal de uma chamada, exponha um recurso de
operação:

```http
HTTP/1.1 202 Accepted
Location: /api/v1/operations/op-123
Retry-After: 2

{"id":"op-123","status":"pending"}
```

O recurso deve definir estados, progresso confiável quando existir, resultado,
erro final, expiração e possibilidade de cancelamento. `202` significa aceito,
não concluído.

## Versionamento e evolução

Estratégias comuns:

- versão no path: `/api/v1/products`;
- media type/header negociado;
- endpoint estável com evolução compatível;
- nova operação/recurso para semântica realmente nova.

Escolha uma política e aplique-a. A versão no path é visível e simples, mas
não elimina a necessidade de evoluir `v1` com compatibilidade.

### Matriz de mudanças

| Mudança | Risco padrão | Condição para ser segura |
|---|---|---|
| adicionar campo opcional na resposta | baixo | clientes toleram campos extras |
| adicionar campo opcional no request | baixo | default e ausência bem definidos |
| tornar campo opcional obrigatório | breaking | nova versão/migração |
| remover ou renomear campo | breaking | depreciação e nova versão |
| adicionar valor de enum | variável | enum foi declarado aberto |
| reduzir limite máximo | potencialmente breaking | consumidores medidos e migrados |
| mudar unidade ou significado | breaking | novo campo/versão |
| adicionar novo status de erro | variável | contrato permite e SDK trata classe |
| corrigir ordenação instável | observável | comunicar e testar consumidores |

Compatibilidade depende do que consumidores realmente fazem, não apenas do
schema. Telemetria de uso e testes de consumidor reduzem a incerteza.

### Depreciação responsável

1. publique substituto e guia de migração;
2. anuncie data e janela compatíveis com o acordo do produto;
3. marque contrato/documentação e, quando adotado, headers de depreciação;
4. meça consumidores restantes sem registrar segredos;
5. contate donos e teste migração;
6. remova somente após o critério definido.

## OpenAPI como artefato executável

Um fragmento mínimo:

```yaml
paths:
  /api/v1/products/{productId}:
    get:
      operationId: getProduct
      parameters:
        - in: path
          name: productId
          required: true
          schema: { type: string, format: uuid }
      responses:
        "200":
          description: Product found
          headers:
            ETag: { schema: { type: string } }
          content:
            application/json:
              schema: { $ref: "#/components/schemas/Product" }
        "404":
          $ref: "#/components/responses/NotFound"
```

O contrato completo deve declarar autenticação, parâmetros, limites, formatos,
respostas, erros, exemplos, headers e depreciação. No CI:

- valide sintaxe e regras de lint;
- detecte mudanças breaking contra a versão publicada;
- teste que a implementação produz respostas conformes;
- gere SDK apenas quando a qualidade do contrato for suficiente;
- execute exemplos, se o tooling permitir.

Documentação gerada não substitui semântica de domínio, fluxos completos e
limites operacionais.

## Anti-padrões frequentes

- `POST /execute` para toda operação sem semântica documentada;
- status `200` para todos os resultados;
- cursor que é apenas um offset codificado em Base64;
- `sort=<qualquer texto>` interpolado na consulta;
- paginação sem desempate único;
- chave idempotente guardada só em memória;
- versionar cedo e manter várias cópias sem política de retirada;
- tratar “adicionar campo” como seguro sem conhecer consumidores;
- evento usado como comando, sem dono claro da decisão.

## Exercícios

1. Desenhe uma API de empréstimos de biblioteca com recursos e comandos.
2. Justifique REST, RPC ou evento para cinco interações desse domínio.
3. Defina Problem Details para validação, conflito, auth e indisponibilidade.
4. Implemente cursor estável e simule inserção entre duas páginas.
5. Especifique idempotência para criação, inclusive duas chamadas simultâneas.
6. Modele uma alteração com ETag e prove que update perdido é rejeitado.
7. Classifique vinte mudanças de contrato como compatíveis ou breaking.
8. Escreva a política de depreciação de `v1` para `v2`.
9. Modele uma exportação assíncrona com recurso de operação.

## Critérios de conclusão

- todos os endpoints possuem intenção e semântica de retry descritas;
- erros têm status e códigos estruturados estáveis;
- toda lista tem limite, ordem total e comportamento concorrente definido;
- comandos repetíveis possuem estratégia de idempotência durável;
- updates concorrentes não sobrescrevem silenciosamente;
- o contrato especifica auth, sucesso, erro, headers e limites;
- uma verificação automática detecta mudança incompatível;
- a depreciação tem comunicação, telemetria, prazo e critério de retirada.

## Checklist de revisão

- [ ] Escolhi o estilo de integração pela semântica.
- [ ] Apliquei corretamente segurança e idempotência dos métodos HTTP.
- [ ] Documentei ausência, `null`, unidades, datas e enums.
- [ ] Paginação e ordenação são determinísticas.
- [ ] Idempotência cobre concorrência e body diferente.
- [ ] OpenAPI e política de compatibilidade entram no CI.
