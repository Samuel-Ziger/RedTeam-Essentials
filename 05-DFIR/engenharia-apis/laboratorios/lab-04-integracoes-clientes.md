# Laboratório 04 — Integrações e clientes

## Pré-requisitos

- [Laboratório 03](lab-03-servico-operavel.md)
- [Webhooks](../18-webhooks.md)
- [APIs assíncronas](../19-apis-assincronas.md)
- [GraphQL](../20-graphql.md)
- [gRPC](../21-grpc.md)
- [Streaming](../22-streaming-tempo-real.md)
- [Clientes e SDKs](../23-clientes-sdks.md)
- [Governança](../24-governanca-dx.md)
- [Exemplos](../exemplos/README.md)

## Missão

Adicione uma integração de entrega e clientes resilientes. Escolha webhook ou
evento como entrega obrigatória; escolha GraphQL, gRPC ou SSE como estudo
especializado. Tudo roda localmente.

## Requisitos de entrega

Para webhook:

- HMAC sobre timestamp + bytes exatos;
- key ID, rotação e janela;
- event ID/inbox contra replay;
- outbox, retry, DLQ e replay auditado;
- destino fake conforme política.

Para evento:

- envelope, partição e sequence;
- consumidor idempotente;
- duplicidade, fora de ordem, lacuna e replay;
- contrato AsyncAPI ou equivalente.

## Requisitos de clientes

Em duas das cinco linguagens:

- timeout e cancelamento;
- erro tipado com problem code/request ID;
- paginação lazy;
- retry conservador;
- idempotency key estável;
- detecção de cursor repetido;
- testes sem Internet.

## Especialização

- GraphQL: N+1 antes/depois, custo e campo sensível; ou
- gRPC: evolução Protobuf, deadline e status; ou
- SSE: Last-Event-ID, buffer limitado e ressincronização.

## Gate

Duplicidade não duplica efeito; timeout não leva a retry inseguro; cliente lento
não gera buffer ilimitado; SDKs concordam com o contrato; nenhuma integração
alcança destino externo.

## Evidências

Inclua matriz de compatibilidade, pacote/reprodução dos clientes, tentativas de
entrega, teste de rotação e ADR justificando a especialização escolhida.

