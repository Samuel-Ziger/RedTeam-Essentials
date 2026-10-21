# Lab 05 — Auditoria offline de perfis

## Procedimento

1. Valide o plist da fixture com `plutil` no Mac e `ProfileAudit.py` em qualquer SO.
2. Liste payload root, internos, identifiers, UUIDs e escopo declarado.
3. Duplique um UUID em cópia temporária e confirme rejeição.
4. Remova `PayloadIdentifier` de um payload e confirme erro.
5. Adicione uma chave desconhecida e marque-a como revisão, não execução.

## Limite

Não instale o perfil. A fixture não contém rede, certificado, segredo, PPPC ou
identificador real. Entregue findings e correção da cópia temporária.
