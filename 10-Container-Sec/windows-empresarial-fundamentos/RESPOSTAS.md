# Respostas orientativas

## Server Core é sempre melhor?

Não. Reduz componentes e servicing, mas workload/ferramenta pode exigir Desktop
Experience. A decisão é por compatibilidade, operação e risco.

## Storage Spaces/RAID substitui backup?

Não. Ajuda disponibilidade diante de algumas falhas físicas; não protege de
exclusão, corrupção lógica, comprometimento ou perda do conjunto.

## Snapshot VSS é backup?

Não isoladamente. Pode participar de um backup consistente, mas frequentemente
compartilha o mesmo armazenamento e ciclo de falha.

## Instalar role significa serviço pronto?

Não. Falta configuração, identidade, dados, proteção, observabilidade, update,
backup, validação e ownership.

## Por que separar Get/Test/Set?

Para observar sem mutar, comparar com objetivo e convergir conscientemente.
Isso facilita `WhatIf`, teste, auditoria, idempotência e rollback.

