# 09 — Firewall, NAT, UPnP e exposição

Firewall stateful permite respostas a conexões iniciadas internamente e bloqueia
entrada não solicitada por padrão. NAT/PAT traduz, mas não expressa sozinho uma
política completa. No IPv6, aplique política equivalente mesmo sem NAT.

Port forwarding publica um serviço interno. Antes de usar, questione se acesso
remoto por VPN, relay do fornecedor ou serviço gerenciado atende com menor
exposição. Se publicar, limite origem quando possível, use autenticação forte,
TLS, atualização, logs e inventário.

UPnP/NAT-PMP/PCP permitem mapeamentos dinâmicos. São convenientes, mas qualquer
aplicativo autorizado na LAN pode solicitar exposição. Desative se desnecessário
ou monitore os mapeamentos. DMZ host residencial frequentemente encaminha quase
toda entrada para um equipamento; não é uma DMZ empresarial e amplia risco.

## Exercício

Audite a fixture: liste mapeamentos, UPnP, administração remota e regras IPv6.
Para cada exposição, defina dono, finalidade, prazo e alternativa.
