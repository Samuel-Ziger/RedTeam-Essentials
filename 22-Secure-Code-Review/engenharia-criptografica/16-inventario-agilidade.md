# 16 — Inventário e agilidade criptográfica

Inventário registra sistema, dado, algoritmo, parâmetros, protocolo, biblioteca,
certificado/chave, localização, proprietário, dependentes, validade e requisito.
Descoberta combina código, configuração, SBOM, certificados, tráfego autorizado
e entrevista; nenhum método sozinho é completo.

Agilidade permite substituir algoritmo, chave, biblioteca ou protocolo com
segurança e continuidade. Use policy central, formatos versionados, telemetria,
dual-read/single-write e teste de rollback. Evite abstração genérica que permite
combinações inseguras.

## Prática

Execute `crypto_inventory.py` na fixture e priorize itens por exposição,
longevidade e suporte.
