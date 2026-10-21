# Transações e concorrência

Código que funciona com uma requisição pode quebrar com duas. Concorrência
introduz interleavings: ambas leem um estado válido, tomam decisões localmente
corretas e, juntas, violam uma regra. A transação define quais operações formam
uma unidade; o nível de isolamento e as constraints definem o que pode ser
observado ou confirmado em paralelo.

Os detalhes deste capítulo descrevem PostgreSQL. Outros SGBDs usam nomes
semelhantes com garantias diferentes; nunca transporte uma tabela de isolamento
sem consultar a documentação do produto e versão.

## Objetivos

Ao concluir, você deverá conseguir:

- explicar ACID sem atribuir ao banco regras que não foram declaradas;
- escolher um limite transacional curto e correto;
- reconhecer snapshots MVCC e o custo de transações longas;
- reproduzir non-repeatable read, lost update, write skew e deadlock;
- escolher entre operação atômica, constraint, lock e versão otimista;
- implementar retry limitado da transação inteira;
- dimensionar e observar um pool de conexões;
- manter efeitos externos fora da janela transacional usando outbox.

## 1. ACID com precisão

- **Atomicidade:** as mudanças da transação confirmam juntas ou são desfeitas.
- **Consistência:** se as regras declaradas e a lógica estiverem corretas, uma
  transação válida leva de um estado válido a outro.
- **Isolamento:** execuções concorrentes observam comportamento definido pelo
  nível escolhido, possivelmente com aborts.
- **Durabilidade:** depois do commit, os dados sobrevivem às falhas cobertas
  pela configuração de WAL, armazenamento e replicação.

O “C” não inventa regras. Se `stock` aceita número negativo, o banco pode
preservar atomicamente um estado de negócio inválido. ACID tampouco significa
que uma transação abrange automaticamente PostgreSQL, MongoDB, fila e email.

### Autocommit

Drivers normalmente iniciam/encerram transações implicitamente. Em autocommit,
cada statement é uma transação própria. Dois comandos consecutivos não são uma
unidade apenas por usarem a mesma conexão:

```text
UPDATE product ...;       -- commit 1
INSERT stock_movement ... -- commit 2; pode falhar
```

Conheça o comportamento do driver, feche a transação em todos os caminhos e
nunca devolva ao pool uma conexão “idle in transaction”.

## 2. Defina o limite pela invariante

Uma venda precisa reduzir o estoque e registrar o movimento juntos. Uma forma
set-based evita registrar movimento quando o saldo é insuficiente:

```sql
BEGIN;

WITH changed AS (
    UPDATE product
    SET stock = stock - $2,
        version = version + 1,
        updated_at = now()
    WHERE id = $1
      AND stock >= $2
    RETURNING id, stock, version
)
INSERT INTO stock_movement (
    id,
    product_id,
    delta,
    reason,
    resulting_stock,
    resulting_version,
    created_at
)
SELECT $3, id, -$2, 'sale', stock, version, now()
FROM changed
RETURNING product_id, delta, resulting_stock, resulting_version;

-- A aplicação exige exatamente uma linha antes de confirmar.
COMMIT;
```

Parâmetros: `$1` produto, `$2` quantidade positiva e `$3` identificador
único do movimento. Se o resultado vier vazio, pode ser produto inexistente ou
estoque insuficiente; consulte/mapeie conforme o contrato e faça rollback se
houver outros efeitos na transação.

Invariantes:

- `CHECK (stock >= 0)` é a última barreira;
- `stock >= $2` torna a decisão e escrita uma operação;
- movimento nasce apenas da linha realmente alterada;
- ambos confirmam no mesmo commit;
- ID único ajuda a impedir repetição do mesmo comando.

### Transação curta

Dentro de uma transação, evite:

- chamada HTTP, email ou espera em fila;
- interação humana;
- processamento pesado que poderia ocorrer antes;
- arquivo ou log remoto como requisito do commit;
- retry com sleep mantendo locks.

Valide formato e calcule dados determinísticos antes de abrir a transação.
Dentro dela, leia o necessário, aplique a decisão, registre a outbox e confirme.

## 3. MVCC: versões e snapshots

PostgreSQL usa Multi-Version Concurrency Control (MVCC). Um `UPDATE` cria uma
nova versão de linha; a antiga permanece enquanto algum snapshot puder
precisar dela. Cada versão carrega metadados transacionais usados para decidir
visibilidade.

Consequências:

- leitores normalmente não bloqueiam escritores e vice-versa;
- uma consulta vê apenas versões permitidas pelo snapshot;
- atualizar ainda adquire lock na linha;
- versões mortas ocupam espaço até vacuum poder removê-las;
- transações longas retêm versões antigas e podem causar bloat;
- vacuum não é backup e não “apaga a tabela”; ele mantém saúde do MVCC.

`VACUUM` comum e autovacuum são parte da operação normal. `VACUUM FULL`
reescreve e adquire lock muito mais forte; não é manutenção rotineira sem
planejamento.

### Snapshot por statement ou transação

Em `READ COMMITTED`, cada statement recebe um snapshot novo. Em
`REPEATABLE READ`, os statements da transação compartilham uma visão estável
(a partir da primeira consulta relevante). Em `SERIALIZABLE`, PostgreSQL soma
detecção de dependências para impedir resultados não serializáveis.

## 4. Anomalias de concorrência

### Dirty read

Uma transação lê escrita ainda não confirmada de outra e depois esta desfaz.
PostgreSQL não permite dirty read, nem mesmo quando solicitado
`READ UNCOMMITTED` (que é tratado como `READ COMMITTED`).

### Non-repeatable read

A mesma linha retorna valores diferentes em duas consultas porque outra
transação confirmou uma atualização entre elas. É possível em `READ COMMITTED`.

### Phantom

Repetir um predicado retorna conjunto diferente por inserção/remoção concorrente.
É possível em `READ COMMITTED`. O `REPEATABLE READ` do PostgreSQL mantém
snapshot e impede esse phantom de leitura, embora ainda permita anomalias de
serialização como write skew.

### Lost update

Duas aplicações leem `stock = 10`, calculam 9 e ambas escrevem 9. Uma redução
se perde. Evite read-modify-write na aplicação:

```sql
UPDATE product
SET stock = stock - 1
WHERE id = $1
  AND stock >= 1
RETURNING stock;
```

Outra opção é lock pessimista ou `version` otimista, conforme o fluxo.

### Write skew

Duas transações leem o mesmo conjunto e alteram linhas diferentes, mantendo
cada regra local, mas quebrando uma invariante conjunta. Exemplo: dois médicos
estão de plantão; cada transação vê o outro disponível e retira uma pessoa,
deixando zero. Locks nas linhas lidas, constraint/modelagem diferente ou
`SERIALIZABLE` com retry podem resolver.

### Read skew

Uma transação lê partes de um estado em momentos diferentes e observa uma
combinação que nunca existiu. Um snapshot por transação pode ser necessário
para relatório coerente.

## 5. Isolamento no PostgreSQL

| Nível solicitado | Snapshot e garantia prática | O que a aplicação ainda faz |
|---|---|---|
| Read Uncommitted | tratado como Read Committed | o mesmo que abaixo |
| Read Committed | snapshot novo por statement; sem dirty read | operação atômica/locks para decisão entre statements |
| Repeatable Read | snapshot estável; sem non-repeatable read/phantom de snapshot | tratar falha de serialização e possíveis write skews |
| Serializable | execução equivalente a alguma ordem serial ou abort | retry completo de `40001` |

Escolher isolamento mais forte não elimina:

- constraints;
- validação/autorização;
- limite de transação;
- idempotência de efeitos externos;
- tratamento de abort;
- timeout e observabilidade.

Configure no início:

```sql
BEGIN TRANSACTION ISOLATION LEVEL SERIALIZABLE;
-- leituras e escritas
COMMIT;
```

Não altere o nível depois de executar operações incompatíveis. Teste o workload:
`SERIALIZABLE` pode aumentar aborts sob contenção, e o retry é parte do contrato.

## 6. Locks pessimistas

```sql
BEGIN;

SELECT id, stock, version
FROM product
WHERE id = $1
FOR UPDATE;

-- decidir e atualizar usando a mesma conexão/transação
UPDATE product
SET stock = stock - $2,
    version = version + 1
WHERE id = $1
  AND stock >= $2
RETURNING stock, version;

COMMIT;
```

`FOR UPDATE` bloqueia mudanças concorrentes incompatíveis na linha selecionada
até o fim da transação. Variantes têm semântica diferente:

- `FOR NO KEY UPDATE`: lock de atualização menos forte em alguns conflitos;
- `FOR SHARE` e `FOR KEY SHARE`: proteções de leitura/referência;
- `NOWAIT`: falha imediatamente se não puder adquirir;
- `SKIP LOCKED`: pula linhas bloqueadas.

`SKIP LOCKED` é útil para múltiplos workers disputando jobs, mas produz visão
inconsistente e não serve para consulta geral. Um consumidor precisa lease,
estado, retry, limite de tentativas e recuperação de job abandonado.

### Lock de tabela e DDL

Mesmo operações “online” podem adquirir locks breves que esperam atrás de
transações antigas. Enquanto esperam, podem bloquear uma fila de comandos.
Defina `lock_timeout`, monitore sessões e teste migrations com tráfego.

### Advisory locks

Advisory locks usam chaves definidas pela aplicação. Servem para coordenação que
não corresponde facilmente a uma linha, mas o banco não conhece sua semântica:
todos os participantes precisam usar a mesma convenção. Prefira locks
transacionais para liberação automática; documente namespace e colisões.

## 7. Deadlocks

Sessão A bloqueia produto 1 e espera produto 2; sessão B bloqueia produto 2 e
espera produto 1. PostgreSQL detecta o ciclo e aborta uma delas.

Reduza deadlocks:

- adquira recursos na mesma ordem global;
- mantenha transações curtas;
- indexe predicados para bloquear somente o conjunto necessário;
- evite interação externa enquanto segura lock;
- processe lotes pequenos;
- trate `40P01` com retry seguro e limitado.

Um deadlock não é corrigido aumentando indefinidamente timeout. Capture
consultas, locks, ordem e contexto da transação abortada, removendo parâmetros
sensíveis dos logs.

## 8. Concorrência otimista

Quando conflitos são raros, compare uma versão:

```sql
UPDATE product
SET name = $1,
    price_cents = $2,
    version = version + 1,
    updated_at = now()
WHERE id = $3
  AND version = $4
RETURNING id, name, price_cents, version, updated_at;
```

Resultado:

- uma linha: atualização aceita;
- zero linhas: recurso não existe **ou** versão está obsoleta.

Para diferenciar, faça consulta posterior conforme a política. Não retire
`version` do predicado depois de verificar na aplicação: haveria janela de
corrida.

Na API, a versão pode ser exposta como ETag:

```http
ETag: "7"

PATCH /products/ID
If-Match: "7"
```

Se a versão atual for 8, responda `412 Precondition Failed`. Isso torna conflito
visível ao cliente, que pode recarregar, mesclar ou pedir decisão humana.

### Otimista versus pessimista

| Situação | Estratégia provável |
|---|---|
| edição de formulário, conflito raro | versão otimista |
| decisão curta depende de valor atual | lock pessimista |
| contador/saldo simples | update atômico |
| unicidade | constraint única |
| regra entre muitas linhas | modelagem/constraint ou Serializable + retry |

Não escolha pelo nome. Escolha pela invariante, contenção, duração e UX de
conflito.

## 9. Savepoints

Um savepoint desfaz parte de uma transação:

```sql
BEGIN;
INSERT INTO import_batch (id, started_at) VALUES ($1, now());

SAVEPOINT before_optional_row;
-- operação que pode falhar
ROLLBACK TO SAVEPOINT before_optional_row;

-- a transação continua
COMMIT;
```

Depois de um erro SQL no PostgreSQL, a transação fica abortada até
`ROLLBACK` ou `ROLLBACK TO SAVEPOINT`. Drivers/frameworks podem administrar
savepoints, mas capturar exceção sem restaurar o estado não torna a conexão útil.

Não use savepoint para confirmar parcialmente uma invariante que deveria ser
atômica. Em importações, registre claramente quais linhas podem falhar isoladas.

## 10. Retry correto

Erros transitórios típicos para retry de transação:

- `40001`: serialization failure;
- `40P01`: deadlock detected.

Algumas falhas de conexão têm resultado **incerto**: o cliente perdeu a resposta
e não sabe se o commit ocorreu. Repetir cegamente pode duplicar efeito. Uma chave
de idempotência ou ID único por intenção permite consultar/reexecutar com segurança.

Algoritmo conceitual:

```text
para tentativa de 1 até limite:
    abrir transação nova
    tentar executar toda a unidade
    se sucesso: commit e retornar
    se SQLSTATE retryable:
        rollback
        se limite atingido: falhar
        esperar backoff exponencial + jitter, respeitando deadline
        continuar
    senão:
        rollback e propagar
```

Requisitos:

- retry da **transação inteira** com snapshot novo;
- conexões/transações novas ou corretamente resetadas;
- limite de tentativas e deadline;
- backoff com jitter;
- classificação pelo código estruturado, não texto;
- nenhum email/HTTP irreversível dentro do trecho repetível;
- métricas por causa e tentativa.

## 11. Efeito externo e outbox

Não existe rollback mágico entre banco e chamada HTTP:

```text
BEGIN
UPDATE estoque
POST /transportadora      <- confirma fora do banco
ROLLBACK                  <- transportadora não desfaz
```

Use outbox:

1. atualize o domínio;
2. insira evento/outbox com ID único na mesma transação;
3. confirme;
4. worker busca eventos pendentes;
5. publica/processa com idempotência;
6. marca progresso/reconcilia.

Há uma janela de consistência intencional. Monitore idade da outbox, falhas,
tentativas, poison messages e divergência entre fonte e projeção.

## 12. Connection pools

Abrir conexão envolve rede, autenticação e memória no servidor. Pool reutiliza e
limita conexões, mas não cria capacidade:

```text
total potencial =
  réplicas da aplicação × pool máximo por réplica
  + workers
  + migrations/administração
  + margem operacional
```

Se 30 réplicas abrem 20 conexões, são 600 antes dos jobs. Um pool grande pode
transformar fila controlada na aplicação em saturação do banco.

Observe:

- conexões ativas, ociosas e aguardando;
- tempo para adquirir conexão;
- duração de statement e transação;
- sessões `idle in transaction`;
- locks e deadlocks;
- taxa de timeout/cancelamento;
- capacidade reservada para administração.

Ao devolver conexão:

- commit ou rollback explícito;
- nenhum cursor/stream pendente;
- parâmetros de sessão restaurados;
- conexão quebrada descartada;
- contexto do usuário não pode vazar para a próxima requisição.

Pool também precisa de timeout de aquisição, tempo máximo/vida e health check
compatíveis com o driver e infraestrutura.

## 13. Timeouts e cancelamento

Proteções complementares:

- timeout para obter conexão;
- `statement_timeout` para consulta;
- `lock_timeout` para esperar lock;
- `idle_in_transaction_session_timeout` como rede de segurança;
- deadline da requisição;
- cancelamento propagado quando o cliente desiste.

O timeout externo deve permitir que camadas internas cancelem e respondam de
modo controlado. Cancelar no cliente não garante que o servidor parou; confirme
comportamento do driver.

## 14. Laboratório em duas sessões

Use duas janelas `psql` no banco local.

### Non-repeatable read

Sessão A:

```sql
BEGIN ISOLATION LEVEL READ COMMITTED;
SELECT status FROM copy WHERE id = 2;
-- aguarde a sessão B confirmar
SELECT status FROM copy WHERE id = 2;
ROLLBACK;
```

Sessão B:

```sql
UPDATE copy SET status = 'retired' WHERE id = 2;
```

Repita A em `REPEATABLE READ` e compare. Restaure a fixture ao final.

### Deadlock controlado

Sessão A:

```sql
BEGIN;
SELECT id FROM copy WHERE id = 1 FOR UPDATE;
-- depois de B bloquear 2:
SELECT id FROM copy WHERE id = 2 FOR UPDATE;
```

Sessão B:

```sql
BEGIN;
SELECT id FROM copy WHERE id = 2 FOR UPDATE;
SELECT id FROM copy WHERE id = 1 FOR UPDATE;
```

Uma sessão recebe `40P01`. Execute `ROLLBACK` nas duas e não deixe locks
abertos. Em seguida, repita bloqueando sempre IDs em ordem crescente.

## 15. Erros recorrentes

- achar que dois statements em autocommit formam uma transação;
- ler, calcular na aplicação e escrever sem lock/versão;
- fazer chamada externa segurando locks;
- ignorar zero linhas em update condicional;
- retry de apenas o último statement;
- retry ilimitado ou baseado na mensagem textual;
- reutilizar conexão cuja transação ficou abortada;
- usar `SKIP LOCKED` como leitura consistente;
- aumentar pool até exceder o banco;
- manter transações abertas durante streaming ou interação humana;
- acreditar que `SERIALIZABLE` elimina constraints e idempotência.

## 16. Exercícios progressivos

1. Reproduza non-repeatable read em duas sessões e compare os snapshots.
2. Implemente redução de estoque atômica; prove que duas sessões não deixam saldo
   negativo.
3. Reproduza lost update ingênuo e corrija com `version`.
4. Crie o deadlock do laboratório, capture SQLSTATE e elimine-o com ordem global.
5. Modele write skew de plantonistas e compare lock explícito com
   `SERIALIZABLE`.
6. Escreva pseudocódigo de retry da transação inteira com limite/deadline.
7. Calcule orçamento de conexões para API, worker e administração.
8. Desenhe outbox, deduplicação e métrica de atraso para uma integração fictícia.

## Critério de conclusão

- [ ] Explico ACID e o que cada letra não garante.
- [ ] Sei dizer quando o driver abre e encerra uma transação.
- [ ] Consigo identificar snapshot e anomalia numa linha do tempo concorrente.
- [ ] Escolho operação atômica, constraint, lock ou versão por invariante.
- [ ] Toda transação é curta e não contém efeito externo irreversível.
- [ ] Trato `40001`/`40P01` refazendo a unidade inteira com limite.
- [ ] Operações de resultado incerto têm estratégia de idempotência.
- [ ] Pool e timeouts cabem no orçamento global do banco.
- [ ] Demonstrei os cenários em duas sessões e restaurei a fixture.

Continue em [Índices e desempenho](05-indices-performance.md) para medir como
essas decisões usam CPU, memória e I/O.
