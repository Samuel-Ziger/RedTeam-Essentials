# 10 — Cloudflare WAF

O WAF da Cloudflare usa rulesets. Regras gerenciadas cobrem classes conhecidas;
custom rules combinam uma expressão e uma ação; rate limiting e sinais de bot
acrescentam contexto. Recursos e limites dependem do plano atual, portanto a
documentação oficial é a fonte operacional.

## Modelo mental

```text
requisição → fases/rulesets → expressão verdadeira → ação
                                              └→ evento com regra/contexto
```

Ordem importa. Ações terminais podem impedir regras posteriores. Antes de
publicar, revise precedência, `skip`, exceções e sobreposição entre regras
gerenciadas e locais.

## Custom rule bem formada

Defina objetivo, host, rota, método, identidade/contexto, ação, expiração e
teste. Uma regra por país ou user-agent raramente é prova suficiente: combine
sinais e proteja o caso de negócio.

```text
nome: login-step-up-risk
se: host e rota de login + sinal de risco composto
então: managed challenge
excluir: healthcheck autenticado e documentado
modo inicial: log/análise
```

## Workflow seguro

Use Security Events/Analytics para baseline, aplique em canário, acompanhe
status, latência, challenge solve rate e suporte. Exporte configuração quando
possível e audite mudanças. Não copie uma regra da Internet sem conhecer o
tráfego da aplicação.

## Purple Team

Red executa casos aprovados pelo hostname de homologação. Blue correlaciona
Ray/request ID, ruleset, ação e log de origem. Purple verifica se a origem não
recebeu o request bloqueado e se o controle não afetou a rota vizinha.
