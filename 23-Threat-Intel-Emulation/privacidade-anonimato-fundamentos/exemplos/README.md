# Ferramenta offline de modelo de privacidade

`privacy_model.py` valida um cenário JSON e produz uma matriz textual de
observadores, achados e controles. Ele não abre sockets, não consulta IPs e não
tenta identificar ninguém.

```bash
python3 privacy_model.py ../fixtures/cenario-pesquisa.json
python3 -m unittest discover -s tests -v
```

O formato aceita atividades com:

- `https`: proteção TLS de aplicação;
- `vpn`: `none`, `commercial`, `self_hosted` ou `corporate`;
- `tor_browser`: se a atividade usa Tor Browser;
- `dns`: `system`, `encrypted`, `tunnel` ou `unknown`;
- `endpoint_trusted`: estado assumido do dispositivo;
- `identifiers`: identificadores presentes;
- `observer_model`: `local`, `service`, `provider` ou `global`.

As conclusões são heurísticas educacionais. Elas organizam perguntas; não são
prova forense nem certificação de anonimato.

