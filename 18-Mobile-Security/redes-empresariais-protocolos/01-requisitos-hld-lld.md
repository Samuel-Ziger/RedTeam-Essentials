# 01 — Requisitos, HLD, LLD e source of truth

Comece por serviços e risco, não equipamentos. Requisitos funcionais dizem quem
precisa falar com quem; não funcionais definem disponibilidade, latência, perda,
capacidade, segurança, conformidade, custo e tempo de recuperação.

**HLD** descreve arquitetura, zonas, sites, dependências, caminhos e decisões.
**LLD** detalha VLANs, prefixos, VRFs, interfaces, protocolos, timers,
políticas e telemetria. ADRs registram alternativas e por que uma decisão foi
tomada.

Source of truth representa o estado pretendido. Deve ter schema, revisão,
validação, owners e integração com IPAM/inventário. Configuração de equipamento
não é source of truth se cada caixa diverge sem controle.

## Critério de requisito

“Rede rápida” é ambíguo. “P95 RTT entre filial e API abaixo de 80 ms, perda
menor que 0,5% e disponibilidade mensal de 99,9%” pode ser medido.
