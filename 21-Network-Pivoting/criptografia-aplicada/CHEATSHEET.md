# Cheatsheet — criptografia aplicada

## Certificado

- validar cadeia, tempo, SAN/nome, KU/EKU, constraints e política;
- inventariar emissor, serial, fingerprint, algoritmo e dias restantes;
- chave privada nunca faz parte do certificado nem do log;
- não desabilitar verificação para contornar CA ou nome errado.

## Operação

- TLS 1.3 como preferência; TLS 1.2 apenas por perfil compatível;
- certificados curtos e renovação automática observável;
- segredo curto entregue por identidade de workload;
- criptografia de disco mais backup cifrado e restauração testada;
- token: algoritmo fixo, issuer/audience/tempo/tipo validados.
