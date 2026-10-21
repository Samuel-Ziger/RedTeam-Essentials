# 07 — Loops e Spanning Tree

STP troca BPDUs para eleger root bridge e manter apenas caminhos necessários,
bloqueando redundância que formaria loop. A eleição usa Bridge ID (prioridade e
MAC); cada switch calcula menor custo até a raiz e escolhe papéis de porta.

A raiz deve ser intencional e estar em camada adequada, não ser o switch com
menor MAC por acidente. Documente root primária/secundária por instância/VLAN.
STP clássico converge mais lentamente; RSTP melhora estados e handshakes.

Porta de endpoint pode entrar rapidamente em forwarding (edge/PortFast), mas
deve perder essa condição ou ser bloqueada ao receber BPDUs conforme proteção.
Nunca habilite edge em enlace entre switches sem entender a topologia.

## Diagnóstico

Confirme root, custo, papéis, portas bloqueadas, mudanças de topologia e origem de
BPDUs. MAC flapping e CPU alta podem ser sintomas, não causa.
