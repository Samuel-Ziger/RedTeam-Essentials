# 10 — IPv6 residencial

A operadora delega um prefixo ao roteador (Prefix Delegation); o roteador anuncia
`/64` nas LANs. Clientes formam endereços por SLAAC e podem receber opções por
RDNSS/DHCPv6. Link-local e Router Advertisement são fundamentais.

Não desative IPv6 para esconder um problema. Isso pode criar comportamento
inconsistente ou fallback lento. Diagnostique separadamente IPv4 e IPv6: prefixo
delegado, RA, endereço, DNS AAAA, rota default, firewall e PMTU.

Endereços temporários reduzem correlação do identificador de interface, mas o
prefixo ainda pode identificar a conexão. ULA é opcional para comunicação local;
não invente prefixos `fd` manualmente sem geração adequada.

## Segurança

Um endereço global não equivale a porta aberta. Confirme firewall de entrada em
todas as redes, inclusive convidados/IoT, e não replique regras IPv4 por
suposição. ICMPv6 necessário deve ser permitido de forma consciente.
