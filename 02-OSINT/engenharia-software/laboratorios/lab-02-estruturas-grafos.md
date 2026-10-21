# Lab 02 — estruturas, busca e grafos

## Resultado esperado

Você implementará o mesmo contrato sobre representações diferentes,
verificará propriedades do resultado e explicará por que uma estrutura adequada
para uma operação pode ser ruim para outra. A entrega conecta os capítulos 02 a
05 sem transformar algoritmos em receitas isoladas.

## Pré-requisitos e tempo

- capítulos 02, 03, 04 e 05;
- Lab 01 concluído;
- duas linguagens entre Python, Java, C17, C# e JavaScript;
- 12 a 18 horas.

## Linha de base

Execute o runner e abra o [guia dos exemplos](../exemplos/README.md):

```bash
bash 02-OSINT/engenharia-software/testar-curso.sh
```

Compare a lista/matriz de adjacência, o conjunto de dependentes, a contagem de
grau e a estrutura de itens prontos. Preencha:

| Implementação | representação | obter vizinhos | escolher pronto | limite | custo total |
|---|---|---|---|---|---|
| Python | | | | | |
| Java | | | | | |
| C17 | | | | | |
| C# | | | | | |
| JavaScript | | | | | |

Não atribua `O(1)` a um mapa sem registrar que é custo esperado e depende de
hash/igualdade. Não atribua `O(V+E)` à matriz C: ela percorre células ausentes.

## Parte 1 — duas representações

Na primeira linguagem, implemente:

1. lista de adjacência com mapa de IDs;
2. matriz de adjacência com mapeamento ID→índice.

Ambas devem cumprir a mesma interface de leitura: `vertices()`, `neighbors(v)`,
`has_edge(u, v)` e `edge_count()`. Rode testes de contrato contra as duas.
Meça memória aproximada para grafo esparso e denso, explicitando o método de
medição e suas limitações.

## Parte 2 — estruturas auxiliares

Implemente uma fila circular limitada e use-a numa BFS. Teste:

- vazio → um item → cheio → wrap-around → vazio;
- leitura sem remoção;
- overflow e underflow conforme o contrato;
- capacidade um;
- nenhuma retenção indevida de referência após remoção.

Depois substitua a fila de prioridade da ordenação topológica por fila FIFO.
Mostre que a ordem ainda pode ser topológica, mas deixa de cumprir o desempate
ordinal. Correção e determinismo são propriedades diferentes.

## Parte 3 — propriedades, não exemplos decorados

Gere DAGs pequenos a partir de uma permutação: só crie aresta da posição
menor para a maior. Para cada grafo, prove automaticamente:

- resultado contém todos e somente os vértices;
- toda aresta respeita a ordem;
- executar duas vezes produz o mesmo resultado;
- adicionar vértice isolado preserva as restrições anteriores;
- adicionar aresta compatível não produz ciclo.

Em seguida, escolha um caminho existente e adicione aresta de retorno. O
algoritmo deve rejeitar o grafo. Preserve a semente quando houver aleatoriedade.

## Parte 4 — busca, ordenação e estabilidade

Implemente busca binária `lower_bound`: devolva a primeira posição em que um
valor poderia ser inserido sem quebrar a ordem. Cubra vazio, antes do primeiro,
duplicatas, entre elementos e depois do último.

Ordene tarefas por duração mantendo a ordem topológica anterior nos empates.
Prove estabilidade com IDs distintos e mesma duração. Compare:

- ordenar tudo e consultar muitas vezes;
- varrer uma vez para uma única consulta;
- manter heap de tamanho `k` para os `k` maiores;
- custo de manter um índice quando dados mudam.

## Parte 5 — diagnóstico de mutações

Introduza temporariamente uma mutação por vez:

1. marque BFS ao remover, não ao inserir;
2. esqueça de decrementar um grau;
3. aceite duplicatas no resultado;
4. inverta uma comparação do heap;
5. remova o desempate do comparador.

Identifique qual teste acusa cada defeito. Se uma mutação sobrevive, acrescente
um teste que expresse a regra ausente e reverta a mutação.

## Gate de conclusão

- duas representações passam pela mesma suíte de contrato;
- fila circular atravessa todas as transições sem estado inconsistente;
- propriedades são verificadas sobre vários DAGs reproduzíveis;
- busca binária possui invariante e casos de duplicata;
- estabilidade e desempate foram demonstrados;
- cada mutação relevante é morta por pelo menos um teste.

