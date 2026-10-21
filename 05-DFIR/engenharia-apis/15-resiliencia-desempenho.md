# 15 — Resiliência, limites e desempenho

Resiliência é controlar trabalho sob falha. Timeout, retry, circuit breaker e
fila não melhoram um sistema automaticamente; configurados em todas as camadas,
podem amplificar carga. Comece por orçamento de tempo e capacidade mensurável.

## Objetivos

- decompor orçamento de latência;
- aplicar timeout, cancelamento, retry e jitter;
- limitar concorrência, fila, corpo e custo;
- usar rate limit, bulkhead e circuit breaker conscientemente;
- executar teste de carga seguro e interpretar cauda.

## 1. Orçamento de latência

Se o consumidor aceita 800 ms, a API não pode dar 800 ms a cada dependência:

~~~text
entrada/fila 50 ms
aplicação 100 ms
dependência A 200 ms
dependência B 250 ms
margem/resposta 200 ms
~~~

Use deadline absoluto ou orçamento restante. Timeout de conexão e de operação
são diferentes. Ao expirar, cancele trabalho quando possível; caso contrário o
servidor continua consumindo recurso depois que o cliente desistiu.

## 2. Retry responsável

Repita somente falhas transitórias e operações seguras/idempotentes:

~~~text
delay = min(cap, base * 2^attempt) + jitter
~~~

Defina tentativas máximas e deadline total. Respeite Retry-After com teto. Não
faça retry em validação, permissão ou precondição sem mudança. Evite retries em
cliente, gateway e serviço ao mesmo tempo: três tentativas em três camadas podem
virar 27 chamadas.

Retry storm ocorre quando dependência recupera e todos tentam juntos. Jitter,
limite e circuit breaker reduzem sincronização.

## 3. Rate limit e quota

Rate limit controla frequência; quota controla consumo numa janela; concurrency
limit controla trabalho simultâneo. A unidade pode ser identidade, tenant,
operação e custo.

RFC 9333 define campos RateLimit para comunicar políticas HTTP; suporte de
clientes e gateways deve ser verificado. 429 e Retry-After continuam essenciais.
Não dependa somente de IP, especialmente atrás de proxy ou para usuários
distribuídos.

## 4. Bulkhead e circuit breaker

Bulkhead separa pools: exportação lenta não ocupa workers de leitura. Circuit
breaker abre após sinais de falha, evita chamadas inúteis e testa recuperação em
half-open. Ele não corrige latência interna e pode mascarar dependência se
fallback retorna dado inadequado.

Fallback precisa ser correto para o domínio. “Lista vazia” no lugar de falha pode
ser interpretada como ausência real. Prefira resposta marcada como stale ou erro
explícito.

## 5. Filas e backpressure

Fila absorve pico curto, não capacidade insuficiente permanente. Defina tamanho,
prioridade, deadline por item e política quando cheia: rejeitar, degradar ou
persistir em outro mecanismo. Buffer infinito só adia a falha e aumenta latência.

Little's Law relaciona itens no sistema, throughput e tempo médio; fila crescente
com throughput estável indica saturação. Observe idade do item mais antigo, não
apenas comprimento.

## 6. Desempenho de dados e serialização

Meça queries, índices, N+1, alocação, compressão e tamanho de resposta. Índice
acelera leitura, mas custa escrita e armazenamento. Cache só ajuda quando hit rate
e consistência justificam.

Paginação, projeção e streaming reduzem memória. Não compacte corpo minúsculo nem
aceite descompressão sem limite. Média de latência esconde p99.

## 7. Teste de carga

Use ambiente autorizado e dados sintéticos. Defina:

- modelo de tráfego e distribuição por operação;
- ramp-up, steady state e ramp-down;
- SLO e limite de erro/saturação;
- critério de parada;
- baseline e versões;
- warm-up/cache;
- limpeza e custo.

Teste carga, stress, spike e soak respondem perguntas diferentes. Pare se risco
ao ambiente compartilhado surgir.

## Falhas comuns

| Falha | Resultado | Correção |
|---|---|---|
| sem timeout | recurso preso | prazo explícito |
| retry em toda camada | amplificação | uma política coordenada |
| fila ilimitada | latência/memória crescem | backpressure |
| fallback vazio | dado falso | resposta explícita |
| otimizar média | cauda ruim | p50/p95/p99 |
| teste sem modelo | número inútil | workload realista |

## Exercícios

### Nível 1 — orçamento

Decomponha 800 ms entre duas dependências. **Aceite:** timeout interno deixa
margem para resposta e cancelamento.

### Nível 2 — retry

Simule 429, 503, timeout e 400. **Aceite:** apenas falhas transitórias repetem,
com jitter, teto e deadline.

### Nível 3 — saturação

Compare fila ilimitada e limitada sob pico. **Aceite:** registre p99, rejeições,
idade da fila, memória e ponto de recuperação.

## Checklist

- [ ] Deadline é propagado e trabalho pode ser cancelado.
- [ ] Retry é limitado, idempotente e coordenado.
- [ ] Frequência, concorrência e custo têm limites.
- [ ] Fila tem tamanho e política de overflow.
- [ ] Fallback preserva semântica.
- [ ] Teste de carga tem autorização e critério de parada.

