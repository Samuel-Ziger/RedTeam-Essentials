# Laboratórios progressivos

Os cinco laboratórios transformam a teoria do módulo em evidência executável.
Siga a ordem: cada etapa reutiliza o vocabulário e as garantias da anterior.

| Lab | Entrega principal | Pré-requisitos recomendados |
|-----|-------------------|-----------------------------|
| [01 — modelagem e SQL](lab-01-modelagem-sql.md) | schema, constraints e testes negativos | capítulos 00–02 |
| [02 — transações e índices](lab-02-transacoes-indices.md) | concorrência e planos medidos | capítulos 03–05 + Lab 01 |
| [03 — MongoDB](lab-03-mongodb-documentos.md) | validator, índices, agregação e migration | capítulos 06–07 + Labs 01–02 |
| [04 — contrato de API](lab-04-contrato-api.md) | clientes e testes HTTP em cinco linguagens | capítulos 08–12 + Labs 01–03 |
| [05 — Inventory API](lab-05-inventory-capstone.md) | capstone com outbox e evolução vertical | capítulos 13–15 + Labs 01–04 |

O checklist dentro de cada lab é a definição de concluído. Marcar o Markdown
como lido não comprova execução, diagnóstico nem autoria.

## Ambiente dos bancos

Ambiente local isolado para os exercícios SQL e MongoDB. Nenhuma porta é
publicada no host e a rede não possui egress.

```bash
cd 01-Recon/programacao-avancada/laboratorios
docker compose up -d
docker compose ps
```

Para uma validação descartável, prefira o runner. Ele cria projeto e volumes
com nome exclusivo e remove apenas esses recursos ao terminar:

```bash
bash testar-laboratorios.sh --postgres-only
bash testar-laboratorios.sh --mongo-only

# Em host compatível com ambos:
bash testar-laboratorios.sh
```

> **Compatibilidade:** MongoDB não executa em kernels Linux de 6.19 até 7.0.13.
> A documentação oficial recomenda kernel anterior a 6.19 ou 7.0.14 e posterior;
> veja as [notas de plataforma](https://www.mongodb.com/docs/manual/administration/production-notes/#platform-support-notes).

## PostgreSQL

```bash
docker compose exec postgres psql -U course -d course -f /course/001_schema.sql
docker compose exec postgres psql -U course -d course -f /course/002_seed.sql
docker compose exec postgres psql -U course -d course -f /course/003_queries.sql
docker compose exec postgres psql -U course -d course -f /course/004_assertions.sql
```

Entre no console:

```bash
docker compose exec postgres psql -U course -d course
```

## MongoDB

```bash
docker compose exec mongo mongosh --file /course/001_setup.js
docker compose exec mongo mongosh --file /course/002_queries.js
docker compose exec mongo mongosh --file /course/003_assertions.js
docker compose exec mongo mongosh course
```

## Backup e restore verificável

Backup só existe quando o restore foi testado. Os comandos abaixo usam bancos
de destino diferentes para não sobrescrever o exercício original.

PostgreSQL, formato lógico customizado:

```bash
docker compose exec -T postgres pg_dump -U course -d course --format=custom \
  > /tmp/rte-course-postgres.dump
docker compose exec postgres createdb -U course course_restore
docker compose exec -T postgres pg_restore -U course -d course_restore \
  < /tmp/rte-course-postgres.dump
docker compose exec postgres psql -U course -d course_restore \
  -c 'SELECT count(*) AS restored_books FROM book;'
docker compose exec postgres dropdb -U course course_restore
```

MongoDB, archive lógico com remapeamento de namespace:

```bash
docker compose exec -T mongo mongodump --quiet --db course --archive \
  > /tmp/rte-course-mongo.archive
docker compose exec -T mongo mongorestore --quiet --archive \
  --nsFrom='course.*' --nsTo='course_restore.*'
docker compose exec mongo mongosh course_restore --quiet \
  --eval 'db.audit_events.countDocuments({})'
docker compose exec mongo mongosh course_restore --quiet \
  --eval 'db.dropDatabase()'
```

Os arquivos em `/tmp` contêm dados fictícios deste curso. Em produção, proteja
confidencialidade, integridade, retenção, acesso às chaves e cópias fora do
domínio de falha principal. Teste restauração com frequência definida.

## Reset

```bash
docker compose down

# Destrutivo somente para os volumes deste laboratório:
docker compose down --volumes
```

`POSTGRES_HOST_AUTH_METHOD=trust` e MongoDB sem autenticação são concessões
deliberadas deste laboratório sem portas/egress. Nunca copie isso para ambiente
compartilhado ou produção.
