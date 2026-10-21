# 06 — Roteamento inter-VLAN

Hosts em VLANs distintas chegam a uma interface de camada 3: subinterfaces em
um roteador (router-on-a-stick), SVIs em switch L3 ou interfaces em firewall.
Essa interface é o gateway do segmento e ponto natural para política/telemetria.

Router-on-a-stick é didático e econômico, mas concentra tráfego em um trunk.
Switch L3 oferece encaminhamento local de alta capacidade; firewall oferece
controle stateful mais rico, possivelmente com menor throughput/custo. Escolha
pela política, escala, visibilidade e falha, não por hábito.

Para cada fluxo, garanta rota de ida e volta, gateway correto, ACL/firewall,
DNS e serviço. “VLANs não se enxergam” pode ser comportamento intencional.

## Exercício

Modele usuários -> impressoras (permitir impressão), convidados -> qualquer LAN
(negar), administração -> gestão (permitir MFA) e IoT -> DNS/NTP (permitir).
