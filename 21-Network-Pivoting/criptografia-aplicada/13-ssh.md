# 13 — SSH, host keys e agentes

SSH separa host key, chave de usuário e chave de sessão. `known_hosts` liga
host a chave; aceitar mudança sem investigação remove a proteção contra
intermediário. Uma CA SSH pode emitir certificados curtos e centralizar política.

Agentes evitam copiar chave privada, mas encaminhamento amplia onde ela pode ser
usada. Restrinja forwarding, duração, comandos e destinos. Prefira Ed25519 ou
algoritmos aprovados no ambiente, inventarie legados e proteja recuperação.

## Prática

Documente bootstrap de host key, rotação planejada e resposta a alerta de chave
alterada.
