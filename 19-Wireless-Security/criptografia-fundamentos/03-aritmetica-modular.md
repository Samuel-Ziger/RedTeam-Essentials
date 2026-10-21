# 03 — Aritmética modular

Em módulo `n`, inteiros que deixam o mesmo resto são congruentes. Somar ou
multiplicar pode ser feito antes ou depois da redução: `(a+b) mod n` e
`((a mod n)+(b mod n)) mod n` coincidem. A exponenciação modular rápida evita
construir números gigantes e aparece em RSA e Diffie–Hellman.

Nem toda divisão existe. Dividir por `a` significa multiplicar pelo inverso de
`a`, que existe somente quando `mdc(a,n)=1`. Não trate exemplos pequenos como
parâmetros seguros: eles tornam a estrutura visível e também trivialmente
enumerável.

## Verificação

Calcule `7^128 mod 13` com `pow(7, 128, 13)` e explique por que a operação não
precisa materializar `7^128`.
