# 11 — OAEP, PSS e parâmetros

RSA-OAEP é o esquema moderno para criptografia RSA; RSA-PSS é recomendado para
assinaturas novas. Ambos combinam hashes, máscaras e aleatoriedade com papéis
distintos. Parâmetros fazem parte do contrato e devem ser verificados, não
aceitos de entrada não confiável.

PKCS#1 v1.5 existe por compatibilidade e requer avaliação específica. Não use a
mesma chave para cifrar e assinar, não faça fallback silencioso e não exponha
diferenças entre falhas de decodificação.

## Prática

Especifique algoritmo, hash, MGF, tamanho de salt e formato de chave para um
perfil RSA-PSS interoperável.
