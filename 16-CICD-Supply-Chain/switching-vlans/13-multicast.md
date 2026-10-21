# 13 — Multicast e IGMP snooping

Multicast entrega um fluxo a muitos receptores interessados. Em IPv4, IGMP
gerencia associação de hosts; em IPv6, MLD. Switch com snooping observa essas
mensagens e encaminha multicast apenas a portas interessadas, em vez de inundar
toda a VLAN.

Um querier mantém estado quando não há roteador multicast. Sem ele, entradas
podem expirar e o comportamento degradar. Multicast entre sub-redes exige
roteamento multicast (por exemplo PIM), fora do simples snooping L2.

Unknown multicast, flooding, fast leave e grupos estáticos variam. Voz, IPTV,
descoberta e aplicações financeiras têm requisitos diferentes. mDNS usa
multicast local e não é encaminhado entre VLANs sem gateway/refletor consciente.

## Exercício

Modele um transmissor, cinco receptores e duas portas sem interesse. Compare
replicação com e sem snooping e descreva o papel do querier.
