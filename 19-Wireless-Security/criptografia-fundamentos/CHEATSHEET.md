# Cheatsheet — fundamentos

| Necessidade | Escolha inicial | Evite |
|---|---|---|
| bytes aleatórios | `secrets.token_bytes(n)` | `random`, timestamp |
| digest geral | SHA-256/SHA-512 ou SHA-3 | MD5/SHA-1 para colisão |
| autenticar mensagem | HMAC-SHA-256 | `hash(key + msg)` |
| derivar segredo forte | HKDF com `info` | cortar hashes sem domínio |
| armazenar senha | Argon2id/scrypt/PBKDF2 com salt | hash rápido, senha cifrada |
| comparar tag | `hmac.compare_digest` | igualdade byte a byte manual |

## Perguntas obrigatórias

1. Qual propriedade precisa ser garantida?
2. Qual é o escopo de unicidade do nonce?
3. Onde a chave nasce, vive, gira e é destruída?
4. Quais bytes exatos entram na operação?
5. Como a falha é testada e observada sem vazar segredo?
