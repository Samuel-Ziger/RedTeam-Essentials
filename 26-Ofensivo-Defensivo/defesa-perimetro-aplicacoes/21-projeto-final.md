# 21 — Projeto final Purple Team

Projete a borda de uma aplicação fictícia com site, API, login, checkout, bot
legítimo e parceiro. Use somente fixtures e serviços locais.

## Entregáveis

1. autoridade, escopo, contatos, limites e critérios de parada;
2. diagrama, ativos, fronteiras e modelo de ameaça;
3. matriz de firewall, egress e proteção da origem;
4. contrato HTTP e estratégia WAF/CRS;
5. comparação fundamentada entre serviço gerenciado e BunkerWeb;
6. taxonomia de automação, score explicável e rate limits;
7. Turnstile/CAPTCHA apenas na jornada humana adequada;
8. MFA resistente a phishing para administração e recuperação segura;
9. esquema de logs, dashboards, alertas, retenção e privacidade;
10. testes Red, observações Blue, tuning, rollback e reteste Purple;
11. runbooks de abuso, falso positivo, perda de credencial e falha da borda;
12. backlog residual da aplicação com owner e prazo.

## Casos obrigatórios

- origem direta deve falhar;
- rota legítima complexa não pode ser bloqueada pelo CRS;
- sequência automatizada sintética deve gerar resposta progressiva;
- API autenticada sem JavaScript deve continuar funcional;
- token de desafio expirado/repetido deve ser rejeitado;
- dois tenants não compartilham budget;
- mudança ruim de regra deve ser revertida e auditada.

## Critério de aprovação

O projeto passa quando resultados são reproduzíveis, logs explicam decisões,
falsos positivos têm tratamento, segredos não aparecem no repositório e a
equipe demonstra rollback. Quantidade de bloqueios e uso de produto caro não
substituem evidência.

## Encerramento

Apresente uma execução de 30 minutos: cinco minutos de contexto, dez de casos
pareados, cinco de incidente/rollback e dez de riscos residuais. A melhor
conclusão é um sistema compreendido, não a promessa de uma borda impenetrável.
