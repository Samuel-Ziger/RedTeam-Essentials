# Modelagem relacional: fatos, chaves e invariantes

Modelar não é desenhar caixas que imitam telas. É decidir quais fatos existem,
como são identificados e quais estados o banco deve recusar. Um bom modelo
permite que consultas diferentes combinem os mesmos fatos sem ambiguidades e
que escritores concorrentes preservem as regras essenciais.

Este capítulo usa sintaxe do PostgreSQL. Os conceitos de relação, dependência
funcional e normalização são gerais; detalhes de tipos, constraints e migrations
variam entre SGBDs.

## Objetivos

Ao concluir, você deverá conseguir:

- converter linguagem do domínio em entidades, relacionamentos e invariantes;
- escolher chaves naturais e substitutas sem perder unicidade de negócio;
- representar cardinalidades e participação obrigatória;
- normalizar um modelo até 3FN/BCNF e reconhecer quando desnormalizar;
- tratar dinheiro, tempo, texto e `NULL` com semântica explícita;
- aplicar constraints e ações referenciais conscientemente;
- planejar migrations compatíveis, observáveis e reversíveis.

## 1. Relação, tupla, atributo e domínio

No modelo relacional, uma **relação** é um conjunto de tuplas. Cada atributo
possui um domínio: valores possíveis e operações coerentes. Em SQL, uma tabela
é a implementação prática mais próxima, embora detalhes como duplicatas e
`NULL` façam SQL não ser idêntico à álgebra relacional pura.

Considere uma biblioteca:

```text
book             = obra intelectual
book_copy        = exemplar físico identificável
member           = pessoa autorizada a emprestar
loan             = empréstimo de um exemplar
author           = autoria independente
book_author      = relação N:N entre obra e autoria
```

“Livro” era ambíguo: pode significar a obra *Dom Casmurro* ou o exemplar com
tombo `EX-0042`. Separar conceitos evita perguntas impossíveis como “o livro
está emprestado?” quando há cinco exemplares.

### Do enunciado à regra executável

| Regra do domínio | Decisão de modelo |
|---|---|
| ISBN, quando informado, identifica uma edição | `UNIQUE` parcial em `isbn` |
| tombo identifica um exemplar | `asset_code NOT NULL UNIQUE` |
| exemplar pertence a uma obra | foreign key `book_id NOT NULL` |
| devolução não precede retirada | `CHECK (returned_at IS NULL OR returned_at >= loaned_at)` |
| membro pode existir sem empréstimo | participação opcional de `member` em `loan` |
| cada empréstimo tem um membro e exemplar | duas foreign keys `NOT NULL` |

Nem toda regra cabe em um `CHECK` de linha. “Um exemplar não pode ter dois
empréstimos ativos” cruza linhas e requer índice único parcial, exclusão por
intervalo, lock ou outra estratégia atômica.

## 2. Identidade e chaves

- **superchave:** qualquer conjunto de atributos que identifica uma tupla;
- **chave candidata:** superchave mínima;
- **chave primária:** candidata escolhida como identidade principal;
- **chave natural:** deriva do domínio, como um código de ativo;
- **chave substituta:** identificador sem significado de negócio;
- **chave estrangeira:** referencia uma chave candidata de outra relação;
- **chave composta:** usa mais de um atributo.

Uma chave substituta não remove a regra natural:

```sql
CREATE TABLE category (
    id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name text NOT NULL,
    CONSTRAINT category_name_not_blank CHECK (btrim(name) <> ''),
    CONSTRAINT category_name_unique UNIQUE (name)
);
```

Sem `UNIQUE (name)`, duas requisições concorrentes podem criar a mesma
categoria apesar do `id` distinto. A aplicação pode verificar antes para
melhor UX, mas somente a constraint decide sem corrida.

### Sequência, UUID e exposição

Identidades sequenciais são compactas, ordenadas e eficientes em B-tree, mas
revelam aproximadamente o volume se expostas. UUIDs podem ser gerados sem
coordenação e são difíceis de adivinhar, mas ocupam mais espaço e versões
aleatórias fragmentam a localidade de escrita.

Nenhuma delas é autorização. Um UUID imprevisível não concede permissão para
ver o recurso. Também não coloque significado mutável na chave: email, nome e
telefone mudam.

## 3. Cardinalidade e participação

Cardinalidade responde quantas ocorrências podem se relacionar:

- **1:1:** um perfil opcional por conta;
- **1:N:** uma obra possui muitos exemplares;
- **N:N:** uma obra pode ter vários autores e um autor várias obras.

Em SQL:

- 1:N coloca foreign key no lado N;
- 1:1 adiciona `UNIQUE` à foreign key;
- N:N usa uma tabela associativa cuja chave geralmente combina as referências.

```sql
CREATE TABLE author (
    id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    display_name text NOT NULL CHECK (btrim(display_name) <> '')
);

CREATE TABLE book (
    id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    title text NOT NULL CHECK (btrim(title) <> ''),
    isbn text,
    published_on date,
    CONSTRAINT book_isbn_unique UNIQUE (isbn)
);

CREATE TABLE book_author (
    book_id bigint NOT NULL
        REFERENCES book(id) ON DELETE CASCADE,
    author_id bigint NOT NULL
        REFERENCES author(id) ON DELETE RESTRICT,
    author_order smallint NOT NULL CHECK (author_order > 0),
    PRIMARY KEY (book_id, author_id),
    UNIQUE (book_id, author_order)
);
```

`author_order` prova que a tabela associativa pode representar fatos próprios.
Não armazene `"2,7,11"` numa coluna textual: isso perde tipos, integridade,
join eficiente e atualização atômica.

Por padrão, `UNIQUE (isbn)` permite vários `NULL`: obras sem ISBN não entram em
conflito, mas todo ISBN informado continua único. `UNIQUE NULLS NOT DISTINCT`,
disponível em versões recentes do PostgreSQL, permitiria no máximo um `NULL` e
só seria correto se o domínio tratasse todas as ausências como o mesmo valor.

### Ações referenciais

Uma foreign key exige decidir o que ocorre ao apagar/alterar o pai:

- `RESTRICT`/`NO ACTION`: impede apagar enquanto houver referência;
- `CASCADE`: propaga a exclusão/alteração;
- `SET NULL`: preserva o filho removendo a associação;
- `SET DEFAULT`: aplica um padrão válido.

`CASCADE` é apropriado para componentes sem vida independente, como linhas de
uma associação. Em dados históricos ou financeiros, apagar em cascata pode ser
desastroso. Soft delete também não é gratuito: todas as constraints, índices e
consultas precisam considerar o estado de exclusão.

## 4. Dependências funcionais

Escrevemos `X → Y` quando o valor de X determina um único valor de Y. Num
rascunho de pedido:

```text
order_id -> ordered_at, customer_id
customer_id -> customer_name
(order_id, product_id) -> quantity, unit_price_cents
product_id -> current_product_name
```

Uma tabela única:

```text
order_id | ordered_at | customer_id | customer_name |
product_id | current_product_name | quantity | unit_price_cents
```

repete pedido e cliente para cada item. Isso produz:

- **anomalia de atualização:** mudar nome exige alterar várias linhas;
- **anomalia de inserção:** não se registra cliente sem pedido;
- **anomalia de exclusão:** apagar o último item pode apagar o único registro do
  pedido ou cliente.

Dependências ajudam a decompor o modelo com raciocínio, em vez de “criar uma
tabela para cada substantivo” mecanicamente.

## 5. Normalização passo a passo

### Primeira Forma Normal (1FN)

Cada posição contém um valor do domínio definido e não há grupos repetidos.
“Atômico” depende do uso: um endereço pode ser um valor único para entrega, mas
precisa de componentes se o sistema pesquisa cidade ou CEP separadamente.

Evite colunas `phone_1`, `phone_2`, `phone_3`; a cardinalidade real pede uma
relação `member_phone`. Um array pode ser válido se o conjunto for parte de um
agregado limitado e as regras/consultas forem compatíveis.

### Segunda Forma Normal (2FN)

Estando em 1FN, todo atributo não-chave depende da chave composta inteira. Em
`order_item(order_id, product_id, ordered_at, quantity)`, `ordered_at`
depende apenas de `order_id`, portanto pertence a `order`.

Essa forma só adiciona restrição quando há chave candidata composta.

### Terceira Forma Normal (3FN)

Estando em 2FN, atributos não-chave não devem depender transitivamente de uma
chave. Se `order_id → customer_id` e `customer_id → customer_name`, gravar
`customer_name` como dado atual do cliente em `order` cria redundância.

Uma exceção semântica importante: `billing_name_at_purchase` pode ser um
**snapshot histórico**, não uma cópia acidental. O nome deixa claro que não deve
acompanhar futuras mudanças do cadastro.

### Boyce–Codd Normal Form (BCNF)

BCNF exige que todo determinante não trivial seja uma superchave. É mais forte
que 3FN e trata certos casos com chaves candidatas sobrepostas. Em modelos
comuns, chegar conscientemente à 3FN e revisar dependências já elimina grande
parte das anomalias; BCNF importa quando as regras revelam outros determinantes.

### Quando desnormalizar

Desnormalização é uma otimização deliberada, não ausência de modelagem. Só faça
quando houver:

1. consulta crítica medida;
2. custo comprovado no modelo normalizado;
3. proprietário da cópia;
4. mecanismo de sincronização/reconciliação;
5. métrica de divergência;
6. plano de reconstrução e rollback.

Uma materialized view, coluna derivada ou projeção externa pode ser melhor que
espalhar duplicatas editáveis.

## 6. Tipos representam regras

Escolha o tipo mais estreito que representa o domínio, sem otimização prematura:

```sql
CREATE TABLE product (
    id uuid PRIMARY KEY,
    category_id bigint REFERENCES category(id) ON DELETE RESTRICT,
    sku varchar(32) NOT NULL,
    name varchar(120) NOT NULL,
    price_cents bigint NOT NULL,
    stock integer NOT NULL DEFAULT 0,
    version integer NOT NULL DEFAULT 1,
    created_at timestamptz NOT NULL DEFAULT now(),
    updated_at timestamptz NOT NULL DEFAULT now(),
    CONSTRAINT product_sku_unique UNIQUE (sku),
    CONSTRAINT product_sku_not_blank CHECK (btrim(sku) <> ''),
    CONSTRAINT product_name_not_blank CHECK (btrim(name) <> ''),
    CONSTRAINT product_price_nonnegative CHECK (price_cents >= 0),
    CONSTRAINT product_stock_nonnegative CHECK (stock >= 0),
    CONSTRAINT product_version_positive CHECK (version > 0)
);
```

### Dinheiro

Não use `real`/`double precision` para valor financeiro exato: ponto
flutuante binário não representa muitos decimais exatamente. Opções comuns:

- inteiro na menor unidade (`price_cents bigint`), simples para uma moeda cuja
  escala foi definida;
- `numeric(19, 4)`, quando a escala decimal faz parte do domínio.

Valor monetário também precisa de moeda. Se o sistema for multimoeda, modele
`currency_code` e nunca some valores de moedas diferentes sem conversão e
regra temporal de câmbio.

### Tempo

- `date`: data civil, como aniversário;
- `time`: horário sem data, raramente suficiente sozinho;
- `timestamp without time zone`: data/hora civil sem instante global;
- `timestamptz`: instante, normalizado internamente e exibido no timezone da
  sessão.

Para eventos, armazene o instante em `timestamptz` e converta na borda. Não
grave apenas uma abreviação ambígua como “BRT”. Agenda recorrente pode exigir
timezone IANA (`America/Sao_Paulo`) separado, pois regras civis mudam.

### Texto, enumeração e domínio

`varchar(120)` impõe comprimento; não é automaticamente mais rápido que
`text` no PostgreSQL. Estados podem usar `CHECK`, tabela de referência ou
`ENUM`. `ENUM` é forte, mas mudanças de valores exigem estratégia de
migration. Tabela de referência suporta metadados; `CHECK` é simples para
conjunto pequeno e estável.

## 7. `NULL` e lógica de três valores

`NULL` significa valor ausente/desconhecido, não string vazia, zero ou falso.
Comparações comuns resultam em `UNKNOWN`:

```sql
SELECT 1 = NULL;       -- NULL/UNKNOWN
SELECT NULL <> NULL;   -- NULL/UNKNOWN
```

Use:

```sql
SELECT *
FROM loan
WHERE returned_at IS NULL;
```

Consequências importantes:

- `WHERE` mantém apenas expressões `TRUE`; `FALSE` e `UNKNOWN` saem;
- `count(column)` ignora `NULL`; `count(*)` conta linhas;
- `NOT IN` pode virar `UNKNOWN` se a subconsulta contiver `NULL`;
- `IS DISTINCT FROM` compara incluindo `NULL` de forma total;
- uma constraint `CHECK` aceita `TRUE` **ou `UNKNOWN`; combine com
  `NOT NULL` quando ausência for inválida.

Use `NOT NULL` por padrão sempre que ausência não tiver significado explícito.
Evite um `NULL` que possa significar simultaneamente “não informado”, “não se
aplica” e “ainda não calculado”.

## 8. Constraints além do básico

```sql
CREATE TABLE member (
    id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    email text NOT NULL,
    active boolean NOT NULL DEFAULT true,
    CONSTRAINT member_email_unique UNIQUE (email),
    CONSTRAINT member_email_not_blank CHECK (btrim(email) <> '')
);

CREATE TABLE book_copy (
    id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    book_id bigint NOT NULL REFERENCES book(id) ON DELETE RESTRICT,
    asset_code text NOT NULL UNIQUE,
    retired_at timestamptz
);

CREATE TABLE loan (
    id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    copy_id bigint NOT NULL REFERENCES book_copy(id) ON DELETE RESTRICT,
    member_id bigint NOT NULL REFERENCES member(id) ON DELETE RESTRICT,
    loaned_at timestamptz NOT NULL,
    due_at timestamptz NOT NULL,
    returned_at timestamptz,
    CONSTRAINT loan_due_after_start CHECK (due_at > loaned_at),
    CONSTRAINT loan_return_after_start
        CHECK (returned_at IS NULL OR returned_at >= loaned_at)
);

CREATE UNIQUE INDEX loan_one_active_per_copy_idx
ON loan (copy_id)
WHERE returned_at IS NULL;
```

O índice parcial torna “um empréstimo ativo por exemplar” uma decisão atômica,
inclusive sob duas inserções concorrentes. Ainda é preciso traduzir a violação
para um erro de domínio adequado.

Constraints podem ser `DEFERRABLE` quando uma regra precisa ser checada no fim
da transação, mas isso deve ser deliberado. Nomes explícitos facilitam logs,
migrations e mapeamento de erros.

## 9. Migrations sem indisponibilidade desnecessária

Migration é código de produção: versionado, revisado, observável e executado uma
vez por ambiente. “Rollback” nem sempre significa desfazer DDL; para mudanças
destrutivas, restaurar compatibilidade pelo caminho adiante costuma ser mais
seguro.

### Padrão expandir–migrar–contrair

Para substituir `name` por `first_name` e `last_name`:

1. **expandir:** adicionar colunas novas opcionais;
2. implantar código capaz de ler o antigo e escrever ambos;
3. preencher em lotes pequenos, idempotentes e retomáveis;
4. medir linhas pendentes e erros;
5. alterar leitura para os campos novos;
6. parar de escrever o antigo;
7. impor constraints novas com estratégia compatível;
8. **contrair:** remover campo antigo somente após observar todos os consumidores.

Adicionar `NOT NULL DEFAULT <valor>`, construir índice ou alterar tipo pode
reescrever tabela ou bloquear operações dependendo da versão e do comando.
Teste com volume representativo e defina `lock_timeout`/`statement_timeout`
apropriados ao procedimento. Para PostgreSQL, criação concorrente de índice tem
restrições transacionais próprias: consulte a documentação da versão.

### Checklist de migration

- aplicação antiga funciona com schema novo?
- aplicação nova tolera schema durante o backfill?
- leitores assíncronos e relatórios foram inventariados?
- a operação adquire qual lock e por quanto tempo?
- há espaço para tabela, WAL e índice adicionais?
- o backfill pode pausar e continuar sem duplicar efeito?
- qual métrica demonstra conclusão?
- como interromper com segurança?
- backup/restore foi testado para uma mudança irreversível?

## 10. Erros recorrentes

- modelar a resposta JSON diretamente como tabelas;
- usar chave substituta e esquecer a unicidade natural;
- armazenar lista de IDs em texto para evitar N:N;
- aplicar `ON DELETE CASCADE` sem avaliar alcance histórico;
- usar float para dinheiro ou texto para todo tipo;
- confundir `NULL` com vazio e escrever `= NULL`;
- confiar apenas em “consultar se existe e depois inserir”;
- desnormalizar antes de medir e sem reconciliação;
- fazer migration destrutiva no mesmo deploy que exige o novo schema;
- adicionar constraint sem verificar/limpar dados legados.

## 11. Exercícios progressivos

### Nível 1 — descoberta

Modele autores, obras, edições, exemplares, membros e empréstimos. Para cada
relação, registre uma frase do tipo “uma linha representa...”. Marque mínimos e
máximos de cada cardinalidade.

### Nível 2 — dependências

Dada a planilha:

```text
loan_id, member_id, member_name, copy_id, book_title,
loaned_at, due_at, returned_at
```

1. liste dependências funcionais;
2. demonstre uma anomalia de inserção, atualização e exclusão;
3. decomponha até 3FN;
4. prove como as relações podem ser reunidas sem perder os fatos necessários.

### Nível 3 — DDL

Escreva DDL completo com chaves, `NOT NULL`, `UNIQUE`, `CHECK`, foreign
keys e ações de exclusão. Force intencionalmente cinco violações e associe cada
erro à invariante protegida.

### Nível 4 — concorrência e evolução

1. tente criar dois empréstimos ativos para o mesmo exemplar em sessões
   concorrentes; a constraint deve permitir apenas um;
2. planeje a divisão de `member.name` em dois campos usando expandir–contrair;
3. descreva backfill, métrica, timeout, compatibilidade e forma de interrupção;
4. explique por que dividir nomes humanos pode ser um requisito de domínio
   inadequado antes mesmo da migration.

## Critério de conclusão

- [ ] Cada tabela possui significado de linha e chave candidata documentados.
- [ ] Cardinalidades e participação opcional/obrigatória estão justificadas.
- [ ] Regras críticas terminam em constraints ou operação atômica.
- [ ] Consigo decompor um exemplo e explicar 1FN, 2FN, 3FN e BCNF.
- [ ] Sei distinguir cópia acidental de snapshot histórico intencional.
- [ ] Dinheiro, tempo, texto e `NULL` têm semântica explícita.
- [ ] Testei violações de integridade, inclusive uma corrida concorrente.
- [ ] Produzi um plano expandir–migrar–contrair com métricas e rollback seguro.

O próximo capítulo transforma o modelo em operações:
[SQL: fundamentos sólidos](02-sql-fundamentos.md). Execute depois o
[guia executável do laboratório SQL](referencias/GUIA-LAB-SQL.md).
