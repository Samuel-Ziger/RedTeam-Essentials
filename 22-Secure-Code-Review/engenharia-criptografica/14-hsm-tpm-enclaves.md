# 14 — HSM, TPM, enclaves e limites

HSM executa operações e protege chaves sob políticas; TPM ancora dispositivo e
medição; secure enclaves isolam execução em modelos próprios. Nenhum deles
torna aplicação autorizada incapaz de abusar da chave.

Avalie attestation, backup, quorum, disponibilidade, latência, exportabilidade,
firmware, certificação e lock-in. Handle, policy e credencial de acesso viram
ativos críticos. Planeje falha e recuperação antes de tornar chave não exportável.

## Prática

Compare software key store, HSM e KMS para CA, assinatura de release e DEK.
