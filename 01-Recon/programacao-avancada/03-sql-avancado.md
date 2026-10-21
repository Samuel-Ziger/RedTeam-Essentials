# SQL avançado: composição, análise e paginação

SQL avançado não é colecionar palavras-chave. É decompor uma pergunta em
conjuntos com grão conhecido, preservar cardinalidade e expressar a operação de
forma que o banco possa executá-la corretamente sob volume e concorrência.

Este capítulo usa PostgreSQL. Revise
[SQL: fundamentos sólidos](02-sql-fundamentos.md) antes de avançar.

## Objetivos

Ao concluir, você deverá conseguir:

- compor consultas legíveis com subqueries e CTEs;
- percorrer hierarquias sem recursão infinita;
- escolher partição, ordem e frame de window functions;
- usar semi-join, anti-join e `LATERAL` conscientemente;
- implementar upsert com uma política de conflito explícita;
- decidir quando JSONB, view, materialized view, função ou trigger é adequado;
- construir paginação keyset total, estável e validável;
- revisar consultas por correção antes de otimizá-las.

## 1. O método: defina o grão de cada etapa

Antes do SQL, escreva:

```text
Pergunta: quais três obras mais emprestadas em cada gênero?
Entrada: uma linha por empréstimo
Etapa A: uma linha por obra com total de empréstimos
Etapa B: uma linha por obra com posição dentro do gênero
Saída: até três linhas por gênero
```

Essa disciplina evita o erro clássico de juntar duas relações 1:N e agregar o
produto cartesiano acidental. Para cada etapa, pergunte:

1. o que uma linha representa?
2. qual conjunto pode ter `NULL`?
3. qual chave torna uma linha única?
4. filtros pertencem antes ou depois da agregação?
5. a saída precisa de ordem total?

## 2. Subqueries e CTEs

Uma subquery pode estar em `FROM`, `WHERE`, `SELECT` ou outro contexto. Uma
Common Table Expression (CTE) nomeia uma etapa:

```sql
WITH loan_count AS (
    SELECT c.book_id,
           count(*) AS total_loans
    FROM copy AS c
    JOIN loan AS l ON l.copy_id = c.id
    GROUP BY c.book_id
)
SELECT b.id,
       b.title,
       coalesce(lc.total_loans, 0) AS total_loans
FROM book AS b
LEFT JOIN loan_count AS lc ON lc.book_id = b.id
ORDER BY total_loans DESC, b.id;
```

O grão da CTE é “uma linha por obra”; o join final não multiplica esse valor.

### CTE não é tabela temporária

Uma CTE existe somente durante o statement. Em versões modernas do PostgreSQL,
uma CTE não recursiva, sem efeitos colaterais e referenciada uma vez pode ser
integrada ao plano da consulta. `MATERIALIZED` força calcular/armazenar a etapa;
`NOT MATERIALIZED` permite integração quando legal:

```sql
WITH recent_loans AS NOT MATERIALIZED (
    SELECT *
    FROM loan
    WHERE borrowed_at >= TIMESTAMPTZ '2026-01-01 00:00:00Z'
)
SELECT count(*)
FROM recent_loans
WHERE member_id = 7;
```

Não espalhe essas opções por intuição. Compare planos e mantenha semântica
correta. Materializar pode evitar cálculo repetido, mas também impede empurrar
filtros e consome memória/disco temporário.

### CTE de modificação

PostgreSQL permite capturar linhas alteradas:

```sql
WITH returned AS (
    UPDATE loan
    SET returned_at = TIMESTAMPTZ '2026-10-03 15:00:00Z'
    WHERE id = 42
      AND returned_at IS NULL
    RETURNING id, copy_id, returned_at
)
UPDATE copy AS c
SET status = 'available'
FROM returned AS r
WHERE c.id = r.copy_id
RETURNING r.id AS loan_id, c.id AS copy_id, c.status;
```

O statement é atômico, mas a modelagem ainda deve impedir combinações inválidas.
Para fluxos maiores, uma transação com comandos claros costuma ser mais fácil de
observar e tratar.

## 3. CTE recursiva

Uma CTE recursiva possui termo base e termo recursivo:

```sql
-- Suponha category(id, parent_id, name).
WITH RECURSIVE category_tree AS (
    SELECT id,
           parent_id,
           name,
           0 AS depth,
           ARRAY[id] AS path
    FROM category
    WHERE id = $1

    UNION ALL

    SELECT child.id,
           child.parent_id,
           child.name,
           parent.depth + 1,
           parent.path || child.id
    FROM category AS child
    JOIN category_tree AS parent
      ON child.parent_id = parent.id
    WHERE parent.depth < 20
      AND NOT child.id = ANY (parent.path)
)
SELECT id, parent_id, name, depth, path
FROM category_tree
ORDER BY path;
```

Proteções:

- condição de parada (`depth < 20`);
- detecção de ciclo pelo caminho;
- índice na coluna usada na travessia (`parent_id`);
- limite de resultado/tempo na aplicação;
- regra de escrita que evita ciclo, quando possível.

`UNION` remove duplicatas e pode interromper alguns ciclos, mas adiciona custo
e não substitui modelagem explícita. `UNION ALL` preserva duplicatas e costuma
ser preferido quando o caminho é controlado.

## 4. Window functions

Agregação com `GROUP BY` colapsa linhas. Uma window function calcula sobre um
conjunto relacionado e mantém cada linha:

```sql
SELECT l.id,
       l.member_id,
       l.borrowed_at,
       row_number() OVER (
           PARTITION BY l.member_id
           ORDER BY l.borrowed_at, l.id
       ) AS sequence_for_member,
       lag(l.borrowed_at) OVER (
           PARTITION BY l.member_id
           ORDER BY l.borrowed_at, l.id
       ) AS previous_loan_at
FROM loan AS l;
```

Uma janela possui três decisões:

- `PARTITION BY`: reinicia cálculo por qual conjunto;
- `ORDER BY`: em qual sequência lógica;
- frame: quais linhas relativas participam do cálculo.

### Ranking não é uma coisa só

Para valores `100, 100, 80`:

- `row_number()`: 1, 2, 3 — sempre posição única;
- `rank()`: 1, 1, 3 — empate deixa lacuna;
- `dense_rank()`: 1, 1, 2 — empate sem lacuna.

```sql
WITH per_book AS (
    SELECT b.id,
           b.genre,
           b.title,
           count(l.id) AS total_loans
    FROM book AS b
    LEFT JOIN copy AS c ON c.book_id = b.id
    LEFT JOIN loan AS l ON l.copy_id = c.id
    GROUP BY b.id, b.genre, b.title
),
ranked AS (
    SELECT *,
           dense_rank() OVER (
               PARTITION BY genre
               ORDER BY total_loans DESC
           ) AS position
    FROM per_book
)
SELECT genre, id, title, total_loans, position
FROM ranked
WHERE position <= 3
ORDER BY genre, position, id;
```

Com `dense_rank`, podem existir mais de três linhas por gênero em caso de
empate. Se o requisito exige exatamente no máximo três, use `row_number` com
desempate determinístico.

### Frames: `ROWS` versus `RANGE`

Para total acumulado:

```sql
SELECT event_id,
       occurred_at,
       delta,
       sum(delta) OVER (
           PARTITION BY copy_id
           ORDER BY occurred_at, event_id
           ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
       ) AS running_balance
FROM copy_movement;
```

Especifique `ROWS`: o frame padrão com `ORDER BY` costuma ter semântica de
`RANGE` até os peers (linhas empatadas na ordenação), podendo somar várias de
uma vez. Um desempate único torna a progressão reproduzível.

`last_value` frequentemente surpreende porque retorna o último valor do frame
atual, não necessariamente da partição inteira. Para a partição toda, declare:

```sql
last_value(status) OVER (
    PARTITION BY copy_id
    ORDER BY changed_at, event_id
    ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
)
```

## 5. `EXISTS`, anti-join e subquery correlacionada

`EXISTS` responde à existência e pode parar na primeira correspondência:

```sql
SELECT b.id, b.title
FROM book AS b
WHERE EXISTS (
    SELECT 1
    FROM copy AS c
    JOIN loan AS l ON l.copy_id = c.id
    WHERE c.book_id = b.id
      AND l.borrowed_at >= TIMESTAMPTZ '2026-09-01 00:00:00Z'
);
```

A referência a `b.id` torna a subquery correlacionada. O otimizador pode
transformá-la em semi-join; não presuma que significa um loop ingênuo.

Para ausência:

```sql
SELECT m.id, m.display_name
FROM member AS m
WHERE NOT EXISTS (
    SELECT 1
    FROM loan AS l
    WHERE l.member_id = m.id
);
```

Evite `NOT IN (subquery)` se a expressão puder conter `NULL`; uma única
ausência pode tornar todas as comparações `UNKNOWN`.

## 6. `LATERAL`: subconsulta por linha externa

`LATERAL` permite que uma subquery em `FROM` use colunas anteriores. Exemplo:
último empréstimo de cada membro, preservando quem nunca emprestou:

```sql
SELECT m.id,
       m.display_name,
       latest.loan_id,
       latest.borrowed_at
FROM member AS m
LEFT JOIN LATERAL (
    SELECT l.id AS loan_id, l.borrowed_at
    FROM loan AS l
    WHERE l.member_id = m.id
    ORDER BY l.borrowed_at DESC, l.id DESC
    LIMIT 1
) AS latest ON true
ORDER BY m.id;
```

Com índice `(member_id, borrowed_at DESC, id DESC)`, esse padrão pode ser
eficiente. Compare-o a window function sobre todos os empréstimos; a melhor
forma depende de seletividade e volume.

## 7. Operações de conjunto

- `UNION`: concatena e remove duplicatas;
- `UNION ALL`: concatena preservando duplicatas;
- `INTERSECT`: mantém linhas presentes nos dois lados;
- `EXCEPT`: linhas do primeiro lado ausentes no segundo.

As consultas devem ter o mesmo número de colunas e tipos compatíveis. Prefira
`UNION ALL` quando duplicatas são permitidas ou impossíveis por construção:
removê-las requer trabalho adicional.

Para reconciliar conjuntos:

```sql
SELECT source_id
FROM imported_member
EXCEPT
SELECT external_id
FROM member;
```

Isso responde quais IDs importados ainda não existem, mas não explica diferenças
de atributos; a reconciliação completa precisa comparar conteúdo e versão.

## 8. Agregações avançadas

`FILTER` evita vários `CASE`:

```sql
SELECT member_id,
       count(*) AS total,
       count(*) FILTER (WHERE returned_at IS NULL) AS open,
       max(borrowed_at) AS last_borrowed_at
FROM loan
GROUP BY member_id;
```

`GROUPING SETS` calcula vários níveis:

```sql
SELECT b.genre,
       date_trunc('month', l.borrowed_at) AS month,
       count(*) AS loans,
       grouping(b.genre) AS genre_is_total,
       grouping(date_trunc('month', l.borrowed_at)) AS month_is_total
FROM loan AS l
JOIN copy AS c ON c.id = l.copy_id
JOIN book AS b ON b.id = c.book_id
GROUP BY GROUPING SETS (
    (b.genre, date_trunc('month', l.borrowed_at)),
    (b.genre),
    ()
)
ORDER BY b.genre NULLS LAST, month NULLS LAST;
```

`NULL` pode ser dado real ou marcador de total; `grouping(...)` diferencia.
Não use esse recurso se três consultas simples forem mais claras ao consumidor.

## 9. Upsert e concorrência

O padrão “`SELECT` para verificar; depois `INSERT`” possui corrida. Use a
constraint como árbitro:

```sql
INSERT INTO member (display_name, email)
VALUES ($1, $2)
ON CONFLICT (email)
DO UPDATE
SET display_name = EXCLUDED.display_name
WHERE member.display_name IS DISTINCT FROM EXCLUDED.display_name
RETURNING id, display_name, email;
```

Decisões obrigatórias:

- qual constraint identifica conflito;
- se conflito é erro, ignorado ou atualização;
- quais campos podem mudar;
- se ausência de alteração deve retornar linha;
- como autorização é verificada;
- qual evento/auditoria corresponde ao resultado.

Se a condição do `DO UPDATE ... WHERE` for falsa, nenhuma linha é retornada.
Não interprete isso automaticamente como recurso inexistente.

`MERGE` atende sincronizações mais gerais, mas não é um substituto automático
para `INSERT ... ON CONFLICT`; garantias e concorrência dependem das cláusulas.
Leia a documentação da versão e teste corridas reais.

## 10. JSONB dentro do modelo relacional

JSONB é útil para atributos opcionais e esparsos que pertencem ao agregado:

```sql
ALTER TABLE book
ADD COLUMN metadata jsonb NOT NULL DEFAULT '{}'::jsonb,
ADD CONSTRAINT book_metadata_object
    CHECK (jsonb_typeof(metadata) = 'object');

UPDATE book
SET metadata = jsonb_build_object(
    'language', 'pt-BR',
    'tags', jsonb_build_array('dados', 'sql')
)
WHERE id = 7;

SELECT id, title
FROM book
WHERE metadata @> '{"language":"pt-BR"}'::jsonb;
```

Um índice GIN pode apoiar contenção:

```sql
CREATE INDEX book_metadata_gin_idx
ON book USING gin (metadata);
```

Não esconda em JSONB:

- foreign keys e identidade central;
- campos usados em quase toda consulta;
- valores com forte regra de tipo/unicidade;
- estado que precisa mudar atomicamente com linhas externas sem estratégia.

O documento também precisa de limite de tamanho, validação, versão e migration.
Índice GIN não torna qualquer expressão JSON rápida; confirme operador e plano.

## 11. Views e materialized views

Uma view armazena a consulta, não o resultado:

```sql
CREATE VIEW open_loan_summary AS
SELECT l.id AS loan_id,
       l.copy_id,
       l.member_id,
       l.borrowed_at,
       l.due_at
FROM loan AS l
WHERE l.returned_at IS NULL;
```

Usos:

- encapsular uma consulta estável;
- fornecer camada de compatibilidade;
- restringir colunas/linhas em conjunto com privilégios e configuração correta;
- facilitar consumidores de relatório.

Uma materialized view armazena resultado:

```sql
CREATE MATERIALIZED VIEW monthly_loan_count AS
SELECT date_trunc('month', borrowed_at) AS month,
       count(*) AS loans
FROM loan
GROUP BY date_trunc('month', borrowed_at);
```

Ela fica obsoleta até `REFRESH MATERIALIZED VIEW`. Refresh concorrente exige,
entre outros requisitos, um índice único apropriado e ainda tem custo. Defina
freshness, agenda, monitoramento e comportamento durante falha.

Uma view é contrato: remover coluna, mudar significado ou alterar cardinalidade
pode quebrar consumidores tanto quanto mudar uma API.

## 12. Funções e triggers

Funções no banco podem aproximar uma operação dos dados e reduzir viagens.
Triggers executam automaticamente em eventos de tabela. Bons casos incluem:

- constraint que não pode ser expressa diretamente, com muito cuidado;
- auditoria local obrigatória e transacional;
- manutenção simples de dado derivado local;
- compatibilidade temporária durante migration.

Riscos:

- efeito não visível na chamada da aplicação;
- ordem e recursão entre triggers;
- trabalho multiplicado em operações em lote;
- lógica duplicada entre banco e serviços;
- deploy/versionamento acoplado;
- acesso externo indevido dentro de transação.

Prefira `DEFAULT`, coluna gerada, `CHECK`, foreign key ou expressão no comando
quando forem suficientes. Nunca faça chamada HTTP a partir de trigger de uma
transação crítica.

## 13. Paginação keyset

`OFFSET` precisa visitar/descartar linhas anteriores e muda sob inserções.
Keyset continua a partir da última chave observada.

Para ordem decrescente:

```sql
SELECT id, title, published_year
FROM book
WHERE (published_year, id) < ($1, $2)
ORDER BY published_year DESC, id DESC
LIMIT 21;
```

Isso funciona quando os campos do cursor são não nulos e a comparação acompanha
a direção. Para primeira página, omita o `WHERE`. Solicite `limite + 1`:

1. devolva no máximo `limite`;
2. se veio a linha extra, há próxima página;
3. codifique as chaves da última linha devolvida no próximo cursor.

### Cursor é parte do contrato

Um cursor deve conter:

- valores de ordenação e desempate;
- versão do formato;
- filtros/escopo quando necessário;
- assinatura/MAC ou validação rígida se adulteração importa;
- tipos e tamanho limitados.

Base64 é codificação, não proteção. Não coloque segredo no cursor.

Exemplo conceitual antes da codificação:

```json
{
  "v": 1,
  "publishedYear": 2025,
  "id": 481,
  "sort": "-publishedYear,-id"
}
```

### `NULL` e direção reversa

Comparações de linha com `NULL` resultam em desconhecido. Normalize uma chave
não nula, separe páginas ou escreva predicado correspondente à política
`NULLS FIRST/LAST`. Paginação para trás exige inverter comparação e ordenação
na consulta e reordenar a resposta; não improvise apenas trocando `<` por `>`.

Keyset dá continuidade estável na ordem, mas não cria snapshot entre requisições.
Atualizar uma coluna usada na ordenação pode mover a linha. Se o requisito exige
foto imutável, use uma revisão/snapshot ou filtre por fronteira temporal definida.

## 14. Consultas em lote

Enviar uma consulta por item cria N+1. Prefira uma operação set-based:

```sql
SELECT c.id, c.book_id, c.status
FROM copy AS c
WHERE c.book_id = ANY ($1::bigint[]);
```

Para grandes importações, staging table e `COPY` podem superar milhares de
`INSERT` individuais. Ainda valide linhas, limite lote, monitore WAL/locks e
trate parcialidade no limite transacional planejado.

## 15. Erros recorrentes

- escrever uma CTE enorme sem declarar o grão de cada etapa;
- assumir que CTE sempre materializa ou nunca materializa;
- recursão sem limite e detecção de ciclo;
- usar window function sem desempate determinístico;
- ignorar frame de acumulado ou `last_value`;
- usar `NOT IN` com conjunto anulável;
- atualizar no upsert campos que o conflito não autoriza;
- transformar JSONB em “gaveta” sem schema;
- usar trigger para esconder integração externa;
- expor cursor como SQL, confiar em Base64 ou esquecer `NULL`;
- chamar keyset de snapshot consistente sem sustentar essa garantia.

## 16. Exercícios progressivos

### Nível 1 — composição

1. Crie CTE “uma linha por obra” com quantidade de exemplares e empréstimos.
2. Liste membros sem empréstimo com `NOT EXISTS`.
3. Reescreva uma subquery com CTE e compare legibilidade e `EXPLAIN`.

### Nível 2 — análise

1. Numere empréstimos por membro com ordem total.
2. Calcule intervalo desde o empréstimo anterior com `lag`.
3. Gere top 3 por gênero e explique a escolha entre `rank`,
   `dense_rank` e `row_number`.
4. Crie saldo acumulado e demonstre a diferença entre `ROWS` e `RANGE`
   usando timestamps empatados.

### Nível 3 — estrutura

1. Modele categorias hierárquicas e percorra-as com limite/ciclo.
2. Adicione metadados JSONB com constraint de objeto.
3. Compare índice GIN e varredura usando consulta seletiva.
4. Crie materialized view, defina freshness máxima e procedimento de refresh.

### Nível 4 — contrato e concorrência

1. Implemente upsert e escreva a política de cada conflito.
2. Implemente cursor opaco para ordem total, limite máximo e linha extra.
3. Teste inserções entre páginas e registre o comportamento.
4. Defina como tratar campos de ordenação mutáveis e cursores adulterados.

## Critério de conclusão

- [ ] Toda etapa complexa possui grão e chave documentados.
- [ ] CTE recursiva tem parada, detecção de ciclo e limite operacional.
- [ ] Window functions possuem partição, ordem total e frame consciente.
- [ ] Sei escolher `EXISTS`, agregação prévia ou `LATERAL`.
- [ ] A política de upsert não permite alteração indevida.
- [ ] JSONB preserva schema, limite e propriedade do dado.
- [ ] Views e materialized views têm contrato/freshness documentados.
- [ ] A paginação keyset trata desempate, `NULL`, cursor e mutações.
- [ ] Comparei os resultados esperados antes de comparar desempenho.

O próximo capítulo mostra o que muda quando várias sessões executam essas
operações ao mesmo tempo:
[Transações e concorrência](04-transacoes-concorrencia.md).
