# 12 — Diagnóstico por sintomas

Comece pelo escopo: um dispositivo, uma banda, um AP, um serviço ou todos?
Determine quando começou e o que mudou.

| Sintoma | Primeiras hipóteses |
|---|---|
| conecta ao Wi-Fi, sem IP | DHCP, isolamento, VLAN/backhaul |
| tem IP, sem nomes | DNS, portal, política |
| cabeado bom, Wi-Fi ruim | rádio, canal, cobertura, cliente |
| apenas um site falha | DNS específico, rota, MTU, serviço remoto |
| tudo lento sob upload | gargalo e bufferbloat |
| acesso remoto falha | CGNAT, firewall, mapeamento, DNS |

Evite reset de fábrica como primeiro passo: ele destrói evidência e pode perder
credenciais da operadora. Capture estado sanitizado, teste uma hipótese por vez
e reverta mudanças sem ganho.

## Runbook curto

energia/sinal -> enlace -> endereço -> gateway -> DNS -> porta -> aplicação.
Compare um dispositivo bom com um ruim para encontrar a menor diferença.
