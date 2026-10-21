# 18 — Secrets, rotação e observabilidade

Secret manager controla autenticação, política, versão, auditoria e entrega de
segredos. Criptografia não elimina a necessidade de restringir quem pode pedir
decriptação. Prefira identidades de workload e credenciais curtas a segredos
estáticos distribuídos em arquivos.

Rotação precisa de sobreposição limitada: publicar nova versão, atualizar
consumidores, observar uso antigo, revogar e verificar. Logs registram operação,
principal, key ID e resultado; filtros impedem valor, plaintext ou token.

## Prática

Modele rotação sem downtime e um alarme para consumidor preso na versão antiga.
