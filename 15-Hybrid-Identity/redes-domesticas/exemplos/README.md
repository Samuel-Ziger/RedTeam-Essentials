# Auditor offline de rede doméstica

`home_audit.py` recebe um documento JSON declarativo e produz achados; ele não
se conecta ao roteador e não aceita credenciais.

```bash
python3 home_audit.py ../fixtures/home-network.json
python3 -m unittest discover -s tests -v
```

O schema deliberadamente registra classes de dispositivo, não pessoas, MACs,
seriais ou PSKs.
