# 09 — Armazenamento empresarial local

Windows Server trabalha com discos, partições, volumes, VHD/VHDX, Storage
Spaces, NTFS e ReFS. O desenho deve separar desempenho, resiliência, capacidade,
backup e recuperação.

## Escolhas

- NTFS: compatibilidade ampla e recursos maduros;
- ReFS: integridade/escala em workloads suportados, com diferenças de features;
- VHDX: imagem virtual resiliente, dinâmica ou fixa;
- Storage Spaces: agrega discos e define layout/resiliência;
- deduplication: economiza capacidade com custo e suporte por workload.

```powershell
Get-PhysicalDisk
Get-StoragePool
Get-VirtualDisk
Get-Disk
Get-Volume
```

RAID/Storage Spaces não substitui backup: protege disponibilidade diante de
algumas falhas, mas replica exclusão, corrupção e erro administrativo.

## Laboratório

Com discos virtuais descartáveis, crie pool e virtual disk simples/espelhado,
formate, grave fixture, simule remoção apenas no hypervisor e observe health.
Restaure snapshot; não use discos físicos do host.

