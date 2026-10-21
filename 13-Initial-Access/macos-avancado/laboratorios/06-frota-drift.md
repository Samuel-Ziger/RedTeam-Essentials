# Lab 06 — Frota, baseline e drift

## Cenário

Uma frota sintética possui Macs arm64 em quatro estados de update, FileVault e
compliance. Nenhuma integração externa será chamada.

## Procedimento

1. Defina desired state com aplicabilidade e severidade.
2. Compare observations e classifique compliant/drift/missing/not-applicable.
3. Separe falha transitória, exceção aprovada e violação acionável.
4. Crie anéis canary/pilot/production e critérios de promoção.
5. Defina dados mínimos, retenção e acesso.

## Entrega

Dashboard textual, fila priorizada, owners, SLA, rollback e expiração das
exceções. Não use serial nem nome de pessoa como chave.
