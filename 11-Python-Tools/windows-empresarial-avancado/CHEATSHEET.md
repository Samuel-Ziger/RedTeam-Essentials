# Consulta rápida

```powershell
# Imagem offline (comece read-only)
dism.exe /Get-WimInfo /WimFile:C:\Lab\install.wim
dism.exe /Mount-Image /ImageFile:C:\Lab\install.wim /Index:1 /MountDir:C:\Lab\mount /ReadOnly
dism.exe /Unmount-Image /MountDir:C:\Lab\mount /Discard

# Estado e política local
gpresult.exe /h C:\RTE-Lab\gpresult.html
auditpol.exe /get /category:*
Get-CimInstance Win32_DeviceGuard
Get-ProcessMitigation -System

# Ferramentas offline do curso
.\Compare-RteBaseline.ps1 -DesiredPath .\desired.json -ActualPath .\actual.json
.\Test-RteEnterpriseModel.ps1 -Path .\model.json
```

Gates: procedência → hash/assinatura → review → build → teste → piloto →
rollout → observação → rollback/close. Exceção sempre tem owner e expiração.

