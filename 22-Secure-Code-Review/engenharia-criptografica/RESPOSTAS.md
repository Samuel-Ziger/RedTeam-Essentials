# Respostas orientativas

- Prova formal cobre modelo e hipótese; operação incorreta continua fora dela.
- Autenticidade não fornece frescor: replay exige estado ou identificador.
- Canonicalização evita que os mesmos bytes/objetos ganhem interpretações diferentes.
- KMS protege KEK e controla decrypt; IAM ainda limita quem pode pedir a operação.
- Rotação só termina após dependências e dados antigos deixarem a versão anterior.
- Shor afeta RSA/DH/ECC; Grover muda margem simétrica, não “quebra toda cifra”.
- KEM estabelece segredo, mas autenticação do peer vem da composição.
- ML-KEM, ML-DSA e SLH-DSA têm papéis diferentes; HQC e FN-DSA ainda não são FIPS finais.
