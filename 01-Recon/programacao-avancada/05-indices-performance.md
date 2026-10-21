# Índices e desempenho orientado por evidência

Um índice troca recursos: mantém uma representação adicional para evitar parte
do trabalho de leitura, pagando com espaço, memória, WAL, manutenção e custo em
cada escrita. “Criar índice na coluna do filtro” não é método de otimização. O
método é definir um SLO, medir uma consulta representativa, compreender o plano,
formular uma hipótese e comparar o sistema inteiro.

Este capítulo trata principalmente do PostgreSQL. Execute `EXPLAIN ANALYZE` de
escritas e cargas sintéticas somente no laboratório local.

## Objetivos

Ao concluir, você deverá conseguir:

- explicar heap, índice, página e seletividade em nível útil;
- escolher B-tree, GIN, GiST, SP-GiST, BRIN ou Hash pelo operador;
- ordenar colunas de índice composto conforme filtro e ordenação;
- usar índices parciais, por expressão, de cobertura e únicos;
- ler estimativas, tempo, loops, buffers e sorts em `EXPLAIN`;
- reconhecer predicados não sargáveis e o problema N+1;
- medir impacto de leitura e escrita antes de manter um índice;
- documentar hipótese, evidência e rollback de uma otimização.

## 1. Modelo físico mínimo

No PostgreSQL, uma tabela comum usa um **heap** dividido em páginas. Uma B-tree
armazena chaves ordenadas e referências às tuplas do heap. Encontrar a chave no
índice não significa que a linha inteira está ali nem que ela é visível ao
snapshot: frequentemente o executor visita também o heap.

```text
predicado
  -> percorre páginas da B-tree
  -> encontra referências candidatas
  -> visita páginas do heap
  -> verifica visibilidade MVCC e filtro residual
  -> devolve colunas
```

Um `Index Only Scan` pode responder pelas colunas do índice, mas ainda depende
do visibility map para evitar visitas ao heap. Escrita recente e vacuum
insuficiente podem aumentar heap fetches mesmo com índice de cobertura.

### O que o índice compra

- localizar pequena fração da tabela;
- entregar linhas em uma ordem útil;
- apoiar join por chave;
- verificar unicidade;
- responder por colunas cobertas em certos planos.

### O que o índice cobra

- espaço em disco e cache;
- atualização em `INSERT`, `DELETE` e alguns `UPDATE`;
- mais WAL, replicação e backup;
- vacuum/análise e possível bloat;
- tempo/lock para construir;
- mais alternativas para o planejador avaliar.

Índice sem uso não é neutro.

## 2. Seletividade, cardinalidade e custo

**Cardinalidade** é a quantidade de linhas. **Seletividade** expressa quanto um
predicado reduz o conjunto. Um filtro por chave única retorna no máximo uma
linha e tende a favorecer índice; `status = 'active'` em uma tabela onde 95%
são ativos pode favorecer varredura sequencial.

O planejador estima custos usando estatísticas:

- quantidade de linhas e páginas;
- número aproximado de valores distintos;
- frequência de valores comuns;
- histogramas;
- fração de `NULL`;
- correlação com ordem física;
- estatísticas estendidas, se criadas.

Ele não “sabe” o resultado real antes de executar. Estimativa errada pode levar
a join, scan ou ordem inadequados.

```sql
ANALYZE loan;
```

Autovacuum normalmente coleta estatísticas. Após carga atípica, `ANALYZE`
planejado pode ser necessário. Não aumente alvo de estatística globalmente sem
medir custo de coleta e planejamento.

## 3. Estruturas de índice do PostgreSQL

| Tipo | Operações/casos típicos | Atenção |
|---|---|---|
| B-tree | igualdade, faixa, ordenação, prefixo | padrão para escalares |
| Hash | igualdade | B-tree costuma ser mais versátil |
| GIN | arrays, JSONB, full text, muitos valores por item | escrita/manutenção mais caras |
| GiST | ranges, geometria, nearest-neighbor, extensível | semântica depende da operator class |
| SP-GiST | dados particionáveis, tries, pontos | útil para distribuições específicas |
| BRIN | tabelas enormes com correlação física | aproximado por ranges de páginas |

O tipo de coluna sozinho não decide. O **operador** da consulta deve ser
suportado pela operator class do índice. Um GIN para `jsonb` pode atender um
operador e não outro.

### B-tree

```sql
CREATE INDEX loan_member_borrowed_idx
ON loan (member_id, borrowed_at DESC, id DESC);
```

Atende bem:

```sql
SELECT id, borrowed_at, due_at
FROM loan
WHERE member_id = $1
  AND (borrowed_at, id) < ($2, $3)
ORDER BY borrowed_at DESC, id DESC
LIMIT 21;
```

Igualdade em `member_id`, seguida da faixa/ordem, corresponde ao índice.

### BRIN

Para uma tabela append-only enorme cujo `occurred_at` cresce junto da posição
física:

```sql
CREATE INDEX event_occurred_brin_idx
ON event USING brin (occurred_at)
WITH (pages_per_range = 64);
```

BRIN guarda resumos por faixa de páginas, é pequeno e pode descartar regiões,
mas não localiza cada linha. Se os timestamps estiverem fisicamente aleatórios,
o benefício cai.

## 4. Índices compostos

A ordem das colunas expressa padrões de acesso. Heurística para B-tree:

1. colunas de igualdade relevantes;
2. coluna de faixa;
3. colunas necessárias para ordenação/desempate;
4. eventualmente colunas de cobertura em `INCLUDE`.

Não aplique “a coluna mais seletiva primeiro” como lei. O conjunto de consultas,
o prefixo utilizável, a ordenação e a distribuição importam.

```sql
CREATE INDEX loan_member_open_due_idx
ON loan (member_id, due_at, id)
WHERE returned_at IS NULL;
```

Consulta compatível:

```sql
SELECT id, due_at
FROM loan
WHERE member_id = $1
  AND returned_at IS NULL
  AND due_at >= $2
ORDER BY due_at, id
LIMIT 50;
```

O índice `(member_id, due_at, id)` também possui prefixo `member_id`. Em
geral, não atende tão diretamente consultas apenas por `due_at`, pois a
primeira coluna não foi restringida. Versões podem usar técnicas como skip scan
em certos casos; confirme no plano, não transforme exceção em design.

### Direção e `NULL`

B-tree pode ser percorrida para frente ou para trás. Em índice multicoluna com
direções mistas, declare a ordem necessária:

```sql
CREATE INDEX book_year_title_idx
ON book (published_year DESC NULLS LAST, title ASC, id ASC);
```

A ordenação da consulta precisa corresponder semanticamente. Políticas de
`NULLS FIRST/LAST` afetam tanto plano quanto paginação.

## 5. Índices parciais

Um índice parcial contém somente linhas que satisfazem o predicado:

```sql
CREATE INDEX loan_open_due_idx
ON loan (due_at, id)
WHERE returned_at IS NULL;
```

É valioso quando consultas frequentes usam um subconjunto pequeno e estável.
Também pode impor unicidade condicional:

```sql
CREATE UNIQUE INDEX loan_one_open_per_copy_idx
ON loan (copy_id)
WHERE returned_at IS NULL;
```

O planejador precisa provar que o predicado da consulta implica o do índice.
Expressões logicamente equivalentes para um humano nem sempre são reconhecidas,
e planos genéricos parametrizados podem limitar essa prova. Teste a consulta
real preparada pelo driver.

Não use índice parcial para excluir arbitrariamente valores comuns sem entender
que consultas sem o predicado não poderão aproveitá-lo.

## 6. Índices por expressão

Se a busca aplica sempre uma expressão:

```sql
CREATE UNIQUE INDEX member_email_lower_unique_idx
ON member (lower(email));

SELECT id, display_name
FROM member
WHERE lower(email) = lower($1);
```

A expressão da consulta precisa corresponder ao índice. Antes disso, decida a
semântica: lowercase simples não resolve todos os casos Unicode nem define por
si só regras de email. Alternativas incluem normalizar na borda e armazenar uma
coluna canônica ou usar tipo/collation apropriado.

Índice por expressão aumenta custo de escrita e acopla consultas à expressão.
Documente-a como parte do modelo.

## 7. Cobertura com `INCLUDE`

```sql
CREATE INDEX book_isbn_cover_idx
ON book (isbn)
INCLUDE (id, title, published_year);
```

As colunas em `INCLUDE` não participam da busca/ordem nem da unicidade; apenas
podem cobrir a saída. Isso pode permitir `Index Only Scan`, dependendo da
visibilidade. Colunas largas incham o índice e reduzem fan-out/cache. Cubra uma
consulta crítica medida, não todas as colunas.

## 8. Índices únicos são integridade

```sql
CREATE UNIQUE INDEX member_email_unique_idx
ON member (email);
```

Além de desempenho, esse índice arbitra escritores concorrentes. A semântica de
`NULL` importa: por padrão, múltiplos `NULL` são distintos em unique index;
PostgreSQL oferece `NULLS NOT DISTINCT` quando a regra considera ausência igual.

Não remova índice/constraint única apenas porque uma ferramenta o marcou como
“pouco lido”: seu uso principal pode ser rejeitar duplicata.

## 9. `EXPLAIN`: estimativa versus execução

```sql
EXPLAIN (ANALYZE, BUFFERS, WAL, SETTINGS, FORMAT TEXT)
SELECT l.id, l.due_at
FROM loan AS l
WHERE l.member_id = 7
  AND l.returned_at IS NULL
ORDER BY l.due_at, l.id
LIMIT 20;
```

- `EXPLAIN` sem `ANALYZE`: planeja, não executa;
- `ANALYZE`: executa de verdade;
- `BUFFERS`: mostra páginas em cache/lidas/sujas;
- `WAL`: mostra geração de WAL em operações que escrevem;
- `SETTINGS`: inclui parâmetros não padrão relevantes.

Nunca use `EXPLAIN ANALYZE DELETE/UPDATE/INSERT` em dados importantes achando
que é simulação. Em laboratório, envolva em `BEGIN; ...; ROLLBACK;` quando a
semântica permitir, sabendo que a execução ainda gera trabalho, locks e WAL.

### Como ler

Comece de dentro para fora e observe:

- `cost=startup..total`: unidade interna estimada, não milissegundos;
- `rows`: linhas estimadas por execução do nó;
- `actual time`: tempo até primeira/última linha por loop;
- `actual rows`: linhas reais por loop;
- `loops`: quantas vezes o nó executou;
- `Rows Removed by Filter`: candidatas descartadas;
- `Buffers: shared hit/read`: páginas em cache versus solicitadas ao sistema;
- método de sort e uso de memória/disco;
- condições `Index Cond`, `Filter` e `Recheck Cond`;
- tempo de planejamento e execução.

Para estimar trabalho total de um nó, considere `actual rows × loops`. O tempo
de nós inclui descendentes em muitos formatos; não some todos cegamente.

### Scan não é diagnóstico automático

- `Seq Scan`: pode ser ótimo para tabela pequena ou grande parte das linhas;
- `Index Scan`: usa índice e visita heap;
- `Index Only Scan`: pode evitar parte das visitas ao heap;
- `Bitmap Index Scan` + `Bitmap Heap Scan`: agrupa referências para visitar
  páginas, útil em seletividade intermediária.

“Há Seq Scan” não significa “falta índice”. Compare linhas, páginas e SLO.

## 10. Estimativas erradas

Se o planejador estima 10 linhas e recebe 100 mil, joins e memória podem ser
mal escolhidos. Investigue:

1. estatísticas foram atualizadas após mudança relevante?
2. distribuição possui valores extremamente frequentes?
3. duas colunas são correlacionadas?
4. expressão/função esconde informação?
5. parâmetro preparado recebe distribuições muito diferentes?

Estatísticas estendidas ajudam dependências e correlações:

```sql
CREATE STATISTICS loan_member_status_stats
    (dependencies, mcv)
ON member_id, returned_at
FROM loan;

ANALYZE loan;
```

Crie somente com uma hipótese; elas aumentam coleta e catálogo. Compare a
estimativa antes/depois.

Planos preparados podem ser customizados para parâmetros ou genéricos. Um valor
raro e um valor muito comum podem pedir planos diferentes. Antes de culpar o
índice, capture a forma real da consulta e parâmetros representativos de modo
seguro.

## 11. SARGability

Um predicado é sargável quando pode virar condição de busca compatível com o
índice.

```sql
-- Função sobre a coluna impede uso direto de B-tree simples:
WHERE date(borrowed_at) = DATE '2026-10-03'

-- Faixa sargável e correta para o dia UTC:
WHERE borrowed_at >= TIMESTAMPTZ '2026-10-03 00:00:00Z'
  AND borrowed_at <  TIMESTAMPTZ '2026-10-04 00:00:00Z'
```

Outros problemas:

- cast da coluna em vez do parâmetro;
- cálculo sobre coluna (`price_cents / 100 > 50`);
- wildcard inicial (`LIKE '%termo'`) numa B-tree comum;
- `OR` amplo com ramos de seletividade muito diferente;
- comparação entre tipos incompatíveis.

Às vezes a expressão é o requisito; então índice por expressão, full-text ou
outro modelo pode ser adequado. Não altere semântica só para “usar índice”.

## 12. Joins e memória

Estratégias principais:

- **Nested Loop:** para cada linha externa, busca internas; excelente se o lado
  externo é pequeno e há acesso eficiente;
- **Hash Join:** constrói hash de um lado; bom para igualdade e conjuntos maiores;
- **Merge Join:** percorre entradas ordenadas; útil para igualdade/faixa conforme
  condições e ordem.

Um nested loop com estimativa errada pode fazer milhões de buscas. Um hash que
não cabe em memória cria lotes e I/O. Aumentar `work_mem` globalmente é
perigoso: ele pode ser usado por vários nós e sessões simultaneamente, não uma
vez por servidor.

Otimize primeiro cardinalidade, filtros e índices; ajuste memória com orçamento
de concorrência.

## 13. N+1 na aplicação

Fluxo ruim:

```text
1 query: SELECT * FROM book LIMIT 100
100 queries: SELECT * FROM author ... para cada livro
```

Latência inclui 101 viagens, parsing e aquisição de conexão. Alternativas:

- join controlando multiplicação;
- duas consultas e associação em memória por IDs;
- carregamento em lote com `WHERE id = ANY(...)`;
- dataloader por janela de execução;
- projeção própria quando a leitura domina e a sincronização está definida.

Um join gigantesco não é automaticamente melhor: autores × exemplares podem
duplicar payload. Meça número de queries, linhas transferidas, bytes e tempo.

## 14. Escrita, HOT update e bloat

Cada índice relevante precisa ser mantido. Atualizar coluna indexada normalmente
impede HOT (Heap-Only Tuple), que poderia evitar novas entradas nos índices sob
condições específicas. Muitos índices tornam updates mais caros.

`DELETE` e `UPDATE` deixam versões mortas para vacuum. Cargas e transações
longas podem gerar bloat em heap e índice. Antes de executar `REINDEX`,
`VACUUM FULL` ou ferramenta de reorganização:

- meça o problema;
- entenda lock/espaço/WAL;
- teste réplica e janela;
- tenha rollback e monitoramento.

Não rode manutenção destrutiva ou pesada como “otimização genérica”.

## 15. Observabilidade de consultas

Uma análise profissional combina:

- latência p50/p95/p99 por operação;
- throughput e concorrência;
- tempo esperando conexão e lock;
- chamadas, tempo total/médio e linhas;
- CPU, I/O, cache e WAL;
- planos amostrados sem dados sensíveis;
- deploy/schema/estatísticas no mesmo período.

`pg_stat_statements` (quando habilitado) agrega consultas normalizadas. Logs de
consulta lenta ajudam, mas parâmetros podem conter dados pessoais; aplique
redação e acesso restrito.

Um plano de ambiente de desenvolvimento com cache quente não representa produção
com dados, distribuição, concorrência e hardware diferentes.

## 16. Processo reproduzível de otimização

1. defina SLO e impacto do problema;
2. capture a forma da query, versão, schema e distribuição;
3. reproduza com dados sintéticos representativos;
4. obtenha baseline com múltiplas execuções e estado de cache registrado;
5. leia plano e identifique maior trabalho/erro de estimativa;
6. formule uma hipótese específica;
7. altere uma variável;
8. compare leitura **e** escrita, disco, WAL e concorrência;
9. teste casos comuns, raros e vazios;
10. implante de modo observável e reversível;
11. registre resultado e remova índice experimental sem utilidade.

Tempo menor uma vez não é evidência suficiente. Ruído de cache, compilação,
autovacuum e outros processos precisa ser considerado.

## 17. Laboratório progressivo

Crie volume fictício somente na base local:

```sql
INSERT INTO member (display_name, email, joined_at)
SELECT 'Pessoa ' || n,
       'pessoa' || n || '@example.test',
       TIMESTAMPTZ '2026-01-01 00:00:00Z'
         + (n % 365) * INTERVAL '1 day'
FROM generate_series(1000, 100999) AS g(n);
```

Use uma transação e confirme a contagem antes do commit. Não presuma IDs fixos
se a fixture já consumiu a sequência.

### Experimentos

1. Consulte um email raro antes/depois de índice e registre plano/buffers.
2. Consulte um atributo presente em quase todas as linhas; explique o Seq Scan.
3. Compare índice `(member_id, borrowed_at DESC, id DESC)` a índices isolados
   para a paginação correspondente.
4. Crie índice parcial de empréstimos abertos e teste consulta que implica — e
   outra que não implica — seu predicado.
5. Demonstre consulta não sargável por data e reescreva como faixa.
6. Adicione cinco índices candidatos, meça lote de inserção e remova os sem ganho.
7. Simule N+1 e substitua por lote; compare queries, bytes e latência.
8. Force uma estimativa ruim com colunas correlacionadas e teste estatística
   estendida.

## Critério de conclusão

- [ ] Cada índice está ligado a consulta, operador e SLO específicos.
- [ ] Consigo explicar por que a ordem de um índice composto atende o predicado.
- [ ] Diferencio índice parcial, por expressão, cobertura e integridade única.
- [ ] Leio estimado versus real, loops, buffers, filtros e sorts no plano.
- [ ] Não classifico Seq Scan como erro sem considerar seletividade.
- [ ] Sei encontrar predicado não sargável e preservar a semântica ao corrigi-lo.
- [ ] Meço custo de escrita, WAL e espaço, não apenas uma leitura.
- [ ] Detecto N+1 sem trocar por join que multiplica dados.
- [ ] Toda otimização possui baseline, hipótese, comparação e rollback.

Agora compare essas garantias com outras famílias em
[NoSQL: modelos e decisões](06-nosql-modelos.md).
