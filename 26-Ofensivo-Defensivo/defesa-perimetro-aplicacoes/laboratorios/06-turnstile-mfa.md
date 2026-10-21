# Laboratório 06 — Turnstile e MFA

## Parte A — desafio

Modele respostas server-side para sucesso, expirado, repetido, hostname errado,
action errada e indisponibilidade. Nenhum token real é usado. Para cada caso,
defina decisão, log minimizado e experiência acessível.

## Parte B — identidade

Desenhe estados de uma conta administrativa: sem fator, enrollment, dois
autenticadores, perda de um, recovery, revogação e break-glass. Prefira
WebAuthn/passkey; documente por que TOTP digitado não é phishing-resistant.

## Red

Teste transições lógicas somente em contas de laboratório ou tabela de estados.

## Blue

Associe eventos e alertas a cadastro/remoção, recovery e mudança administrativa.

## Purple

Garanta que indisponibilidade do CAPTCHA não vire bypass silencioso de operação
sensível e que recuperação não seja mais fraca que o login.
