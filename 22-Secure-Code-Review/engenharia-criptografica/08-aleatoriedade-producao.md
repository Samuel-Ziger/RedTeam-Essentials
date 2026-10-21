# 08 — Aleatoriedade em produção

Aplicações consomem CSPRNG do sistema; fabricantes de geradores e módulos seguem
processos específicos de fonte de entropia, DRBG, health tests e reseed. Containers
clonados, boot inicial, devices embarcados e snapshots merecem avaliação.

Falha de RNG deve impedir geração de chave/nonce, não cair para timestamp ou
PID. Monitore erros e volume sem logar saída. Determinismo é útil em testes
somente quando injetado e impossível de habilitar silenciosamente em produção.

## Prática

Documente fonte, API, condição de falha e teste de snapshot do seu ambiente.
