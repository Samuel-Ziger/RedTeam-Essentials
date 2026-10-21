# Lab 03 — estratégias algorítmicas e design modular

## Resultado esperado

Você calculará caminho crítico por programação dinâmica, construirá um
contraexemplo para uma heurística gulosa e separará política de mecanismo por
portas e adaptadores. A entrega deve mostrar que abstração é uma decisão sobre
dependências, não uma quantidade de classes.

## Pré-requisitos e tempo

- capítulos 06 a 10;
- Labs 01 e 02 concluídos;
- projeto [Dependency Planner](../projetos/dependency-planner/README.md);
- 12 a 18 horas.

## Parte 1 — do estado à recorrência

Para cada tarefa `v` de um DAG, defina:

```text
finish(v) = duration(v),                                      se v não depende de ninguém
finish(v) = duration(v) + max(finish(u) para u em deps(v)),   caso contrário
```

Explique por que a ordem topológica garante que os estados necessários já estão
calculados. Implemente duração mínima e reconstrução do caminho, guardando o
predecessor escolhido. Defina o desempate quando dois predecessores terminam no
mesmo instante.

Teste ao menos:

- vazio e tarefa única;
- cadeia;
- diamante com caminhos de pesos diferentes;
- empate de caminhos;
- dois componentes;
- duração inválida;
- ciclo rejeitado antes da DP.

Compare a solução iterativa com uma versão recursiva memoizada. Registre
profundidade, estados calculados e comportamento numa cadeia maior que o limite
de pilha da linguagem.

## Parte 2 — prove onde o guloso falha

Considere a extensão: selecionar tarefas independentes sob orçamento de horas
para maximizar valor. Proponha as heurísticas “maior valor”, “menor duração” e
“melhor valor/duração”. Para cada uma, forneça um fixture pequeno em que ela
perde para a solução ótima 0/1.

Implemente a DP de mochila somente depois de declarar:

- significado de `dp[i][capacity]`;
- transição e casos-base;
- ordem de iteração;
- como reconstruir os itens;
- complexidade e por que ela é pseudopolinomial.

Se comprimir para uma dimensão, explique por que capacidades precisam ser
percorridas de trás para frente. Um teste deve falhar quando a direção é
invertida.

## Parte 3 — política injetável

No planejador, extraia a escolha do próximo item pronto para um contrato. Crie
duas estratégias:

1. ID ordinal crescente;
2. maior duração primeiro, com ID como desempate.

O algoritmo continua responsável por graus, arestas e detecção de ciclo; a
estratégia não pode modificar o grafo. Rode os mesmos testes de propriedade para
as duas. Não compare uma ordem exata quando a estratégia promete apenas uma
ordem topológica.

Avalie a representação idiomática em duas linguagens:

| Linguagem | contrato | implementação | composição |
|---|---|---|---|
| Python/JS | callable/protocolo estrutural | função ou objeto | argumento |
| Java/C# | interface/delegate | classe/lambda | construtor |
| C | ponteiro de função + contexto | função | `struct` de opções |

Não force herança onde uma função expressa todo o contrato.

## Parte 4 — porta de entrada e adapter

Adicione um adapter CSV ao projeto sem importar CSV no domínio ou em
`graph.py`. Defina cabeçalho, escaping, encoding, limites e como representar
dependências. O adapter deve produzir os mesmos `WorkItem` do JSON.

Crie testes de contrato executados contra repositório JSON, CSV e fake em
memória. Eles devem provar snapshot imutável, erros tipados e equivalência do
modelo, sem exigir que os adapters tenham os mesmos métodos internos.

## Parte 5 — composition root e erros

A CLI é o único lugar que escolhe adapter, estratégia e formato de saída.
Desenhe a direção das dependências e confirme que:

- domínio não importa terminal, JSON ou CSV;
- casos de uso dependem de portas;
- adapters dependem do modelo/porta;
- exceções esperadas são traduzidas uma vez;
- erro vai para `stderr` e resultado para `stdout`;
- código de saída faz parte do contrato.

## Gate de conclusão

- recorrência, ordem e reconstrução da DP estão documentadas;
- três heurísticas gulosas têm contraexemplos reproduzíveis;
- duas estratégias preservam propriedades do grafo;
- JSON, CSV e fake passam pelo mesmo contrato;
- dependências apontam para o núcleo;
- a suíte anterior continua verde.

