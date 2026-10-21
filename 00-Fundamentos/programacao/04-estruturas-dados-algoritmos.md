# Estruturas de dados e algoritmos: correção, custo e escolha

Uma estrutura de dados organiza informação; um algoritmo transforma informação.
Os dois são inseparáveis: escolher um conjunto pode reduzir uma busca quadrática
a uma passagem linear, enquanto escolher uma fila em vez de uma pilha muda a
ordem de exploração de um grafo.

O objetivo não é decorar problemas de entrevista. É aprender um processo:

1. definir contrato e exemplos;
2. escolher representação;
3. estabelecer uma solução correta e simples;
4. justificar correção por invariante ou decomposição;
5. analisar tempo e espaço;
6. medir com entradas representativas;
7. otimizar somente quando o requisito justificar.

## Objetivos de aprendizagem

Ao concluir, você deverá conseguir:

- distinguir tipo abstrato de dados, implementação e interface da linguagem;
- calcular complexidade de laços, chamadas e estruturas compostas;
- escolher entre sequência, mapa, conjunto, pilha, fila, heap, árvore e grafo;
- implementar e explicar busca binária, BFS, DFS e ordenação por intercalação;
- reconhecer quando usar dois ponteiros, janela deslizante, divisão e conquista,
  guloso, programação dinâmica ou backtracking;
- declarar invariantes e argumentar por que um algoritmo está correto;
- medir desempenho sem confundir benchmark com prova assintótica;
- considerar memória, localidade, mutabilidade, estabilidade e casos de
  fronteira na escolha.

## 1. Antes da velocidade: contrato e tamanho da entrada

Considere “encontre um usuário pelo nome”. Faltam decisões:

- nomes são únicos?
- comparação diferencia maiúsculas e acentos?
- os dados mudam com frequência?
- quantas buscas ocorrerão por atualização?
- resultado ausente é erro ou valor opcional?
- qual é o tamanho máximo `n`?

Se existe uma única busca em dez itens, uma lista pode ser perfeita. Se existem
milhões de consultas por chave única, construir um mapa pode compensar. Sem
contrato e carga esperada, “estrutura mais rápida” não significa nada.

Defina `n` explicitamente. Em uma matriz pode ser número de células; em um
grafo, geralmente usamos `V` vértices e `E` arestas. Em duas entradas
independentes, use `n` e `m`.

## 2. Tipo abstrato, implementação e biblioteca

Um **tipo abstrato de dados (TAD)** especifica operações e comportamento. Uma
**implementação** decide representação e custo.

Exemplo: fila é o contrato “inserir no final e remover do início”. Pode ser
implementada com:

- array circular;
- lista ligada com ponteiros para início e fim;
- deque oferecido pela biblioteca.

A sintaxe da biblioteca não muda o contrato. Nas cinco linguagens:

| Conceito | Python | Java | C# | JavaScript | C |
|----------|--------|------|----|------------|---|
| sequência dinâmica | `list` | `ArrayList` | `List<T>` | `Array` | implementar/vetor alocado |
| mapa hash | `dict` | `HashMap` | `Dictionary<K,V>` | `Map` | implementar/biblioteca escolhida |
| conjunto hash | `set` | `HashSet` | `HashSet<T>` | `Set` | implementar/biblioteca escolhida |
| fila dupla | `collections.deque` | `ArrayDeque` | `LinkedList<T>` | array ou estrutura própria | estrutura própria |
| heap | `heapq` | `PriorityQueue` | `PriorityQueue<TElement,TPriority>` | estrutura própria | estrutura própria |

Conhecer o nome não basta: confirme documentação de complexidade, igualdade,
ordenação, mutabilidade e comportamento concorrente da implementação concreta.

## 3. Como analisar complexidade

Notação assintótica descreve como o custo cresce quando a entrada cresce. Ela
não prevê segundos exatos.

- **O(g(n))**: limite superior assintótico; crescimento não pior que essa ordem
  sob as premissas declaradas;
- **Ω(g(n))**: limite inferior;
- **Θ(g(n))**: limite justo, superior e inferior da mesma ordem.

No uso cotidiano, “Big O” frequentemente comunica um limite de pior caso. Seja
preciso ao falar de caso médio, amortizado ou esperado.

| Complexidade | Exemplo | `n` dobra |
|--------------|---------|-----------|
| Θ(1) | acesso por índice em array | quase igual |
| Θ(log n) | busca binária | acrescenta uma etapa |
| Θ(n) | percorrer todos os itens | aproximadamente dobra |
| Θ(n log n) | merge sort | pouco mais que dobra |
| Θ(n²) | examinar todos os pares | aproximadamente quadruplica |
| Θ(2ⁿ) | enumerar subconjuntos ingênuo | aproximadamente eleva ao quadrado |

### Regras práticas de derivação

1. operações sequenciais somam custos;
2. laços aninhados multiplicam quantidades de iterações;
3. em ramos, o pior caso toma o ramo dominante;
4. descarte constantes e termos de menor ordem no limite assintótico;
5. chamadas de biblioteca também possuem custo;
6. construir uma estrutura auxiliar conta em tempo e memória.

```python
def contem(valores: list[int], alvo: int) -> bool:
    for valor in valores:        # no pior caso, n iterações
        if valor == alvo:        # custo constante sob a premissa de inteiros
            return True
    return False                 # tempo O(n), espaço extra O(1)
```

```python
def pares(valores: list[int]) -> list[tuple[int, int]]:
    resultado = []
    for i in range(len(valores)):
        for j in range(i + 1, len(valores)):
            resultado.append((valores[i], valores[j]))
    return resultado
```

O segundo algoritmo produz `n(n-1)/2` pares: tempo Θ(n²). A própria saída ocupa
Θ(n²), então nenhum algoritmo que materialize todos os pares pode usar menos
espaço total que a quantidade produzida.

### Pior caso, caso médio e amortização

Adicionar ao final de um vetor dinâmico é ocasionalmente O(n), quando o buffer
precisa crescer e copiar elementos. Em uma longa sequência de inserções, o custo
**amortizado** costuma ser O(1). Isso não garante que cada inserção seja constante.

Busca em tabela hash é O(1) **esperado/médio** sob boa dispersão e política de
redimensionamento, mas colisões adversas ou implementação específica alteram o
pior caso.

## 4. Tempo real, memória e localidade

Duas soluções O(n) podem ter desempenhos diferentes por:

- constantes e quantidade de alocações;
- acesso contíguo versus indireções na memória;
- cache da CPU;
- representação compacta versus objetos;
- custo de hash, comparação ou conversão;
- runtime, coleta de lixo e otimização JIT;
- distribuição real das entradas.

Big O orienta escala; benchmark avalia uma implementação em um ambiente. Use os
dois. Primeiro evite ordem de crescimento incompatível com o requisito. Depois
meça.

## 5. Sequências: arrays, vetores dinâmicos e listas ligadas

### Array/vetor contíguo

Vantagens:

- acesso por índice O(1);
- boa localidade de cache;
- iteração simples e eficiente.

Custos:

- inserir/remover no início ou meio exige deslocamento O(n);
- array de C tem tamanho fixo; vetores dinâmicos realocam ocasionalmente;
- uma fatia pode copiar dados ou criar uma visão, conforme a linguagem/API.

### Lista ligada

Cada nó guarda valor e referência ao próximo; na versão duplamente ligada,
também ao anterior. Inserir após um nó conhecido pode ser O(1), mas encontrar o
nó é O(n). Ela adiciona alocações e indireções e geralmente perde em localidade.

Não conclua “muitas inserções = lista ligada”. Pergunte onde ocorre a inserção,
como o ponto é localizado e como a estrutura é percorrida.

### Matriz

Uma matriz `linhas × colunas` possui Θ(linhas × colunas) células. Ao representar
um tabuleiro plano, converta coordenadas com cuidado:

```python
def indice(linha: int, coluna: int, colunas: int) -> int:
    return linha * colunas + coluna
```

Valide cada dimensão. Erros de índice em C podem acessar memória indevida; em
linguagens gerenciadas normalmente geram exceção.

## 6. Mapa e conjunto: associação, unicidade e igualdade

Use **mapa** quando precisa associar chave a valor; **conjunto** quando precisa
apenas de pertencimento ou unicidade.

Problema: detectar o primeiro valor repetido.

Versão ingênua:

```python
def primeira_repeticao_quadratica(valores: list[int]) -> int | None:
    for i in range(len(valores)):
        for j in range(i):
            if valores[i] == valores[j]:
                return valores[i]
    return None
```

Versão com conjunto:

```python
def primeira_repeticao(valores: list[int]) -> int | None:
    vistos: set[int] = set()
    for valor in valores:
        if valor in vistos:
            return valor
        vistos.add(valor)
    return None
```

A segunda usa tempo esperado O(n) e espaço O(n). Não é “gratuitamente melhor”:
troca memória adicional por tempo.

### Hash, igualdade e chaves mutáveis

Uma tabela hash calcula um índice aproximado a partir da chave e resolve
colisões. Chaves consideradas iguais precisam produzir hash compatível. Alterar
uma chave enquanto ela está na tabela pode torná-la inalcançável; por isso APIs
exigem chaves imutáveis ou igualdade/hash estáveis.

Não confunda mapa hash com mapa ordenado. Se precisa percorrer por chave em ordem,
consultar intervalos ou obter menor/maior eficientemente, uma árvore balanceada
ou ordenação posterior pode ser mais apropriada.

## 7. Pilha, fila, deque e fila de prioridade

### Pilha — LIFO

O último a entrar é o primeiro a sair. Usos: desfazer, parsing, DFS iterativa e
simulação de chamadas.

Parênteses balanceados:

```python
def balanceado(texto: str) -> bool:
    pares = {")": "(", "]": "[", "}": "{"}
    pilha: list[str] = []

    for caractere in texto:
        if caractere in "([{":
            pilha.append(caractere)
        elif caractere in pares:
            if not pilha or pilha.pop() != pares[caractere]:
                return False

    return not pilha
```

Invariante: a pilha contém exatamente as aberturas ainda não fechadas do prefixo
já lido. Tempo O(n), espaço O(n) no pior caso.

### Fila — FIFO

O primeiro a entrar é o primeiro a sair. Usos: processamento por chegada e BFS.
Em Python, remover o índice zero de `list` é O(n); use `deque.popleft()`.

### Deque

Permite inserir e remover nas duas pontas em O(1) amortizado na implementação
usual. É útil em janelas deslizantes e pode implementar pilha ou fila.

### Fila de prioridade/heap

Retira o menor ou maior elemento segundo prioridade, não segundo chegada. Em
heap binário:

- consultar o topo: O(1);
- inserir: O(log n);
- retirar topo: O(log n);
- construir heap em lote: O(n) em implementações usuais.

Use em escalonamento, menor caminho e seleção dos `k` menores. Um heap não deixa
todos os elementos ordenados; garante apenas a relação necessária com o topo.

## 8. Árvores

Uma árvore representa hierarquia. Conceitos:

- raiz, pai, filho, folha;
- profundidade de um nó e altura da árvore;
- subárvore;
- percurso em pré-ordem, em ordem e pós-ordem.

Em árvore binária de busca (BST), chaves menores ficam de um lado e maiores do
outro conforme a convenção. Busca é O(h), onde `h` é a altura. Se a árvore
degenera em cadeia, `h=n`; árvores balanceadas mantêm `h=O(log n)`.

Não confunda:

- árvore binária: no máximo dois filhos;
- BST: mantém ordem de busca;
- heap: mantém prioridade parcial;
- trie: organiza por prefixos;
- árvore balanceada: controla altura.

Arquivos, DOM e ASTs são árvores mesmo quando não são BSTs.

Percurso iterativo simples:

```python
from dataclasses import dataclass


@dataclass
class No:
    valor: int
    esquerda: "No | None" = None
    direita: "No | None" = None


def pre_ordem(raiz: No | None) -> list[int]:
    if raiz is None:
        return []

    resultado: list[int] = []
    pilha = [raiz]
    while pilha:
        atual = pilha.pop()
        resultado.append(atual.valor)
        if atual.direita is not None:
            pilha.append(atual.direita)
        if atual.esquerda is not None:
            pilha.append(atual.esquerda)
    return resultado
```

Direita entra primeiro porque a pilha retira o último, permitindo visitar a
esquerda primeiro.

## 9. Grafos: representação e percurso

Um grafo possui vértices e arestas. Pode ser dirigido ou não, ponderado ou não,
conectado ou desconectado, cíclico ou acíclico.

Representações principais:

- **lista de adjacência:** espaço O(V+E), boa para grafos esparsos;
- **matriz de adjacência:** espaço O(V²), consulta de aresta O(1), útil em grafos
  densos ou pequenos;
- **lista de arestas:** simples para algoritmos que percorrem todas as arestas.

### BFS — busca em largura

BFS usa fila e encontra a menor quantidade de arestas a partir da origem em
grafo não ponderado.

```python
from collections import deque


def menores_distancias(
    grafo: dict[str, list[str]], origem: str
) -> dict[str, int]:
    distancias = {origem: 0}
    fila = deque([origem])

    while fila:
        atual = fila.popleft()
        for vizinho in grafo.get(atual, []):
            if vizinho not in distancias:
                distancias[vizinho] = distancias[atual] + 1
                fila.append(vizinho)

    return distancias
```

Marcar ao inserir na fila evita enfileirar o mesmo vértice repetidamente.
Complexidade O(V+E) com lista de adjacência.

### DFS — busca em profundidade

DFS usa recursão ou pilha. É útil para componentes, detecção de ciclos,
backtracking e ordenação topológica.

```python
def dfs(grafo: dict[str, list[str]], origem: str) -> list[str]:
    ordem: list[str] = []
    visitados: set[str] = set()
    pilha = [origem]

    while pilha:
        atual = pilha.pop()
        if atual in visitados:
            continue
        visitados.add(atual)
        ordem.append(atual)
        pilha.extend(reversed(grafo.get(atual, [])))
    return ordem
```

Em grafos, “visitado” é necessário para terminar quando há ciclo.

### Qual algoritmo de caminho?

- grafo não ponderado: BFS;
- pesos não negativos: Dijkstra com fila de prioridade;
- pesos negativos: algoritmo apropriado como Bellman–Ford;
- DAG: ordem topológica permite soluções específicas.

Dijkstra não é correto com arestas negativas. Escolher algoritmo exige conhecer
as propriedades da entrada.

## 10. Busca linear e binária

Busca linear funciona em qualquer sequência e custa O(n). Busca binária exige
ordenação compatível com a comparação e custa O(log n).

```python
def busca_binaria(valores: list[int], alvo: int) -> int:
    esquerda = 0
    direita = len(valores)  # intervalo semiaberto [esquerda, direita)

    while esquerda < direita:
        meio = esquerda + (direita - esquerda) // 2
        if valores[meio] < alvo:
            esquerda = meio + 1
        else:
            direita = meio

    if esquerda < len(valores) and valores[esquerda] == alvo:
        return esquerda
    return -1
```

Essa versão encontra a primeira ocorrência. Invariante: toda posição que ainda
pode ser a primeira ocorrência está em `[esquerda, direita)`. O intervalo reduz
em toda iteração, portanto termina.

Erros comuns:

- executar em dados não ordenados;
- misturar intervalo fechado e semiaberto;
- não reduzir o intervalo quando `meio` coincide com uma ponta;
- não definir qual ocorrência retornar quando há duplicatas;
- ordenar por uma chave e buscar por outra.

Ordenar primeiro custa O(n log n). Para uma única busca, isso pode ser pior que
O(n); para muitas buscas em dados estáveis, pode compensar.

## 11. Ordenação: propriedades além do Big O

Pergunte:

- precisa ser estável (preservar ordem relativa de chaves iguais)?
- pode modificar a entrada?
- cabe em memória?
- dados já estão quase ordenados?
- chave é barata de calcular?
- biblioteca oferece garantia adequada?

| Algoritmo | Tempo típico/pior | Espaço extra | Estável? |
|-----------|-------------------|--------------|----------|
| insertion sort | O(n²), bom quase ordenado | O(1) | sim |
| merge sort | O(n log n) | O(n) comum | sim |
| heap sort | O(n log n) | O(1) comum | não |
| quicksort | médio O(n log n), pior O(n²) | depende | não em geral |
| algoritmos da biblioteca | implementação específica | específica | consulte docs |

Merge sort mostra divisão e conquista:

```python
def merge_sort(valores: list[int]) -> list[int]:
    if len(valores) <= 1:
        return valores.copy()

    meio = len(valores) // 2
    esquerda = merge_sort(valores[:meio])
    direita = merge_sort(valores[meio:])
    return intercalar(esquerda, direita)


def intercalar(a: list[int], b: list[int]) -> list[int]:
    resultado: list[int] = []
    i = j = 0

    while i < len(a) and j < len(b):
        if a[i] <= b[j]:
            resultado.append(a[i])
            i += 1
        else:
            resultado.append(b[j])
            j += 1

    resultado.extend(a[i:])
    resultado.extend(b[j:])
    return resultado
```

`intercalar` é linear porque cada elemento avança uma vez. A recursão tem
`log n` níveis com trabalho O(n) por nível: O(n log n). As fatias também alocam;
uma implementação otimizada pode trabalhar com índices e buffer auxiliar.

Em produção, prefira a ordenação da biblioteca: é testada, otimizada e pode
explorar características dos dados. Implemente algoritmos clássicos aqui para
compreender propriedades, não para substituir a biblioteca por hábito.

## 12. Recursão e sua relação com a pilha

Uma função recursiva precisa de:

1. caso base;
2. passo que reduz o problema;
3. hipótese de que a chamada menor está correta;
4. combinação que produz a resposta maior.

```python
def mdc(a: int, b: int) -> int:
    a, b = abs(a), abs(b)
    if b == 0:
        return a
    return mdc(b, a % b)
```

O segundo argumento diminui até zero no algoritmo de Euclides. Cada chamada
consome quadro de pilha. Python não elimina recursão de cauda e possui limite;
para percursos muito profundos, use pilha explícita.

Recursão ingênua pode repetir subproblemas:

```python
def fib_lento(n: int) -> int:
    if n <= 1:
        return n
    return fib_lento(n - 1) + fib_lento(n - 2)
```

O custo cresce exponencialmente. Memoização ou iteração o reduz a O(n), mas
primeiro valide o domínio (`n >= 0`) e o real objetivo da função.

## 13. Padrões de resolução

Padrão é uma hipótese de estrutura, não palavra mágica.

### Dois ponteiros

Útil quando dois índices percorrem uma sequência com relação monotônica.
Em vetor ordenado, encontre par que soma alvo:

```python
def par_com_soma(valores: list[int], alvo: int) -> tuple[int, int] | None:
    esquerda, direita = 0, len(valores) - 1
    while esquerda < direita:
        soma = valores[esquerda] + valores[direita]
        if soma == alvo:
            return valores[esquerda], valores[direita]
        if soma < alvo:
            esquerda += 1
        else:
            direita -= 1
    return None
```

Correção depende da ordenação: se a soma é pequena, nenhum par com o menor valor
e uma ponta ainda mais à esquerda existe; avançá-lo não perde solução.

### Janela deslizante

Evita recalcular intervalos contíguos:

```python
def maior_soma_janela(valores: list[int], k: int) -> int:
    if not 1 <= k <= len(valores):
        raise ValueError("k deve estar entre 1 e o tamanho da lista")

    soma = sum(valores[:k])
    melhor = soma
    for direita in range(k, len(valores)):
        soma += valores[direita] - valores[direita - k]
        melhor = max(melhor, soma)
    return melhor
```

Tempo O(n), em vez de O(nk) ao somar cada janela do zero.

### Prefixos

Pré-calcule somas para responder várias consultas de intervalo:

```python
def prefixos(valores: list[int]) -> list[int]:
    p = [0]
    for valor in valores:
        p.append(p[-1] + valor)
    return p


def soma_intervalo(p: list[int], inicio: int, fim: int) -> int:
    """Soma no intervalo semiaberto [inicio, fim)."""
    return p[fim] - p[inicio]
```

Construção O(n); cada consulta O(1). O contrato semiaberto reduz casos especiais.

### Dividir e conquistar

Divide em subproblemas independentes, resolve e combina. Merge sort é exemplo.
A análise costuma usar recorrência como `T(n)=2T(n/2)+O(n)`.

### Guloso

Escolhe a melhor opção local e não volta atrás. Só é correto quando existe uma
propriedade que garante ótimo global. “Parece melhor agora” não é prova. Troco
com certas moedas funciona; com conjunto arbitrário pode falhar.

### Programação dinâmica

Aplica-se quando subproblemas se repetem e a solução ótima possui subestrutura
apropriada. Processo:

1. defina estado com significado;
2. escreva transição;
3. determine casos base;
4. escolha memoização (top-down) ou tabela (bottom-up);
5. defina ordem de preenchimento;
6. reconstrua solução se necessário.

Para número de maneiras de subir `n` degraus com passos 1 ou 2:

```python
def maneiras(n: int) -> int:
    if n < 0:
        raise ValueError("n deve ser não negativo")
    anterior, atual = 1, 1
    for _ in range(n):
        anterior, atual = atual, anterior + atual
    return anterior
```

O estado completo usa apenas os dois valores anteriores: tempo O(n), espaço
extra O(1).

### Backtracking

Constrói candidato, verifica restrições e desfaz. É adequado para busca
combinatória, mas pode ser exponencial. Podas corretas eliminam ramos que não
podem gerar solução; não devem eliminar uma solução válida.

## 14. Correção: invariantes, indução e contraexemplos

Testes encontram casos; argumento de correção cobre classes de casos.

Para um laço, demonstre:

1. **inicialização:** invariante vale antes da primeira iteração;
2. **manutenção:** se vale antes, continua valendo depois;
3. **término:** quando o laço encerra, invariante + condição de término implicam
   a pós-condição.

Na busca binária, a região possível contém a resposta na inicialização; cada
comparação descarta apenas região impossível; quando esvazia, não há resposta.

Busque contraexemplos pequenos:

- vazio;
- um elemento;
- dois elementos invertidos;
- todos iguais;
- alvo ausente abaixo/acima dos limites;
- negativos e zero;
- grafo desconectado, autoaresta e ciclo;
- tamanho máximo esperado.

Uma implementação que passa no exemplo feliz ainda não demonstrou correção.

## 15. Testes para algoritmos

Combine:

- exemplos fixos legíveis;
- fronteiras;
- propriedades;
- comparação com solução simples para entradas pequenas;
- medições separadas de testes funcionais.

Exemplo de propriedade de ordenação:

```python
def esta_ordenado(valores: list[int]) -> bool:
    return all(a <= b for a, b in zip(valores, valores[1:]))


entrada = [3, 1, 2, 1]
saida = merge_sort(entrada)
assert esta_ordenado(saida)
assert len(saida) == len(entrada)
assert sorted(saida) == sorted(entrada)  # mesma multiplicidade
assert entrada == [3, 1, 2, 1]          # contrato não modifica entrada
```

Para validar uma solução otimizada de janela, gere listas pequenas sintéticas e
compare com uma implementação O(nk) simples. A referência lenta pode ser ótima
como oráculo de teste.

## 16. Medição responsável

Um benchmark minimamente útil:

1. gera entradas fora da região medida ou documenta esse custo;
2. usa relógio monotônico de alta resolução;
3. aquece runtimes JIT quando relevante;
4. repete e apresenta distribuição, não apenas melhor execução;
5. verifica resultado para impedir trabalho eliminado ou algoritmo incorreto;
6. registra hardware, runtime, versão e tamanho;
7. mede memória quando ela faz parte do requisito.

Exemplo didático em Python:

```python
from time import perf_counter


def medir(funcao, *args, repeticoes: int = 5) -> list[float]:
    tempos = []
    for _ in range(repeticoes):
        inicio = perf_counter()
        resultado = funcao(*args)
        fim = perf_counter()
        assert resultado is not None
        tempos.append(fim - inicio)
    return tempos
```

Não misture geração aleatória, impressão e algoritmo na mesma medição. Para
entradas minúsculas, ruído domina. Para entradas enormes, monitore memória e não
comprometa a máquina.

## 17. Escolha orientada por operação

| Necessidade dominante | Candidato inicial | Atenção |
|-----------------------|------------------|---------|
| percorrer em ordem e acessar índice | vetor/lista dinâmica | inserção no meio O(n) |
| pertencimento/unicidade | conjunto hash | memória e hash/igualdade |
| associar chave a valor | mapa hash | não pressuponha ordenação |
| menor chave e consultas ordenadas | árvore ordenada | implementação da biblioteca |
| último item inserido | pilha | limite de memória |
| ordem de chegada | fila/deque | não remova início de vetor inadequado |
| próximo por prioridade | heap | restante não está ordenado |
| hierarquia | árvore | profundidade e ciclos acidentais |
| relações gerais | grafo | representação esparsa/densa |
| sequência de bytes compacta | array/buffer | limites e codificação |

Comece pela operação dominante, depois avalie atualização, memória, ordem,
concorrência e simplicidade. A estrutura mais sofisticada raramente é a melhor
sem um requisito que a justifique.

## 18. Estudo de caso: planejador de disciplinas

### Problema

Cada disciplina possui zero ou mais pré-requisitos. Precisamos:

- validar se todos os pré-requisitos existem;
- rejeitar ciclos;
- produzir uma ordem possível de estudo;
- explicar por que não existe ordem quando há ciclo.

Isso é um grafo dirigido. Uma aresta `A → B` significa “A deve vir antes de B”.
A ordenação topológica por algoritmo de Kahn usa grau de entrada:

```python
from collections import deque


def ordem_de_estudo(
    prerequisitos: dict[str, list[str]],
) -> list[str]:
    disciplinas = set(prerequisitos)
    for requisitos in prerequisitos.values():
        desconhecidos = set(requisitos) - disciplinas
        if desconhecidos:
            raise ValueError(
                f"pré-requisitos desconhecidos: {sorted(desconhecidos)}"
            )

    dependentes = {nome: [] for nome in disciplinas}
    grau = {nome: 0 for nome in disciplinas}

    for disciplina, requisitos in prerequisitos.items():
        grau[disciplina] = len(requisitos)
        for requisito in requisitos:
            dependentes[requisito].append(disciplina)

    fila = deque(sorted(nome for nome, g in grau.items() if g == 0))
    ordem: list[str] = []

    while fila:
        atual = fila.popleft()
        ordem.append(atual)
        for dependente in sorted(dependentes[atual]):
            grau[dependente] -= 1
            if grau[dependente] == 0:
                fila.append(dependente)

    if len(ordem) != len(disciplinas):
        raise ValueError("dependências contêm ciclo")
    return ordem
```

### Por que funciona

Um vértice de grau zero não depende de disciplina ainda pendente. Ao removê-lo,
reduzimos o grau de seus dependentes. Se processamos todos, a ordem respeita
cada aresta. Se restam vértices mas nenhum tem grau zero, eles participam de ou
dependem de um ciclo.

Complexidade é O(V+E), desconsiderando a ordenação extra dos nomes para saída
determinística. Ordenar vizinhos acrescenta custos relacionados aos graus; essa
decisão existe para testes e relatórios reproduzíveis, não para a lógica básica.

### Casos de teste essenciais

1. nenhuma disciplina;
2. uma disciplina sem requisito;
3. cadeia `A → B → C`;
4. duas disciplinas independentes;
5. pré-requisito desconhecido;
6. auto-ciclo `A → A`;
7. ciclo `A → B → C → A`;
8. múltiplas ordens válidas — verifique arestas, não uma ordem arbitrária.

## 19. Erros comuns e antídotos

- **Otimizar antes de definir contrato:** escreva casos e restrições primeiro.
- **Afirmar O(1) para hash sem qualificar:** diga médio/esperado e conheça a
  implementação.
- **Ignorar espaço:** mapa pode acelerar e ainda exceder limite de memória.
- **Usar lista como fila ineficiente:** confirme custo de remover no início.
- **Esquecer visitados em grafo:** ciclos causam repetição ou não término.
- **Usar BFS em grafo ponderado:** menor número de arestas não é menor custo.
- **Busca binária sem ordenação:** o descarte de metade deixa de ser válido.
- **Recursão sem progresso:** caso base nunca é alcançado.
- **Programação dinâmica sem estado claro:** tabela cresce, mas não representa
  subproblema verificável.
- **Benchmark de uma execução:** aquecimento e ruído dominam.
- **Teste acoplado a uma ordem válida específica:** grafos podem admitir várias.
- **Modificar entrada sem contrato:** chamador observa efeito inesperado.

## 20. Exercícios graduais

Para cada exercício, registre: contrato, exemplos, estrutura escolhida,
invariante, complexidade de tempo/espaço e teste que quebra a solução ingênua.

### Nível 1 — estruturas básicas

1. Conte palavras com mapa e produza lista ordenada por frequência e depois nome.
2. Remova duplicatas preservando a primeira ocorrência.
3. Valide `()[]{}` com pilha e informe a posição do primeiro erro.
4. Implemente fila com deque e simule atendimento por chegada.
5. Compare busca linear em dados não ordenados com busca binária após ordenação.

### Nível 2 — algoritmos clássicos

1. Implemente primeira ocorrência e ponto de inserção com busca binária.
2. Implemente merge sort estável sem modificar a entrada.
3. Calcule componentes conectados de um grafo não dirigido.
4. Detecte ciclo em dependências dirigidas.
5. Encontre os `k` menores valores usando heap e compare com ordenar tudo.
6. Resolva maior soma de janela fixa em O(n).
7. Responda mil consultas de soma de intervalo usando prefixos.

### Ponte guiada para o nível 3

Os três primeiros problemas do próximo nível combinam várias estruturas. Não
comece diretamente pela versão otimizada. Use as etapas abaixo e preserve os
testes da versão simples como oráculo para a versão final.

#### Cache LRU: primeiro correto, depois O(1)

**Contrato mínimo:** `get(chave)` devolve o valor ou ausência; `put(chave,
valor)` insere ou atualiza; a capacidade é positiva; ao excedê-la, sai a chave
usada há mais tempo. Toda leitura bem-sucedida torna a chave a mais recente.

Comece com um mapa para valores e uma lista de chaves ordenada da menos para a
mais recente. Remover uma chave do meio custa O(n), mas deixa a política visível:

```text
capacidade = 2
put(A, 1)       ordem [A]
put(B, 2)       ordem [A, B]
get(A) -> 1     ordem [B, A]
put(C, 3)       remove B; ordem [A, C]
get(B) -> ausência
```

Somente depois de essa versão passar nos testes, substitua a lista por uma lista
duplamente ligada e faça o mapa apontar para os nós. Use sentinelas de início e
fim para que inserir e remover não precisem de casos especiais:

```text
get(chave):
    nó = mapa[chave]
    se não existe, retornar ausência
    desligar nó da posição atual
    ligar nó imediatamente antes da sentinela final
    retornar nó.valor

put(chave, valor):
    se chave existe, atualizar e mover seu nó para o fim
    senão, criar nó, registrar no mapa e ligar no fim
    se tamanho > capacidade, desligar o primeiro nó real e removê-lo do mapa
```

Invariantes: cada chave do mapa possui exatamente um nó; os vizinhos apontam de
volta um para o outro; a quantidade de nós reais é igual ao tamanho do mapa e
nunca supera a capacidade. Teste capacidade 1, atualização de chave existente,
leitura que muda a ordem, evicções consecutivas e consulta ausente.

#### Dijkstra: tabela de distâncias antes do heap

Use este grafo dirigido fictício: `A -> B (4)`, `A -> C (1)`, `C -> B (2)`,
`B -> D (1)` e `C -> D (5)`. Partindo de `A`, as distâncias esperadas são
`A=0`, `C=1`, `B=3`, `D=4`.

Represente adjacências como `vertice -> [(vizinho, peso)]`. Antes de programar,
preencha à mão uma tabela com `vértice`, `melhor distância`, `anterior` e
`finalizado`. Depois implemente a versão com fila de prioridade:

```text
validar que nenhum peso é negativo
distância[início] = 0; demais = infinito
heap = [(0, início)]

enquanto heap não vazio:
    (custo, atual) = remover menor
    se custo != distância[atual], ignorar entrada antiga
    para cada (vizinho, peso) de atual:
        candidato = custo + peso
        se candidato < distância[vizinho]:
            atualizar distância e anterior
            inserir (candidato, vizinho) no heap
```

A checagem da entrada antiga é importante porque heaps comuns não diminuem uma
prioridade no lugar: uma melhora insere outro par. Aceite somente pesos finitos
e não negativos. Teste o grafo acima, vértice isolado (distância infinita),
origem igual ao destino, caminhos de mesmo custo e rejeição de peso negativo.
Dijkstra não deve ser adaptado silenciosamente para aresta negativa.

#### Mochila 0/1: da enumeração para a recorrência

O contrato 0/1 permite escolher cada item no máximo uma vez. Para capacidade
`5` e itens `(peso=2, valor=3)`, `(3, 4)` e `(4, 5)`, o valor ótimo é `7` ao
escolher os dois primeiros.

Primeiro enumere, para no máximo 20 itens, todas as escolhas incluir ou não
incluir. Essa versão exponencial é pequena e fácil de conferir. Depois defina:

```text
dp[i][c] = maior valor usando apenas os primeiros i itens e capacidade c

dp[0][c] = 0
se peso[i] > c:
    dp[i][c] = dp[i-1][c]
senão:
    dp[i][c] = max(
        dp[i-1][c],
        valor[i] + dp[i-1][c-peso[i]]
    )
```

Construa a tabela para o exemplo antes de reduzir a memória para uma linha. Na
versão de uma linha, percorra capacidades em ordem **decrescente**; ordem
crescente permitiria reutilizar o mesmo item e resolveria outro problema,
mochila ilimitada. Compare as duas implementações em muitos casos pequenos
determinísticos. Teste capacidade zero, lista vazia, item pesado demais, solução
combinada, empate e entradas com peso não positivo.

### Nível 3 — projeto e prova

1. Implemente cache LRU combinando mapa e lista duplamente ligada; justifique
   O(1) esperado para consultar e atualizar.
2. Implemente Dijkstra para um mapa fictício com pesos não negativos e rejeite
   peso negativo na entrada.
3. Resolva uma mochila pequena primeiro por força bruta e depois por programação
   dinâmica; compare estados, tempo e memória.
4. Implemente o planejador de disciplinas em uma segunda linguagem.
5. Crie gerador de casos pequenos e compare algoritmo otimizado com referência
   simples em centenas de entradas determinísticas.

### Nível 4 — análise aplicada

1. Escolha uma coleção de um projeto seu, liste operações e frequências e avalie
   se a estrutura atual é apropriada.
2. Construa benchmark reproduzível para duas soluções, separando preparação da
   medição e registrando mediana.
3. Encontre uma troca tempo–memória real e escreva um pequeno registro de decisão.
4. Estime o limite prático para O(n²) no seu ambiente e explique por que ele não
   é uma constante universal.

## Critério de conclusão do capítulo

- [ ] Distingo TAD, implementação e API da biblioteca.
- [ ] Derivo custos de laços, estruturas auxiliares e saídas materializadas.
- [ ] Qualifico pior caso, caso esperado e amortizado corretamente.
- [ ] Justifico a estrutura por operações e restrições, não por preferência.
- [ ] Implemento busca binária sem misturar convenções de intervalo.
- [ ] Explico BFS, DFS e quando cada uma não resolve menor caminho.
- [ ] Escrevo um invariante e argumento inicialização, manutenção e término.
- [ ] Testo vazio, limites, duplicatas, ciclos e entradas inválidas.
- [ ] Comparo uma solução otimizada com uma referência simples.
- [ ] Meço desempenho sem misturar geração, I/O e algoritmo.
- [ ] Consigo explicar tempo, espaço e limitações do planejador de disciplinas.

## Conexão com os próximos capítulos

Em [Engenharia de software e testes](05-engenharia-software.md), esses contratos e
casos de fronteira tornam-se testes automatizados e decisões arquiteturais. Em
[Web, HTTP, APIs e bancos](06-web-http-bancos.md), mapas, filas, índices e grafos
aparecem em cache, roteamento, paginação e consultas. Em
[Sistemas, memória e concorrência](07-sistemas-concorrencia.md), custo deixa de
ser apenas abstrato: representação, alocação, cache e sincronização passam a
afetar diretamente o comportamento do programa.
