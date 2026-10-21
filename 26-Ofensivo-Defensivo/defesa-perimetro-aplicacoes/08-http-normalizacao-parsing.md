# 08 — HTTP, normalização e parsing

Uma requisição passa por componentes que podem discordar sobre caminho,
codificação, tamanho, cabeçalhos duplicados e fronteiras da mensagem. A defesa
começa definindo uma representação canônica e rejeitando ambiguidade.

## Superfícies

- percent-encoding e decodificação repetida;
- barras, pontos, Unicode e case no caminho;
- `Host`/`:authority` e múltiplos cabeçalhos;
- `Content-Length`, transferência e corpos incompletos;
- content type declarado versus parser escolhido;
- HTTP/1.1, HTTP/2 e HTTP/3 atravessando traduções.

Não tente "consertar" entrada indefinida silenciosamente. Defina tamanho
máximo, métodos, tipos aceitos e comportamento para duplicidade. Proxy e
aplicação devem chegar à mesma interpretação.

## Contrato de borda

```yaml
route: /v1/orders
methods: [POST]
content_types: [application/json]
max_body_bytes: 32768
duplicate_security_headers: reject
canonical_path_required: true
request_id: regenerate_at_edge
```

## Teste diferencial seguro

Monte uma tabela de mensagens sintéticas ambíguas e alimente parsers locais,
sem enviá-las a terceiros. Registre se edge e aplicação aceitam, rejeitam ou
normalizam. Qualquer divergência é defeito de arquitetura, ainda que o caso
específico não resulte em impacto.

## Telemetria

Registre protocolo, método, host canônico, rota normalizada, tamanho, regra,
status e request ID. Não grave token, cookie, senha ou corpo completo por padrão.

## Exercício

Red propõe cinco casos de ambiguidade abstratos. Blue define rejeição e log.
Purple transforma cada divergência em teste unitário nos dois componentes.
