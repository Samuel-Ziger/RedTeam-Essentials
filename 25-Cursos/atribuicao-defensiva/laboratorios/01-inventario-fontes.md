# Lab 01 — Inventário de fontes

Para cada `source` da fixture, registre owner, schema, timestamp, fuso, atraso,
retenção, campos pessoais, método de coleta e teste de saúde.

## Passos

1. leia o JSON sem alterar;
2. conte eventos por fonte e tipo;
3. identifique campos ausentes;
4. classifique pivôs fortes e fracos;
5. proponha uma métrica de saúde por fonte;
6. defina quem pode consultar cada campo.

## Aceite

O catálogo deve explicar que `src_ip` isolado não é chave de identidade e que
um evento sem campo não autoriza preenchê-lo por suposição.

