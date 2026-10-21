# 02 — Modem, ONT, roteador, switch e AP

- **modem:** adapta sinal ao meio de acesso;
- **ONT/ONU:** termina uma rede óptica passiva;
- **roteador:** encaminha entre redes e aplica políticas;
- **switch:** conecta dispositivos na LAN e aprende MACs;
- **access point:** conecta clientes 802.11 à LAN;
- **firewall:** permite/nega fluxos segundo estado e política;
- **gateway residencial:** combina vários desses papéis.

Modo bridge desativa funções de roteamento/NAT do equipamento anterior para o
roteador próprio assumir. Access Point mode desativa roteamento do dispositivo
secundário para evitar double NAT e dois DHCPs. “Mesh” descreve coordenação e
backhaul entre APs, não garante desempenho.

## Escolha

Avalie suporte a atualizações, WPA3, redes de convidados, VLAN quando preciso,
logs, exportação de configuração, quantidade de portas, capacidade de rádio e
ciclo de vida. Marketing de velocidade agregada não é throughput de um cliente.
