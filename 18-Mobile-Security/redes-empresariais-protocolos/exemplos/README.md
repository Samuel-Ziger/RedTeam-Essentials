# Exemplos — arquitetura e RNP/1

- `architecture_audit.py`: valida sites, prefixos, owners e SLOs de uma fixture;
- `rnp1.py`: codec incremental, leitura exata e servidor de estado RNP/1;
- `rnp1_demo.py`: sessão completa por `socketpair`, sem abrir porta;
- `tests/`: limites, framing fragmentado, estado, auditor e fuzzing bounded.

```bash
python3 architecture_audit.py ../fixtures/architecture.json
python3 rnp1_demo.py
python3 -m unittest discover -s tests -v
```
