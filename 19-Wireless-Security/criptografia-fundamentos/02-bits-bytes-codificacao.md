# 02 — Bits, bytes, texto e codificação

Criptografia opera em bytes. Texto exige codificação, normalmente UTF-8;
hexadecimal e Base64 apenas representam bytes como caracteres. Eles são
reversíveis sem chave e portanto não são criptografia. Defina ordem de bytes,
comprimentos e normalização antes de assinar ou autenticar estruturas.

`b"A"`, o texto `A`, o hexadecimal `41` e o Base64 `QQ==` podem representar o
mesmo octeto, mas pertencem a camadas diferentes. Ambiguidade entre campos
permite que duas estruturas produzam a mesma concatenação. Prefira um formato
canônico com comprimentos explícitos.

## Prática

Converta `Cripto ✓` entre UTF-8, hex e Base64 e confirme a ida e volta. Depois
explique por que Base64 não fornece confidencialidade.
