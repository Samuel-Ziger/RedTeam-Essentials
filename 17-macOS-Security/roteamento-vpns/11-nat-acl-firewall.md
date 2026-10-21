# 11 — NAT, ACL e firewall

ACL stateless avalia campos de pacote e ordem de regras; retorno precisa de regra
quando não há estado. Firewall stateful acompanha sessões e pode entender
aplicação/identidade. NAT traduz endereços/portas e é função distinta.

Defina política como origem, destino, protocolo/serviço, direção, identidade,
ação, log, dono e validade. Regras específicas devem preceder genéricas quando
a plataforma usa first-match. Implicit deny precisa ser conhecido.

NAT estático, dinâmico e PAT atendem necessidades diferentes. Ordem NAT versus
política varia por produto; documente endereço real e traduzido nos logs.

## Prática

```bash
python3 exemplos/route_policy.py acl fixtures/acl.json 10.1.10.5 10.2.20.8 tcp 443
```

O simulador ensina first-match, mas não substitui semântica do fabricante.
