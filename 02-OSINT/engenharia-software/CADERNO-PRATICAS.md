# Caderno de práticas — algoritmos e engenharia de software

Este caderno contém experimentos menores que os laboratórios. Faça-os em uma
branch ou diretório descartável, com entradas sintéticas. O valor está em prever,
medir e explicar; copiar uma implementação pronta elimina justamente a etapa de
raciocínio que o exercício pretende desenvolver.

## Formato de registro

```text
pergunta:
contrato/hipótese:
casos escolhidos:
implementação ou comando:
resultado essencial:
explicação e custo:
limite/contraexemplo:
teste permanente:
```

Se a previsão estiver errada, preserve-a. A diferença entre modelo mental e
resultado observado é uma pista concreta do que precisa ser revisto.

## Bloco A — problema, contrato e custo

### 1. Transforme adjetivos em cenários

Reescreva “o planejador deve ser rápido, robusto e fácil de usar” como cinco
cenários mensuráveis. Cada cenário deve indicar entrada/carga, ambiente,
resposta, medida e limite. Separe requisito funcional de atributo de qualidade.

### 2. Tabela de decisão

Modele os resultados para arquivo ausente, JSON inválido, campo ausente, ID
duplicado, referência desconhecida, ciclo e sucesso. Defina status, canal de
saída e se existe resultado parcial. Procure combinações ainda ambíguas.

### 3. Invariantes executáveis

Escreva `is_topological_order` sem reutilizar o algoritmo que produz a ordem.
Alimente-o com uma ordem válida e cinco inválidas. Um oráculo que repete a
mesma implementação tende a repetir o mesmo defeito.

### 4. Conte operações

Instrumente busca linear e binária com um contador de comparações. Use
entradas vazia, melhor caso, pior caso e ausente. Compare contagem com tempo e
explique por que tempo de parede não é a definição de complexidade.

### 5. Crescimento de memória

Compare lista de adjacência e matriz para grafos com mesmo `V` e densidades
diferentes. Inclua capacidade ociosa, objetos/ponteiros e limite do método de
medição; não conte apenas os valores armazenados.

## Bloco B — estruturas e representação

### 6. Pilha com contrato

Implemente `push`, `pop`, `peek` e `size`. Decida se `pop` vazio retorna opção
ou erro. Teste transições, não apenas uma sequência feliz.

### 7. Fila circular

Use capacidade quatro e desenhe os índices após cada operação até ocorrer
wrap-around. Diferencie cheio de vazio sem depender apenas de `head == tail`.

### 8. LRU em `O(1)` esperado

Combine mapa e lista duplamente encadeada. Escreva invariantes entre ambos e
teste atualização de chave existente, capacidade um e eviction. Explique a
hipótese por trás do custo do hash.

### 9. BST degenerada

Insira chaves ordenadas e aleatórias numa árvore binária simples. Meça altura,
não apenas tempo. Compare com a garantia que uma árvore balanceada ofereceria.

### 10. Heap parcial

Mantenha os `k` maiores valores de um fluxo com min-heap de tamanho `k`.
Compare com ordenar tudo para `k=10` e `n` crescente. Registre custo e memória.

### 11. Trie e Unicode

Defina se prefixo opera sobre bytes, code points ou unidades da linguagem.
Teste acentos, normalização e palavra que é prefixo de outra. Documente o
contrato; não “corrija” texto silenciosamente.

## Bloco C — grafos e algoritmos

### 12. BFS versus DFS

Execute ambos no mesmo grafo com ordem de vizinhos definida. Compare caminho
não ponderado, memória de fronteira e profundidade. Marque visitado ao inserir
e depois ao remover para observar a duplicação de trabalho.

### 13. Ordem topológica independente

Implemente Kahn e DFS com cores. Compare detecção de ciclo, profundidade de
pilha e determinismo. Valide resultados por propriedade, não por igualdade
entre as duas ordens.

### 14. Dijkstra e a pré-condição esquecida

Construa um grafo pequeno com aresta negativa em que Dijkstra produz decisão
incorreta. Rejeite peso negativo na borda ou escolha algoritmo adequado.

### 15. Estabilidade observável

Ordene objetos primeiro por ID e depois, com algoritmo estável, por grupo.
Mostre a ordem secundária preservada. Troque por implementação instável e crie
um teste que exponha a diferença.

### 16. `lower_bound`

Mantenha o invariante de dois intervalos e devolva a primeira posição válida.
Teste todas as fronteiras e duplicatas. Evite `mid = (low + high) / 2` em tipos
onde a soma pode transbordar.

## Bloco D — recursão, DP e escolha gulosa

### 17. Recursão para iteração

Converta DFS recursiva para pilha explícita preservando a ordem. Liste o estado
antes implícito em cada frame: vértice, próximo vizinho e caminho atual.

### 18. Backtracking com desfazer

Gere combinações de soma limitada. Após retornar, prove que o estado voltou ao
valor anterior. Uma asserção interna ajuda a detectar `undo` incompleto.

### 19. Memoização observável

Conte chamadas de Fibonacci ingênuo e memoizado. Depois use um problema em que
nem todo estado é alcançado e compare memoização com tabulação.

### 20. Reconstrução da resposta

Não retorne apenas o valor de uma LCS ou caminho crítico. Guarde decisões,
reconstrua uma solução e verifique se ela realmente satisfaz o problema.

### 21. Contraexemplo guloso

Para mochila 0/1, encontre instâncias que derrotam maior valor, menor peso e
melhor razão. Explique por que um exemplo basta para refutar correção geral.

## Bloco E — tipos, módulos e padrões

### 22. Estado impossível

Modele resultado de planejamento como união `Success | InvalidInput | Cycle`
ou equivalente. Compare com dois booleanos e campos opcionais que permitem
combinações contraditórias.

### 23. Mutabilidade atravessando fronteira

Retorne uma coleção interna e mostre como o consumidor viola a invariante.
Corrija com cópia, visão imutável ou iterator. Compare custo e ownership.

### 24. Teste de contrato de porta

Rode a mesma suíte contra repositório em memória e JSON. O contrato cobre
semântica observável, não métodos privados ou quantidade de chamadas.

### 25. Strategy sem cerimônia

Injete o critério de desempate como função, delegate ou interface. Justifique a
forma idiomática em duas linguagens. Não crie factory se a composição é fixa.

### 26. Adapter rigoroso

Converta CSV ou YAML ao modelo. Rejeite coluna desconhecida, valor ausente,
encoding inválido e excesso de tamanho. O núcleo nunca deve receber linhas
semi-parseadas.

## Bloco F — evolução, arquitetura e qualidade

### 27. Characterization test

Capture saída e status de um script legado antes de extrair uma função. Faça
uma mudança mecânica por commit e mantenha a rede verde.

### 28. ADR honesto

Registre uma decisão entre lista e matriz de adjacência. Inclua densidade,
limites, alternativa rejeitada, consequência negativa e gatilho de revisão.

### 29. Mate a mutação

Remova validação, inverta comparação, ignore aresta e quebre desempate, uma
por vez. Para cada sobrevivente, adicione teste que expresse a regra ausente.

### 30. Pull request operável

Escreva problema, escopo, risco, testes, migração, rollback e evidência de uma
mudança. Peça revisão sobre invariante e trade-off específicos, não apenas
“opiniões?”.

### 31. Runbook de resultado errado

Simule um fixture que gera ordem inválida. Registre versão, entrada mínima,
primeira invariante quebrada, causa, correção e teste de regressão.

### 32. Defesa em cinco minutos

Explique o projeto sem slides: contrato, representação, algoritmo, custo,
fronteiras, erro mais perigoso e alternativa rejeitada. Grave apenas se todos
os participantes consentirem; caso contrário, use uma pessoa revisora.

## Critério de aproveitamento

Uma prática está concluída quando tem previsão anterior ao experimento,
evidência reproduzível, explicação causal e um teste ou decisão permanente. A
quantidade de linhas produzidas não é critério de qualidade.

