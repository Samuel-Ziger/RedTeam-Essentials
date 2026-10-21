# 07 — Instalação e verificação

Use os repositórios suportados da distribuição. Em Debian/Ubuntu atuais:

```bash
sudo apt update
sudo apt install wireguard nftables
```

Consulte a página oficial de instalação para outras plataformas. Evite scripts
obtidos aleatoriamente e instaladores que também mudam SSH, firewall, DNS e
usuários sem apresentar plano.

## Verificações

```bash
wg --version
systemctl status nftables --no-pager
ip link show type wireguard
```

A ausência de uma interface antes da configuração é normal. Confirme que o
módulo/implementação é compatível com o kernel e que as ferramentas vêm do
repositório esperado.

## Diretório

`/etc/wireguard` deve ser acessível apenas por root. Arquivos `wg0.conf` contêm
chave privada e normalmente usam modo `0600`:

```bash
sudo install -d -m 700 /etc/wireguard
sudo install -m 600 /dev/null /etc/wireguard/wg0.conf
```

Edite pelo método seguro da sua operação. Não cole chave em terminal gravado,
histórico, CI ou gerenciador de configuração sem secret store adequado.

## Prática

Instale em VM descartável, valide pacote e permissões e remova a VM ao final.

