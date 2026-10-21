# 24 — VPN própria e operação segura

Este módulo transforma os fundamentos de privacidade em uma implantação
administrável: uma VPN WireGuard em uma VPS própria, com chaves por dispositivo,
firewall mínimo, roteamento, DNS, IPv4/IPv6, monitoramento, atualização e plano
de recuperação. A VPS e as contas usadas devem pertencer ao estudante ou à
organização que autorizou o laboratório.

Uma VPN própria oferece controle do servidor, não anonimato automático. O
provedor da VPS, o provedor de acesso, o serviço de destino e aplicações ainda
podem observar partes diferentes da sessão. O curso trata essa troca de
confiança explicitamente.

## Contrato do módulo

| Campo | Definição |
|---|---|
| Público | Administradores, desenvolvedores e estudantes de segurança com base em Linux e redes. |
| Pré-requisitos | Módulos 06, 14–18, 21 e 23. |
| Tempo estimado | 160–240 horas. |
| Ambiente | VPS própria ou VM local equivalente; endereços de documentação nas fixtures; mudanças somente após revisão. |
| Evidência final | Arquitetura, configurações sem segredos, checklist de hardening, testes e runbook de recuperação. |
| Critério de conclusão | Implantar e manter um túnel autorizado, explicar rotas e confiança e recuperar uma falha simulada. |

## Comece aqui

- [Curso completo](vpn-propria-operacao-segura/README.md)
- [Laboratórios](vpn-propria-operacao-segura/laboratorios/README.md)
- [Planejador e auditor offline](vpn-propria-operacao-segura/exemplos/README.md)
- [Consulta rápida](vpn-propria-operacao-segura/CHEATSHEET.md)

## Entregáveis

- diagrama de fluxo e fronteiras de confiança;
- plano de endereçamento sem sobreposição;
- configuração WireGuard revisada, sem chaves privadas no Git;
- política de firewall e encaminhamento com rollback;
- testes de DNS, IPv4, IPv6, MTU e queda do túnel;
- inventário de peers, rotação, revogação, atualização e backup.

## Vídeos em português

Use os vídeos como demonstração complementar e mantenha as chaves do seu
laboratório fora de gravações, repositórios e capturas de tela.

1. [Configurando VPN Client to Site — Windows e WireGuard](https://www.youtube.com/watch?v=zxqHlXJXi2g) — **Hackone — Lucas Palma**.
2. [Conexão VPN em laboratório](https://www.youtube.com/watch?v=EMH5dL3KoAQ) — **Cybersecurity With Mateus Novaes**.
3. [Protocolo TCP/IP — curso completo](https://www.youtube.com/watch?v=kP1kktlbUTs) — **Hardware Redes Brasil**.
4. [IP, DNS, DHCP e roteamento](https://www.youtube.com/watch?v=z2vnQcb8nGI) — **Cyber Security Br**.
5. [Privacidade na Internet: roteamento aleatorizado com Tor](https://www.youtube.com/watch?v=J2jzgYwMDhk) — **NIC.br**.
