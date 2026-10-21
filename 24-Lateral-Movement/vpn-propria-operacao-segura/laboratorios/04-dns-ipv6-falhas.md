# Lab 04 — DNS, IPv6 e comportamento de falha

Construa uma matriz para túnel ativo, interface parada, reinício e troca de rede.
Registre o resultado esperado de IPv4, IPv6 e DNS.

Em ambiente local:

1. valide qual resolvedor é usado antes do túnel;
2. suba o túnel com DNS fictício/local controlado;
3. valide rota DNS e resolução da zona de lab;
4. teste IPv6 conforme a política escolhida;
5. derrube o túnel e observe fallback ou bloqueio;
6. compare o resultado com a política, não com slogans de “leak”.

## Aceite

Nenhum protocolo fica em estado “não pensado”. Se IPv6 não é oferecido, há
bloqueio explícito ou risco residual documentado.

