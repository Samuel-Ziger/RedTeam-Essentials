# 25 — Projeto final e avaliação

O capstone demonstra que contrato, implementação e operação contam a mesma
história. Quantidade de endpoints não vale ponto por si só. A entrega precisa
provar invariantes sob sucesso, entrada inválida, concorrência, duplicidade,
dependência lenta e evolução.

## Objetivos

- consolidar a formação em uma API executável;
- produzir evidências reproduzíveis;
- revisar arquitetura e ameaça por decisões;
- conduzir game day e migração;
- defender limites e riscos residuais.

## 1. Escopo

Evolua a [Contract Lab API](projetos/contract-lab-api/README.md) ou crie sistema
equivalente com dados fictícios. Escolha domínio pequeno com profundidade:
catálogo, reserva de sala, tarefas ou empréstimos. Não use dado pessoal real,
serviço externo não autorizado ou funcionalidade ofensiva.

O produto deve ter:

- duas identidades e dois tenants;
- ao menos três estados de recurso;
- coleção paginada por cursor;
- escrita idempotente;
- atualização condicional;
- evento/outbox ou webhook;
- uma dependência falsa com falhas controláveis;
- um cliente em duas linguagens.

## 2. Dossiê de design

Entregue:

1. visão, consumidores, jornada e owner;
2. contexto e fronteiras de confiança;
3. linguagem do domínio, invariantes e máquina de estados;
4. duas ADRs com alternativa rejeitada e sinal de revisão;
5. matriz de autorização por objeto/propriedade;
6. threat model com riscos e controles;
7. garantias e não garantias;
8. política de versão, depreciação e retirada;
9. SLI, SLO e error budget;
10. riscos residuais aceitos.

Diagramas ajudam, mas cada seta relevante precisa dizer protocolo, identidade,
timeout e ownership.

## 3. Contrato

OpenAPI validado inclui:

- operationId estável;
- schemas separados para comandos e views;
- exemplos válidos;
- Problem Details RFC 9457;
- autenticação e autorização documentadas;
- paginação, limites e cursor;
- ETag, If-Match, Location, Retry-After quando aplicáveis;
- status felizes e falhas;
- política de idempotência;
- depreciação e versão.

Se houver evento, publique AsyncAPI ou documento equivalente com canal, envelope,
partição, entrega, ordem, retenção e compatibilidade. Webhook precisa de assinatura
e replay.

## 4. Implementação

Separe transporte, caso de uso, domínio e persistência. O domínio não depende do
framework. Use Clock e IdGenerator injetáveis ou explique por que não. Persistência
impõe tenant/version de forma atômica. Mudança + evento usam outbox ou protocolo
equivalente.

Entradas possuem limites de corpo, lista, string e complexidade. Dependências
têm timeout, resposta limitada e validação. Segredos não estão no código ou
telemetria.

## 5. Testes obrigatórios

Suite cobre:

- invariantes e transições;
- validação e campos extras;
- 401/403/404 e isolamento entre tenants;
- propriedade somente leitura;
- cursor alterado e filtro diferente;
- idempotency key igual com corpo igual/diferente;
- duas atualizações com mesma ETag;
- falha antes/depois do commit;
- duplicidade de evento/webhook;
- dependência lenta, grande e inválida;
- resposta real contra OpenAPI;
- cliente antigo contra evolução aditiva;
- canário de segredo em logs/artifacts.

Teste de carga pequeno, local e autorizado mede p50/p95/p99, erros e saturação.

## 6. Operação

Forneça dashboard ou especificação com RED, dependências, outbox e autorização.
Alertas usam SLO/burn rate ou sintomas claros. Runbook inclui:

- impacto e triagem;
- queries seguras;
- mitigação e rollback;
- backlog/replay;
- comunicação;
- verificação de recuperação;
- encerramento e pós-incidente.

Log estruturado e trace carregam request ID sem payload sensível. Auditoria
registra ações críticas com política própria.

## 7. Clientes e developer experience

Quickstart parte de checkout limpo. Um comando valida, outro inicia e outro roda
testes. Clientes em duas linguagens demonstram:

- autenticação do laboratório;
- timeout/cancelamento;
- erro tipado;
- paginação lazy;
- retry apenas quando seguro;
- envio de idempotency key;
- captura de request ID.

Geração, quando usada, é fixada e reproduzível. Nenhum arquivo gerado é editado
manualmente.

## 8. Game day

Outra pessoa opera usando somente documentação. O avaliador injeta:

1. cursor adulterado;
2. tentativa cruzada entre tenants;
3. duas escritas concorrentes;
4. timeout depois do commit;
5. backlog ou entrega duplicada;
6. dependência lenta;
7. falha do sink de auditoria;
8. cliente usando versão deprecada.

O operador deve identificar impacto, usar evidência, mitigar e verificar
recuperação sem editar banco manualmente. Registre linha do tempo e melhoria.

## 9. Rubrica — 100 pontos

| Área | Pontos | Evidência |
|---|---:|---|
| contrato e compatibilidade | 18 | spec, examples, lint e diff |
| domínio e consistência | 15 | invariantes, transações e outbox |
| segurança | 18 | ameaça, autorização e abuso |
| confiabilidade | 14 | timeout, retry, limites e concorrência |
| verificação | 15 | testes determinísticos e conformidade |
| operação | 12 | sinais, SLO, alertas e runbook |
| DX e documentação | 8 | clientes, quickstart e decisões |

Nota mínima 75. Segurança, contrato, testes e operação são gates: zero em um
deles reprova. Uma promessa sem evidência perde o item correspondente.

## 10. Revisão oral

Em até 20 minutos, explique:

- um invariante e a prova em todas as camadas;
- uma alternativa rejeitada e quando seria melhor;
- uma falha cujo resultado fica incerto;
- uma garantia que o sistema deliberadamente não oferece;
- como migraria e retiraria a versão;
- maior risco residual e owner.

## Exercícios preparatórios

### Nível 1 — rastreabilidade

Ligue dez requisitos a contrato, código, teste e sinal. **Aceite:** não há
requisito apenas na documentação.

### Nível 2 — rehearsal

Execute instalação e operação em ambiente limpo. **Aceite:** nenhum estado global
ou caminho do autor é necessário.

### Nível 3 — defesa

Peça revisão sem explicar a implementação. **Aceite:** revisor integra e
diagnostica apenas com artifacts; lacunas viram issues priorizadas.

## Checklist

- [ ] Domínio é pequeno e tecnicamente profundo.
- [ ] Contrato, código, testes e telemetria são rastreáveis.
- [ ] Concorrência, duplicidade e falha parcial foram demonstradas.
- [ ] Nenhum tenant ou segredo atravessa fronteiras.
- [ ] Outra pessoa executou quickstart e runbook.
- [ ] Migração, retirada e risco residual foram defendidos.
