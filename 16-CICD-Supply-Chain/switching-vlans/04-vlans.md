# 04 — VLANs e segmentação

VLAN separa logicamente uma infraestrutura de camada 2. Hosts em VLANs distintas
precisam de roteamento para conversar, permitindo política no ponto L3. IDs
802.1Q utilizáveis normalmente vão de 1 a 4094, com valores reservados; detalhes
e faixas suportadas variam.

Segmente por requisitos e confiança, não apenas organograma: usuários, voz,
impressoras, IoT, servidores, convidados, gestão e quarentena podem precisar de
políticas diferentes. Uma VLAN não cifra dados e não impede ataques entre hosts
da mesma VLAN.

Cada VLAN deve ter nome, ID, finalidade, dono, prefixo, gateway, DHCP, política,
sites, criticidade e ciclo de vida. Evite VLAN 1/nativa para gestão e usuários
por conveniência; documente qualquer exceção.

## Exercício

Proponha VLANs para uma escola com administrativo, alunos, professores, voz,
câmeras, convidados e gestão. Depois reduza o desenho ao menor número que ainda
atenda políticas distintas.
