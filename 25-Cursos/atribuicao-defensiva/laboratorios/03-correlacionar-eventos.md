# Lab 03 — Correlacionar eventos e montar grafo

Execute:

```bash
python3 ../exemplos/telemetry_correlator.py ../fixtures/eventos-sinteticos.json
```

Para cada cluster:

1. liste eventos e fontes;
2. identifique chaves compartilhadas (`request_id`, `session_id`, `device`);
3. desenhe nós e arestas;
4. rotule arestas observadas ou inferidas;
5. declare confiança e alternativa;
6. explique por que endereço IP não é usado sozinho para unir eventos.

## Aceite

A ação `role.grant` deve se ligar à autenticação e ao endpoint por mais de uma
fonte. A conclusão permanece técnica e admite sessão/token roubado.

