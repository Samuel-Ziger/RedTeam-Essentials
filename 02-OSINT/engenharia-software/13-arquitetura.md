# 13 — Arquitetura de software: limites, qualidades e evolução

Arquitetura é o conjunto de decisões que condiciona atributos de qualidade e é
caro mudar: limites de domínio, direção das dependências, propriedade dos dados,
comunicação, implantação e operação. Não é sinônimo de microserviços, framework
ou diagrama com muitas caixas.

O [Dependency Planner](projetos/dependency-planner/README.md) começa como um
monólito modular de linha de comando. Esse ponto de partida permite estudar
arquitetura sem introduzir rede e distribuição antes que exista uma necessidade.

## Objetivos

Ao concluir, você deverá conseguir:

- derivar decisões arquiteturais de cenários de qualidade;
- distinguir camadas, arquitetura hexagonal, Clean Architecture e módulos;
- preservar a regra de dependência em um monólito modular;
- avaliar quando eventos ou serviços distribuídos compensam seus custos;
- projetar consistência, idempotência, resiliência e degradação;
- aplicar threat modeling nas fronteiras de confiança;
- desenhar observabilidade a partir de SLOs;
- registrar e revisar decisões com ADRs e evidência.

## Pré-requisitos e modelo mental

Conclua [Requisitos e modelagem](12-requisitos-modelagem.md) e revise
[Design modular](09-design-modular.md). Use este encadeamento:

```text
drivers de negócio e restrições
  -> cenários de qualidade priorizados
  -> decisões e limites
  -> implementação
  -> sinais em execução
  -> revisão da decisão
```

Arquitetura não elimina trade-offs; torna-os visíveis e testáveis. Uma decisão
correta para equipe de duas pessoas e ferramenta offline pode ser incorreta para
uma plataforma multi-tenant 24×7.

## 1. Drivers arquiteturais

Liste antes de desenhar:

- capacidades do domínio e invariantes;
- volume, distribuição e picos;
- latência, disponibilidade e consistência;
- confidencialidade, integridade e auditoria;
- frequência de mudança;
- tamanho/experiência da equipe;
- orçamento, prazo e tecnologias operáveis;
- integrações e legado;
- requisitos de recuperação;
- decisões ainda incertas.

### Cenário de qualidade

```text
Fonte: pipeline de CI
Estímulo: envia um arquivo válido com 50 mil tarefas e 200 mil arestas
Ambiente: máquina de referência, sem cache prévio, uma execução por processo
Artefato: CLI do Planner
Resposta: valida e produz JSON completo, sem ordem não determinística
Medida: p95 <= 2 s em 20 execuções; memória máxima <= 512 MiB
```

Esse cenário pode justificar lista de adjacência e algoritmo aproximadamente
`O(V + E + V log V)`. Ele não justifica banco, fila ou microserviço.

### Priorize tensões

| Decisão | Favorece | Cobra |
|---|---|---|
| validação estrita do JSON | segurança e erro precoce | evolução aditiva exige versão |
| heap para desempate | determinismo | fator `log V` |
| processo único | simplicidade/transação local | escala/implantação conjunta |
| saída síncrona | contrato simples | não serve a trabalhos muito longos |
| evento assíncrono | desacoplamento temporal | ordem, duplicidade e observabilidade |

Se tudo é prioridade máxima, nada orienta a decisão.

## 2. Arquitetura atual do Dependency Planner

```text
                    política
       +--------------------------------+
       | domain.py       graph.py       |
       | WorkItem/Plan   build_plan     |
       +---------------^----------------+
                       |
                 service.py
                 PlanProject
                       ^
                       | porta
                    ports.py
              WorkItemRepository
                       ^
                       |
       +---------------+----------------+
       | JsonWorkItemRepository         |
       | cli.py (composition root/UI)    |
       +--------------------------------+
                    mecanismos
```

Fluxo de execução aponta para fora quando o caso de uso lê arquivo, mas
**dependência de código** aponta para a política: `PlanProject` conhece a porta,
não o adaptador concreto. `cli.py` monta tudo no composition root.

Invariantes arquiteturais:

- `domain.py` e `graph.py` não importam CLI, arquivo ou JSON;
- o adaptador traduz estrutura externa para `WorkItem`;
- o caso de uso retorna `Plan`, não texto terminal;
- a CLI converte exceções esperadas em stderr e código de saída;
- trocar entrada não altera algoritmo.

Transforme essas regras em testes de arquitetura ou verificação de imports se o
projeto crescer.

## 3. Camadas, hexagonal e Clean Architecture

Esses estilos se sobrepõem, mas enfatizam problemas diferentes.

### Camadas

```text
apresentação -> aplicação -> domínio -> persistência
```

É simples, desde que a dependência não volte para cima e o domínio não vire um
conjunto anêmico de estruturas. Uma pasta por camada global pode reduzir coesão
em sistemas grandes.

### Ports and Adapters (hexagonal)

O núcleo expõe portas definidas pelas necessidades dos casos de uso. Adaptadores
convertem CLI, HTTP, JSON ou banco para essas portas:

```text
adaptador de entrada -> caso de uso -> porta de saída <- adaptador de saída
```

No Planner, `WorkItemRepository` é uma porta de saída consumida pelo caso de
uso; `JsonWorkItemRepository` é adaptador. Uma futura API é outro adaptador de
entrada.

### Clean Architecture

Enfatiza círculos concêntricos e a **regra de dependência**: detalhes apontam
para políticas internas; entidades/casos de uso não conhecem frameworks. Dados
cruzam limites por estruturas próprias, sem vazar objetos de ORM ou request.

### O que não fazer

- criar uma interface para toda classe sem volatilidade;
- fazer o domínio depender de DTO do framework;
- esconder SQL/rede atrás de “repository” genérico que oferece qualquer query;
- converter três funções puras em dezenas de classes cerimoniais;
- duplicar modelo em cada camada sem diferença semântica.

Arquitetura deve reduzir custo de mudança real, não maximizar quantidade de
abstrações.

## 4. Monólito modular como padrão inicial

Um monólito modular é uma unidade implantável com módulos coesos e limites
internos explícitos. Benefícios:

- chamada local e depuração direta;
- transação local;
- testes/implantação simples;
- refatoração de limites enquanto o domínio amadurece;
- menor custo operacional.

Riscos:

- imports cruzados corroem limites;
- banco compartilhado vira interface informal;
- implantação conjunta pode limitar equipes/cargas independentes;
- uma falha de recurso pode afetar o processo inteiro.

Mitigações: APIs de módulo pequenas, testes de dependência, ownership, orçamento
de recursos e métricas por capacidade.

### Quando extrair um serviço

Exija evidência:

- limite de domínio estável e com proprietário;
- necessidade real de escala/implantação/isolamento independente;
- contrato e dados sob controle;
- equipe opera rede, observabilidade, segurança e falha parcial;
- benefício supera consistência distribuída e custo cognitivo.

“O módulo está bagunçado” é motivo para modularizar, não distribuí-lo.

## 5. Evolução proposta: API sem contaminar o núcleo

Uma API HTTP poderia chamar o mesmo `PlanProject`:

```text
HTTP request
  -> limite de body e autenticação
  -> DTO/validação de transporte
  -> InMemoryWorkItemRepository ou comando
  -> PlanProject.execute()
  -> Plan
  -> DTO HTTP + status
```

Decisões:

- o domínio não importa o framework;
- JSON HTTP e JSON de arquivo podem ter contratos/versionamentos diferentes;
- erro de ciclo vira erro estruturado, não traceback;
- limite de tarefas/arestas é validado antes de alocar estruturas enormes;
- timeout/cancelamento protege o servidor;
- saída determinística ajuda cache e testes.

Adicionar um adaptador em memória apenas para encaixar a porta atual pode ser
aceitável, mas talvez o caso de uso devesse receber itens diretamente e outro
caso de uso orquestrar repositório. Portas devem refletir necessidades, não
congelar o primeiro design.

## 6. Event-driven: fatos, entrega e ordem

Arquitetura orientada a eventos desacopla no tempo. Use quando consumidores
precisam reagir independentemente, o produtor não precisa da resposta síncrona e
a janela de consistência é aceitável.

Exemplo futuro:

```text
PlanRequested -> worker calcula -> PlanCompleted ou PlanRejected
```

Contrato de evento:

```json
{
  "eventId": "evt-01J...",
  "eventType": "plan.completed",
  "schemaVersion": 1,
  "occurredAt": "2026-10-03T14:00:00Z",
  "correlationId": "req-01J...",
  "planId": "plan-42",
  "inputDigest": "sha256:..."
}
```

Questões obrigatórias:

- entrega pode duplicar? consumidor é idempotente?
- ordem é global, por `planId` ou inexistente?
- evento perdido pode ser reconstruído?
- quem versiona e deprecia o schema?
- por quanto tempo reter?
- como medir lag e poison messages?
- o que usuário vê enquanto processa?

Evento não é chamada remota disfarçada. Se o produtor bloqueia aguardando o
mesmo resultado imediato, RPC síncrona pode ser mais honesta.

### Outbox

Quando estado e evento precisam nascer juntos:

```text
transação local:
  salvar plano
  inserir outbox(eventId, payload)
commit

publicador:
  lê pendentes
  publica com retry
  marca progresso
```

Entrega pode ocorrer mais de uma vez; consumidor deduplica. Outbox resolve a
janela do dual write, não exatamente-once nem ordenação universal.

## 7. Distribuição e consistência

Separar serviços troca chamada local por uma rede que:

- atrasa, perde, duplica ou reordena mensagens;
- pode concluir no servidor depois de timeout no cliente;
- cria versões incompatíveis;
- falha parcialmente;
- exige identidade e criptografia entre serviços.

Defina consistência por operação:

| Operação | Garantia possível |
|---|---|
| criar solicitação com chave idempotente | uma intenção lógica, mesmo sob retry |
| consultar status logo após criar | read-your-writes ou resposta com estado conhecido |
| projetar relatório | atraso até 30 s, com métrica e reconciliação |
| publicar evento | at-least-once + consumidor idempotente |

Sagas coordenam transações locais por passos/compensações. Compensar não é
voltar no tempo: email enviado ou artefato consumido pode exigir ação de negócio,
não rollback técnico.

Para o Planner local, distribuição é custo sem benefício atual. Documentar isso
é decisão arquitetural válida.

## 8. Resiliência por orçamento

### Timeout

Toda chamada remota tem deadline. O timeout externo deve deixar tempo para
camadas internas falharem de forma controlada:

```text
deadline do cliente: 3 s
gateway: 2,8 s
serviço: 2,4 s
dependência: 1,5 s
```

Valores vêm de SLO e distribuição, não desta ilustração.

### Retry

Somente para falha transitória classificada e operação idempotente:

- tentativas limitadas;
- backoff exponencial com jitter;
- respeito ao deadline total;
- nova conexão/transação quando exigido;
- métrica por motivo/tentativa.

Retry em todas as camadas multiplica carga. Defina um dono.

### Circuit breaker

Interrompe tentativas temporariamente quando a dependência falha. Precisa de
estado, janela, limiar, half-open e métrica. Não substitui timeout nem corrige
erro permanente.

### Bulkhead, fila e backpressure

Isole pools por dependência/carga crítica. Fila deve ter limite; quando cheia,
rejeite, degrade ou aplique pressão ao produtor. Fila ilimitada transforma
sobrecarga em latência e falta de memória.

### Degradação

Se o adaptador de auditoria falhar, o plano pode ser devolvido? Depende de a
auditoria ser obrigatória. Declare:

- capacidade essencial;
- dado que pode ficar obsoleto;
- comportamento visível;
- duração máxima;
- recuperação/reconciliação.

## 9. Threat modeling

Segurança começa no contexto e nas fronteiras de confiança:

```text
arquivo não confiável -> parser/validador -> domínio
argumentos CLI --------> roteamento/formato
filesystem ------------> leitura
stdout/stderr ----------> pipeline/log
```

Use STRIDE como checklist, não como substituto de análise:

| Categoria | Exemplo no Planner/API | Controle |
|---|---|---|
| Spoofing | cliente/API sem identidade | autenticação quando houver serviço |
| Tampering | arquivo alterado | origem/permissão/digest quando requisito |
| Repudiation | não saber quem solicitou | auditoria com identidade e request ID |
| Information disclosure | traceback ou leitura de caminho arbitrário | mensagens controladas, raiz permitida e processo sem privilégios |
| Denial of service | grafo/JSON gigante ou profundo | limites antes do processamento |
| Elevation of privilege | runtime comum usa papel administrativo | papéis separados e autorização centralizada |

Para cada ameaça, registre ativo, ator, precondição, impacto e controle. Priorize
por risco e valide o controle. Não registre o conteúdo completo de projetos se
puder conter informação sensível.

## 10. Observabilidade orientada a perguntas

Logs, métricas e traces têm funções diferentes:

- **log:** evento discreto com contexto;
- **métrica:** série agregável para tendência/alerta;
- **trace:** caminho de uma operação por componentes.

Para uma futura API:

- SLIs: taxa de sucesso válido, latência p95/p99, saturação de workers;
- métricas de domínio: tarefas/arestas por plano, ciclos, duração calculada;
- logs: `request_id`, versão, categoria de erro, sem payload;
- trace: validação, construção do grafo e renderização;
- alertas: derivados de SLO e impacto, não de qualquer exceção.

Exemplo de SLO:

```text
99,5% das solicitações válidas com até 10 mil tarefas completam em menos de
800 ms numa janela móvel de 28 dias.
```

O error budget orienta ritmo de mudança e trabalho de confiabilidade. Não use
média para esconder cauda. Alta cardinalidade, como `planId`, deve ir a logs/
traces, não a labels de métricas sem limite.

Na CLI local, sinais ainda importam: duração, tamanho da entrada, exit code e
categoria de erro podem ser medidos pelo chamador, preservando privacidade.

## 11. ADRs

Um Architecture Decision Record registra uma decisão, não toda a arquitetura:

```markdown
# ADR-001 — Manter o Planner como monólito modular

Status: aceito
Data: 2026-10-03

## Contexto
Equipe pequena; processamento local; até 50 mil tarefas; domínio em evolução.

## Drivers
Determinismo, execução offline, baixo custo operacional e adaptadores trocáveis.

## Opções
1. monólito modular;
2. API única;
3. workers orientados a eventos.

## Decisão
Um processo com domínio/algoritmo independentes das bordas.

## Consequências
Implantação e depuração simples; escala junto; sem histórico compartilhado.

## Evidência e revisão
Revisar se p95 exceder SLO, houver múltiplos clientes remotos ou necessidade
comprovada de isolamento/implantação independente.
```

ADRs devem ser imutáveis como histórico; uma nova decisão substitui a antiga e
liga os documentos. Status úteis: proposto, aceito, rejeitado, substituído.

## 12. Diagnóstico arquitetural

| Sintoma | Suspeita | Evidência |
|---|---|---|
| regra exige filesystem no teste | detalhe vazou ao núcleo | grafo de imports/teste unitário |
| toda mudança toca todos os módulos | limites sem coesão | histórico de commits |
| timeout gera trabalho duplicado | retry sem idempotência | correlation/idempotency IDs |
| fila cresce continuamente | sem backpressure/capacidade | idade e tamanho da fila |
| erro não localizável | contexto/telemetria insuficiente | logs/traces e request ID |
| deploy de um módulo quebra outro | contrato implícito | testes de contrato/versionamento |
| microserviços compartilham tabelas | propriedade de dados falsa | acessos e migrations |
| alertas constantes sem impacto | sinais sem SLO | relação alerta–incidente |

Arquitetura se avalia em mudanças e falhas reais, não apenas no desenho.

## 13. Exercícios em três níveis

### Nível 1 — ler a arquitetura atual

1. Desenhe C4 contexto, contêiner e componentes do Planner.
2. Gere o grafo de imports e marque a direção das dependências.
3. Escreva quatro cenários de qualidade mensuráveis.
4. Registre um ADR que mantenha o monólito modular.

**Evidência:** diagramas correspondem ao código; cada decisão cita um driver.

### Nível 2 — evoluir uma borda

Projete um adaptador CSV ou HTTP sem implementar:

1. contrato e validação na borda;
2. porta/caso de uso afetado;
3. limites de recurso e threat model;
4. testes de contrato;
5. sinais e SLO;
6. compatibilidade/rollback.

**Evidência:** `domain.py` e `graph.py` permanecem independentes; o diagrama
mostra composition root e fluxo de erro.

### Nível 3 — avaliar distribuição

Compare três opções para planos demorados: síncrona, job assíncrono no mesmo
serviço e event-driven distribuída. Para cada uma, modele:

- consistência e estado visível;
- timeout/retry/idempotência;
- fila/backpressure;
- ameaça e autorização;
- observabilidade;
- recuperação;
- custo operacional e condição de adoção.

Produza ADR e revisão crítica por outra pessoa. A conclusão “não distribuir
agora” é válida quando sustentada.

## Checklist de domínio

- [ ] Decisões partem de cenários de qualidade priorizados.
- [ ] Distingo fluxo de execução de dependência de código.
- [ ] Sei explicar camadas, hexagonal e Clean sem tratá-las como sinônimos.
- [ ] O monólito possui módulos e invariantes arquiteturais verificáveis.
- [ ] Extração de serviço exige evidência de domínio e operação.
- [ ] Eventos têm identidade, versão, ordem, retry e reconciliação.
- [ ] Toda chamada remota possui deadline; retry tem dono e idempotência.
- [ ] Threat model cobre fronteiras, ativos, abuso e controles verificáveis.
- [ ] Logs, métricas e traces respondem a SLOs e preservam dados.
- [ ] ADR contém contexto, opções, consequências e gatilho de revisão.

Continue em [Testes e qualidade](14-testes-qualidade.md), onde as decisões passam
a ter evidência automatizada.
