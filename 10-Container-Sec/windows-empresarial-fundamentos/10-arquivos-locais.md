# 10 — Serviços de arquivo locais

Este capítulo prepara a camada de armazenamento sem criar compartilhamentos.
SMB, DFS e acesso remoto dependem do futuro módulo de redes.

## Namespace e governança

Defina volumes/pastas por finalidade, owner, classificação, retenção, quota,
backup e descarte. ACLs devem usar grupos funcionais mesmo no modelo; evitar
permissões diretas por pessoa reduz complexidade.

## FSRM

File Server Resource Manager pode modelar quotas, file screens, classificação
e relatórios. File screen não é antivírus e extensão não prova conteúdo. Comece
em audit/passive quando possível e trate falsos positivos.

```powershell
Get-WindowsFeature FS-Resource-Manager
Get-FsrmQuota -ErrorAction SilentlyContinue
Get-FsrmFileScreen -ErrorAction SilentlyContinue
```

## Data Deduplication

Confirme se o workload/volume é suportado, meça economia e CPU/I/O, planeje
scrubbing/garbage collection e assegure recuperação em ambiente compatível.

## Exercício

Crie árvore local de fixture com grupos/ACLs, quota de teste e relatório. Não
publique a pasta. Restaure ACL e remova feature/fixture no cleanup.

