# Exercícios SQL

Execute na ordem:

1. [`001_schema.sql`](../laboratorios/sql/001_schema.sql) cria tabelas e invariantes;
2. [`002_seed.sql`](../laboratorios/sql/002_seed.sql) carrega dados fictícios;
3. [`003_queries.sql`](../laboratorios/sql/003_queries.sql) contém exemplos verificáveis;
4. [`004_assertions.sql`](../laboratorios/sql/004_assertions.sql) prova dados, constraints e
   resultados esperados, falhando com código diferente de zero em divergências.

O [Lab 01](../laboratorios/lab-01-modelagem-sql.md) orienta modelagem e invariantes; o
[Lab 02](../laboratorios/lab-02-transacoes-indices.md) cobre concorrência e planos. O runner
[`testar-laboratorios.sh`](../laboratorios/testar-laboratorios.sh) executa tudo em um
projeto Compose efêmero.

Depois escreva sem consultar:

- membros sem empréstimo;
- livros nunca emprestados;
- três autores com mais obras;
- empréstimos atrasados e dias de atraso;
- ranking de popularidade por gênero;
- saldo acumulado de empréstimos/devoluções por exemplar.

Para cada consulta, declare o grão de uma linha do resultado e teste um caso
com `NULL`, duplicidade e conjunto vazio.
