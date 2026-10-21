# Consulta rápida

## Escolha de rota

1. prefixo mais longo;
2. preferência entre fontes;
3. métrica/best-path do protocolo;
4. resolução do next hop e instalação na FIB.

## OSPF

Link -> IP/MTU -> Hello/area/timers/auth -> estado do vizinho -> LSDB -> SPF ->
RIB/FIB -> retorno e política.

## BGP

TCP/peer -> capabilities -> UPDATE -> filtro in -> best path -> export policy ->
filtro out. Sempre use prefix allowlist e maximum-prefix.

## VPN

Underlay -> identidade/tempo -> IKE/handshake -> SA/peer -> seletores/AllowedIPs
-> rota -> NAT/firewall -> MTU/MSS -> retorno -> aplicação.
