# Lab 05 — Detecção de proxy e lacuna de telemetria

Use os eventos `proxy_policy_change` e `sensor_health` da fixture.

1. formule uma detecção de proxy não autorizado com processo + mudança + fluxo;
2. adicione um caso legítimo de suporte remoto aprovado;
3. formule alerta de ausência de heartbeat;
4. adicione manutenção planejada como negativo;
5. defina triagem e contenção reversível;
6. mapeie T1090/T1070 apenas no relatório.

Não execute proxy nem apague evento. A emulação é um registro sintético.

## Aceite

A regra deve exigir contexto e não alertar apenas por nome de ferramenta ou IP.

