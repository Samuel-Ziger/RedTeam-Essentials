# 09 — ECMP, FHRP e alta disponibilidade

ECMP instala múltiplos next hops de custo igual e distribui fluxos por hash.
Per-packet pode reordenar; per-flow preserva melhor ordem, mas fluxos grandes
podem desequilibrar. Consistent/resilient hashing reduz remapeamento em falha.

FHRP oferece gateway virtual compartilhado por roteadores, com ativo/standby ou
balanceamento conforme protocolo. Prioridade, preemption, tracking e timers
definem failover. Tracking precisa observar o serviço/caminho relevante, não
apenas interface local.

Alta disponibilidade exige estado simétrico: retorno pode atravessar outro
firewall/NAT e falhar se sessão não for sincronizada. ECMP com dispositivos
stateful precisa de desenho de simetria ou cluster adequado.

## Teste

Meça falha de membro, nó, link upstream e caminho de retorno. Registre perda,
tempo de convergência, capacidade residual e comportamento de sessões existentes.
