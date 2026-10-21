# Inventory API — projeto integrador

API educacional completa para estudar dados relacionais, documentos e HTTP.
Ela mantém produtos/estoque no PostgreSQL e projeta eventos de auditoria no
MongoDB por transactional outbox.

## Arquitetura

```text
curl / cliente
      |
      | 127.0.0.1:8101
      v
Nginx gateway ── rede service ── FastAPI
                                     |
                          rede data (interna)
                              /              \
                     PostgreSQL              MongoDB
                  fonte de verdade      projeção de eventos
                        |
                    outbox worker ────────────>
```

Somente o gateway publica porta. Bancos não possuem porta no host ou egress.

## Contrato

| Método/caminho | Semântica |
|----------------|-----------|
| `GET /health/live` | processo responde |
| `GET /health/ready` | PostgreSQL e MongoDB respondem |
| `POST /api/v1/products` | cria com `Idempotency-Key` |
| `GET /api/v1/products` | lista com filtro e cursor |
| `GET /api/v1/products/{id}` | retorna produto e ETag |
| `PATCH /api/v1/products/{id}` | altera com `If-Match` |
| `POST /api/v1/products/{id}/stock-movements` | ajusta estoque com operation ID |
| `GET /api/v1/products/{id}/events` | histórico eventual no MongoDB |

OpenAPI: `http://127.0.0.1:8101/openapi.json`. Documentação interativa:
`http://127.0.0.1:8101/docs`.

## Executar

```bash
cd 01-Recon/programacao-avancada/projetos/inventory-api
docker compose config
docker compose up --build -d
docker compose ps
bash smoke-test.sh
```

Se `8101` estiver ocupada, escolha outra porta sem editar o Compose:

```bash
INVENTORY_PORT=18101 docker compose up --build -d --wait
BASE_URL=http://127.0.0.1:18101 bash smoke-test.sh
```

> **Compatibilidade do host:** o MongoDB interrompe a inicialização em kernels
> Linux de 6.19 até 7.0.13 por uma incompatibilidade com TCMalloc. Isso também
> afeta contêineres. Use um host com kernel anterior a 6.19 ou igual/superior a
> 7.0.14; não tente contornar a verificação do servidor. Consulte as
> [notas oficiais de plataforma](https://www.mongodb.com/docs/manual/administration/production-notes/#platform-support-notes).

O smoke test demonstra:

- criação `201`, `Location` e ETag;
- retry idempotente com a mesma resposta;
- conflito quando a chave é reutilizada com outro body;
- alteração condicional e rejeição de versão obsoleta;
- ajuste transacional de estoque;
- replay de movimento somente quando body, recurso e precondição são iguais;
- busca literal mesmo quando o texto contém `%` ou `_`;
- paginação por cursor em duas páginas;
- Problem Details para 409, 412 e 428;
- preservação de request ID válido pelo gateway;
- publicação eventual no MongoDB;
- contrato OpenAPI e cabeçalhos defensivos do gateway.

## Requisições manuais

```bash
curl -i -X POST http://127.0.0.1:8101/api/v1/products \
  -H 'Content-Type: application/json' \
  -H 'Idempotency-Key: tutorial-product-001' \
  -d '{"sku":"BOOK-001","name":"Banco de Dados","priceCents":4500,"initialStock":2}'

curl -i 'http://127.0.0.1:8101/api/v1/products?limit=20&q=BOOK'
```

Copie o ID e ETag da resposta:

```bash
curl -i -X PATCH http://127.0.0.1:8101/api/v1/products/SEU_ID \
  -H 'Content-Type: application/json' \
  -H 'If-Match: "1"' \
  -d '{"priceCents":4900}'
```

## Clientes em cinco linguagens

Depois do smoke test, execute os
[clientes Python, Java, C, C# e JavaScript](../../exemplos/README.md). Todos
consomem este mesmo contrato, aplicam timeout e tratam status não 2xx. O cliente
C mostra o HTTP/1.1 bruto; os demais desserializam a resposta no modelo próprio
do runtime.

## Testes sem bancos

```bash
cd api
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements-dev.txt
PYTHONPATH=src pytest -q
```

Os testes substituem repositórios e validam configuração, modelos estritos,
cursores, casos de uso, outbox, busca com caracteres de `LIKE`, Problem Details
e contrato HTTP. O smoke test usa bancos reais e cobre diferenças que mocks não
detectam.

Da raiz do repositório, o runner do módulo também compila e executa os cinco
clientes contra uma API falsa em porta efêmera:

```bash
bash 01-Recon/programacao-avancada/testar-curso.sh
bash 01-Recon/programacao-avancada/testar-curso.sh --require-all
```

O modo estrito falha se algum runtime ou dependência estiver ausente. A prática
completa está no [Lab 05](../../laboratorios/lab-05-inventory-capstone.md).

## Inspecionar dados

```bash
docker compose exec postgres psql -U inventory -d inventory \
  -c 'TABLE product;'

docker compose exec postgres psql -U inventory -d inventory \
  -c 'SELECT id, event_type, published_at FROM outbox_event ORDER BY occurred_at;'

docker compose exec mongo mongosh inventory --quiet \
  --eval 'db.audit_events.find({}, {_id:0}).sort({occurredAt:-1}).limit(5).toArray()'
```

## Experimento de falha

Pare MongoDB, mas não remova dados:

```bash
docker compose stop mongo
```

Crie um produto. A transação PostgreSQL confirma e o evento fica pendente.

```bash
docker compose exec postgres psql -U inventory -d inventory \
  -c 'SELECT id, event_type FROM outbox_event WHERE published_at IS NULL;'
docker compose start mongo
docker compose logs -f api
```

O worker repete e converge. O índice único `eventId` torna a projeção
idempotente.

## Decisões importantes

- SQL parametrizado e constraints protegem a fonte de verdade.
- ETag/`If-Match` impedem lost update silencioso.
- Chave de idempotência é associada ao hash do request.
- Operation ID torna ajuste de estoque repetível.
- Cursor usa `(created_at, id)` para ordem total.
- Problem Details padroniza erros sem stack trace.
- Request ID correlaciona gateway e aplicação.
- Request ID do cliente só é preservado quando contém 8–64 caracteres seguros;
  caso contrário, o gateway gera outro.
- Busca trata `%`, `_` e `\` como texto, não como wildcard SQL implícito.
- Respostas do gateway incluem `nosniff` e `no-store`; rate limit responde 429.
- Outbox elimina a janela de dual write, mas mantém consistência eventual.

## Limites deliberados

Este é um laboratório local, não um template de produção:

- PostgreSQL usa `trust` e MongoDB não usa autenticação porque nenhuma porta é
  publicada e a rede é interna;
- não há identidade de usuário nem autorização por recurso;
- um único worker simplifica o exemplo;
- migrations são executadas pela imagem somente no volume vazio;
- registros de idempotência não possuem política de expiração neste exemplo;
- não há TLS, métricas, tracing, PITR ou replicação.

Antes de produção: secret manager, usuários mínimos, TLS, migrations explícitas,
OIDC/autorização, telemetria, política de retry, backup/PITR, alta disponibilidade
e testes de carga.

## Cleanup

```bash
docker compose down

# Remove também todos os dados deste projeto:
docker compose down --volumes
```

Confirme o diretório antes do segundo comando.
