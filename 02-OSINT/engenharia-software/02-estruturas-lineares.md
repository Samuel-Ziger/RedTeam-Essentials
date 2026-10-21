# 02 — Estruturas lineares e tabelas hash

Uma estrutura de dados é um conjunto de operações com contratos e custos, não
apenas um tipo oferecido pela linguagem. Duas estruturas capazes de armazenar a
mesma sequência podem ter comportamento muito diferente em acesso, inserção,
memória, cache e concorrência. A escolha correta começa pelas operações dominantes
e pelas invariantes que precisam permanecer verdadeiras.

## Objetivos verificáveis

Ao concluir, você deverá conseguir:

1. explicar a representação e os custos de vetor, lista ligada, pilha, fila e deque;
2. implementar um buffer circular sem deslocar elementos;
3. manter invariantes de tamanho, capacidade, cabeça e cauda, inclusive no vazio;
4. explicar colisões, fator de carga, redimensionamento e contratos de hash/igualdade;
5. comparar encadeamento separado e endereçamento aberto;
6. relacionar layout, indireção e localidade de cache ao desempenho observado;
7. justificar as coleções usadas no Dependency Planner.

## Pré-requisitos e mapa mental

Revise referências/ponteiros, arrays, classes ou structs e a diferença entre custo
pior e amortizado no [capítulo 01](01-complexidade.md).

```text
sequência
  + acesso por posição -> vetor dinâmico
  + inserção local conhecida -> lista ligada
  + uma ponta -> pilha ou fila
  + duas pontas -> deque/buffer circular

associação
  + chave -> valor -> mapa
  + apenas pertencimento -> conjunto
  + ordem não necessária -> tabela hash como candidata
```

Antes de escolher, escreva: operações, frequência, volume, ordem exigida, limite
de memória, padrão de mutação e comportamento em falha.

## Vetores: contiguidade como contrato físico

Um vetor armazena elementos de tamanho fixo em endereços contíguos. Se o primeiro
elemento está em `base` e cada elemento ocupa `s` bytes, o endereço do índice `i`
é `base + i*s`. Esse cálculo explica o acesso `Θ(1)` e exige índice válido.

```c
#include <stddef.h>

int at(const int *values, size_t length, size_t index, int *out) {
    if (values == NULL || out == NULL || index >= length) {
        return 0;
    }
    *out = values[index];
    return 1;
}
```

O contrato separa sucesso do valor armazenado: retornar `0` como erro seria
ambíguo se zero for elemento válido. Em C, o chamador continua responsável pela
vida útil de `values` e `out`.

Varreduras sequenciais aproveitam linhas de cache e prefetch do processador.
Inserir no meio, entretanto, desloca um sufixo: no pior caso `Θ(n)`. Remover
preservando ordem também desloca; se ordem não importa, substituir o removido pelo
último pode reduzir a operação para `Θ(1)`, alterando o contrato.

## Vetores dinâmicos

Um vetor dinâmico mantém:

- `0 ≤ size ≤ capacity`;
- os elementos válidos ocupam `[0, size)`;
- a região `[size, capacity)` está reservada, mas não faz parte da sequência;
- nenhuma referência ao armazenamento antigo permanece válida após realocação,
  salvo garantia específica da linguagem.

Quando `size == capacity`, uma política comum aloca capacidade multiplicada por
um fator, copia os itens e libera a região antiga. Dobrar produz `append` `O(1)`
amortizado e pico temporário de memória. Crescer exatamente uma posição faria
`1 + 2 + ... + n = Θ(n²)` cópias para `n` inserções.

| Linguagem | Estrutura comum | Detalhe relevante |
|---|---|---|
| Python | `list` | vetor de referências, não de objetos inline |
| Java | `ArrayList<T>` | primitivos sofrem boxing; iteradores detectam certas mutações |
| C | array/alocação manual | capacidade, overflow e propriedade são explícitos |
| C# | `List<T>` | `Capacity` difere de `Count`; structs podem ficar inline |
| JavaScript | `Array` | motor especializa layouts; buracos e tipos mistos podem degradá-los |

Reservar capacidade antecipadamente evita realocações quando há uma estimativa
boa, mas reservar demais desperdiça memória.

## Listas ligadas

Uma lista simplesmente ligada guarda valor e referência ao próximo nó:

```c
typedef struct Node {
    int value;
    struct Node *next;
} Node;
```

Invariantes típicas:

- `head == NULL` se, e somente se, o tamanho é zero;
- seguindo `next` a partir de `head`, alcançam-se exatamente `size` nós;
- o último aponta para `NULL` em uma lista não circular;
- nenhum nó aparece duas vezes;
- em lista duplamente ligada, `x.next.prev == x` e `x.prev.next == x` onde definidos.

Inserir depois de um nó **já conhecido** custa `Θ(1)`. Encontrar esse nó pelo
índice custa `Θ(n)`. A frase “inserção em lista ligada é constante” omite essa
pré-condição. Remover exige atualizar todos os elos envolvidos; em C, também
liberar exatamente uma vez e evitar uso posterior.

Cada nó traz ponteiros, alinhamento e uma alocação potencialmente dispersa. A
varredura sofre indireção e faltas de cache. Na prática, vetores frequentemente
vencem listas para sequências pequenas ou percorridas com frequência, mesmo com
alguns deslocamentos. Listas brilham quando já se possui o nó, endereços precisam
ser estáveis ou elementos são frequentemente ligados e desligados.

## Pilha: LIFO com uma fronteira pequena

Uma pilha oferece `push`, `pop`, `peek` e `is_empty`; o último item inserido sai
primeiro. Sua invariante essencial é que apenas o topo muda. Aplicações incluem
histórico de desfazer, interpretação de expressões e DFS iterativa.

```python
def balanced(text: str) -> bool:
    opening = {"(", "[", "{"}
    expected = {")": "(", "]": "[", "}": "{"}
    stack: list[str] = []

    for char in text:
        if char in opening:
            stack.append(char)
        elif char in expected:
            if not stack or stack.pop() != expected[char]:
                return False
    return not stack
```

Invariante do laço: `stack` contém exatamente os delimitadores abertos e ainda
não fechados do prefixo lido, na ordem em que precisam ser fechados. O tempo é
`Θ(n)` porque cada caractere é examinado uma vez; o espaço é `O(n)` e chega a
esse limite com uma entrada formada somente por aberturas.

Em uma função desfazer/refazer, uma nova ação após `undo` deve limpar a pilha de
refazer; essa é uma regra do domínio, não da estrutura.

## Fila, deque e buffer circular

Fila é FIFO: inserir no fim, retirar no início. Deque opera eficientemente nas
duas pontas. Remover o primeiro elemento de um vetor deslocando os demais custa
`Θ(n)`; uma fila precisa de nós ligados ou de índices.

Um buffer circular de capacidade fixa usa o array como um anel:

```python
class RingQueue:
    def __init__(self, capacity: int) -> None:
        if capacity <= 0:
            raise ValueError("capacity must be positive")
        self._data: list[object | None] = [None] * capacity
        self._head = 0
        self._size = 0

    def enqueue(self, value: object) -> None:
        if self._size == len(self._data):
            raise OverflowError("queue is full")
        tail = (self._head + self._size) % len(self._data)
        self._data[tail] = value
        self._size += 1

    def dequeue(self) -> object:
        if self._size == 0:
            raise IndexError("queue is empty")
        value = self._data[self._head]
        self._data[self._head] = None
        self._head = (self._head + 1) % len(self._data)
        self._size -= 1
        return value
```

Invariantes: `0 ≤ size ≤ capacity`; `head` está no intervalo do array; os
`size` itens lógicos começam em `head` e continuam módulo `capacity`. Zerar a
posição retirada evita reter objetos desnecessariamente em runtimes com GC.

A semântica de fila cheia precisa ser explícita:

- rejeitar oferece backpressure ao chamador;
- bloquear exige sincronização e política de cancelamento;
- descartar o novo preserva o backlog;
- sobrescrever o mais antigo preserva dados recentes;
- crescer perde o limite fixo de memória.

Em telemetria, áudio e sistemas embarcados, essa escolha altera o significado dos
dados. Nenhuma é apenas uma decisão de implementação.

## Tabelas hash: da chave ao compartimento

Um mapa associa chave a valor; um conjunto armazena apenas pertencimento. Uma
tabela hash calcula um inteiro a partir da chave e o reduz a uma posição. Como o
número de chaves é maior que o de compartimentos, colisões são inevitáveis.

O contrato fundamental é:

```text
se a == b, então hash(a) == hash(b)
```

O inverso não é exigido: hashes iguais podem representar chaves diferentes. Se
campos usados em igualdade/hash mudam depois da inserção, a chave pode ficar no
compartimento antigo e tornar-se logicamente “perdida”. Use chaves imutáveis ou
identidade estável.

### Encadeamento separado

Cada compartimento aponta para uma coleção de entradas. Colisões ficam na mesma
coleção. Remoção é direta, e o fator de carga pode superar 1, mas existem
ponteiros/alocações e localidade pior. Algumas implementações transformam baldes
muito grandes em árvores para limitar degradação.

### Endereçamento aberto

Todas as entradas ficam no próprio array. Em colisão, uma sequência de sondagem
procura outra posição: linear, quadrática ou hash duplo. A localidade pode ser
boa, mas o desempenho degrada quando o array enche. Remover geralmente deixa um
marcador de tumba; transformar a posição diretamente em vazia poderia interromper
uma busca por uma chave colocada mais adiante pela mesma colisão.

O **fator de carga** `α = itens / compartimentos` governa colisões. Ao cruzar um
limite, a tabela aloca outra capacidade e reinsere itens, pois a posição depende
da capacidade. A operação individual pode custar `Θ(n)`, mas com crescimento
geométrico a sequência costuma oferecer inserção `O(1)` amortizada.

Busca, inserção e remoção são `O(1)` **esperadas** sob hash bem distribuído e
controle de carga; o pior caso é `O(n)`. Runtimes podem aleatorizar hashes para
dificultar entradas hostis. Ainda assim, limite tamanho e não use hashes não
criptográficos como prova de autenticidade.

## Exemplo trabalhado: cache LRU

Um cache *least recently used* precisa buscar por chave, promover um item para o
início e remover o menos recente. Nenhuma estrutura isolada oferece tudo em
tempo constante:

- mapa `chave -> nó` localiza em tempo esperado `O(1)`;
- lista duplamente ligada remove/promove um nó conhecido em `O(1)`;
- a cauda identifica a vítima em `O(1)`.

Invariantes:

1. mapa e lista possuem exatamente as mesmas chaves;
2. cada chave aparece uma vez;
3. cabeça é a mais recente, cauda é a menos recente;
4. tamanho não supera capacidade;
5. elos anterior/próximo são simétricos.

Evicção precisa retirar a cauda **da lista e do mapa**. Atualizar apenas um cria
vazamento ou devolve valor expirado. Em concorrência, uma trava global simples
pode preservar as invariantes; tentar travas finas sem protocolo claro introduz
ciclos, nós duplicados e races.

## Tabela de custos e hipóteses

| Operação | Vetor dinâmico | Lista ligada | Deque circular | Hash |
|---|---:|---:|---:|---:|
| acesso por índice | `Θ(1)` | `Θ(n)` | `Θ(1)` se exposto | não se aplica |
| busca por valor | `Θ(n)` | `Θ(n)` | `Θ(n)` | `O(1)` esperada |
| inserir no fim | `O(1)` amort. | `Θ(1)` com cauda | `Θ(1)` | `O(1)` amort./esp. |
| inserir no meio conhecido | `Θ(n)` | `Θ(1)` | `Θ(n)` | não se aplica |
| remover nas pontas | fim `Θ(1)`; início `Θ(n)` | cabeça `Θ(1)`; cauda `Θ(1)` em lista dupla | `Θ(1)` | não se aplica |
| localidade | alta | baixa | alta | depende da estratégia |

Custos de lista pressupõem referência ao nó correto; custos de hash pressupõem
hash/igualdade adequados. Registrar a hipótese é parte da resposta.

## Aplicação no Dependency Planner

O planejador usa estruturas distintas porque as perguntas são distintas:

- mapa `id -> tarefa`: validar unicidade e resolver dependência sem varrer `V`;
- conjunto por tarefa: impedir aresta duplicada;
- lista de adjacência: percorrer apenas sucessoras existentes;
- mapa `id -> grau`: acompanhar dependências ainda pendentes;
- vetor de resultado: acumular ordem com `append` amortizado;
- heap, estudado no próximo capítulo: escolher o menor ID disponível.

Faça uma simulação de `modelo -> {api, web} -> entrega`. Depois de processar
`modelo`, somente os graus de `api` e `web` mudam; uma matriz exigiria examinar
todas as tarefas. Para um grafo esparso, a lista evita trabalho e espaço `V²`.

Uma otimização perigosa seria usar o mesmo objeto mutável como chave e alterar
seu ID. O mapa deixaria de representar a identidade. No domínio, tarefa e ID
devem ser imutáveis durante um planejamento.

## Falhas comuns e diagnóstico

### Fila implementada com remoção do índice zero

**Sintoma:** tempo quadrático em cargas grandes.  
**Diagnóstico:** conte elementos deslocados ou use profiler. Troque por deque ou
índice de cabeça, cuidando para não reter um prefixo morto indefinidamente.

### Estado vazio inconsistente

**Sintoma:** `head` nulo, `tail` não nulo ou tamanho negativo.  
**Diagnóstico:** verifique invariantes depois de toda mutação, especialmente
transições `0 -> 1` e `1 -> 0`.

### Off-by-one em buffer circular

**Sintoma:** capacidade efetiva menor ou item sobrescrito.  
**Diagnóstico:** escolha uma representação sem ambiguidade: mantenha `size`, ou
reserve uma posição para distinguir cheio de vazio. Não misture convenções.

### Chave mutável ou igualdade inconsistente

**Sintoma:** chave visível na iteração, mas busca falha.  
**Diagnóstico:** registre hash antes/depois da mutação e teste `a == b` junto de
`hash(a) == hash(b)`.

### Confiar em ordem acidental do mapa

Algumas linguagens preservam inserção; outras versões ou estruturas não. Se a
ordem é requisito, escolha uma coleção cujo contrato a garanta ou ordene a saída.

### Escolher lista ligada apenas por inserção `O(1)`

Inclua o custo de encontrar a posição e o padrão de leitura. Meça com volume e
layout representativos; em sequências pequenas, cache domina muitas diferenças.

## Exercícios por nível

### Nível 1 — invariantes

1. Implemente pilha sobre vetor dinâmico e defina `pop` no vazio.
2. Desenhe estados de uma fila circular de capacidade quatro após duas voltas.
3. Compare bytes teóricos de mil inteiros em vetor e lista duplamente ligada.

**Aceite:** operações preservam tamanho e limites; testes cobrem vazio, um item,
cheio e transição no módulo da capacidade.

### Nível 2 — compor estruturas

1. Implemente deque circular que cresce geometricamente.
2. Crie histórico desfazer/refazer com duas pilhas e documente nova ação após undo.
3. Implemente LRU com mapa e lista dupla.

**Aceite:** testes de propriedades comparam deque a uma coleção de referência;
LRU nunca excede capacidade e lista/mapa mantêm as mesmas chaves.

### Nível 3 — medir e defender

1. Compare vetor e lista ligada em inserção e varredura, registrando alocações.
2. Implemente tabela hash educacional com encadeamento, resize e chaves conflitantes.
3. Troque os conjuntos de dependências do planejador por listas e meça entradas
   com duplicatas; depois reverta a experiência.

**Aceite:** relatório separa custo assintótico de efeito de cache; a tabela hash
preserva valores em resize e trata atualizar uma chave sem aumentar tamanho.

## Checklist de domínio

- [ ] Derivo o endereço de um item no vetor e explico sua localidade.
- [ ] Explico `append` amortizado e pico de memória no crescimento.
- [ ] Declaro a pré-condição por trás da inserção `O(1)` em lista.
- [ ] Mantenho invariantes nas transições vazio/não vazio.
- [ ] Implemento pilha, fila e buffer circular com erros definidos.
- [ ] Explico colisão, fator de carga, resize e tumbas.
- [ ] Garanto coerência entre igualdade e hash e evito chaves mutáveis.
- [ ] Escolho estrutura pelas operações dominantes e pela memória real.
- [ ] Justifico cada coleção usada no Dependency Planner.

Domínio aqui significa enxergar tanto a interface abstrata quanto os bytes,
ponteiros e invariantes que tornam essa interface correta e eficiente.
