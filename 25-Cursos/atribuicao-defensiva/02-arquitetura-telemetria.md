# 02 — Arquitetura de telemetria

Planeje visibilidade em camadas:

```text
identidade ─┐
endpoint ───┼─> coleta autenticada -> normalização -> armazenamento imutável
rede/DNS ───┤                              |              |
aplicação ──┤                              v              v
nuvem/SaaS ─┘                         detecção        investigação
```

## Fonte e transporte

Registre versão, owner, esquema, timezone, clock, autenticação do emissor,
buffer/fila, perda e transformação. Encaminhamento central reduz oportunidade de
alteração local, mas o coletor também precisa de hardening e segregação.

## Campos comuns

`event_id`, `timestamp`, `source`, `actor`, `device`, `src_ip`, `src_port`,
`dst_ip`, `dst_port`, `protocol`, `session_id`, `request_id`, `action`, `result`
e `raw_reference`. Nem toda fonte terá tudo; não invente valores ausentes.

## Qualidade

Monitore volume esperado, atraso, duplicação, parsing, mudanças de esquema e
silêncio por fonte. Uma busca que retorna zero pode significar ausência de
evento, falha de coleta, retenção expirada ou consulta errada.

## Privacidade

Classifique campos pessoais, aplique controle de acesso por função e use dados
agregados para saúde quando detalhes não são necessários.

## Prática

Crie data dictionary de cinco fontes e defina owner, relógio, retenção e teste
de saúde.

