# 13 — Segurança, zero trust e microsegmentação

Zero trust remove confiança implícita por localização: cada acesso avalia
identidade, dispositivo, recurso, contexto e política. Não é produto nem exige
eliminar toda VPN de imediato.

Macrosegmentação usa VRF/VLAN/zona; microsegmentação aplica política entre
workloads/identidades. Comece por inventário e fluxos observados, proponha allowlist,
rode em monitor mode, corrija dependências e aplique por ondas.

Controles incluem 802.1X/NAC, firewalls, security groups, host firewall,
service mesh e proxies de acesso. Escolha o enforcement mais próximo do recurso
que preserve identidade e observabilidade sem criar ponto único de falha.

## Management plane

Separe, autentique fortemente, use protocolos cifrados, allowlist e logs. Plano
de controle precisa de CoPP/rate limit e peers autenticados. Plano de dados
aplica anti-spoofing, filtros e proteção DDoS proporcional.
