# 08 — HTTP, APIs, WebSocket, gRPC e mensageria

HTTP/1.1 usa mensagens textuais e conexões persistentes; HTTP/2 multiplexa
streams sobre TCP e comprime headers; HTTP/3 usa QUIC. A semântica de métodos,
status e cache permanece central mesmo quando framing muda.

REST organiza recursos sobre HTTP; OpenAPI descreve contrato. WebSocket faz
upgrade para canal bidirecional. gRPC usa HTTP/2 e Protocol Buffers, com unary e
streaming. Filas/pub-sub desacoplam produtores e consumidores e exigem semântica
de entrega, idempotência, ordering, retry e dead-letter.

## Decisão

- interoperabilidade externa e debug humano: HTTP/JSON;
- contratos tipados e alto volume interno: gRPC pode ajudar;
- eventos assíncronos: mensageria;
- atualização bidirecional longa: WebSocket/stream.

Não transforme escolha de protocolo em religião. Meça payload, latência,
compatibilidade, observabilidade, evolução e falhas. Timeout, retry com jitter,
circuit breaker e idempotency key devem ser especificados juntos.
