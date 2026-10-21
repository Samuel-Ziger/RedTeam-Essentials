# 00 — Laboratório e governança

O laboratório representa uma empresa fictícia sem usar dados, tenants, domínios
ou credenciais reais. VMs não possuem adaptador de rede. Modelos que dependeriam
de comunicação são validados por fixtures e tabletop.

## Repositório de configuração

```text
enterprise-lab/
├── decisions/       # ADRs e riscos aceitos
├── images/          # manifests, hashes; não ISOs/WIM grandes
├── policies/        # configurações e exceções
├── identity/        # modelo sintético
├── evidence/        # saídas sanitizadas
├── runbooks/
└── tests/
```

## Gates

Fonte oficial → hash/assinatura → revisão → build reproduzível → teste →
piloto → aprovação → rollout → observação → rollback/encerramento.

Artefatos licenciados e grandes ficam fora do Git. Segredos ficam fora de
scripts/manifests. Dumps, logs e inventários recebem classificação/retenção.

## Prática

Crie a árvore, um ADR para "Server Core por padrão" e um change plan com
owner, janela, prechecks, teste, rollback e evidência.

