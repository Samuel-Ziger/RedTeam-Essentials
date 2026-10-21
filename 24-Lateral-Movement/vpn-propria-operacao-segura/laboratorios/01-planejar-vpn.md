# Lab 01 — Planejar antes de implantar

1. Copie as fixtures para diretório temporário.
2. Defina objetivo, usuários, serviços e volume.
3. Escolha full ou split tunnel e justifique.
4. Verifique sobreposição com LAN, VPC e containers.
5. Defina DNS, IPv6, endpoint, porta e interface de saída.
6. Execute:

```bash
python3 ../exemplos/wireguard_plan.py ../fixtures/vpn-plan.json
python3 ../exemplos/vpn_policy_audit.py ../fixtures/vpn-policy.json
```

## Testes negativos

Duplique um IP de peer, use prefixo sobreposto e remova o console de recuperação.
As ferramentas devem rejeitar ou alertar.

## Evidência

Templates com placeholders, relatório do auditor e registro das decisões.

