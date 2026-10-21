# 20 — Continuidade, clustering e recuperação empresarial

Alta disponibilidade reduz algumas interrupções; disaster recovery restabelece
serviço após desastre; backup recupera estado/dados. Nenhum substitui os outros.

## Conceitos Windows

- Failover Clustering coordena nodes/resources/quorum;
- Cluster-Aware Updating organiza servicing;
- Storage Replica replica volumes em cenários suportados;
- Hyper-V Replica replica VMs;
- backup application-aware preserva estado recuperável;
- forest recovery cobre catástrofe de identidade.

Todas essas operações dependem de redes, storage, identidade e tempo. Aqui são
modeladas; instalação/configuração real só depois dos pré-requisitos.

## Quorum

Quorum decide se o cluster pode continuar com o conjunto de votos disponível;
não é simplesmente "maioria de servidores" em todo desenho. Witness e
topologia mudam a decisão.

## Tabletop

Para cada falha (host, disco, site, identidade, update, erro humano) indique
detecção, failover, dados perdidos, RTO, autoridade, comunicação, failback e
prova. Inclua cenário onde automação propaga corrupção.

