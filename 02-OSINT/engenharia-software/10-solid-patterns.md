# 10 — SOLID e padrões de projeto sem dogma

SOLID e padrões são vocabulários para discutir forças de design. Não são metas
de pontuação, obrigação de criar classes nem substitutos para compreender o
problema. Um design é bom quando preserva invariantes, torna mudanças prováveis
locais e continua compreensível para quem o opera.

## Objetivos verificáveis

Ao final, você deverá conseguir:

- traduzir cada princípio SOLID em uma consequência observável no código;
- encontrar violações comportamentais, não apenas formas “feias”;
- aplicar Strategy, Adapter, Factory, Observer, Command e Repository;
- comparar um padrão com uma função, composição direta ou estrutura de dados;
- distinguir padrão de objeto, padrão arquitetural e detalhe de framework;
- escrever contratos que preservam pré-condições, pós-condições e invariantes;
- remover uma abstração quando ela custa mais do que a mudança que isola;
- justificar uma escolha no contexto do Dependency Planner.

Pré-requisitos: interfaces/protocolos, composição, testes e o capítulo anterior.
Todos os exemplos se conectam ao
[Dependency Planner](projetos/dependency-planner/README.md).

## Primeiro o problema, depois o nome

Observe uma variação concreta antes de escolher um padrão:

```text
mudança: aceitar JSON e CSV
fronteira: documento externo -> tarefas do domínio
força: formatos mudam sem alterar o algoritmo
possível padrão: Adapter
alternativa simples: duas funções de parsing
evidência: mesmos testes de contrato para ambos
```

Se você começa com “onde posso colocar uma Factory?”, o padrão vira decoração.
Registre: contexto, forças, opções, decisão e consequência. Uma abstração deve
responder a uma pergunta de mudança, propriedade ou teste.

## SOLID em termos operacionais

### SRP — responsabilidade única

SRP não significa “uma função por arquivo” nem “uma classe faz uma coisa” sem
definir coisa. Uma unidade deve ter uma razão coesa para mudar e um conjunto
coerente de interessados.

No planejador:

- parser JSON muda por contrato de entrada;
- algoritmo de grafo muda por política de planejamento;
- formatador muda por experiência da CLI;
- persistência muda por operação e tecnologia.

Uma classe `PlannerManager` que lê arquivo, calcula o plano e imprime possui
razões independentes. Em contraste, uma função longa que percorre uma matriz em
uma única transformação pode continuar coesa; fragmentá-la em dez métodos
genéricos não melhora o design.

**Teste prático:** descreva o módulo em uma frase e liste três mudanças recentes.
Se mudanças por motivos independentes sempre atingem a mesma unidade, considere
separá-la. Não separe apenas porque ela ultrapassou uma contagem de linhas.

### OCP — aberto para extensão, fechado para modificação

OCP pede que uma variação conhecida possa ser acrescentada em um ponto estável,
sem condicionais espalhadas. Não pede previsão de todas as mudanças futuras.

```python
from collections.abc import Callable, Iterable

ChaveDeDesempate = Callable[[str], tuple[object, ...]]


def ordenar_disponiveis(
    ids: Iterable[str],
    chave: ChaveDeDesempate = lambda item: (item,),
) -> list[str]:
    return sorted(ids, key=chave)
```

Uma nova política de desempate entra por função, sem editar o algoritmo. Isso é
OCP suficiente para a variação. Uma hierarquia `AbstractSortStrategyFactory`
seria custo sem benefício.

OCP tem limite: quando muda a própria regra — por exemplo, tarefas agora podem
ser interrompidas e dividir duração — editar o núcleo pode ser a opção honesta.
Uma “extensão” que contorna invariantes é pior que uma modificação revisada.

### LSP — substituição de Liskov

Se `S` substitui `T`, consumidores de `T` devem continuar corretos sem conhecer
`S`. A implementação não pode fortalecer pré-condições, enfraquecer
pós-condições ou quebrar invariantes e propriedades históricas do contrato.

Contrato de `LeitorDeTarefas.listar`:

- devolve uma sequência, inclusive quando vazia;
- cada tarefa já satisfaz invariantes locais;
- não oculta duplicatas nem referências desconhecidas: a validação global
  pertence ao planejador, que enxerga o conjunto completo;
- erro de fonte é reportado, nunca convertido silenciosamente em lista vazia;
- chamada não altera a fonte.

Um `LeitorRemoto` que devolve `None` em timeout ou exige chamar `conectar()`
antes viola o contrato, ainda que a assinatura compile. Um repositório somente
leitura não deve implementar `salvar` lançando `UnsupportedOperationException`;
a interface deveria ser segregada.

**Teste de contrato:** execute a mesma suíte contra memória e JSON. Testes não
provam toda substituição, mas tornam as promessas observáveis.

### ISP — segregação de interfaces

Consumidores não devem depender de operações que não utilizam. Em vez de:

```text
TaskRepository: listar, buscar, inserir, atualizar, remover,
                exportar_csv, limpar_cache, iniciar_transacao
```

defina portas conforme os casos de uso:

```python
class LeitorDeTarefas:
    def listar(self) -> tuple[Tarefa, ...]: ...


class GravadorDePlanos:
    def salvar(self, plano: Plano) -> None: ...
```

Interfaces menores reduzem dependências e fakes. Porém, dividir cada método em
um arquivo distinto pode tornar descoberta e evolução difíceis. O critério é a
necessidade dos consumidores, não “interface mínima” como valor absoluto.

### DIP — inversão de dependência

Políticas de alto nível não devem depender de detalhes voláteis; ambos dependem
de contratos estáveis. A abstração pertence conceitualmente ao consumidor.

```text
CLI -> PlanejarProjeto -> LeitorDeTarefas <- AdaptadorJson
                       -> Relogio         <- RelogioDoSistema
```

Não é obrigatório um container. O construtor torna dependências obrigatórias e
a [composition root](09-design-modular.md#composition-root-onde-o-concreto-é-escolhido)
fornece implementações. DIP não é satisfeito ao esconder o ORM atrás de uma
interface com os mesmos métodos e tipos do ORM; o detalhe continua vazando.

## Strategy: trocar uma política

Strategy encapsula algoritmos intercambiáveis sob o mesmo contrato. No
planejador, o desempate entre tarefas simultaneamente disponíveis pode ser por
ID, prioridade ou menor duração.

```python
from collections.abc import Callable

Strategy = Callable[[Tarefa], tuple[object, ...]]


def por_id(tarefa: Tarefa) -> tuple[object, ...]:
    return (tarefa.id,)


def por_menor_duracao(tarefa: Tarefa) -> tuple[object, ...]:
    return (tarefa.duracao, tarefa.id)
```

O segundo elemento preserva determinismo em empates. Strategy muda a escolha
entre planos topologicamente válidos; não pode violar dependências. A invariante
continua sendo “uma tarefa só sai após seus predecessores”.

Em Java, use `Comparator<Task>` ou uma interface; em C#, `Comparison<Task>` ou
`IComparer<Task>`; em C, ponteiro de função mais `void *context`; em JavaScript,
uma callback. Crie classe própria quando a estratégia possui configuração,
estado ou contrato complexo. Para uma chave pura, função basta.

**Custo:** chamada indireta e mais uma decisão de configuração. **Benefício:**
política variável e testável. Se só há uma regra e nenhuma mudança plausível,
deixe concreto.

## Adapter: traduzir um mundo externo

Adapter converte a interface de um fornecedor na linguagem interna. O
`JsonTaskRepository` converte `duration` e `dependencies` em `duracao` e
`dependencias`, valida limites e traduz falhas de parsing.

```python
def tarefa_do_documento(item: object) -> Tarefa:
    if not isinstance(item, dict):
        raise DocumentoInvalido("item deve ser objeto")
    try:
        return Tarefa(
            id=item["id"],
            duracao=item["duration"],
            dependencias=tuple(item["dependencies"]),
        )
    except (KeyError, TypeError, ValueError) as erro:
        raise DocumentoInvalido("tarefa invalida") from erro
```

O `from erro` preserva a causa para diagnóstico. O domínio não recebe
dicionários. Adapter não corrige semanticamente dados inválidos nem engole
falhas. Para CSV, outro adaptador pode reutilizar os testes de contrato.

## Factory: centralizar criação variável

Factory é útil quando a construção exige escolher uma implementação, validar
configuração ou coordenar ciclo de vida:

```python
def criar_leitor(uri: str) -> LeitorDeTarefas:
    if uri.startswith("file:"):
        return LeitorJson(Path(uri.removeprefix("file:")))
    if uri.startswith("memory:"):
        return LeitorEmMemoria(())
    raise ConfiguracaoInvalida(f"fonte nao suportada: {uri!r}")
```

Essa factory pertence à borda/composição. O domínio não deve escolher fonte. Se
a factory apenas chama `Tarefa(...)`, o construtor comunica melhor. Não use
service locator global: ele esconde dependências e permite falha tardia.

## Observer: anunciar um fato

Observer notifica vários interessados sem o emissor conhecer cada implementação.
Após um plano ser calculado, métricas e auditoria podem observar o evento:

```python
from collections.abc import Callable
from dataclasses import dataclass


@dataclass(frozen=True)
class PlanoCalculado:
    total_tarefas: int
    duracao: int


Observador = Callable[[PlanoCalculado], None]


def publicar(evento: PlanoCalculado, observadores: tuple[Observador, ...]) -> None:
    for observar in observadores:
        observar(evento)
```

O código parece simples; o contrato difícil é operacional:

- ordem dos observadores importa?
- uma falha interrompe os seguintes?
- entrega é síncrona, assíncrona, uma vez ou “pelo menos uma vez”?
- observador pode alterar o evento?
- reentrada e inscrição durante publicação são permitidas?

No mesmo processo, callbacks podem bastar. Entre serviços, broker e eventos
duráveis introduzem duplicação, atraso e consistência eventual. Observer não é
automaticamente “event-driven architecture”.

## Command: intenção como valor

Command representa uma solicitação executável. É útil para filas, auditoria,
retry controlado, histórico ou composição.

```python
from dataclasses import dataclass


@dataclass(frozen=True)
class CalcularPlano:
    projeto_id: str
    estrategia: str


def executar(comando: CalcularPlano, servico: PlanejarProjeto) -> Plano:
    if not comando.projeto_id.strip():
        raise ValueError("projeto_id vazio")
    return servico.executar()
```

O comando guarda intenção, não dependências de execução. Não serialize objetos
de conexão dentro dele. Retry só é seguro se o efeito for idempotente ou tiver
deduplicação. Para uma chamada local trivial sem histórico, uma função direta é
mais clara que uma classe por verbo.

## Repository: coleção orientada ao domínio

Repository oferece a ilusão de uma coleção de agregados, com operações ditadas
pelos casos de uso. Não é um wrapper genérico de tabela.

```python
class Projetos:
    def obter(self, projeto_id: str) -> Projeto | None: ...
    def salvar(self, projeto: Projeto, versao_esperada: int) -> None: ...
```

`salvar(..., versao_esperada)` pode tornar concorrência otimista explícita. Uma
operação `projetos_prontos_para_planejar(limite)` comunica mais que
`find_by_status_and_date`. Evite `GenericRepository<T>` se ele elimina
constraints, paginação, transação e consultas próprias de cada agregado.

No Dependency Planner atual, a fonte é somente leitura; `LeitorDeTarefas` é um
nome mais preciso que Repository completo. O padrão não deve ser imposto onde a
semântica não existe.

## Como os padrões se combinam

Uma evolução possível do projeto:

```text
composition root
  Factory escolhe Adaptador JSON/CSV
       |
       v
Command -> caso de uso -> Repository/Leitor
              |
              +-> Strategy de desempate
              +-> publica evento para Observers
```

Essa figura não é uma lista de implementação. Adote apenas o necessário. Cada
padrão acrescenta um contrato e possíveis modos de falha.

## Padrões arquiteturais são outra escala

MVC organiza entrada/apresentação, ports-and-adapters organiza dependências,
event-driven organiza comunicação e CQRS separa modelos de leitura/escrita.
Eles não são alternativas diretas a Factory ou Strategy. Um sistema pode usar
ports-and-adapters e, dentro de um adaptador, Strategy. Nomear a escala evita a
discussão “qual padrão é melhor?” sem contexto.

## Sinais de uso prematuro

- interface com uma implementação, sem fronteira ou variação real;
- factory que apenas repassa os mesmos argumentos ao construtor;
- herança usada só para compartilhar três linhas;
- cadeia de decorators impossível de depurar;
- Observer para fluxo que exige resposta transacional imediata;
- Repository genérico que expõe consulta e modelo do ORM;
- nomes `Manager`, `Processor` e `Handler` sem linguagem do domínio;
- teste que mocka cada chamada interna e quebra em toda refatoração.

Também há subdesign: `if formato == ...` repetido em cinco lugares, parsing no
domínio e instanciação concreta dentro do caso de uso são sinais de variação sem
fronteira. O equilíbrio vem de evidência, não de uma quantidade ideal de classes.

## Falhas comuns e diagnóstico

| Sintoma | Princípio/força provável | Diagnóstico |
|---|---|---|
| adaptador retorna `None` só em erro | LSP | rode teste de contrato em todas as implementações |
| fake precisa implementar 20 métodos | ISP | liste operações realmente usadas pelo consumidor |
| regra importa ORM | DIP | inspecione tipos públicos e imports transitivos |
| uma mudança toca parser e algoritmo | SRP | separe as razões de mudança no diff |
| novo formato adiciona condicionais em todo lugar | OCP/Adapter | concentre tradução em uma borda |
| eventos somem ou duplicam | contrato de Observer | defina entrega, retry, ordem e idempotência |
| Command é reexecutado com efeito duplicado | semântica de retry | use chave idempotente ou proíba retry |

## Laboratórios

### Básico — SOLID por comportamento

Escolha uma classe que lê JSON, ordena e imprime. Separe parser e regra, sem
criar framework próprio.

**Critérios de aceite:**

- teste do algoritmo não toca disco nem console;
- erro de documento e erro de ciclo permanecem distinguíveis;
- cada unidade tem uma razão de mudança escrita em uma frase;
- nenhum método foi criado apenas para reduzir contagem de linhas.

### Intermediário — Strategy e Adapter

Adicione CSV e duas políticas determinísticas de desempate.

**Critérios de aceite:**

- JSON e CSV passam pela mesma suíte de contrato;
- domínio não conhece nomes de colunas ou chaves;
- cada Strategy produz uma ordem topológica válida;
- empate total é resolvido de forma reproduzível;
- há um contraexemplo mostrando que menor duração não minimiza necessariamente
  a duração total quando recursos limitados forem introduzidos.

### Avançado — Command, Repository e Observer

Modele `CalcularPlano`, persista o resultado e notifique métricas/auditoria.

**Critérios de aceite:**

- composition root monta todas as implementações;
- falha de observabilidade não corrompe o plano, conforme política documentada;
- reexecução do mesmo comando tem semântica definida e testada;
- concorrência de gravação é detectada ou serializada;
- ADR explica por que cada padrão foi escolhido e qual alternativa foi recusada;
- remover um observador não exige alterar domínio ou repositório.

## Checklist de domínio

- [ ] Explico SOLID por contratos e mudanças, não por slogans.
- [ ] Consigo mostrar uma violação real de LSP com pré/pós-condições.
- [ ] Projeto uma interface a partir do consumidor.
- [ ] Sei quando callback substitui uma classe Strategy.
- [ ] Mantenho formato externo dentro de um Adapter.
- [ ] Uso Factory apenas quando a construção tem uma decisão relevante.
- [ ] Defino ordem, falha e entrega antes de adotar Observer.
- [ ] Defino idempotência/retry antes de enfileirar um Command.
- [ ] Diferencio Repository de CRUD genérico.
- [ ] Consigo remover um padrão prematuro e simplificar o sistema.
- [ ] Demonstro que cada abstração reduz um custo maior do que introduz.

Padrões maduros desaparecem atrás de nomes do domínio. O usuário do planejador
deve entender tarefas, dependências e planos — não uma coleção de siglas.
