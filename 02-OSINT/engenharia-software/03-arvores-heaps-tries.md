# 03 — Árvores, heaps e tries

Árvores representam hierarquia e mantêm relações que permitem descartar partes
da busca. O custo não vem do desenho parecer uma árvore: vem de invariantes como
ordem, altura limitada, preenchimento de páginas ou prioridade entre pai e filhos.
Quando uma dessas propriedades não é preservada, a complexidade prometida deixa
de valer.

## Objetivos verificáveis

Ao concluir, você deverá conseguir:

1. distinguir profundidade, altura, grau, árvore, floresta e subárvore;
2. derivar busca, inserção e remoção de BST em função da altura;
3. explicar as invariantes de AVL e rubro-negra e o papel das rotações;
4. relacionar B-tree/B+tree, fator de ramificação e acesso por página;
5. implementar e validar min-heap e demonstrar por que `heapify` custa `O(n)`;
6. modelar prefixos com trie/radix tree sem confundir bytes, pontos de código e grafemas;
7. escolher uma estrutura apropriada para buscas exatas, intervalos, prioridade e prefixo;
8. explicar por que o Dependency Planner usa heap, e não uma árvore completa.

## Pré-requisitos e mapa mental

Revise recursão, arrays, listas e complexidade. O mapa de decisão inicial é:

```text
preciso de...
  hierarquia geral -> árvore de n filhos
  busca ordenada/faixa -> BST balanceada
  índice em armazenamento por blocos -> B-tree/B+tree
  apenas menor/maior repetidamente -> heap
  consulta por prefixo -> trie/radix tree
  busca exata sem ordem -> tabela hash
```

Uma estrutura especializada pode ser excelente para uma pergunta e inadequada
para outra. Heap encontra o mínimo, mas não responde busca arbitrária rapidamente;
trie encontra prefixos, mas pode consumir muito mais memória que um mapa.

## Vocabulário e propriedades estruturais

- **raiz:** nó sem pai;
- **folha:** nó sem filhos;
- **profundidade:** quantidade de arestas da raiz até o nó;
- **altura de um nó:** maior quantidade de arestas dele até uma folha;
- **altura da árvore:** altura da raiz;
- **grau/fator de ramificação:** quantidade de filhos;
- **subárvore:** um nó e todos os seus descendentes;
- **floresta:** conjunto de árvores disjuntas.

Uma árvore não vazia com `n` nós possui `n-1` arestas, é conectada e não possui ciclo.
Retirar qualquer aresta a desconecta; adicionar uma aresta entre dois de seus nós
cria exatamente um ciclo. Estruturas chamadas de “árvore” podem deixar de sê-lo:
links simbólicos em um sistema de arquivos e compartilhamento de subexpressões em
uma AST podem produzir grafos.

Percursos binários clássicos:

| Percurso | Ordem | Uso típico |
|---|---|---|
| pré-ordem | nó, esquerda, direita | serializar/copiar estrutura |
| em ordem | esquerda, nó, direita | obter chaves de BST em ordem |
| pós-ordem | esquerda, direita, nó | liberar/calcular resultado dos filhos |
| por nível | profundidade crescente | menor número de arestas, visualização |

Percursos recursivos usam `O(h)` de pilha. Uma entrada adversa pode produzir
`h=n`; a versão iterativa com pilha/fila explícita evita o limite de chamadas,
mas continua usando memória proporcional à fronteira.

## Árvore binária de busca

Para cada nó de uma BST, todas as chaves da subárvore esquerda são menores e
todas as da direita são maiores, segundo um comparador consistente. Chaves
duplicadas exigem política: rejeitar, guardar contador/valores no mesmo nó ou
escolher deterministicamente um lado.

```text
search(node, key):
    enquanto node existe:
        se key == node.key: retorne node
        se key < node.key: node = node.left
        senão:             node = node.right
    retorne ausente
```

Cada comparação desce um nível; busca e inserção custam `Θ(h)`. Em uma árvore
balanceada `h=Θ(log n)`; inserir `1, 2, 3, ..., n` em uma BST simples cria uma
corrente com `h=n-1` e operações `Θ(n)`.

### Remoção e sua invariante

Existem três casos:

1. folha: retire a referência do pai;
2. um filho: ligue o pai diretamente ao filho;
3. dois filhos: substitua a chave pelo sucessor em ordem, o menor da subárvore
   direita, e remova esse sucessor em seu local original.

O sucessor não tem filho esquerdo, logo o terceiro caso se reduz a um dos dois
primeiros. Se o nó também guarda valor, mova o par completo, não apenas a chave.
Em implementação com ponteiros para pai ou metadados de altura/cor, todos eles
precisam ser atualizados.

### Comparador é parte do contrato

A ordem precisa ser total ou adequada ao domínio: antissimétrica, transitiva e
estável durante a permanência do item. Se `a < b`, `b < c` e `c < a`, a busca
não tem caminho coerente. Mudar uma chave depois de inseri-la também viola a
posição. Para strings, defina se a ordem é por bytes, Unicode, locale ou uma chave
normalizada; esses critérios não produzem necessariamente a mesma sequência.

## Balanceamento: limitar altura sem perder ordem

Rotações locais reorganizam poucos elos preservando a ordem em percurso:

```text
      y                 x
     / \               / \
    x   C   direita    A   y
   / \       ---->        / \
  A   B                 B   C
```

Antes e depois, `A < x < B < y < C`. A rotação muda alturas, não a ordenação.

### AVL

Em cada nó, o fator de balanço `altura(esquerda) - altura(direita)` pertence a
`{-1, 0, 1}`. Após inserção ou remoção, alturas são recalculadas no caminho até
a raiz e casos externos/internos usam rotações simples ou duplas. Essa regra
mantém altura `O(log n)` e costuma favorecer buscas pela árvore mais rigidamente
balanceada, ao custo de mais metadados e possíveis rotações em atualizações.

### Rubro-negra

Uma formulação comum exige:

1. cada nó é vermelho ou preto;
2. raiz é preta;
3. folhas sentinela `NIL` são pretas;
4. nó vermelho não tem filho vermelho;
5. todo caminho de um nó até folhas `NIL` possui o mesmo número de nós pretos.

Essas propriedades limitam o caminho mais longo a menos do dobro do mais curto,
produzindo altura `O(log n)`. Recolorações e rotações restauram as invariantes.
Rubro-negras permitem balanço menos rígido que AVL e são comuns em mapas/conjuntos
ordenados com muitas inserções e remoções.

Em produção, prefira `TreeMap`, `SortedDictionary`/estruturas equivalentes ou
bibliotecas maduras. Implementar balanceamento é excelente exercício, mas remoção
correta possui muitos estados de borda.

## Consultas que justificam uma árvore ordenada

Tabela hash tende a ser mais simples para consulta exata. Uma árvore balanceada
oferece também, em `O(log n)` ou `O(log n + k)`:

- menor/maior chave;
- predecessor e sucessor;
- primeira chave maior ou igual a `x` (*lower bound*);
- intervalo `[a,b]`, emitindo `k` resultados;
- iteração ordenada sem ordenar novamente.

Se o sistema precisa dessas operações repetidamente, manter ordem incremental
pode compensar o `log n` de cada atualização.

## B-tree e B+tree: altura medida em páginas

BSTs têm no máximo dois filhos. Em armazenamento, uma leitura traz uma página de
vários KiB; usar só duas referências por página desperdiça largura de banda e
aumenta acessos. B-trees guardam muitas chaves e filhos por nó.

Para uma B-tree de grau mínimo `t`, uma definição comum mantém:

- cada nó, exceto a raiz, possui entre `t-1` e `2t-1` chaves;
- um nó interno com `k` chaves possui `k+1` filhos;
- chaves separam intervalos dos filhos;
- todas as folhas estão na mesma profundidade;
- split e merge restauram ocupação durante atualizações.

Um grande fator de ramificação produz altura pequena. Com centenas de filhos por
página, milhões de registros podem exigir poucos acessos. A CPU ainda compara
chaves dentro do nó, mas o objetivo principal é reduzir I/O e faltas de página.

Na B+tree, valores ou ponteiros de registros ficam tipicamente nas folhas; nós
internos servem de índice, e folhas são ligadas em ordem. Isso favorece varreduras
por intervalo: localize a primeira folha e percorra folhas adjacentes. Bancos de
dados precisam lidar ainda com concorrência, WAL, page split, preenchimento,
compressão de prefixos e cache; o desenho abstrato é apenas o começo.

## Heap: ordem parcial para prioridade

Um min-heap binário possui duas invariantes:

1. **forma:** árvore binária completa, preenchida por níveis da esquerda para a direita;
2. **ordem:** a chave de cada pai é menor ou igual às chaves dos filhos.

A forma permite armazenar em vetor, para índice zero:

```text
pai(i)      = (i - 1) // 2, para i > 0
esquerdo(i) = 2*i + 1
direito(i)  = 2*i + 2
```

Somente a raiz é garantidamente mínima; irmãos e subárvores não estão totalmente
ordenados. Procurar chave arbitrária continua `O(n)`.

### Inserir e remover

- inserir no fim preserva a forma; subir trocando com o pai (*sift up*) restaura
  ordem em `O(log n)`;
- remover a raiz coloca o último item na raiz; descer trocando com o menor filho
  (*sift down*) restaura ordem em `O(log n)`;
- consultar a raiz custa `Θ(1)`;
- alterar prioridade exige conhecer a posição ou inserir nova entrada e ignorar
  a obsoleta quando sair.

### Por que `heapify` é `O(n)`

Inserir `n` itens um a um dá `O(n log n)`. O algoritmo bottom-up aplica *sift
down* dos últimos pais até a raiz. Aproximadamente metade dos nós é folha e não
desce; um quarto pode descer um nível; um oitavo, dois. A soma ponderada
`n/4*1 + n/8*2 + n/16*3 + ...` é `O(n)`. Multiplicar todos os `n` nós pela altura
máxima fornece um limite verdadeiro, mas frouxo.

### Prioridade composta e estabilidade

Se duas tarefas têm a mesma prioridade, compare `(prioridade, sequencia, item)`.
O contador crescente produz FIFO entre empates e evita comparar objetos sem ordem.
Se a regra do planejador é escolher menor ID, o próprio ID é a chave. Unicode e
locale precisam de semântica definida se essa ordem for exibida a humanos.

## Trie e radix tree

Uma trie representa cada unidade da chave em uma aresta. Palavras com prefixo
comum compartilham caminho; um marcador informa se o nó termina uma chave.

```text
(raiz)
  c - a - r [fim]
      |   \
      s    t - a [fim]
      |
      a [fim]
```

Buscar/inserir uma chave de comprimento `k` custa `O(k)` no modelo em que acessar
o filho é constante. Esse custo independe da quantidade de palavras, mas o total
de nós pode chegar à soma dos comprimentos. Um mapa de filhos por nó economiza
alfabeto esparso, porém adiciona hashes/alocações; um array de tamanho fixo é
rápido e desperdiça espaço.

Uma radix tree comprime caminhos de nós com um único filho em uma aresta rotulada
por segmento. Reduz nós e indireções, mas inserção pode dividir arestas. Patricia
tries operam sobre bits e são usadas em prefixos de endereçamento.

### Texto e Unicode

Defina a unidade de `k`:

- bytes UTF-8 variam por ponto de código;
- pontos de código não equivalem a caracteres percebidos;
- grafema pode conter base, marcas e sequências compostas;
- formas visualmente iguais podem ter normalizações diferentes.

Normalizar para NFC ou aplicar *case folding* pode ser correto para busca humana,
mas errado para identificadores sensíveis a bytes. Guarde a forma original se
precisar exibi-la e trate a chave normalizada como uma decisão de domínio.

Autocomplete normalmente localiza o nó do prefixo em `O(k)` e depois percorre
resultados. O custo total precisa incluir os itens emitidos. Limitar a `r`
sugestões pode exigir metadados ou heap por popularidade; uma DFS simples retorna
ordem estrutural, não necessariamente relevância.

## Comparando estruturas

| Necessidade | Estrutura | Custo principal | Limitação |
|---|---|---|---|
| chave exata | hash | esperado `O(1)` | sem faixas/ordem geral |
| chave e intervalo | BST balanceada | `O(log n + k)` | ponteiros/comparações |
| páginas persistentes | B+tree | `O(log_B n + k)` I/Os | splits e concorrência complexos |
| próximo menor/maior | heap | topo `O(1)`, update `O(log n)` | busca arbitrária `O(n)` |
| prefixo | trie/radix | `O(k + saída)` | memória e semântica textual |

`k` na consulta de intervalo é quantidade de resultados; na trie é comprimento
da chave, portanto sempre nomeie as variáveis no contexto.

## Aplicação no Dependency Planner

Durante a ordenação, várias tarefas podem ter grau de entrada zero. O requisito
é produzir resultado determinístico pelo menor ID. Um min-heap oferece:

```python
from heapq import heapify, heappop, heappush

available = [task_id for task_id, degree in indegree.items() if degree == 0]
heapify(available)

order: list[str] = []
while available:
    current = heappop(available)
    order.append(current)
    for successor in adjacency[current]:
        indegree[successor] -= 1
        if indegree[successor] == 0:
            heappush(available, successor)
```

Invariante: o heap contém exatamente tarefas ainda não emitidas cuja quantidade
de predecessoras pendentes é zero; sua raiz é o menor ID entre elas. `heapify`
inicial custa `O(V)`, e cada tarefa entra/sai no máximo uma vez. A escolha
determinística acrescenta `O(V log V)` ao percurso `O(V+E)`.

Uma BST balanceada também poderia manter o conjunto disponível, com inserção e
remoção `O(log V)`. Ela oferece intervalos e remoção arbitrária de que o algoritmo
não precisa. Heap possui contrato menor e representa melhor “sempre tire o menor”.
Uma trie só se justificaria para um recurso de autocomplete de IDs, fora do núcleo.

## Falhas comuns e diagnóstico

### Confundir árvore binária com BST

**Sintoma:** busca escolhe esquerda/direita em uma árvore sem invariante de ordem.  
**Diagnóstico:** percurso em ordem deve produzir sequência ordenada segundo o
comparador; valide limites inferior/superior para cada subárvore.

### Atualizar elos sem metadados

Após rotação, confira pais, raiz, alturas/cores e tamanho. Um validador recursivo
que recalcula tudo é lento para produção, mas excelente em testes.

### Usar heap como lista ordenada

Iterar o vetor interno não produz ordem. Remova repetidamente de uma cópia ou use
ordenação. Alterar um item no meio sem sift viola a propriedade.

### Esquecer entrada obsoleta na fila de prioridade

Ao simular `decrease-key` inserindo nova prioridade, duas versões coexistem.
Compare com o estado atual ao retirar e descarte a antiga; caso contrário o mesmo
objeto pode ser processado duas vezes.

### Trie explode em memória

Meça nós, filhos vazios e alocações. Considere mapa compacto, radix tree,
minimal automaton ou lista ordenada com busca de prefixo, conforme o volume.

### Comparador inconsistente

Gere triplas e teste transitividade, sinal invertido e igualdade. Valores como
`NaN`, locale e campos mutáveis merecem casos explícitos.

## Exercícios por nível

### Nível 1 — construir invariantes

1. Implemente BST com inserção, busca e percurso em ordem; defina duplicatas.
2. Insira uma sequência crescente e registre a altura a cada passo.
3. Implemente min-heap em vetor e um validador da propriedade pai/filho.

**Aceite:** vazio e um nó funcionam; percurso da BST está ordenado; cada operação
do heap preserva forma, tamanho e ordem.

### Nível 2 — comparar e ampliar

1. Implemente remoção dos três casos da BST.
2. Construa heap por inserções e por `heapify`; conte comparações.
3. Implemente trie com inserção, busca exata, remoção e autocomplete limitado.
4. Desenhe splits de uma B-tree pequena para uma sequência fornecida.

**Aceite:** remoção de prefixo não apaga palavra maior; `heapify` mostra
crescimento linear; todos os nós B-tree respeitam ocupação definida.

### Nível 3 — uso profissional

1. Implemente AVL ou rubro-negra com validador independente de todas as invariantes.
2. Compare mapa hash, mapa ordenado e trie para IDs reais e Unicode normalizado.
3. Substitua o heap do planejador por fila e árvore ordenada; meça e explique
   diferenças de resultado e custo.

**Aceite:** testes aleatórios comparam operações a uma biblioteca de referência;
o relatório inclui altura, alocações, memória e semântica de desempate.

## Checklist de domínio

- [ ] Distingo profundidade de altura e árvore de grafo geral.
- [ ] Derivo operações da BST como `Θ(h)`, não automaticamente `O(log n)`.
- [ ] Explico o que rotações preservam e as invariantes AVL/rubro-negras.
- [ ] Relaciono B+tree a páginas, ramificação e consultas por faixa.
- [ ] Implemento heap e explico por que seu vetor não está totalmente ordenado.
- [ ] Demonstro `heapify` linear pela distribuição das alturas.
- [ ] Escolho conscientemente a unidade textual e normalização de uma trie.
- [ ] Comparo hash, árvore, heap e trie pela pergunta que precisam responder.
- [ ] Justifico heap e seu custo dentro do Dependency Planner.

Uma árvore é eficiente apenas enquanto seu contrato estrutural permanece
verdadeiro. Implementar a operação e validar a invariante são a mesma tarefa.
