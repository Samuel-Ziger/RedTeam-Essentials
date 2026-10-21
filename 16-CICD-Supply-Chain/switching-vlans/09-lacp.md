# 09 — Agregação e LACP

Link aggregation agrupa enlaces compatíveis em um canal lógico. LACP negocia e
monitora membros. Todos devem concordar em velocidade, duplex, VLANs, MTU e
atributos; configure STP no agregado, não de modo inconsistente por membro.

Agregação aumenta capacidade total e tolera falha de membro, mas um fluxo
normalmente fica em um enlace conforme hash de MAC/IP/portas. Dois links de
1 Gbit/s não garantem 2 Gbit/s para uma única conexão.

Modo ativo inicia negociação; passivo responde. Dois lados passivos podem não
formar. Port-channel estático não detecta as mesmas incompatibilidades e exige
mais cuidado.

## Exercício

Distribua oito fluxos por um hash fictício em quatro membros. Remova um membro,
recalcule e explique microinterrupção, reordenação e capacidade residual.
