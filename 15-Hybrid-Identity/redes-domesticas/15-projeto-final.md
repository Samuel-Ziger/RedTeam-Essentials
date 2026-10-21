# 15 — Projeto final: casa e pequeno escritório

Projete rede para oito moradores/colaboradores, trabalho remoto, dois APs, NAS,
impressora, câmeras e 20 dispositivos IoT. A operadora entrega IPv4 em CGNAT e
IPv6 `/56`.

## Entregáveis

1. requisitos de cobertura, capacidade, disponibilidade e privacidade;
2. diagrama físico/lógico e inventário;
3. redes principal, convidados e IoT com matriz de fluxos;
4. plano DHCP, reservas, DNS e IPv6;
5. plano de canais/APs e medição antes/depois;
6. WPA2/WPA3, WPS, administração e atualização;
7. decisão de acesso remoto compatível com CGNAT;
8. runbooks de “sem Internet”, Wi-Fi lento e falha de AP;
9. backup, restauração, UPS e continuidade;
10. custos, riscos residuais e roadmap.

Modele a configuração em `fixtures/home-network.json`, rode o auditor e trate
todos os achados. Não exponha nomes, MACs ou credenciais reais.
