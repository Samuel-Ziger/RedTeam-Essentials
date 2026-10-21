# 04 — Grafos: modelagem, percursos e caminhos

Grafos modelam relações: dependências, rotas, chamadas, permissões, estados,
recomendações e conexões físicas. O algoritmo só é correto se a representação
preservar a semântica do domínio e se suas pré-condições forem verdadeiras.
Dijkstra com peso negativo ou ordenação topológica em grafo cíclico não são
versões aproximadas: resolvem outro problema ou produzem resposta inválida.

## Objetivos verificáveis

Ao concluir, você deverá conseguir:

1. traduzir um domínio para vértices, arestas, direção, pesos e rótulos;
2. escolher matriz, lista, conjunto, lista de arestas ou CSR pelos custos exigidos;
3. implementar BFS e DFS iterativas e declarar suas invariantes;
4. detectar ciclos e produzir uma ordenação topológica verificável;
5. distinguir conectividade, componentes fortemente conexos e alcançabilidade;
6. escolher BFS, Dijkstra, Bellman–Ford, Floyd–Warshall ou A* pelas pré-condições;
7. distinguir menor caminho de árvore geradora mínima;
8. analisar tempo e memória em termos de `V` e `E` e aplicar isso ao Dependency Planner.

## Pré-requisitos e mapa mental

Revise filas, pilhas, conjuntos, mapas e heaps nos capítulos
[02](02-estruturas-lineares.md) e [03](03-arvores-heaps-tries.md).

```text
domínio
  -> semântica dos vértices e arestas
  -> classe: dirigido? ponderado? multigrafo? dinâmico?
  -> representação conforme operações e densidade
  -> algoritmo com pré-condições satisfeitas
  -> certificado/verificação do resultado
  -> custo em V, E, pesos e saída
```

## Modelo e semântica antes do código

Um grafo `G=(V,E)` possui conjunto de vértices e relações entre eles. Uma aresta
dirigida é um par ordenado `(u,v)`; em grafo não dirigido, `{u,v}` não tem sentido.

Classificações que alteram algoritmos:

- **dirigido/não dirigido:** seguir `u -> v` permite voltar?
- **ponderado/não ponderado:** custo é uniforme ou existe valor por aresta?
- **simples/multigrafo:** arestas paralelas e laços são permitidos?
- **cíclico/acíclico:** retornar a um vértice pelo sentido das arestas é possível?
- **estático/dinâmico:** consultas predominam ou arestas mudam continuamente?
- **finito/implícito:** todos os estados são materializados ou gerados sob demanda?

No planejador, adote explicitamente:

```text
A -> B significa: A precisa terminar antes de B começar.
```

Outra implementação poderia armazenar em `B` a lista de suas dependências e
descrever a mesma relação como `B -> A`. Ambas são possíveis, mas misturar a
convenção inverte grau de entrada, ordem e resultados. Escreva uma frase antes
de desenhar setas.

Perguntas de modelagem:

1. o que possui identidade e deve ser vértice?
2. a relação possui direção, peso, capacidade, tempo ou rótulo?
3. duas arestas entre o mesmo par representam eventos distintos?
4. peso pertence à aresta ou ao vértice?
5. ausência de aresta significa impossibilidade ou valor desconhecido?
6. o grafo cabe em memória e pode ser reconstruído?
7. o resultado precisa ser exato, determinístico ou incremental?

## Representações e contratos

### Matriz de adjacência

Uma matriz `V × V` guarda se, ou com que peso, cada par se conecta.

- espaço `Θ(V²)`;
- testar aresta `Θ(1)`;
- percorrer todos os vizinhos de um vértice `Θ(V)`;
- boa localidade e representação compacta com bitset para grafos densos;
- precisa distinguir “sem aresta” de um peso válido igual a zero.

### Lista de adjacência

Cada vértice aponta para seus vizinhos.

- espaço `Θ(V+E)`;
- percorrer vizinhos `Θ(grau(u))`;
- testar aresta custa `O(grau(u))` com lista ou esperado `O(1)` com conjunto;
- em grafo não dirigido, cada aresta costuma aparecer duas vezes;
- conjuntos removem duplicatas, mas acrescentam memória e podem perder ordem.

Invariantes: todo vizinho existe em `V`; cada aresta aparece conforme a convenção;
em grafo simples não há duplicatas; em grafo não dirigido, `v` aparece em
`adj[u]` se, e somente se, `u` aparece em `adj[v]`.

### Lista de arestas

Guarda pares ou triplas `(u,v,peso)`. Usa `Θ(E)`, é conveniente para importar,
ordenar por peso e executar Bellman–Ford/Kruskal. Encontrar todos os vizinhos
varre `E`, a menos que exista índice auxiliar.

### CSR/CSC

*Compressed Sparse Row* usa um vetor contíguo de vizinhos e outro com offsets de
cada vértice. Tem pouca sobrecarga e boa localidade para grafos esparsos estáticos.
Inserir uma aresta é caro porque pode deslocar o vetor. CSC organiza por destino
e favorece predecessores. Sistemas profissionais podem manter ambas ou criar uma
sob demanda, pagando memória por direções de percurso rápidas.

| Representação | Espaço | Existe `(u,v)` | Vizinhos de `u` | Atualização |
|---|---:|---:|---:|---:|
| matriz | `Θ(V²)` | `Θ(1)` | `Θ(V)` | `Θ(1)` |
| lista com vetor | `Θ(V+E)` | `O(grau(u))` | `Θ(grau(u))` | fim amort. `O(1)` |
| lista com set | `Θ(V+E)` + overhead | esperada `O(1)` | `Θ(grau(u))` | esperada `O(1)` |
| arestas | `Θ(E)` | `O(E)` | `O(E)` | fim amort. `O(1)` |
| CSR | `Θ(V+E)` compacto | busca/scan local | `Θ(grau(u))` | reconstrução cara |

## BFS: explorar por distância em arestas

Busca em largura usa fila. Em grafo não ponderado, a primeira descoberta de um
vértice fornece menor quantidade de arestas desde a origem.

```python
from collections import deque

def breadth_first_paths(graph: dict[str, set[str]], source: str):
    if source not in graph:
        raise KeyError(source)

    distance = {source: 0}
    parent: dict[str, str | None] = {source: None}
    queue = deque([source])

    while queue:
        current = queue.popleft()
        for neighbor in sorted(graph[current]):  # apenas para desempate reproduzível
            if neighbor not in distance:
                distance[neighbor] = distance[current] + 1
                parent[neighbor] = current
                queue.append(neighbor)
    return distance, parent
```

Invariantes:

1. um vértice entra na fila apenas na primeira descoberta;
2. ao entrar, sua distância e seu pai ficam definidos;
3. a fila contém uma fronteira de no máximo duas distâncias consecutivas;
4. ao retirar `u`, nenhum caminho com menos arestas até `u` permanece por descobrir.

Com lista de adjacência, cada vértice é enfileirado uma vez e cada aresta é
examinada uma vez (duas em não dirigido), portanto `Θ(V+E)` para percorrer todos
os componentes alcançáveis. O espaço é `O(V)`, além do grafo. O `sorted` do
exemplo adiciona custos; retire-o quando ordem não fizer parte do contrato.

O mapa `parent` é um certificado compacto. Para reconstruir caminho até `x`,
siga pais até a origem e inverta. Vértice ausente de `distance` é inalcançável,
não necessariamente inexistente.

## DFS: aprofundar e observar tempo estrutural

Busca em profundidade usa pilha explícita ou recursão. É adequada para percursos,
componentes, ciclos, ordenação por término e decomposições.

Uma DFS dirigida usa cores:

- branco: ainda não descoberto;
- cinza: descoberto e ainda na pilha ativa;
- preto: todos os seus descendentes foram concluídos.

Encontrar aresta para nó cinza revela ciclo dirigido. Aresta para nó preto não
prova ciclo. Em grafo não dirigido, a aresta de volta ao pai deve ser ignorada,
ou toda aresta pareceria ciclo.

Recursão expressa naturalmente entrada/saída, mas uma cadeia profunda pode
estourar a pilha. Para preservar exatamente o comportamento de pós-ordem de forma
iterativa, a pilha precisa guardar também estado do iterador ou eventos de entrada
e saída; simplesmente empilhar vizinhos não é equivalente em todos os algoritmos.

## Ordenação topológica e ciclo

Uma ordem topológica de um grafo dirigido posiciona `u` antes de `v` para toda
aresta `u -> v`. Ela existe se, e somente se, o grafo é um DAG. Pode haver muitas
ordens válidas.

O algoritmo de Kahn:

```text
calcule indegree[v] para todo v
coloque todo v com indegree zero em disponiveis

enquanto disponiveis não estiver vazio:
    u = retire segundo a política de desempate
    emita u
    para cada aresta u -> v:
        indegree[v] -= 1
        se indegree[v] == 0:
            adicione v

se emitidos != V:
    existe ciclo
```

Invariante: `indegree[v]` representa arestas provenientes de vértices ainda não
emitidos; `disponiveis` contém exatamente os não emitidos com valor zero. Uma fila
resulta `Θ(V+E)`; heap acrescenta `O(V log V)` e fornece menor chave em cada
empate. O prefixo emitido é sempre válido.

Validar uma ordem é simples e independente do algoritmo: construa `position[v]`
e verifique `position[u] < position[v]` para cada aresta. Isso custa `Θ(V+E)` e
funciona como certificado positivo. Quando existe ciclo, devolver um caminho
como `A -> B -> C -> A` é diagnóstico melhor que apenas “falhou”; DFS com pais
pode reconstruí-lo.

## Componentes e conectividade

Em grafo não dirigido, iniciar BFS/DFS em cada vértice ainda não visitado separa
componentes conexos em `Θ(V+E)`. Em grafo dirigido, “conectado” é ambíguo:

- **fracamente conectado:** conectado ao ignorar direções;
- **fortemente conectado:** todo par alcança um ao outro respeitando direção.

Tarjan encontra componentes fortemente conexos (SCCs) em uma DFS usando índice,
`lowlink` e pilha; Kosaraju usa ordem de término e grafo transposto. Ambos são
`Θ(V+E)`. Contraindo cada SCC em um supervértice, obtém-se sempre um DAG.

No planejador, uma SCC com mais de um vértice, ou uma SCC unitária com laço,
é um grupo circular. Relatar a SCC inteira ajuda a corrigir várias dependências,
enquanto Kahn apenas indica que algum ciclo impediu a conclusão.

## Menores caminhos: escolha pelas pré-condições

### BFS

Use quando todas as arestas têm mesmo custo, ou quando a métrica é quantidade de
arestas. Para pesos apenas `0` ou `1`, 0–1 BFS usa deque e continua linear.

### Dijkstra

Mantém estimativas e extrai a menor distância provisória com heap. Requer pesos
**não negativos**. Quando `u` é extraído com a melhor estimativa vigente, sua
distância pode ser finalizada porque qualquer continuação acrescenta custo não
negativo. Uma aresta negativa destrói esse argumento.

Com lista e heap binário, custo usual `O((V+E) log V)`, simplificado para
`O(E log V)` em grafos alcançáveis. Bibliotecas sem `decrease-key` podem inserir
nova entrada e descartar a obsoleta ao sair; esquecer a verificação repete trabalho
ou processa resultado incorreto.

### Bellman–Ford

Relaxa todas as arestas `V-1` vezes: `O(VE)`. Aceita pesos negativos e uma rodada
adicional detecta ciclo negativo alcançável. Se tal ciclo pode reduzir o custo
indefinidamente em direção ao destino, não existe menor caminho finito.

### Floyd–Warshall

Calcula todos os pares por programação dinâmica em `Θ(V³)` tempo e `Θ(V²)`
espaço. É simples e útil para grafos menores/densos. Aceita arestas negativas,
mas ciclos negativos aparecem na diagonal e precisam ser tratados.

### A*

Prioriza `g(v)+h(v)`, custo conhecido mais estimativa ao objetivo. Uma heurística
admissível nunca superestima e preserva otimalidade em condições apropriadas;
consistência simplifica finalização sem reabrir nós. `h=0` reduz A* a Dijkstra.
Uma boa heurística explora menos estados; uma errada pode perder o melhor caminho.

| Situação | Algoritmo inicial | Condição crítica |
|---|---|---|
| custo uniforme | BFS | grafo não ponderado/equipesos |
| pesos 0/1 | 0–1 BFS | somente dois pesos |
| pesos não negativos | Dijkstra | nenhuma aresta negativa |
| pesos negativos | Bellman–Ford | tratar ciclo negativo |
| todos os pares, `V` pequeno | Floyd–Warshall | `V³` e `V²` cabem |
| objetivo e boa heurística | A* | admissibilidade/consistência declarada |

## Árvore geradora mínima não é menor caminho

Em grafo não dirigido, ponderado e conectado, uma MST conecta todos os vértices
minimizando a **soma das arestas escolhidas**. Ela não minimiza a distância de uma
origem a cada destino.

- Kruskal ordena arestas e adiciona uma quando une componentes distintos. Union-
  find com compressão de caminho e união por rank detecta componentes quase em
  tempo constante amortizado. Custo dominado por `O(E log E)`.
- Prim cresce uma fronteira a partir de um vértice, usando heap. Com lista e heap,
  custa `O(E log V)`.

Se o grafo é desconectado, ambos produzem uma floresta geradora mínima, salvo se
o contrato exigir erro. Pesos iguais podem gerar várias MSTs; determinismo exige
desempate.

## Escala, memória e grafos externos

`O(V+E)` pode ser enorme. Objetos e mapas por aresta custam muito mais que pares
compactos; CSR melhora localidade, mas perde mutabilidade. Em grafos que não cabem
na RAM, particionamento, processamento por blocos e bancos especializados mudam o
modelo de custo para I/O. Distribuir um percurso introduz mensagens, sincronização
e partições desequilibradas por vértices de alto grau.

Também proteja a fronteira: entrada com milhões de arestas duplicadas pode consumir
memória antes da validação; profundidade adversa derruba DFS recursiva; pesos podem
transbordar inteiros fixos. Limites e representações fazem parte da correção.

## Aplicação no Dependency Planner

Para tarefas `modelo`, `api`, `web`, `entrega`:

```text
modelo -> api -> entrega
       \-> web -/
```

Uma representação adequada é:

```python
adjacency = {
    "modelo": {"api", "web"},
    "api": {"entrega"},
    "web": {"entrega"},
    "entrega": set(),
}
indegree = {"modelo": 0, "api": 1, "web": 1, "entrega": 2}
```

Invariante cruzada: a soma dos graus de entrada é `E` e equivale à soma dos
tamanhos das listas. O algoritmo em [exemplos](exemplos/) usa Kahn e heap. Depois
de `modelo`, `api` e `web` ficam disponíveis; `entrega` somente após ambos.

Para caminho crítico com duração nos **vértices**, processe a ordem topológica e
calcule, para cada tarefa, o maior término de suas predecessoras mais sua duração.
Isso é diferente de Dijkstra: procura caminho de maior soma em DAG, problema
resolvido em `Θ(V+E)` após a ordem. Em grafo geral, maior caminho simples é um
problema muito mais difícil; a precondição DAG é essencial.

Valide qualquer ordem produzida construindo posições e examinando todas as arestas.
Valide os lotes confirmando que nenhuma aresta liga tarefas no mesmo lote ou em
direção contrária. Essas propriedades são mais fortes que comparar uma lista fixa,
pois várias ordens podem ser corretas.

## Falhas comuns e diagnóstico

### Inverter a aresta

**Sintoma:** dependente aparece antes da dependência.  
**Diagnóstico:** escreva a frase da seta e teste o grafo mínimo `A -> B`; confira
graus (`A=0`, `B=1` na convenção deste curso).

### Marcar visitado tarde demais na BFS

Marcar somente ao retirar permite enfileirar o mesmo vértice por vários pais,
aumentando memória e confundindo pais. Marque ao descobrir/enfileirar.

### Reutilizar detecção de ciclo entre classes

Cores de DFS dirigida e regra “vizinho visitado diferente do pai” para grafo não
dirigido não são intercambiáveis. Declare a classe no contrato.

### Aplicar algoritmo apesar da precondição

Antes de Dijkstra, valide ou garanta pesos não negativos. Antes de topológica,
trate a possibilidade de ciclo. Um resultado plausível não é certificado.

### Usar matriz para grafo esparso grande

**Sintoma:** memória cresce quadraticamente antes do percurso.  
**Diagnóstico:** estime `V²` bytes/bits e compare com `V+E`; meça densidade
`E / V(V-1)` conforme direção.

### Confundir tarefa inalcançável com inexistente

Mantenha conjunto de vértices separado do mapa de visitados/distâncias. Ausência
no primeiro é erro de identificação; ausência no segundo é resultado do percurso.

## Exercícios por nível

### Nível 1 — representar e percorrer

1. Modele estações e conexões; declare sentido e significado do peso.
2. Implemente BFS e DFS iterativas com ordem de vizinhos determinística.
3. Reconstrua um caminho usando pais e trate destino inalcançável.

**Aceite:** a representação preserva todos os vértices, inclusive isolados;
cada percurso visita alcançáveis uma vez e possui testes de vazio, ciclo e componentes.

### Nível 2 — validar propriedades

1. Detecte ciclo dirigido com cores e devolva um caminho fechado.
2. Implemente Kahn com fila e heap; valide cada ordem por todas as arestas.
3. Compare matriz, lista e CSR para grafos esparsos e densos.
4. Implemente Dijkstra e rejeite peso negativo antes do processamento.

**Aceite:** ciclo de tamanho um e ciclo em componente desconectado são encontrados;
resultados de caminho incluem distância e predecessores verificáveis.

### Nível 3 — selecionar e defender

1. Implemente SCC e use-a para relatar todos os grupos circulares do planejador.
2. Compare Bellman–Ford e Dijkstra em casos válidos e em aresta negativa.
3. Implemente Kruskal e demonstre com contraexemplo que MST não é árvore de
   menores caminhos.
4. Gere cadeias, leques e DAGs aleatórios; meça `V`, `E`, tempo e pico de memória.

**Aceite:** cada algoritmo registra pré-condições e as valida ou as recebe como
garantia; benchmarks confrontam previsão assintótica e dados observados.

## Checklist de domínio

- [ ] Escrevo a semântica da aresta antes de calcular graus.
- [ ] Escolho representação por densidade, mutação e operações dominantes.
- [ ] Explico as invariantes e o custo `Θ(V+E)` de BFS/DFS com lista.
- [ ] Distingo ciclo dirigido do não dirigido.
- [ ] Produzo e valido uma ordem topológica; reconheço múltiplas respostas.
- [ ] Distingo alcançabilidade, componente conexo e SCC.
- [ ] Escolho menor caminho a partir dos pesos e da consulta.
- [ ] Sei por que Dijkstra rejeita pesos negativos.
- [ ] Distingo MST, menor caminho e caminho crítico em DAG.
- [ ] Analiso o Dependency Planner em `V`, `E`, memória e desempate.

Grafos recompensam precisão. A maior parte dos erros não nasce de uma linha do
algoritmo, mas de uma seta cujo significado ou precondição nunca foi declarado.
