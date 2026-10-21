# 07 — AES-GCM

GCM combina CTR com autenticação GHASH. É rápido e amplamente interoperável,
mas reutilizar nonce com a mesma chave compromete confidencialidade e pode
permitir falsificação. Use nonces de 96 bits gerados conforme a estratégia da
biblioteca e imponha limite de mensagens por chave.

Tag truncada reduz margem e deve seguir um perfil explícito. AAD e ordem dos
bytes precisam ser idênticos na leitura. Nunca trate `InvalidTag` como dado
corrompido recuperável: a saída não é confiável.

## Prática

Execute o envelope do curso e altere separadamente nonce, AAD, ciphertext e tag.
