# Lab 01 — do modelo conceitual ao schema relacional

## Resultado esperado

Você vai explicar o grão de cada tabela, executar um schema PostgreSQL real e
provar que suas invariantes continuam válidas quando a entrada é incorreta. O
objetivo não é decorar `CREATE TABLE`: é transformar regras de domínio em
restrições que sobrevivem a qualquer cliente da aplicação.

## Pré-requisitos e tempo

- capítulos 00, 01 e 02;
- Docker Engine com Compose v2;
- 8 a 12 horas;
- somente dados fictícios e ambiente local sem portas publicadas.

## Materiais executáveis

- [`compose.yaml`](compose.yaml): PostgreSQL e MongoDB em rede interna;
- [`sql/001_schema.sql`](sql/001_schema.sql): tabelas, chaves e índices;
- [`sql/002_seed.sql`](sql/002_seed.sql): conjunto pequeno e determinístico;
- [`sql/003_queries.sql`](sql/003_queries.sql): joins, anti-join e janela;
- [`sql/004_assertions.sql`](sql/004_assertions.sql): testes das invariantes;
- [`testar-laboratorios.sh`](testar-laboratorios.sh): execução efêmera e cleanup.
- [guia dos scripts SQL](../referencias/GUIA-LAB-SQL.md): ordem, desafios e
  critérios para interpretar as consultas.

## Antes de executar

Leia o schema e produza, em texto, este dicionário para cada tabela:

| Pergunta | Exemplo de resposta para `book_author` |
|----------|-----------------------------------------|
| Qual é o grão? | uma associação ordenada entre um livro e um autor |
| Qual identidade? | par `book_id, author_id` |
| O que nunca pode ser nulo? | as duas FKs e `author_order` |
| Que duplicidade é proibida? | mesmo autor ou mesma posição no mesmo livro |
| O que acontece no delete? | vínculo acompanha livro; autor referenciado é protegido |

Repita para `author`, `book`, `copy`, `member` e `loan`. Se você não consegue
descrever uma linha sem usar “dados de…”, o grão ainda está ambíguo.

## Execução reproduzível

A partir da raiz do repositório:

```bash
bash 01-Recon/programacao-avancada/laboratorios/testar-laboratorios.sh \
  --postgres-only
```

O script usa um nome de projeto exclusivo, não publica portas e remove os
volumes que ele próprio criou. O último resultado SQL deve conter
`status=ok`, três livros e três empréstimos.

Para inspeção interativa, suba somente o PostgreSQL:

```bash
cd 01-Recon/programacao-avancada/laboratorios
docker compose up --detach --wait postgres
docker compose exec postgres psql -U course -d course
```

No `psql`, execute `\d book`, `\d loan` e `\di`. Não confunda índice, constraint
e trigger: anote qual objeto garante cada regra.

## Experimentos obrigatórios

Faça cada tentativa dentro de uma transação e termine com `ROLLBACK`:

1. livro com ISBN curto;
2. segundo autor na mesma ordem de um livro;
3. empréstimo cujo vencimento precede a retirada;
4. segundo empréstimo aberto da mesma cópia;
5. exclusão de autor ainda referenciado;
6. membro com e-mail repetido.

Para cada uma, registre:

- SQL enviado;
- SQLSTATE e constraint mencionada;
- camada que rejeitou a escrita;
- como a mesma regra seria vulnerável se existisse apenas na interface.

## Exercício de modelagem

Acrescente reservas de livros sem editar os arquivos originais. Crie
`005_reservation.sql` na sua cópia com:

- identidade da reserva;
- livro e membro;
- instante de criação e expiração;
- status em domínio fechado;
- no máximo uma reserva ativa por par livro/membro;
- índice compatível com “próximas reservas ativas de um livro”.

Escreva ao menos quatro asserções negativas. Não use dados pessoais reais.

## Gate de conclusão

- o runner PostgreSQL termina com código zero;
- você explica o grão e as cardinalidades sem olhar o diagrama;
- seis escritas inválidas são rejeitadas pelo banco;
- seu novo schema pode ser aplicado duas vezes ou documenta explicitamente por
  que é uma migração de uso único;
- o cleanup foi executado com `docker compose down` no ambiente interativo.

Marcar o arquivo como lido não substitui essas evidências.
