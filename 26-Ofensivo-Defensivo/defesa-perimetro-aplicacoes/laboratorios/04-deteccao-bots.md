# Laboratório 04 — Detecção de automação

## Executar

```bash
python3 ../exemplos/edge_risk_engine.py ../fixtures/requests-sinteticas.json
```

## Red

Classifique os eventos por objetivo possível sem afirmar autoria. Acrescente uma
cópia do evento legítimo com taxa maior e uma API autenticada sem JavaScript.

## Blue

Explique score, razões e ação. Identifique quais campos são fracos, quais podem
afetar privacidade e quais dependem da aplicação. Calcule falso positivo no seu
conjunto ampliado.

## Purple

Ajuste pesos em uma cópia da ferramenta e prove que a API legítima não recebe
CAPTCHA. Um score alto deve produzir resposta progressiva e auditável; não use
fingerprint ou IP para identificar pessoa.
