# 15 — Autenticação e armazenamento de senhas

O módulo 19 tratou KDF; aqui ela integra um serviço. O registro versiona algoritmo
e custos, autenticação limita tentativas e evita enumeração, MFA reduz impacto e
recuperação possui controles equivalentes ao login.

Após sucesso, compare parâmetros com política e rederive de forma gradual.
Breaches exigem revogar sessões, avaliar pepper e notificar conforme plano; não
há como “descriptografar” um verificador bem projetado para recuperar senha.

## Prática

Teste senha correta, incorreta, registro malformado, custo fora do limite e
upgrade de parâmetros sem expor diferença externa.
