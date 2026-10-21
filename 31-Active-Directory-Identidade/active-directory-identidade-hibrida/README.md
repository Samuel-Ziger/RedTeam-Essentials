# Active Directory e identidade híbrida

Esta rota parte do inventário para chegar a caminhos de privilégio e controles
de identidade, sempre em uma floresta de laboratório.

## Sequência

1. Modele domínios, trusts, contas e delegações com os
   [comandos de inventário](ad_enum_commands.md).
2. Interprete relações no [BloodHound](bloodhound_teoria.md)
   sem confundir possibilidade gráfica com impacto comprovado.
3. Estude [Kerberoasting](kerberoasting_teoria.md) junto a
   higiene de contas de serviço, telemetria e remediação.
4. Analise [cenários modernos](modern-ad-attacks-2026.md)
   somente em identidades fictícias.
5. Conecte o diretório local ao modelo de
   [identidade híbrida](LEGADO-IDENTIDADE-HIBRIDA.md).

## Entrega

Produza um grafo comentado com caminhos priorizados, evidência de cada aresta,
detecções esperadas, correções propostas e reteste. Segredos nunca entram no
relatório; use identificadores e dados sintéticos.
