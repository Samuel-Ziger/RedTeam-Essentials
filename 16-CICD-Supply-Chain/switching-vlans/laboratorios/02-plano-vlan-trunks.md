# Lab 02 — Plano de VLAN e trunks

Edite uma cópia de `fixtures/vlan-plan.json`: adicione voz e impressoras, limite
os trunks e associe portas access. Execute:

```bash
python3 ../exemplos/vlan_plan.py ../fixtures/vlan-plan.json
```

**Aceite:** IDs/prefixos únicos, nenhuma VLAN ausente, VLAN nativa não usada por
usuário/gestão e trunks com allowlist mínima.
