# Consulta rápida

```powershell
# SO, roles e volumes
Get-ComputerInfo
Get-WindowsFeature
Get-Disk; Get-Volume; Get-PhysicalDisk; Get-StoragePool

# Operação
Get-Service
Get-ScheduledTask
Get-WinEvent -LogName System -MaxEvents 50
auditpol.exe /get /category:*

# Segurança e servicing
Get-MpComputerStatus
Get-MpPreference
Get-HotFix
dism.exe /Online /Cleanup-Image /ScanHealth

# Recuperação/virtualização
vssadmin.exe list writers
Get-VM; Get-VMSnapshot; Get-VMHardDiskDrive
```

Antes de mudar: ticket, baseline, `-WhatIf`, snapshot/backup adequado, validação
e rollback. Depois: reinício quando exigido, health checks e evidência.

