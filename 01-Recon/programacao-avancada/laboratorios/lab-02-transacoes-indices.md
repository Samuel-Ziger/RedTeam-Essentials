# Lab 02 — transações, concorrência e índices com evidência

## Resultado esperado

Você vai reproduzir um conflito concorrente, escolher a política de bloqueio e
comparar planos antes/depois de um índice. O laboratório separa três ideias que
costumam ser confundidas: atomicidade, isolamento e velocidade.

## Pré-requisitos e tempo

- Lab 01 concluído;
- capítulos 03, 04 e 05;
- 10 a 16 horas;
- dois terminais com `psql` no PostgreSQL local.

Recrie os dados com os arquivos
[`001_schema.sql`](sql/001_schema.sql) e
[`002_seed.sql`](sql/002_seed.sql), ou execute
[`testar-laboratorios.sh`](testar-laboratorios.sh) com `--postgres-only` para
validar a linha de base.

## Parte 1 — observar uma transação, não imaginar

Abra sessões A e B:

```bash
docker compose exec postgres psql -U course -d course
```

Na sessão A:

```sql
BEGIN;
SELECT id, status FROM copy WHERE id = 2 FOR UPDATE;
UPDATE copy SET status = 'loaned' WHERE id = 2;
```

Na sessão B, reduza o tempo máximo e tente alterar a mesma linha:

```sql
SET lock_timeout = '2s';
BEGIN;
UPDATE copy SET status = 'retired' WHERE id = 2;
```

Registre o erro e consulte, numa terceira sessão, `pg_stat_activity` e
`pg_locks`. Depois execute `ROLLBACK` nas sessões abertas. O timeout é uma
política operacional; não “resolve” a disputa, apenas limita espera.

## Parte 2 — lost update e duas correções

Crie uma tabela de rascunho com `id`, `quantity` e `version`. Faça A e B lerem a
mesma quantidade e gravarem resultados derivados do valor antigo. Demonstre a
perda de atualização sob `READ COMMITTED`.

Corrija de duas maneiras e compare:

1. atualização atômica: `quantity = quantity + :delta`;
2. concorrência otimista: `WHERE id = :id AND version = :expected`.

Na segunda solução, zero linhas alteradas não é sucesso: é o sinal de conflito
que a aplicação deve traduzir, por exemplo, para HTTP 412.

## Parte 3 — savepoint e atomicidade

Dentro de uma transação:

1. insira um membro válido;
2. crie `SAVEPOINT before_invalid_loan`;
3. tente um empréstimo que viole uma constraint;
4. volte ao savepoint;
5. insira outra operação válida;
6. confirme;

Explique por que capturar um erro sem rollback deixa a transação PostgreSQL em
estado abortado.

## Parte 4 — plano de execução

O conjunto didático é pequeno demais para uma medição honesta. Gere, em uma
transação que será revertida, pelo menos 50 mil empréstimos históricos com
`generate_series`. Em seguida execute:

```sql
EXPLAIN (ANALYZE, BUFFERS, WAL, FORMAT TEXT)
SELECT id, due_at
FROM loan
WHERE member_id = 1
ORDER BY borrowed_at DESC
LIMIT 20;
```

Capture o plano, remova em sua cópia o índice `loan_member_borrowed_idx`, rode
`ANALYZE loan` e capture novamente. Compare:

- tipo de scan;
- linhas estimadas e reais;
- buffers lidos/atingidos;
- presença de sort;
- tempo, lembrando efeito de cache.

Não conclua que um índice “é melhor” só porque existe `Index Scan`. Inclua o
custo de escrita e o tamanho obtido em `pg_relation_size`.

## Parte 5 — explicar o índice parcial

Abra [`003_queries.sql`](sql/003_queries.sql) e explique por que
`one_open_loan_per_copy` é simultaneamente:

- uma estrutura de busca;
- uma constraint de unicidade condicional;
- uma proteção contra duas transações concorrentes;
- menor que um índice contendo empréstimos devolvidos.

Use [`004_assertions.sql`](sql/004_assertions.sql) como exemplo de teste
negativo automatizado.

## Gate de conclusão

- conflito de lock reproduzido sem deixar sessão/transação aberta;
- lost update demonstrado e corrigido por duas estratégias;
- plano antes/depois preservado com interpretação, não somente screenshot;
- asserções do Lab 01 continuam verdes;
- toda massa sintética foi revertida ou removida.
