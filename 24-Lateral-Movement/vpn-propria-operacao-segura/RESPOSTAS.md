# Respostas orientativas

## Plano

Cada peer recebe `/32` IPv4 e, se usado, `/128` IPv6 exclusivos. O servidor usa
o primeiro endereço do prefixo por convenção. Prefixos não podem sobrepor LAN,
VPC, Kubernetes ou redes de clientes.

## `AllowedIPs`

No servidor, um peer de acesso remoto normalmente anuncia apenas seu endereço
de túnel. No cliente full-tunnel, o peer servidor pode usar `0.0.0.0/0` e
`::/0`. Trocar essas posições cria rotas erradas ou permite origem indevida.

## Firewall

Liberar UDP do WireGuard não basta para acesso à internet: forwarding e política
de saída precisam permitir o fluxo; NAT é necessário quando a rede externa não
tem rota de retorno ao prefixo do túnel.

## Privacidade

Uma VPS própria mantém controle do software e da configuração, mas não elimina
metadados do provedor, do ISP ou do destino. A aplicação ainda pode identificar
o usuário por conta e dispositivo.

## Recuperação

Console do provedor, backup da configuração sem chaves em texto público, regra
com tempo de expiração e teste em sessão separada reduzem risco de lockout.

