# Respostas orientativas

- Certificado parseável ou assinado não é automaticamente confiável para um nome.
- SAN identifica serviço; CN não deve ser a única decisão moderna de hostname.
- TLS 1.3 suite não escolhe sozinha grupo de acordo e assinatura.
- 0-RTT pode ser repetido e exige operação apropriada.
- mTLS autentica uma chave/workload; autorização continua separada.
- Full-disk encryption protege mídia em repouso, não processo já desbloqueado.
- JWS não cifra e Base64url não fornece sigilo.
- Rotação termina apenas quando uso da versão anterior chega a zero e ela é revogada.
