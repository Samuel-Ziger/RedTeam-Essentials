# Lab 05 — capstone Inventory API

## Objetivo

Executar, explicar, testar e evoluir uma API que combina PostgreSQL, MongoDB,
HTTP, concorrência otimista, idempotência e transactional outbox. O resultado
final é uma evidência técnica reproduzível, não apenas “os containers subiram”.

## Pré-requisitos e tempo

- capítulos 13, 14 e 15;
- Labs 01–04 concluídos;
- Docker Engine/Compose v2 e os runtimes do runner;
- 18 a 28 horas;
- ambiente local, dados fictícios e porta publicada somente em loopback.

## Mapa do projeto

Comece pelo [README da Inventory API](../projetos/inventory-api/README.md) e
associe cada responsabilidade a um artefato:

- [Compose](../projetos/inventory-api/compose.yaml): isolamento e ciclo de vida;
- [Dockerfile da API](../projetos/inventory-api/api/Dockerfile): runtime mínimo;
- [entrada HTTP](../projetos/inventory-api/api/src/inventory_api/main.py);
- [casos de uso](../projetos/inventory-api/api/src/inventory_api/service.py);
- [adaptadores de dados](../projetos/inventory-api/api/src/inventory_api/repositories.py);
- [worker outbox](../projetos/inventory-api/api/src/inventory_api/outbox.py);
- [schema PostgreSQL](../projetos/inventory-api/db/postgres/001_schema.sql);
- [índices MongoDB](../projetos/inventory-api/db/mongo/001_indexes.js);
- [gateway Nginx](../projetos/inventory-api/gateway/nginx.conf);
- [smoke test](../projetos/inventory-api/smoke-test.sh).

## Fase 1 — regressão sem infraestrutura

Crie ambiente virtual fora ou dentro da sua cópia do projeto:

```bash
cd 01-Recon/programacao-avancada/projetos/inventory-api/api
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements-dev.txt
PYTHONPATH=src pytest -q
```

Leia uma falha proposital: altere temporariamente uma expectativa e confirme que
o teste realmente acusa o defeito. Reverta imediatamente. Teste sempre verde
que não consegue ficar vermelho não é evidência suficiente.

## Fase 2 — arquitetura e fronteiras

Desenhe o fluxo de criação:

```text
cliente -> Nginx -> adapter HTTP -> caso de uso -> transação PostgreSQL
                                                   | produto
                                                   | idempotency record
                                                   ` outbox event
                                                          |
                                              worker -> MongoDB
```

Explique as janelas de falha antes e depois do commit. A outbox evita dual write
na requisição, mas a projeção continua eventual e pode ser entregue mais de uma
vez; o `eventId` único torna o consumidor idempotente.

## Fase 3 — execução completa

```bash
cd 01-Recon/programacao-avancada/projetos/inventory-api
docker compose config
docker compose up --detach --build --wait
bash smoke-test.sh
docker compose ps
```

O smoke test deve provar saúde, criação, replay idempotente, conflito de chave,
ETag, ajuste de estoque, cursor, Problem Details e convergência da outbox.
Registre comandos, versões e respostas mínimas relevantes.

## Fase 4 — falhas controladas

Faça uma falha por vez e restaure o estado entre elas:

1. pare MongoDB e crie produto; confirme evento pendente no PostgreSQL;
2. reinicie MongoDB; confirme convergência e ausência de evento duplicado;
3. envie o mesmo operation ID com body diferente; espere 409;
4. envie ETag obsoleto; espere 412 sem lost update;
5. peça estoque negativo; espere 409 e nenhuma mudança parcial;
6. pare a API; observe gateway e healthcheck;
7. tente corpo acima do limite do Nginx; registre 413.

Nunca desative validações ou exponha bancos no host para “facilitar” o teste.

## Fase 5 — mudança vertical autoral

Implemente **uma** capacidade completa, por exemplo reserva de estoque com
expiração. Antes de codificar, escreva:

- invariantes e estados;
- contrato HTTP e Problem Details;
- política de idempotência;
- efeito concorrente e precondição;
- migration PostgreSQL;
- evento e versão de schema;
- projeção MongoDB;
- testes unitários, de contrato e smoke;
- observabilidade e procedimento de rollback.

Faça commits pequenos. A mudança só termina quando atravessa modelo, caso de
uso, adapter, armazenamento, documentação e testes.

## Fase 6 — defesa técnica

Entregue uma nota curta respondendo:

1. o que ocorre se dois workers processarem o mesmo evento;
2. por que ETag e idempotency key resolvem problemas diferentes;
3. quais dados são fonte de verdade;
4. que garantias o healthcheck realmente oferece;
5. que limites tornam este projeto inadequado para produção;
6. qual métrica/alerta detectaria crescimento da outbox pendente;
7. como rotacionar credenciais sem downtime num ambiente real.

## Cleanup e gate

```bash
docker compose down

# Somente se deseja apagar os dados deste projeto:
docker compose down --volumes
```

Conclua quando:

- suíte sem bancos e smoke test passam;
- falhas controladas produzem o comportamento previsto;
- a mudança vertical possui testes e migration;
- nenhum serviço além do gateway aparece publicado;
- logs/evidências não contêm segredo nem dado real;
- os recursos temporários foram encerrados conscientemente.
