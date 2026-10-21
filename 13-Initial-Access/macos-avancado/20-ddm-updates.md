# 20 — Declarative management e atualizações

Declarative Device Management move parte da lógica para declarações, ativações,
assets e status no dispositivo. Isso reduz polling, mas não elimina projeto de
estado, observabilidade ou reconciliação.

Updates precisam de inventário compatível, anéis, prazo, energia/espaço,
comunicação ao usuário, exceções e recuperação. Rapid Security Responses e
Background Security Improvements têm ciclos próprios conforme versão.

## Anéis

- canário de TI com rollback conhecido;
- piloto representativo de hardware/apps;
- produção em ondas;
- exceções com prazo e owner.

## Prática

Receba um status sintético de dez dispositivos, classifique ready/deferred/
blocked/failed e escreva critérios de promoção. Não busque updates na rede.
