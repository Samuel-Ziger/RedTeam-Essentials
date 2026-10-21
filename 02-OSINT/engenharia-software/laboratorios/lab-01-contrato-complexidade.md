# Lab 01 — contrato, oráculo e complexidade

## Resultado esperado

Você transformará um pedido ambíguo em contrato verificável, construirá um
oráculo independente da implementação e confrontará a análise assintótica com
medições controladas. O objetivo é evitar dois erros comuns: otimizar uma
especificação errada e usar benchmark como substituto de raciocínio.

## Pré-requisitos e tempo

- capítulos 00 e 01;
- Python 3.12+ ou outra linguagem do curso;
- 8 a 12 horas;
- fixtures exclusivamente sintéticas.

## Cenário

Um planejador recebe tarefas e relações do tipo “A depende de B”. Ele deve
produzir uma ordem em que todo pré-requisito aparece antes de seus dependentes.
Se houver mais de uma ordem válida, o menor identificador ordinal disponível é
escolhido. Referência desconhecida, ID duplicado e ciclo são erros de entrada.

Antes de abrir o código, escreva:

1. tipos e limites de cada campo;
2. pré-condições e pós-condições;
3. invariantes do grafo;
4. política para entrada vazia, aresta repetida e autoaresta;
5. critério de determinismo;
6. classes de falha e o que permanece observável em cada uma.

## Parte 1 — tabela de exemplos

Crie fixtures para, no mínimo:

- grafo vazio;
- um vértice isolado;
- cadeia de cinco tarefas;
- diamante (`A -> B`, `A -> C`, `B -> D`, `C -> D`);
- dois componentes desconectados;
- aresta repetida;
- referência desconhecida;
- autoaresta;
- ciclo de dois vértices;
- ciclo dentro de um componente maior.

Para entradas válidas, não compare somente com uma lista fixa. Implemente um
oráculo `is_topological_order(vertices, edges, result)` que prove:

```text
result possui exatamente os vértices da entrada, sem repetição
e, para toda aresta u -> v, position[u] < position[v]
```

Uma ordem diferente pode estar correta quando o contrato não exige desempate.
Como este laboratório exige ordem ordinal, acrescente casos em que vários itens
ficam prontos simultaneamente.

## Parte 2 — derive o custo

Para o algoritmo de Kahn com lista de adjacência e fila de prioridade, derive
separadamente:

- construção do índice e dos graus;
- inserções/remoções da fila;
- visita das arestas;
- memória de entrada e memória adicional.

Declare `V` e `E` antes da fórmula. Explique por que dizer apenas `O(n)` apaga
uma dimensão essencial. Depois repita a análise para a matriz de adjacência da
implementação C e identifique a diferença entre limite assintótico e limite
fixo `MAX_NODES`.

## Parte 3 — experimento de crescimento

Gere três famílias de DAGs determinísticos: cadeia, leque e esparso. Use
tamanhos dobrados, por exemplo `128, 256, 512, 1024, 2048`. Não inclua a
geração do fixture na região medida.

Registre:

| Família | V | E | mediana | p95 | tempo/V | tempo/(V+E) |
|---|---:|---:|---:|---:|---:|---:|

Faça aquecimento, execute repetições suficientes e use relógio monotônico.
Não remova outliers sem explicar sua causa. O experimento deve sustentar uma
tendência, não provar Big O matematicamente.

## Parte 4 — entrada adversarial e limites

Estime a memória de um documento com 100 mil vértices e um milhão de arestas.
Defina limites de arquivo, quantidade de itens, tamanho de ID e número de
dependências por item. Diferencie:

- rejeitar antes de carregar;
- validar enquanto converte;
- detectar regra global depois de indexar;
- interromper com erro estável sem resultado parcial.

Não use os limites escolhidos como se fossem universais: registre a carga e o
ambiente que justificam a política.

## Gate de conclusão

- contrato cobre sucesso, vazio, limites e erros;
- o oráculo rejeita pelo menos três ordens deliberadamente inválidas;
- a análise usa `V` e `E` e inclui espaço;
- o benchmark é repetível e não mede geração do fixture;
- resultados diferentes de sua previsão foram explicados, não ocultados;
- um teste permanente falha se a política de desempate for removida.

