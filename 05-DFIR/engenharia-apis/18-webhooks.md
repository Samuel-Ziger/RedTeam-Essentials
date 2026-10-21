# 18 — Webhooks confiáveis

Webhook é uma requisição iniciada pelo produtor para endpoint registrado pelo
consumidor. Reduz polling, mas transforma destino externo em dependência hostil
e introduz autenticidade, duplicidade, replay, SSRF e operação de entregas.

## Objetivos

- projetar envelope e ciclo de assinatura;
- garantir entrega ao menos uma vez com outbox;
- validar destinos e limitar SSRF;
- implementar retry, dead-letter e replay auditado;
- construir consumidor idempotente.

## 1. Evento e envelope

~~~json
{
  "id": "evt_01",
  "type": "item.created.v1",
  "occurredAt": "2026-10-05T12:00:00Z",
  "subject": "items/itm_01",
  "data": {"itemId": "itm_01"}
}
~~~

ID identifica a ocorrência para deduplicação. type e versão têm semântica
estável. occurredAt é instante do fato, não da entrega. data contém o mínimo
necessário e respeita classificação. Tentativa e evento são entidades distintas:
um evento pode produzir várias tentativas.

## 2. Assinatura dos bytes

Assine timestamp, versão e bytes exatos recebidos:

~~~text
signed = version + "." + timestamp + "." + rawBody
signature = HMAC-SHA256(secret, signed)
~~~

O consumidor lê corpo bruto, calcula HMAC e compara em tempo constante antes de
parsear. Limite diferença de relógio e registre event ID para rejeitar replay.
Não serialize novamente o JSON: espaços e ordem podem mudar os bytes.

Inclua key ID para rotação. Durante overlap, aceite chave atual e anterior por
janela controlada. Nunca logue segredo ou assinatura completa.

Assinatura prova posse do segredo, não autorização do evento no domínio. Após
validar, confira type, schema, tenant e transição.

## 3. Entrega

Fluxo produtor:

~~~text
transação domínio + outbox
 -> dispatcher seleciona pendente
 -> POST com timeout curto
 -> 2xx confirma conforme política
 -> falha transitória agenda retry com jitter
 -> esgotamento vai para dead-letter
~~~

Crash depois de o consumidor processar e antes do produtor registrar 2xx causa
duplicidade. O consumidor usa event ID/inbox. Não prometa ordem global; quando
necessária por objeto, use sequence e trate lacunas.

## 4. Respostas e retries

Documente quais status confirmam, repetem ou encerram:

- qualquer 2xx pode confirmar;
- 408, 429 e 5xx podem repetir;
- 400/401/403 normalmente exigem correção/configuração;
- 404/410 podem desativar subscription após política.

Respeite Retry-After com teto. A entrega tem prazo de expiração: evento antigo
pode não ter utilidade. Dead-letter não é cemitério invisível; possui alerta,
consulta, correção e replay.

## 5. Registro de destinos e SSRF

Valide HTTPS, porta, domínio permitido, DNS e redirecionamentos. Quando possível,
faça challenge de posse do endpoint. Bloqueie loopback, link-local, metadata
service e redes internas conforme arquitetura. Reavalie DNS no momento da
conexão e use proxy de egress.

Limite resposta em bytes/tempo e ignore corpo não necessário. Credencial para o
destino deve ser isolada por subscription.

## 6. Operação

Exponha ao consumidor:

- histórico de tentativas sem segredos;
- motivo categórico;
- próximo retry e expiração;
- rotação de segredo;
- botão/API de replay com autorização;
- evento de teste claramente marcado.

Métricas incluem idade da outbox, sucesso por destino, tentativas, latência,
dead-letter e replay. Não use URL completa como label.

## Falhas comuns

| Falha | Consequência | Correção |
|---|---|---|
| assinar JSON reserializado | assinatura diverge | bytes brutos |
| só timestamp contra replay | duplicidade na janela | event ID/inbox |
| destino livre | SSRF | política de egress |
| retry sem prazo | evento eterno | expiração/DLQ |
| segredo único global | impacto amplo | segredo por subscription |

## Exercícios

### Nível 1 — assinatura

Implemente sign/verify. **Aceite:** corpo alterado, tempo expirado, algoritmo e
assinatura inválidos falham em tempo seguro.

### Nível 2 — entrega

Simule 500, 429, timeout e 400. **Aceite:** política escolhe retry, terminal e
dead-letter corretamente.

### Nível 3 — duplicidade e rotação

Entregue o mesmo ID durante overlap de chaves. **Aceite:** apenas um efeito de
negócio ocorre e ambas as chaves obedecem à janela.

## Checklist

- [ ] Assinatura cobre timestamp e bytes exatos.
- [ ] Replay usa janela e event ID.
- [ ] Outbox e consumidor idempotente tratam duplicidade.
- [ ] Destino passa por política anti-SSRF.
- [ ] Retry tem jitter, teto, expiração e DLQ.
- [ ] Rotação e replay são auditáveis.

