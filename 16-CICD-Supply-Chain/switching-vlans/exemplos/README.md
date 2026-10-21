# Validador de plano de VLAN

`vlan_plan.py` valida um modelo neutro: VLANs, prefixos IPv4, portas access e
trunks. Ele não gera configuração nem acessa equipamentos.

```bash
python3 vlan_plan.py ../fixtures/vlan-plan.json
python3 -m unittest discover -s tests -v
```

Um resultado válido prova consistência estrutural, não que o desenho atende todos
os requisitos ou que foi implantado corretamente.
