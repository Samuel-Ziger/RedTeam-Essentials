# 05 — Padding, oráculos e mensagens de erro

Padding completa o último bloco, mas não autentica. Um serviço que revela se o
padding, MAC, JSON ou usuário falhou fornece sinais diferentes a entradas
controladas. Tempo, status, corpo e logs também podem formar um oráculo.

A defesa é usar AEAD; em legado, autenticar ciphertext e metadados antes de
decifrar, comparar MAC em tempo constante e unificar a resposta externa. O log
interno pode ter diagnóstico correlacionado e sanitizado, sem incluir plaintext,
chave, tag ou conteúdo controlado sem limites.

## Prática

Projete testes que confirmem a mesma classe de erro para tag, nonce e ciphertext
alterados, sem implementar exploração de oráculo.
