# 01 — Modelo operacional empresarial

Tecnologia sem ownership vira dívida. Organize pessoas, processo e plataforma.

## Funções

- service owner define resultado/SLO e aceita risco;
- platform owner mantém imagem, baseline e tooling;
- security define controles e monitora eficácia;
- operations executa mudanças/incidentes;
- application owner valida compatibilidade;
- data owner classifica e define retenção;
- auditor verifica evidência independente.

## Ambientes e anéis

Dev/lab → validação → piloto → broad → critical. Um anel é grupo com
risco e critério de promoção, não apenas atraso de dias. Cada transição exige
health, compatibilidade, telemetria e rollback.

## Artefatos essenciais

CMDB/inventário, catálogo de software, matriz de suporte, baseline, exceções,
runbooks, backup tests, change records, incident reviews e roadmap de lifecycle.

## Exercício

Modele RACI e SLO para endpoints, servidores e imagem de referência. Inclua
quem pode aprovar exceção e quando ela expira.

