# Lab 04 — Baseline e recuperação

Execute o auditor na fixture:

```bash
python3 ../exemplos/home_audit.py ../fixtures/home-network.json
```

Trate cada achado com risco, alteração, validação e rollback. Escreva um plano
de restauração a partir de reset de fábrica, mas não o execute em produção.

**Aceite:** backup classificado como sensível, WPS/administração WAN/UPnP
decididos conscientemente e firewall IPv6 verificado.
