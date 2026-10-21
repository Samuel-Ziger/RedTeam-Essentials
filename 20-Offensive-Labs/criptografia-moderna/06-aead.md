# 06 — AEAD e dados associados

Authenticated Encryption with Associated Data protege confidencialidade do
plaintext, integridade do ciphertext e autenticidade de AAD não cifrado. AAD é
ideal para versão, tenant, tipo e cabeçalho que precisam ser lidos antes, mas
não podem ser alterados.

AEAD não esconde tamanho, horário, frequência nem AAD. A aplicação deve limitar
entradas e vincular contexto correto. Decriptação só devolve plaintext depois
da verificação da tag; não faça streaming de dados não autenticados para sinks.

## Verificação

Escolha quais campos de um registro versionado ficam em AAD e quais exigem
confidencialidade. Justifique cada um.
