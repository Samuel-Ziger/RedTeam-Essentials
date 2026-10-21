# 02 — Arquiteturas de campus, filial, datacenter e nuvem

Campus favorece acesso/distribuição/core e limites L3. Filial busca simplicidade,
operação remota e continuidade de WAN. Datacenter usa leaf-spine para muitos
caminhos previsíveis leste-oeste. Nuvem oferece VPC/VNet, sub-redes, route tables,
gateways e controles distribuídos definidos por software.

Híbrido interliga esses ambientes, mas semântica difere: security group pode ser
stateful e ligado à interface; ACL de sub-rede pode ser stateless; load balancer
pode terminar TLS e esconder origem. Traduza requisito, não sintaxe.

## Decisões

- onde termina camada 2;
- onde ocorre roteamento e política;
- como identidade chega ao enforcement;
- como DNS, tempo e certificados sobrevivem a falhas;
- quais serviços continuam localmente sem WAN;
- como caminhos e custos são observados.

## Exercício

Compare aplicação de três camadas em datacenter e nuvem. Desenhe os mesmos
fluxos e destaque componentes gerenciados, responsabilidade e telemetria.
