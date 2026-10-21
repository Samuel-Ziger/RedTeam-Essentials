# Respostas orientativas

Estas respostas descrevem critérios e raciocínio, não um projeto único. Compare
depois de executar os exercícios e preserve decisões diferentes quando sua
evidência as sustenta.

## Práticas 01–10 — contrato e HTTP

**01. Proposta:** deve nomear tarefa do consumidor, estado que pertence ao
provider, owner, dados, limites, SLO e ao menos uma não garantia. Endpoints vêm
depois.

**02. Máquina de estados:** cada seta possui comando, ator, estado de origem,
precondição, resultado e evento. Transição ausente é rejeitada, não improvisada.

**03. Métodos/status:** GET é seguro; PUT/DELETE são idempotentes no efeito; POST
não é por padrão. 201 cria, 202 aceita trabalho, 204 não carrega corpo, 412
representa precondição falsa.

**04. Negociação:** Content-Type inválido produz 415; Accept impossível, 406.
Vary inclui a dimensão que seleciona a representação.

**05. Cache:** primeira resposta contém ETag e política. If-None-Match atual
produz 304 sem corpo; ETag muda quando a representação relevante muda.

**06. Concorrência:** compare-and-set ocorre no UPDATE/commit. Duas escritas com
a mesma ETag resultam em um sucesso e um 412.

**07. Job:** 202 só é útil com identidade consultável. Estados incluem queued,
running, succeeded/failed/cancelled e resultado/erro seguro.

**08. Schemas:** Create não recebe ID/version; Patch distingue ausente/null; View
não expõe segredo; Event contém o mínimo estável.

**09. Limites:** rejeição ocorre antes de parse/alocação cara e cobre bytes após
descompressão, profundidade, itens e tempo.

**10. Problems:** clientes usam type/code, nunca detail. 401, 403, 404, 409, 412,
422, 429, 500 e 503 levam a ações diferentes.

## Práticas 11–23 — coleção, evolução e identidade

**11. Keyset:** consulta usa condição lexicográfica e ORDER BY com a mesma chave
composta. ID desempata timestamps iguais.

**12. Cursor:** payload leva versão, posição e digest/filtros; HMAC impede
alteração. Tamanho é validado antes de decode.

**13. Coleção móvel:** inserções posteriores podem aparecer; mudança de filtro
pode remover item. Se isso é inaceitável, use watermark/snapshot com custo
declarado.

**14. Idempotência:** escopo + operação + chave apontam digest canônico, estado e
resposta. Chave igual com digest diferente é 409.

**15. Crash:** efeito e registro confirmam juntos. Timeout após commit reproduz
a resposta ou reconcilia; nunca assume que nada aconteceu.

**16. Diff:** campo opcional pode passar; remoção, tipo, required, limite menor e
status removido falham. Mudança semântica ainda exige review.

**17. Enum:** cliente preserva valor desconhecido, escolhe fallback não perigoso
e emite sinal. Switch exaustivo sem default é incompatível.

**18. Sunset:** alternativa existe antes do aviso; uso é medido por consumidor;
remoção depende de evidência e tem rollback.

**19. Identidade:** SPA usa code + PKCE; workload usa identidade própria; CLI usa
device/loopback conforme suporte. ID token não substitui access token.

**20. JWT:** assinatura, algoritmo permitido, issuer, audience e tempos são gates
antes de scopes/ownership.

**21. Rotação:** chave antiga/nova coexistem por janela. Cache respeita refresh;
kid desconhecido consulta somente issuer configurado e tem limite.

**22. Matriz:** default deny. Testes incluem objeto real de outro tenant,
propriedade sensível, estado arquivado e função privilegiada.

**23. Multitenancy:** tenant deriva da identidade e participa de banco, cache,
idempotência, busca, evento e job. ID opaco não é controle.

## Práticas 24–32 — segurança, contrato e dados

**24. Threat model:** risco sem prevenção, detecção, teste e owner está
incompleto. Inclua usuário legítimo automatizando fluxo sensível.

**25. Recursos:** limite por identidade/tenant/operação/custo e concorrência.
Corpo enorme é bloqueado antes da leitura completa.

**26. SSRF:** allowlist quando possível, HTTPS/porta, resolução controlada,
bloqueio de redes internas, redirecionamento revalidado e proxy de egress.

**27. Dependência hostil:** status, media type, tamanho e schema são validados.
Timeout e circuit limitam propagação; resposta externa não entra diretamente no
domínio.

**28. OpenAPI:** schemas, examples, security, problems, headers e limites
validam. operationId é único e estável.

**29. Drift:** compare operações do runtime e valide respostas reais. Alteração
manual só no código ou só na spec falha no CI.

**30. Caso de uso:** controller converte transporte. Domínio não importa
framework; repositório expressa operações do domínio.

**31. Outbox:** estado + evento pendente ficam na mesma transação. Crash depois
de publish pode duplicar; inbox impede efeito duplicado.

**32. Saga:** compensação é nova operação de negócio. Se compensar falha, estado
manual_review preserva verdade e tem runbook.

## Práticas 33–40 — resiliência e verificação

**33. Deadline:** soma de orçamentos internos é menor que o externo e inclui
margem. Prazo restante é propagado e cancelamento libera recurso.

**34. Retry:** 400 não repete; 429/503/timeout podem repetir quando operação é
segura, com backoff, jitter, teto e budget total.

**35. Backpressure:** fila limitada estabiliza memória e rejeita cedo. Compare
idade, p99 e tempo de recuperação, não apenas throughput.

**36. SLO:** numerador, denominador, janela, fonte e exclusões são explícitos.
Error budget não exclui o incidente que deveria medir.

**37. Canário:** valor não aparece em resposta, stdout, stderr, log, trace,
artifact ou bundle. Redação ocorre antes de cada sink.

**38. Fault injection:** antes do commit não há efeito; depois do commit pode
haver resposta perdida; depois do publish pode duplicar. Cada estado tem
reconciliação.

**39. Propriedades:** decode/encode, tamper rejection, normalização idempotente,
isolamento e replay único são boas propriedades. Preserve seed.

**40. Carga:** cenário declara distribuição, ramp-up, baseline, SLO, saturação e
stop condition. Média sem p95/p99 não basta.

## Práticas 41–45 — integrações e entrega

**41. Webhook:** HMAC cobre timestamp + bytes exatos, comparação é constante,
event ID bloqueia replay e rotação usa key ID/overlap.

**42. Eventos:** sequence por agregado detecta antigo/lacuna; inbox deduplica;
replay de projeção não reenvia efeito externo.

**43. GraphQL/gRPC:** GraphQL deve provar redução do N+1 e limite de custo; gRPC
deve reservar field numbers e propagar deadline/cancelamento.

**44. SDKs:** ambos expõem erro tipado, request ID, iterator lazy, timeout e
cancelamento. POST só repete com chave estável.

**45. Game day:** operador usa contrato, sinais e runbook; não edita banco. O
encerramento prova SLO recuperado, backlog normal e estados incertos
reconciliados.

## Como avaliar uma resposta diferente

Uma solução alternativa é boa quando:

1. preserva os invariantes;
2. declara garantias e não garantias;
3. possui teste reproduzível;
4. produz evidência operacional;
5. limita falha e dados;
6. explica custo e condição de revisão.
