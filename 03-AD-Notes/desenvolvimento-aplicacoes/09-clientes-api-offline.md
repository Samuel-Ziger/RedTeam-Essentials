# 09 — Clientes de API resilientes e experiência offline

Projetar uma API e consumi-la são problemas complementares. O cliente convive com
latência, respostas fora de ordem, indisponibilidade, expiração de credenciais,
dados obsoletos e dúvidas sobre o resultado de uma escrita. Uma interface robusta
trata essas condições como estados normais, não como exceções que aparecem apenas
depois do lançamento.

O módulo 01 definiu contratos de API. Aqui o foco é a aplicação consumidora. O
[Study Desk](projetos/study-desk/README.md) é local-first e funciona sem servidor;
neste capítulo, uma sincronização opcional será usada como evolução hipotética.
Ela nunca deve comprometer a cópia local nem prometer consistência que não foi
implementada.

## Objetivos verificáveis

Ao concluir, você deverá conseguir:

1. modelar estados `idle`, carregando, vazio, sucesso, atualizando, erro e offline;
2. aplicar timeout, cancelamento, retry, backoff e jitter com contratos honestos;
3. distinguir operação idempotente de repetição arbitrária;
4. impedir que uma resposta antiga substitua uma consulta recente;
5. definir cache por chave, escopo, validade, revalidação e invalidação;
6. projetar fila offline e reconciliação sem perda silenciosa;
7. tratar autenticação, autorização e dados sensíveis no limite do cliente;
8. testar falhas de forma determinística e diagnosticar cada tentativa.

## Pré-requisitos e modelo mental

Você deve conhecer Promises/async, JSON, contratos HTTP e estado de UI dos módulos
01 e dos [capítulos 03](03-validacao-erros-feedback.md) e
[05](05-estado-eventos.md). Detalhes de roteamento, transporte e infraestrutura
pertencem à trilha de Redes; aqui observamos somente o contrato da aplicação.

```text
intenção da pessoa
  -> comando com identidade
  -> política do cliente (timeout/retry/cache)
  -> transporte por uma porta
  -> resposta validada
  -> reconciliação com estado vigente
  -> feedback e persistência
```

Uma falha precisa ser classificada antes de ser repetida. “Não obtive resposta”
não significa “o servidor não executou”. Um timeout do cliente limita quanto ele
espera; a operação remota pode ter terminado. Cancelar significa que o resultado
deixou de interessar ao consumidor, não que todos os efeitos foram revertidos.

## Modele o recurso remoto como estado, não como booleanos

Um `loading: true|false` não distingue primeira carga de atualização, vazio de
erro ou conteúdo novo de conteúdo obsoleto. Use uma união conceitual:

```text
RemoteData<T>
  Idle
  Loading(requestId)
  Empty(receivedAt)
  Success(data, receivedAt, freshness)
  Refreshing(data, requestId, receivedAt)
  Failure(previousData?, error, retryable)
  Offline(previousData?, pendingCount)
```

Preserve dado estável durante `Refreshing`; apagar a tela cria cintilação e perde
contexto. Marque quando o dado pode estar obsoleto. `Empty` é sucesso válido e
merece orientação própria; não deve parecer uma falha silenciosa.

No Study Desk, a lista local pode continuar utilizável enquanto a sincronização
falha. Mostre “3 alterações aguardando sincronização”, não “seus dados falharam”.
O estado remoto é uma projeção adicional, não substitui automaticamente o estado
de domínio confirmado localmente.

## Um cliente JavaScript com contrato explícito

Este exemplo usa `fetch`, `AbortController`, timeout e validação mínima. O cliente
não conhece o DOM:

```javascript
export class ApiError extends Error {
  constructor(kind, message, details = {}) {
    super(message);
    this.name = "ApiError";
    this.kind = kind;
    this.details = details;
  }
}

export async function listSessions({ baseUrl, signal, timeoutMs = 5000 }) {
  const timeout = AbortSignal.timeout(timeoutMs);
  const combined = AbortSignal.any([signal, timeout].filter(Boolean));

  let response;
  try {
    response = await fetch(`${baseUrl}/sessions`, {
      headers: { Accept: "application/json" },
      signal: combined,
    });
  } catch (error) {
    if (timeout.aborted && combined.reason === timeout.reason) {
      throw new ApiError("timeout", "A consulta excedeu o tempo limite.");
    }
    if (signal?.aborted || combined.aborted) {
      throw new ApiError("cancelled", "A consulta foi interrompida.");
    }
    throw new ApiError("unavailable", "Não foi possível consultar as sessões.");
  }

  if (!response.ok) {
    throw new ApiError("http", "A API recusou a consulta.", {
      status: response.status,
      retryAfter: response.headers.get("retry-after"),
    });
  }

  let document;
  try {
    document = await response.json();
  } catch (error) {
    if (timeout.aborted && combined.reason === timeout.reason) {
      throw new ApiError("timeout", "A resposta excedeu o tempo limite.");
    }
    if (signal?.aborted || combined.aborted) {
      throw new ApiError("cancelled", "A leitura da resposta foi interrompida.");
    }
    throw new ApiError("invalid_response", "A resposta não contém JSON válido.");
  }
  if (!Array.isArray(document.items)) {
    throw new ApiError("invalid_response", "Resposta incompatível com o contrato.");
  }
  return document.items;
}
```

O `reason` do sinal combinado preserva qual sinal abortou primeiro: isso impede
que expiração do orçamento seja relatada como cancelamento voluntário. O teste
precisa controlar as duas causas. `AbortSignal.timeout` e `AbortSignal.any`
exigem runtimes modernos; uma aplicação com alvos mais antigos pode compor
controladores manualmente. A lição durável é a assinatura: dependências e
políticas entram explicitamente, cancelamento é recebido, a resposta é validada
e erros são classificados.

Não apresente diretamente `error.message` de bibliotecas à pessoa. Traduza o tipo
para feedback estável e registre detalhes técnicos filtrados. Uma resposta com
status de sucesso ainda pode violar o schema; parsear JSON não prova que os dados
têm campos, limites e tipos corretos.

## Evite respostas fora de ordem

Uma busca por “java” pode retornar depois da busca posterior por “javascript”.
Sem identidade, a primeira resposta sobrescreve a intenção mais recente:

```javascript
let currentRequest = 0;

async function search(query) {
  const requestId = ++currentRequest;
  dispatch({ type: "SEARCH_STARTED", requestId, query });
  try {
    const items = await client.search(query);
    if (requestId !== currentRequest) return;
    dispatch({ type: "SEARCH_SUCCEEDED", requestId, items });
  } catch (error) {
    if (requestId !== currentRequest) return;
    dispatch({ type: "SEARCH_FAILED", requestId, error: classify(error) });
  }
}
```

Cancelar a requisição anterior economiza trabalho, mas a verificação de identidade
continua útil: cancelamento pode chegar tarde ou não estar disponível em todas as
fronteiras. O reducer também pode rejeitar eventos cujo `requestId` não corresponde
ao ativo, criando defesa em profundidade contra estado obsoleto.

## Timeout, retry, backoff e orçamento

Retry serve a falhas transitórias quando repetir é seguro. Defina a política por
operação:

| Pergunta | Exemplo de decisão |
|---|---|
| a operação é idempotente? | listar é; criar pode exigir chave de idempotência |
| quais falhas são transitórias? | indisponibilidade temporária, não validação 400 |
| quantas tentativas? | uma inicial e no máximo duas repetições |
| qual orçamento total? | abandonar após 8 segundos, mesmo se restarem tentativas |
| como espaçar? | backoff exponencial limitado com jitter |
| há orientação remota? | respeitar `Retry-After` dentro do orçamento |
| a pessoa pode cancelar? | o mesmo sinal encerra espera e tentativa ativa |

Uma forma simples de jitter completo:

```javascript
function retryDelay(attempt, baseMs = 250, capMs = 4000) {
  const maximum = Math.min(capMs, baseMs * (2 ** attempt));
  return Math.random() * maximum;
}
```

Em teste, injete uma função aleatória determinística e um relógio falso. Não espere
segundos reais. A política deve retornar uma decisão testável: repetir, intervalo
e motivo.

Não repita `POST` automaticamente sem saber se o servidor o trata de forma
idempotente. Use uma chave única persistida junto da operação quando o contrato
oferecer essa capacidade. Se o cliente encerrar após enviar, mantenha a operação
como “resultado desconhecido” até consultar ou reconciliar; não diga que falhou
nem envie outra cópia cegamente.

## Cache é contrato de consistência

Todo cache precisa declarar:

- **chave:** quais parâmetros e versão compõem a identidade;
- **escopo:** usuário, workspace ou instalação;
- **valor:** resposta validada, nunca um erro arbitrário como verdade permanente;
- **validade:** TTL ou regra de expiração;
- **revalidação:** ETag, versão, data ou consulta condicional;
- **invalidação:** quais escritas afetam quais leituras;
- **offline:** por quanto tempo dado obsoleto ainda é útil;
- **sensibilidade:** pode ser persistido e exportado?

Estratégias têm trade-offs:

- **cache-first:** rápido, mas pode servir dado antigo;
- **network-first:** atualizado quando disponível, porém aumenta espera;
- **stale-while-revalidate:** mostra cache e atualiza, exigindo indicar mudança;
- **cache-only:** apropriado apenas quando ausência de atualização é aceitável.

Inclua identidade do usuário na chave ou limpe cache na troca de contexto. Uma
falha grave é mostrar dados da sessão anterior. Não cacheie token junto do objeto
de domínio nem persista corpo sensível “para depurar”.

## Local-first, offline-first e fila de saída

**Local-first** dá primazia à cópia e à resposta locais. **Offline-first** garante
jornadas definidas sem acesso remoto. Uma aplicação pode ser local-first sem
sincronização, como o Study Desk atual. Adicionar servidor exige novos estados:

```text
ação local
  -> validar e persistir localmente
  -> registrar operação { id, entityId, baseVersion, intent }
  -> pending -> sending -> acknowledged
                         -> retryable
                         -> conflict
                         -> rejected
```

A fila deve sobreviver ao reinício, preservar ordem quando necessário e usar uma
identidade idempotente. Não armazene apenas a requisição serializada; guarde a
**intenção** do domínio quando isso facilitar migração e resolução de conflito.

Após confirmação, marque a operação antes de removê-la de modo recuperável. Se a
aplicação interromper entre confirmação e limpeza, repetir com a mesma identidade
não deve duplicar o efeito. Defina limite da fila e feedback quando ele for
atingido; crescimento infinito não é resiliência.

## Conflitos e reconciliação

Last-write-wins é uma política, não ausência de política. Ela pode apagar trabalho
legítimo. Escolha conforme o domínio:

- comparação por versão e decisão da pessoa;
- merge por campos independentes;
- histórico append-only;
- operações comutativas;
- estruturas específicas de convergência quando a complexidade se justifica.

Para uma sessão editada em dois lugares, mostre “versão local” e “versão remota”,
campos diferentes e instante de cada alteração formatado para a pessoa. Permita
escolher ou combinar. Nunca descarte uma versão antes de produzir cópia de
recuperação.

Conflito também ocorre quando uma sessão foi excluída remotamente e editada
localmente. O contrato deve dizer se restaurar cria nova entidade, se edição é
arquivada ou se a exclusão prevalece. Não deixe o cliente inventar isso pela ordem
casual das respostas.

## Autenticação e autorização no cliente

Uma aplicação distribuída não consegue esconder para sempre um segredo embutido.
Não inclua credenciais permanentes no código, pacote ou log. Minimize vida e
escopo de tokens e use o mecanismo seguro disponibilizado pela plataforma para
armazenamento, quando necessário.

Trate condições separadamente:

- `401`: a autenticação pode estar ausente ou expirada; uma renovação controlada
  pode ocorrer uma vez;
- `403`: a identidade foi entendida, mas a ação não é permitida; repetir não
  concede autorização;
- logout/troca de conta: cancele operações, separe cache e limpe estado sensível;
- renovação concorrente: uma única tentativa atende clientes aguardando, evitando
  tempestade de refresh.

Não exponha token em URL, mensagem, analytics ou pacote de diagnóstico. O
[capítulo 11](11-logs-diagnostico.md) mostra redaction antes do sink.

## As cinco linguagens e uma porta comum

O mesmo contrato pode ser implementado de formas diferentes:

| Linguagem | Cliente comum | Cancelamento/timeout | Teste recomendado |
|---|---|---|---|
| Python | `urllib` ou cliente escolhido | timeout + abstração própria | adaptador fake e relógio injetado |
| Java | `java.net.http.HttpClient` | timeout e `CompletableFuture` | `HttpClient` atrás de porta |
| C | biblioteca HTTP explícita | callbacks/handles da biblioteca | função de transporte injetada |
| C# | `HttpClient` | `CancellationToken` | `HttpMessageHandler` controlado |
| JavaScript | `fetch` | `AbortSignal` | função `fetch` injetada |

Não crie uma abstração genérica que apague capacidades importantes. A porta deve
expressar o que o caso de uso precisa: `listSessions`, `pushOperation` e
`resolveConflict`, não cada opção do cliente HTTP.

## Falhas e diagnóstico determinístico

| Sintoma | Hipótese | Evidência segura | Ação |
|---|---|---|---|
| item duplicado | escrita repetida sem idempotência | operation ID e tentativas | persistir chave e reconciliar |
| busca volta no tempo | resposta fora de ordem | request ID e consulta mascarada | cancelar e rejeitar obsoleta |
| cliente insiste em 400 | retry classifica todo erro como transitório | status/classe por tentativa | tabela explícita de retry |
| dado de outra conta | chave de cache sem escopo | cache key sem PII | separar/limpar por contexto |
| fila nunca esvazia | operação permanentemente inválida | estado e razão tipada | mover para rejeitada e orientar |
| UI pisca vazia | refresh descarta dado anterior | transições do reducer | estado `Refreshing(data)` |

Registre `operationId`, `requestId`, tentativa, duração, resultado classificado e
se veio de cache. Não registre token, query pessoal, corpo completo nem títulos de
sessões. Testes devem simular timeout, cancelamento, duas respostas invertidas,
erro transitório, erro permanente, conflito e reinício com fila pendente.

## Exercícios em três níveis

### Nível 1 — Cliente de leitura

Implemente `listSessions` atrás de uma porta com timeout e validação de schema.
Modele `Loading`, `Empty`, `Success` e `Failure`, preservando dado anterior no
refresh.

**Critérios de aceite:** timeout e cancelamento são distinguíveis; JSON incompatível
é rejeitado; vazio não parece erro; renderer não chama `fetch`; testes não acessam
serviço real; logs não guardam o corpo.

### Nível 2 — Retry, cache e concorrência

Adicione busca, cache com revalidação e retry apenas para falhas transitórias.
Simule duas respostas fora de ordem e troca de usuário.

**Critérios de aceite:** resposta antiga é ignorada; backoff tem limite, jitter e
orçamento; teste usa relógio determinístico; cache inclui escopo e é invalidado na
escrita; `403` não entra em loop; submissão duplicada é impedida.

### Nível 3 — Study Desk sincronizável

Projete e implemente uma fila persistente para sincronização opcional do Study
Desk. Cubra criação, edição concorrente, exclusão remota, reinício durante envio e
operação rejeitada permanentemente.

**Critérios de aceite:** uso local continua funcionando offline; operações têm
identidade idempotente e estados explícitos; reinício não duplica efeitos;
conflito preserva ambas as versões; limite da fila é visível; pacote de diagnóstico
contém contagens e IDs efêmeros, nunca conteúdo ou credenciais.

## Checklist de conclusão

- [ ] Estado remoto não é representado por um único booleano.
- [ ] Timeout e cancelamento não prometem desfazer trabalho remoto.
- [ ] Retry possui classificação, limite, backoff, jitter e orçamento.
- [ ] Escrita só é repetida quando o contrato garante idempotência.
- [ ] Resposta obsoleta não substitui intenção recente.
- [ ] Cache declara chave, escopo, validade, revalidação e invalidação.
- [ ] Fila offline sobrevive a reinício e possui estados terminais.
- [ ] Conflito nunca perde uma versão silenciosamente.
- [ ] Troca de identidade separa cache e dados sensíveis.
- [ ] Testes simulam falhas sem depender de serviço real.
