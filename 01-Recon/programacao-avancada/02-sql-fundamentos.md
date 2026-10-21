# SQL: fundamentos sólidos

SQL é uma linguagem declarativa: você descreve o resultado e as restrições; o
SGBD escolhe um plano físico compatível. Isso não significa que desempenho seja
automático, mas muda o raciocínio: pense em **conjuntos de linhas**, tipos,
cardinalidade e invariantes, não em um laço manual por registro.

Os exemplos usam PostgreSQL e o domínio do
[laboratório de biblioteca](referencias/GUIA-LAB-SQL.md). Execute somente em um
banco local de estudos com dados fictícios.

## Objetivos

Ao concluir, você deverá conseguir:

- distinguir DDL, DML, DQL, DCL e TCL;
- criar tabelas com tipos e constraints coerentes;
- inserir, atualizar e remover linhas com segurança;
- prever a ordem lógica de uma consulta;
- combinar relações sem multiplicar resultados por acidente;
- agregar corretamente, inclusive na presença de `NULL`;
- usar parâmetros de driver em vez de concatenar entrada;
- verificar efeitos e erros de cada comando.

## 1. Orientação: servidor, banco, schema e sessão

Uma instância PostgreSQL pode conter vários bancos; cada conexão entra em um
banco. Dentro dele, schemas organizam objetos. Um nome não qualificado é
resolvido pelo `search_path`, portanto código sensível deve controlar o schema
e permissões.

Uma **sessão** mantém estado como transação atual, timezone, parâmetros e tabelas
temporárias. Uma conexão de pool pode ser reutilizada por requisições diferentes;
não deixe nela uma transação aberta ou configuração inesperada.

No `psql`, estes metacomandos ajudam a estudar (não são SQL):

```text
\conninfo        mostra a conexão
\dn              lista schemas
\dt              lista tabelas visíveis
\d loan          descreve tabela
\x auto          alterna exibição expandida
\pset null '(null)'
```

Para SQL executável e portável entre clientes, use comandos como
`SELECT current_database(), current_user, current_schema();`.

## 2. Famílias de comandos

| Família | Finalidade | Exemplos |
|---|---|---|
| DDL | definir estrutura | `CREATE`, `ALTER`, `DROP` |
| DML | alterar dados | `INSERT`, `UPDATE`, `DELETE` |
| DQL | consultar | `SELECT` |
| DCL | controlar privilégios | `GRANT`, `REVOKE` |
| TCL | controlar transação | `BEGIN`, `COMMIT`, `ROLLBACK` |

Essas categorias são didáticas; documentação e fornecedores podem classificá-las
de forma ligeiramente diferente. O importante é entender efeito, lock, privilégio
e limite transacional de cada comando.

## 3. DDL: transforme regras em estrutura

Um recorte mínimo do laboratório:

```sql
CREATE TABLE member (
    id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    display_name varchar(120) NOT NULL,
    email varchar(254) NOT NULL,
    joined_at timestamptz NOT NULL DEFAULT now(),
    CONSTRAINT member_name_not_blank
        CHECK (btrim(display_name) <> ''),
    CONSTRAINT member_email_unique UNIQUE (email)
);

CREATE TABLE book (
    id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    isbn varchar(13) NOT NULL,
    title varchar(200) NOT NULL,
    published_year integer,
    CONSTRAINT book_isbn_format CHECK (isbn ~ '^[0-9]{13}$'),
    CONSTRAINT book_isbn_unique UNIQUE (isbn),
    CONSTRAINT book_title_not_blank CHECK (btrim(title) <> ''),
    CONSTRAINT book_year_reasonable
        CHECK (published_year BETWEEN 1450 AND 2100)
);

CREATE TABLE copy (
    id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    book_id bigint NOT NULL,
    acquired_at date NOT NULL,
    status varchar(12) NOT NULL DEFAULT 'available',
    CONSTRAINT copy_book_fk
        FOREIGN KEY (book_id) REFERENCES book(id) ON DELETE RESTRICT,
    CONSTRAINT copy_status_valid
        CHECK (status IN ('available', 'loaned', 'retired'))
);
```

Leia cada linha como uma promessa:

- identidade é gerada pelo banco e não inserida manualmente;
- ISBN possui formato e unicidade;
- título não aceita apenas whitespace;
- exemplar não existe sem obra;
- obra referenciada não é apagada silenciosamente;
- estado do exemplar pertence a um conjunto conhecido.

### Ordem de criação e remoção

Crie primeiro objetos referenciados e depois dependentes. Ao remover, faça a
ordem inversa. `DROP TABLE ... CASCADE` é conveniente, mas pode apagar objetos
dependentes além do esperado; em ambientes persistentes, liste e revise o alvo.

`DROP`, `TRUNCATE` e updates sem filtro são destrutivos. O fato de PostgreSQL
permitir DDL transacional não substitui backup, revisão e entendimento dos locks.

## 4. Literais, tipos e conversão

Prefira literais tipados quando a intenção importa:

```sql
SELECT DATE '2026-10-03',
       TIMESTAMPTZ '2026-10-03 12:00:00Z',
       4500::bigint,
       true;
```

O banco faz coerções implícitas em alguns contextos, mas depender delas pode
criar ambiguidade ou impedir índices. A aplicação deve enviar valores no tipo
do protocolo do driver, não montar texto SQL.

Strings usam aspas simples: `'texto'`. Identificadores usam aspas duplas:
`"MixedCaseName"`. Evite identificadores com case especial; sem aspas,
PostgreSQL normaliza nomes para minúsculas.

## 5. `INSERT`: crie fatos e leia o resultado real

```sql
INSERT INTO member (display_name, email, joined_at)
VALUES (
    'Pessoa de Laboratório',
    'pessoa@example.test',
    TIMESTAMPTZ '2026-10-03 12:00:00Z'
)
RETURNING id, display_name, email, joined_at;
```

`RETURNING` evita outra consulta e devolve valores gerados/defaults. Para várias
linhas:

```sql
INSERT INTO book (isbn, title, published_year)
VALUES
    ('9780000000100', 'Álgebra Relacional Aplicada', 2025),
    ('9780000000101', 'Transações sem Mistério', 2026)
RETURNING id, isbn;
```

Sem `ORDER BY`, nem mesmo a ordem de um resultado com `RETURNING` deve virar
contrato acidental da aplicação.

### Conflito esperado

Quando a unicidade faz parte do fluxo, PostgreSQL oferece upsert:

```sql
INSERT INTO member (display_name, email)
VALUES ('Nome Atual', 'pessoa@example.test')
ON CONFLICT (email)
DO UPDATE
SET display_name = EXCLUDED.display_name
RETURNING id, display_name, email;
```

Isso é atômico, mas a política precisa ser válida: nem todo conflito autoriza
sobrescrever dados. Para “criar usuário”, talvez o email duplicado deva gerar
erro, não atualizar a conta existente.

## 6. `SELECT`: forma básica e ordem lógica

```sql
SELECT id, title, published_year
FROM book
WHERE published_year >= 2024
ORDER BY published_year DESC, id ASC
LIMIT 20;
```

A ordem textual não é a ordem lógica aproximada:

```text
FROM / JOIN
  -> WHERE
  -> GROUP BY
  -> HAVING
  -> SELECT
  -> DISTINCT
  -> ORDER BY
  -> OFFSET / LIMIT
```

Isso explica por que um alias criado em `SELECT` normalmente não está
disponível em `WHERE`: o filtro é conceitualmente avaliado antes.

### Predicados

```sql
SELECT id, title
FROM book
WHERE published_year BETWEEN 2020 AND 2026
  AND title ILIKE '%dados%'
  AND genre IN ('databases', 'software');
```

- `BETWEEN` inclui os dois limites;
- `LIKE` usa `%` (qualquer sequência) e `_` (um caractere);
- `ILIKE` é extensão case-insensitive do PostgreSQL;
- `IN` expressa uma lista/conjunto;
- `IS NULL` e `IS NOT NULL` tratam ausência;
- parênteses tornam explícita a precedência entre `AND` e `OR`.

Para intervalos de instantes, prefira limite inferior inclusivo e superior
exclusivo:

```sql
WHERE joined_at >= TIMESTAMPTZ '2026-10-01 00:00:00Z'
  AND joined_at <  TIMESTAMPTZ '2026-11-01 00:00:00Z'
```

Isso evita inventar “último microssegundo do mês”.

### Projeção e expressões

```sql
SELECT id,
       title,
       coalesce(published_year::text, 'ano desconhecido') AS year_label
FROM book;
```

Evite `SELECT *` em contratos de aplicação: ele transfere colunas
desnecessárias, torna o consumidor dependente de mudanças e pode expor campos.
Em exploração interativa, `*` continua útil.

## 7. Ordenação e paginação básica

SQL não garante ordem sem `ORDER BY`. Um plano diferente, vacuum ou paralelismo
pode mudar a sequência observada.

```sql
SELECT id, title, published_year
FROM book
ORDER BY published_year DESC NULLS LAST, id ASC
LIMIT 20 OFFSET 0;
```

A ordenação deve ser **total**: `id` desempata anos iguais. `OFFSET` é
adequado para exemplos e páginas pequenas, mas fica caro e instável enquanto
linhas são inseridas/removidas. O capítulo de
[SQL avançado](03-sql-avancado.md) implementa paginação por cursor.

## 8. `UPDATE`: altere somente o conjunto pretendido

```sql
UPDATE copy
SET status = 'retired'
WHERE id = 42
  AND status = 'available'
RETURNING id, book_id, status;
```

A condição codifica uma transição: somente exemplar disponível pode ser
aposentado nessa operação. O número de linhas afetadas importa:

- 1: transição aplicada;
- 0: exemplar ausente ou estado incompatível;
- mais de 1: impossível aqui por chave primária; em outro filtro pode ser bug.

Para operação manual:

1. abra transação;
2. execute um `SELECT` com o mesmo predicado;
3. confirme o conjunto e, quando necessário, bloqueie;
4. execute `UPDATE ... RETURNING`;
5. confira contagem e valores;
6. faça `COMMIT` ou `ROLLBACK`.

Não transforme isso em falsa garantia: entre um `SELECT` e um `UPDATE`
separados, outra transação pode agir. Para invariantes, use operação condicional,
constraint ou lock no limite transacional adequado.

## 9. `DELETE`, retenção e histórico

```sql
DELETE FROM member
WHERE id = 42
  AND NOT EXISTS (
      SELECT 1
      FROM loan
      WHERE loan.member_id = member.id
  )
RETURNING id, email;
```

Foreign keys ainda protegem referências. Exclusão física, anonimização e soft
delete têm objetivos diferentes:

- **física:** dado some das tabelas e precisa de política de backup;
- **anonimização:** preserva estatística/histórico sem identidade recuperável;
- **soft delete:** marca estado, mas aumenta complexidade de todas as consultas,
  unicidade, índices e retenção.

Não use soft delete automaticamente. Se dados pessoais devem ser apagados,
mantê-los com `deleted_at` pode não cumprir o requisito.

## 10. Joins: combine fatos e controle cardinalidade

```sql
SELECT c.id AS copy_id,
       b.title,
       c.status
FROM copy AS c
JOIN book AS b ON b.id = c.book_id
ORDER BY c.id;
```

### Tipos principais

- `INNER JOIN`: somente pares que satisfazem a condição;
- `LEFT JOIN`: todas as linhas da esquerda e correspondência opcional;
- `RIGHT JOIN`: equivalente invertendo os lados; menos usado por legibilidade;
- `FULL JOIN`: preserva não correspondentes de ambos;
- `CROSS JOIN`: produto cartesiano intencional;
- `EXISTS`: testa existência sem duplicar a linha externa.

Para listar membros sem empréstimo:

```sql
SELECT m.id, m.display_name
FROM member AS m
WHERE NOT EXISTS (
    SELECT 1
    FROM loan AS l
    WHERE l.member_id = m.id
)
ORDER BY m.id;
```

### Armadilha: transformar `LEFT JOIN` em inner join

```sql
-- Perde membros sem empréstimo ou sem empréstimo recente:
SELECT m.id, l.id
FROM member AS m
LEFT JOIN loan AS l ON l.member_id = m.id
WHERE l.borrowed_at >= TIMESTAMPTZ '2026-09-01 00:00:00Z';
```

Como a linha estendida possui `l.borrowed_at = NULL`, o `WHERE` a elimina. Para
preservar todos os membros e associar somente empréstimos recentes, mova o
predicado para o `ON`:

```sql
SELECT m.id, m.display_name, l.id AS recent_loan_id
FROM member AS m
LEFT JOIN loan AS l
  ON l.member_id = m.id
 AND l.borrowed_at >= TIMESTAMPTZ '2026-09-01 00:00:00Z'
ORDER BY m.id, l.id;
```

Para associar somente empréstimos abertos, use do mesmo modo
`AND l.returned_at IS NULL` no `ON`. Colocar esse teste no `WHERE` mistura a
linha “sem empréstimo” com a linha “empréstimo aberto”, porque ambas possuem
`NULL` nessa expressão.

### Multiplicação de linhas

Se uma obra tem 3 autores e 4 exemplares, juntar ambas as relações produz 12
combinações. Somar atributos depois pode multiplicar valores. Antes de escrever
um join, declare o **grão** esperado: “uma linha por obra”, “por exemplar” ou
“por empréstimo”. Agregue cada lado antes de reuni-los quando necessário.

## 11. Agregações

```sql
SELECT b.id,
       b.title,
       count(DISTINCT c.id) AS copies,
       count(l.id) AS loans,
       count(l.id) FILTER (WHERE l.returned_at IS NULL) AS open_loans
FROM book AS b
LEFT JOIN copy AS c ON c.book_id = b.id
LEFT JOIN loan AS l ON l.copy_id = c.id
GROUP BY b.id, b.title
HAVING count(DISTINCT c.id) > 0
ORDER BY loans DESC, b.id;
```

- `WHERE` filtra linhas antes da formação dos grupos;
- `GROUP BY` define o grão de saída;
- `HAVING` filtra grupos;
- `count(*)` conta linhas;
- `count(expression)` ignora valores `NULL`;
- `sum` e `avg` retornam `NULL` sobre conjunto vazio;
- `FILTER` calcula agregações condicionais com clareza.

`DISTINCT` não deve “corrigir” um join que você não compreendeu. Ele pode
esconder multiplicação incorreta e adicionar sort/hash caro.

## 12. Parâmetros: valores nunca viram código

Código inseguro:

```python
# NÃO FAÇA: entrada muda a estrutura do SQL.
sql = f"SELECT id, title FROM book WHERE isbn = '{isbn}'"
```

Código parametrizado com um driver DB-API compatível:

```python
row = connection.execute(
    "SELECT id, title FROM book WHERE isbn = %s",
    (isbn,),
).fetchone()
```

O placeholder exato depende do driver. Parâmetros transportam **valores**,
preservam tipos e impedem que conteúdo seja interpretado como sintaxe. Não
servem normalmente para nomes de coluna, tabela, direção `ASC/DESC` ou
fragmentos SQL.

Para identificadores dinâmicos:

1. evite-os se possível;
2. mapeie uma allowlist de opções da API para identificadores conhecidos;
3. use o construtor seguro de SQL do driver;
4. nunca aceite um fragmento arbitrário do cliente.

```python
SORTS = {
    "title": "title ASC, id ASC",
    "-year": "published_year DESC NULLS LAST, id ASC",
}
order_by = SORTS.get(requested_sort)
if order_by is None:
    raise ValueError("sort não permitido")
# order_by veio da allowlist do servidor, não da entrada literal.
```

Parâmetros evitam injeção de valores, mas não substituem menor privilégio,
timeouts, limite de linhas e validação de autorização.

## 13. Privilégios mínimos

A aplicação não deve conectar como superusuário ou dono de todos os schemas.
Separe, quando possível:

- papel de migration, capaz de alterar estrutura;
- papel de runtime, com apenas `SELECT/INSERT/UPDATE/DELETE` necessários;
- papel somente leitura para relatórios;
- administração operacional auditada.

Qualificar schema e revogar criação no schema público reduz confusão. Segredos
de conexão ficam fora do repositório e dos logs.

## 14. Erros recorrentes

- confiar na ordem observada sem `ORDER BY`;
- usar `LIMIT` com ordenação não determinística;
- concatenar valor ou identificador vindo do cliente;
- executar `UPDATE`/`DELETE` sem validar predicado e contagem;
- usar `DISTINCT` para esconder join multiplicado;
- filtrar a tabela direita de um `LEFT JOIN` no lugar errado;
- escrever `NOT IN (subquery)` sem considerar `NULL`;
- depender de coerção implícita de tipo;
- conectar a aplicação com privilégios de owner/superuser;
- confundir linha afetada com operação de domínio concluída sem verificar regras.

## 15. Exercícios progressivos

Execute primeiro os scripts do [laboratório SQL](referencias/GUIA-LAB-SQL.md).

### Nível 1 — leitura e filtros

1. Liste obras por ano, com `NULL` por último e `id` como desempate.
2. Liste empréstimos iniciados em setembro de 2026 usando intervalo semiaberto.
3. Mostre somente campos necessários, com aliases legíveis.

### Nível 2 — integridade e escrita

1. Insira membro e capture `id` com `RETURNING`.
2. Force violações de `NOT NULL`, `UNIQUE`, `CHECK` e foreign key.
3. Registre nome da constraint/SQLSTATE e a invariante correspondente.
4. Faça update condicional e trate separadamente zero e uma linha afetada.

### Nível 3 — joins

1. Liste obras sem exemplar usando `NOT EXISTS`.
2. Liste todos os membros e apenas seus empréstimos abertos sem perder membros.
3. Demonstre a multiplicação autores × exemplares e corrija para uma linha por
   obra com pré-agregação.

### Nível 4 — segurança e contrato

1. Reescreva uma consulta concatenada usando parâmetros.
2. Implemente ordenação dinâmica por allowlist.
3. Crie um papel de laboratório com somente os privilégios necessários.
4. Explique por que parâmetro não resolve autorização nem limite de custo.

## Critério de conclusão

- [ ] Consigo explicar o efeito e o risco de DDL, DML, DQL, DCL e TCL.
- [ ] Todo exemplo de escrita verifica linhas retornadas/afetadas.
- [ ] Minhas consultas têm grão e ordenação declarados.
- [ ] Sei prever como `NULL` altera filtro e agregação.
- [ ] Diferencio filtro de linha (`WHERE`) de filtro de grupo (`HAVING`).
- [ ] Consigo explicar a cardinalidade de cada join antes de executá-lo.
- [ ] Valores usam parâmetros e opções estruturais usam allowlist.
- [ ] A conta de runtime possui privilégio mínimo.
- [ ] Completei e documentei os exercícios sem dados reais ou sensíveis.

Avance para [SQL avançado](03-sql-avancado.md), onde as mesmas relações serão
usadas em CTEs, janelas, paginação e transformações mais complexas.
