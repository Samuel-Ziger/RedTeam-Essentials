# 14 — Automação, APIs e infraestrutura como código

Automatize intenção validada, não comandos copiados. Pipeline seguro:

1. schema e source of truth;
2. validação sintática/semântica;
3. renderização determinística;
4. diff e revisão;
5. testes offline/lab;
6. canário e pre-check;
7. commit confirmado/rollback;
8. post-check e reconciliação.

APIs modernas podem usar REST/JSON, NETCONF/YANG, RESTCONF, gNMI ou SDK de
fabricante. Prefira modelos estruturados a parsing de CLI, mas trate versões,
timeouts, paginação, idempotência e erros parciais.

Segredos ficam em secret manager e credenciais de curta duração. Logs removem
tokens/configurações sensíveis. Runner tem menor privilégio e alcance. Fixe
dependências, revise módulos e gere trilha de auditoria.

Drift deve ser detectado e classificado; auto-remediação cega pode ampliar um
incidente.
