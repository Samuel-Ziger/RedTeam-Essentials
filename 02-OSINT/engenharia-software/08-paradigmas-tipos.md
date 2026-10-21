# 08 — Paradigmas, tipos, ownership e erros

Paradigmas são formas de organizar estado e comportamento; sistemas reais
costumam combiná-los. Tipos descrevem quais valores e operações são permitidos,
mas não substituem invariantes de negócio. Ownership responde quem pode usar,
alterar e liberar um recurso. Erros descrevem como uma operação deixa de cumprir
seu contrato.

## Objetivos verificáveis

Ao final, você deverá conseguir:

- escolher entre fluxo imperativo, funções puras e objetos por suas forças;
- diferenciar tipagem estática/dinâmica e nominal/estrutural;
- modelar estados válidos sem depender de comentários;
- explicar valor, referência, aliasing, mutabilidade e ownership;
- tratar ausência sem misturá-la com vazio ou falha;
- definir estratégia consistente para erros esperados, infraestrutura e bugs;
- comparar Python, Java, C, C# e JavaScript sem supor garantias inexistentes;
- aplicar objetos imutáveis e portas tipadas ao Dependency Planner.

Pré-requisitos: funções, classes, coleções, memória e exceções. Os exemplos
tornam contratos visíveis; não impõem uma arquitetura.

## Modelo mental: dados válidos e efeitos visíveis

Ao desenhar uma operação, responda:

1. que valores podem entrar e sair?
2. quais combinações são válidas?
3. quem possui cada recurso e por quanto tempo?
4. que estado pode ser alterado?
5. quais efeitos externos ocorrem?
6. quais falhas são esperadas e como o chamador as distingue?

Uma assinatura `process(data) -> data` não responde nada. Uma operação
`planejar(tarefas: Sequence[Tarefa]) -> Plano` já expressa parte do contrato; os
tipos `Tarefa` e `Plano` devem proteger o restante.

## Paradigma imperativo

O estilo imperativo descreve uma sequência de comandos e mudanças de estado.
Ele é natural para I/O, parsing, máquinas de estado e algoritmos eficientes com
estruturas mutáveis.

```python
grau = {tarefa: 0 for tarefa in tarefas}
for origem, destinos in adjacencias.items():
    for destino in destinos:
        grau[destino] += 1
```

O invariante do laço pode ser declarado: após processar um prefixo de arestas,
`grau[v]` conta exatamente quantas arestas desse prefixo chegam a `v`. Sem esse
invariante, mutação vira uma sequência difícil de verificar.

Vantagens: controle explícito, custo previsível e correspondência com operações
de máquina. Riscos: aliasing, ordem implícita e estado parcialmente atualizado
quando ocorre erro. Restrinja o escopo da mutação e não exponha estruturas
incompletas.

## Paradigma funcional

Funções puras devolvem resultado determinado apenas pela entrada e não produzem
efeito observável. Imutabilidade e composição facilitam raciocínio local,
paralelismo e testes.

```python
def duracao_total(tarefas: tuple[Tarefa, ...]) -> int:
    return sum(tarefa.duracao for tarefa in tarefas)
```

Pureza não significa proibir todo estado. Uma aplicação precisa ler arquivo e
mostrar saída; uma estratégia útil é **functional core, imperative shell**:

```text
shell: lê JSON -> core: valida/calcula -> shell: imprime/persiste
```

Imutabilidade também tem custo. Copiar um vetor grande em cada atualização pode
ser caro; linguagens funcionais usam estruturas persistentes com compartilhamento
estrutural. Em Python/Java/C#/JS, use mutação local controlada em algoritmos
quando ela melhora custo e não vaza para consumidores.

## Orientação a objetos

Objetos combinam estado e comportamento atrás de um contrato. São úteis para:

- entidades com identidade e ciclo de vida;
- valores com invariantes;
- recursos cujo uso precisa de protocolo;
- polimorfismo entre implementações de uma porta.

```python
from dataclasses import dataclass


@dataclass(frozen=True)
class Tarefa:
    id: str
    titulo: str
    duracao: int
    dependencias: tuple[str, ...]

    def __post_init__(self) -> None:
        if not self.id.strip():
            raise ValueError("id vazio")
        if not self.titulo.strip():
            raise ValueError("titulo vazio")
        if self.duracao <= 0:
            raise ValueError("duracao deve ser positiva")
```

`Tarefa` é um valor imutável: igualdade pode considerar seus campos. Um projeto,
por outro lado, pode ser entidade identificada por `projeto_id` mesmo quando seu
nome muda. Confundir valor e entidade causa equality, cache e persistência
incorretos.

Herança é apropriada quando há substituição comportamental real. Reutilizar
código por herança cria acoplamento à implementação; composição costuma ser mais
explícita. Uma classe sem invariante, identidade ou polimorfismo pode ser apenas
uma coleção de funções com cerimônia.

## Outros estilos relevantes

SQL e regras de build são **declarativos**: descrevem o resultado. Sistemas
orientados a eventos reagem a fatos e precisam contratar ordem e entrega. Design
orientado a dados prioriza representação e localidade. Atores dão um dono ao
estado e o alteram por mensagens. Esses estilos coexistem; escolha pelo problema.

## Sistemas de tipos: dimensões diferentes

**Estático** significa que certas incompatibilidades são verificadas antes da
execução; **dinâmico**, que o valor é verificado durante a execução. **Nominal**
considera identidade/declaracão do tipo; **estrutural**, suas operações/forma.

| Linguagem | Perfil predominante | Observação importante |
|---|---|---|
| Python | dinâmico; hints estruturais/nominais opcionais | annotations não validam runtime sozinhas |
| Java | estático e principalmente nominal | generics sofrem type erasure; referências aceitam `null` por padrão |
| C | estático, baixo nível | casts e ponteiros permitem quebrar garantias; sem bounds checking geral |
| C# | estático, nominal com recursos modernos | nullable reference types são análise, não novo runtime type |
| JavaScript | dinâmico e coercivo | TypeScript analisa, mas tipos somem no runtime |

Tipagem estática elimina uma classe de programas inválidos, mas não prova “grafo
sem ciclo” ou “duração positiva”. Sistemas dinâmicos ainda precisam de contratos,
validação e testes.

### Nominal versus estrutural

Em Java, uma classe precisa declarar `implements TaskReader`. Em Python, um
objeto que possui `listar()` compatível satisfaz um `Protocol` estrutural para o
verificador. JavaScript usa duck typing em runtime. Tipagem estrutural reduz
adaptação, mas pode confundir formas parecidas; nominal explicita intenção e pode
exigir adaptadores.

## Faça estados inválidos difíceis de representar

Primitivos permitem confusão:

```text
planejar("42", "7")  # qual string é projeto? qual é usuário?
```

Tipos distintos comunicam intenção:

```python
from dataclasses import dataclass


@dataclass(frozen=True)
class ProjetoId:
    valor: str

    def __post_init__(self) -> None:
        if not self.valor.strip():
            raise ValueError("projeto_id vazio")
```

Um value object se paga quando há invariante, unidade, conversão ou risco de
troca. Em C, `typedef` melhora o nome, mas aliases continuam compatíveis; use
`struct` wrapper quando precisar de distinção forte.

### Estados discriminados

Flags booleanas permitem combinações impossíveis:

```text
is_running=True, is_finished=True, has_error=False
```

Modele uma união de estados:

```python
@dataclass(frozen=True)
class Pendente: pass


@dataclass(frozen=True)
class Concluido:
    plano: Plano


@dataclass(frozen=True)
class Falhou:
    motivo: str


Estado = Pendente | Concluido | Falhou
```

Java pode usar sealed interfaces; C combina `enum` e `union` com tag; C# usa
records e switch; TypeScript usa união discriminada com `kind`. Python aceita
união e `match`, mas um verificador estático é necessário para exaustividade.

## Valor, referência, aliasing e cópia

Uma variável pode conter um valor ou uma referência para um objeto. Duas
referências ao mesmo objeto criam **aliasing**: uma mutação é vista pela outra.

```javascript
const original = { tags: ["api"] };
const raso = { ...original };
raso.tags.push("dados");
console.log(original.tags); // ["api", "dados"]
```

O spread copiou o objeto externo, não o array interno. Python apresenta o mesmo
risco com `copy.copy`; Java/C# copiam referências a objetos; em C, copiar uma
`struct` que contém ponteiro copia o endereço, não o bloco apontado.

Defina para cada API:

- **borrow/read-only:** consumidor observa enquanto o dono mantém válido;
- **mutable borrow:** consumidor pode alterar com exclusividade lógica;
- **transferência:** responsabilidade passa ao receptor;
- **cópia:** novo valor independente, raso ou profundo;
- **compartilhamento:** vários usuários, com imutabilidade ou sincronização.

As linguagens do curso não têm o borrow checker de Rust, então o contrato é
expresso por tipos, `const` limitado, convenção, wrappers e testes.

### Particularidades de ownership

**C:** ownership é obrigação explícita. Documente quem chama `free`, se o
ponteiro pode ser `NULL`, tamanho do buffer e validade. Todo caminho de erro deve
liberar o que já foi adquirido; cleanup centralizado pode ajudar.

```c
char *buffer = malloc(tamanho);
if (buffer == NULL) return ERR_MEMORIA;
FILE *arquivo = fopen(caminho, "rb");
if (arquivo == NULL) {
    free(buffer);
    return ERR_ARQUIVO;
}
/* ... */
fclose(arquivo);
free(buffer);
```

**Java/C#/Python/JavaScript:** garbage collection não encerra deterministicamente
arquivo, socket, lock ou transação. Use
try-with-resources (Java), `using`/`await using` (C#), `with` (Python) e
`try/finally` ou APIs explícitas (JavaScript). GC não substitui ownership de
recursos.

## Ausência não é vazio nem erro

`null`, `None`, `undefined`, ponteiro nulo, lista vazia e exceção comunicam coisas
diferentes:

- tarefa não encontrada: ausência esperada;
- projeto existe e não tem tarefas: coleção vazia válida;
- fonte indisponível: falha;
- função esqueceu de retornar: defeito, especialmente em JavaScript/Python.

Contrato possível: `buscar(id) -> Tarefa | None`; o chamador trata ausência. Já
`listar() -> tuple[Tarefa, ...]` deve devolver tupla vazia, nunca `None`.

| Linguagem | Técnicas para ausência |
|---|---|
| Python | `T | None`, checagem explícita; evite truthiness quando zero/vazio é válido |
| Java | `Optional<T>` em retornos selecionados; referências ainda podem ser `null` |
| C | ponteiro `NULL` + código/status; não desreferencie sem contrato |
| C# | `T?`, nullable annotations e pattern matching |
| JavaScript | `undefined`/`null`; escolha um contrato e use `===` |

Não use `-1` se for valor legítimo. Não transforme falha de banco em “não
encontrado”; isso pode criar duplicata.

## Modelagem de erros

Classifique antes de escolher mecanismo:

1. **erro esperado do domínio:** ciclo de dependência, tarefa ausente;
2. **entrada inválida na borda:** JSON truncado, campo com tipo incorreto;
3. **falha transitória de infraestrutura:** timeout, indisponibilidade;
4. **falha permanente/configuração:** arquivo sem permissão, schema incompatível;
5. **cancelamento:** chamador não precisa mais do resultado;
6. **defeito de programação:** índice impossível, invariante interna quebrada.

O chamador precisa distinguir o que pode corrigir, repetir ou reportar. Uma
mensagem textual não é categoria estável.

```python
class ErroDePlanejamento(Exception):
    """Base para falhas esperadas da operação."""


class CicloDeDependencia(ErroDePlanejamento):
    def __init__(self, caminho: tuple[str, ...]) -> None:
        super().__init__("ciclo de dependencia")
        self.caminho = caminho


def carregar_e_planejar(caminho: str) -> Plano:
    try:
        tarefas = LeitorJson(caminho).listar()
        return planejar(tarefas)
    except OSError as erro:
        raise FonteIndisponivel(caminho) from erro
```

Preservar a causa ajuda diagnóstico. Traduza uma vez na fronteira: a CLI converte
`CicloDeDependencia` em mensagem e código de saída; uma API poderia convertê-lo
em erro HTTP. O domínio não deve conhecer `stderr` ou status HTTP.

### Exceção ou resultado?

Use o mecanismo idiomático e considere frequência/controle:

- exceção funciona bem para abandonar uma operação por caminho não local;
- resultado discriminado torna erro esperado visível na assinatura;
- código de erro em C exige checagem disciplinada e parâmetros de saída;
- não use exceção para controle de laço normal nem ignore retorno.

Java separa checked/unchecked, mas a categoria da linguagem não decide se retry
é seguro. C# não tem checked exceptions. JavaScript rejeita promises com qualquer
valor; normalize para objetos `Error`. Python permite capturar amplamente, mas
`except Exception: pass` destrói evidência e pode deixar estado parcial.

### Cleanup e atomicidade

Se uma função adquire A, depois B e falha, precisa liberar A. Use estruturas de
escopo. Se altera múltiplos estados, defina se a operação é atômica, compensável
ou parcial. `finally` garante tentativa de cleanup; não garante rollback de uma
ação remota.

Nunca faça retry indiscriminado. Repita somente falha classificada como
transitória, operação idempotente ou deduplicada, com limite, backoff e deadline.

## Polimorfismo útil no Dependency Planner

O caso de uso depende de uma porta:

```python
from typing import Protocol


class LeitorDeTarefas(Protocol):
    def listar(self) -> tuple[Tarefa, ...]: ...
```

JSON, memória ou banco podem satisfazer o contrato. O polimorfismo existe para
separar política estável de mecanismo variável, não para demonstrar herança. A
porta real está em
[ports.py](projetos/dependency-planner/src/dependency_planner/ports.py); o
adaptador em
[repository.py](projetos/dependency-planner/src/dependency_planner/repository.py)
valida a borda, e o domínio recebe objetos válidos.

Imutabilidade de `WorkItem` permite compartilhar tarefas entre algoritmo e
relatório sem medo de alteração intermediária. Ainda há objetos internos
mutáveis no algoritmo para eficiência; eles não escapam da função.

## Concorrência, ownership e efeitos

Estado mutável compartilhado exige sincronização e política de propriedade.
Prefira mensagens imutáveis e dono único. `async` permite não bloquear a thread
durante I/O; não torna cálculo CPU-bound mais rápido e não elimina corridas.

Uma função pura pode executar em paralelo se as entradas e saídas forem
independentes. Um objeto “imutável” que contém lista mutável ainda pode ter race.
Em Java/C#, coleções read-only podem ser apenas views; em Python, `frozen=True`
não congela objetos internos; em JavaScript, `Object.freeze` é raso.

## Trade-offs e contraexemplos

- Tipos muito genéricos (`dict[str, object]`, `Object`, `any`) movem falhas para
  runtime e escondem contrato.
- Um tipo por campo pode gerar cerimônia sem invariantes relevantes.
- Imutabilidade total pode copiar volumes grandes; mutação local encapsulada pode
  ser mais segura que uma API complexa de compartilhamento.
- Exceções tornam assinatura concisa, mas falhas esperadas podem ficar invisíveis.
- Resultado explícito aumenta ramificações, mas força tratamento.
- Herança reduz duplicação imediata e aumenta dependência de longo prazo.
- Tipos não provam semântica; testes sem tipos não documentam todas as combinações.

## Falhas comuns e diagnóstico

| Sintoma | Hipótese | Diagnóstico |
|---|---|---|
| mudança em uma cópia altera original | cópia rasa/aliasing | compare identidade dos objetos internos |
| `null` aparece longe da origem | ausência não modelada | torne retorno opcional na primeira fronteira |
| recurso fica aberto | GC tratado como cleanup | use mecanismo de escopo e teste falha intermediária |
| erro vira lista vazia | falha confundida com ausência | teste fonte indisponível separadamente |
| cast explode em runtime | tipo amplo demais | reduza tipo e valide na borda |
| objeto “imutável” muda | coleção interna compartilhada | converta/copie na construção |
| retry duplica efeito | erro e idempotência indefinidos | classifique operação e use chave de deduplicação |
| subclasses exigem `if tipo` | polimorfismo não preserva contrato | revise LSP ou prefira composição |

## Laboratórios

### Básico — valor válido e erro explícito

Modele `Tarefa` imutável e `buscar_tarefa` com ausência explícita nas cinco
linguagens, ao menos em pseudocódigo compilável onde o ambiente não existir.

**Critérios de aceite:** ID vazio e duração não positiva são impossíveis após a
construção; lista vazia difere de tarefa ausente; cópia não permite mutação
acidental; cada linguagem documenta sua garantia e sua limitação.

### Intermediário — functional core, imperative shell

Separe leitura JSON, cálculo e apresentação do planejador.

**Critérios de aceite:** núcleo não acessa arquivo/console; erros de documento,
ciclo e I/O são categorias distintas; a CLI traduz cada categoria uma vez;
testes puros cobrem regra e integração cobre ownership do arquivo; nenhuma causa
é descartada.

### Avançado — protocolo de recurso e concorrência

Adicione um repositório com transação ou uma fonte remota simulada, incluindo
cancelamento e timeout.

**Critérios de aceite:** ciclo de vida está documentado; recurso fecha em sucesso
e erro; retry só ocorre para caso transitório e idempotente; coleção devolvida
não pode corromper estado interno; teste concorrente reproduz e elimina uma race;
ADR compara exceção e resultado discriminado.

## Checklist de domínio

- [ ] Escolho paradigma por estado, efeitos e invariantes.
- [ ] Distingo tipagem estática/dinâmica e nominal/estrutural.
- [ ] Sei quais regras o compilador prova e quais exigem runtime/testes.
- [ ] Modelo combinações inválidas como estados distintos ou impossíveis.
- [ ] Explico cópia rasa, profunda, aliasing e ownership.
- [ ] Defino quem fecha/libera recursos em todos os caminhos.
- [ ] Não confundo ausência, vazio, falha e defeito.
- [ ] Traduzo erro na fronteira sem perder causa.
- [ ] Defino idempotência antes de retry.
- [ ] Uso polimorfismo para uma variação real e preservo substituição.
- [ ] Consigo mostrar no Dependency Planner onde há pureza e mutação local.

No próximo capítulo, esses contratos serão organizados em fronteiras modulares,
com dependências apontando para as políticas mais estáveis.
