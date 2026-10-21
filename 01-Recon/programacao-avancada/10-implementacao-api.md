# Implementação de API em camadas

Um framework resolve roteamento, parsing e integração com o servidor HTTP. Ele
não define onde ficam invariantes, transações, autorização ou tradução de
falhas. Este capítulo implementa esses limites sem transformar um projeto
pequeno em uma coleção cerimonial de interfaces.

## Objetivos de aprendizagem

Ao terminar, você deverá conseguir:

- separar transporte, aplicação, domínio e infraestrutura;
- implementar um caso de uso testável sem iniciar servidor;
- preservar invariantes com transação e constraints;
- mapear falhas previstas para um contrato HTTP estável;
- controlar pools, timeouts, startup e shutdown;
- publicar integrações por outbox sem prometer atomicidade inexistente.

## Arquitetura guiada por dependências

```text
entrada HTTP / worker / CLI
          |
          v
       aplicação  ------> portas necessárias
          |                         ^
          v                         |
        domínio              adaptadores externos
                          PostgreSQL / MongoDB / clock / broker
```

Dependências de código apontam para regras mais estáveis:

- **transporte:** conhece HTTP, JSON, headers e status;
- **aplicação:** coordena caso de uso, política e transação;
- **domínio:** expressa estados, transições e invariantes;
- **porta:** descreve exatamente o que o caso de uso precisa;
- **adaptador:** implementa porta usando driver/biblioteca externa.

Não é obrigatório criar uma classe para cada linha. Módulos e funções pequenas
podem manter os mesmos limites. Extraia abstração quando ela permite testar,
trocar uma fronteira ou nomear uma política real.

## Estrutura pequena e suficiente

```text
inventory/
  http/
    routes.py
    schemas.py
    errors.py
  application/
    create_product.py
    ports.py
  domain/
    product.py
    errors.py
  infrastructure/
    postgres_products.py
    outbox_worker.py
  config.py
  main.py
```

Evite pastas genéricas como `utils` e `helpers` para regras importantes. O nome
deve indicar a responsabilidade e o dono conceitual.

## Do DTO ao domínio

Um DTO de entrada descreve o contrato de transporte. Um comando descreve a
intenção validada o suficiente para a aplicação. A entidade protege regra de
domínio. Não reutilize automaticamente o objeto do ORM como os três.

```python
from dataclasses import dataclass
from decimal import Decimal
from uuid import UUID


@dataclass(frozen=True)
class CreateProductCommand:
    tenant_id: UUID
    sku: str
    name: str
    price: Decimal


@dataclass(frozen=True)
class CreatedProduct:
    id: UUID
    sku: str
    name: str
    price: Decimal
    version: int
```

Use tipos que preservem o significado. `Decimal` com precisão definida ou
inteiro em centavos é melhor que `float` para dinheiro. O tenant vem da
identidade autenticada ou de contexto autorizado, nunca é aceito cegamente de
um body.

## Portas orientadas ao caso de uso

Uma porta pequena torna dependências visíveis:

```python
from typing import Protocol
from uuid import UUID


class ProductRepository(Protocol):
    def add(self, product: "Product") -> None: ...

    def find_by_sku(self, tenant_id: UUID, sku: str) -> "Product | None": ...


class UnitOfWork(Protocol):
    products: ProductRepository
    outbox: "OutboxRepository"

    def __enter__(self) -> "UnitOfWork": ...
    def __exit__(self, exc_type, exc, traceback) -> None: ...
    def commit(self) -> None: ...
```

Não copie a API inteira do driver para a porta. Se o caso de uso precisa de
`reserve_stock`, uma operação atômica com esse nome pode ser melhor que expor
`get`, modificar em memória e `save`.

## Caso de uso completo

```python
import json
from dataclasses import asdict
from uuid import uuid4


class DuplicateSku(Exception):
    pass


def create_product(command: CreateProductCommand, uow: UnitOfWork) -> CreatedProduct:
    product = Product.create(
        product_id=uuid4(),
        tenant_id=command.tenant_id,
        sku=command.sku,
        name=command.name,
        price=command.price,
    )

    with uow:
        # Esta leitura melhora a mensagem, mas a constraint do banco ainda é
        # necessária: outra transação pode inserir depois desta linha.
        if uow.products.find_by_sku(command.tenant_id, command.sku):
            raise DuplicateSku(command.sku)

        uow.products.add(product)
        uow.outbox.add(
            event_id=uuid4(),
            event_type="product.created",
            aggregate_id=product.id,
            payload=json.dumps(asdict(product.to_event()), default=str),
        )
        uow.commit()

    return CreatedProduct.from_domain(product)
```

O adaptador PostgreSQL também traduz violação da constraint conhecida para
`DuplicateSku`. Sem isso, o `if` possui uma corrida clássica:

```text
T1 consulta: ausente
T2 consulta: ausente
T1 insere
T2 insere
```

A constraint única decide o vencedor de forma atômica.

## O adaptador HTTP deve ser fino

Exemplo conceitual com injeção de dependência:

```python
@router.post("/products", status_code=201)
def post_product(
    body: CreateProductRequest,
    principal: Principal = Depends(authenticate),
    service: InventoryService = Depends(get_service),
) -> Response:
    command = CreateProductCommand(
        tenant_id=principal.tenant_id,
        sku=body.sku,
        name=body.name,
        price=body.price,
    )
    result = service.create_product(command, principal)
    return Response.created(
        body=ProductResponse.from_result(result),
        location=f"/api/v1/products/{result.id}",
        etag=f'"{result.version}"',
    )
```

O framework e os nomes exatos variam. As propriedades importantes são:

- o tenant confiável não vem do JSON;
- schema HTTP não vaza para o domínio;
- regra e transação não ficam no controller;
- o resultado é traduzido explicitamente para contrato externo.

## Configuração validada no startup

Leia ambiente uma vez, converta para tipos e falhe cedo:

```python
@dataclass(frozen=True)
class Settings:
    database_url: str
    pool_min: int
    pool_max: int
    statement_timeout_ms: int

    @classmethod
    def from_env(cls) -> "Settings":
        settings = cls(
            database_url=required_env("DATABASE_URL"),
            pool_min=parse_int("DB_POOL_MIN", minimum=1),
            pool_max=parse_int("DB_POOL_MAX", minimum=1),
            statement_timeout_ms=parse_int("DB_STATEMENT_TIMEOUT_MS", minimum=10),
        )
        if settings.pool_min > settings.pool_max:
            raise ConfigError("DB_POOL_MIN cannot exceed DB_POOL_MAX")
        return settings
```

Não espalhe `os.environ`, defaults perigosos e parsing por controllers.
Segredos vêm de secret manager ou arquivo montado com proteção apropriada,
nunca de Git, imagem, log ou mensagem de erro.

Ambientes diferem por configuração e capacidade, não por branches de código.
Feature flags precisam de dono, valor seguro, telemetria e plano de remoção.

## Dependency injection sem service locator

Injete dependências no ponto de composição:

```text
main
  -> settings
  -> pool
  -> repository factory / unit of work
  -> service
  -> router
  -> server
```

Um objeto global mutável ou chamadas arbitrárias a `container.resolve()` tornam
dependências ocultas. O teste deve conseguir montar o caso de uso com fake sem
rede, banco ou servidor.

Fakes preservam comportamento relevante em memória; mocks verificam interações.
Prefira fake quando o estado e as invariantes importam. Use mock com moderação
em uma fronteira como envio de e-mail.

## Validação e normalização

As camadas possuem responsabilidades diferentes:

1. servidor limita framing, headers, body e tempo;
2. parser valida JSON e encoding;
3. schema valida campos, tipos, formatos e limites locais;
4. caso de uso valida permissão e regra contextual;
5. entidade impede estado impossível;
6. banco garante invariantes concorrentes;
7. adaptador traduz apenas falhas previstas.

Não capture `Exception` para devolver 400. Isso atribui ao cliente um defeito
de programação e remove o sinal operacional. Erros inesperados devem gerar 500
sanitizado e log/trace interno correlacionado.

### Unicode, números e tempo

- defina se comprimento significa bytes, pontos de código ou grafemas;
- rejeite números não finitos mesmo que algum parser os aceite;
- não converta string numérica silenciosamente;
- use UTC para instantes e preserve timezone quando ele faz parte da intenção;
- limite profundidade e quantidade de elementos, não apenas bytes;
- normalize identificadores somente com regra de domínio explícita.

## Transação e operações atômicas

O exemplo abaixo altera estoque sem janela entre leitura e escrita:

```python
row = connection.execute(
    """
    UPDATE product
       SET stock = stock + %(delta)s,
           version = version + 1,
           updated_at = CURRENT_TIMESTAMP
     WHERE tenant_id = %(tenant_id)s
       AND id = %(id)s
       AND version = %(expected_version)s
       AND stock + %(delta)s >= 0
     RETURNING id, stock, version
    """,
    command,
).fetchone()
```

Se nenhuma linha voltar, pode haver recurso ausente, versão obsoleta ou estoque
insuficiente. A API decide quanto distinguir sem vazar informação; o repositório
deve produzir um resultado explícito, não `None` ambíguo.

### Isolamento não substitui modelagem

Escolha o isolamento a partir das anomalias que a invariante tolera. Mesmo em
isolamento forte, mantenha transações curtas e retry controlado para aborts
transitórios. Uma transação não deve esperar chamada HTTP externa.

## Mapeamento de erros

Defina uma tabela central de erros esperados:

| Erro interno | HTTP | Código externo | Log |
|---|---:|---|---|
| `InvalidProduct` | 422 | `invalid_product` | info |
| `DuplicateSku` | 409 | `duplicate_sku` | info |
| `NotAuthenticated` | 401 | `invalid_credentials` | info/segurança |
| `NotAuthorized` | 403 ou 404 | `forbidden`/`not_found` | info/segurança |
| `VersionConflict` | 412 | `stale_version` | info |
| `PoolTimeout` | 503 | `temporarily_unavailable` | warning |
| erro inesperado | 500 | `internal_error` | error + incidente |

Não exponha nomes de exceção, SQL ou mensagens do driver. Preserve a causa
no log interno usando encadeamento de exceção.

## Cliente de dependência remota

Toda chamada de saída precisa de:

- timeout de conexão e de resposta dentro do deadline;
- pool limitado;
- validação TLS;
- limite de resposta;
- retry apenas para operação e falha apropriadas;
- circuito ou proteção de capacidade quando justificado;
- mapeamento de erro que não transforma tudo em `500` genérico;
- propagação segura de trace, nunca de credencial irrelevante.

Circuit breaker não conserta uma dependência. Ele limita trabalho condenado e
precisa de estados, janela, limiar, half-open e telemetria bem definidos.

## Outbox transacional

Gravar PostgreSQL e depois publicar diretamente cria um dual write:

```text
COMMIT produto -> processo cai -> evento não publicado
```

Com outbox:

1. produto e evento entram na mesma transação local;
2. worker busca lote pendente com coordenação entre workers;
3. publica mensagem contendo `event_id` estável;
4. consumidor aplica efeito idempotente;
5. worker marca publicação ou agenda novo retry;
6. monitor mede idade do evento mais antigo e quantidade pendente.

```sql
CREATE TABLE outbox_event (
    event_id UUID PRIMARY KEY,
    aggregate_id UUID NOT NULL,
    event_type TEXT NOT NULL,
    schema_version INTEGER NOT NULL,
    payload JSONB NOT NULL,
    occurred_at TIMESTAMPTZ NOT NULL,
    published_at TIMESTAMPTZ NULL,
    attempts INTEGER NOT NULL DEFAULT 0
);
```

Marcar como publicado e publicar no broker ainda não são uma transação única.
Duplicatas continuam possíveis. A garantia prática é entrega ao menos uma vez
com consumidor idempotente, não “exactly once” fim a fim.

## Migrations e compatibilidade de deploy

Em deploy sem parada, código antigo e novo podem coexistir. Use expand/contract:

1. **expandir:** adicione coluna/tabela compatível;
2. publique código que escreve/lê o novo formato com fallback controlado;
3. migre/backfill em lotes observáveis;
4. confirme que nenhum consumidor depende do formato antigo;
5. **contrair:** remova campo/constraint antigos em deploy posterior.

Migrations devem ter backup/restore praticado, estimativa de locks, estratégia
de rollback ou roll-forward e teste do zero e da versão anterior.

## Startup, readiness, liveness e shutdown

No startup:

- valide toda configuração;
- verifique migrations esperadas;
- abra pools com limites;
- inicialize workers com ciclo controlado;
- falhe claramente se uma dependência obrigatória não puder ser usada.

**Liveness** responde se o processo deve ser reiniciado. **Readiness** responde
se deve receber tráfego. Não faça liveness depender de cada serviço remoto: uma
falha externa poderia reiniciar todas as réplicas em loop.

No shutdown:

1. marque a instância como não pronta;
2. pare de aceitar novo tráfego;
3. sinalize workers e consumidores;
4. aguarde requisições com deadline;
5. devolva/rejeite mensagens conforme o broker;
6. feche pools e clientes;
7. finalize dentro do grace period da plataforma.

O grace period externo deve ser maior que o prazo interno de drenagem.

## Invariantes implementáveis

- toda consulta de produto inclui `tenant_id` por construção;
- SKU é único por tenant via constraint;
- estoque nunca fica negativo, inclusive sob concorrência;
- update exige versão esperada;
- produto e outbox compartilham commit;
- resposta de sucesso ocorre apenas depois do commit;
- nenhuma chamada de rede acontece segurando transação de banco;
- recursos têm limites e são fechados no sucesso e na exceção.

## Exercícios

1. Implemente `create_product` com fake e teste sem servidor HTTP.
2. Injete um `Clock` e torne datas determinísticas.
3. Execute duas criações simultâneas do mesmo SKU e prove unicidade.
4. Execute duas retiradas concorrentes e prove que estoque não fica negativo.
5. Faça o adaptador MongoDB falhar e confirme que a outbox permanece pendente.
6. Reinicie o worker e confirme convergência sem efeito duplicado.
7. Provoque timeout do pool e verifique resposta, log, métrica e trace.
8. Desenhe uma migration expand/contract compatível com duas versões do app.
9. Teste shutdown durante uma requisição e durante publicação de evento.

## Critérios de conclusão

- regras do domínio executam em teste sem framework ou banco;
- constraints protegem invariantes que enfrentam concorrência;
- o controller apenas traduz transporte e chama aplicação;
- toda dependência externa tem limite, timeout e fechamento;
- falhas esperadas possuem mapeamento estável e falhas inesperadas ficam visíveis;
- outbox tolera queda e duplicação sem perder efeito de negócio;
- startup, readiness e shutdown possuem testes ou verificação reproduzível;
- migrations suportam coexistência de versões durante o deploy.

## Checklist de revisão

- [ ] Dependências apontam para o código de regra mais estável.
- [ ] Configuração é carregada e validada uma vez.
- [ ] DTO, comando, domínio e persistência não são o mesmo objeto por acidente.
- [ ] Transação acompanha a invariante.
- [ ] Exceções desconhecidas não viram erro do cliente.
- [ ] Pools, threads, tasks e clientes possuem ciclo de vida explícito.
- [ ] Dual write foi removido ou sua limitação foi aceita conscientemente.
