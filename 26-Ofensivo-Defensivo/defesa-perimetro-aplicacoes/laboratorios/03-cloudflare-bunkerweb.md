# Laboratório 03 — Cloudflare e BunkerWeb

## Objetivo

Comparar uma borda gerenciada e uma autogerenciada por responsabilidade, não por
marketing. O compose de exemplo é revisado, mas não iniciado automaticamente.

## Red

Revise `fixtures/bunkerweb-compose.exemplo.yml` e identifique superfície de
dados, gestão, volumes, rede, versão e portas. Para Cloudflare, modele DNS,
custom/managed rules, origem e conta administrativa.

## Blue

Preencha para cada opção: patching, integridade, segredo, log, retenção,
backup, HA, DDoS a montante, MFA, rollback, custo e dependência.

## Purple

Escolha uma arquitetura para um site pequeno e outra para uma empresa regulada.
Justifique com requisitos. Inclua plano híbrido se fizer sentido e deixe claro
que WAF autogerenciado não absorve ataque que já saturou o link.
