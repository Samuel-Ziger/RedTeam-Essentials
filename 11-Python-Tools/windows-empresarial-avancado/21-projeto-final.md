# 21 — Projeto final: plataforma Windows empresarial de referência

## Cenário

Projete uma organização fictícia com três personas de endpoint, dois workloads
Server Core e uma futura floresta. A implementação permanece offline; itens que
dependem de redes são contratos prontos para o módulo correspondente.

## Entregáveis

1. modelo operacional, RACI, SLOs e anéis;
2. catálogo de SKUs/builds/lifecycle;
3. pipeline de imagem com WIM read-only lab, hashes e change log;
4. unattend sem secrets e validação;
5. autoridade de política e baseline versionada;
6. modelo AD de OU/grupos/delegação validado offline;
7. designs de GPO, gMSA/LAPS, PKI e JEA;
8. rollout App Control/Defender/VBS/BitLocker por audit/pilot/enforce;
9. schema de inventário e relatório de drift;
10. logging/detections/tabletop de incidente;
11. backup/forest recovery/HA tabletop com RPO/RTO;
12. dependências formais para redes, sem implementá-las.

## Defesa

Apresente ADRs, riscos, exceções, testes e rollback. Um avaliador introduz uma
build fora de suporte, grupo cíclico, setting divergente e exceção expirada; as
ferramentas devem detectar sem corrigir automaticamente.

## Rubrica

Arquitetura 20%, identidade/política 20%, segurança 20%, automação/evidência
20%, continuidade 15%, clareza/cleanup 5%. Secrets ou implantação prematura de
rede/domínio invalidam o projeto.

