# 01 — Complexidade de tempo, espaço e custo real

Complexidade descreve como o consumo de um algoritmo cresce quando a entrada
cresce. Ela não responde quantos milissegundos uma execução levará; responde se
dobrar a entrada tende a manter, dobrar, quadruplicar ou tornar inviável o
trabalho. Essa abstração permite comparar ideias antes de depender de uma máquina,
mas não substitui medição, perfil nem compreensão do modelo de memória.

## Objetivos verificáveis

Ao concluir, você deverá conseguir:

1. definir o tamanho da entrada e a operação elementar de uma análise;
2. distinguir `O`, `Ω` e `Θ` e não confundi-los com melhor, pior e caso médio;
3. derivar custos de laços, recursões e algoritmos com duas dimensões independentes;
4. demonstrar um limite amortizado pelos métodos agregado, contábil ou potencial;
5. calcular espaço auxiliar, pilha, representação da entrada e custo de saída;
6. explicar quando cache, alocação, JIT, GC ou I/O dominam a notação assintótica;
7. analisar e medir o Dependency Planner sem produzir um benchmark enganoso.

## Pré-requisitos e mapa mental

Você deve reconhecer funções, laços, recursão básica e estruturas como vetor,
mapa e conjunto. Use este roteiro para qualquer análise:

```text
entrada e parâmetros
  -> modelo de custo
  -> quantidade de operações
  -> limite assintótico e caso analisado
  -> memória e custo da saída
  -> hipóteses da estrutura/runtime
  -> medição representativa
```

Sem declarar as hipóteses, dizer apenas “é `O(n)`” informa pouco.

## Primeiro defina o que cresce

`n` não significa automaticamente “tamanho”. Em uma string pode ser a quantidade
de bytes, pontos de código ou grafemas. Em um grafo, usar apenas `n` esconde duas
dimensões importantes: vértices `V` e arestas `E`. Em uma consulta entre duas
coleções, use `n` e `m` quando seus tamanhos variam independentemente.

Para o planejador:

- `V`: quantidade de tarefas;
- `E`: quantidade de relações de dependência;
- `L`: total de caracteres dos identificadores, quando hashing/comparação importa;
- `R`: tamanho da resposta serializada.

Depois escolha o modelo de custo. O modelo RAM costuma tratar leitura, escrita,
soma e comparação de valores de tamanho limitado como custo constante. Isso é
uma aproximação. Comparar duas strings pode custar até o tamanho do prefixo comum;
somar inteiros arbitrariamente grandes não é `O(1)`; acessar disco ou rede tem
latência muito diferente de acessar registrador.

## `O`, `Ω` e `Θ` com significado preciso

Para funções não negativas a partir de certo ponto:

- `f(n) ∈ O(g(n))` quando existem constantes `c > 0` e `n₀` tais que
  `f(n) ≤ c g(n)` para todo `n ≥ n₀`: **limite superior**;
- `f(n) ∈ Ω(g(n))` quando existem `c > 0` e `n₀` tais que
  `f(n) ≥ c g(n)` para todo `n ≥ n₀`: **limite inferior**;
- `f(n) ∈ Θ(g(n))` quando ambos valem: **limite assintoticamente justo**.

Se um algoritmo executa `3n² + 7n + 12` operações, ele pertence a `O(n²)`,
`Ω(n²)` e portanto `Θ(n²)`. Também é tecnicamente `O(n³)`, mas esse limite
é menos informativo. Big O não quer dizer automaticamente “pior caso”. É possível
dizer que o melhor caso de uma busca linear é `Θ(1)` e o pior é `Θ(n)`.

| Ordem | Se `n` dobra | Exemplo sob hipóteses usuais |
|---|---:|---|
| `Θ(1)` | quase não muda | ler vetor por índice |
| `Θ(log n)` | acrescenta uma etapa | busca binária |
| `Θ(n)` | aproximadamente dobra | varrer todos os itens |
| `Θ(n log n)` | pouco mais que dobra | mergesort |
| `Θ(n²)` | aproximadamente quadruplica | comparar todos os pares |
| `Θ(2ⁿ)` | eleva ao quadrado | enumerar subconjuntos |
| `Θ(n!)` | multiplica pelo produto de `n+1` até `2n` | enumerar permutações |

A base do logaritmo muda por fator constante: `log₂ n = log₁₀ n / log₁₀ 2`.
Por isso ela costuma ser omitida na notação assintótica, embora importe no
tempo real e em algoritmos que trabalham com bits.

## Melhor, médio, pior e esperado

São eixos diferentes da notação:

- **melhor caso:** menor custo entre entradas de tamanho `n`;
- **pior caso:** maior custo entre entradas de tamanho `n`;
- **caso médio:** média segundo uma distribuição de entradas declarada;
- **esperado:** expectativa sobre aleatoriedade da entrada, do algoritmo ou de ambos.

Uma tabela hash costuma oferecer busca `Θ(1)` esperada sob boa distribuição,
mas pode ter pior caso `Θ(n)` com colisões. Não chame isso de “caso médio” sem
dizer qual distribuição está sendo promediada. Para uma API exposta a chaves
controladas por usuários, o pior caso e as proteções do runtime podem importar.

## Contar laços de forma sistemática

Considere a versão ingênua de detecção de duplicata:

```python
def has_duplicate(values: list[str]) -> bool:
    for i in range(len(values)):
        for j in range(i + 1, len(values)):
            if values[i] == values[j]:
                return True
    return False
```

No pior caso, para cada `i` o laço interno executa `n-i-1` vezes:

```text
(n - 1) + (n - 2) + ... + 1
= n(n - 1) / 2
∈ Θ(n²)
```

Se strings de comprimento até `k` forem comparadas, uma comparação não é
necessariamente constante: o limite fica `O(n²k)`. Com um conjunto:

```python
def has_duplicate(values: list[str]) -> bool:
    seen: set[str] = set()
    for value in values:
        if value in seen:
            return True
        seen.add(value)
    return False
```

Sob hashing esperado constante, o tempo esperado é `Θ(n)` e o espaço adicional
é `O(n)`. O ganho de tempo compra memória e depende do contrato de igualdade e
hash. Incluir o custo de ler todas as strings produz pelo menos `Ω(L)`.

Regras úteis, sempre verificando os limites reais:

- blocos consecutivos somam: `O(n) + O(n²) = O(n²)`;
- laços independentes aninhados multiplicam: `n` por `m` gera `O(nm)`;
- um índice que dobra gera `Θ(log n)` iterações;
- `for j in range(i)` produz soma triangular, não simplesmente “dois laços”;
- gerar ou copiar uma saída de tamanho `R` impõe `Ω(R)`.

## Recorrências e divisão do problema

Algoritmos recursivos podem ser descritos por recorrências. A busca binária faz
trabalho constante e continua em metade:

```text
T(n) = T(n/2) + Θ(1) = Θ(log n)
```

Mergesort resolve duas metades e intercala `n` elementos:

```text
T(n) = 2T(n/2) + Θ(n) = Θ(n log n)
```

Uma forma de enxergar o segundo resultado é a árvore de recursão: existem
`log₂ n` níveis e o trabalho total de cada nível é `Θ(n)`. O Teorema Mestre
formaliza muitos casos `T(n) = aT(n/b) + f(n)`, mas não se aplica automaticamente
a subproblemas de tamanhos irregulares, dependentes ou recorrências como
`T(n)=T(n-1)+T(n-2)`. Antes de invocá-lo, confira suas condições.

O custo em pilha também importa. Busca binária recursiva usa `O(log n)` frames;
um percurso recursivo de uma cadeia de `n` nós usa `O(n)` e pode exceder o limite
da linguagem. Uma versão iterativa pode preservar o tempo e reduzir pilha.

## Análise amortizada não é média probabilística

Uma lista dinâmica com capacidade dobrada oferece `O(1)` **amortizado** por
inserção ao final, embora uma inserção isolada possa copiar `n` elementos. O
limite vale para qualquer sequência de operações do tipo analisado, sem assumir
distribuição aleatória.

### Método agregado

Ao crescer de capacidades `1, 2, 4, ..., 2ᵏ`, as cópias antes de `n` inserções
somam menos que `1 + 2 + 4 + ... + n < 2n`. Somadas às `n` escritas dos novos
itens, o custo total é menor que `3n`; dividido por `n`, resulta constante.

### Método contábil

Cobre-se um valor constante maior por cada inserção barata e guarda-se crédito.
Quando ocorre realocação, o crédito dos itens paga suas cópias. O saldo nunca
pode ficar negativo.

### Método potencial

Define-se uma função de energia acumulada, por exemplo ligada ao tamanho e à
capacidade ociosa. O custo amortizado é o custo real mais a variação dessa
energia. Operações baratas aumentam potencial; a operação cara o consome.

Esses métodos também explicam pilhas com operação `multipop`, contadores binários
e algumas formas de union-find.

## Espaço: mais que contar elementos

Distinga:

- **espaço da entrada:** memória para representar o que foi recebido;
- **espaço auxiliar:** alocações do algoritmo além da entrada;
- **espaço da saída:** inevitável quando o resultado precisa ser materializado;
- **pico de memória:** objetos antigos e novos coexistindo durante cópia/resize;
- **pilha:** frames, variáveis locais e endereços de retorno;
- **overhead:** cabeçalhos, ponteiros, alinhamento, capacidade ociosa e metadados.

Uma lista Python de um milhão de inteiros não é apenas quatro ou oito megabytes:
ela guarda referências e, em geral, objetos inteiros separados. Um array contíguo
de inteiros C tem representação muito mais compacta. Ambos são `Θ(n)`, mas a
constante e o padrão de acesso podem decidir se o sistema cabe na memória.

No planejador, listas de adjacência, contagens, heap e saída ocupam `O(V+E)` em
ordem assintótica. Durante o parsing, o JSON bruto, o objeto decodificado e o
modelo podem coexistir; o pico operacional pode ser várias vezes o tamanho do
arquivo. Assintótico igual não significa consumo igual.

## Hierarquia de memória e localidade

Processadores carregam linhas de cache, não objetos abstratos. Um vetor percorre
endereços contíguos, facilita prefetch e usa cada linha carregada. Uma lista
encadeada exige seguir ponteiros possivelmente espalhados, sofrendo faltas de
cache. Por isso uma varredura `O(n)` em vetor pode ser muito mais rápida que uma
varredura `O(n)` em nós, mesmo que inserir no meio pareça favorecer a lista.

Outros custos ocultos:

- alocações pequenas pressionam o alocador e o coletor de lixo;
- boxing de primitivos cria objetos e indireções;
- branch misprediction penaliza fluxos imprevisíveis;
- JIT precisa aquecer e pode otimizar caminhos quentes;
- paginação e NUMA alteram custos para volumes grandes;
- serialização e I/O podem dominar o algoritmo em aplicações reais.

Big O continua útil: ele filtra soluções que não escalam. Depois dele, perfis e
medições tratam constantes e arquitetura.

## Aplicação no Dependency Planner

Considere o algoritmo de Kahn com listas de adjacência e heap de IDs disponíveis:

1. criar mapas para `V` tarefas: tempo esperado `O(V)`;
2. registrar `E` arestas e graus: tempo esperado `O(E)`;
3. inserir até `V` tarefas no heap: `O(V log V)` se inseridas individualmente;
4. remover exatamente `V` itens em um DAG: `O(V log V)`;
5. percorrer cada aresta uma vez: `O(E)`;
6. materializar a ordem: `Θ(V)`.

Resultado: `O(V + E + V log V)`, normalmente escrito `O(E + V log V)`, e espaço
`O(V+E)`. Se uma fila FIFO substituir o heap, o algoritmo chega a `Θ(V+E)`,
mas o desempate passa a depender da ordem de descoberta/entrada. O `log V` compra
reprodutibilidade lexicográfica.

Se comparar IDs custa `O(k)`, operações do heap podem custar `O(k log V)`. Se as
arestas forem guardadas em uma matriz, o percurso pode subir a `Θ(V²)`, mesmo
quando `E` é pequeno. A representação faz parte da análise.

O melhor caso de uma entrada inválida pode encerrar no primeiro item, mas o pior
caso da validação precisa ler toda a entrada antes de descobrir um ciclo. Não use
o encerramento precoce para anunciar o custo geral.

## Benchmark sem autoengano

Um benchmark confiável começa por hipótese: “trocar busca linear por conjunto
reduz o crescimento quando há muitas consultas de pertencimento”.

```python
from statistics import median
from timeit import repeat

def measure(statement: str, namespace: dict[str, object]) -> float:
    samples = repeat(statement, globals=namespace, number=1_000, repeat=9)
    return median(samples)

for size in (100, 1_000, 10_000, 100_000):
    values = list(range(size))
    values_set = set(values)  # construção fora da região medida
    namespace = {"target": size - 1, "values": values, "values_set": values_set}
    print(size,
          measure("target in values", namespace),
          measure("target in values_set", namespace))
```

Boas práticas:

1. verifique que todas as versões produzem o mesmo resultado;
2. varie tamanhos e formatos: cadeia, leque, grafo esparso e denso;
3. separe construção, algoritmo, serialização e I/O;
4. aqueça JIT e caches quando isso representar a operação real;
5. repita e reporte mediana/percentis, ambiente e dispersão;
6. observe memória de pico, não apenas tempo;
7. evite concluir a partir de um único ponto ou de dados pequenos demais;
8. use profiler no sistema completo antes de otimizar microcódigo.

Tempo de parede inclui escalonador e ambiente; tempo de CPU pode omitir espera;
throughput e latência respondem perguntas diferentes. Declare qual mediu.

## Trade-offs frequentes

| Escolha | Benefício | Custo/risco |
|---|---|---|
| pré-computar mapa | consultas posteriores rápidas | construção e memória |
| ordenar antes | buscas binárias e intervalos | `O(n log n)` inicial e mutações caras |
| memoizar | evita recomputação | invalidação, memória e chaves corretas |
| vetor contíguo | cache e pouco overhead | inserção intermediária desloca itens |
| estrutura ligada | operação local barata | ponteiros, alocação e cache ruim |
| heap no Kahn | menor ID disponível | fator `log V` |
| recursão | código próximo da definição | pilha limitada e overhead de chamada |

O objetivo não é sempre obter a menor classe assintótica. É cumprir escala,
latência, memória, manutenibilidade e previsibilidade com margem.

## Falhas comuns e diagnóstico

### Usar uma letra para tudo

**Sintoma:** BFS chamado de `O(n)`.  
**Correção:** nomeie `V` e `E`; pergunte se o grafo pode ser denso (`E` próximo
de `V²`) ou esparso.

### Contar linhas de código

Uma linha pode executar uma vez, `n` vezes ou ordenar toda uma coleção. Expanda
o custo das operações chamadas e conte frequências.

### Declarar tabela hash como garantia constante

Documente se o limite é esperado, quais chaves existem e que proteções a
implementação oferece. Perfis com muitas colisões ou hashes caros mudam o custo.

### Ignorar criação do índice

Um conjunto oferece consultas esperadas `O(1)`, mas construí-lo custa tempo e
memória. Para uma única consulta em poucos dados, busca linear pode vencer.

### Confundir amortizado com “normalmente rápido”

Exija uma sequência e uma demonstração do custo total. Sistemas de tempo real
podem rejeitar um bom limite amortizado se uma operação isolada não puder pausar.

### Otimizar o trecho errado

Se 90% do tempo está no parser ou no banco, reduzir o algoritmo de 5 ms para
3 ms não muda a experiência. Meça ponta a ponta e depois use profiler.

## Exercícios por nível

### Nível 1 — derivar

1. Determine melhor e pior caso de busca linear, com limite `Θ`.
2. Calcule tempo e espaço auxiliar para copiar uma matriz `n × m`.
3. Analise um laço cujo índice dobra e outro que executa de `0` até `i`.
4. Explique por que `O(n²)` e pior caso não são sinônimos.

**Aceite:** cada resposta define entrada, operação, caso e hipóteses; usa `Θ`
quando o limite é justo.

### Nível 2 — comparar

1. Remova duplicatas preservando ordem com laços e com conjunto; derive ambos.
2. Demonstre por soma geométrica o custo amortizado da lista que dobra capacidade.
3. Compare representação por matriz e lista para grafos com `V=10.000` e
   `E=30.000`, estimando bytes segundo uma linguagem escolhida.
4. Meça busca em lista e conjunto para cinco tamanhos, incluindo construção.

**Aceite:** benchmark repetível, dados e ambiente registrados, resultado correto
antes da medição e conclusão limitada ao que foi medido.

### Nível 3 — analisar o planejador

1. Instrumente cópias ou operações de heap em cadeias e leques crescentes.
2. Compare fila FIFO e heap, verificando custo e determinismo.
3. Meça pico de memória separando parsing e planejamento.
4. Produza uma previsão para dobrar `V` mantendo grau médio constante e confronte
   com os dados.

**Aceite:** relatório separa `V`, `E`, tempo, memória e serialização; qualquer
divergência entre teoria e medição recebe uma hipótese testável.

## Checklist de domínio

- [ ] Defino os parâmetros da entrada antes de escrever Big O.
- [ ] Distingo limite superior, inferior e justo de caso melhor, médio e pior.
- [ ] Derivo somas, laços aninhados e recorrências simples.
- [ ] Sei explicar por que `append` dinâmico é constante amortizado.
- [ ] Conto espaço auxiliar, pilha, pico e representação da saída.
- [ ] Declaro hipóteses sobre hash, comparação e tamanho dos valores.
- [ ] Relaciono localidade, alocação e GC ao desempenho real.
- [ ] Derivo `O(E + V log V)` para o planejador com heap.
- [ ] Elaboro um benchmark que mede a pergunta formulada.

Dominar complexidade é conseguir explicar tanto o crescimento matemático quanto
as condições sob as quais ele representa o sistema executado.
