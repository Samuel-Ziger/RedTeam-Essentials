# 19 — Implementação e testes do RNP/1

Leia a [especificação](PROTOCOLO-RNP1.md) antes do código. A implementação
possui codec, leitura exata, limite de payload e máquina de estados.

```bash
python3 exemplos/rnp1_demo.py
python3 -m unittest discover -s exemplos/tests -v
```

O demo prefere `socket.socketpair()`, dois sockets conectados dentro do processo,
sem bind, porta ou tráfego externo. Em sandbox que bloqueia sockets locais, usa
um fluxo fragmentado em memória. Ambos exercitam handshake, DATA, PING/PONG e CLOSE.

## Estratégia de testes

- vetores conhecidos de bytes;
- round-trip encode/decode;
- todos os tipos e limites 0/máximo/máximo+1;
- magic, versão, flags, tipo e comprimento inválidos;
- leitura fragmentada e EOF parcial;
- transições válidas/fora de ordem;
- fuzzing bounded do parser;
- interoperabilidade entre duas implementações independentes antes de produção.

Coverage alto não prova conformidade; derive testes normativos de cada MUST.
