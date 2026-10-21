# 14 — Senhas, salts e KDFs de memória

Armazene um verificador, não a senha nem criptografia reversível. Gere salt
aleatório por registro e use Argon2id, scrypt ou PBKDF2 conforme plataforma e
política. O custo precisa ser medido no hardware do serviço, registrado no
formato e atualizado após autenticação bem-sucedida.

Pepper é um segredo adicional guardado fora do banco e aumenta complexidade de
rotação; não substitui salt. Limite tentativas, ofereça MFA/passkeys e trate
recuperação como parte do sistema. Comparação deve ser constante e mensagens de
erro não devem enumerar contas.

## Prática

Use `password_kdf.py` com dados sintéticos; compare dois registros da mesma
senha e explique por que são diferentes e ainda verificáveis.
