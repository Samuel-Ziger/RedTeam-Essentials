# Gabarito orientativo — Engenharia de Software

> **Regra de uso:** tente cada exercício e registre sua primeira solução antes de consultar este documento. O objetivo deste gabarito é ensinar a avaliar raciocínio, não fornecer texto para copiar. Uma resposta diferente pode ser melhor se cumprir o contrato, preservar as invariantes, declarar hipóteses e apresentar evidência reproduzível.

Este documento acompanha os capítulos [00](00-como-pensar-problemas.md) a [16](16-projetos-avaliacao.md). Ele é autocontido o suficiente para corrigir os exercícios, mas pressupõe que você estudou o capítulo correspondente. Para cada entrega, separe cinco coisas:

1. **contrato:** entradas, saídas, erros, limites e efeitos;
2. **invariantes:** fatos que precisam continuar verdadeiros durante e depois da operação;
3. **correção:** argumento de por que o resultado satisfaz o contrato e por que o processo termina;
4. **custo:** parâmetros relevantes, tempo, memória e hipóteses do modelo;
5. **evidência:** testes, medidas, diagramas ou histórico que outra pessoa consegue reproduzir.

Use a notação do curso: V é a quantidade de vértices, E a quantidade de arestas, n o tamanho de uma sequência e k uma quantidade explicitamente definida no contexto. Big O é limite assintótico, não cronômetro nem sinônimo de pior caso. Custos esperados de hash, custos amortizados e limites pseudopolinomiais devem ser identificados como tais.

---

## 00 — Como pensar problemas antes de programar

### Nível 1 — tornar o pedido verificável

Uma boa reescrita de “o programa deve ser rápido” contém carga, ambiente, medida e limiar. Exemplo orientativo: “para documentos válidos com até 100 mil tarefas e 500 mil dependências, no ambiente de referência, 95% das execuções devem terminar em até 2 s e usar no máximo 512 MiB”. O número não é universal; ele precisa vir de uma necessidade ou ser marcado como hipótese a validar. “Fácil de usar” pode virar “uma pessoa que conhece a CLI conclui o fluxo válido com um comando, recebe ajuda para parâmetro ausente e distingue erro de entrada de falha de I/O pelos códigos de saída”.

Uma classificação plausível de regras do Planner é:

| Regra | Classe principal | Por quê |
|---|---|---|
| ID não vazio | pré-condição/invariante local | um item válido nunca existe sem identidade |
| duração inteira positiva | pré-condição/invariante local | protege o domínio e o cálculo |
| IDs únicos | invariante global | depende do conjunto completo |
| dependência existente | invariante global | exige índice de todos os itens |
| ausência de autoaresta | pré-condição local | pode ser rejeitada ao construir a tarefa |
| ausência de ciclo | pré-condição global | ordem topológica só existe para DAG |
| cada tarefa aparece uma vez | pós-condição | propriedade do plano produzido |
| dependência precede dependente | pós-condição | define correção topológica |
| menor ID desempata disponíveis | pós-condição/política | torna a saída determinística |
| limite de memória/latência | atributo de qualidade | mede comportamento sob cenário |

Outras classificações são defensáveis quando o proprietário da regra é explicado. Por exemplo, a aplicação pode aceitar objetos ainda não validados e transformar “duração positiva” em pré-condição da operação de planejamento.

Para um validador de parênteses, o contrato mínimo é: recebe uma sequência finita; decide se aberturas e fechamentos estão corretamente aninhados; declara se ignora outros caracteres; não altera a entrada. Erros de tipo são separados de resultado falso. A invariante do laço é: a pilha contém exatamente as aberturas ainda não fechadas do prefixo já lido, na ordem em que precisam ser fechadas. Um fechamento exige pilha não vazia e topo correspondente; no final, a pilha deve estar vazia. Cada caractere é visitado uma vez: tempo Θ(n), espaço O(n), atingido por n aberturas.

**Aceite:** as frases permitem que outra pessoa crie casos positivo, negativo e de fronteira sem perguntar o significado; os termos “pré”, “pós” e “invariante” não são usados como sinônimos.

### Nível 2 — especificar e decompor

No encurtador de URL, uma resposta suficiente define ao menos: URL de destino, alias opcional, normalização, limite de tamanho, unicidade do alias, expiração, resultado de criação repetida e política de redirecionamento. Cinco exemplos úteis são criação automática, alias escolhido disponível, conflito, URL inválida e consulta expirada. Invariantes: um alias ativo resolve para no máximo um destino; a expiração não antecede a criação; um identificador emitido nunca é vazio. Segurança e abuso entram como limites de entrada, esquema permitido e proteção contra destinos proibidos conforme o contexto. Não é correto declarar “URL válida” sem dizer qual parser ou regra decide isso.

Para a opção de alvo do Planner, a interpretação mais conservadora é planejar o fecho transitivo das dependências do alvo, não todos os itens e não seus dependentes. Pseudocódigo orientativo:

    exigir que alvo exista
    pendentes = [alvo]
    selecionadas = conjunto vazio
    enquanto pendentes não vazio:
        atual = retirar
        se atual ainda não foi selecionado:
            adicionar atual
            adicionar todas as dependências de atual a pendentes
    construir subgrafo induzido por selecionadas
    ordenar topologicamente com a mesma política de desempate

Invariantes do laço: todo ID em selecionadas é o alvo ou uma dependência alcançável dele; todo caminho ainda não explorado começa em pendentes; nenhum ID precisa ser expandido duas vezes. O conjunto garante término em no máximo V expansões. Construção e percurso custam O(V+E) no pior caso alcançável; a ordenação com heap custa O(E+V log V). A opção precisa definir o comportamento para alvo ausente, ciclo no subgrafo e dependências fora do limite carregado.

No conversor CSV para relatório, separe: leitura de bytes e encoding; parsing CSV e validação de cabeçalho; tradução para objetos do domínio; cálculo puro; formatação; gravação/publicação. Leitura e gravação são efeitos. Validação e cálculo podem ser funções puras sobre valores. O parser conhece aspas e colunas; o domínio conhece tarefas e dependências; o apresentador conhece o formato final. Essa decomposição permite testar regra sem arquivo e integração do parser com arquivo temporário real.

**Aceite:** cada responsabilidade tem entrada/saída nomeada; efeitos e categorias de erro não atravessam o núcleo como dicionários ou mensagens soltas.

### Nível 3 — decidir sob ambiguidade

Para remover uma tarefa, duas especificações coerentes são:

- **rejeição:** a remoção falha quando existem dependentes; preserva a intenção explícita de cada relação e exige que o usuário trate os dependentes primeiro;
- **cascata:** remove a tarefa e um conjunto definido de dependentes alcançáveis; reduz trabalho manual, mas pode apagar muito mais do que o pedido aparente.

Uma terceira política possível remove apenas as arestas e mantém dependentes, mas muda a semântica do plano e não deve ser chamada de cascata. A matriz de decisão deve incluir volume, reversibilidade, expectativa do usuário, auditoria, atomicidade, concorrência e custo. Uma escolha profissional registra não objetivos e exige confirmação ou dry-run quando o impacto pode ser amplo.

A prova de correção da opção escolhida deve cobrir: o estado final contém exatamente os itens previstos; nenhuma referência aponta para item inexistente; IDs continuam únicos; a operação é atômica ou define estado parcial; o algoritmo termina porque cada vértice é visitado no máximo uma vez. Na cascata, BFS/DFS sobre dependentes custa O(V+E) no subgrafo alcançável e usa O(V) de memória. Na rejeição, consultar um índice reverso custa O(grau de dependentes); sem índice pode custar O(V+E).

Testes metamórficos adequados: permutar a ordem do documento não muda o conjunto removido; renomear IDs por uma bijeção e aplicar a mesma remoção preserva a estrutura; adicionar componente desconectado não altera o resultado; repetir uma remoção pode ser ausência idempotente ou erro estável conforme contrato. Estresse deve incluir cadeia profunda, leque amplo, entrada máxima e tentativa de cascata acima do limite.

**Critério de domínio:** a decisão é aceitável quando premissas, perdas possíveis, complexidade, rollback e observações do usuário estão explícitos. “É mais simples de implementar” não basta.

---

## 01 — Complexidade, memória e medição

### Nível 1 — derivar, não decorar

Na busca linear, o melhor caso é Θ(1) quando o primeiro item corresponde; o pior é Θ(n) quando está ausente ou no final. O caso médio depende de uma distribuição, por exemplo posição uniforme entre itens presentes; sem ela, não há média única. O espaço auxiliar é Θ(1), desconsiderando a entrada.

Copiar uma matriz retangular n por m exige visitar e produzir nm elementos: tempo Θ(nm) e memória auxiliar Θ(nm) se a cópia for independente. Uma visão ou compartilhamento estrutural pode usar Θ(1), mas muda ownership, mutabilidade e vida útil; não é a mesma operação.

No laço em que i dobra até alcançar n, a quantidade de iterações é ⌈log₂ n⌉, portanto Θ(log n), assumindo aritmética constante. No laço triangular que executa i passos para cada i de 1 a n, a soma é n(n+1)/2, portanto Θ(n²). A resposta precisa indicar o que o corpo custa; uma operação interna não constante multiplica o resultado.

Dizer “este algoritmo é O(n²)” não significa que seu pior caso é exatamente quadrático. Pode ser linear e ainda pertencer a O(n²); pode ter melhor e pior casos diferentes. Para um limite justo, informe Θ quando houver limites superior e inferior coincidentes e separe a classe de entrada.

**Aceite:** cada fórmula nomeia tamanho e operação contada; melhor/pior/médio não são confundidos com O/Ω/Θ.

### Nível 2 — comparar alternativas

Para remover duplicatas preservando a primeira ocorrência:

    resultado = []
    vistos = conjunto vazio
    para item na entrada:
        se item não está em vistos:
            adicionar item a vistos
            anexar item ao resultado

Com hash bem distribuído, tempo esperado O(n) e espaço O(n). Dois laços que procuram no resultado custam Θ(n²) no pior caso e O(n) de espaço para a saída. O conjunto exige hash coerente com igualdade e pode sofrer pior caso O(n) por operação; a hipótese deve aparecer.

No vetor dinâmico que dobra capacidade, uma sequência de n inserções copia aproximadamente 1 + 2 + 4 + ... < 2n elementos. Assim, o custo total de realocações é O(n), e o append custa O(1) amortizado. O pior custo de uma inserção individual continua Θ(n); há também pico temporário entre armazenamento velho e novo.

Para V=10.000 e E=30.000, uma matriz booleana conceitual tem V² = 100 milhões de células. Com um byte seriam cerca de 100 MB; com booleanos empacotados, cerca de 12,5 MB; com objetos ou linhas, muito mais. Uma lista de adjacência armazena V cabeçalhos e E destinos, mas mapas, objetos e ponteiros podem dominar. A resposta profissional fornece uma estimativa inferior e uma medida na linguagem, deixando claro se conta apenas payload ou o heap inteiro.

No benchmark lista versus conjunto, meça separadamente construção e consultas. Use pelo menos cinco tamanhos, aquecimento, várias repetições, relógio monotônico, dados determinísticos e resultados consumidos para evitar eliminação. Registre mediana e dispersão, versão do runtime e distribuição de acertos. O conjunto tende a vencer muitas consultas; para uma busca única, construir o índice pode não se pagar.

### Nível 3 — instrumentar o Planner

Para Kahn com min-heap, conte: inserções e remoções do heap; comparações; arestas visitadas; pico de disponíveis; bytes aproximados de adjacência, graus e saída. Em uma cadeia, o heap tem tamanho máximo um: embora o limite geral seja O(V log V), o custo observado de prioridade se aproxima de linear. Em um leque, muitos vértices tornam-se disponíveis juntos e o heap evidencia log V. O percurso de arestas continua Θ(E).

Com FIFO, o algoritmo custa Θ(V+E), mas a saída depende da ordem de descoberta/inserção. Com heap, custa O(E+V log V) e sempre escolhe o menor ID disponível. Ambos podem produzir ordem topológica correta; somente o segundo satisfaz o desempate ordinal. O trade-off é custo adicional por uma garantia externa.

Pico de memória precisa incluir documento parseado e objetos de domínio coexistindo com índices. Uma medição que começa depois do parse omite frequentemente o maior pico. Declare fases: bytes do arquivo, árvore JSON, WorkItems, adjacência, graus, heap e resultado; meça retenção e liberação entre elas.

Ao dobrar V mantendo grau médio constante, E também dobra. Prevê-se tempo quase dobrado para FIFO e aproximadamente um pouco mais de duas vezes para heap, devido ao log V e constantes. O resultado real pode ser afetado por cache, GC, alocação e aquecimento. Compare razão observada à hipótese; não “prove Big O” por cinco pontos.

**Critério de domínio:** relatório reproduzível, contadores coerentes com o algoritmo e explicação de desvios valem mais do que uma curva visualmente bonita.

---

## 02 — Estruturas lineares e tabelas hash

### Nível 1 — representar invariantes

Uma pilha sobre vetor mantém os elementos válidos no prefixo de comprimento size. Push acrescenta ao fim; pop rejeita vazio ou retorna um resultado discriminado, remove o último e reduz size. Não use um valor sentinela que também possa ser dado válido. Cada operação é O(1) amortizada; o pior push pode realocar em Θ(n).

Para a fila circular de capacidade quatro, uma representação não ambígua mantém head e size; tail é calculado por (head + size) módulo capacidade. Desenhar duas voltas deve mostrar índices físicos sendo reutilizados sem mudar a ordem lógica. Invariantes: 0 ≤ size ≤ capacity; head sempre pertence ao array; exatamente size posições consecutivas no anel são válidas. Casos obrigatórios: capacidade um, vazio, cheio, wrap-around e transições 0→1 e 1→0.

Mil inteiros de 32 bits ocupam 4.000 bytes de payload contíguo. Em lista duplamente ligada, cada nó precisa de inteiro, dois ponteiros, alinhamento e possivelmente metadados do alocador. Em máquina de 64 bits, um nó pode ter ao menos 24 bytes antes do overhead, isto é, pelo menos 24.000 bytes mais fragmentação. O valor exato depende de ABI, runtime e representação; meça, não trate essa conta como universal.

### Nível 2 — compor estruturas

Um deque circular expansível copia os elementos em ordem lógica para um novo array quando cheio, reposiciona head em zero e cresce geometricamente. Todas as operações nas pontas são O(1) amortizadas; a expansão individual é Θ(n). Teste por propriedade comparando a uma coleção de referência após sequências aleatórias.

No desfazer/refazer, duas pilhas representam ações aplicadas e desfeitas. Undo retira da primeira, aplica a inversa e põe na segunda; redo faz o oposto. Uma nova ação após undo limpa a pilha de refazer, pois a linha do tempo anterior deixou de ser continuação válida. Se uma ação falha no meio, o contrato deve impedir que pilhas e estado de negócio discordem.

LRU combina mapa chave→nó e lista duplamente ligada. Invariantes: mapa e lista contêm exatamente as mesmas chaves; cada chave aparece uma vez; cabeça é mais recente; cauda é menos recente; tamanho não excede capacidade; elos são simétricos. Get e put esperados O(1). Evicção remove a cauda das duas estruturas. Capacidade zero precisa ser rejeitada ou ter semântica explícita.

### Nível 3 — medir e defender

No comparativo vetor/lista, separe inserção com posição já conhecida da busca dessa posição. Conte alocações e bytes, além do tempo. A lista pode ganhar em religação local, mas perder a varredura por indireção e cache; dados pequenos frequentemente favorecem vetor.

Uma tabela hash educacional por encadeamento precisa: array de baldes; índice derivado do hash; busca por igualdade dentro do balde; fator de carga; resize geométrico com rehash; atualização sem aumentar size; remoção; validação de hash/igualdade. Teste chaves deliberadamente conflitantes e confirme que todas sobrevivem ao resize. Tempo esperado O(1), pior O(n), espaço O(n + capacidade).

Trocar conjuntos de dependências do Planner por listas não deve mudar o resultado em entradas sem duplicatas, mas torna detecção de duplicata O(grau) e pode aceitar/processar a mesma aresta várias vezes se a validação falhar. Gere documentos com duplicatas crescentes, conte comparações e memória e reverta a experiência. A conclusão deve separar “a lista usa menos overhead em graus minúsculos” de “o conjunto protege unicidade com custo esperado constante”.

**Evidência mínima:** testes das transições de estado, propriedades contra referência, validação explícita das invariantes compostas e medição com ambiente identificado.

---

## 03 — Árvores, heaps e tries

### Nível 1 — construir e validar

Uma BST simples mantém, para cada nó, chaves menores à esquerda e maiores à direita segundo um comparador total. Duplicatas podem ser rejeitadas, contadas no nó ou posicionadas por regra estável; a política deve aparecer nos testes. Busca e inserção custam Θ(h), onde h é a altura. O percurso em ordem deve produzir chaves ordenadas e o validador deve verificar limites herdados, não apenas pai e filho imediatos.

Inserir 1, 2, ..., n numa BST não balanceada cria altura n−1. Registrar a altura em cada passo expõe crescimento linear e operações totais Θ(n²). Não conclua que toda BST é O(log n); isso exige balanceamento ou hipótese sobre a entrada.

Um min-heap em vetor preserva forma completa e pai ≤ filhos. Insert acrescenta e sobe; extract-min troca pela última posição, reduz o tamanho e desce pelo menor filho. Valide a propriedade em todos os índices após cada operação em testes. Topo é Θ(1); inserção/remoção O(log n); busca arbitrária O(n).

### Nível 2 — ampliar sem perder contrato

Na remoção da BST: folha é desligada; nó com um filho é substituído por ele; nó com dois filhos recebe o par chave/valor do sucessor e remove esse sucessor. Atualize raiz, pais e metadados quando existirem. O teste deve remover raiz em todos os três casos e confirmar ordem, tamanho e política de duplicatas.

Construir heap por n inserções custa O(n log n). Heapify bottom-up custa O(n), pois a maioria dos nós está perto das folhas e desce pouco. Conte comparações em entradas crescentes, decrescentes e aleatórias; uma única medição não substitui a soma por alturas.

Uma trie precisa distinguir “prefixo existe” de “palavra termina aqui”. Remover uma palavra desmarca o final e poda somente nós sem filhos que não encerram outra palavra. Autocomplete custa O(p + saída) no modelo de acesso aos filhos, em que p é o tamanho do prefixo. Defina bytes, pontos de código ou grafemas e a normalização. Um limite r de resultados exige ordem e política de corte.

No desenho de B-tree, declare o grau mínimo ou capacidade antes de fazer splits. Todos os nós não raiz respeitam ocupação, chaves separam intervalos e folhas ficam na mesma profundidade. Respostas com desenhos diferentes podem estar corretas se usam a mesma convenção de split consistentemente.

### Nível 3 — uso profissional

AVL exige fator de balanço em −1, 0 ou 1 e alturas corretas; rubro-negra exige cor, raiz/NIL pretos, ausência de vermelho-vermelho e mesma altura negra. Um validador independente recalcula propriedades após operações aleatórias comparadas a uma biblioteca. A implementação não recebe crédito apenas por produzir busca correta em poucos exemplos.

Ao comparar hash, árvore ordenada e trie para IDs, meça busca exata, intervalo/prefixo, memória, alocações e Unicode. Hash tende a consulta exata esperada O(1); árvore oferece faixa em O(log n + k); trie depende do comprimento da chave e pode consumir muito espaço. Não existe vencedora sem consulta dominante.

No Planner, FIFO mantém correção topológica, mas não o menor ID; árvore ordenada e heap satisfazem o desempate em O(log V). A árvore oferece remoção arbitrária e faixas não necessárias. Meça cadeia e leque e explique por que o heap expressa o contrato mínimo.

**Aceite:** validadores independentes, referência de biblioteca, altura/memória medidas e semântica de desempate explícita.

---

## 04 — Grafos: modelagem, percursos e caminhos

### Nível 1 — representar e percorrer

Para estações, uma modelagem aceitável diz se conexões são dirigidas e o que o peso significa: tempo, distância ou custo não são intercambiáveis. Inclua estações isoladas. Se toda conexão custa uma unidade, BFS fornece menor número de arestas; com pesos não negativos, Dijkstra; com negativos, outra estratégia e tratamento de ciclos negativos.

BFS usa fila e marca na descoberta, não na remoção. Invariante: cada vértice descoberto possui distância e pai; a fila contém fronteira de no máximo duas distâncias consecutivas. DFS iterativa usa pilha; para reproduzir pós-ordem, guarde estado do iterador/entrada e saída. Ambas custam Θ(V+E) com lista de adjacência e O(V) auxiliar, visitando todos os componentes quando um laço externo inicia novas raízes.

Um caminho é reconstruído seguindo parent do destino até a origem e invertendo. Destino fora do grafo é erro de identidade; dentro do grafo, mas ausente do mapa de pais, é inalcançável. O caminho deve começar na origem, terminar no destino e cada par adjacente deve ser uma aresta.

### Nível 2 — validar propriedades

Na detecção de ciclo dirigido, branco é não visitado, cinza está na pilha ativa e preto foi concluído. Aresta para cinza fecha um ciclo; guarde pais para devolver um caminho fechado. Teste autoaresta e ciclo em componente desconectado. A regra de ignorar o pai pertence a grafos não dirigidos e não pode ser transplantada.

Kahn com fila e heap deve produzir todos os V IDs e respeitar position[u] < position[v] em toda aresta. Se emite menos de V, há ciclo. Fila dá Θ(V+E); heap, O(E+V log V) com menor ID. Não compare apenas uma ordem fixa quando o contrato permite várias.

Matriz usa Θ(V²) espaço e examina V posições para vizinhos; lista usa Θ(V+E); CSR é compacto e favorece leitura, mas atualização pode exigir reconstrução. Gere grafos esparsos e densos e registre operação, memória e método. O ponto de cruzamento é empírico e dependente da representação.

Dijkstra precisa rejeitar peso negativo antes de prometer correção. Resultado contém distâncias e predecessores; valide que cada caminho soma a distância e que nenhuma aresta relaxável permanece. Heap sem decrease-key pode conter entradas obsoletas; descarte quando a distância retirada difere da atual.

### Nível 3 — selecionar e defender

Tarjan ou Kosaraju devolve SCCs em Θ(V+E). No Planner, SCC com mais de um vértice ou autoaresta representa circularidade. O relatório deve listar todos os grupos, não só afirmar que Kahn parou.

Bellman–Ford aceita pesos negativos em O(VE) e detecta ciclo negativo alcançável; Dijkstra é mais eficiente sob pesos não negativos. Um caso com aresta negativa que melhora caminho depois de um nó “finalizado” demonstra por que Dijkstra falha.

Kruskal/Prim minimizam a soma da rede; uma árvore de caminhos mínimos minimiza distâncias desde uma origem. Um triângulo ponderado ou grafo de quatro nós pode mostrar objetivos distintos. Verifique conexão, número de arestas e propriedade de corte; em grafo desconectado, declare erro ou floresta.

Cadeia, leque e DAG aleatória devem registrar V, E, tempo e pico. A soma dos graus de entrada precisa ser E. No Planner, caminho crítico em DAG é maior soma de durações em ordem topológica, não Dijkstra.

**Critério de domínio:** algoritmo escolhido a partir da classe do grafo, pré-condições validadas e resultado acompanhado de certificado verificável.

## 05 — Busca e ordenação

### Nível 1 — contratos e invariantes

Lower bound trabalha sobre intervalo semiaberto [lo, hi). A invariante forte é: todo índice menor que lo contém valor menor que o alvo; todo índice a partir de hi contém valor maior ou igual; a fronteira procurada está em [lo, hi]. Se values[mid] < target, descarte até mid inclusive; caso contrário, mantenha mid como candidato reduzindo hi. A variante hi−lo diminui estritamente. O retorno pertence a [0,n], inclusive n quando o alvo seria inserido no final. Upper bound troca a condição para localizar o primeiro valor estritamente maior. Teste vazio, um item, antes/depois de todos e blocos duplicados.

Insertion sort mantém o prefixo [0,i) ordenado e como permutação dos primeiros i itens originais. Ao deslocar apenas quando key < anterior, itens de chave igual não se ultrapassam e a ordenação é estável. Melhor caso Θ(n), pior Θ(n²), memória auxiliar Θ(1) na versão in-place.

O verificador de ordenação precisa testar três propriedades independentes:

1. cada par adjacente está em ordem;
2. a saída contém o mesmo multiconjunto da entrada;
3. para chaves iguais, IDs originais aparecem na mesma ordem.

Somente a primeira aceita algoritmos que perdem ou duplicam itens. Use identificadores únicos anexados aos valores para observar estabilidade.

### Nível 2 — comparar estratégias

Mergesort que devolve nova coleção divide, ordena e intercala. No merge, a saída contém exatamente os prefixos já consumidos, está ordenada e o menor restante está em uma das cabeças. Escolher a metade esquerda no empate preserva estabilidade. Tempo Θ(n log n) em todos os casos, buffer de pico usual Θ(n) e pilha O(log n); medir slices pode revelar cópias adicionais da linguagem.

Quicksort de três vias mantém regiões menores, iguais e maiores que o pivô. Ele lida bem com repetidos, mas uma política de pivô ruim ainda pode produzir profundidade linear. Registre tamanho das partições e profundidade em entradas ordenada, reversa, constante e aleatória. Resultado deve passar o mesmo oráculo de multiconjunto.

Para q consultas: varredura repetida custa O(qn); ordenar e usar busca custa O(n log n + q log n); conjunto custa construção O(n) e consulta esperada O(q), usando memória O(n). O benchmark deve separar construção de consulta e incluir atualizações, pois um índice precisa ser mantido ou reconstruído.

Para k maiores em fluxo, mantenha min-heap de no máximo k elementos: descarte menores que o topo e substitua quando necessário. Tempo O(n log k), espaço O(k). Defina empates e, se a saída final precisa estar ordenada, inclua O(k log k).

### Nível 3 — limites e sistema

A prova do limite inferior usa uma árvore de decisão: n elementos distintos admitem n! permutações; uma árvore binária de altura h tem no máximo 2^h folhas; portanto h ≥ log₂(n!) = Ω(n log n). Isso vale para algoritmos gerais baseados em comparação, não para chaves com estrutura limitada nem para instâncias parcialmente ordenadas sob algoritmo adaptativo.

Counting sort custa Θ(n+K) e memória Θ(K), em que K é o universo; radix custa Θ(d(n+b)), com d dígitos e base b. O experimento deve variar n e K ou d, não apenas n. Inclua memória e casos em que o universo esparso elimina a vantagem.

External merge sort respeita a quota: cria runs ordenadas que cabem em memória, grava temporários, faz merge k-way por heap e publica por rename atômico quando possível. Em falha, fecha e limpa temporários; nunca expõe saída parcial como final. Registre bytes de I/O e quantidade de passes.

No Planner, três versões demonstram o contrato: ordenar globalmente por ID pode violar dependências; Kahn sem desempate pode ser correto mas não determinístico; Kahn com heap respeita dependências e política ordinal. Um contraexemplo mínimo é z-modelo → a-api com b-docs isolada. A ordem alfabética começa por a-api e é inválida.

**Aceite:** invariantes e medida de término escritas, multiconjunto preservado, hipóteses de algoritmos não comparativos declaradas e publicação externa segura.

---

## 06 — Recursão e backtracking

### Básico — DFS recursiva e iterativa

As duas versões precisam visitar o mesmo conjunto, não necessariamente a mesma ordem. A recursiva mantém um frame por vértice no caminho; a iterativa deve guardar explicitamente o estado necessário. Para simples pré-ordem, empilhar vizinhos em ordem reversa pode reproduzir a visita recursiva. Para cores e pós-ordem, cada frame precisa incluir o próximo vizinho ou um evento de saída; marcar preto logo ao empilhar é erro.

Invariantes: visitado contém exatamente vértices já descobertos; nenhum vértice é expandido duas vezes; cada item na pilha representa trabalho ainda válido. Tempo Θ(V+E), memória O(V). A cadeia de 100 mil vértices deve funcionar iterativamente sem depender do limite da call stack. Vazio, desconectado e ciclo não podem provocar acesso inválido ou repetição infinita.

**Evidência:** teste compara conjuntos; mede profundidade/pico; documenta a ordem e mostra por que a versão iterativa termina.

### Intermediário — permutações únicas

Para valores ordenados, em cada nível ignore uma candidata igual à anterior que ainda não foi usada naquele mesmo nível. Um vetor used distingue posições; o prefixo atual contém posições distintas e representa exatamente as escolhas do caminho. Ao voltar, desmarque a posição e remova o último valor. Pular duplicatas entre níveis seria incorreto, pois impediria usar as duas ocorrências de 1 em [1,1,2].

Para [1,1,2], as únicas saídas são [1,1,2], [1,2,1] e [2,1,1]. Armazene snapshot/tupla ou produza com gerador; não devolva a mesma lista mutável três vezes. O custo inferior é proporcional à quantidade de resultados vezes n; no pior caso sem repetidos há n! resultados. Memória de estado é O(n), sem materializar toda a saída.

Contadores úteis: nós visitados, escolhas descartadas, profundidade e soluções. Chamar a eliminação de duplicatas de “poda” exige explicar que ramos equivalentes produziriam exatamente o mesmo conjunto de valores.

### Avançado — lote sob limite de duração

Somente tarefas atualmente disponíveis podem entrar; dependências são tratadas antes da seleção. O subproblema de escolher um subconjunto cuja soma não excede a capacidade e maximiza ocupação é uma mochila 0/1. Backtracking mantém índice, soma atual e escolhidas. Invariantes: soma é a soma exata das escolhidas; nenhuma tarefa aparece duas vezes; toda escolhida estava disponível; soma não excede o limite.

Podas seguras possíveis: interromper quando a soma excede a capacidade, pois durações são positivas; abandonar quando soma atual mais todas as durações restantes não supera a melhor conhecida; usar limite fracionário otimista se calculado corretamente. “Escolher menor primeiro” é heurística, não poda. Compare com força bruta em instâncias pequenas e preserve o menor contraexemplo de uma regra gulosa.

O pior caso continua O(2^n), profundidade O(n). Entrada grande precisa de limite de n, deadline/cancelamento ou algoritmo alternativo. Relate nós/podas/tempo, não somente latência final.

**Critério de domínio:** caso base, medida de progresso, restauração simétrica, prova de completude e prova individual de cada poda.

---

## 07 — Programação dinâmica e algoritmos gulosos

### Básico — troco por memoização e tabulação

Defina dp[v] como a menor quantidade de moedas positivas que forma exatamente v; dp[0]=0 e impossível é infinito. A transição considera 1 + dp[v−m] para toda moeda m≤v alcançável. Positividade garante v−m<v e ordem acíclica. Guarde a moeda escolhida para reconstrução; valide que a lista soma o total e tem comprimento dp[total].

Memoização calcula apenas estados alcançados, mas usa pilha e cache; tabulação percorre 0..total e evita recursão. Ambas têm limite O(total×M) e espaço O(total), onde M é a quantidade de moedas. É pseudopolinomial porque total pode ser enorme em relação ao número de bits. Rejeite moeda zero/negativa; total zero devolve lista vazia; impossível devolve ausência distinta de erro.

Se houver empate, qualquer solução ótima pode ser aceita ou uma política determinística deve ser declarada. Comparar listas exatas sem contrato de desempate cria teste frágil.

### Intermediário — LCS

Uma definição consistente é: dp[i][j] é o comprimento da maior subsequência comum entre os prefixos de tamanhos i e j. Bases dp[0][j]=dp[i][0]=0. Se os últimos elementos coincidem, dp[i][j]=1+dp[i−1][j−1]; senão, máximo entre dp[i−1][j] e dp[i][j−1]. Tempo e espaço Θ(nm).

Reconstrução caminha da célula final: em igualdade, emite o elemento e vai à diagonal; caso contrário, segue um vizinho de mesmo valor máximo. Empate precisa de política se a subsequência textual for determinística. A saída deve ser subsequência das duas entradas e ter comprimento ótimo.

Duas linhas reduzem o valor para O(min(n,m)) de memória, mas apagam decisões antigas; reconstruir exige armazenar predecessores, recomputar ou usar algoritmo como Hirschberg. A resposta correta declara essa perda, em vez de fingir reconstrução gratuita. Para texto, defina se a unidade é ponto de código ou grafema.

### Avançado — caminho crítico e contraponto guloso

Em uma DAG, finish[v] é duração[v] mais o maior finish das dependências, ou apenas duração[v] sem predecessores. A ordem topológica garante que cada predecessor já foi calculado. Guarde predecessor escolhido para reconstruir. Tempo O(V+E), espaço O(V) além do grafo. Vazio produz duração zero/caminho vazio; duração inválida e ciclo falham antes. Em empates, escolha, por exemplo, menor ID.

Valide com oráculo exato em DAGs pequenas: enumere caminhos ou compare recorrência memoizada. O caminho devolvido deve ser formado por arestas válidas e a soma de durações deve igualar a duração mínima do projeto.

Uma regra gulosa de escalonamento, como “maior duração primeiro”, pode mudar a ordem entre tarefas disponíveis, mas não reduz necessariamente o makespan quando há recursos limitados. Apresente um contraexemplo ou restrinja o domínio e prove a escolha. Para seleção sob orçamento, [1,3,4] com total 6 mostra que maior moeda falha; na mochila 0/1, os itens (10,60), (20,100), (30,120) com capacidade 50 refutam razão valor/peso: 160 contra 220.

**Aceite:** estado descrito em frase, transição derivada, ordem de avaliação, reconstrução validada, custo em número de estados/transições e guloso acompanhado de prova ou contraexemplo.

---

## 08 — Paradigmas, tipos, ownership e erros

### Básico — valor válido e ausência explícita

Em todas as linguagens, Tarefa precisa sair da construção com ID não vazio, duração positiva e dependências em representação que o chamador não corrompe. A solução idiomática varia:

- Python: dataclass congelada e tupla; hints não validam runtime sozinhos;
- Java: record/classe com validação e cópia defensiva; Optional pode expressar busca ausente;
- C: função de inicialização retorna status e somente publica a struct em sucesso; ownership de strings/array é documentado;
- C#: record/classe imutável, validação no construtor e nullable annotations;
- JavaScript: factory valida em runtime, cria cópias e pode congelar profundamente os campos relevantes.

Buscar tarefa ausente é resultado esperado; listar projeto vazio é coleção vazia; falha de fonte é erro. Não use o mesmo null para os três. Teste alteração da coleção original após construir a tarefa e tentativa de alterar a coleção devolvida.

Complexidade da busca deve ser declarada: varredura O(n), mapa esperado O(1) após construção O(n). O exercício não exige esconder esse custo atrás do tipo.

### Intermediário — núcleo funcional e shell imperativo

A fronteira recomendada é:

    arquivo/bytes -> parser/validador -> WorkItems válidos
    WorkItems -> algoritmo puro -> Plano
    Plano -> apresentador -> stdout/arquivo

O núcleo não importa sistema de arquivos, console, JSON ou runtime HTTP. Entrada malformada, ciclo e I/O são categorias distintas e preservam causa. A CLI traduz cada uma uma única vez em mensagem/código. Captura ampla que converte tudo em “não encontrado” viola o contrato.

Teste o núcleo com valores; o adapter com arquivo temporário real e encoding; a CLI com processo/subprocesso. Recursos fecham em sucesso e exceção. Em C, cada caminho libera apenas o que adquiriu; em runtimes com GC, arquivo/socket ainda exige escopo determinístico.

### Avançado — recurso remoto, transação e concorrência

Defina o protocolo antes da implementação: quem abre/fecha; prazo e cancelamento; quais falhas são transitórias; idempotência; consistência do snapshot; máximo de itens; ownership da coleção. Uma chamada remota com timeout não deve virar coleção vazia.

Retry é permitido somente para operação idempotente ou deduplicada, com quantidade limitada, backoff e deadline. Se houver transação, sucesso publica tudo e falha não deixa plano parcial, ou a compensação é explícita. Um teste deve injetar falha entre aquisição e uso e confirmar cleanup.

Para race, crie reprodução determinística com barreira/latch em vez de esperar “acontecer”. A correção pode usar dono único, imutabilidade, lock ou controle otimista. Verifique a invariante afetada, não apenas ausência de exceção. O ADR compara exceção e resultado discriminado pela forma de uso, frequência e integração da linguagem.

**Critério de domínio:** tipos tornam alguns estados impossíveis, validação protege os demais, ownership cobre todos os caminhos e categorias de erro informam ação do chamador.

---

## 09 — Design modular e dependências

### Básico — separar regra e I/O

Extraia uma função que recebe tarefas já válidas e devolve Plano ou erro de domínio. Ela não importa JSON, pathlib, argparse e não imprime. O adapter continua responsável por bytes, encoding e documento; o apresentador converte Plano em texto/JSON. A mesma entrada externa deve produzir a mesma saída observável de antes.

Testes mínimos: DAG válida, referência desconhecida e ciclo. A complexidade não pode piorar por conversões repetidas; construir índice uma vez mantém O(V+E) mais a política do heap. Um teste da regra não cria arquivo.

A fronteira correta preserva a invariante: o domínio só recebe WorkItems válidos localmente; o serviço valida relações globais; a CLI não implementa regra topológica.

### Intermediário — porta e dois adaptadores

A porta LeitorDeTarefas oferece somente a operação de que o caso de uso precisa. JSON e memória a implementam; nenhum if por tipo concreto aparece no caso de uso. A composition root escolhe a implementação e injeta a porta.

Uma suíte de contrato compartilhada verifica: coleção vazia válida; snapshot não mutável pelo consumidor; IDs/objetos coerentes; falha de fonte distinta de documento inválido; nenhuma alteração silenciosa entre chamadas conforme o contrato. O adapter JSON ainda precisa de integração real para encoding, permissões e parsing; o fake não substitui isso.

Formato externo é traduzido uma vez: nenhum dicionário, nome de chave ou exceção do parser vaza ao domínio. A causa técnica é preservada para diagnóstico, enquanto a mensagem ao usuário não exibe traceback.

### Avançado — nova saída e decisão arquitetural

DOT ou HTTP é adaptador de saída. Domain e graph não importam Graphviz, framework web ou escaping. Defina contrato: ordenação, encoding, escaping de aspas/quebras, tipo de conteúdo, status/código e representação de erro. A mesma entrada deve produzir saída determinística.

Um teste de contrato valida estrutura e caracteres adversariais. Para HTTP, inclua limite de corpo, timeout do cliente, correlação e mapeamento de erros; para DOT, parseie com ferramenta quando disponível e cubra IDs hostis como dados, nunca como comandos.

O ADR contém contexto, forças, opções, decisão, consequências negativas e gatilho de revisão. O diff é evidência: política central inalterada, montagem e adaptador são os pontos tocados.

**Aceite:** dependências apontam para contratos do núcleo; a troca de mecanismo afeta composição e adapter, e nenhuma abstração existe apenas para aumentar a quantidade de camadas.

## 10 — SOLID e padrões sem dogma

### Básico — SOLID por comportamento

Parta da classe que lê JSON, ordena e imprime. A separação mínima é parser/adapter, regra de planejamento e apresentador. SRP aparece porque cada parte muda por um motivo diferente, não porque ficou pequena. O teste do algoritmo recebe WorkItems e não toca disco ou console. Erro de documento e ciclo continuam categorias distintas.

Uma explicação operacional dos princípios deve mencionar evidência:

- **SRP:** uma mudança de formato não toca o algoritmo;
- **OCP:** uma variação conhecida, como desempate, entra por um ponto estável;
- **LSP:** JSON, CSV e memória cumprem as mesmas pré/pós-condições;
- **ISP:** o leitor não obriga consumidor a depender de escrita/exportação;
- **DIP:** o caso de uso depende da porta na linguagem do domínio.

Extrair método somente para reduzir linhas não recebe crédito. Uma função longa e coesa pode ser melhor que uma cadeia de delegações sem decisão protegida.

### Intermediário — Strategy e Adapter

As duas estratégias podem ser funções/comparadores: ID crescente; menor duração com ID como desempate, por exemplo. A invariante do algoritmo não muda: somente tarefas com grau zero entram na escolha. Cada resultado deve conter todos os IDs uma vez e respeitar todas as arestas. O desempate final torna repetição determinística.

JSON e CSV passam por uma suíte compartilhada de contrato, mas cada adapter tem testes próprios do mecanismo. CSV precisa declarar cabeçalho, encoding, quoting, como codifica múltiplas dependências, campos desconhecidos, tamanho e linhas inválidas. O domínio recebe WorkItem, nunca colunas ou dicionários.

“Menor duração primeiro” não garante menor duração total quando há capacidade de recursos, porque a ordem topológica isolada não modela alocação paralela. Um contraexemplo deve incluir recursos/tempos suficientes para mostrar a divergência; sem esse modelo, todas as ordens de um mesmo DAG têm o mesmo caminho crítico intrínseco.

### Avançado — Command, persistência e observação

CalcularPlano representa intenção e dados estáveis, não conexão, logger ou serviço. O repositório expõe operações do domínio e concorrência: salvar com versão esperada é mais informativo que CRUD genérico. A composition root monta Command handler, leitor, gravador e observadores.

Defina idempotência: repetir a mesma chave retorna o plano persistido, rejeita duplicata ou recalcula sem duplicar efeitos. Se gravação e publicação não forem atômicas, use uma política explícita, como outbox, ou aceite e monitore a janela. Falha de métrica não deve corromper o plano quando observabilidade é best effort; auditoria obrigatória pode exigir outra decisão.

Observer precisa de contrato de ordem, sincronismo, tratamento de falha e entrega. Concorrência de gravação é serializada ou detectada por versão. O ADR de cada padrão registra alternativa simples: função direta, chamada explícita, leitor específico. Remover um observador não altera domínio/repositório.

**Aceite:** cada padrão resolve uma variação observada; testes são comportamentais; remover cerimônia desnecessária é uma resposta válida e justificada.

---

## 11 — Refatoração segura e legado

### Básico — caracterizar antes de extrair

Primeiro capture o fluxo externo: argumentos, status, stdout, stderr e estrutura do resultado para sucesso e ciclo. Compare JSON semanticamente se whitespace não for contrato. Marque quais peculiaridades serão preservadas e qual comportamento é defeito aprovado para mudança; characterization test não santifica todo acidente.

Depois extraia uma função pura em passos separados. O commit de caracterização deve ficar verde antes da refatoração; o commit estrutural não muda a observação; a correção funcional vem depois com novo requisito/teste. A função pura recebe valores e não cria processo/arquivo.

Uma boa evidência inclui o comando exato antes/depois e diff pequeno. “A suíte passa” é insuficiente se ela não cobre a fronteira alterada.

### Intermediário — três costuras

Sistema de arquivos pode ser uma função/leitor; relógio, uma função now; destino de relatório, um writer/apresentador. As implementações reais são escolhidas somente na composition root. O teste fornece memória, instante fixo e coletor em memória.

Cada costura preserva categorias e causa: I/O, documento inválido e falha de escrita não viram o mesmo erro. Há integração separada para o adapter real, pois fake não testa permissões, encoding nem flush. Nenhum teste depende de horário atual ou diretório global.

A abstração deve ser mínima. Um callable é suficiente para relógio; um protocolo pode fazer sentido para fonte com ciclo de vida. Framework de mocks criado para o exercício aumenta risco e não é evidência de design.

### Avançado — migração gradual

Em branch by abstraction, introduza a porta diante do leitor antigo, migre consumidores, adicione o leitor rigoroso, compare ambos em sombra sem duplicar efeitos, altere a seleção e remova legado/flag. Em Strangler, roteie uma capacidade vertical completa. A escolha depende de coexistência dentro do processo ou na fronteira.

Baseline e hipótese devem ser mensuráveis. A flag tem dono, fallback seguro, métrica, data e critério de remoção. Divergências são contadas por categoria e amostras sanitizadas; não ficam apenas em logs livres. Rollback é ensaiado antes de apagar suporte antigo.

Para mudanças de formato, expanda para ler antigo/novo, migre com checkpoint e idempotência, observe consumidores, depois contraia. Dual write não é atomicidade. A conclusão exige remover caminho antigo e compatibilidade temporária, não mantê-los indefinidamente.

**Aceite:** histórico reversível, comportamento classificado, costuras alinhadas ao design futuro e evidência de equivalência/rollback.

---

## 12 — Descoberta, requisitos e modelagem

### Nível 1 — tornar verificável

Cinco reescritas devem usar a forma cenário: fonte do estímulo, estímulo, ambiente, resposta e medida. Exemplos:

- sob arquivo válido com 100 mil itens e grau médio cinco, o comando conclui no p95 acordado e dentro do orçamento de memória;
- dado ciclo, retorna código 2, stdout vazio e stderr identifica ao menos um caminho fechado;
- dado JSON acima do limite, rejeita antes da construção completa sem saída parcial;
- permutar itens e dependências mantém o resultado segundo a política de desempate;
- arquivo inexistente cita o caminho sanitizado, não exibe traceback e não é classificado como documento inválido.

O glossário precisa definir, entre outros, tarefa, ID, dependência, dependente, aresta, DAG, ordem topológica, lote, duração mínima e caminho crítico. Na convenção do curso, se B depende de A, a aresta é A→B; A é dependência e B é dependente.

Tabela de decisão orientativa:

| Condição | Resultado externo | Dono da detecção |
|---|---|---|
| JSON sintaticamente inválido | erro de documento | adapter |
| referência desconhecida | erro de domínio/entrada | validação global |
| ciclo com referências válidas | erro de ciclo | algoritmo/grafo |
| mais de uma condição | precedência definida pelo contrato | fronteira + domínio |

Critérios positivos cobrem casos válidos; negativos, rejeições; fronteira, vazio, limite exato e um acima. Um critério contém entrada e observação, não “funciona corretamente”.

### Nível 2 — modelar e rastrear

C4 contexto mostra pessoa e Planner; contêiner mostra processo CLI e sistema de arquivos; componentes mostram CLI/composition root, adapter, caso de uso, domínio/grafo e apresentação. Uma sequência de erro deve mostrar onde nasce, como é traduzido e que stdout permanece vazio. Diagrama atual não mistura componentes propostos.

Invariantes locais: ID/título não vazios, duração positiva, dependências distintas, ausência de autoaresta. Globais: IDs únicos, toda referência existe, grafo acíclico. Pós-condições do plano não devem ser classificadas como invariantes do WorkItem.

Use IDs como FUN-001, QUA-001 e OPS-001. Para oito requisitos, ligue fonte/decisão, arquivo ou componente, teste e evidência. Uma lacuna é real quando um requisito de risco não possui verificação: por exemplo, mutação de desempate sobrevive ou erro de Unicode nunca atravessa o adapter. Não altere o projeto neste exercício; registre impacto e prioridade.

Hipótese boa: “ordenar vizinhos é responsável por mais de 20% do tempo em leques de 100 mil itens”; experimento, métrica, ambiente e prazo de revisão acompanham. “Acho que está lento” não é hipótese testável.

### Nível 3 — conduzir uma mudança

Para duração decimal opcional, defina unidade/precisão, arredondamento, ausência versus zero, compatibilidade do campo inteiro, serialização e tipo numérico. O algoritmo topológico não muda, mas soma, comparação, caminho crítico e contrato externo mudam; ponto flutuante binário pode ser inadequado. Para recurso por lote, o problema muda de uma simples ordenação topológica para escalonamento sob capacidade; heurísticas talvez não sejam ótimas e complexidade precisa ser reavaliada.

Em ambos os casos, documente atores, problema, não objetivos, estados válidos, invariantes, exemplos, atributos de qualidade, superfícies JSON/CLI, migração, riscos e rollback. A matriz de impacto cobre código, dados, testes, docs, operação e consumidores. A decisão pode rejeitar a proposta se o valor não paga a complexidade.

**Aceite:** outra pessoa deriva testes, identifica compatibilidade e consegue contestar a decisão usando premissas registradas.

---

## 13 — Arquitetura e decisões sistêmicas

### Nível 1 — ler o sistema atual

Os diagramas devem corresponder ao runtime, não a uma arquitetura desejada. Contexto: usuário executa Planner sobre arquivo. Contêiner: um processo local lê, calcula e escreve. Componentes: CLI/composição, repositório JSON, serviço, domínio/grafo e presenter. Mostre fluxo de chamada e direção de dependência separadamente.

O grafo de imports deve apontar infraestrutura para contratos/modelo estáveis; domain e graph não importam CLI, JSON ou framework. Ciclo de imports é evidência a investigar. Quatro cenários de qualidade podem cobrir desempenho, segurança de entrada, modificabilidade e recuperabilidade, cada um com estímulo/ambiente/resposta/medida.

Um ADR para manter monólito modular é válido: baixa escala operacional, transação simples e equipe pequena favorecem processo único; perde-se deploy/escala independente; gatilhos de revisão podem ser isolamento de carga, equipes autônomas ou SLOs incompatíveis. “Microserviço é complexo” sem drivers não basta.

### Nível 2 — evoluir uma borda

Para CSV ou HTTP, especifique contrato externo, validação, tradução para WorkItem, limites de bytes/itens/tempo, autenticação se aplicável e ameaça de conteúdo hostil. A porta permanece orientada ao caso de uso; composition root escolhe adapter. Domain e graph não mudam.

Testes de contrato rodam contra implementações; integração usa mecanismo real. Sinais incluem taxa/latência por resultado, rejeições por limite e correlação sem dados sensíveis. SLO precisa de população, janela e limiar. Compatibilidade define versão, depreciação e rollback.

Threat model mínimo identifica ativo, fronteira de confiança, atacante/capacidade, abuso e controle: exaustão por arquivo enorme, CSV formula injection na saída, path traversal quando caminho é externo, payload repetido e vazamento em logs. Segurança aqui é de robustez e proteção da aplicação, não de exploração.

### Nível 3 — decidir sobre distribuição

Compare:

| Opção | Estado/consistência | Falhas novas | Quando faz sentido |
|---|---|---|---|
| síncrona | resultado na chamada | timeout e ocupação do processo | cálculo curto e previsível |
| job no mesmo serviço | aceito→executando→concluído/falhou | fila local, retomada | cálculo longo sem necessidade de outro serviço |
| event-driven distribuída | consistência eventual e correlação | duplicação, partição, broker, compatibilidade | autonomia/escala/isolamento comprovados |

Todas precisam de timeout/deadline, cancelamento e limites. Jobs e eventos precisam de ID idempotente, política de retry, fila limitada, backpressure, autorização para consultar resultado, métricas de idade/profundidade e recuperação após reinício. “Exactly once” não deve ser prometido sem protocolo; normalmente aceite ao menos uma vez com deduplicação.

O ADR declara custo operacional e condição de adoção. Concluir “não distribuir agora” é tecnicamente maduro quando satisfaz os drivers. Observabilidade deve responder onde o trabalho está e por que falhou, sem usar logs como substituto de estado.

**Aceite:** cenários mensuráveis, trade-offs completos, threat model, recuperação e gatilho de revisão; diagrama consistente com imports e runtime.

## 14 — Estratégia de testes e qualidade

### Nível 1 — exemplos e fronteiras

A matriz de duração deve distinguir: campo ausente, null, booleano, string numérica, zero, negativo, inteiro positivo, decimal e valor acima do limite. Em Python, bool é subtipo de int, portanto True precisa de rejeição explícita. Cada linha informa camada que detecta, categoria e observação externa. O teste não deve depender somente do texto completo da mensagem.

Projeto vazio é sucesso com ordem/lotes/caminho vazios e duração zero. ID duplicado, referência ausente e ciclo são falhas diferentes. Ciclo só é diagnosticado após referências válidas; a precedência entre erros precisa ser estável.

No repositório, grave JSON real em diretório temporário com UTF-8, caracteres compostos e escape; cubra documento truncado e objeto de forma errada. Testar apenas um dicionário montado em memória não verifica parser/encoding. Na CLI, execute o processo nos formatos texto e JSON e verifique status, canais, schema e determinismo. Timeout impede travamento silencioso.

**Evidência:** testes curtos e determinísticos ficam vermelhos ao remover validação relevante ou alterar código de saída.

### Nível 2 — propriedades, relações e força

Gere DAGs por uma permutação/índices crescentes e registre cem sementes. Verifique as oito propriedades:

1. todos e somente os IDs aparecem uma vez na ordem;
2. toda dependência precede o dependente;
3. todos os IDs aparecem uma vez entre os lotes;
4. lote do dependente é posterior ao das dependências;
5. duração mínima é ao menos a maior duração individual;
6. caminho crítico é válido e soma a duração mínima;
7. vazio produz estruturas vazias e duração zero;
8. a saída é determinística.

Falha deve imprimir seed e, idealmente, reduzir o caso. Três relações metamórficas possíveis: permutar documento preserva plano sob desempate definido; multiplicar durações positivas por k multiplica duração mínima; adicionar componente isolado não invalida relações anteriores. Renomear IDs pode alterar desempate, portanto compare estrutura mapeada, não bytes sem qualificação.

Troque mock acoplado a chamadas por fake quando o objetivo é comportamento do caso de uso; use integração quando parsing/arquivo é o risco. Justifique a fronteira. Injete mutantes: aceitar zero, ignorar duplicata, não decrementar grau, usar min no caminho crítico, retornar status zero em erro. Mutante sobrevivente indica teste fraco, código morto, requisito ambíguo ou equivalência; registre a análise.

### Nível 3 — estratégia profissional

A matriz de risco liga ameaça/falha a probabilidade, impacto, controle, teste, frequência e dono. A suíte pode ser:

- PR: unidade, domínio, contrato rápido, lint/tipos;
- main: integração e CLI completas;
- noturna: propriedades amplas, mutação, fuzz e performance.

Cada gate possui orçamento e política de bloqueio. Testes lentos não são simplesmente omitidos; rodam na cadência que produz feedback útil.

Performance cobre cadeia, leque, esparso e denso, registrando V/E, versão, hardware, aquecimento, repetições, mediana/p95 e pico. O gerador fica fora da região medida. Fuzz do adapter é local e limitado por bytes, profundidade, tempo e memória; sucesso sempre produz objetos válidos, falha é classificada e nunca há crash/loop.

Para flaky test, reproduza várias vezes, capture concorrência/seed/tempo e encontre a primeira fonte não controlada. Fixe relógio, ordenação, porta, isolamento ou sincronização. Retry pode coletar evidência temporariamente, mas não é correção.

**Aceite:** cada risco crítico possui teste adequado no nível certo, mutações importantes morrem e falhas são reproduzíveis.

---

## 15 — Colaboração, versionamento e operação

### Nível 1 — mudança revisável

Uma sequência possível para adapter CSV é:

1. contrato e fixtures sem alterar produção;
2. modelo/tradução pura;
3. adapter com testes de integração;
4. composição/opção de CLI;
5. documentação e limpeza.

Cada commit compila e tem intenção única. Mensagem orientativa: “feat(input): adiciona tradução CSV validada” seguida do motivo e das incompatibilidades; “updates” não explica nada. Não force esta divisão quando ela deixaria commits quebrados; a unidade é reversibilidade e revisão.

A descrição do PR informa problema, escopo/não escopo, contrato, risco, comandos/evidência e rollback. Comentários de revisão são classificados: bloqueio de correção/segurança/contrato; sugestão; dúvida; nit automatizável. Preferência de estilo não deve bloquear quando a regra é automatizável.

### Nível 2 — superfícies e compatibilidade

Inventarie CLI e flags, códigos de saída, stdout/stderr, schema JSON de entrada/saída, API Python pública, arquivos/fixtures, mensagens prometidas e requisitos operacionais. Uma mudança pode ser:

- patch: correção compatível sem mudar promessa;
- minor: capacidade aditiva compatível;
- major: remoção, renome, restrição ou mudança semântica incompatível;
- dependente de política: ordenação, mensagem, campo desconhecido e limite podem ou não ser públicos.

Classificar dez casos exige justificar consumidor afetado, não olhar apenas forma. Campo novo quebra leitores que rejeitam desconhecidos; mudança de performance pode ser incompatibilidade operacional.

Para deprecar duration, expanda leitores para duration e durationMinutes com precedência definida, passe a produzir o novo de forma compatível, observe migração, comunique prazo, pare de produzir antigo e só depois remova leitura. README ensina uso; changelog comunica impacto; ADR registra decisão duradoura. Exemplos devem ser executados em CI para não apodrecer.

### Nível 3 — incidente de leitor v1

Defina severidade por impacto, não por emoção. Papéis mínimos: coordenação, execução técnica e comunicação; em equipe pequena, uma pessoa pode acumular papéis explicitamente. A linha do tempo separa fato, decisão e hipótese com horários consistentes.

O runbook começa por impacto e sinais, oferece diagnóstico seguro/read-only, mitigação reversível, escalada, recuperação e verificação. Uma mitigação plausível é restaurar gravação do formato antigo ou rollback do produtor, preservando dados. Mensagens informam alcance e próxima atualização sem expor payload sensível.

O post-mortem descreve condições sistêmicas: contrato sem teste entre versões, rollout sem compatibilidade, telemetria tardia. “Erro humano” não encerra causa. Três ações têm dono, prazo e teste de conclusão, por exemplo contrato v1/v2 em CI, gate de compatibilidade e ensaio de rollback. “Ter mais cuidado” não é verificável.

**Aceite:** outra pessoa reconstrói o incidente, executa recuperação e confirma cada ação sem depender de conversa oral.

---

## 16 — Projeto guiado, projeto autoral e avaliação

Este capítulo não possui uma implementação única. O gabarito avalia o processo e as evidências; não escolha arquitetura, biblioteca ou tema apenas para imitar o projeto de referência.

### Nível 1 — projeto guiado

A linha de base inclui comando executado, versões, resultado e mapa de responsabilidades. Você deve explicar onde nascem validação local, referência global, ciclo, cálculo e tradução da CLI. Escolha uma evolução vertical pequena e escreva atores, exemplos, invariantes, limites, compatibilidade e aceite antes do código.

Diagramas correspondem ao estado implementado; ADR registra uma decisão real e alternativa. A fatia vertical atravessa apenas as camadas necessárias e inclui caso feliz e erro. A demonstração em checkout limpo segue instruções documentadas, sem arquivo local oculto.

Milestones 1–3 fecham quando requisito, código, teste e documento têm links/comandos navegáveis. Quantidade de funcionalidades não compensa uma invariante central quebrada.

### Nível 2 — endurecimento

Propriedades validam regras gerais; testes de contrato comparam adapters; integração executa mecanismo real. Cinco defeitos deliberados devem representar riscos e ser mortos por testes relevantes. Benchmark registra ambiente, V/E, distribuição e dispersão; não use uma execução como afirmação universal.

Threat model identifica ativos/fronteiras e testa limites de bytes, itens, profundidade e tempo. Segredos e dados reais não entram em fixtures. O runbook é ensaiado com falha controlada, incluindo rollback e verificação. Release possui versão, changelog, compatibilidade e revisão por outra pessoa.

Milestones 4–6 fecham quando outra pessoa executa tudo sem orientação oral. Evidência pode revelar limite não resolvido, desde que seja classificado e não viole gate essencial.

### Nível 3 — projeto autoral e defesa

A proposta define problema, usuário, não objetivos e risco técnico. Milestones terminam em resultados observáveis; walking skeleton cedo prova build, entrada, regra mínima e saída real. Registro semanal contém objetivo, hipótese, mudança, evidência, resultado inesperado, decisão e próximo risco.

Na revisão cruzada, cada ponto da rubrica tem link. Antes de congelar, resolva todos os gates essenciais: execução limpa, invariantes, testes, segredo/licença/autoria, operação destrutiva, integração real e explicação do código. A recomendação é pelo menos 75/100, sem gate aberto.

A defesa explica escolhas, custos, falhas e alternativas. Para a pergunta surpresa, não prometa implementação imediata: faça análise de impacto em requisitos, domínio, algoritmo, dados, contrato, segurança, observabilidade, rollout e rollback. Admitir uma incerteza e propor experimento é melhor que inventar garantia.

**Critério de correção:** solução autoral continua autoral. O avaliador aceita decisões diferentes quando as premissas são explícitas e a evidência sustenta o resultado.

---

## Orientação para os cinco laboratórios formais

Os laboratórios são integrações dos capítulos, não uma segunda lista de respostas. Consulte esta seção somente depois de produzir os artefatos pedidos.

### [Lab 01 — contrato, oráculo e complexidade](laboratorios/lab-01-contrato-complexidade.md)

O núcleo da entrega é a separação entre especificação, oráculo e implementação. O oráculo de ordem topológica deve verificar conjunto/multiplicidade e cada aresta independentemente do algoritmo testado. Para o desempate ordinal, acrescente casos em que vários IDs estão disponíveis; validar apenas precedência não testa essa política.

Na análise, use V/E: construir índices e graus é Θ(V+E); Kahn com heap é O(E+V log V); memória é Θ(V+E). Na matriz C, examinar células pode levar Θ(V²), e MAX_NODES é limite de implementação, não complexidade constante. Benchmark não inclui geração, registra mediana/p95 e deve comparar cadeia, leque e esparso.

**Gate orientativo:** o oráculo rejeita ordens inválidas plantadas; uma mutação de desempate falha; limites adversariais têm política antes, durante e depois do parse.

### [Lab 02 — estruturas, busca e grafos](laboratorios/lab-02-estruturas-grafos.md)

A mesma suíte de contrato precisa passar para lista e matriz. Registre custo real de has_edge, neighbors e escolha de disponível; não chame hash de O(1) garantido nem matriz de O(V+E). A fila circular deve cruzar wrap-around, capacidade um, overflow/underflow e limpar referências.

Propriedades de DAG são o oráculo principal. FIFO demonstra que correção topológica não implica desempate. Lower bound usa intervalo semiaberto; estabilidade usa identidades distintas com a mesma duração. Cada uma das cinco mutações precisa de um teste que falhe ou de uma justificativa de equivalência.

**Gate orientativo:** duas linguagens, duas representações, seeds reproduzíveis, invariantes validadas e nenhuma mutação temporária restante.

### [Lab 03 — estratégias algorítmicas e design](laboratorios/lab-03-estrategias-design.md)

Caminho crítico exige recorrência, ordem topológica e predecessor para reconstrução. Compare iterativo e memoizado também pela profundidade. A mochila deve declarar estado/transição antes do código e demonstrar por teste por que a atualização unidimensional ocorre de trás para frente.

Strategies só escolhem entre disponíveis; não alteram grafo. JSON, CSV e memória passam pelo mesmo contrato e os mecanismos mantêm integração própria. A CLI/composition root escolhe adapter, estratégia e saída; domínio não importa essas tecnologias. Os três gulosos devem ter contraexemplos reproduzíveis, não afirmações.

**Gate orientativo:** propriedades anteriores continuam verdes; direção de dependência está desenhada; stdout, stderr e códigos de saída são parte do contrato.

### [Lab 04 — evolução segura, arquitetura e testes](laboratorios/lab-04-evolucao-arquitetura-testes.md)

O fixture legado é benigno, pequeno e isolado. Caracterize antes de corrigir e classifique cada observação. A tabela de rastreabilidade liga IDs a riscos, testes e evidência. Cada commit de refatoração é verde, reversível e não mistura formatação ampla com regra.

C4 e ADR devem corresponder ao código. A estratégia de qualidade combina unidade, contrato, integração, propriedade, mutação, limite e benchmark. O flaky test é corrigido pela fonte de não determinismo, nunca por sleep maior. A revisão prioriza correção, segurança, recursos e operação antes de estilo.

**Gate orientativo:** histórico prova a sequência; rollback foi possível; requisito, arquitetura e teste apontam para o mesmo comportamento.

### [Lab 05 — capstone Dependency Planner](laboratorios/lab-05-dependency-planner.md)

Comece pela linha de base e matriz externa. Escolha somente uma evolução vertical e leve-a até requisito, código, testes, documentação e operação. As cinco opções propostas têm soluções distintas; o gabarito não seleciona uma. Em qualquer opção, preserve dependências, determinismo contratado, limites e categorias de erro.

A campanha de qualidade combina pelo menos unidade, contrato, integração, propriedades, cinco mutações e benchmark com V/E. Os dois diagnósticos devem chegar à primeira fronteira divergente e deixar teste permanente. README/runbook cobrem instalação, códigos, limites, atualização e rollback.

Na defesa, responda pelo modelo: sentido da aresta, efeito do heap, separação entre referência ausente e ciclo, precondição DAG do caminho crítico, garantias de domínio versus adapter, riscos de exaustão, alternativa recusada e teste de determinismo.

**Gate orientativo:** runner/matriz passam, evolução é revisável, evidência é reproduzível e a rubrica alcança ao menos 75% sem gate essencial aberto.

---

## Como corrigir sem transformar o gabarito em receita

Use esta escala por exercício:

- **insuficiente:** apresenta saída ou código sem contrato e não trata bordas;
- **básico:** caminho feliz correto e custo principal identificado;
- **competente:** invariantes, erros, testes e complexidade coerentes;
- **profissional:** evidencia trade-offs, limites, diagnóstico, operação e reprodutibilidade.

Uma solução não perde pontos por usar outra linguagem, estrutura ou arquitetura quando preserva as garantias e mede o custo correto. Ela perde pontos se esconder hipótese crítica, confundir teste com prova, afirmar desempenho sem protocolo ou introduzir abstração sem variação real.

## Verificação do projeto guiado

Na raiz do repositório:

    bash 02-OSINT/engenharia-software/testar-curso.sh

O resultado esperado é PASS para as toolchains instaladas. SKIP informa uma dependência ausente e não comprova o exemplo daquela linguagem. Falha deve ser investigada antes de atribuí-la à máquina; registre versão, comando e primeiro limite divergente.
