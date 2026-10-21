# 24 — Developer experience e governança

Uma boa API é encontrável, compreensível, experimentável, previsível e
suportável. Governança eficaz automatiza regras mecânicas, oferece caminhos
simples e reserva análise humana para decisões de domínio e risco.

## Objetivos

- desenhar jornada de integração;
- manter catálogo e scorecard;
- automatizar lint, diff, testes e publicação;
- gerir exceções e ownership;
- medir DX e ciclo de vida.

## 1. Jornada do consumidor

~~~text
descobrir -> entender -> obter acesso -> primeira chamada
          -> integrar -> operar -> migrar -> encerrar
~~~

Documentação precisa responder propósito, ambiente, autenticação, quickstart,
erros, limites, exemplos, SDKs, suporte e changelog. Sandbox usa dados fictícios
e comportamento representativo, sem credencial de produção.

Meça time-to-first-success, taxa de integração sem suporte, erros iniciais e
tempo de migração. Page views não provam sucesso.

## 2. Catálogo mínimo

Cada API registra:

- owner técnico e de produto;
- consumidores e criticidade;
- ambientes e exposição;
- contrato e versão publicada;
- dados/classificação;
- autenticação/autorização;
- SLO, dashboards e runbook;
- dependências e custos;
- política de versão/retirada;
- última revisão e status.

O pipeline atualiza catálogo; planilha manual envelhece. Descoberta automática
ajuda, mas owner confirma semântica e criticidade.

## 3. Padrões automatizáveis

- validação OpenAPI/AsyncAPI/Protobuf/GraphQL;
- nomenclatura e operationId;
- problems e respostas comuns;
- segurança declarada;
- limites e paginação;
- exemplos contra schemas;
- breaking diff;
- geração reproduzível;
- testes de contrato;
- links, owner e metadata.

Lint não sabe se refund pode ocorrer após settlement. Revisão humana cobre
domínio, ameaça, privacidade, SLO e trade-offs.

## 4. Golden path e exceções

Template oferece contrato, handlers de erro, telemetria, CI, SDK e runbook
básicos. Ele reduz decisões repetitivas sem virar plataforma rígida.

Exceção deve registrar regra, justificativa, risco, compensação, owner e
expiração. Exceção permanente sem revisão é uma segunda política escondida.

## 5. Scorecard

Um scorecard pode avaliar:

| Área | Evidência |
|---|---|
| ownership | owner e contato válidos |
| contrato | validado e publicado |
| compatibilidade | diff no CI |
| segurança | threat model e testes |
| operação | SLO, alertas, runbook |
| lifecycle | versão, deprecation, consumidores |
| DX | quickstart executável e sandbox |

Não transforme score em competição. Gate essencial impede publicação; aviso
orienta melhoria; tendência mostra maturidade.

## 6. Portal e documentação

Portal deve servir artifact versionado, exemplos executáveis e changelog.
Documentação gerada descreve forma; guias manuais explicam jornada, decisões e
falhas. Snippets precisam rodar no CI para não apodrecer.

Busca e links permanentes importam. Uma versão antiga deve continuar acessível
durante suporte. Nunca exponha credencial real em Try It.

## 7. Governança federada

Equipe central mantém princípios, tooling e componentes. Times de domínio mantêm
contratos e operação. Architecture review entra em mudanças de alto risco, não
em toda rota. Comunidade de prática compartilha decisões e incidentes.

Métricas úteis:

- tempo de aprovação e primeira chamada;
- breaking changes prevenidas;
- APIs sem owner/contrato/SLO;
- adoção por versão;
- incidentes por incompatibilidade;
- idade de exceções;
- tempo de sunset.

## 8. Maturidade e resposta a incidentes

Incidente de compatibilidade deve retornar ao sistema de governança. Registre
qual regra faltou, por que review/teste não a detectou e como o golden path será
melhorado. Evite responder com mais um checklist manual quando um validador ou
teste de consumidor pode impedir recorrência. Scorecards medem tendência por
API e por portfólio; não escondem risco crítico numa média alta. Uma API sem
owner, inventário ou procedimento de retirada permanece bloqueada, ainda que
tenha documentação elegante.

## Falhas comuns

| Falha | Resultado | Correção |
|---|---|---|
| comitê em toda mudança | fila | automação + risco |
| template obrigatório sem saída | workaround | exceção governada |
| portal sem fonte | docs antigas | artifact do pipeline |
| score sem consequência | decoração | gates/owners |
| medir endpoints | vaidade | jornada e confiabilidade |

## Exercícios

### Nível 1 — catálogo

Cadastre uma API com todos os campos mínimos. **Aceite:** links apontam artifacts
versionados e owners reais.

### Nível 2 — scorecard

Crie dez checks automáticos e cinco humanos. **Aceite:** cada falha tem owner e
consequência.

### Nível 3 — golden path

Monte template que publica contrato, mock, SDK e docs. **Aceite:** projeto novo
chega à primeira chamada com comandos reproduzíveis e sem segredo.

## Checklist

- [ ] Jornada do consumidor é medida.
- [ ] Catálogo nasce do pipeline.
- [ ] Regras mecânicas são automatizadas.
- [ ] Decisões de domínio recebem revisão humana.
- [ ] Exceções têm risco, owner e expiração.
- [ ] Documentação e exemplos são versionados e testados.
