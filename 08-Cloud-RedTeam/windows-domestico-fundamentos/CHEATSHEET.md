# Consulta rápida

Use depois de compreender os capítulos. Confirme o alvo, execute como usuário
comum e eleve somente o comando que precisar.

## Identidade do sistema

```powershell
Get-ComputerInfo |
  Select-Object WindowsProductName, WindowsVersion, OsBuildNumber,
    OsArchitecture, BiosFirmwareType
Get-CimInstance Win32_OperatingSystem |
  Select-Object Caption, Version, BuildNumber, InstallDate
```

## Firmware e dispositivos

```powershell
Get-Tpm
Confirm-SecureBootUEFI
Get-CimInstance Win32_PnPSignedDriver |
  Select-Object DeviceName, DriverVersion, Manufacturer, IsSigned
```

Erro de acesso, cmdlet ausente, `$null` e `False` têm significados diferentes.

## Arquivos e integridade

```powershell
$path = Join-Path $env:TEMP 'RTE-Arquivos'
Get-ChildItem -LiteralPath $path -Force
Get-FileHash -LiteralPath (Join-Path $path 'fixture.txt') -Algorithm SHA256
Get-AuthenticodeSignature -FilePath .\artefato.exe
```

## Discos e BitLocker

```powershell
Get-Disk | Select-Object Number, Size, PartitionStyle, IsBoot, IsSystem
Get-Partition | Select-Object DiskNumber, PartitionNumber, DriveLetter, Type, Size
Get-Volume | Select-Object DriveLetter, FileSystem, HealthStatus, Size, SizeRemaining
Get-BitLockerVolume | Select-Object MountPoint, VolumeStatus,
  EncryptionPercentage, ProtectionStatus, EncryptionMethod
```

Nunca opere por letra/número memorizado; revalide imediatamente antes da ação.

## Identidade e ACL

```powershell
whoami /user
whoami /groups
whoami /priv
Get-LocalUser | Select-Object Name, Enabled, SID
Get-Acl -LiteralPath 'C:\RTE-Lab\dados' |
  Select-Object Owner, AreAccessRulesProtected, AccessToString
```

## Processos, serviços e inicialização

```powershell
Get-Process | Sort-Object CPU -Descending |
  Select-Object -First 10 Name, Id, CPU, WorkingSet64
Get-Service | Group-Object Status
Get-CimInstance Win32_Service |
  Select-Object Name, State, StartMode, StartName, ProcessId, PathName
Get-ScheduledTask | Select-Object -First 20 TaskPath, TaskName, State
```

CPU é acumulada; estado atual e modo de início do serviço são diferentes.

## Aplicativos e servicing

```powershell
winget list
Get-AppxPackage | Select-Object Name, Publisher, Architecture, Version
Get-HotFix | Sort-Object InstalledOn -Descending
Get-WindowsPackage -Online |
  Where-Object PackageState -eq Installed |
  Select-Object -First 20 PackageName, ReleaseType, InstallTime
```

Nenhuma dessas consultas cobre sozinha todos os aplicativos ou atualizações.

## Registro isolado

```powershell
$path = 'HKCU:\Software\RTECourse'
New-Item -Path $path -Force
New-ItemProperty -Path $path -Name Lesson -PropertyType String `
  -Value 'registry-basics'
Get-ItemProperty -LiteralPath $path
Remove-Item -LiteralPath $path -Recurse -Confirm
```

## Eventos

```powershell
$start = (Get-Date).AddMinutes(-15)
Get-WinEvent -FilterHashtable @{
  LogName = 'System'
  StartTime = $start
} | Select-Object -First 50 TimeCreated, ProviderName, Id,
    LevelDisplayName, RecordId
```

Identifique evento por canal, provider, ID e horário; não apenas pelo número.

## Defender

```powershell
Get-MpComputerStatus |
  Select-Object AntivirusEnabled, RealTimeProtectionEnabled,
    AntivirusSignatureVersion, AntivirusSignatureLastUpdated, QuickScanAge
Get-MpPreference |
  Select-Object PUAProtection, EnableControlledFolderAccess
```

Não crie exclusões nem desative proteção para “testar”.

## Verificação antes de reparo

```powershell
DISM.exe /Online /Cleanup-Image /CheckHealth
DISM.exe /Online /Cleanup-Image /ScanHealth
sfc.exe /verifyonly
chkdsk.exe C: /scan
```

Use apenas quando a hipótese envolve o objeto verificado. Modos de reparo alteram
estado e exigem backup, elevação, logs e validação posterior.

## Regra de ouro

```text
snapshot → baseline → hipótese → alvo → consulta → mudança única
         → validação funcional/técnica → rollback → comparação
```
