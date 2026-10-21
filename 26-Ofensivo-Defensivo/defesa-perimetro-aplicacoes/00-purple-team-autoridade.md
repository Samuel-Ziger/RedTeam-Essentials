# 00 — Purple Team, autoridade e método

Purple Team não é uma ferramenta nem a simples soma de Red e Blue. É um modo de
trabalho no qual uma hipótese adversária autorizada gera evidência que melhora
prevenção, detecção e resposta.

## Regras de engajamento

Antes de testar, registre proprietário, ativos, horário, origem permitida,
limites de taxa, dados proibidos, contato de emergência, critérios de parada,
rollback e retenção. "Está na Internet" não significa autorização.

Neste curso, o escopo executável é somente:

- fixtures JSON incluídas no repositório;
- serviços ligados a loopback e controlados pelo aluno;
- ambientes próprios com autorização escrita.

## Cartão de experimento

```yaml
id: PT-EDGE-001
hipotese: "o login limita tentativas por conta e contexto"
escopo: "fixture login-lab; nenhuma conta real"
estimulo: "sequencia sintética de sucessos e falhas"
esperado_red: "a resposta muda sem revelar se a conta existe"
esperado_blue: "evento correlacionado com regra, request_id e motivo"
parada: "qualquer impacto fora da fixture"
rollback: "reverter a politica versionada"
```

## Evidência e métricas

Colete configuração antes/depois, casos de teste, eventos correlacionáveis,
latência, taxa de bloqueio, falso positivo e resultado do reteste. Contagem de
"ataques bloqueados" isolada é métrica fraca: scanners, retry legítimo e uma
regra ruidosa podem inflá-la.

Red descreve o que observou sem transformar a aula em manual de evasão. Blue
explica como chegou à decisão e quais lacunas permanecem. Purple registra um
controle mensurável, um owner e uma data de revisão.

## Exercício

Escreva um cartão para proteger `POST /login`. Defina dois casos legítimos, dois
negativos e um falso positivo conhecido. Sem esses cinco casos, nenhuma regra
está pronta para bloquear.
