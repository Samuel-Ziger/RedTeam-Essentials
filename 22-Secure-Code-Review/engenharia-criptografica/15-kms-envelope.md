# 15 — KMS e envelope em escala

KMS centraliza KEKs e operações auditadas. A aplicação gera DEK, cifra dados
localmente, pede encapsulamento e guarda a DEK cifrada. Cache de DEK melhora
latência, mas amplia duração em memória e precisa de limite e invalidação.

AAD/contexto de criptografia impede mover ciphertext entre recursos quando o
provedor o autentica. IAM restringe decrypt por serviço, ambiente e contexto.
Métricas cobrem volume, erro, latência, key ID antigo e chamadas anômalas.

## Prática

Projete falha do KMS: o que continua, por quanto tempo e sem cair para plaintext?
