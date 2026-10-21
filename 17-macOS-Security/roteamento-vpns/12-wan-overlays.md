# 12 — WAN, overlays e SD-WAN

WAN conecta sites sobre Internet, transporte privado, ondas/licenças ou serviços
de operadora. Requisitos incluem disponibilidade, latência, jitter, perda,
capacidade, simetria, MTU, QoS, endereçamento, segurança e suporte.

Overlay cria topologia lógica/túneis sobre underlay IP. O overlay só é tão
saudável quanto reachability, MTU e estabilidade do underlay. Encapsulamento
reduz MTU efetiva; ajuste MSS/PMTU conscientemente.

SD-WAN centraliza política e seleciona caminho por medições/aplicação. Controller
não elimina roteamento, PKI ou operação; adiciona dependências de identidade,
orquestração e software. Analise comportamento sem controlador e durante split
brain.

## Contrato

Defina SLO por classe, método de medição, local de demarcação, capacidade de
falha e escalonamento. “Dois links” não é redundância se compartilham rota física.
