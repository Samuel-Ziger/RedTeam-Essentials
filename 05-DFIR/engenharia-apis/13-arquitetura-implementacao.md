# 13 — Arquitetura de implementação

O framework converte transporte. Regras de negócio, autorização e transações
precisam sobreviver à troca do framework e ser testáveis sem servidor. Boa
arquitetura torna dependências e commits explícitos, não cria camadas por ritual.

## Objetivos

- separar adapter, aplicação, domínio e infraestrutura;
- orientar dependências para o núcleo;
- definir unidade de trabalho e fronteiras transacionais;
- traduzir modelos externos com camada anticorrupção;
- testar casos de uso sem rede ou banco real.

## 1. Portas e adapters

~~~text
HTTP adapter -> application service -> domain
       |               |              ^
       |               +-> ports -----+
       |                     |
       +-> auth/telemetry    +-> database, broker, partner adapters
~~~

O adapter HTTP valida estrutura, cria contexto autenticado, chama um caso de uso
e mapeia resultado. Serviço de aplicação coordena autorização, carregamento,
transação e portas. Domínio protege invariantes. Adapter de persistência traduz
operações para tecnologia concreta.

Domínio não importa FastAPI, ORM, driver, request ou response. Isso evita regras
presas a callbacks do framework.

## 2. Fluxo de leitura e escrita

Leitura:

~~~text
decodificar -> autenticar -> autorizar consulta -> buscar com escopo
            -> projetar campos permitidos -> representar -> observar
~~~

Escrita:

~~~text
decodificar -> validar -> autenticar -> autorizar -> carregar estado
            -> aplicar regra -> persistir condicionalmente
            -> registrar outbox -> commit -> responder
~~~

Autorizar depois de carregar pode ser necessário para avaliar ownership, mas a
consulta deve impedir exposição cruzada. Em alguns domínios, o repositório
retorna “não encontrado dentro do escopo” e não revela existência.

## 3. Caso de uso explícito

Uma entrada tipada evita passar Request por toda aplicação:

~~~python
@dataclass(frozen=True)
class UpdateItemCommand:
    actor_id: str
    tenant_id: str
    item_id: str
    expected_version: int
    title: str | None

class UpdateItem:
    def execute(self, command: UpdateItemCommand) -> Item:
        item = self.items.get_for_tenant(command.tenant_id, command.item_id)
        self.policy.require_update(command.actor_id, item)
        updated = item.rename(command.title)
        return self.items.save_if_version(updated, command.expected_version)
~~~

O exemplo ainda precisa de unidade de trabalho, mas mostra que HTTP e banco não
definem a regra.

## 4. Transação e efeitos externos

Declare onde a transação começa, quais escritas cobre e quando confirma. Não faça
chamada remota enquanto mantém lock do banco sem medir impacto. Para publicar
evento após alteração, grave outbox na mesma transação; worker publica depois.

Responder antes do commit gera falso sucesso. Publicar antes do commit produz
evento sobre estado inexistente. Chamar parceiro depois do commit pode falhar e
exige estado de workflow/retry, não rollback mágico.

## 5. Portas úteis e abstração suficiente

Porta expressa necessidade do caso de uso:

~~~text
ItemRepository.get_for_tenant
ItemRepository.save_if_version
EventOutbox.append
Clock.now
IdGenerator.next
~~~

Evite IRepository<T> genérico com consultas livres; ele vaza modelo do banco.
Também não encapsule cada função padrão. Isole o que muda, falha, tem efeito ou
precisa de teste determinístico. Clock e gerador de ID são portas pequenas com
grande benefício em testes.

## 6. Camada anticorrupção

Modelo de API parceira não deve virar domínio interno. Traduza status, unidades,
IDs e erros em adapter:

~~~text
PartnerPaymentResponse -> PaymentAuthorization
PartnerTimeout -> AuthorizationUncertain
PartnerDeclined -> PaymentDeclined
~~~

Isso impede que mudança de enum externo se espalhe. Preserve identificador de
correlação necessário à reconciliação.

## 7. Configuração e composição

O composition root cria adapters e injeta dependências. Configuração é validada
no início: URLs, limites, timeouts e nomes. Segredo vem de mecanismo apropriado,
nunca de valor padrão inseguro.

Aplicação deve ter um caminho único de inicialização usado por produção e testes
de componente. Montagem diferente em testes mascara erro.

## 8. Erros e observabilidade

Domínio emite erros tipados. Adapter mapeia para Problem Details. Métricas e
traces envolvem o caso de uso sem colocar logger em cada entidade. Auditoria de
negócio pode ser evento explícito dentro da transação.

Não capture Exception e retorne 400. Erro inesperado é 500, preserva request ID e
dispara sinal operacional.

## Falhas comuns

| Falha | Resultado | Correção |
|---|---|---|
| controller com toda lógica | teste lento/acoplado | caso de uso |
| entidade importa ORM/framework | domínio dependente | mapeamento |
| repositório genérico | regra de consulta espalhada | porta por domínio |
| chamada remota em lock | saturação/deadlock | workflow/outbox |
| mock de tudo | teste da implementação | fakes nas portas relevantes |

## Exercícios

### Nível 1 — extração

Extraia um endpoint para adapter e caso de uso. **Aceite:** regra é testada sem
FastAPI/HTTP.

### Nível 2 — unidade de trabalho

Implemente alteração + outbox atômicas. **Aceite:** falha antes do commit não
publica; depois do commit pode repetir sem duplicar efeito.

### Nível 3 — parceiro hostil

Crie adapter para respostas lentas, desconhecidas e inválidas. **Aceite:** domínio
recebe erros próprios e consegue reconciliar estado incerto.

## Checklist

- [ ] Domínio não depende do framework.
- [ ] Casos de uso expressam transação e autorização.
- [ ] Repositórios falam a linguagem do domínio.
- [ ] Efeito externo não está escondido em callback.
- [ ] Clock e IDs podem ser controlados em teste.
- [ ] Erros inesperados preservam diagnóstico.

