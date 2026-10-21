# 10 — Observabilidade, auditoria e operação baseada em evidência

Uma automação observável responde: o que tentou, com qual versão, sobre qual
janela, quais efeitos confirmou, o que ficou incerto e como retomar. JSON por si
só não é log estruturado; estrutura exige schema e semântica estáveis.

## Objetivos

- projetar eventos versionados e correlacionáveis;
- distinguir log, métrica, trace, manifesto e audit trail;
- reconciliar operações sem registrar dados excessivos;
- criar alertas acionáveis, SLOs e runbooks;
- preservar evidência diante de falha do próprio sink de telemetria.

## 1. Cinco formas de evidência

| Tipo | Pergunta |
|---|---|
| evento/log | o que aconteceu nesta etapa? |
| métrica | com que frequência e distribuição? |
| trace | onde o tempo e a falha atravessaram componentes? |
| manifesto/relatório | qual era o plano e resultado do lote? |
| auditoria | quem ou qual identidade provocou qual efeito? |

Não tente usar um tipo para tudo. Log detalhado não substitui contador barato;
métrica agregada não explica um item; audit log não é debug irrestrito.

## 2. Evento estruturado

Defina nomes e campos estáveis:

~~~json
{
  "schemaVersion": 1,
  "timestamp": "2026-10-05T14:10:21.381Z",
  "severity": "INFO",
  "eventName": "fileflow.operation.completed",
  "serviceVersion": "1.2.0",
  "runId": "run-01J...",
  "operationId": "op-sha256...",
  "attempt": 1,
  "outcome": "succeeded",
  "durationMs": 42
}
~~~

Timestamp é o instante do evento; observedTimestamp pode ser o momento em que um
coletor o recebeu. Use UTC canônico. Duração deve vir de relógio monotônico, não da
subtração de relógio civil sujeito a ajuste.

EventName identifica a classe; message humana pode mudar ou ser localizada sem
quebrar consultas. Não use texto livre como chave de agregação.

## 3. Correlação e cardinalidade

Run ID liga a execução; operation ID liga o item; trace/span IDs ligam chamadas.
Propague correlação através de filas e HTTP segundo o contrato, sem aceitar um ID
externo ilimitado como nome de métrica.

Campos de alta cardinalidade, como item ID e URL, pertencem a logs/traces, não a
labels de métrica sem controle. Alta cardinalidade aumenta custo e pode tornar o
sistema de observação indisponível.

## 4. Outcome e taxonomia de erro

Use estados enumerados: succeeded, skipped, conflict, failed, uncertain, cancelled.
Erro tem classe estável e causa segura:

~~~text
INPUT_INVALID
DEPENDENCY_TIMEOUT
DEPENDENCY_PROTOCOL
PRECONDITION_CONFLICT
INTEGRITY_MISMATCH
STORAGE_UNAVAILABLE
INTERNAL_ERROR
~~~

Não transforme toda exceção em INTERNAL_ERROR se o operador precisa agir de forma
diferente. Tampouco exponha mensagem bruta de biblioteca como contrato.

## 5. Reconciliação do lote

Ao final, um evento de resumo inclui contagens e digest do plano:

~~~text
planned = succeeded + skipped + conflict + failed + uncertain + cancelled
~~~

Eventos por item ajudam a explicar; resumo ajuda a verificar completude. Se o
processo cair antes do resumo, o operador reconstrói a partir de checkpoint e
eventos, mas não deve inventar sucesso.

## 6. Métricas

Conjunto inicial:

- runs started/completed por outcome;
- items por outcome e tipo de operação;
- duration histogram por job;
- queue depth e idade do mais antigo;
- retries e rate-limit responses;
- checkpoint age;
- last successful logical window;
- dead-letter depth e oldest age.

Percentis explicam cauda melhor que média. Defina unidade no nome ou metadado e
não misture segundos com milissegundos.

## 7. Traces

Trace mostra caminho causal e tempo entre estágios. Crie spans para operações
significativas, não para cada linha trivial. Registre status e atributos limitados.

Sampling pode remover detalhes; auditoria e reconciliação essenciais não devem
depender de trace amostrado. Propagação de contexto de origem não confiável precisa
de validação e política.

## 8. Audit trail

Auditoria registra ator, ação, alvo lógico, decisão, resultado e momento. Proteja
acesso, integridade e retenção. Append-only na API não basta se a mesma identidade
pode apagar o armazenamento.

Hash encadeado detecta algumas alterações, mas não impede que quem controla todo o
arquivo refaça a cadeia. Para garantia forte, use armazenamento/identidade separada,
assinatura ou serviço de auditoria apropriado.

## 9. Privacidade e redação

Crie allowlist de campos. Evite payload, segredo, e-mail, caminho pessoal e URL com
query. Quando identificador for necessário, considere ID interno ou HMAC com chave
controlada; hash simples de conjunto pequeno pode ser revertido por enumeração.

Redação ocorre antes de serializar e antes de qualquer sink. Se o sink principal
falhar, o fallback não pode despejar o objeto original em stderr.

## 10. Falha do logger

Telemetria é uma dependência. Defina:

- evento de negócio pode prosseguir sem log remoto?
- existe buffer limitado?
- o que acontece ao encher?
- audit event essencial bloqueia commit ou usa outbox?
- fallback local é protegido e sanitizado?

Nunca cause recursão infinita ao tentar registrar a falha do logger. Use caminho
terminal mínimo e contador interno.

## 11. Alertas e SLOs

Alerta deve ligar sinal a impacto e ação. “Job falhou” é fraco. Melhor:

~~~text
Janela daily-sales de 2026-10-04 ainda não foi publicada 90 min após o prazo.
Impacto: relatório financeiro atrasado.
Verificar: runbook SALES-02, runId ..., checkpoint ...
~~~

Alertas úteis incluem janela atrasada, idade de fila, taxa de falha sustentada,
dead-letter antiga e ausência de sucesso. Evite alertar cada retry transitório.

Um SLO pode ser “99% das janelas diárias publicadas até 07:00 local, medidas por
30 dias”. Ele exige indicador, população, alvo e janela.

## 12. Runbook

Todo alerta aponta para um runbook com:

1. significado e impacto;
2. como confirmar o sinal;
3. consultas seguras e IDs necessários;
4. decisão entre aguardar, retomar, replay e escalar;
5. limites e ações proibidas;
6. recuperação e pós-verificação;
7. contatos e ownership;
8. data do último ensaio.

## Falhas e diagnóstico

| Sintoma | Causa | Correção |
|---|---|---|
| JSON impossível de consultar | schema instável | nomes/tipos versionados |
| custo explode | labels de alta cardinalidade | mover IDs para log/trace |
| sucesso sem itens | resumo antecipado | emitir após reconciliação |
| logger derruba job | sink no caminho crítico | buffer/fallback conforme contrato |
| alerta sem ação | sinal técnico isolado | impacto e runbook |

## Exercícios

### Nível 1 — schema

Defina cinco eventos e duas métricas. **Aceite:** campos têm tipo, semântica,
cardinalidade e regra de privacidade.

### Nível 2 — reconciliação

Gere eventos de lote com falha parcial. **Aceite:** contagens fecham e operador
localiza item sem payload sensível.

### Nível 3 — operação

Simule sink de logs indisponível e janela atrasada. **Aceite:** o sistema segue a
política declarada, fallback é seguro e alerta conduz a runbook ensaiado.

## Checklist

- [ ] Eventos possuem schema, versão e nomes estáveis.
- [ ] IDs de alta cardinalidade não viram labels irrestritas.
- [ ] Outcomes reconciliam o plano completo.
- [ ] Redação ocorre antes de todos os sinks.
- [ ] Falha da telemetria tem comportamento limitado.
- [ ] Alertas expressam impacto, janela e ação.

