# 10 — RSA e suas garantias

RSA usa aritmética modular sobre um módulo produto de primos grandes. A operação
matemática determinística não é um esquema seguro por si; criptografia e
assinatura exigem codificações padronizadas. Gere chaves com biblioteca madura,
expoente público adequado e tamanho conforme política vigente.

RSA é mais lento e produz chaves/ciphertexts grandes; costuma encapsular uma
chave simétrica, não cifrar arquivos inteiros. Proteção da chave privada,
blinding, validação e padding são responsabilidades da implementação.

## Verificação

Por que “aplicar a chave privada” não é uma descrição correta de uma assinatura
RSA moderna?
