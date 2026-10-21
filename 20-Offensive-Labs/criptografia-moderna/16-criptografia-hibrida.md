# 16 — Criptografia híbrida e envelope

Dados grandes são cifrados por uma DEK simétrica aleatória. A DEK é encapsulada
para um destinatário por RSA-OAEP, KEM ou KMS; o registro guarda ciphertext,
nonce, chave encapsulada, versão e identificadores. Isso é criptografia híbrida.

AAD vincula metadados, e rotação de KEK pode reencapsular DEKs sem decifrar todo
o conteúdo. O envelope precisa limitar tamanhos, rejeitar algoritmos desconhecidos
e impedir substituição cruzada entre tenant, objeto e ambiente.

## Verificação

Quais campos mudam ao rotacionar apenas a KEK? Quais mudam ao rotacionar a DEK?
