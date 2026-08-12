# Microemulação Purple Team segura

## Cenário

Objetivo: validar se concessões administrativas cloud sintéticas e criação de
pod privilegiado são identificadas, triadas e comunicadas. Nenhuma ação ocorre
em infraestrutura real.

## Plano

| Fase | Entregável | Critério de sucesso |
|------|------------|---------------------|
| Planejar | RoE, responsáveis, hipóteses e parada | Aprovação antes da execução. |
| Executar | Analisadores sobre fixtures versionadas | Eventos positivos detectados e negativos ignorados. |
| Observar | Alertas normalizados e timestamps | Ator, alvo, ação e fonte preservados. |
| Responder | Decisão simulada e evidência mínima | Contenção proporcional, sem destruir fixture. |
| Melhorar | Gap, owner e prazo | Teste de regressão associado ao gap. |

## Execução

```bash
python3 08-Cloud-RedTeam/labs/analyze_events.py \
  08-Cloud-RedTeam/labs/fixtures/aws-cloudtrail.jsonl
pytest -q tests/python/test_cloud_lab.py tests/python/test_lab_fixtures.py
```

## Debrief

Registre cobertura observada, falso positivo, dado ausente, tempo de decisão,
controle preventivo e próximo teste. Não use contagem de técnicas ATT&CK como
substituto para resultado operacional.

