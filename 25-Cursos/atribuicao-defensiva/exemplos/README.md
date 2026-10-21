# Ferramentas defensivas offline

- `telemetry_correlator.py` valida e correlaciona eventos sintéticos por IDs de
  sessão/requisição/dispositivo, nunca apenas por IP;
- `evidence_manifest.py` calcula SHA-256 e tamanho de arquivos locais, sem
  alterá-los.

```bash
python3 telemetry_correlator.py ../fixtures/eventos-sinteticos.json
python3 evidence_manifest.py ../fixtures/evidencias-demo
python3 -m unittest discover -s tests -v
```

As ferramentas são didáticas. Um correlator de produção também precisa de
schema versionado, RBAC, qualidade de dados, observabilidade e revisão jurídica.

