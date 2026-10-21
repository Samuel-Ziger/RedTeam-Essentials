# 16 — Criptoanálise e canais laterais

Modelos clássicos incluem ciphertext conhecido, plaintext conhecido, entrada
escolhida e ciphertext escolhido. Segurança precisa resistir ao modelo do
protocolo; esconder exemplos ou negar erros não substitui essa análise.

Canais laterais exploram implementação: tempo, cache, energia, falhas, tamanho,
mensagens e padrões de acesso. Use operações constantes oferecidas pela
biblioteca, reduza metadados, autentique antes de distinguir erros e imponha
limites. Python não é ambiente para prometer tempo constante além das
primitivas nativas documentadas.

## Verificação

Dê um exemplo de algoritmo matematicamente correto que ainda vaza pela forma de
comparar tags.
