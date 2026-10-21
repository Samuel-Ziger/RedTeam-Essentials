# 22 — Streaming e tempo real

Tempo real não significa latência zero. Significa um orçamento de atualização e
um canal capaz de manter ordem, backpressure, reconexão e autorização. Polling,
SSE, WebSocket e gRPC streaming resolvem formas diferentes do problema.

## Objetivos

- escolher mecanismo por direção e volume;
- definir protocolo de aplicação do stream;
- implementar heartbeat, resume e reconexão;
- limitar buffers e clientes lentos;
- reavaliar identidade e autorização em conexão longa.

## 1. Comparação

| Opção | Direção | Melhor característica | Custo |
|---|---|---|---|
| polling | cliente → servidor | simplicidade e cache | atraso/requisições vazias |
| long polling | servidor segura resposta | compatibilidade HTTP | conexões/repetição |
| SSE | servidor → cliente | reconexão/event ID | texto e unidirecional |
| WebSocket | bidirecional | baixa latência/interação | protocolo próprio |
| gRPC stream | uni/bidirecional | tipagem/flow control | ecossistema |

Se atualização ocorre uma vez por minuto, polling condicional pode ser melhor que
milhares de conexões persistentes. Meça custo e latência desejada.

## 2. Contrato de sessão

Defina:

- handshake e autenticação;
- canais/subjects autorizados;
- envelope e versão;
- sequence/event ID;
- heartbeat e idle timeout;
- tamanho e frequência máximos;
- política de backpressure;
- erro e encerramento;
- resume token/retenção;
- expiração de credencial e revogação.

WebSocket fornece frames, não semântica de domínio. Crie mensagens subscribe,
subscribed, event, error, ping/pong e unsubscribe com IDs de correlação.

## 3. Backpressure

Produtor mais rápido que consumidor acumula buffer. Políticas:

- desacelerar upstream;
- buffer limitado;
- coalescer estados substituíveis;
- descartar eventos explicitamente descartáveis;
- desconectar e oferecer resume;
- mover para broker durável.

Nunca use buffer infinito. Em preço atual, pode bastar manter o último valor; em
transações financeiras, descartar é inaceitável. A regra vem do domínio.

## 4. Heartbeat e detecção de falha

Conexão TCP aberta não prova cliente saudável. Heartbeat detecta caminho morto e
mantém intermediários. Intervalos muito curtos custam bateria e carga; muito
longos atrasam detecção.

Timeout e encerramento devem ter códigos/motivos seguros. Cliente usa backoff e
jitter ao reconectar para evitar tempestade.

## 5. Resume e lacunas

SSE Last-Event-ID ou token próprio permite retomar. Servidor mantém eventos por
janela. Se posição expirou, retorna sinal para ressincronização completa:

~~~text
resume accepted -> eventos após sequence
resume expired -> snapshot atual + nova sequence
~~~

Token precisa de integridade e vínculo com identidade/canal. Não permita que
resume revele evento de outro tenant.

## 6. Identidade em conexão longa

Token pode expirar e permissão pode ser revogada. Escolha reautenticação,
reconexão ou reavaliação periódica. Subscription a novo canal sempre autoriza.
Não considere o handshake autorização eterna.

Mudança de membership deve fechar ou reduzir streams afetados dentro do prazo
documentado.

## 7. Operação

Observe conexões, subscriptions, mensagens, bytes, lag, buffer, desconexões por
motivo, reconexões e idade do evento. Não use connection ID como label.

Deploy precisa drenar conexões ou permitir reconexão. Teste proxy, balanceador,
idle timeout e distribuição de sessões no ambiente real, sem transformar o
capítulo em administração de rede.

## 8. Snapshot mais delta

Streams não devem ser a única forma de reconstruir estado quando a retenção é
finita. Um padrão robusto oferece snapshot autorizado e depois deltas a partir
de uma posição:

~~~text
GET snapshot -> state at sequence 120
SUBSCRIBE after 120 -> 121, 122, ...
~~~

É preciso fechar a corrida entre snapshot e subscription. O servidor pode emitir
watermark no snapshot e reter deltas até o cliente assinar. Se detectar lacuna,
o cliente descarta estado parcial e ressincroniza. Snapshot também tem paginação,
limites e ETag; resume token não substitui uma estratégia de reconstrução.

## Falhas comuns

| Falha | Resultado | Correção |
|---|---|---|
| WebSocket sem protocolo | estados incompatíveis | schema/versionamento |
| buffer infinito | OOM | limite/backpressure |
| reconnect imediato | tempestade | backoff/jitter |
| token validado uma vez | acesso após revogação | reavaliação |
| resume sem tenant | vazamento | token contextual |

## Exercícios

### Nível 1 — decisão

Compare polling, SSE e WebSocket para status de exportação. **Aceite:** direção,
frequência, custo e recuperação justificam escolha.

### Nível 2 — protocolo

Defina mensagens e estados de sessão. **Aceite:** handshake, erro, heartbeat,
resume e encerramento estão especificados.

### Nível 3 — cliente lento

Simule consumo abaixo da produção. **Aceite:** memória fica limitada, política de
perda é correta e reconexão recupera ou ressincroniza.

## Checklist

- [ ] “Tempo real” possui orçamento mensurável.
- [ ] Protocolo de sessão está versionado.
- [ ] Buffer e frequência têm limites.
- [ ] Heartbeat e reconexão usam política.
- [ ] Resume preserva tenant e detecta expiração.
- [ ] Autorização é reavaliada em conexões longas.
