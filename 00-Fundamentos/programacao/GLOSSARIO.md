# Glossário técnico de programação

Este glossário define os termos no contexto do curso. A definição curta serve
para recuperar o modelo mental; volte ao capítulo correspondente para estudar
mecanismo, exemplos e limites.

## Valores, tipos e execução

| Termo | Definição e exemplo |
|-------|---------------------|
| Algoritmo | Sequência finita e não ambígua de passos que transforma entradas em saídas. “Somar os valores e dividir pela quantidade” é um algoritmo; o código é uma implementação. |
| Bit | Unidade binária com valor 0 ou 1. Bits são agrupados para representar números, instruções e dados. |
| Byte | Grupo de oito bits. O número de caracteres não é necessariamente o número de bytes: “á” ocupa mais de um byte em UTF-8. |
| Codificação | Regra que relaciona símbolos e bytes. UTF-8 codifica texto; Base64 representa bytes como texto, mas não protege o conteúdo. |
| Valor | Dado manipulável, como 42, “azul” ou uma lista. Um valor tem representação e operações definidas pelo tipo. |
| Literal | Notação escrita diretamente no código para produzir um valor, como <code>10</code>, <code>true</code> ou <code>[]</code>. |
| Variável | Nome associado a um valor ou referência durante certo escopo e lifetime. “Caixa” é apenas uma analogia e não descreve todas as linguagens. |
| Constante | Nome cujo vínculo ou valor não deve mudar após inicializado. Não significa automaticamente que todo objeto alcançável seja imutável. |
| Tipo | Conjunto de valores, representação possível e operações válidas. Inteiro e texto possuem contratos diferentes. |
| Tipagem estática | Grande parte da compatibilidade de tipos é verificada antes da execução. Java, C e C# também fazem algumas verificações em runtime. |
| Tipagem dinâmica | O tipo acompanha o valor e operações incompatíveis são detectadas durante a execução. Python e JavaScript continuam tendo tipos. |
| Inferência de tipo | A ferramenta deduz um tipo pelo contexto; isso não transforma uma linguagem estática em dinâmica. |
| Conversão | Transformação de tipo ou representação. Converter o texto “10” para número pode falhar e precisa de contrato. |
| Expressão | Construção que produz valor, como <code>preco * quantidade</code> ou uma chamada de função. |
| Instrução | Unidade que realiza uma ação ou controla o fluxo, como atribuição, retorno ou decisão. |
| Operador | Símbolo ou palavra que opera sobre valores, como <code>+</code>, <code>==</code> ou <code>&amp;&amp;</code>. |
| Precedência | Regras de agrupamento de operadores. Parênteses tornam a intenção explícita quando há dúvida. |
| Booleano | Tipo lógico com verdadeiro e falso. Condições compostas seguem regras de álgebra booleana. |
| Curto-circuito | Em <code>A &amp;&amp; B</code>, B não é avaliado se A já torna o resultado falso. Isso afeta efeitos e acessos seguros. |
| Estado | Informação mutável que influencia o comportamento futuro, como conteúdo de lista ou saldo de conta. |
| Invariante | Propriedade que deve permanecer verdadeira em pontos definidos, como saldo maior ou igual a zero. |
| Mutabilidade | Possibilidade de alterar um objeto após sua criação. Uma referência constante ainda pode apontar para objeto mutável. |
| Identidade | Noção de “ser o mesmo objeto”, diferente de ter conteúdo igual. |
| Escopo | Região do programa em que um nome pode ser resolvido. |
| Lifetime | Intervalo durante o qual um valor, objeto ou recurso existe e pode ser usado validamente. |

## Controle de fluxo e funções

| Termo | Definição e exemplo |
|-------|---------------------|
| Condição | Expressão booleana que decide um caminho. Deve ser testada nos limites e combinações relevantes. |
| Ramo | Caminho possível de uma decisão, como o bloco do <code>if</code> ou do <code>else</code>. |
| Laço | Repetição controlada por coleção, contador ou condição. Deve existir progresso até o término. |
| Iteração | Uma execução do corpo do laço ou a produção do próximo elemento. |
| Recursão | Função resolve uma instância usando outra menor. Exige caso-base e progresso em direção a ele. |
| Função | Unidade de comportamento com entradas, resultado e efeitos definidos. Pequena não significa automaticamente bem projetada. |
| Parâmetro | Nome declarado por uma função para receber uma entrada. |
| Argumento | Valor ou expressão fornecido na chamada da função. |
| Retorno | Resultado entregue ao chamador. Imprimir no terminal não é o mesmo que retornar. |
| Efeito colateral | Interação observável além do retorno: alterar estado, escrever arquivo, consultar relógio, rede ou console. |
| Função pura | Com as mesmas entradas, produz o mesmo resultado e não causa efeito externo observável. |
| Closure | Função que conserva acesso ao escopo léxico em que foi criada. |
| Callback | Função fornecida para ser chamada por outro componente, de forma síncrona ou assíncrona. |
| Predicado | Função ou expressão booleana usada para filtrar, procurar ou validar. |
| Idempotência | Repetir a operação produz o mesmo estado final relevante. Isso não obriga todos os detalhes da resposta a serem iguais. |

## Organização e modelagem

| Termo | Definição e exemplo |
|-------|---------------------|
| Módulo | Unidade de organização, nomes e visibilidade. A forma concreta varia por linguagem. |
| Pacote | Agrupamento distribuível ou namespace de módulos. Pacote instalado e módulo importado não são sempre a mesma coisa. |
| Dependência | Componente necessário a outro: biblioteca, serviço, relógio, banco ou filesystem. |
| API | Interface contratual de um componente. Pode ser função, biblioteca, sistema operacional ou serviço HTTP. |
| Contrato | Entradas, saídas, efeitos, erros e garantias observáveis. |
| Abstração | Modelo que expõe o necessário e oculta detalhes irrelevantes para determinado uso. |
| Encapsulamento | Fronteira que controla acesso ao estado para proteger invariantes. |
| Classe | Definição de tipo que pode reunir dados, invariantes e comportamento. |
| Objeto | Valor com estado e comportamento e, em muitos modelos, identidade própria. |
| Interface | Operações exigidas sem obrigar o consumidor a conhecer uma implementação concreta. |
| Composição | Construção de comportamento combinando componentes menores. |
| Herança | Relação de derivação que deve preservar substituição válida, e não servir apenas para copiar código. |
| Polimorfismo | Uso de implementações diferentes por meio de um contrato comum. |
| Genérico | Código parametrizado por tipo, preservando verificações sem duplicar implementação. |
| Coesão | Grau em que as responsabilidades de um componente pertencem ao mesmo propósito. |
| Acoplamento | Dependência entre componentes. O objetivo é torná-la explícita, estável e testável, não fingir que não existe. |
| DTO | Objeto de transferência usado em uma fronteira; não precisa ser o mesmo modelo do domínio. |
| Entidade | Conceito de domínio reconhecido por identidade ao longo do tempo, como tarefa com ID. |
| Objeto de valor | Conceito definido por seus atributos, sem identidade independente relevante. |

## Estruturas de dados e algoritmos

| Termo | Definição e exemplo |
|-------|---------------------|
| Coleção | Estrutura que reúne valores e define operações de acesso, inserção, remoção e percurso. |
| Array | Região indexada, normalmente contígua, com tamanho e representação definidos pela linguagem. |
| Lista | Sequência ordenada. Array dinâmico e lista ligada têm custos diferentes apesar do mesmo nome informal. |
| Mapa/dicionário | Associação de chaves a valores. Tabela hash costuma ter acesso médio próximo de O(1), não uma garantia universal. |
| Conjunto | Coleção de elementos únicos, útil para pertinência e deduplicação. |
| Pilha | Estrutura LIFO: último a entrar, primeiro a sair. Não confunda com a pilha de chamadas. |
| Fila | Estrutura FIFO: primeiro a entrar, primeiro a sair. |
| Deque | Fila de duas pontas com operações eficientes nos dois extremos. |
| Árvore | Estrutura hierárquica de nós e arestas sem ciclos no caminho estrutural. |
| Grafo | Vértices e relações; pode ser direcionado, ponderado, cíclico ou desconectado. |
| Iterador | Protocolo/objeto que produz elementos sob demanda sem expor a representação inteira. |
| Gerador | Forma de construir iterador suspendendo e retomando uma função. |
| Complexidade | Crescimento de tempo ou espaço em função do tamanho da entrada. Precisa ser combinado com medição real. |
| Big O | Limite assintótico superior, como O(n) ou O(log n). Não representa segundos. |
| Busca binária | Busca em domínio ordenado/monotônico que elimina metade do intervalo por etapa. |
| Ordenação estável | Mantém a ordem relativa de itens considerados iguais pela chave. |

## Toolchain, qualidade e falhas

| Termo | Definição e exemplo |
|-------|---------------------|
| Código-fonte | Representação do programa antes de ser transformada em artefato. |
| Compilador | Analisa e traduz código para outra representação, como bytecode ou código de máquina. |
| Interpretador | Executa uma representação do programa. Implementações podem combinar interpretação e compilação JIT. |
| Linker | Resolve símbolos e combina objetos/bibliotecas em executável ou biblioteca. |
| Runtime | Ambiente e serviços presentes na execução, como JVM, CLR ou runtime Python. |
| Build | Processo reproduzível que transforma fontes e dependências em artefatos verificáveis. |
| Artefato | Resultado de build, como executável, pacote, imagem ou relatório. |
| Lint | Análise estática de estilo, construções suspeitas e regras. Não substitui compilador nem testes. |
| Warning | Diagnóstico de possível problema que não interrompeu a ferramenta. Deve ser entendido, não silenciado às cegas. |
| Exceção | Mecanismo de sinalização e propagação de condição anormal em várias linguagens. |
| Stack trace | Sequência de chamadas ativas numa falha. Mostra onde ela apareceu, não necessariamente onde nasceu. |
| Código de saída | Inteiro devolvido pelo processo; zero costuma significar sucesso. |
| stdout | Fluxo da saída normal ou de dados do programa. |
| stderr | Fluxo independente destinado a diagnósticos e erros. |
| Debugger | Ferramenta para pausar, avançar, inspecionar estado e observar chamadas. |
| Breakpoint | Ponto de parada do depurador, opcionalmente condicionado a uma expressão. |
| Asserção | Verificação interna de uma condição esperada pelo programador. Não substitui validação externa. |
| Teste unitário | Verifica pequena unidade comportamental com dependências controladas. |
| Teste de integração | Verifica colaboração real entre componentes, como API e banco. |
| Teste de contrato | Verifica que produtor e consumidor concordam sobre interface e representação. |
| Teste de regressão | Preserva um caso que falhava antes da correção. |
| Fixture | Estado ou dado controlado preparado para um teste. |
| Stub | Implementação simples que fornece respostas predeterminadas. |
| Mock | Dublê usado para verificar interações esperadas; excesso torna testes frágeis. |
| Refatoração | Mudança interna sem alteração intencional do comportamento observável. |
| Dívida técnica | Custo futuro de decisão ou limitação consciente. Não é apenas sinônimo de código feio. |

## Sistema operacional e concorrência

| Termo | Definição e exemplo |
|-------|---------------------|
| Processo | Instância de programa em execução, com memória e recursos administrados pelo sistema operacional. |
| Thread | Fluxo de execução dentro de processo; threads normalmente compartilham memória do processo. |
| Stack de chamadas | Estrutura para frames, retornos e dados locais conforme runtime e plataforma. |
| Heap | Região/estratégia para alocações de lifetime dinâmico; a gestão varia entre C, JVM, .NET e Python. |
| Ponteiro | Valor que representa endereço/localização de memória. Operações inválidas em C podem gerar comportamento indefinido. |
| Referência | Forma controlada de alcançar objeto ou valor. Não é automaticamente igual a ponteiro manipulável. |
| Garbage collector | Recupera memória de objetos inalcançáveis; não fecha todo recurso externo no momento necessário. |
| Recurso | Algo que exige aquisição e liberação: arquivo, socket, lock, memória nativa ou transação. |
| Concorrência | Várias tarefas progridem em intervalos sobrepostos, mesmo em um único núcleo. |
| Paralelismo | Trabalho executado simultaneamente por recursos diferentes. |
| Assíncrono | Operação suspende a continuação sem manter a thread bloqueada durante a espera. |
| Event loop | Laço que agenda callbacks/continuações por eventos e filas. Código síncrono longo ainda o bloqueia. |
| Promise/Future/Task | Representação de resultado eventual que pode completar ou falhar. Cancelamento depende da API: uma `Promise` JavaScript não é cancelável por si; `AbortSignal` apenas solicita cancelamento cooperativo à operação. |
| Race condition | Correção depende de ordem de eventos que não é garantida. |
| Data race | Acessos concorrentes incompatíveis à mesma memória sem sincronização, conforme o modelo da linguagem. |
| Lock | Mecanismo de exclusão ou coordenação. Uso incorreto causa contenção ou deadlock. |
| Deadlock | Tarefas esperam circularmente recursos que nenhuma poderá liberar. |
| Timeout | Limite de espera. Não significa necessariamente que o trabalho remoto foi cancelado. |
| Cancelamento | Solicitação cooperativa de interrupção; deve ser propagada e tratada. |
| Backpressure | Impede que produtor rápido sobrecarregue consumidor ou memória. |

## Web, dados e entrega

| Termo | Definição e exemplo |
|-------|---------------------|
| HTTP | Protocolo de requisição e resposta; método, alvo, cabeçalhos e corpo têm papéis distintos. |
| URL | Identificador que pode conter esquema, autoridade, caminho, consulta e fragmento. O fragmento não vai ao servidor HTTP. |
| Cabeçalho | Metadado de mensagem HTTP, como tipo de conteúdo, cache ou autenticação. |
| Status HTTP | Código sobre o resultado no protocolo. Erro do cliente, do servidor e redirecionamento têm classes diferentes. |
| JSON | Formato textual de valores, arrays e objetos. Não possui data nem comentário como tipos nativos. |
| CRUD | Criar, consultar, atualizar e remover. É um conjunto de operações, não uma arquitetura. |
| Schema | Regras estruturais de campos, tipos, relações e restrições. |
| Chave primária | Identificador único de linha no modelo relacional. |
| Chave estrangeira | Restrição que referencia outra chave e preserva integridade entre tabelas. |
| Índice | Estrutura auxiliar que acelera certos acessos com custo de espaço e escrita. |
| Transação | Unidade confirmada ou revertida segundo as garantias do banco. |
| Migração | Alteração versionada e repetível do schema ou dos dados estruturais. |
| Cache | Cópia reutilizada para reduzir custo; exige política de validade e invalidação. |
| Container | Processo isolado com filesystem/configuração derivados de imagem; não é uma VM completa. |
| Imagem | Artefato imutável em camadas usado para iniciar containers. |
| Volume | Armazenamento fora da camada gravável efêmera do container. |
| Proxy reverso | Servidor que recebe do cliente e encaminha a backend, podendo aplicar TLS, limites e roteamento. |
| Healthcheck | Sinal operacional de saúde/prontidão definida. Não substitui teste de negócio. |
| Log | Registro de evento com contexto e política de retenção, sem segredos. |
| Métrica | Medição numérica agregável, como latência ou quantidade de erros. |
| Trace | Caminho de uma operação por múltiplos componentes. |

## Segurança básica

| Termo | Definição e exemplo |
|-------|---------------------|
| Autenticação | Verificação de identidade: “quem é você?”. |
| Autorização | Decisão sobre ação: “esta identidade pode fazer isto neste recurso?”. |
| Privilégio | Capacidade concedida a processo ou identidade. Menor privilégio reduz impacto. |
| Segredo | Dado que concede acesso ou prova identidade, como token, chave ou senha. Não deve ir para código, log ou commit. |
| Validação | Verificação de forma, faixa e regra da entrada antes de ela alcançar o núcleo. |
| Sanitização | Transformação específica para um contexto de saída. Não é solução universal nem substitui parametrização. |
| Hash criptográfico | Resumo unidirecional usado em integridade e protocolos. Senhas exigem função própria, lenta e com salt. |
| Criptografia | Transformação reversível com chave para proteger confidencialidade e, em modos adequados, integridade. |
| Escopo autorizado | Limites explícitos de alvo, tempo e técnica. Estudo local não autoriza ações em terceiros. |

## Diferenças que você deve saber explicar

- parâmetro × argumento;
- valor igual × mesmo objeto;
- constante × objeto imutável;
- erro de sintaxe × exceção × erro lógico;
- stack de chamadas × estrutura de dados pilha;
- processo × thread × tarefa assíncrona;
- concorrência × paralelismo;
- status HTTP × código de saída de processo;
- autenticação × autorização;
- encoding × hash × criptografia;
- container × máquina virtual;
- teste unitário × integração × contrato;
- log × métrica × trace.
