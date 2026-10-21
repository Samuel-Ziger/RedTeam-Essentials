# 14 — Dados, transações e consistência

Uma resposta de API promete algo sobre estado. Essa promessa precisa caber nas
garantias do armazenamento, réplicas, filas e parceiros. Distribuir dados sem
declarar ownership transforma falhas normais em inconsistência misteriosa.

## Objetivos

- definir unidade atômica e ownership;
- escolher consistência forte ou eventual por invariante;
- aplicar outbox, inbox, saga e reconciliação;
- lidar com leitura após escrita e duplicidade;
- expor estado incerto sem mentir ao consumidor.

## 1. Invariantes e fronteira transacional

Uma transação protege invariantes dentro de seu limite. Se pedido e estoque
pertencem a bancos distintos, não existe commit atômico gratuito. Opções:

- redesenhar ownership para mesma unidade;
- reservar e confirmar com estados explícitos;
- saga com compensações de negócio;
- aceitar consistência eventual;
- coordenar protocolo distribuído quando custo justifica.

Antes de escolher padrão, escreva o invariante: “estoque nunca negativo” pode
exigir decisão no owner do estoque; “tela atualiza em até 5 s” aceita propagação.

## 2. Níveis de isolamento e concorrência

Transação não significa ausência de anomalias. Dependendo do isolamento, leituras
podem observar versões diferentes, phantom rows ou write skew. Restrições únicas,
checks, foreign keys e compare-and-set reforçam invariantes no ponto de commit.

Para saldo ou quota, leitura seguida de escrita sem lock/condição perde
atualizações. Use update condicional ou operação atômica adequada.

## 3. Transactional outbox

Na mesma transação:

~~~text
UPDATE domain_state
INSERT outbox(event_id, type, payload, status=pending)
COMMIT
~~~

Um relay lê pendentes, publica e marca. Crash após publish antes de marcar pode
republicar; consumidor precisa deduplicar event_id. Outbox garante que estado e
intenção de publicação confirmam juntos, não entrega exatamente uma vez.

Inbox no consumidor registra message_id e efeito na mesma transação. Retenção da
inbox cobre janela de replay.

## 4. Saga e compensação

Saga coordena transações locais. Coreografia reage a eventos; orquestração usa
coordenador explícito. Ambas precisam de estado, timeout, idempotência e
observabilidade.

Compensação não é rollback técnico. Estornar pagamento é uma nova operação,
pode falhar e deixa trilha. Não apague reserva sem verificar que ainda pertence à
saga.

~~~text
pending -> reserved -> charged -> completed
                   \-> compensation_pending -> compensated | manual_review
~~~

Estado manual_review é melhor que declarar rollback bem-sucedido sem prova.

## 5. Leitura após escrita

Réplicas podem atrasar. Após POST, GET na réplica pode retornar 404. Alternativas:

- responder com representação criada;
- rotear leitura para primário por janela;
- token de consistência ou versão mínima;
- aguardar projeção com limite;
- expor 202/job quando conclusão é assíncrona.

Documente a garantia: read-your-writes por sessão, monotonic read ou consistência
eventual até limite. Não prometa “imediato” sem medição.

## 6. Eventos, ordem e replay

Particione pela identidade cujos eventos exigem ordem. Ordem global custa mais e
raramente é necessária. Inclua sequence/version por agregado para detectar lacuna
ou evento antigo.

Replay deve ser seguro: consumidor idempotente, schema histórico, efeito externo
protegido e modo de dry-run quando aplicável. Retenção precisa respeitar PII e
obrigações legais.

## 7. Estado incerto e reconciliação

Timeout de parceiro deixa resultado unknown. Registre identificador externo e
consulte posteriormente. Não repetir cegamente débito ou envio. Um reconciler
compara estado desejado, local e remoto e produz decisão auditável:

~~~text
local pending + remote captured -> confirmar local
local pending + remote absent -> repetir com mesma chave
local completed + remote absent -> alerta/investigar
~~~

## Falhas comuns

| Falha | Consequência | Correção |
|---|---|---|
| dual write banco+broker | evento perdido | outbox |
| consumidor sem inbox | efeito duplicado | deduplicação transacional |
| compensação como delete | destruição indevida | operação versionada |
| réplica sem contrato | 404 após criação | garantia de leitura |
| ordem global desnecessária | gargalo | partição por agregado |

## Exercícios

### Nível 1 — pagamento

Modele pending, authorized, captured, failed e refunded. **Aceite:** invariantes,
duplicidade e estado incerto estão claros.

### Nível 2 — outbox/inbox

Simule crash antes/depois de publish. **Aceite:** evento não se perde e efeito do
consumidor não duplica.

### Nível 3 — saga

Injete falha em cada etapa e na compensação. **Aceite:** todo caminho termina em
estado verificável ou manual_review com runbook.

## Checklist

- [ ] Cada invariante possui owner transacional.
- [ ] Isolamento e constraints são suficientes.
- [ ] Outbox não é confundida com exactly-once.
- [ ] Consumidores deduplicam.
- [ ] Read-after-write tem garantia explícita.
- [ ] Estado incerto leva a reconciliação.

