# Referências e materiais complementares

O curso foi escrito para ser suficiente por si só. Use estes materiais para
ouvir outra explicação, consultar especificações e aprofundar tópicos. Links
foram selecionados por autoridade, acesso público e utilidade; uma referência
externa pode mudar ou sair do ar.

## Currículos e engenharia de software

- [ACM/IEEE-CS/AAAI Computer Science Curricula 2023](https://csed.acm.org/) —
  organização moderna das áreas essenciais da computação.
- [Knowledge Areas do CS2023](https://csed.acm.org/knowledge-areas/) — algoritmos,
  fundamentos de desenvolvimento, engenharia e sistemas.
- [SWEBOK Guide v4 (IEEE Computer Society)](https://ieeecs-media.computer.org/media/education/swebok/swebok-v4.pdf) —
  corpo de conhecimento de engenharia de software.
- [Software Engineering Stack Exchange](https://softwareengineering.stackexchange.com/) —
  discussões comunitárias; valide respostas pela documentação e pelo contexto.

## Algoritmos e estruturas de dados

- [Algorithms, 4th Edition](https://algs4.cs.princeton.edu/home/) — texto, código
  e exercícios de Princeton.
- [VisuAlgo](https://visualgo.net/en) — visualização interativa de estruturas e
  algoritmos.
- [CP-Algorithms](https://cp-algorithms.com/) — referência prática; confira as
  pré-condições antes de reutilizar implementações.
- [Open Data Structures](https://opendatastructures.org/) — livro aberto.
- [Algoritmos e Complexidade — NAU](https://www.nau.edu.pt/pt/curso/algoritmos-e-complexidade/) —
  curso em português.
- [Vídeos de Desenho e Análise de Algoritmos — DCC/FCUP](https://www.dcc.fc.up.pt/~pribeiro/aulas/daa2021/videos/index.html) —
  coleção universitária em português.
- [Estruturas de Dados e Algoritmos com Java — Loiane Groner](https://www.youtube.com/playlist?list=PLGxZ4Rq3BOBrgumpzz-l8kFMw2DLERdxi) —
  série prática; [código-fonte](https://github.com/loiane/estrutura-dados-algoritmos-java).
- [Big O — CFB Cursos](https://www.youtube.com/watch?v=vhvocEO3t74) — introdução
  em vídeo em português.
- [Python `heapq`](https://docs.python.org/3/library/heapq.html) e
  [Java `PriorityQueue`](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/util/PriorityQueue.html) —
  contratos e custos das filas de prioridade usadas nos exemplos.
- [.NET `PriorityQueue<TElement,TPriority>`](https://learn.microsoft.com/dotnet/api/system.collections.generic.priorityqueue-2) —
  contrato oficial da estrutura usada em C#.

## Medição e desempenho

- [Python `timeit`](https://docs.python.org/3/library/timeit.html) e
  [`profile`/`cProfile`](https://docs.python.org/3/library/profile.html) —
  medição e profiling na biblioteca padrão.
- [OpenJDK JMH](https://openjdk.org/projects/code-tools/jmh/) — harness para
  microbenchmarks na JVM, com aquecimento e controle do ciclo de medição.
- [BenchmarkDotNet](https://benchmarkdotnet.org/) — ferramenta do ecossistema
  .NET para experimentos reproduzíveis.
- [Node.js Performance Measurement APIs](https://nodejs.org/api/perf_hooks.html) —
  relógio, marcas e medidas do runtime.

Microbenchmark responde a uma pergunta estreita. Ele não substitui perfil do
sistema, modelo assintótico nem teste de requisito sob carga representativa.

## Design, arquitetura e refatoração

- [Refactoring.Guru: Design Patterns](https://refactoring.guru/design-patterns) e
  [Refactoring](https://refactoring.guru/refactoring) — catálogos visuais; padrões
  são opções, não obrigações.
- [Martin Fowler — Software Architecture Guide](https://martinfowler.com/architecture/) —
  artigos sobre decisões e estilos arquiteturais.
- [C4 Model](https://c4model.com/) — diagramas de contexto, contêiner, componente
  e código.
- [Quality Attributes — CMU Software Engineering Institute](https://www.sei.cmu.edu/library/quality-attributes/) —
  base para relacionar cenários mensuráveis a decisões arquiteturais.
- [Quality Attribute Workshops — SEI](https://www.sei.cmu.edu/library/quality-attribute-workshops-qaws-third-edition/) —
  método de elicitação com stakeholders antes de a arquitetura estar pronta.
- [Thoughtworks Technology Radar](https://www.thoughtworks.com/radar) — sinais da
  indústria; use como fonte de perguntas, não como lista de compras.
- [Fundamentos da Arquitetura de Software — Full Cycle](https://www.youtube.com/watch?v=Xt66rPTAWMs) —
  introdução em português.
- [Arquitetura de código, software e solução — Full Cycle](https://www.youtube.com/watch?v=6Q_uxdQJjJE) —
  distinções de escala.
- [Design Patterns — Filipe Deschamps](https://www.youtube.com/watch?v=arAz2Ff8s88) —
  contextualização em português.

## Testes, segurança e qualidade

- [Google Testing Blog](https://testing.googleblog.com/) — estratégias e relatos
  de engenharia de testes.
- [OWASP ASVS](https://owasp.org/projects/asvs/) — requisitos verificáveis de
  segurança de aplicações.
- [Semantic Versioning](https://semver.org/lang/pt-BR/) — política de versões para
  APIs públicas.
- [Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/) — estrutura de
  changelog orientada a consumidores.
- [Git bisect](https://git-scm.com/docs/git-bisect) — documentação oficial para
  localizar a mudança que alterou uma propriedade reproduzível.
- [Google Engineering Practices: code review](https://google.github.io/eng-practices/review/) —
  guias públicos de autor e revisor; adapte-os ao risco e ao contexto da equipe.

## Documentação oficial das linguagens

- [Python](https://docs.python.org/3/),
  [Java](https://docs.oracle.com/en/java/),
  [C (WG14)](https://www.open-std.org/jtc1/sc22/wg14/),
  [.NET/C#](https://learn.microsoft.com/dotnet/csharp/) e
  [JavaScript no MDN](https://developer.mozilla.org/pt-BR/docs/Web/JavaScript).

## Como avaliar uma fonte

1. Prefira especificação ou documentação oficial para comportamento exato.
2. Confira data, versão e pressupostos do ambiente.
3. Reproduza exemplos mínimos e leia erros completos.
4. Compare opinião de blog/fórum com fonte primária.
5. Nunca copie código sem entender licença, entradas e tratamento de falhas.
