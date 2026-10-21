# 03 — Underlay, overlay e domínios de falha

Underlay fornece reachability IP entre endpoints de túnel; overlay cria redes
lógicas, segmentação e política. VXLAN, por exemplo, encapsula quadros sobre UDP
e usa VNI para identificar segmentos; EVPN pode distribuir reachability por BGP.

Overlay não corrige underlay instável. Monitore os dois: adjacências, rotas, MTU,
latência e perda abaixo; peers, endpoints, VNIs e policies acima. Encapsulamento
exige MTU maior ou payload menor.

Domínio de falha é o conjunto afetado por componente/mudança. Reduza blast radius
com cells/pods, limites L3, controladores redundantes e rollout gradual. Evite
stretch L2 entre datacenters sem requisito e entendimento de failure modes.

## Exercício

Mapeie falha de leaf, spine, VTEP, route reflector e controller. Para cada uma,
indique plano afetado, alcance, detecção e capacidade residual.
