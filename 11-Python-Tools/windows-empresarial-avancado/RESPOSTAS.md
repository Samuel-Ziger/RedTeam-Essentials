# Respostas orientativas

## Uma domain é fronteira de segurança contra admins da forest?

Em geral, não. A forest é a principal fronteira do AD DS. Domains organizam e
particionam diversos aspectos, mas administradores de floresta têm alcance amplo.

## OU deve copiar o organograma?

Não por padrão. OU serve a delegação e aplicação de política. Estrutura deve
ser estável, simples e orientada a requisitos administrativos.

## `missing` é não conforme?

Não automaticamente. Significa evidência ausente; trate como desconhecido,
corrija a coleta e só então avalie conformidade.

## Hash é sempre a melhor regra de App Control?

Não. É exato, mas quebra em cada update. Publisher/catálogo podem escalar melhor,
desde que identidade e escopo do signatário sejam adequados.

## Alta disponibilidade substitui backup?

Não. Replicação/failover podem propagar corrupção. Backup independente e
restore testado cobrem outra classe de falha.

