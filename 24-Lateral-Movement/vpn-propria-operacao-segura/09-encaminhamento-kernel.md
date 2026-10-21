# 09 — Encaminhamento no kernel

Uma interface ativa não torna a VPS roteador automaticamente. Para encaminhar
IPv4, crie um arquivo dedicado:

```ini
# /etc/sysctl.d/90-wireguard-router.conf
net.ipv4.ip_forward = 1
```

Para IPv6 roteado:

```ini
net.ipv6.conf.all.forwarding = 1
```

Aplique e verifique:

```bash
sudo sysctl --system
sysctl net.ipv4.ip_forward
sysctl net.ipv6.conf.all.forwarding
```

Habilitar forwarding aumenta responsabilidade: o firewall deve definir quais
interfaces, origens e destinos podem atravessar o host. Não use `accept` global.

## rp_filter

Reverse path filtering pode interferir em roteamento assimétrico. Não o desative
globalmente como primeira tentativa. Entenda rotas, política e documentação do
sistema; faça ajuste por interface apenas com justificativa.

## Rota de retorno

Forwarding permite entrada e saída, mas a resposta ainda precisa retornar. Use
rota explícita na rede de destino ou NAT no gateway. Capture apenas em seu lab
para provar onde o pacote para.

## Prática

Em VM roteadora, alterne forwarding e observe contadores do firewall. Registre
o resultado sem usar destinos externos não necessários.

