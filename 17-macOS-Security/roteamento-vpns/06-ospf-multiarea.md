# 06 — OSPF multiárea e operações

Área 0 é backbone; ABRs conectam outras áreas ao backbone. Multiárea reduz
escopo de LSAs/cálculos, mas acrescenta desenho, sumarização e troubleshooting.
Uma rede pequena não fica melhor apenas por ter muitas áreas.

Stub, totally stubby (extensão de fornecedor) e NSSA limitam LSAs externos em
graus diferentes. Entenda necessidade de rotas externas/default antes de
escolher. Sumarize nos limites onde endereçamento foi planejado para isso.

OSPFv3 suporta IPv6 e evoluiu em relação a endereçamento/autenticação; confira a
versão/implementação. Não trate configuração OSPFv2 como simples copiar/colar.

## Operação

Monitore vizinhos, alterações LSDB, SPF frequente, rotas por área, autenticação,
uso de CPU e flaps. Baseline normal permite diferenciar crescimento legítimo de
instabilidade.
