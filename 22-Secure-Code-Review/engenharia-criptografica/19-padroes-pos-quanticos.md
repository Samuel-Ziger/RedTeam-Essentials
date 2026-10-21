# 19 — ML-KEM, ML-DSA e SLH-DSA

NIST FIPS 203 padroniza ML-KEM para estabelecimento de chave; FIPS 204 padroniza
ML-DSA; FIPS 205 padroniza SLH-DSA, assinatura baseada em hash. SP 800-227
explica uso de KEMs. KEM estabelece segredo; não autentica o peer sozinho.

Em outubro de 2026, FIPS 203/204/205 são finais. FN-DSA/FIPS 206 e HQC continuam
em padronização, não devem ser descritos como padrões finais. Migração considera
tamanhos, desempenho, side channels, parsing, certificados/protocolos e suporte
de fornecedor. Modos híbridos exigem construção padronizada, não concatenação
inventada.

## Prática

Compare ML-KEM, ML-DSA e SLH-DSA por função, artefatos e integração; não por um
ranking genérico de “mais forte”.
