# 06 — Retry, backoff, rate limit e backpressure

Retry não elimina falha: transforma uma falha em nova carga. Sem classificação,
orçamento e idempotência, uma dependência degradada recebe uma tempestade de
tentativas justamente quando tem menos capacidade.

## Objetivos

- classificar falhas transitórias, permanentes, ambíguas e de sobrecarga;
- implementar backoff exponencial com jitter e deadline;
- respeitar Retry-After e limitar retries entre camadas;
- distinguir rate limit, concorrência, backpressure e circuit breaker;
- operar dead-letter e replay com segurança.

## 1. Antes de repetir

Responda quatro perguntas:

1. A causa pode melhorar sem alterar a entrada?
2. Repetir o efeito é seguro ou existe chave idempotente?
3. Há tempo no deadline para uma nova tentativa?
4. A nova carga ajuda ou agrava a dependência?

| Falha | Retry automático? | Observação |
|---|---|---|
| entrada/schema inválido | não | corrigir produtor |
| autenticação ausente | não | configurar/rotacionar |
| permissão negada | geralmente não | escopo não melhora com espera |
| timeout em leitura | talvez | leitura idempotente e deadline |
| timeout após escrita | reconciliar | efeito pode ter ocorrido |
| 429 | sim, condicionado | respeitar Retry-After |
| 503 | talvez | backoff, jitter e limite |
| conflito de versão | não cego | reler e decidir |

## 2. Orçamentos em camadas

Defina maxAttempts, maxElapsedTime e deadline absoluto. Uma biblioteca pode
repetir três vezes e o job inteiro repetir três vezes, gerando nove chamadas.
Escolha uma camada responsável e exponha attempt nos eventos.

~~~text
deadline total: 20 s
tentativa 1: timeout 4 s
espera: até 1 s
tentativa 2: timeout limitado pelo restante
nenhuma tentativa começa sem tempo para concluir
~~~

## 3. Backoff exponencial com jitter

Sem jitter, clientes que falham juntos retornam juntos. Full jitter:

~~~text
limite = min(cap, base * 2^attempt)
delay  = random(0, limite)
~~~

Exemplo testável:

~~~python
def next_delay(attempt: int, base: float, cap: float, random01) -> float:
    ceiling = min(cap, base * (2 ** attempt))
    return random01() * ceiling
~~~

Injete aleatoriedade e sleeper. Testes não devem realmente esperar. Garanta que
o expoente não cause overflow e que o cap seja aplicado antes.

Retry-After pode ser segundos ou uma data HTTP. Rejeite valor inválido, considere
clock skew e não espere além do deadline. A política pode escolher o maior valor
entre backoff local e pedido do servidor, dentro do orçamento.

## 4. Rate limiting

Rate limita inícios por tempo; concorrência limita trabalhos simultâneos. São
controles diferentes.

- **token bucket:** permite rajada até a capacidade e repõe tokens;
- **leaky bucket:** suaviza saída;
- **janela fixa:** simples, mas permite rajada na fronteira;
- **janela deslizante:** mais fiel, com maior custo;
- **semáforo:** limita concorrência, não taxa.

Particione por tenant ou credencial quando a cota também for particionada. Um
bucket global pode permitir que um cliente consuma toda a capacidade.

## 5. Backpressure e fila limitada

Quando produtor é mais rápido que consumidor, existem apenas algumas escolhas:

- desacelerar ou pausar o produtor;
- limitar fila e rejeitar com evidência;
- derrubar itens segundo política declarada;
- aumentar consumidores dentro da capacidade do sink;
- persistir backlog durável e operar sua idade.

Fila ilimitada troca erro imediato por falta de memória e latência invisível. Meça
tamanho e idade do item mais antigo. Tamanho estável pode esconder itens presos.

## 6. Circuit breaker

Circuit breaker reduz chamadas quando a dependência está falhando:

~~~text
closed --falhas acima do limite--> open
open --tempo de recuperação--> half-open
half-open --sucesso controlado--> closed
half-open --falha--> open
~~~

Ele não corrige idempotência, não substitui timeout e não deve contar erro de
validação do cliente como indisponibilidade do servidor. Limite chamadas de prova
em half-open para evitar nova rajada.

## 7. Bulkhead e isolamento

Pools separados impedem que uma dependência lenta esgote todas as threads,
conexões ou workers. Isole por tipo de trabalho e criticidade, mantendo limites
totais. Isolamento excessivo desperdiça capacidade; meça filas por partição.

## 8. Dead-letter e replay

Depois do orçamento, preserve:

- item ID e chave idempotente;
- versão do schema e origem;
- classe da falha e última causa segura;
- tentativas e timestamps;
- digest do payload ou referência protegida;
- próxima ação esperada.

Dead-letter precisa de ownership, alerta, retenção e ferramenta de replay. Replay
em massa sem corrigir a causa repete o incidente. Use canário, limite e a mesma
chave original. Nunca edite silenciosamente o item preservado; crie uma nova versão
com relação de proveniência.

## 9. Degradação e fallback

Fallback só é seguro quando seu dado tem semântica conhecida. Cache antigo deve
mostrar idade e limite de staleness. Retornar lista vazia ao falhar confunde
“nenhum resultado” com “não foi possível consultar”.

Prefira resultado tipado: fresh, stale, unavailable ou partial. O chamador decide
se pode continuar.

## Falhas e diagnóstico

| Sintoma | Causa | Medida |
|---|---|---|
| picos periódicos | backoff sem jitter | distribuição dos delays |
| nove chamadas por item | retries em camadas | attempt por camada |
| fila pequena, itens antigos | item preso | idade p95 e oldest age |
| breaker abre por 400 | classificação errada | classe da falha |
| replay duplica | chave nova | conservar identidade |

## Exercícios

### Nível 1 — classificar

Classifique 15 falhas. **Aceite:** cada decisão explica transitoriedade,
idempotência e estado incerto.

### Nível 2 — retry determinístico

Implemente policy com relógio, RNG e sleeper falsos. **Aceite:** testes afirmam
agenda, cap, Retry-After, cancelamento e deadline sem esperar tempo real.

### Nível 3 — sobrecarga

Combine fila limitada, token bucket e breaker em simulação. **Aceite:** memória é
limitada, itens têm estado final e recuperação não gera rajada.

## Checklist

- [ ] Retry possui condição, idempotência, tentativas e deadline.
- [ ] Backoff usa jitter testável e respeita Retry-After.
- [ ] Rate, concorrência e fila são limites distintos.
- [ ] Circuit breaker conta apenas falhas relevantes.
- [ ] Fallback não esconde indisponibilidade.
- [ ] Dead-letter tem triagem, retenção e replay controlado.

