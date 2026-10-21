# APIs e dados nas cinco linguagens

O protocolo HTTP e as garantias do banco não mudam quando a linguagem muda.
O que muda é a forma de representar tipos, controlar recursos, expressar
concorrência e integrar bibliotecas. Esta unidade conecta a formação do módulo
00 ao projeto integrador deste curso.

Os [clientes executáveis](exemplos/README.md) consultam a mesma Inventory API em
Python, Java, C, C# e JavaScript. Execute-os com a API local ativa e compare o
que cada runtime faz por você.

## A fronteira que todas precisam respeitar

Em qualquer stack, separe estas responsabilidades:

```text
entrada HTTP -> DTO -> caso de uso -> porta de repositório -> driver -> banco
                     <- modelo/erro <-                    <-
```

- DTO representa o contrato externo e pode mudar com a versão da API;
- modelo de domínio representa regras e não deve depender do framework;
- repositório oferece operações necessárias ao caso de uso;
- driver traduz tipos, parâmetros, transações e erros do servidor;
- pool administra conexões caras e limitadas.

Não retorne diretamente uma entidade do driver. Ela pode carregar tipos que não
são JSON, estado de sessão, lazy loading ou campos que o cliente não deveria
ver.

## Tipos atravessando fronteiras

| Conceito | HTTP/JSON | PostgreSQL | MongoDB | Regra prática |
|----------|-----------|------------|---------|---------------|
| ID | string | `uuid` | string/`ObjectId` | escolha um formato público estável |
| dinheiro | inteiro em centavos | `bigint` ou `numeric` | inteiro/Decimal128 | nunca use `float` binário |
| instante | RFC 3339 UTC | `timestamptz` | BSON Date UTC | converta somente na borda |
| ausência | campo omitido ou `null` | `NULL` | ausente ou `null` | defina as duas semânticas |
| versão | inteiro/ETag | coluna `version` | campo `version` | use compare-and-set |

O driver deve receber valores tipados como parâmetros. Converter tudo para
string elimina validação, prejudica índices e reintroduz injeção.

## Python

Python favorece composição simples, mas o Global Interpreter Lock não torna
transações nem objetos compartilhados automaticamente seguros.

Stack comum:

- FastAPI ou Django para HTTP;
- `psycopg`/SQLAlchemy para PostgreSQL;
- PyMongo/Motor para MongoDB;
- Pydantic para contratos, não para esconder regras de domínio.

### Unidade de trabalho

```python
def transfer(pool: ConnectionPool, source: UUID, target: UUID, cents: int) -> None:
    with pool.connection() as connection:
        with connection.transaction():
            debit(connection, source, cents)
            credit(connection, target, cents)
            append_outbox(connection, "money.transferred", source)
```

O contexto confirma no final e faz rollback quando uma exceção escapa. Não faça
chamada HTTP dentro dessa transação: o lock ficaria aberto durante uma operação
externa imprevisível.

Em aplicações assíncronas, use driver assíncrono ou execute o acesso bloqueante
em worker apropriado. Colocar `async def` ao redor de I/O bloqueante não o
transforma em assíncrono.

## Java

Java torna contratos e ciclos de vida explícitos. JDBC é a base; frameworks
como Spring Data reduzem repetição, mas não substituem o entendimento de SQL.

```java
if (cents <= 0) {
    throw new IllegalArgumentException("cents deve ser positivo");
}
String sql = "UPDATE account SET balance = balance - ? WHERE id = ? AND balance >= ?";
try (Connection connection = dataSource.getConnection()) {
    connection.setAutoCommit(false);
    try (PreparedStatement statement = connection.prepareStatement(sql)) {
        statement.setLong(1, cents);
        statement.setObject(2, accountId);
        statement.setLong(3, cents);
        if (statement.executeUpdate() != 1) {
            throw new IllegalStateException("saldo insuficiente ou conta ausente");
        }
    }
    connection.commit();
}
```

Em código de produção, faça rollback explícito no `catch`, traduza a exceção
para erro de aplicação e deixe o `try-with-resources` devolver a conexão ao
pool. O exemplo destaca três garantias: parâmetro preparado, atualização
atômica e verificação da cardinalidade alterada.

Ao usar JPA/Hibernate, monitore SQL gerado, lazy loading e N+1. Uma anotação de
transação define fronteira, mas não escolhe isolamento, idempotência ou índice
por você.

## C

C revela o protocolo e o custo de cada buffer. Para aplicações reais, use
`libpq` no PostgreSQL, MongoDB C Driver e `libcurl`; não implemente TLS ou parser
HTTP próprio.

```c
const char *values[2] = {sku, minimum_stock_text};
PGresult *result = PQexecParams(
    connection,
    "SELECT id, stock FROM product WHERE sku = $1 AND stock >= $2::integer",
    2,
    NULL,
    values,
    NULL,
    NULL,
    0
);
```

Verifique sempre:

- retorno de alocação e de cada chamada do driver;
- tamanho antes de copiar/formatar;
- ownership de cada ponteiro;
- `PQresultStatus` antes de ler linhas;
- `PQclear` e `PQfinish` em todos os caminhos;
- timeout e limite de resposta na rede.

O cliente C do curso abre um socket HTTP somente para `127.0.0.1`. Ele existe
para revelar request line, headers, `\r\n` e leitura parcial. Para HTTPS, proxy,
redirecionamento e produção, use uma biblioteca madura.

## C Sharp (.NET)

ASP.NET Core integra injeção de dependência, configuração, logging e pipeline
HTTP. Npgsql e MongoDB.Driver são os drivers comuns.

```csharp
await using var connection = await dataSource.OpenConnectionAsync(cancellationToken);
await using var transaction = await connection.BeginTransactionAsync(cancellationToken);
await using var command = connection.CreateCommand();
command.Transaction = transaction;
command.CommandText = """
    UPDATE product
    SET stock = stock + @delta,
        version = version + 1
    WHERE id = @id
      AND version = @expectedVersion
      AND stock + @delta >= 0
    """;
command.Parameters.AddWithValue("delta", delta);
command.Parameters.AddWithValue("id", id);
command.Parameters.AddWithValue("expectedVersion", expectedVersion);
if (await command.ExecuteNonQueryAsync(cancellationToken) != 1)
    throw new InvalidOperationException(
        "produto ausente, estoque insuficiente ou versão obsoleta"
    );
await transaction.CommitAsync(cancellationToken);
```

Propague `CancellationToken` do request até o driver. Cancelamento não equivale
a rollback depois de um commit: ele apenas permite interromper trabalho ainda
em andamento.

Reutilize `HttpClient` por meio de `IHttpClientFactory` ou instância de longa
duração. Criar um cliente por request pode esgotar sockets mesmo que cada
objeto seja descartado corretamente.

## JavaScript

No Node.js, uma thread de JavaScript coordena muitas operações de I/O. Trabalho
CPU-bound ainda bloqueia o event loop e deve ser dividido ou enviado a worker.

```javascript
const client = await pool.connect();
try {
  await client.query("BEGIN");
  const result = await client.query(
    `UPDATE product
        SET stock = stock + $1,
            version = version + 1
      WHERE id = $2
        AND version = $3
        AND stock + $1 >= 0
      RETURNING stock, version`,
    [delta, id, expectedVersion],
  );
  if (result.rowCount !== 1) {
    throw new Error(
      "produto ausente, estoque insuficiente ou versão obsoleta",
    );
  }
  await client.query("COMMIT");
} catch (error) {
  await client.query("ROLLBACK");
  throw error;
} finally {
  client.release();
}
```

A transação pertence a uma conexão. Não execute `BEGIN` em um `pool.query` e as
operações seguintes em outras conexões. Em MongoDB, passe a mesma sessão para
todas as operações da transação.

No navegador, CORS é uma política aplicada pelo user agent, não autenticação.
No servidor, valide origem quando necessário, mas sempre autentique e autorize
o principal.

## Concorrência comparada

| Stack | Modelo frequente | Perigo principal |
|-------|-----------------|------------------|
| Python | threads, processos, `asyncio` | bloquear o event loop |
| Java | pool de threads, futures, virtual threads | pool sem backpressure |
| C | threads/event loop explícitos | race, lifetime e buffer |
| C# | Tasks e `async`/`await` | bloquear com `.Result`/`.Wait()` |
| JavaScript | event loop, promises, workers | CPU bloquear o loop |

Em todas elas, o banco possui seu próprio limite. Se a API aceita 1.000 requests
concorrentes e o pool tem 20 conexões, 980 operações precisam aguardar, falhar
cedo ou sofrer backpressure. Abrir 1.000 conexões raramente é a resposta.

## Contrato primeiro, framework depois

Antes de escolher controller ou ORM, escreva:

1. recurso, método e URI;
2. request e response com exemplos;
3. invariantes e autorização;
4. status e Problem Details;
5. idempotência e regra de retry;
6. transação e consistência esperada;
7. limites, timeout e observabilidade;
8. testes de contrato independentes da implementação.

Depois implemente o mesmo contrato em uma segunda linguagem. Se a especificação
só pode ser entendida lendo o primeiro framework, ela ainda não é um contrato
suficiente.

## O algoritmo de um cliente robusto

Bibliotecas escondem framing e conexões, mas não decidem a política. Em qualquer
linguagem, um cliente confiável segue essencialmente esta sequência:

```text
validar entrada local
  -> construir URI codificando cada componente
  -> definir deadline e limite de resposta
  -> enviar request com Content-Type/Accept explícitos
  -> receber status e cabeçalhos
  -> rejeitar corpo acima do limite
  -> validar Content-Type
  -> ler/decodificar o corpo completamente
  -> separar sucesso de Problem Details
  -> validar schema da representação
  -> devolver valor tipado ou erro tipado
  -> liberar resposta, conexão, buffer e cancelamento
```

Erros de DNS, conexão, TLS, timeout, protocolo, status e schema são classes
diferentes. Transformar todos em “não encontrado” destrói diagnóstico e pode
levar o chamador a repetir uma operação que já confirmou.

Um timeout deve ser um **deadline total**, ou um conjunto consciente de limites
para conectar, enviar, receber cabeçalhos e consumir o corpo. Limitar apenas a
abertura da conexão ainda permite que um corpo lento ocupe recurso
indefinidamente.

## Tipos que parecem iguais, mas não são

### Inteiros e JSON

PostgreSQL `bigint`, Java `long`, C# `long` e C `int64_t` representam inteiros de
64 bits. O tipo `number` do JavaScript representa exatamente apenas inteiros até
`2^53 - 1`. Para IDs ou valores maiores, publique string decimal ou estabeleça
limite contratual verificável. Não permita que um identificador mude
silenciosamente ao atravessar JSON.

### Dinheiro

Escolha uma representação e preserve-a de ponta a ponta:

- centavos como inteiro, com moeda e faixa documentadas; ou
- decimal como string validada e tipo decimal no domínio/banco.

`0.1 + 0.2` não é argumento contra computação; é um lembrete de que ponto
flutuante binário não representa toda fração decimal exatamente.

### Tempo

Instante, data civil e duração são tipos diferentes:

- instante: RFC 3339 com offset, normalizado quando apropriado;
- data civil: `YYYY-MM-DD`, sem inventar meia-noite UTC;
- duração: unidade explícita ou tipo próprio;
- agenda local: inclui fuso e regra para horário inexistente/ambíguo.

Um sufixo `Z` afirma UTC. Não o acrescente a uma data local sem conversão.

### Ausente, `null` e vazio

Em PATCH, estes estados podem significar coisas diferentes:

| Entrada | Semântica possível |
|---------|--------------------|
| campo omitido | não alterar |
| `null` | remover valor opcional |
| `""` | texto vazio, se permitido |
| `[]` | substituir por coleção vazia |

Python `None`, Java `null`/`Optional`, C ponteiro nulo, C# `null` e JavaScript
`null`/`undefined` não são automaticamente equivalentes. O DTO de entrada deve
preservar a distinção exigida pelo contrato.

## Retry por semântica, não por exceção

| Operação | Retry automático? | Condição |
|----------|-------------------|----------|
| `GET` de representação | geralmente sim | deadline, backoff e limite |
| `PUT` determinístico | possível | mesma intenção e precondições |
| `DELETE` | possível | contrato define estado final e respostas |
| `POST` de criação | não por padrão | chave de idempotência persistida |
| ajuste de estoque | somente condicionado | operation ID único e resultado recuperável |
| erro `400`/`422` | não | corrigir entrada |
| erro `401`/`403` | não cegamente | corrigir identidade/permissão |
| erro `409`/`412` | depende | reler estado e tomar nova decisão |
| `429`/`503` | possível | respeitar `Retry-After`, jitter e orçamento |

Se a conexão cai depois do envio, o cliente pode não saber se houve commit.
Essa **falha ambígua** não é resolvida repetindo qualquer POST. A operação
precisa de identidade estável, armazenamento do resultado e regra de conflito.

Backoff exponencial sem limite apenas adia a saturação. Combine:

- número máximo de tentativas;
- deadline global;
- jitter;
- respeito ao servidor;
- circuit breaker somente quando o padrão de falha justificar;
- métrica que distingue chamada original de retry.

## Paginação e consumo incremental

Um cliente não deve carregar uma coleção potencialmente ilimitada. Para cada
página:

1. valide itens e cursor antes de anexar;
2. rejeite cursor repetido para evitar loop infinito;
3. aplique limite total de itens/páginas;
4. propague cancelamento entre iterações;
5. decida se falha parcial descarta ou preserva os itens anteriores;
6. não interprete cursor opaco nem o registre se ele carregar dado sensível.

Geradores Python, streams Java, `IAsyncEnumerable<T>` em C#, iteradores em C e
async iterators JavaScript podem expressar consumo incremental. Ainda assim, a
conexão HTTP deve ser fechada se o consumidor abandonar a iteração.

## Drivers de banco: a conexão é parte do contrato

| Questão | Regra |
|---------|-------|
| Quem abre? | pool/data source configurado no composition root |
| Quem toma emprestada? | unidade de trabalho ou caso de uso |
| Quem inicia transação? | camada que conhece a atomicidade do caso de uso |
| Quem confirma? | mesma unidade que iniciou, depois de todos os efeitos locais |
| Quem devolve? | `finally`, contexto, try-with-resources ou descarte assíncrono |
| O que não fazer? | guardar conexão em singleton de domínio ou cruzar requests |

Uma transação pertence a uma conexão. Isto vale para JDBC, Npgsql, psycopg,
node-postgres, libpq e drivers MongoDB com session. Uma abstração que esconde
essa afinidade pode executar `BEGIN`, updates e `COMMIT` em conexões diferentes.

Configure o pool a partir da capacidade do banco e do tempo de serviço, não do
número máximo de requests HTTP. Meça:

- conexões em uso, ociosas e limite;
- tempo aguardando conexão;
- duração de transação;
- queries e locks longos;
- timeouts e cancelamentos;
- taxa de rollback.

Se todos os workers aguardam o pool, a aplicação está saturada antes de o banco
necessariamente estar. Backpressure e falha precoce podem proteger a latência.

## Cancelamento e resultado desconhecido

Cancelar no cliente não desfaz automaticamente o servidor. Existem pelo menos
três momentos:

1. antes de enviar: nenhum efeito remoto;
2. durante execução: o servidor pode cancelar, continuar ou já ter alterado;
3. depois do commit e antes da resposta: efeito confirmado, resultado perdido.

Propague cancelamento quando o driver suportar, mas projete idempotência para o
terceiro caso. Nunca prometa “cancelado” apenas porque uma `Task`, `Future` ou
`AbortController` deixou de esperar.

## Matriz de testes entre linguagens

Execute a mesma fixture contra cada cliente:

| Cenário | Evidência esperada |
|---------|--------------------|
| resposta `200` válida | modelo tipado equivalente |
| Problem Details `404` | erro de domínio, não parse como sucesso |
| `Content-Type` inesperado | rejeição explícita |
| JSON truncado | erro de protocolo/schema |
| corpo acima do limite | interrupção segura |
| timeout antes de headers | erro transitório classificado |
| inteiro acima de `2^53-1` | sem arredondamento no JavaScript |
| timestamp com offset | mesmo instante após parse |
| Unicode fora do BMP | contagem conforme contrato |
| cursor repetido | loop interrompido |

Não é necessário que todas as linguagens usem o mesmo nome de classe. Elas
precisam preservar a mesma semântica observável.

## Quando implementar o servidor em outra linguagem

Reescrever a API inteira cinco vezes ensina menos do que parece: muito tempo vai
para configuração de frameworks. Primeiro implemente uma fatia vertical pequena
em uma segunda stack:

```text
GET /health/ready
POST /products com idempotência
GET /products/{id} com ETag
PATCH /products/{id} com If-Match
```

Mantenha o mesmo OpenAPI e a mesma suíte externa. Compare:

- lifecycle da aplicação e do pool;
- tradução de erros;
- validação de DTOs;
- fronteira transacional;
- cancelamento;
- geração de OpenAPI;
- integração de logs/traces;
- consumo de memória e comportamento sob saturação.

A conclusão correta não é “linguagem X é melhor”. É quais garantias exigem
menos código acidental naquela equipe, runtime e operação.

## Exercícios

1. Execute os cinco clientes e capture a requisição no Nginx. Compare headers.
2. Adicione `X-Request-ID` em cada linguagem e localize o mesmo valor no log.
3. Implemente Problem Details tipado em Python, Java, C# e JavaScript.
4. Faça o cliente C separar status line, headers e body sem assumir um único
   `recv`.
5. Implemente um repositório da Inventory API em uma segunda stack.
6. Meça 50 chamadas sequenciais e concorrentes sem aumentar o pool.
7. Documente como cada runtime cancela, fecha e reutiliza conexões.

Critério de aceite: os clientes tratam timeout e status não 2xx; nenhum exemplo
concatena entrada em SQL; e você consegue explicar quem possui cada conexão,
buffer, task e transação.
