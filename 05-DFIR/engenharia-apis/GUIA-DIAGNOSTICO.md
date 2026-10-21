# Guia de diagnóstico de APIs

Diagnóstico confiável preserva evidência e começa pela fronteira do consumidor.
Não reinicie, limpe fila ou altere banco antes de registrar request ID, horário,
versões, identidade sintética, operação e resultado.

## 1. Coleta mínima

Registre:

~~~text
instante com timezone:
ambiente e versão:
método/rota ou operação:
request/trace/event ID:
status e problem code:
cliente/SDK e versão:
tenant/actor sintéticos:
latência observada:
reprodução mínima:
mudança recente:
~~~

Redija Authorization, Cookie, chaves e PII. Preserve headers úteis sem copiar
segredos. Corpo só entra em evidência quando é sintético e necessário.

## 2. Árvore inicial

~~~text
falhou antes de chegar ao serviço?
  -> cliente, resolução, TLS, proxy ou limite de borda
chegou e recebeu 4xx?
  -> contrato, identidade, autorização, estado ou quota
recebeu 5xx/timeout?
  -> aplicação, dependência, saturação ou resultado incerto
respondeu 2xx mas efeito está errado?
  -> commit, consistência, cache, outbox ou autorização de propriedade
mensagem não chegou?
  -> outbox, dispatcher, destino, retry, DLQ ou deduplicação
~~~

Use route template e request ID para localizar sinais. Não busque por corpo ou
token.

## 3. Diagnóstico por classe

### 400, 415 e 422

Compare Content-Type, bytes, schema e versão. Valide exemplo com a mesma spec
publicada. Verifique campo extra, null, unidade, Unicode e tamanho. 415 aponta
formato; 422 aponta conteúdo entendido, porém inválido.

### 401

Confirme presença da credencial sem registrá-la. Verifique issuer, audience,
algoritmo, exp/nbf, clock skew e disponibilidade/cache de JWKS. Não “corrija”
desativando validação.

### 403 ou 404 inesperado

Confirme principal derivado, tenant, ação, ownership, estado e versão da policy.
Compare listagem e acesso direto. 404 pode ocultar objeto de outro tenant.

### 409 ou 412

409 costuma indicar conflito de negócio/idempotência; 412, precondição HTTP.
Obtenha versão atual, compare digest da intenção e nunca force update removendo
If-Match.

### 429

Identifique dimensão do limite: cliente, usuário, tenant, operação, concorrência
ou custo. Confira Retry-After/RateLimit e se retries estão amplificando carga.

### 500 ou 503

Use request/trace ID. Diferencie bug, dependência indisponível e proteção
intencional. Verifique saturação, pool, fila, deadline e circuit state. Não
transforme 500 em 400 para silenciar alerta.

### Timeout

Determine onde expirou e se o efeito pode ter ocorrido. Para escrita, consulte
idempotency record ou recurso antes de repetir. Verifique orçamento restante,
cancelamento e tentativa por camada.

## 4. Coleções

Itens repetidos/sumidos:

1. confirme ordem total e desempate;
2. decodifique cursor apenas em ferramenta local autorizada;
3. confirme vínculo com filtro/versão;
4. observe mutações entre páginas;
5. verifique collation/null;
6. reproduza com IDs/timestamps empatados.

Loop infinito em SDK geralmente indica cursor repetido ou provider retornando o
mesmo token. Cliente deve detectar; servidor deve corrigir.

## 5. Cache

Resposta de outro usuário/tenant é incidente:

1. preserve headers e chave lógica;
2. impeça reutilização compartilhada;
3. verifique Cache-Control, Vary e chave no gateway/aplicação;
4. identifique janela e consumidores afetados;
5. invalide de forma controlada;
6. teste duas identidades na mesma URL.

304 incorreto sugere ETag que não representa todos os bytes/dimensões.

## 6. Idempotência e concorrência

Duplicidade:

- a chave foi reutilizada entre tentativas?
- scope inclui consumidor/operação?
- digest usa comando canônico?
- efeito e registro confirmaram juntos?
- registro expirou antes do retry?

Lost update:

- ETag foi devolvida e If-Match exigido?
- condição foi aplicada no UPDATE/commit?
- alguma rota escreve sem versão?

Não deduplicate só em memória quando há vários processos.

## 7. Eventos e webhooks

Mensagem ausente:

~~~text
estado confirmado?
 -> outbox gravada?
 -> dispatcher selecionou?
 -> publish confirmou?
 -> broker/destino recebeu?
 -> consumidor processou?
 -> inbox/efeito confirmou?
~~~

Mensagem duplicada é esperada em at-least-once; investigue se o efeito duplicou.
Assinatura inválida: use bytes brutos, timestamp, key ID e versão. Não copie
segredo para comando de suporte. Backlog: observe idade, não só quantidade.

## 8. GraphQL e gRPC

GraphQL lento: capture operação persistida/hash, custo, quantidade de resolvers e
queries. Procure N+1, aliases, listas e erro parcial. HTTP 200 pode conter errors.

gRPC: registre method, status, deadline restante e attempt count. DEADLINE_EXCEEDED
não prova ausência de efeito. Verifique service config e propagação/cancelamento.

## 9. Saturação

Sinais:

- p99 e fila crescem antes da taxa de erro;
- pool de conexão/workers saturado;
- idade de fila aumenta;
- timeout gera retries e mais carga;
- GC/memória acompanham corpos/buffers.

Mitigue reduzindo admissão, concorrência ou recurso caro; pause retry não
essencial; degrade somente se semântica permitir. Aumentar capacidade sem conter
amplificação pode adiar a falha.

## 10. Fechamento

Antes de encerrar:

- comportamento do consumidor voltou ao SLO;
- backlog/idade retornaram ao normal;
- estado incerto foi reconciliado;
- nenhuma duplicidade ou vazamento ficou sem análise;
- mitigação temporária tem owner/expiração;
- regressão automatizada foi adicionada;
- contrato/runbook foi corrigido;
- linha do tempo e decisão estão preservadas.

## Checklist de segurança

- [ ] Nenhuma credencial foi copiada para ticket ou terminal compartilhado.
- [ ] Evidência usa dados sintéticos ou redigidos.
- [ ] Ações mutáveis tiveram alvo e consequência confirmados.
- [ ] Replay/retry preservou idempotência.
- [ ] Cache e tenant foram verificados.
- [ ] Correção foi provada pelo consumidor, não só pelo servidor.
