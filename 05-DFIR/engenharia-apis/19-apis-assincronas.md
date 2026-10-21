# 19 — APIs assíncronas e orientadas a eventos

Comando pede uma ação; evento declara um fato. Mensagens desacoplam tempo e
implantação, mas introduzem duplicidade, ordenação parcial, replay, schema
histórico e consistência eventual. O broker não resolve regras do domínio.

## Objetivos

- diferenciar comando, evento e consulta;
- projetar envelope, canal, partição e retenção;
- implementar consumidor idempotente;
- evoluir schemas e suportar replay;
- documentar contrato com AsyncAPI.

## 1. Tipos de mensagem

**Comando:** “ReserveInventory”; tem destinatário lógico e pode ser rejeitado.
**Evento:** “InventoryReserved”; fato no passado e pode ter vários consumidores.
**Consulta:** solicita informação e normalmente exige resposta.

Nomear evento OrderProcess não revela fato. Use verbo no passado e preserve
significado. Não publique evento dizendo succeeded antes do commit.

## 2. Contrato da mensagem

Defina:

- id, type, version e occurredAt;
- source, subject e correlation/causation IDs;
- schema e exemplos;
- owner e classificação;
- canal e chave de partição;
- garantia de entrega e ordem;
- retenção, replay e dead-letter;
- compatibilidade e depreciação.

CloudEvents 1.0.2 oferece envelope interoperável; AsyncAPI descreve canais,
operações, mensagens, schemas e bindings. A página estável oficial de AsyncAPI
continua expondo 3.0.0 como referência; valide suporte antes de usar recursos de
versões novas em tooling.

## 3. Partição e ordem

Ordem global custa throughput. Geralmente basta ordenar por agregado:

~~~text
partitionKey = orderId
event.version = 7
~~~

Consumidor detecta versão repetida, antiga ou lacuna. Processamento paralelo
entre orders continua possível. A chave não deve conter PII desnecessária.

## 4. Entrega e deduplicação

At-least-once pode redeliver. O consumidor grava message ID e efeito na mesma
transação. Se efeito externo não participa, use idempotency key e reconciliação.

At-most-once pode perder. “Exactly-once” do broker costuma valer dentro de
fronteira específica, não para banco + e-mail + parceiro. Declare a garantia
fim a fim que foi realmente testada.

## 5. Retry e poison messages

Falha transitória repete com backoff. Mensagem inválida ou permanentemente
incompatível não deve bloquear partição para sempre. Envie a quarantine/DLQ com
motivo, schema version e referência segura.

DLQ exige owner, alerta, ferramenta de inspeção, correção e replay. Reprocessar
após corrigir consumidor deve preservar ordem/efeitos definidos.

## 6. Evolução e replay

Campos novos geralmente são tolerados por leitores. Remoção, tipo e significado
pedem nova versão. Schema registry impõe regras, mas não entende toda semântica.

Replay pode acionar e-mail ou cobrança de novo. Separe projeções reprocessáveis de
efeitos externos; use modo de rebuild ou idempotência persistente. Teste eventos
históricos no CI.

## 7. Observabilidade

Propague trace/correlation sem depender de ordem global. Métricas:

- lag por consumer group;
- idade da mensagem mais antiga;
- taxa e duração;
- retries, duplicatas e DLQ;
- lacunas de versão;
- tempo fato-até-projeção.

Não coloque event ID em label. Trace de mensagem segue semântica producer,
publish, receive/process conforme instrumentação.

## 8. Quando não usar eventos

Não escolha eventos apenas para evitar uma chamada HTTP. Se o consumidor precisa
de confirmação imediata, erro detalhado e consistência forte entre as partes, uma
operação síncrona pode ser mais simples. Eventos também não eliminam dependência:
eles a movem para schema, canal, retenção e tempo de convergência. Prefira uma
transação local quando o invariante cabe no mesmo owner. Adote mensageria quando
desacoplamento temporal, fan-out, buffer ou replay têm valor suficiente para
pagar operação, reconciliação e suporte adicionais.

## Falhas comuns

| Falha | Resultado | Correção |
|---|---|---|
| evento usado como comando genérico | ownership ambíguo | semântica explícita |
| offset como deduplicação | replay duplica efeito | inbox de negócio |
| ordem global | gargalo | partição por agregado |
| DLQ sem processo | perda escondida | owner/runbook |
| replay dispara efeitos | dano/duplicidade | modo rebuild/idempotência |

## Exercícios

### Nível 1 — contrato

Modele order.created e order.cancelled. **Aceite:** envelope, partição, retenção,
ordem, PII e owner existem.

### Nível 2 — consumidor

Entregue duplicado, fora de ordem e com lacuna. **Aceite:** efeito não duplica,
lacuna é observada e evento antigo não regride estado.

### Nível 3 — replay

Reconstrua projeção a partir de histórico. **Aceite:** nenhum efeito externo é
reenviado e schemas antigos continuam legíveis.

## Checklist

- [ ] Comando e evento não foram confundidos.
- [ ] Ordem necessária define partição.
- [ ] Consumidor é idempotente.
- [ ] DLQ possui operação e replay.
- [ ] Evolução considera eventos históricos.
- [ ] Lag e tempo até consistência são observáveis.
