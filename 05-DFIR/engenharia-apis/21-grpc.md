# 21 — gRPC e Protocol Buffers

gRPC modela serviços e mensagens em Protocol Buffers, gera stubs e suporta
chamadas unary e streaming. Tipagem reduz ambiguidade mecânica, mas deadlines,
compatibilidade, autorização e retry ainda são decisões do produto.

## Objetivos

- escrever serviços e mensagens evolutivos;
- preservar field numbers e presença;
- propagar deadline e cancelamento;
- configurar retry, health e limites;
- mapear status e observabilidade.

## 1. Contrato

~~~proto
syntax = "proto3";
package catalog.v1;

service CatalogService {
  rpc GetItem(GetItemRequest) returns (Item);
  rpc WatchItems(WatchItemsRequest) returns (stream ItemEvent);
}

message GetItemRequest {
  string item_id = 1;
}

message Item {
  string item_id = 1;
  string title = 2;
  int64 version = 3;
}
~~~

Package versiona namespace. Método e mensagem têm responsabilidades próprias;
não reutilize Request genérico.

## 2. Evolução Protobuf

Field number é identidade no wire. Ao remover:

~~~proto
message Item {
  reserved 4;
  reserved "legacy_name";
}
~~~

Nunca reutilize número. Adicionar campo costuma ser compatível porque leitores
antigos ignoram unknown fields, mas semântica, enum e presença ainda importam.
Não altere tipo para outro wire type incompatível.

Em proto3, presença de scalar depende da forma usada; optional permite
distinguir ausente de default. Wrapper/oneof pode ser apropriado. Enum deve
reservar zero como valor não especificado e consumidores precisam de fallback.

## 3. Deadlines e cancelamento

gRPC não define deadline por padrão; o guia oficial recomenda sempre configurar
prazo realista. Cliente envia deadline; servidor propaga orçamento restante às
dependências e para trabalho cancelável quando expira.

Timeout sem cancelamento deixa CPU/banco ocupados. Em streaming, ambos os lados
precisam observar cancelamento e liberar buffers.

## 4. Retry e idempotência

gRPC possui transparent retry e política configurável por service config, mas
não há política geral de retry ativada para qualquer método. Declare códigos,
tentativas, backoff e throttling somente para operações seguras/idempotentes.

Um unary pode ter sido executado antes de UNAVAILABLE. Escritas ainda pedem
idempotency key ou request ID de negócio.

## 5. Status e rich errors

Use status canônico: INVALID_ARGUMENT, UNAUTHENTICATED, PERMISSION_DENIED,
NOT_FOUND, ALREADY_EXISTS, FAILED_PRECONDITION, ABORTED, RESOURCE_EXHAUSTED,
UNAVAILABLE e INTERNAL. Não devolva UNKNOWN para erro de domínio conhecido.

Detalhes ricos podem carregar códigos tipados, mas não exponha stack/segredo.
Clientes decidem por code, não message.

## 6. Segurança e operação

TLS protege canal; mTLS pode autenticar workload. Metadata carrega token, mas não
deve ir ao log. Autorize método, recurso e propriedade após autenticar.

Defina max message size, keepalive, concorrência, compression e flow control.
Health Checking Protocol permite status por serviço; reflection em produção
segue política de exposição. Service config também distribui load balancing e
retry quando ecossistema suporta.

## 7. Streaming e backpressure

Server, client e bidirectional streaming exigem contrato de sequência,
half-close, heartbeat, tamanho e erro parcial. Flow control do transporte não
substitui limite de buffer da aplicação. Cliente lento precisa desacelerar,
descartar quando permitido ou ser desconectado com posição retomável.

## 8. Interoperabilidade e gateway

Browser, proxy e ferramenta de inspeção podem não oferecer suporte direto ao
mesmo conjunto do gRPC nativo. gRPC-Web e JSON transcoding são adapters, não
equivalência automática: status, streaming, metadata e nomes precisam de teste.
Se a organização oferece REST e gRPC para o mesmo caso de uso, ambos chamam o
mesmo serviço de aplicação e compartilham invariantes, mas preservam contratos de
transporte próprios. Gere stubs no pipeline, fixe protoc/plugins e execute teste
de compatibilidade com uma versão anterior do cliente.

## 9. Capacidade

Conexões multiplexadas ainda competem por CPU, memória e streams simultâneos.
Meça mensagens por segundo, bytes, active streams, deadline exceeded, retry e
flow-control stalls. Separe operações longas em pools quando necessário. Um
canal saudável não prova que método ou dependência está saudável; health por
serviço precisa refletir capacidade de aceitar trabalho, sem executar transação
real a cada probe.

## Falhas comuns

| Falha | Consequência | Correção |
|---|---|---|
| reutilizar field number | corrupção | reserved |
| chamada sem deadline | recurso preso | deadline obrigatório |
| retry de escrita | duplicidade | idempotência |
| auth só por método | BOLA | recurso/propriedade |
| message enorme | memória/latência | limites/stream |

## Exercícios

### Nível 1 — evolução

Evolua Item por três versões. **Aceite:** números removidos reservados, enum
unknown e cliente antigo continuam seguros.

### Nível 2 — deadline

Propague prazo a duas dependências. **Aceite:** cancelamento encerra trabalho e
retorna status correto.

### Nível 3 — retry/stream

Simule UNAVAILABLE antes/depois do commit e cliente lento. **Aceite:** escrita
não duplica e buffer permanece limitado.

## Checklist

- [ ] Field numbers nunca são reutilizados.
- [ ] Presença/default têm semântica.
- [ ] Toda chamada possui deadline.
- [ ] Retry é configurado apenas quando seguro.
- [ ] Status e detalhes são estáveis.
- [ ] Streaming tem backpressure e cancelamento.
