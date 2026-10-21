# Simulador de rotas e ACL

`route_policy.py` implementa dois mecanismos didáticos:

- longest-prefix, preferência e métrica sobre fixture;
- ACL stateless first-match sobre prefixos, protocolo e porta.

```bash
python3 route_policy.py lookup ../fixtures/routes.json 10.20.30.40
python3 route_policy.py acl ../fixtures/acl.json 10.1.10.5 10.2.20.8 tcp 443
python3 -m unittest discover -s tests -v
```

Ele não altera rotas ou firewall do sistema.
