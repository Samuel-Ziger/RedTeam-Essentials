# Laboratório 05 — Capstone Contract Lab

## Pré-requisitos

- [Laboratório 01](lab-01-contrato-http.md)
- [Laboratório 02](lab-02-contrato-seguranca.md)
- [Laboratório 03](lab-03-servico-operavel.md)
- [Laboratório 04](lab-04-integracoes-clientes.md)
- [Caderno de práticas](../CADERNO-PRATICAS.md)
- [Guia de diagnóstico](../GUIA-DIAGNOSTICO.md)
- [Projeto e avaliação](../25-projeto-avaliacao.md)
- [Contract Lab API](../projetos/contract-lab-api/README.md)

## Missão

Entregue a API como produto operável. Um avaliador novo deve instalar, integrar,
provocar falhas, diagnosticar, recuperar e planejar migração sem conversa privada
com o autor.

## Entrega

- proposta, contexto e duas ADRs;
- domínio, invariantes e máquina de estados;
- threat model e matriz de autorização;
- OpenAPI/contrato de evento validados;
- implementação e clientes em duas linguagens;
- suite de contrato, abuso, concorrência e falha;
- SLO, dashboards, alertas e runbook;
- catálogo/scorecard e política de depreciação;
- artifacts reproduzíveis em checkout limpo;
- gravação textual do game day e pós-incidente.

## Cenário do avaliador

O avaliador injeta cursor adulterado, tenant cruzado, mesma chave com outro
payload, ETag antiga, timeout depois do commit, evento duplicado, dependência
lenta, backlog e cliente de versão anterior.

Você não pode corrigir dado manualmente durante a avaliação. Use somente
interfaces e runbooks previstos. Se o estado ficar incerto, reconcilie e preserve
evidência.

## Gates essenciais

- contrato: runtime e spec concordam;
- segurança: isolamento e segredo canário passam;
- dados: commit/outbox/duplicidade são verdadeiros;
- confiabilidade: deadline, retry e limites são demonstrados;
- operação: SLO, alerta e runbook funcionam;
- evolução: cliente antigo e plano de sunset existem.

## Aprovação

Use a rubrica do capítulo 25. Nota mínima 75, sem gate essencial zerado. Issues
residuais têm severidade, owner e prazo; não são escondidas para elevar a nota.

## Retrospectiva

Responda:

1. qual garantia exigiu mais camadas;
2. qual hipótese de consumidor estava errada;
3. qual falha ainda pede intervenção;
4. qual controle gerou mais custo operacional;
5. o que mudaria antes de uma publicação real.
