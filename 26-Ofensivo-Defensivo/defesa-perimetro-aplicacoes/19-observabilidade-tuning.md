# 19 — Observabilidade, tuning e falsos positivos

Um controle sem telemetria explicável vira caixa-preta. Registre o suficiente
para reproduzir a decisão, com minimização de dados e retenção definida.

## Esquema de evento

```json
{
  "timestamp": "2026-10-01T12:00:00Z",
  "request_id": "req-001",
  "route": "/login",
  "rule_id": "login-risk-v3",
  "action": "challenge",
  "reasons": ["auth_failures", "high_rate"],
  "policy_version": "2026.10.1"
}
```

Evite corpo, senha, cookie, token e PII desnecessária. Se IP for necessário,
controle acesso e prazo. Preserve identificação de regra, versão e request ID
em edge, proxy e aplicação.

## Métricas

- aceitação, desafio, limite e bloqueio por rota;
- falso positivo confirmado e tempo de resolução;
- solve/abandon rate de desafio;
- p50/p95/p99 de latência adicionada;
- cobertura de logs e falhas de exportação;
- deriva, idade e uso das exceções.

## Tuning como engenharia

Reproduza o caso, encontre a regra e o campo, crie menor exclusão, teste o caso
negativo relacionado, aplique canário e defina expiração. Não permita uma rota
inteira porque um parâmetro legítimo acionou detecção.

## Shadow e regressão

Nova regra deve observar antes de bloquear quando o risco permitir. Congele um
conjunto sanitizado de verdadeiros/falsos positivos e execute-o a cada mudança.

## Purple Team

Red entrega caso reproduzível e impacto. Blue investiga sem pedir segredo do
usuário. Purple só encerra quando o legítimo funciona, o negativo continua
coberto, os dashboards refletem a versão nova e o rollback foi testado.
