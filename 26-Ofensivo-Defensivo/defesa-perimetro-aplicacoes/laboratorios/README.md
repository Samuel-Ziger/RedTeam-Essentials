# Laboratórios Purple Team

Todos os laboratórios usam fixtures ou um serviço local de propriedade do aluno.
Não direcione testes a Cloudflare, BunkerWeb, sites ou APIs de terceiros.

| # | Laboratório | Produto |
|---:|---|---|
| 01 | [Modelo de ameaça e matriz de firewall](01-modelo-matriz-firewall.md) | diagrama + matriz |
| 02 | [WAF, CRS e falso positivo](02-waf-crs-falso-positivo.md) | suite de regressão |
| 03 | [Cloudflare e BunkerWeb](03-cloudflare-bunkerweb.md) | comparação operacional |
| 04 | [Detecção de automação](04-deteccao-bots.md) | relatório do score |
| 05 | [Token bucket](05-rate-limit.md) | simulação determinística |
| 06 | [Turnstile e MFA](06-turnstile-mfa.md) | testes de fluxo |
| 07 | [Capstone Purple Team](07-capstone-purple-team.md) | dossiê completo |

## Formato da evidência

Para cada caso, registre `id`, hipótese, entrada, resultado esperado, resultado
observado, log/request ID, conclusão, mudança, rollback e reteste. Dados reais e
segredos não fazem parte da entrega.
