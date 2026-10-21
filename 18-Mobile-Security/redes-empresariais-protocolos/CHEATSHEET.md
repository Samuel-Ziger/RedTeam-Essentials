# Consulta rápida

## Arquitetura

Requisitos -> fluxos -> zonas/VRFs -> endereçamento/DDI -> caminhos -> política
-> identidade -> observabilidade -> capacidade N-1 -> operação/rollback.

## Protocolo

Objetivo -> atores -> transporte -> framing -> tipos/campos -> estado -> erros ->
timeouts/limites -> versão/extensão -> threat model -> registros -> vetores.

## Produção

- deny por padrão e fluxos com owner/validade;
- NTP, certificados e secrets com expiração monitorada;
- diff/review/test/canary/confirmed commit/post-check;
- métricas, logs, traces/flows e mudanças correlacionáveis;
- RTO/RPO testados, não apenas documentados.
