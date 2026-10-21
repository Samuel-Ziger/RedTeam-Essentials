# 16 — Hyper-V standalone e offline

Hyper-V usa hypervisor tipo 1; root/management partition administra child
partitions. VMBus e dispositivos sintéticos reduzem overhead. Neste curso todas
as VMs são criadas sem adaptador de rede.

## Objetos

- VM configuration e generation;
- VHDX fixo/dinâmico/differencing;
- checkpoint standard/production;
- memória estática/dinâmica;
- vCPU, NUMA e integration services;
- export/import e compatibilidade de versão.

```powershell
Get-WindowsFeature Hyper-V
Get-VM | Select-Object Name, State, Generation, Version
Get-VMHardDiskDrive
Get-VMSnapshot
```

Checkpoint não substitui backup e uma cadeia longa de differencing disks aumenta
risco/complexidade. Production checkpoint tenta consistência de workload, mas
ainda precisa de teste.

## Laboratório

Crie VM Generation 2 sem NIC, VHDX de dados, checkpoint, alteração de fixture e
rollback. Exporte/import, valide boot e remova todos os artefatos.

