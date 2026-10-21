# 11 — Cliente Linux

Exemplo full-tunnel em `/etc/wireguard/wg0.conf`:

```ini
[Interface]
Address = 10.66.0.2/32
PrivateKey = <CHAVE_PRIVADA_DESTE_CLIENTE>
DNS = 10.66.0.1

[Peer]
PublicKey = <CHAVE_PUBLICA_DO_SERVIDOR>
Endpoint = vpn.example.test:51820
AllowedIPs = 0.0.0.0/0, ::/0
PersistentKeepalive = 25
```

Use `PersistentKeepalive` apenas se o cliente atrás de NAT precisar manter o
mapeamento. Se não há IPv6 no servidor, não anuncie `::/0` sem uma política
explícita; trate IPv6 no capítulo 14.

## Teste progressivo

Comece com `AllowedIPs = 10.66.0.0/24`, valide ping/serviço do túnel e somente
depois altere rota padrão. Isso separa handshake de encaminhamento/NAT.

```bash
sudo wg-quick up wg0
sudo wg show
ip route get 10.66.0.1
```

Faça teste de nova sessão administrativa antes de habilitar no boot.

## NetworkManager

Ambientes desktop podem importar configuração WireGuard. Escolha um único
gerenciador da interface; `wg-quick` e NetworkManager disputando o mesmo nome
causam resultados confusos.

## Prática

Use chaves descartáveis em duas VMs. Teste primeiro prefixo do túnel, depois
DNS e somente por último rota padrão.

