# Glossário de dados e APIs

Use este arquivo para revisão, não como substituto dos capítulos. Quando dois
termos parecem sinônimos, a diferença costuma definir uma garantia importante.

## Modelagem e persistência

- **Agregado:** conjunto de objetos tratado como uma fronteira de consistência;
  alterações externas passam pela raiz do agregado.
- **Atributo:** propriedade de uma entidade ou relação no modelo conceitual.
- **Cardinalidade:** quantidade permitida de elementos numa relação (`1:1`,
  `1:N`, `N:M`) ou estimativa/distribuição de valores numa coluna.
- **Chave candidata:** conjunto mínimo de atributos que identifica uma linha;
  uma delas pode ser escolhida como chave primária.
- **Chave natural:** identificador com significado no domínio, como um código
  regulado; pode mudar por regras externas.
- **Chave substituta:** identificador sem significado de negócio, como UUID ou
  sequência; não elimina a necessidade de unicidade natural quando ela existe.
- **Constraint:** regra declarativa que impede estados inválidos no banco, como
  `NOT NULL`, `CHECK`, `UNIQUE`, `PRIMARY KEY` e `FOREIGN KEY`.
- **DDL:** linguagem que define estrutura, como `CREATE`, `ALTER` e `DROP`.
- **DML:** linguagem que consulta ou altera dados, como `SELECT`, `INSERT`,
  `UPDATE` e `DELETE`.
- **Dado derivado:** valor calculado a partir de uma fonte canônica; deve ser
  reconstruível ou possuir regra explícita de sincronização.
- **Desnormalização:** duplicação deliberada para um acesso medido, aceitando
  custo de atualização e risco de divergência.
- **Entidade:** conceito com identidade e ciclo de vida próprios no domínio.
- **Fonte de verdade:** armazenamento autorizado a decidir o valor canônico de
  um fato; cópias e caches não competem com ela.
- **Invariante:** condição que deve permanecer verdadeira em todo estado
  confirmado, inclusive sob concorrência e retry.
- **Migration:** mudança versionada, ordenada e reproduzível de schema ou dados.
- **Modelo conceitual:** descreve conceitos e relações sem detalhes do banco.
- **Modelo lógico:** traduz conceitos para entidades, atributos, chaves e regras
  de um paradigma, ainda sem todos os detalhes operacionais.
- **Modelo físico:** define tipos, tabelas/coleções, índices, partições e opções
  concretas de um produto/versão.
- **Normalização:** decomposição orientada por dependências para reduzir
  redundância e anomalias de inserção, alteração e exclusão.
- **Schema:** estrutura, tipos e regras esperados dos dados, impostos pelo banco,
  pela aplicação ou por ambos.
- **Valor-objeto:** valor definido pelos seus atributos, sem identidade
  independente, como dinheiro com quantia e moeda.

## SQL, consultas e desempenho

- **CTE:** resultado nomeado introduzido por `WITH`; melhora composição e pode
  ser recursivo, mas não é automaticamente mais rápido.
- **Cobertura de índice:** capacidade de responder uma consulta usando dados do
  índice, condicionada ao plano e à visibilidade das linhas.
- **Custo estimado:** unidade relativa do planner para comparar planos; não é
  milissegundo nem promessa de latência.
- **Estatística:** resumo de distribuição/cardinalidade usado pelo otimizador;
  dado desatualizado pode produzir estimativa ruim.
- **Execução parametrizada:** envio separado de SQL e valores ao driver; evita
  injeção de dados como sintaxe e preserva tipos.
- **Índice:** estrutura auxiliar que acelera certos acessos em troca de espaço,
  escrita, cache e manutenção.
- **Índice composto:** índice com várias chaves cuja ordem precisa refletir
  igualdade, ordenação e faixa das consultas relevantes.
- **Índice parcial:** inclui somente linhas que satisfazem um predicado; o
  planner precisa provar que a consulta implica esse predicado.
- **Join:** combina linhas por uma condição; tipo de join define o que ocorre
  com linhas sem correspondência.
- **N+1:** uma consulta inicial seguida de uma consulta por item, aumentando
  round trips e carga de forma proporcional ao resultado.
- **Planner/otimizador:** componente que estima alternativas e escolhe um plano
  de execução para a consulta.
- **SARGable:** predicado que permite busca eficiente por uma estrutura de
  acesso; aplicar função à coluna pode impedir o uso direto do índice.
- **Sequential scan:** leitura sequencial da relação; pode ser a melhor escolha
  quando grande parte das linhas será lida.
- **Window function:** calcula sobre uma janela de linhas sem colapsá-las como
  um `GROUP BY` faria.

## Transações e concorrência

- **ACID:** atomicidade, consistência, isolamento e durabilidade; cada termo
  descreve uma garantia diferente, não um selo binário do produto.
- **Atomicidade:** todos os efeitos da transação confirmam ou nenhum confirma.
- **Compare-and-set:** altera somente se a versão/valor ainda for o esperado;
  zero linhas alteradas representa conflito ou ausência a distinguir.
- **Deadlock:** ciclo de esperas por locks; o banco aborta uma participante e a
  aplicação decide se a operação pode ser repetida.
- **Durabilidade:** depois do commit reportado, a mudança sobrevive aos tipos de
  falha cobertos pela configuração de persistência/replicação.
- **Isolamento:** limita quais efeitos concorrentes uma transação observa; seu
  significado depende do nível e da implementação do banco.
- **Lock:** reserva coordenada sobre recurso ou intervalo; granularidade, ordem
  e duração influenciam correção e contenção.
- **Lost update:** uma escrita substitui silenciosamente outra baseada em estado
  lido anteriormente.
- **MVCC:** controle de concorrência por versões que fornece snapshots e reduz
  conflito entre leitura e escrita; versões antigas ainda precisam de limpeza.
- **Rollback:** desfaz efeitos não confirmados da transação; não desfaz chamada
  externa que já ocorreu.
- **Savepoint:** ponto interno que permite desfazer parte da transação sem
  encerrar todo o bloco.
- **Snapshot:** visão consistente das versões visíveis para uma operação ou
  transação.
- **Write skew:** duas transações alteram linhas distintas após observar uma
  condição compartilhada, quebrando uma invariante entre linhas.

## NoSQL e sistemas distribuídos

- **BSON:** representação binária de documentos usada pelo MongoDB, com tipos
  adicionais aos existentes em JSON.
- **Consistência eventual:** réplicas/projeções podem divergir temporariamente,
  mas existe processo e condição de convergência definidos.
- **Documento:** agregado persistido como estrutura de campos e valores; sua
  flexibilidade não remove schema ou limite de crescimento.
- **Embed:** armazena dados relacionados no mesmo documento para leitura e
  atomicidade conjuntas, aceitando duplicação/crescimento.
- **Idempotent consumer:** registra identidade do evento/operação para que
  entrega repetida não repita o efeito.
- **NoSQL:** conjunto de famílias cujo modelo principal não é relacional,
  incluindo chave-valor, documentos, colunar e grafo.
- **Outbox transacional:** grava evento e mudança de domínio na mesma transação;
  um worker publica depois, normalmente com entrega ao menos uma vez.
- **Particionamento/sharding:** distribui dados por uma chave; acessos fora
  dessa chave podem exigir fan-out e coordenação.
- **Projeção:** cópia derivada, otimizada e reconstruível de eventos ou fonte
  canônica.
- **Read concern/write concern:** garantias solicitadas pelo cliente MongoDB
  para visibilidade de leituras e confirmação de escritas.
- **Reference:** guarda identidade de dado relacionado em outro documento;
  reduz crescimento/duplicação, mas exige consulta ou coordenação adicional.
- **Replica:** cópia do estado para disponibilidade/leitura; replicação não
  substitui backup contra exclusão ou corrupção lógica.
- **TTL:** tempo após o qual um dado pode expirar; remoção costuma ser
  assíncrona, portanto não é deadline exato.

## HTTP e contratos de API

- **Autenticação:** estabelece qual principal realizou a requisição.
- **Autorização:** decide se aquele principal pode executar a ação naquele
  recurso e contexto.
- **Cache validator:** metadado como ETag ou data usado para validar uma
  representação sem transferi-la novamente.
- **Cursor:** token opaco que identifica a continuação de uma ordenação
  estável; não deve ser interpretado pelo consumidor.
- **ETag:** validador HTTP de uma representação; com `If-Match`, pode expressar
  precondição para impedir sobrescrita concorrente.
- **Idempotência:** repetir a mesma intenção produz o mesmo efeito pretendido;
  respostas e logs podem diferir.
- **Idempotency key:** identidade fornecida para associar retries de uma
  operação não idempotente ao primeiro resultado persistido.
- **Media type:** identifica o formato e a semântica do corpo, por exemplo
  `application/json` ou `application/problem+json`.
- **OpenAPI:** descrição legível por humanos e ferramentas de uma interface HTTP;
  não substitui teste da implementação real.
- **Precondição:** condição HTTP avaliada antes de executar o método, como
  `If-Match`; falha normalmente produz `412`.
- **Problem Details:** formato padronizado para erros de API com tipo, título,
  status, detalhe, instância e extensões controladas.
- **Recurso:** conceito identificado por URI; representação é uma forma de
  descrever seu estado, não o recurso em si.
- **Safe method:** método cuja semântica solicitada é somente leitura, embora
  logs e contadores internos ainda possam mudar.
- **Versionamento:** política para evoluir contrato preservando consumidores;
  número em URI é apenas um mecanismo possível.

## Arquitetura, testes e operação

- **ADR:** registro curto de contexto, decisão, alternativas e consequências de
  uma escolha arquitetural.
- **Backpressure:** mecanismo para limitar ou desacelerar entrada quando a
  capacidade a jusante está saturada.
- **Contract test:** verifica comportamento observável entre consumidor e
  provedor, independentemente de detalhes internos.
- **DTO:** estrutura da fronteira de transporte; não deve carregar por acidente
  objetos de driver, campos internos ou lazy loading.
- **Health/liveness:** indica se o processo está vivo e capaz de continuar seu
  ciclo; não garante dependências prontas.
- **Readiness:** indica se a instância deve receber tráfego naquele momento.
- **Pool:** conjunto limitado de conexões reutilizáveis; seu tempo de espera é
  um sinal de saturação.
- **RPO:** quantidade máxima de dados que pode ser perdida, expressa em tempo ou
  ponto de recuperação.
- **RTO:** tempo máximo para restaurar a capacidade definida após falha.
- **SLI:** medida de comportamento do serviço, como proporção de requests
  válidos abaixo de uma latência.
- **SLO:** alvo para um SLI durante uma janela; orienta risco e prioridade.
- **Trace/span:** trace representa o caminho causal; span representa uma
  operação com duração e contexto dentro dele.
- **Unidade de trabalho:** fronteira que coordena repositórios e uma transação
  para um caso de uso.

## Distinções para memorizar

| Não confunda | Diferença essencial |
|--------------|---------------------|
| autenticação e autorização | identidade versus permissão contextual |
| validação e invariante | formato de entrada versus estado sempre válido |
| recurso e representação | identidade/semântica versus corpo transferido |
| idempotência e deduplicação | efeito pretendido versus mecanismo possível |
| replicação e backup | disponibilidade versus recuperação independente |
| liveness e readiness | processo vivo versus apto a receber tráfego |
| estimativa e medição | modelo do planner versus execução observada |
| schema flexível e sem schema | estrutura evolutiva versus estado arbitrário |
| timeout e cancelamento | parar de esperar versus desfazer efeito remoto |
| consistência eventual e acaso | convergência definida versus divergência sem controle |
