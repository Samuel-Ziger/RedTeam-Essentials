# VPN própria em VPS — projeto, implantação e operação

Curso prático para construir uma VPN WireGuard em infraestrutura própria ou
formalmente administrada. A implantação é um serviço de rede real: faça backup,
mantenha console fora de banda e teste primeiro em VM descartável.

## Resultado de aprendizagem

Você aprenderá a:

- transformar requisito em arquitetura full-tunnel ou split-tunnel;
- escolher endereçamento, rotas, DNS e política IPv4/IPv6;
- gerar, armazenar, rotacionar e revogar chaves por dispositivo;
- instalar WireGuard e aplicar firewall mínimo com nftables;
- configurar Linux, Windows, macOS e dispositivos móveis;
- verificar cobertura, MTU, encaminhamento e comportamento de falha;
- monitorar disponibilidade com minimização de dados;
- recuperar uma configuração defeituosa sem perder acesso administrativo.

## Rota

| # | Capítulo |
|---:|---|
| 00 | [Escopo, segurança e preflight](00-escopo-preflight.md) |
| 01 | [Arquitetura e fronteiras de confiança](01-arquitetura-confianca.md) |
| 02 | [VPS, provedor e responsabilidade](02-vps-provedor.md) |
| 03 | [Base Linux e acesso administrativo](03-base-linux-acesso.md) |
| 04 | [WireGuard e cryptokey routing](04-wireguard-conceitos.md) |
| 05 | [Endereçamento e rotas](05-enderecamento-rotas.md) |
| 06 | [Chaves, peers e ciclo de vida](06-chaves-peers.md) |
| 07 | [Instalação e verificação](07-instalacao.md) |
| 08 | [Configuração do servidor](08-configuracao-servidor.md) |
| 09 | [Encaminhamento no kernel](09-encaminhamento-kernel.md) |
| 10 | [Firewall e NAT com nftables](10-firewall-nftables.md) |
| 11 | [Cliente Linux](11-cliente-linux.md) |
| 12 | [Windows, macOS e mobile](12-clientes-gui.md) |
| 13 | [DNS pelo túnel](13-dns-tunel.md) |
| 14 | [IPv6 de ponta a ponta](14-ipv6.md) |
| 15 | [Full tunnel e split tunnel](15-full-split-tunnel.md) |
| 16 | [Kill switch e falhas seguras](16-kill-switch.md) |
| 17 | [MTU e troubleshooting](17-mtu-troubleshooting.md) |
| 18 | [Operação, logs, rotação e resposta](18-operacao.md) |
| 19 | [Projeto final e runbook](19-projeto-final.md) |

## Começo rápido seguro

Antes de alterar uma VPS, gere e revise templates sem segredos:

```bash
python3 exemplos/wireguard_plan.py fixtures/vpn-plan.json
python3 exemplos/vpn_policy_audit.py fixtures/vpn-policy.json
```

Os arquivos de exemplo usam redes e endereços reservados para documentação.
Substitua-os apenas em uma cópia privada. Nunca versione chaves reais.

## Materiais

- [Laboratórios](laboratorios/README.md)
- [Ferramentas](exemplos/README.md)
- [Glossário](GLOSSARIO.md)
- [Cheatsheet](CHEATSHEET.md)
- [Respostas](RESPOSTAS.md)
- [Referências](REFERENCIAS.md)

