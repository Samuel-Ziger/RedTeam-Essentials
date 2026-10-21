# 14 — Redes virtuais e bridges

Hypervisors, containers e nuvens implementam switches/bridges virtuais. Uma
vNIC liga a VM ao vSwitch; port groups ou redes virtuais associam VLAN/política.
Trunks podem chegar a hypervisors, appliances e servidores, mas ampliam o
impacto de configuração incorreta.

Bridge conecta camada 2; roteamento conecta sub-redes; NAT traduz; overlay
encapsula uma rede virtual sobre underlay IP. O host pode filtrar tráfego sem que
o switch físico o veja, então observabilidade precisa cobrir ambos.

Containers em um host podem usar bridge, veth, namespace e NAT. Orquestradores
adicionam CNI, service routing e network policies. Não presuma que “VLAN 30” no
switch tem o mesmo significado de uma label no cluster.

## Exercício

Desenhe duas VMs em VLANs diferentes no mesmo host e uma em outro host. Marque
onde quadros entram no switch físico, onde o roteamento ocorre e quais fluxos
podem nunca sair do hypervisor.
