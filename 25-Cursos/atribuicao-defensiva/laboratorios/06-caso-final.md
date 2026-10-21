# Lab 06 — Caso final reproduzível

Entregue o pacote do capítulo 19.

## Comandos

```bash
python3 ../exemplos/evidence_manifest.py ../fixtures/evidencias-demo
python3 ../exemplos/telemetry_correlator.py ../fixtures/eventos-sinteticos.json
```

## Testes obrigatórios

- manifesto muda quando uma cópia da evidência muda;
- evento sem autorização é rejeitado pela ferramenta;
- timestamp inválido é rejeitado;
- dois eventos com mesmo IP, mas sem chave forte, não são unidos;
- sessão e request ID coerentes formam cluster;
- conclusão lista pelo menos duas hipóteses.

## Comunicação

Produza resumo técnico restrito e resumo executivo minimizado. Inclua orientação
de contenção, impacto conhecido, desconhecidos e próxima atualização.

