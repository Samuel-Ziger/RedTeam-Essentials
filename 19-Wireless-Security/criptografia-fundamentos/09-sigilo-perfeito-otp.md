# 09 — Sigilo perfeito e one-time pad

No one-time pad, a chave é uniforme, tão longa quanto a mensagem, mantida em
segredo e usada uma única vez. Sob essas condições, o ciphertext não informa
qual plaintext foi usado. Reutilizar a chave cancela o segredo ao combinar
ciphertexts; distribuição e armazenamento tornam o método impraticável em
muitos sistemas.

OTP fornece confidencialidade, não integridade. Um bit alterado no ciphertext
altera o plaintext correspondente sem ser detectado. O exercício mostra por
que uma propriedade isolada não compõe automaticamente um canal seguro.

## Verificação

Liste as quatro condições do OTP e identifique qual delas um “pad” derivado de
senha viola.
