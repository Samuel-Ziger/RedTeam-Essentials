# Consulta rápida — Windows doméstico avançado

Use estes comandos somente na VM e em fixtures próprias. Leia a ajuda da versão instalada. Consultas vazias ou indisponíveis viram `unknown`, não “falso”.

## Identidade do ambiente

```powershell
Get-ComputerInfo | Select-Object WindowsProductName, WindowsVersion,
    OsBuildNumber, OsArchitecture
whoami /all
Get-Process -Id $PID | Select-Object Id, SessionId, StartTime,
    HandleCount, WorkingSet64, PrivateMemorySize64
```

## PE, DLL e assinatura

```powershell
.\exemplos\Get-RtePeSummary.ps1 -Path .\fixture.exe |
    Select-Object Machine, Format, Subsystem, EntryPointRva,
        SizeOfImage, SectionCount, Sha256, SignatureStatus

Get-AuthenticodeSignature -LiteralPath .\fixture.exe
Get-FileHash -LiteralPath .\fixture.exe -Algorithm SHA256
dumpbin.exe /headers .\fixture.exe
dumpbin.exe /imports .\fixture.exe
```

Hash responde se os bytes são iguais; assinatura acrescenta identidade e cadeia de confiança; nenhum dos dois prova que o comportamento é seguro.

## Registro, serviços e drivers

```powershell
Get-ItemProperty -LiteralPath 'HKCU:\Software\RTECourse\Advanced'
Get-CimInstance Win32_Service |
    Select-Object Name, State, StartMode, StartName, PathName
Get-ScheduledTask | Select-Object TaskPath, TaskName, State
Get-CimInstance Win32_PnPSignedDriver |
    Select-Object DeviceName, DriverProviderName, DriverVersion, IsSigned, InfName
```

Não altere serviço ou driver do sistema. A tarefa permitida é apenas a fixture descrita no capítulo 11.

## Eventos e desempenho

```powershell
$start = (Get-Date).AddMinutes(-15)
Get-WinEvent -FilterHashtable @{ LogName='System'; StartTime=$start; Level=2,3 } |
    Select-Object TimeCreated, ProviderName, Id, RecordId, Message

Get-Counter '\Processor(_Total)\% Processor Time',
    '\Memory\Available MBytes' -SampleInterval 1 -MaxSamples 10
```

No ProcMon: pare → limpe → filtre pelo executável → capture uma reprodução → pare → interprete a sequência. No WPA: delimite o intervalo → filtre processo/thread → confira unidade → valide símbolos → examine stack.

## Proteções

```powershell
Get-MpComputerStatus | Select-Object AntivirusEnabled,
    RealTimeProtectionEnabled, AntivirusSignatureVersion,
    AntivirusSignatureLastUpdated
Get-ProcessMitigation -System
Get-ProcessMitigation -Name .\fixture.exe
Get-CimInstance -ClassName Win32_DeviceGuard `
    -Namespace root\Microsoft\Windows\DeviceGuard |
    Select-Object VirtualizationBasedSecurityStatus,
        SecurityServicesConfigured, SecurityServicesRunning,
        AvailableSecurityProperties
Get-Tpm
Confirm-SecureBootUEFI
```

Separe disponibilidade, configuração e execução. Não use exclusão ampla, `DisableRealtimeMonitoring` ou política `Bypass`.

## WinDbg para mini dump próprio

```text
.sympath        revisar caminho
.reload /f      carregar e conferir símbolos
lm              listar módulos/builds
!analyze -v     hipótese automatizada inicial
.ecxr           contexto da exceção, quando aplicável
k               stack atual
~               threads
```

Encontre o primeiro frame próprio com PDB correspondente. Não capture processo externo ou sensível.

## Modelo mínimo de relatório

```text
escopo + classe de risco
ambiente + versão + hashes + UTC
sintoma esperado/observado
hipóteses e previsões
fonte + filtro + comando + limitação
linha do tempo de fatos
causa ou próximo teste
correção + regressão + desempenho
retenção + cleanup
```

