# Ferramentas offline

As ferramentas aceitam apenas arquivos locais, validam `authorized: true` e
imprimem JSON. Não abrem sockets nem chamam subprocessos.

## Motor de risco explicável

```bash
python3 edge_risk_engine.py ../fixtures/requests-sinteticas.json
```

Combina taxa, falhas, enumeração, anomaly score, estado e identidade. O modelo
é didático e não deve ser promovido a produção como classificador pronto.

## Auditor de controles

```bash
python3 control_plane_audit.py ../fixtures/politica-edge.json
```

Verifica invariantes de firewall, origem, WAF, Turnstile, MFA, logs e mudança.

## Simulador token bucket

```bash
python3 token_bucket.py ../fixtures/eventos-rate-limit.json
```

Usa timestamps da fixture para permitir testes reproduzíveis sem esperar ou
enviar requisições.
