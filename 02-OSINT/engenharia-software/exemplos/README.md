# Exemplo comparado — grafo de dependências em cinco linguagens

As cinco implementações resolvem o mesmo núcleo: registrar tarefas, interpretar
`pré-requisito -> dependente`, produzir uma ordem topológica determinística e
rejeitar ciclos. Elas não tentam parecer idênticas; cada uma evidencia tipos,
memória e tratamento de erros da linguagem.

Para que “menor ID ordinal” tenha a mesma semântica nos cinco runtimes, os
exemplos aceitam apenas IDs no formato ASCII seguro
`[A-Za-z0-9][A-Za-z0-9._-]*`.

## Arquivos

- [Python](python/dependency_graph.py) e [testes](python/test_dependency_graph.py);
- [Java](java/DependencyPlanner.java);
- [C17](c/dependency_graph.c);
- [C#](csharp/Program.cs) e [projeto](csharp/DependencyPlanner.csproj);
- [JavaScript](javascript/dependencyGraph.mjs) e
  [testes](javascript/dependencyGraph.test.mjs).

Execute todos os runtimes disponíveis:

```bash
bash 02-OSINT/engenharia-software/testar-curso.sh
```

## Contrato comum

Para um grafo válido, a saída deve:

1. conter cada vértice exatamente uma vez;
2. posicionar todo pré-requisito antes do dependente;
3. escolher o menor ID ordinal entre os vértices prontos;
4. ser igual em execuções repetidas;
5. não alterar a estrutura original de dependências.

Grafo cíclico não possui ordem topológica e precisa ser rejeitado. As versões
didáticas diferem na riqueza do erro; o projeto completo devolve um caminho de
ciclo fechado.

## A mesma ideia, custos diferentes

| Aspecto | Python | Java | C17 | C# | JavaScript |
|---|---|---|---|---|---|
| vértices/arestas | `dict` + `set` | `HashMap` + `HashSet` | arrays + matriz fixa | `Dictionary` + `HashSet` | `Map` + `Set` |
| prontos | `heapq` | `PriorityQueue` | varredura linear | `PriorityQueue` | array ordenado |
| erro esperado | exceção própria | exceção | sentinela/`bool` | exceção | exceção |
| limite | memória/entrada | memória/entrada | 32 nós, IDs de 31 bytes | memória/entrada | memória/entrada |
| custo dominante | `O(V+E+V log V)` | `O(V+E+V log V)` esperado | `O(V²)` | `O(V+E+V log V)` esperado | pode chegar a `O(V² log V)` pelo resort |

Os limites assumem hashes bem comportados e contam operações abstratas. A
versão C usa matriz: obter uma aresta é simples, mas localizar próximo pronto e
percorrer dependentes varre os `V` slots. JavaScript reordena o array de prontos
após inserções; isso é intencional para discutir a diferença entre interface e
estrutura adequada.

## Pontos para leitura crítica

### Direção da aresta

“`api` depende de `modelo`” é armazenado como `modelo -> api`. Assim, o grau de
entrada de `api` conta pré-requisitos ainda não satisfeitos. Inverter uma das
estruturas pode produzir resultado plausível, mas semanticamente errado.

### Duplicatas

Conjuntos tornam uma aresta repetida idempotente. Se a representação usasse
lista e incrementasse o grau duas vezes, remover apenas uma ocorrência deixaria
a tarefa bloqueada. A escolha da coleção participa da correção.

### Determinismo

Uma DAG pode ter muitas ordens válidas. Heap, priority queue ou seleção ordinal
criam um contrato mais forte: a mesma entrada produz a mesma saída. Isso ajuda
testes, diffs e cache, mas adiciona custo.

### Ownership e exposição

Python devolve tupla em `nodes`; Java usa `List.copyOf`; C escreve num buffer do
chamador; C# devolve interface somente leitura; JavaScript mantém campos
privados. Nenhuma dessas escolhas torna objetos profundamente imutáveis por si
só. Analise quem ainda possui referências mutáveis.

### Limites e falhas

Em C, `graph_add_node` pode falhar por ID inválido ou capacidade, e o chamador
precisa verificar o `bool`. Nas linguagens com exceção, capturar tudo e continuar
seria igualmente incorreto: falha de contrato não deve produzir plano parcial.
Por isso `addDependency` valida os dois IDs — e, em C, também a capacidade —
antes da primeira mutação.

## Exercícios comparativos

1. Adicione vértice isolado e teste se aparece na saída.
2. Crie diamante e prove propriedades em vez de uma ordem arbitrária.
3. Duplique uma aresta e confirme idempotência.
4. Introduza autoaresta e documente se a rejeição ocorre na escrita ou leitura.
5. Troque a estrutura de prontos e meça o efeito sem mudar o contrato.
6. Adicione limites equivalentes de ID/quantidade ou documente por que não são
   equivalentes.
7. Implemente um validador de ordem separado nas cinco linguagens.

## Critério de domínio

Você concluiu a comparação quando consegue prever a saída e o custo, explicar
uma diferença idiomática sem classificar linguagem como “melhor” e escrever um
teste que detecta aresta invertida, ciclo, duplicata e perda de determinismo.
