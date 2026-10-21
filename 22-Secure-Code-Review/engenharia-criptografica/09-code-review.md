# 09 — Code review criptográfico

Localize fontes de chave/nonce, chamadas de primitivas, serialização, storage,
logs, erros e policy. Trace um dado desde entrada não confiável até decisão de
autorização ou plaintext. Procure defaults, fallback, truncamento e conversões.

Pergunte: chave separada por propósito? nonce único? AEAD? AAD completa? parser
estrito? comparação constante? tamanho limitado? falha fechada? rotação real?
teste negativo? dependência suportada? Aponte evidência e impacto, não apenas
uma lista de algoritmos.

## Prática

Revise `secure_record.py` e associe cada validação a uma ameaça.
