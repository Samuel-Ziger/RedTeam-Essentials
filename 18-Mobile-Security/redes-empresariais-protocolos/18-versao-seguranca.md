# 18 — Versionamento, segurança e extensibilidade

Compatibilidade precisa ser especificada. Campos desconhecidos podem ser
ignorados somente quando marcados opcionais e sem alterar semântica; tipos
desconhecidos no RNP/1 são erro. Bits reservados devem ser zero para futura
negociação segura.

Versione o wire protocol separadamente da implementação. Mudança compatível
adiciona capacidade opcional; incompatível exige nova versão/negociação. Evite
“tentar parsear e ver”, que cria downgrade/ambiguidade.

## Threat model

Atacante pode fragmentar bytes, mentir comprimento, repetir, reordenar, inundar,
enviar UTF-8 inválido ou manter conexão lenta. Parser deve ser total, limitado e
falhar fechado sem stack trace/segredo.

RNP/1 não cifra nem autentica e por isso **MUST NOT** atravessar rede não
confiável. Uma evolução real usaria TLS 1.3 com autenticação adequada e binding
de identidade/autorizacão. Checksum não substitui MAC criptográfico.

Reserve registros de message types/error codes com owner e processo. Documente
depreciação, telemetria de uso e data de remoção.
