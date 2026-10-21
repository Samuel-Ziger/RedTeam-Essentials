# 12 — Requisitos e modelagem: da necessidade ao contrato verificável

Requisitos conectam uma necessidade real a comportamento observável. Modelagem
transforma linguagem ambígua em conceitos, estados, relações e invariantes. Uma
lista de telas, endpoints ou tecnologias não cumpre nenhuma dessas funções.

Este capítulo usa o
[Dependency Planner](projetos/dependency-planner/README.md): uma aplicação local
que lê tarefas, valida o grafo e calcula ordem, lotes paralelos e caminho crítico.
Ela **não** executa nem acompanha tarefas. Essa fronteira de escopo é parte do
requisito, não detalhe de implementação.

## Objetivos

Ao concluir, você deverá conseguir:

- descobrir necessidades sem tratar a primeira solução sugerida como requisito;
- separar requisitos funcionais, regras, restrições e atributos de qualidade;
- escrever critérios com exemplos positivos, negativos e limites;
- criar linguagem ubíqua, modelo de domínio e máquina de estados;
- selecionar diagramas C4/UML pela pergunta que precisam responder;
- rastrear requisito até decisão, código, teste e evidência;
- administrar hipóteses e mudanças sem burocracia vazia.

## Pré-requisitos

Você já deve dominar funções, tipos, testes, JSON e Git, além dos capítulos de
[design modular](09-design-modular.md) e
[refatoração](11-refatoracao-legado.md). Abra também o código do Planner enquanto
estuda: requisito, modelo e implementação precisam usar o mesmo vocabulário.

## 1. Modelo mental: problema, necessidade, solução e evidência

Uma pessoa pode pedir “coloque um banco e um dashboard”. Isso é uma solução
proposta. A necessidade talvez seja comparar planos repetidamente, compartilhar
resultados ou auditar alterações. Cada necessidade admite soluções diferentes.

```text
contexto
  -> problema observado
  -> resultado desejado
  -> regra/restrição
  -> comportamento proposto
  -> critério verificável
  -> evidência em execução
```

Exemplo:

| Camada | Formulação |
|---|---|
| observação | planejadores montam a ordem manualmente e esquecem dependências |
| necessidade | detectar planos impossíveis antes de iniciar o trabalho |
| comportamento | rejeitar qualquer grafo que contenha ciclo |
| limite | arquivo local, no máximo 50 mil tarefas no cenário inicial |
| evidência | fixture cíclica termina com código 2 e informa caminho fechado |

## 2. Descoberta e elicitação

**Elicitar** não é apenas perguntar “o que você quer?”. Pessoas descrevem a
solução atual, omitem exceções habituais e discordam sobre palavras comuns.
Combine técnicas:

- entrevista semiestruturada para objetivos, exceções e responsabilidades;
- observação contextual do trabalho real;
- workshop para conflitos e decisões coletivas;
- análise de planilhas, tickets, logs, contratos e incidentes;
- protótipo descartável para revelar interpretação de fluxo;
- exemplos concretos e contraexemplos;
- event storming leve para fatos, comandos, políticas e dúvidas;
- análise de interfaces/sistemas que já impõem contratos.

### Perguntas que revelam regras

- O que dispara o planejamento?
- Qual é a menor entrada válida?
- O que nunca pode acontecer?
- Quem decide quando há empate?
- Qual erro precisa ser corrigido por quem?
- O que acontece se um item referenciar outro inexistente?
- “Duração” usa horas, pontos ou unidades abstratas?
- Duas execuções iguais precisam produzir bytes idênticos?
- Qual volume e tempo de resposta tornam a ferramenta útil?
- O resultado é decisão final ou apoio à decisão?

Para o Planner, uma descoberta importante é que `dependencies` contém
**pré-requisitos da tarefa**, não tarefas que dependem dela. Assim:

```json
{"id":"api","dependencies":["model"]}
```

significa “`model` termina antes de `api`”. No grafo interno, a aresta útil
para liberar trabalho vai de `model` para `api`. Sem essa definição, duas
implementações corretas de grafos podem produzir semânticas opostas.

### Registre fatos, hipóteses e decisões separadamente

```text
FATO-01: a entrada atual é um documento JSON local.
HIP-03: 50 mil tarefas cobrem 99% dos projetos esperados.
DEC-02: empates serão resolvidos por ID em ordem lexicográfica.
ABERTA-04: durações de tarefas paralelas compartilham algum recurso limitado?
```

Hipótese precisa de proprietário, evidência esperada e data/gatilho de revisão.
Não a transforme silenciosamente em fato.

## 3. Escopo, atores e fronteira

Um documento curto de visão deve responder:

- quem usa ou é afetado;
- qual decisão o sistema apoia;
- entradas e saídas;
- sistemas externos;
- o que está explicitamente fora;
- métricas de sucesso e riscos.

### Exemplo do Planner

**Atores**

- responsável pelo projeto: fornece tarefas e interpreta o plano;
- automação de CI: consome JSON e código de saída;
- mantenedor: diagnostica entrada inválida e evolui o contrato.

**Dentro do escopo**

- ler um único arquivo UTF-8 JSON;
- validar estrutura, tarefas e referências;
- detectar ciclo;
- calcular ordem determinística, lotes e caminho crítico;
- renderizar texto ou JSON.

**Fora do escopo atual**

- executar tarefas;
- considerar calendário, pessoas ou limite de recursos;
- atualizar progresso em tempo real;
- persistir histórico;
- otimizar custo com dependências opcionais.

Declarar não objetivos previne “só mais um campo” que muda a classe do problema.
Por exemplo, lotes paralelos significam “sem dependência pendente”, não que há
pessoas ou máquinas suficientes para executar tudo ao mesmo tempo.

## 4. Taxonomia prática de requisitos

### Requisito funcional

Comportamento que produz valor:

```text
RF-PLAN-03
O sistema deve rejeitar um grafo cíclico e informar um caminho fechado do ciclo.
```

### Regra de negócio

Condição verdadeira no domínio:

```text
RN-ITEM-02
Uma tarefa não pode depender de si nem repetir o mesmo pré-requisito.
```

### Atributo de qualidade

Forma mensurável de executar o comportamento:

```text
QA-DET-01
Dado o mesmo conjunto de tarefas válido, independentemente da ordem no arquivo,
a saída semântica deve ser determinística em 100 execuções.
```

### Restrição

Limite imposto:

```text
RES-IO-01
A versão atual opera offline e lê somente arquivos locais UTF-8.
```

### Requisito operacional

Como implantar, observar, recuperar e suportar:

```text
ROP-CLI-02
Erro esperado de entrada deve ir para stderr, não produzir resultado parcial em
stdout e terminar com código 2.
```

### Requisito de transição

Necessário durante mudança:

```text
RT-JSON-01
Durante uma versão de convivência, o leitor aceitará schemaVersion 1 e 2; o
escritor emitirá somente 2 e medirá leituras de 1 antes da remoção.
```

## 5. Atributos de qualidade como cenários

“Rápido”, “seguro” e “escalável” não orientam arquitetura. Um cenário inclui:

```text
fonte + estímulo + ambiente + artefato + resposta + medida
```

| Atributo | Cenário verificável do Planner |
|---|---|
| desempenho | em máquina de referência o caso de 50 mil tarefas e 200 mil arestas conclui em até 2 s no p95 de 20 execuções |
| determinismo | permutar a ordem da entrada não muda ordem, lotes, caminho crítico ou duração |
| confiabilidade | entrada inválida nunca produz plano parcial e sempre retorna erro categorizado |
| segurança | caminho e conteúdo malformado não causam traceback ao usuário nem escrita fora do destino |
| observabilidade | toda falha na borda informa fase, categoria e contexto não sensível |
| modificabilidade | adicionar adaptador CSV não altera `domain.py` nem `graph.py` |
| portabilidade | suíte obrigatória executa com a versão mínima de Python documentada |

Um número só é útil com ambiente, conjunto e método. “2 s” sem hardware,
warm-up, distribuição e repetição é marketing, não requisito.

### Conflitos entre qualidades

- mensagem de erro detalhada ajuda diagnóstico, mas pode expor caminho/dado;
- validação estrita encontra erro cedo, mas dificulta compatibilidade aditiva;
- determinismo por heap adiciona `log V`, mas melhora teste e reprodução;
- cache reduz latência, mas adiciona invalidação e estado;
- replicação aumenta disponibilidade, mas não é backup.

Registre prioridade e cenário, não prometa maximizar tudo.

## 6. Critérios de aceitação por exemplo

Formato Given–When–Then ajuda, mas não substitui regra formal:

```gherkin
Cenário: tarefas independentes ficam no mesmo lote
  Dado as tarefas "api" e "docs" sem dependências
  Quando o plano for calculado
  Então o primeiro lote será ["api", "docs"]
  E a ordem será determinística por ID
```

```gherkin
Cenário: ciclo é explicado
  Dado A depende de C, B depende de A e C depende de B
  Quando o arquivo for planejado
  Então nenhum plano será emitido em stdout
  E stderr conterá um caminho fechado como A -> B -> C -> A
  E o processo terminará com código 2
```

O caminho exato pode depender da política determinística; se o contrato aceita
qualquer ciclo real, o teste deve verificar que:

1. primeiro e último ID são iguais;
2. cada par consecutivo é uma aresta pré-requisito → dependente;
3. os IDs existem na entrada.

### Tabela de decisão

| JSON válido | referências existem | há ciclo | resultado |
|---|---|---|---|
| não | — | — | erro de estrutura, código 2 |
| sim | não | — | erro de referência, código 2 |
| sim | sim | sim | erro com ciclo fechado, código 2 |
| sim | sim | não | plano completo, código 0 |

Inclua fronteiras:

- projeto vazio;
- uma tarefa;
- ID duplicado;
- dependência repetida;
- autorreferência;
- duração zero, negativa, booleana ou não inteira;
- campo ausente/desconhecido;
- cadeia longa;
- muitos empates;
- múltiplos ciclos.

## 7. Linguagem ubíqua e glossário

Termos do Planner:

| Termo | Definição |
|---|---|
| tarefa/`WorkItem` | unidade imutável com ID, título, duração e pré-requisitos |
| dependência | pré-requisito que deve terminar antes da tarefa |
| dependente | tarefa liberada quando seus pré-requisitos terminam |
| DAG | grafo direcionado sem ciclos |
| ordem topológica | sequência em que todo pré-requisito precede dependente |
| lote | tarefas liberadas na mesma rodada lógica, sem limite de recursos |
| caminho crítico | cadeia de maior duração total segundo o modelo |
| duração mínima | duração do caminho crítico sob paralelismo ilimitado |

Evite sinônimos soltos como “etapa”, “job”, “nó” e “atividade” quando designam a
mesma coisa. “Nó” é útil ao falar do algoritmo; “tarefa” pertence ao domínio.

## 8. Modelo de domínio

### Entidade e objeto de valor

`WorkItem` possui identidade estável (`id`) e invariantes locais. A tupla de
dependências é um valor imutável. `Plan` é um resultado imutável:

```text
WorkItem
  id: TaskId
  title: NonBlankText
  duration: PositiveDuration
  dependencies: Set[TaskId]

Plan
  order: Sequence[TaskId]
  batches: Sequence[Sequence[TaskId]]
  criticalPath: Sequence[TaskId]
  minimumDuration: NonNegativeDuration
```

Na implementação atual, alguns objetos de valor são representados por primitivos
validados. Criar classes específicas só vale se centralizar regras, reduzir
ambiguidades ou impedir combinações inválidas.

### Invariantes locais e globais

Locais, verificáveis ao construir uma tarefa:

- ID e título não vazios;
- duração inteira positiva e não booleana;
- dependências como tupla de IDs não vazios;
- sem repetição e sem autorreferência.

Globais, verificáveis ao reunir o projeto:

- IDs únicos;
- toda referência aponta para uma tarefa existente;
- o grafo não contém ciclo.

Não force invariante global dentro de `WorkItem`: ela não possui o conjunto
completo. O limite correto evita dependência oculta.

### Estado: planejar não é executar

O fluxo da aplicação pode ser modelado assim:

```text
RECEIVED
  -> PARSED
  -> VALIDATED
  -> PLANNED
  -> RENDERED

PARSE_FAILED / VALIDATION_FAILED / CYCLE_DETECTED
  -> REPORTED
```

Já estados `pending/running/done` seriam de um **executor de tarefas**, produto
diferente. Se essa capacidade for adicionada, modele transições:

```text
PENDING -> READY -> RUNNING -> SUCCEEDED
                    |   |
                    |   +-> FAILED -> READY (retry permitido)
                    +-> CANCELLED
```

Defina guardas, idempotência e concorrência antes de adicionar campos ao Planner.

## 9. Diagramas que respondem perguntas

### C4 — contexto

Pergunta: quem usa e quais sistemas cercam a aplicação?

```text
[Responsável] -- arquivo JSON --> [Dependency Planner]
[CI] --------- invoca/consome --> [Dependency Planner]
[Dependency Planner] ---------> stdout/stderr + exit code
```

### C4 — contêiner

Hoje há um único processo CLI:

```text
[Arquivo JSON] -> [Processo Python/CLI] -> [Terminal ou pipeline]
```

Não desenhe banco, fila ou API que não existem. C4 descreve arquitetura atual ou
uma proposta claramente rotulada.

### Componentes

```text
cli -> PlanProject -> WorkItemRepository (porta)
 |         |                    ^
 |         v                    |
 |     build_plan       JsonWorkItemRepository
 |         |
 +------> Plan (formatação na borda)
```

### UML de sequência

```text
Usuário -> CLI: project.json --format json
CLI -> JsonRepository: construir(path)
CLI -> PlanProject: construir(repository)
CLI -> PlanProject: execute()
PlanProject -> JsonRepository: list_items()
JsonRepository -> WorkItem: construir/validar
JsonRepository --> PlanProject: items
PlanProject -> build_plan: items
build_plan --> PlanProject: Plan ou erro
PlanProject --> CLI: Plan
CLI --> Usuário: stdout + exit 0
```

Em erro, o fluxo alternativo termina em `stderr + exit 2`.

### Diagrama de estado

Use quando transições e guardas são a pergunta. Para estrutura estática, use
classe/ER. Para implantação, C4 deployment. Um único diagrama universal tende a
misturar níveis e envelhecer.

Todo diagrama precisa de:

- título/pergunta;
- escopo e nível;
- legenda;
- direção de dependência/fluxo;
- status “atual” ou “proposto”;
- dono e gatilho de atualização.

## 10. Rastreabilidade

Rastreabilidade útil permite responder “se esta regra mudar, onde verificar?”:

| ID | Regra | Código | Teste | Evidência |
|---|---|---|---|---|
| RN-ITEM-02 | sem autorreferência | `domain.WorkItem` | `test_rejects_self_dependency` | teste passa |
| RF-PLAN-03 | ciclo com caminho | `graph._cycle_path` | `test_reports_closed_cycle_path` | caminho fechado |
| ROP-CLI-02 | erro em stderr/código 2 | `cli.main` | `test_cycle_returns_expected_exit_code_and_stderr` | stdout vazio |
| QA-DET-01 | resultado determinístico | `graph._topological_order` | `test_every_generated_dag_preserves_edges_and_is_deterministic` | teste passa |

Não ligue toda linha de código a um ticket. Dê IDs estáveis às regras críticas e
mantenha links no requisito, teste, ADR ou PR. Automatize o que for verificável.

### Matriz de impacto

Ao propor “duração aceita decimal”:

- requisitos: unidade e arredondamento;
- domínio: tipo e validação;
- JSON: contrato e compatibilidade;
- algoritmo: soma/comparação;
- saída: representação;
- testes: limite, precisão e caminho empatado;
- documentação: schema e versionamento.

A matriz revela que uma alteração “pequena” cruza contratos.

## 11. Mudança e baseline

Um requisito passa por estados explícitos:

```text
proposto -> refinado -> aceito -> implementado -> verificado -> observado
                  \-> rejeitado/substituído
```

Para mudança relevante:

1. descreva motivação e evidência;
2. localize requisitos/ADRs/testes afetados;
3. classifique compatibilidade;
4. atualize exemplos antes ou junto do código;
5. defina rollout, telemetria e rollback;
6. registre a decisão.

“Aceito” não quer dizer eterno. Baseline é um ponto conhecido para discutir a
mudança, não proibição de aprender.

## 12. Falhas comuns e diagnóstico

| Sinal | Causa provável | Diagnóstico/correção |
|---|---|---|
| histórias vagas | conversa não virou exemplo | criar tabela de decisão e casos negativos |
| requisitos contraditórios | stakeholders/termos divergentes | workshop com exemplos e decisão registrada |
| teste não prova requisito | critério mede outra coisa | rastrear ID e revisar observação esperada |
| modelo imita JSON | transporte virou domínio | nomear invariantes antes dos campos |
| diagrama desatualizado | sem pergunta/dono | reduzir ao mínimo e revisar no PR |
| “não funcional” ignorado | sem cenário/medida | escrever estímulo, ambiente, resposta e métrica |
| escopo cresce sem controle | não objetivos ausentes | registrar fronteira e impacto da mudança |

Pergunta de revisão: **qual evidência faria este requisito ser considerado
atendido ou refutado?** Se ninguém consegue responder, ele ainda não está pronto.

## 13. Exercícios em três níveis

### Nível 1 — tornar verificável

1. Reescreva cinco desejos vagos do Planner como cenários mensuráveis.
2. Crie dez termos de glossário, incluindo dependência versus dependente.
3. Monte uma tabela de decisão para JSON inválido, referência ausente e ciclo.
4. Escreva três critérios positivos, três negativos e três de fronteira.

**Evidência:** outra pessoa consegue derivar entradas e resultados sem perguntar
o que você quis dizer.

### Nível 2 — modelar e rastrear

1. Desenhe contexto, contêiner, componentes e uma sequência de erro.
2. Separe invariantes locais e globais.
3. Crie IDs para oito requisitos e rastreie-os ao código/testes existentes.
4. Identifique duas lacunas reais da suíte sem alterar o projeto ainda.
5. Registre duas hipóteses com experimento e prazo de revisão.

**Evidência:** matriz de rastreabilidade aponta arquivo, teste e resultado
observável; diagramas distinguem atual de proposto.

### Nível 3 — conduzir uma mudança

Especifique “duração opcional em minutos decimais” **ou** “limite de recursos por
lote”, sem implementar:

1. descubra o problema e os atores;
2. declare não objetivos;
3. modele novos estados/invariantes;
4. identifique se o problema algorítmico muda;
5. classifique compatibilidade do JSON/CLI;
6. escreva critérios e atributos de qualidade;
7. produza matriz de impacto, risco e rollout;
8. defenda aceitar ou rejeitar a proposta.

**Evidência:** revisão por outra pessoa encontra todas as mudanças de contrato e
consegue discordar usando premissas explícitas.

## Checklist de domínio

- [ ] Distingo necessidade, solução, requisito, regra e restrição.
- [ ] Uso pelo menos duas técnicas de elicitação e comparo suas evidências.
- [ ] Requisitos funcionais têm exemplos, erros e fronteiras.
- [ ] Atributos de qualidade incluem contexto, estímulo, resposta e medida.
- [ ] Termos do domínio significam a mesma coisa em texto, código e testes.
- [ ] Invariantes locais e globais estão no limite correto.
- [ ] Diagramas C4/UML respondem perguntas e indicam estado atual/proposto.
- [ ] Requisitos críticos chegam a teste e evidência executável.
- [ ] Hipóteses possuem dono e gatilho de revisão.
- [ ] Mudanças têm análise de impacto, compatibilidade e rollback.

Avance para [Arquitetura de software](13-arquitetura.md), onde esses cenários se
transformam em limites e decisões de longo alcance.
