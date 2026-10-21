# 17 — MTU e troubleshooting

Encapsulamento adiciona overhead. Se o caminho não aceita o tamanho resultante,
algumas páginas ou transferências travam apesar de handshake funcionar.

## Sintomas

- ping pequeno funciona, tráfego grande falha;
- handshake existe, mas HTTPS fica pendente;
- funciona em uma rede e falha em outra;
- IPv6 apresenta black hole quando ICMPv6 necessário foi filtrado.

## Método por camadas

1. confirme relógio, endpoint, porta e chave pública;
2. verifique `latest handshake` e contadores;
3. teste o IP do túnel;
4. inspecione rotas e `AllowedIPs`;
5. verifique forwarding e contadores nftables;
6. separe DNS de conectividade por IP;
7. compare IPv4 e IPv6;
8. teste tamanho progressivo em destinos próprios;
9. ajuste MTU apenas com evidência.

`tcpdump` pode expor endereços e metadados. Capture na própria VM, com filtro,
tempo curto, autorização e descarte planejado. O curso não exige captura.

## MTU

`wg-quick` costuma inferir valor adequado. Fixar `MTU = 1280` sem diagnóstico
pode mascarar problema e reduzir eficiência. Registre caminho e justificativa.

## Prática

A partir de uma falha fictícia “handshake sim, DNS não”, construa árvore de
decisão que não começa reinstalando tudo.

