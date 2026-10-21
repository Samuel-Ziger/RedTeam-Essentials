# Referências comentadas

## WireGuard

- [WireGuard Quick Start](https://www.wireguard.com/quickstart/) — comandos,
  geração de chaves, `wg-quick` e keepalive.
- [Cryptokey Routing](https://www.wireguard.com/) — relação entre chaves e
  `AllowedIPs`.
- [Protocolo WireGuard](https://www.wireguard.com/protocol/) — construção
  criptográfica e mensagens.
- [Instalação oficial](https://www.wireguard.com/install/) — pacotes por sistema.

## Padrões e operação

- [NIST SP 800-77 Rev. 1](https://csrc.nist.gov/pubs/sp/800/77/r1/final) —
  planejamento de VPNs IPsec e princípios aplicáveis à operação segura.
- [CISA: hardening de infraestrutura de comunicações](https://www.cisa.gov/resources-tools/resources/enhanced-visibility-and-hardening-guidance-communications-infrastructure) — exposição mínima, criptografia forte e logging central.
- [RFC 4787](https://www.rfc-editor.org/info/rfc4787/) — NAT UDP.
- [RFC 6598](https://www.rfc-editor.org/info/rfc6598/) — CGNAT.
- [nftables Wiki](https://wiki.nftables.org/) — modelo e sintaxe; confirme com
  o manual da distribuição.
- [Debian Handbook — firewall](https://www.debian.org/doc/manuals/debian-handbook/sect.firewall-packet-filtering.en.html) — administração de filtragem.

## Comunidade

- [WireGuard mailing list](https://lists.zx2c4.com/mailman/listinfo/wireguard) —
  discussão técnica do projeto.
- [Server Fault](https://serverfault.com/) — problemas de administração;
  valide respostas contra documentação e versão do sistema.

Revisado em 1 de outubro de 2026. Pacotes e sistemas mudam; consulte a
documentação da distribuição antes de aplicar comandos em produção.

