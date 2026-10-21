# 05 — Busca e ordenação: contratos, estabilidade e limites

Busca e ordenação mostram como uma pré-condição sustenta todo um algoritmo.
Busca binária é logarítmica porque a sequência está ordenada e o comparador é
coerente; mergesort é estável apenas se o merge desempata corretamente; o limite
`Ω(n log n)` vale para ordenação geral baseada em comparações, não para chaves
inteiras em intervalo limitado.

Em produção, use algoritmos da biblioteca salvo requisito excepcional. Eles lidam
com casos extremos, otimizam constantes e evoluem com o runtime. Implemente-os
aqui para compreender as garantias que você passa a exigir da biblioteca.

## Objetivos verificáveis

Ao concluir, você deverá conseguir:

1. especificar busca em termos de entrada, comparador, duplicatas e resultado ausente;
2. implementar busca binária e variantes `lower_bound`/`upper_bound` por invariantes;
3. explicar e provar invariantes de seleção, inserção, merge e particionamento;
4. comparar mergesort, quicksort, heapsort e algoritmos híbridos;
5. definir estabilidade, ordenação in-place e adaptabilidade sem ambiguidade;
6. demonstrar o limite inferior de comparações por uma árvore de decisão;
7. declarar as condições em que counting/radix sort podem ser lineares;
8. considerar cache, alocação, dados externos e ordenação paralela;
9. aplicar busca e desempate determinístico ao Dependency Planner.

## Pré-requisitos e mapa mental

Revise invariantes e complexidade nos capítulos [00](00-como-pensar-problemas.md)
e [01](01-complexidade.md).

```text
consulta
  dados sem ordem -> busca linear, hash ou índice
  dados ordenados + acesso ao meio -> busca binária

ordenar
  comparador geral -> algoritmo de comparação
  chave com estrutura limitada -> counting/radix/bucket
  dados maiores que RAM -> runs + merge externo

sempre declarar
  duplicatas, estabilidade, mutação, memória, comparador e distribuição
```

## O contrato de uma busca

“Encontre `x`” não define:

- se a coleção está ordenada;
- se o acesso por índice é barato;
- se existem duplicatas e qual ocorrência devolver;
- se comparação é igualdade, ordem total ou chave derivada;
- como representar ausência sem colidir com um índice válido;
- se a estrutura pode mudar durante a busca.

Busca linear funciona em qualquer sequência finita: melhor caso `Θ(1)`, pior
`Θ(n)`, espaço auxiliar `Θ(1)`. Pode retornar a primeira ocorrência e
funciona em iteradores sem acesso aleatório. Um mapa/conjunto oferece consultas
exatas esperadas `O(1)`, pagando construção e memória; árvore ordenada responde
também intervalos em `O(log n + k)`.

Ordenar antes de uma única busca costuma custar mais que varrer. Para `q` buscas,
compare aproximadamente:

```text
linear repetida:             O(qn)
ordenar + busca binária:     O(n log n + q log n)
construir hash + consultar:   O(n + q) esperado, com O(n) espaço
```

Atualizações, necessidade de ordem, memória e custo do hash/comparador podem
mudar a decisão.

## Busca binária por invariante

A versão abaixo busca uma ocorrência em um intervalo semiaberto `[lo, hi)`. A
sequência deve estar ordenada em ordem crescente pelo mesmo critério.

```python
from collections.abc import Sequence

def binary_search(values: Sequence[int], target: int) -> int | None:
    lo, hi = 0, len(values)
    while lo < hi:
        mid = lo + (hi - lo) // 2
        value = values[mid]
        if value == target:
            return mid
        if value < target:
            lo = mid + 1
        else:
            hi = mid
    return None
```

Invariante: se o alvo existe entre os candidatos ainda possíveis, seu índice
pertence a `[lo,hi)`. A variante diminui: `hi-lo` fica estritamente menor a cada
passo, garantindo terminação. O intervalo vazio ocorre quando `lo==hi`.

Em linguagens com inteiros fixos, `lo + (hi-lo)/2` evita overflow que `(lo+hi)/2`
pode causar. Em Python isso não é necessário para overflow, mas preserva um padrão
portável. Em lista ligada, localizar repetidamente o meio custa linear, eliminando
o benefício; a estrutura deve oferecer acesso aleatório eficiente.

### `lower_bound`: a variante mais reutilizável

Em vez de parar ao encontrar igualdade, procure a primeira posição cujo valor
é maior ou igual ao alvo:

```python
def lower_bound(values: Sequence[int], target: int) -> int:
    lo, hi = 0, len(values)
    while lo < hi:
        mid = lo + (hi - lo) // 2
        if values[mid] < target:
            lo = mid + 1
        else:
            hi = mid
    return lo
```

Contrato: retorna `i` em `[0,n]`; todo elemento antes de `i` é menor que `target`
e todo elemento a partir de `i` é maior ou igual. Se `i<n` e `values[i]==target`,
`i` é a primeira ocorrência. `upper_bound` busca a primeira posição estritamente
maior; o intervalo de duplicatas é `[lower_bound, upper_bound)`.

Essa formulação resolve busca, ponto de inserção, contagem de iguais e consultas
por faixa. Teste vazio, um item, alvo menor/maior que todos, todas as chaves iguais
e limites da representação.

## O que significa ordenar corretamente

Dado comparador `<=`, uma saída correta deve satisfazer:

1. **ordem:** `out[i] <= out[i+1]` para todo par adjacente;
2. **permutacão:** possui exatamente os mesmos elementos e multiplicidades da entrada;
3. **estabilidade**, se prometida: itens de chave igual mantêm ordem relativa;
4. **efeito declarado:** altera a entrada ou devolve nova coleção;
5. **tratamento de erro:** comparador inválido, valor não comparável e memória.

Verificar somente que a saída está crescente não detecta algoritmo que perdeu
ou duplicou itens. Compare contagens ou use uma identificação única no teste.

## Comparadores e chaves

Uma ordem total deve ser consistente. Em termos práticos:

- `compare(a,a)` representa igualdade;
- inverter argumentos inverte o sinal;
- se `a<b` e `b<c`, então `a<c`;
- a relação não muda durante a ordenação;
- se o container exige consistência com igualdade, itens comparados como iguais
  seguem esse contrato.

Evite `return a - b` em linguagens onde a subtração pode transbordar. Valores
`NaN` quebram intuições (`NaN` não é igual nem menor/maior); strings dependem de
bytes, Unicode, locale e normalização. Prefira uma função de chave quando a
biblioteca oferece:

```python
tasks.sort(key=lambda task: (task.priority, task.id))
```

Calcular a chave uma vez por item evita recomputá-la a cada comparação. O tuple
declara desempate. Se a ordenação é estável, ordenar primeiro pela chave secundária
e depois pela primária também funciona; a última ordenação domina sem destruir
a ordem relativa dos empates.

## Algoritmos elementares e suas invariantes

### Selection sort

Na iteração `i`, encontre o menor elemento de `[i,n)` e troque com `i`.
Invariante: `[0,i)` contém os `i` menores itens em ordem final. Faz
`Θ(n²)` comparações em todos os casos e `O(n)` trocas; não é estável na
forma comum. Pode ser relevante quando escrever é muito mais caro que comparar,
mas raramente é escolha geral.

### Insertion sort

Insira `values[i]` na posição correta do prefixo. Invariante: `[0,i)` está
ordenado e é permutação dos `i` primeiros itens originais. É estável se itens
iguais não forem ultrapassados, in-place e adaptativo: `Θ(n)` em entrada já
ordenada, `Θ(n²)` no pior caso. Tem excelente desempenho para segmentos
pequenos e quase ordenados, por isso aparece dentro de algoritmos híbridos.

```text
para i de 1 até n-1:
    key = A[i]
    j = i
    enquanto j > 0 e key < A[j-1]:
        A[j] = A[j-1]
        j -= 1
    A[j] = key
```

Usar `<`, e não `<=`, preserva estabilidade entre chaves iguais.

### Bubble sort

Trocas adjacentes levam o maior restante ao fim. Com indicador de nenhuma troca,
o melhor caso é `Θ(n)`; pior `Θ(n²)`. É estável na forma que troca apenas
desordens estritas, mas geralmente perde para insertion sort em utilidade real.

## Mergesort: dividir e intercalar

Mergesort divide em metades, ordena cada uma e intercala:

```text
mergesort(A):
    se |A| <= 1: retorne A
    L = mergesort(primeira metade)
    R = mergesort(segunda metade)
    retorne merge(L, R)
```

Invariante do merge: a saída é ordenada e contém exatamente os itens já
consumidos de `L` e `R`; o menor item ainda não emitido está em uma das duas
cabeças. Em empate, escolher primeiro da metade esquerda preserva estabilidade.

Recorrência `T(n)=2T(n/2)+Θ(n)` produz `Θ(n log n)` em melhor, médio e
pior caso. A versão comum sobre arrays usa `Θ(n)` de espaço auxiliar, mais
`O(log n)` de pilha. Em listas ligadas, o merge pode relinkar nós. Acesso
sequencial o torna base natural de ordenação externa.

## Quicksort: particionar ao redor do pivô

Particionamento reorganiza a faixa de modo que itens menores fiquem de um lado e
maiores do outro, colocando o pivô ou delimitando regiões. Depois, subfaixas são
ordenadas recursivamente.

Com divisões equilibradas, `Θ(n log n)`; se o pivô é sempre extremo,
`T(n)=T(n-1)+Θ(n)=Θ(n²)` e a pilha pode crescer `Θ(n)`. Randomização,
mediana de amostra e particionamento em três vias reduzem casos ruins práticos,
especialmente com muitas duplicatas, mas não transformam toda versão em garantia
de pior caso `n log n`.

Quicksort costuma ter boa localidade, poucas alocações e ser rápido em arrays.
A forma in-place comum não é estável. Invariantes dependem do esquema (Lomuto,
Hoare ou três vias); misturar condições e índices de esquemas diferentes é fonte
clássica de loops infinitos e perda de elementos.

## Heapsort e algoritmos híbridos

Heapsort constrói max-heap em `O(n)` e move repetidamente o máximo para o fim,
restaurando o heap em `O(log n)`. Garante `Θ(n log n)`, usa `O(1)` auxiliar na
forma de array e não é estável. Seu padrão de acesso costuma aproveitar cache
menos que quicksort.

Bibliotecas combinam ideias:

- **introsort:** inicia quicksort e troca por heapsort quando a recursão indica
  pior caso; insertion sort em faixas pequenas;
- **Timsort:** detecta runs já ordenadas e faz merges estáveis; excelente para
  dados parcialmente ordenados;
- **dual-pivot/híbridos especializados:** escolhas dependem do tipo e runtime.

Não suponha algoritmo ou estabilidade apenas pelo nome `sort`; consulte o
contrato da versão usada quando isso for requisito.

## Limite inferior por comparações

Para `n` elementos distintos existem `n!` permutações possíveis. Um algoritmo
baseado apenas em comparações pode ser representado por árvore binária de decisão:
cada comparação escolhe um ramo e cada folha precisa identificar uma permutação.

Uma árvore binária de altura `h` tem no máximo `2^h` folhas. Logo:

```text
2^h >= n!
h >= log2(n!)
log2(n!) = Ω(n log n)
```

Portanto qualquer ordenação geral somente por comparação exige
`Ω(n log n)` comparações no pior caso. Mergesort e heapsort atingem esse
limite assintótico. A prova não diz que toda implementação precisa desse tempo em
entradas já ordenadas, nem se aplica quando exploramos dígitos ou um universo
restrito de chaves.

## Ordenações não comparativas

### Counting sort

Para chaves inteiras em intervalo de tamanho `K`, conte frequências e reconstrua
a saída. Tempo `Θ(n+K)`, espaço `Θ(K)` ou `Θ(n+K)` para versão estável.
Se IDs variam de `0` a um bilhão e existem mil itens, `K` torna a solução inviável.

### Radix sort

Ordena por dígitos usando uma ordenação estável em cada passagem (na versão LSD).
Com `d` dígitos e base `b`, custo típico `Θ(d(n+b))`. Chaves negativas,
comprimentos variáveis, encoding e ordem lexicográfica precisam de tratamento
explícito. Chamar de linear pressupõe `d`/tamanho de palavra limitado.

### Bucket sort

Distribui valores em baldes e ordena cada um. Pode ter tempo esperado linear sob
distribuição adequada, mas entradas concentradas colocam quase tudo no mesmo
balde e recuperam o custo do algoritmo interno. A hipótese probabilística é parte
da garantia.

## Seleção: quando não é preciso ordenar tudo

Para os `k` menores ou maiores:

- ordenar tudo: `O(n log n)`;
- manter heap de tamanho `k`: `O(n log k)`, espaço `O(k)`;
- quickselect: `O(n)` esperado, `O(n²)` no pior caso comum;
- seleção determinística por mediana de medianas: `O(n)` pior caso, constantes
  maiores.

Em fluxo que não cabe em memória, heap de tamanho `k` é especialmente útil.
Defina empates e se a saída final precisa vir ordenada; o heap só seleciona.

## Memória, cache e ordenação externa

Mesmo com igual `Θ(n log n)`, implementações diferem:

- quicksort percorre segmentos contíguos e tende a boa localidade;
- mergesort faz acessos sequenciais, mas precisa de buffer em arrays;
- heapsort salta entre pai/filhos e pode gerar mais faltas de cache;
- ordenar ponteiros move poucos bytes, mas compara objetos dispersos;
- ordenar objetos inline move mais dados, mas pode melhorar localidade posterior.

Quando dados excedem a RAM, use ordenação externa:

1. leia um bloco que caiba com margem;
2. ordene-o em memória e grave uma *run*;
3. repita para toda entrada;
4. faça merge k-way com heap das cabeças;
5. escreva sequencialmente a saída.

O custo relevante passa a ser leituras/escritas por bloco. Compressão pode reduzir
I/O ao custo de CPU. Falha no meio requer arquivos temporários identificáveis,
limpeza e publicação atômica para não expor resultado parcial.

Ordenação paralela divide e combina, mas transferência, balanceamento,
sincronização e largura de banda da memória limitam ganho. Primeiro meça a versão
sequencial e tamanho em que o paralelismo paga seu overhead.

## Aplicação no Dependency Planner

O planejador não pode simplesmente ordenar tarefas pelo ID: isso ignora
dependências. Ele usa ordem topológica; o ID atua somente como desempate entre
tarefas simultaneamente disponíveis.

Considere:

```text
z-modelo -> a-api
b-docs (isolada)
```

Ordenar alfabeticamente produziria `a-api, b-docs, z-modelo`, violando a aresta.
Kahn primeiro encontra `b-docs` e `z-modelo`; um min-heap escolhe `b-docs`, depois
`z-modelo`, e só então `a-api`. A propriedade do domínio domina a ordenação local.

Possíveis usos legítimos neste projeto:

- `lower_bound` em uma lista persistida de IDs para sugestões por faixa;
- sort estável de relatórios por duração, preservando ordem topológica nos empates;
- heap para próxima tarefa disponível;
- heap limitado para as `k` tarefas mais longas, sem ordenar todo o relatório.

Teste determinismo permutando a ordem dos itens e dependências no JSON. Se o
contrato diz que IDs decidem empates, a saída deve permanecer igual. Se usar
strings Unicode, declare que a ordem técnica segue o comparador da linguagem ou
introduza uma chave normalizada bem especificada.

## Falhas comuns e diagnóstico

### Busca binária entra em loop ou perde extremos

**Diagnóstico:** escreva o intervalo como fechado ou semiaberto e não misture
fórmulas. Prove que a variante diminui. Teste comprimentos 0, 1 e 2 e alvos fora.

### Dados deixaram de estar ordenados

Busca binária pode retornar ausência falsa sem erro visível. Encapsule mutações,
insira na posição correta ou invalide/reconstrua o índice.

### Sort parece ordenado, mas perdeu elementos

Valide ordem **e** multiconjunto. Use IDs únicos anexados para testar estabilidade
de chaves repetidas.

### Merge quebra estabilidade

Em empate, retirar primeiro da metade direita inverte itens iguais separados pela
divisão. Compare pela chave e favoreça a esquerda.

### Quicksort degrada com repetidos ou entrada ordenada

Registre profundidade e tamanhos das partições. Use pivô robusto, randomização,
partição em três vias ou algoritmo híbrido com limite de profundidade.

### Comparador viola transitividade

Resultados podem variar, falhar ou entrar em comportamento não garantido. Teste
triplas, empates, valores extremos, `NaN` e overflow. Não compare campos mutáveis
durante a operação.

### Chamar counting/radix de linear sem qualificar

Inclua `K`, base, quantidade de dígitos, representação e memória na análise. Uma
entrada pequena com universo enorme pode ser pior que comparação.

## Exercícios por nível

### Nível 1 — contratos e invariantes

1. Implemente `lower_bound` e `upper_bound` sobre intervalo semiaberto.
2. Implemente insertion sort estável sem usar `sort`.
3. Verifique automaticamente ordem, permutação e estabilidade.

**Aceite:** testes cobrem vazio, duplicatas, extremos e alvo ausente; cada laço
possui invariante escrita e uma medida que prova terminação.

### Nível 2 — comparar algoritmos

1. Implemente mergesort que não altera a entrada e mede buffer de pico.
2. Implemente quicksort em três vias; gere casos ordenados, reversos e repetidos.
3. Compare ordenar+buscar, busca linear e conjunto para `q` crescente.
4. Use heap para encontrar `k` maiores em fluxo.

**Aceite:** todas as versões produzem o mesmo multiconjunto; benchmark separa
construção de consulta e relata distribuição, memória e ambiente.

### Nível 3 — limites e sistema real

1. Escreva a prova por árvore de decisão para `Ω(n log n)`.
2. Implemente counting ou radix sort e determine empiricamente quando `K`/dígitos
   anulam a vantagem.
3. Crie um external merge sort limitado a uma pequena quota de memória.
4. No planejador, compare saída sem desempate, com ordenação global incorreta e
   com heap correto; produza um contraexemplo mínimo.

**Aceite:** arquivos temporários são limpos em sucesso e falha; resultado só é
publicado completo; a análise declara hipóteses e valida dependências do plano.

## Checklist de domínio

- [ ] Defino duplicatas, ausência, comparador e mutação no contrato de busca.
- [ ] Implemento busca binária por intervalo/invariante, sem decorar índices.
- [ ] Sei usar `lower_bound` e `upper_bound` para ocorrências e faixas.
- [ ] Verifico ordem, permutação e estabilidade separadamente.
- [ ] Explico invariantes de insertion, merge e particionamento.
- [ ] Comparo mergesort, quicksort e heapsort em tempo, memória e cache.
- [ ] Demonstro o limite de comparações e seus limites de aplicação.
- [ ] Declaro `K`, dígitos e distribuição em algoritmos não comparativos.
- [ ] Reconheço quando selecionar `k` itens é melhor que ordenar todos.
- [ ] Preservo dependências antes de aplicar desempate no Dependency Planner.

Dominar busca e ordenação não é recitar nomes. É reconstruir o algoritmo a
partir do contrato, provar a invariante e reconhecer quando outra estrutura torna
a operação desnecessária.
