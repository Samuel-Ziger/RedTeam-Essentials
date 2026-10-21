# 17 — Migração, depreciação e incidentes

Migração: descobrir, priorizar, testar, implantar leitura compatível, mudar
escrita, converter histórico, observar, retirar e provar ausência. Exceções têm
dono, prazo e controle compensatório. Backup e rollback não podem reintroduzir
formatos já proibidos silenciosamente.

Incidente criptográfico pode ser chave exposta, nonce repetido, certificado
indevido, RNG falho ou vulnerabilidade de biblioteca. Preserve evidência,
contenha uso, avalie dados afetados, rotacione/reemita, corrija a causa e
notifique conforme obrigações.

## Prática

Faça tabletop de nonce GCM repetido e identifique por que apenas trocar a chave
não repara confidencialidade passada.
