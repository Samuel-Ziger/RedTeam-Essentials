# 05 — Endereçamento e rotas

Escolha prefixos que não colidam com redes domésticas, corporativas, VPCs,
containers ou Kubernetes. Colisão faz o sistema enviar pacotes à interface
errada. Registre tudo em IPAM, mesmo em laboratório.

Exemplo didático:

```text
VPN IPv4: 10.66.0.0/24
servidor: 10.66.0.1/24
alice:    10.66.0.2/32
bob:      10.66.0.3/32
```

No servidor, `AllowedIPs = 10.66.0.2/32` associa o endereço a Alice. No cliente
full-tunnel, `AllowedIPs = 0.0.0.0/0, ::/0` diz que o servidor recebe a rota
padrão. No split-tunnel, use apenas prefixos necessários, como `10.20.0.0/16`.

## Rota de retorno

O destino precisa saber voltar ao prefixo VPN. Há duas estratégias:

- rota explícita na rede de destino, preservando IP do cliente;
- NAT no gateway, simplificando retorno e perdendo origem interna no destino.

## Sobreposição

Verifique com `ip route get <destino>` antes e depois. Redes `10.0.0.0/8` são
amplas demais para `AllowedIPs` se você precisa de apenas um serviço.

## Prática

Use o planejador para rejeitar peers duplicados e uma rede sobreposta listada em
`reserved_networks`.

