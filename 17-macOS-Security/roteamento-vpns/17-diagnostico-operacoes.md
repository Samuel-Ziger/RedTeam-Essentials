# 17 — Diagnóstico e operações

## Sequência

1. escopo, horário, origem, destino, protocolo e mudanças;
2. interface, erros, MTU e vizinhança;
3. RIB/FIB e longest-prefix em cada direção;
4. adjacência/LSDB ou sessão/política;
5. VRF, PBR, NAT, ACL/firewall e estado;
6. VPN SA, seletores, contadores e rekey;
7. DNS/transporte/aplicação;
8. correlação com telemetria e mudanças.

Uma captura em um ponto mostra apenas aquele ponto. Capture dos dois lados de
uma tradução/túnel quando autorizado e minimize payload. Contadores antes/depois
de um teste controlado ajudam a localizar descarte.

## Indicadores

Vizinhos, rotas/prefixos, churn, CPU/memória, drops por política, utilização,
latência/perda, SAs, expiração de certificados e sucesso de autenticação.
Alertas devem apontar impacto e runbook, não apenas estado técnico.
