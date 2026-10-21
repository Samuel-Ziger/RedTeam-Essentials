# 19 — Projeto final: Mac local recuperável

O projeto entrega um baseline e um plano de recuperação, não uma coleção de
prints. Use apenas fixtures e dados sanitizados.

## Entregáveis

1. ficha de versão, build, arquitetura e capacidade, sem identificadores;
2. mapa APFS e explicação de System/Data/Recovery;
3. matriz de contas, grupos e elevações necessárias;
4. inventário de apps com origem e assinatura;
5. baseline de FileVault, SIP e Gatekeeper;
6. consulta de logs para um incidente de fixture;
7. backup com manifesto e restauração comprovada;
8. runbook de atualização, falha e recuperação.

## Critérios

- nenhum controle foi reduzido;
- nenhuma informação pessoal ou segredo foi coletado;
- comandos distinguem observação e mutação;
- hashes, tempos e pós-condições sustentam as conclusões;
- outra pessoa consegue restaurar a fixture usando somente o runbook.

Depois da apresentação, remova artefatos derivados e mantenha apenas evidência
sanitizada. O próximo módulo explica internals e gestão em escala.
