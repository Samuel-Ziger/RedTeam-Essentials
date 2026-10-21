# 04 — WireGuard e cryptokey routing

WireGuard expõe uma interface de rede e associa cada peer a uma chave pública e
uma lista de `AllowedIPs`. Essa lista tem dois papéis:

- na saída, escolhe qual peer recebe pacotes destinados aos prefixos;
- na entrada, valida se o endereço interno de origem é permitido para aquele
  peer.

Isso é **cryptokey routing**. Ainda é necessário firewall para controlar portas,
direções, redes e política de aplicação.

## Estado mínimo

Servidor: chave privada, endereço da interface, porta de escuta e peers. Cliente:
chave privada, endereço do túnel, chave pública/endpoint do servidor e rotas.
Chaves efêmeras de sessão são negociadas pelo protocolo; o administrador lida
com chaves estáticas dos peers.

## Silêncio e keepalive

WireGuard transmite quando há dados. Cliente atrás de NAT que precisa receber
após períodos ociosos pode usar `PersistentKeepalive = 25`; não o habilite sem
necessidade, pois aumenta tráfego e não é monitor de disponibilidade.

## Ausências intencionais

WireGuard não distribui endereços, usuários ou DNS por conta própria. Inventário,
provisionamento, revogação e política ficam com a operação. Simplicidade do
protocolo não elimina trabalho de serviço.

## Prática

Para dois clientes, desenhe chave pública e `/32` de cada peer. Explique o que
acontece se ambos anunciarem o mesmo endereço no servidor.

