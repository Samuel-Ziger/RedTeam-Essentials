# 03 — Domínios de colisão e broadcast

Em Ethernet moderna com switch/full-duplex, cada porta elimina contenção do
antigo meio compartilhado. Um hub mantém um domínio de colisão; um switch cria
um por porta, embora colisão deixe de ser a preocupação normal em full-duplex.

Uma VLAN é um domínio de broadcast. Roteadores ou interfaces L3 separam esses
domínios. Broadcast excessivo consome airtime/CPU e amplia impacto de erros,
mas dividir VLANs demais aumenta roteamento, política e operação.

Falha de duplex pode causar perda/desempenho ruim; loops L2 podem replicar
broadcast indefinidamente porque Ethernet não possui TTL por quadro. STP existe
para manter uma topologia lógica sem loops.

## Exercício

Em dois switches ligados por duas conexões paralelas sem LACP/STP, descreva por
que um broadcast volta, é replicado e impede estabilidade da tabela MAC.
