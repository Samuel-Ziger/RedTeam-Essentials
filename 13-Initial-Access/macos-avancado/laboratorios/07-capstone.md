# Lab 07 — Capstone empresarial

Projete uma organização fictícia com 50 Macs e três perfis de trabalho. Modele
sem conectividade: hardware/lifecycle, ADE, MDM/DDM, identidade, FileVault,
software, update, baseline, observabilidade, suporte e offboarding.

## Incidentes de mesa

- update causa incompatibilidade no piloto;
- app perde assinatura ou ticket esperado;
- perfil duplicado cria conflito;
- recovery key não está disponível ao time autorizado;
- dispositivo fica sem status durante rollout.

## Critério

Cada decisão possui owner, evidência, limite de privacidade, fallback e cleanup.
Dependências de APNs, IdP, DNS, certificados e transporte são marcadas para o
módulo de redes, sem inventar uma implantação incompleta.
