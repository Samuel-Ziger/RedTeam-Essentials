# Caderno de práticas — Engenharia de APIs

Estas 45 práticas convertem leitura em evidência. N1 fixa fundamentos, N2 integra
controles e N3 exige decisão, falha injetada e defesa. Use o Contract Lab, dados
fictícios e somente serviços locais ou autorizados.

Para cada entrega registre hipótese, versões, entrada, comando, saída, falha,
correção e teste de regressão. Consulte [respostas](RESPOSTAS.md) depois de tentar.

## Contrato e HTTP

### 01 — Proposta de API (N1)

Escreva consumidor, tarefa, owner, invariantes e não garantias. **Aceite:** nenhum
endpoint é necessário para explicar o problema.

### 02 — Máquina de estados (N1)

Modele três estados e transições. **Aceite:** ator, precondição, efeito e erro
aparecem em cada transição.

### 03 — Métodos e status (N1)

Classifique doze operações. **Aceite:** segurança, idempotência e status são
justificados pela intenção.

### 04 — Negociação (N2)

Sirva JSON e rejeite media type incompatível. **Aceite:** Content-Type, Accept,
406 e 415 são testados.

### 05 — Cache condicional (N2)

Implemente GET com ETag/If-None-Match. **Aceite:** 304 não possui corpo e mantém
metadados necessários.

### 06 — Concorrência HTTP (N2)

Implemente PATCH com If-Match. **Aceite:** duas escritas baseadas na mesma versão
não perdem atualização.

### 07 — Trabalho assíncrono (N2)

Modele exportação como recurso. **Aceite:** aceitação, progresso, resultado,
falha, expiração e cancelamento são consultáveis.

### 08 — Quatro representações (N1)

Crie schemas Create, Patch, View e Event. **Aceite:** campos server-only e
write-only não atravessam a borda errada.

### 09 — Limites de entrada (N2)

Teste bytes, strings, listas, profundidade e expansão. **Aceite:** rejeição
ocorre antes do trabalho caro.

### 10 — Catálogo de problemas (N1)

Defina dez Problems RFC 9457. **Aceite:** type/code, status, ação e retry são
estáveis; detail não é chave de decisão.

## Coleções, evolução e identidade

### 11 — Paginação keyset (N2)

Use createdAt + id. **Aceite:** empate e inserção concorrente não produzem
omissão pela ordem incompleta.

### 12 — Cursor assinado (N3)

Vincule cursor a filtro e versão. **Aceite:** adulteração, tamanho e uso em outra
consulta falham com problema seguro.

### 13 — Coleção em movimento (N2)

Altere itens entre páginas. **Aceite:** garantia observada e alternativa de
snapshot estão documentadas.

### 14 — Chave idempotente (N2)

Registre scope, digest e resposta. **Aceite:** replay igual preserva resultado e
payload divergente recebe conflito.

### 15 — Crash idempotente (N3)

Falhe antes/depois do commit. **Aceite:** nenhuma janela duplica efeito ou afirma
resultado falso.

### 16 — Diff de contrato (N2)

Faça mudança aditiva e breaking. **Aceite:** pipeline permite a primeira e bloqueia
a segunda.

### 17 — Enum desconhecido (N2)

Execute cliente antigo com valor novo. **Aceite:** fallback é seguro, preserva o
valor e gera evidência.

### 18 — Sunset (N2)

Crie plano de retirada. **Aceite:** consumidores, alternativa, métricas, datas,
comunicação, rollback e confirmação existem.

### 19 — Fluxos de identidade (N1)

Desenhe SPA, workload e CLI. **Aceite:** credential, audience, scope, expiração e
revogação são distintos.

### 20 — Validação JWT (N2)

Teste assinatura, alg, issuer, audience, exp, nbf e kid. **Aceite:** nenhum caso
inválido chega à autorização.

### 21 — Rotação de chave (N3)

Simule JWKS antigo/novo. **Aceite:** overlap, cache, kid desconhecido e rollback
têm comportamento.

### 22 — Matriz de autorização (N1)

Cruze sujeito, ação, objeto, estado e campo. **Aceite:** default deny e casos
negativos dominam a tabela.

### 23 — Isolamento multitenant (N3)

Teste GET, lista, PATCH, cache, evento e job com A/B. **Aceite:** nenhum dado ou
efeito atravessa tenant.

## Segurança, contrato e implementação

### 24 — Threat model (N2)

Mapeie ativos, fronteiras, abuso e dependências. **Aceite:** cada risco possui
prevenção, detecção, teste e owner.

### 25 — Consumo de recursos (N2)

Teste lote, corpo, complexidade, concorrência e frequência. **Aceite:** limites
protegem capacidade sem depender apenas de IP.

### 26 — SSRF defensivo (N3)

Valide destinos em fake local. **Aceite:** esquema, redirecionamento, DNS, redes
internas, tamanho e timeout são controlados; não use alvos externos.

### 27 — Dependência hostil (N3)

Fake retorna lento, grande, tipo errado e schema inválido. **Aceite:** adapter
limita e traduz sem corromper domínio.

### 28 — OpenAPI completo (N2)

Descreva quatro operações. **Aceite:** examples, errors, security, headers,
limites e paginação validam.

### 29 — Drift runtime/spec (N3)

Compare implementação ao contrato-fonte. **Aceite:** mudar status, media type ou
campo obrigatório quebra o teste.

### 30 — Extração de caso de uso (N2)

Remova regra do controller. **Aceite:** domínio roda sem framework e adapter só
traduz.

### 31 — Outbox (N3)

Grave estado + evento e simule crash. **Aceite:** evento não se perde, pode
duplicar e consumidor deduplica.

### 32 — Saga (N3)

Falhe etapa e compensação. **Aceite:** estados uncertain/manual_review têm
reconciliação e runbook.

## Resiliência, observabilidade e testes

### 33 — Orçamento de deadline (N1)

Distribua 800 ms em duas dependências. **Aceite:** sobra margem para resposta e
cancelamento.

### 34 — Retry com jitter (N2)

Simule 400, 429, 503 e timeout. **Aceite:** apenas transitórios repetem dentro do
orçamento.

### 35 — Backpressure (N3)

Compare fila limitada e ilimitada. **Aceite:** registre p99, memória, idade,
rejeição e recuperação.

### 36 — SLI/SLO (N2)

Defina disponibilidade e latência. **Aceite:** numerador, denominador, janela,
fonte, exclusões e budget são inequívocos.

### 37 — Canário de segredo (N2)

Provoque erros com segredo sintético. **Aceite:** canário não aparece em logs,
traces, métricas, resposta ou artifact.

### 38 — Fault injection (N3)

Falhe antes/depois de commit, publish e resposta. **Aceite:** estado real,
resultado e retry permanecem coerentes.

### 39 — Propriedades (N2)

Gere entradas para cursor, normalização e idempotência. **Aceite:** seed é
reproduzível e falha reduzida vira regressão.

### 40 — Carga local (N3)

Execute ramp-up autorizado. **Aceite:** workload, baseline, p50/p95/p99,
saturação e critério de parada são registrados.

## Integrações, clientes e governança

### 41 — Webhook (N3)

Assine bytes, entregue duplicado e rotacione chave. **Aceite:** replay não gera
segundo efeito e tentativas ficam observáveis.

### 42 — Consumidor de eventos (N3)

Entregue duplicado, fora de ordem e com lacuna. **Aceite:** estado não regride,
lacuna alerta e replay é seguro.

### 43 — GraphQL ou gRPC (N2)

Escolha um. **Aceite:** GraphQL prova batching/custo/autorização; gRPC prova
evolução/deadline/status.

### 44 — SDK em duas linguagens (N3)

Implemente paginação lazy e cancelamento. **Aceite:** erros, retry e idempotência
têm comportamento equivalente.

### 45 — Game day do capstone (N3)

Outra pessoa opera enquanto falhas são injetadas. **Aceite:** diagnóstico,
mitigação, recuperação e pós-incidente usam somente artifacts entregues.

## Diário de aprendizagem

Após cada bloco, responda:

1. Qual garantia agora possui prova automatizada?
2. Que hipótese foi refutada?
3. Qual falha ainda exige intervenção manual?
4. Qual decisão merece ADR?
5. Outro consumidor reproduziu o resultado?

