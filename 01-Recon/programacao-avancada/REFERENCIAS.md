# Referências, vídeos e comunidades

> Curadoria revisada em **2026-10-03**. O curso local é autocontido. Use as
> fontes externas para aprofundar, confirmar comportamento de versão e conhecer
> outras explicações.

Links com `/current/` acompanham a versão corrente e podem mudar de conteúdo.
Ao investigar comportamento, troque `current` pelo major executado no
laboratório. Nesta revisão, a documentação corrente do PostgreSQL é a 18; o
Compose permanece fixado também por tag e digest para tornar a prática
reproduzível.

## Como pesquisar uma dúvida

1. reduza o problema a schema, dados e consulta mínimos;
2. registre versão exata do servidor, driver e framework;
3. use `EXPLAIN`/logs/mensagem completa, removendo segredos;
4. consulte primeiro a documentação daquela versão;
5. reproduza a resposta antes de adotá-la;
6. verifique custo, concorrência e comportamento de falha.

## PostgreSQL e SQL

- [Documentação atual do PostgreSQL](https://www.postgresql.org/docs/current/).
- [Tutorial oficial](https://www.postgresql.org/docs/current/tutorial.html).
- [Linguagem SQL](https://www.postgresql.org/docs/current/sql.html).
- [Data definition e constraints](https://www.postgresql.org/docs/current/ddl.html).
- [Tutorial de transações](https://www.postgresql.org/docs/current/tutorial-transactions.html).
- [Controle de concorrência](https://www.postgresql.org/docs/current/mvcc.html).
- [Níveis de isolamento](https://www.postgresql.org/docs/current/transaction-iso.html).
- [Locks explícitos](https://www.postgresql.org/docs/current/explicit-locking.html).
- [Índices](https://www.postgresql.org/docs/current/indexes.html).
- [`EXPLAIN`](https://www.postgresql.org/docs/current/using-explain.html).
- [Estatísticas usadas pelo planner](https://www.postgresql.org/docs/current/planner-stats.html).
- [Monitoramento de atividade](https://www.postgresql.org/docs/current/monitoring-stats.html).
- [Backup e restore](https://www.postgresql.org/docs/current/backup.html).
- [Matriz oficial de versões suportadas](https://www.postgresql.org/support/versioning/).

## MongoDB e PyMongo

- [MongoDB Manual](https://www.mongodb.com/docs/manual/).
- [Plataformas suportadas e compatibilidade de kernel](https://www.mongodb.com/docs/manual/administration/production-notes/#platform-support-notes).
- [Modelagem de dados](https://www.mongodb.com/docs/manual/data-modeling/).
- [Consistência de dados](https://www.mongodb.com/docs/manual/data-modeling/data-consistency/).
- [Atomicidade e transações](https://www.mongodb.com/docs/manual/core/write-operations-atomicity/).
- [Índices](https://www.mongodb.com/docs/manual/indexes/).
- [`explain` e resultados de execução](https://www.mongodb.com/docs/manual/reference/explain-results/).
- [Aggregation pipeline](https://www.mongodb.com/docs/manual/core/aggregation-pipeline/).
- [Transações](https://www.mongodb.com/docs/manual/core/transactions/).
- [Schema validation](https://www.mongodb.com/docs/manual/core/schema-validation/).
- [Padrões de schema](https://www.mongodb.com/docs/manual/data-modeling/design-patterns/).
- [Read concern](https://www.mongodb.com/docs/manual/reference/read-concern/)
  e [write concern](https://www.mongodb.com/docs/manual/reference/write-concern/).
- [Driver oficial PyMongo](https://www.mongodb.com/docs/languages/python/pymongo-driver/current/).
- [Tutorial oficial FastAPI + PyMongo em português](https://www.mongodb.com/pt-br/docs/languages/python/pymongo-driver/current/integrations/fastapi-integration/).

## HTTP e APIs

- [RFC 9110 — HTTP Semantics](https://www.rfc-editor.org/rfc/rfc9110.html).
- [RFC 9111 — HTTP Caching](https://www.rfc-editor.org/rfc/rfc9111.html).
- [RFC 9457 — Problem Details](https://www.rfc-editor.org/rfc/rfc9457.html).
- [RFC 8259 — JSON](https://www.rfc-editor.org/rfc/rfc8259.html).
- [OpenAPI Specification](https://spec.openapis.org/oas/latest.html).
- [Índice de versões OpenAPI](https://spec.openapis.org/oas/). A especificação
  e o ecossistema não avançam necessariamente juntos; confirme o dialeto
  aceito pelo gerador, validador e consumidor usados no projeto.
- [FastAPI Tutorial](https://fastapi.tiangolo.com/tutorial/).
- [FastAPI Dependencies](https://fastapi.tiangolo.com/tutorial/dependencies/).
- [FastAPI Testing](https://fastapi.tiangolo.com/tutorial/testing/).
- [FastAPI release notes](https://fastapi.tiangolo.com/release-notes/).
- [MDN HTTP](https://developer.mozilla.org/en-US/docs/Web/HTTP).

No RFC 9110, leia especialmente métodos seguros/idempotentes, validators e
conditional requests. Uma `ETag` não impede lost update sozinha: a escrita
precisa exigir e avaliar uma precondição, como `If-Match`, antes do efeito.

## Drivers nas cinco linguagens

- [psycopg 3](https://www.psycopg.org/psycopg3/docs/).
- [PostgreSQL JDBC](https://jdbc.postgresql.org/documentation/).
- [libpq para C](https://www.postgresql.org/docs/current/libpq.html).
- [Npgsql para .NET](https://www.npgsql.org/doc/).
- [node-postgres](https://node-postgres.com/).
- [Drivers oficiais do MongoDB](https://www.mongodb.com/docs/drivers/) — C, C#,
  Java, Node.js, Python e outras linguagens.
- [`httpx2` no PyPI](https://pypi.org/project/httpx2/) — cliente mantido pela
  Pydantic usado pelos testes atuais do FastAPI; confira o pacote e a versão
  antes de instalar porque o nome difere do projeto histórico `httpx`.

## Segurança e operação

- [OWASP API Security Top 10](https://owasp.org/API-Security/).
- [OWASP API Security Top 10:2023](https://owasp.org/API-Security/editions/2023/en/0x11-t10/).
- [OWASP Authentication Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html).
- [OWASP Authorization Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html).
- [OAuth 2.0 Security Best Current Practice — RFC 9700](https://www.rfc-editor.org/rfc/rfc9700.html).
- [OpenTelemetry Documentation](https://opentelemetry.io/docs/).
- [Sinais do OpenTelemetry](https://opentelemetry.io/docs/concepts/signals/).
- [Docker Compose](https://docs.docker.com/compose/).
- [Nginx proxy module](https://nginx.org/en/docs/http/ngx_http_proxy_module.html).

## Vídeos e cursos complementares

Vídeos envelhecem mais rápido que especificações. Use-os para intuição e
confirme comandos na documentação da versão utilizada.

- [Curso completo de SQL com PostgreSQL — do zero ao avançado](https://www.youtube.com/watch?v=9cAKQWodpvM) — Stack Mobile.
- [O que é um banco de dados?](https://www.youtube.com/watch?v=Ofktsne-utM) — Curso em Vídeo; fundamentos relacionais.
- [Curso de PostgreSQL — Bóson Treinamentos](https://www.bosontreinamentos.com.br/curso-completo-de-postgresql/) — aulas e textos organizados.
- [Como criar API em Python usando FastAPI](https://www.youtube.com/watch?v=R26iojTwUv8) — Hashtag Programação.
- [Curso de MongoDB fundamental](https://www.youtube.com/watch?v=x9tC0eK0GtA) — Matheus Battisti - Hora de Codar.
- [Curso API REST completo](https://www.youtube.com/watch?v=5mMuX8AWxxs) — While True.
- [FastAPI and MongoDB](https://learn.mongodb.com/learn/course/fastapi-and-mongodb/learning-byte/learn?page=1) — MongoDB University.
- [MongoDB Data Modeling Path](https://learn.mongodb.com/learning-paths/data-modeling-for-mongodb) — trilha oficial com embed/reference, padrões, índices e desempenho.
- [MongoDB Aggregation Fundamentals](https://learn.mongodb.com/learn/course/fundamentals-of-data-transformation) — curso oficial com vídeos e prática.
- [FastAPI Learn](https://fastapi.tiangolo.com/learn/) — curso/livro oficial recomendado pelo projeto.
- [POSETTE 2026 talks](https://www.postgresql.org/about/news/all-44-talks-from-posette-an-event-for-postgres-2026-are-available-on-youtube-3336/) — palestras técnicas de PostgreSQL.

## Fóruns e comunidades

- [Stack Overflow em Português](https://pt.stackoverflow.com/).
- [Database Administrators Stack Exchange](https://dba.stackexchange.com/).
- [PostgreSQL mailing lists](https://www.postgresql.org/list/).
- [PostgreSQL Wiki](https://wiki.postgresql.org/).
- [MongoDB Community Forums](https://www.mongodb.com/community/forums/).
- [FastAPI Discussions](https://github.com/fastapi/fastapi/discussions).
- [TabNews](https://www.tabnews.com.br/).

Ao perguntar, nunca publique connection string, dump, token, email real ou
plano contendo dados sensíveis. Substitua por fixture sintética reproduzível.

## Blogs técnicos

- [PostgreSQL News](https://www.postgresql.org/about/news/).
- [Planet PostgreSQL](https://planet.postgresql.org/) — agrega publicações da comunidade; valide cada autor e versão.
- [MongoDB Developer Center](https://www.mongodb.com/developer/).
- [FastAPI release notes](https://fastapi.tiangolo.com/release-notes/).
- [Python Software Foundation blog](https://pyfound.blogspot.com/).
- [Martin Fowler — architecture](https://martinfowler.com/architecture/).

Artigo de blog é evidência contextual, não especificação. Confira data,
premissas, versão e fonte primária antes de levar uma recomendação à produção.
