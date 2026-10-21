# Planejador WireGuard e auditor de política

As ferramentas são totalmente offline:

- `wireguard_plan.py` valida endereços/peers e imprime templates sem segredos;
- `vpn_policy_audit.py` verifica preflight, operação e privacidade.

```bash
python3 wireguard_plan.py ../fixtures/vpn-plan.json
python3 vpn_policy_audit.py ../fixtures/vpn-policy.json
python3 -m unittest discover -s tests -v
```

O gerador nunca cria nem grava chaves. Placeholders lembram onde cada segredo
deve ser inserido no dispositivo apropriado.

