# 🪟 Windows Privilege Escalation - Teoria Completa

> Guia educacional sobre escalação de privilégios no Windows

---

## 📚 O que é Privilege Escalation?

**Privilege Escalation** (PrivEsc) é elevar permissões de um usuário de baixo privilégio para um contexto privilegiado (Administrators, SYSTEM ou equivalente).

### Tipos
```
Vertical PrivEsc:
└─ user → Administrator / SYSTEM

Horizontal PrivEsc:
└─ user1 → user2 (mesmo nível, outro contexto)
```

### Contexto Windows
```
Após foothold:
├─ Entender token, grupos e privs
├─ Mapear caminhos de elevação locais
├─ Obter SYSTEM ou Admin local
└─ Depois: lateral movement — ver windows_lateral_movement_teoria.md
```

⚠️ **Use apenas em ambientes autorizados (labs, CTFs, pentests com escopo escrito)**

Este material é **teoria + enumeração**. Não inclui exploits funcionais, shellcode nem PoCs weaponizados.

---

## ⚖️ Disclaimer Ético

```
PERMITIDO (com autorização):
├─ Labs pessoais (VMs isoladas)
├─ Plataformas oficiais (TryHackMe, HackTheBox, etc.)
├─ Exercícios GOAD / ranges internos autorizados
└─ Pentests com contrato e escopo claro

NÃO PERMITIDO:
├─ Sistemas sem autorização explícita
├─ Contornar controles em produção "para testar"
└─ Distribuir/usar exploits fora do escopo ético
```

**Regra prática:** sem autorização por escrito (ou lab claramente seu), **pare**.

---

## 🔍 Enumeração Inicial Windows

A maior parte do PrivEsc é **encontrar** a misconfiguração.

### Quem sou eu?
```cmd
whoami
whoami /all
whoami /priv
whoami /groups
```

```powershell
[System.Security.Principal.WindowsIdentity]::GetCurrent().Name
Get-LocalGroupMember Administrators
```

**Interprete `whoami /priv`:**
```
Enabled  → privilégio ativo no token atual
Disabled → presente; pode ser habilitado (ainda útil)
Ausente  → não faz parte do token
```

Privilégios de alto interesse: `SeImpersonatePrivilege`, `SeAssignPrimaryTokenPrivilege`, `SeDebugPrivilege`, `SeBackupPrivilege`, `SeRestorePrivilege`, `SeTakeOwnershipPrivilege`, `SeLoadDriverPrivilege`.

---

### Sistema, usuários e rede
```cmd
systeminfo
hostname
ver
wmic os get Caption,Version,BuildNumber,OSArchitecture

net user
net user %USERNAME%
net localgroup
net localgroup Administrators
net accounts
net share

ipconfig /all
route print
netstat -ano
```

```powershell
Get-ComputerInfo | Select-Object WindowsProductName, WindowsVersion
Get-LocalUser | Format-Table Name, Enabled, LastLogon
Get-LocalGroupMember -Group "Administrators"
Get-NetTCPConnection | Where-Object {$_.State -eq "Listen"}
```

**Grupos relevantes:** Administrators, Backup Operators, Remote Desktop Users, Remote Management Users, Distributed COM Users, Hyper-V Administrators.

**Anote:** edição (Home/Pro/Server), build, patches, domínio vs workgroup, arquitetura.

---

### Processos, serviços, PATH e software
```cmd
tasklist /v
tasklist /svc
sc query state= all
wmic service get Name,StartName,PathName,StartMode
echo %PATH%
set
wmic product get Name,Version
wmic qfe get HotFixID,InstalledOn
```

```powershell
Get-CimInstance Win32_Service | Select-Object Name, StartName, PathName, StartMode
Get-HotFix | Sort-Object InstalledOn -Descending
Get-ItemProperty HKLM:\Software\Microsoft\Windows\CurrentVersion\Uninstall\* |
  Select-Object DisplayName, DisplayVersion | Sort-Object DisplayName
```

---

## 🛡️ UAC (User Account Control) — Conceitos

### O que é UAC?
O UAC separa token **filtrado** (Medium IL) e token **elevado** (High IL) para contas administrativas. Processos comuns rodam sem privilégios plenos até haver consentimento/elevação.

```
Admin logado com UAC:
├─ Token filtrado  → apps do dia a dia (Medium Integrity)
└─ Token elevado   → após prompt UAC (High Integrity)
```

```cmd
whoami /groups | findstr /i "Mandatory"
```

### Bypass UAC — teoria (sem PoC)
Em labs, "UAC bypass" costuma significar: **obter High Integrity a partir de Medium** via auto-elevação, COM, hijack de caminhos confiáveis ou políticas enfraquecidas — **não** é PrivEsc de usuário comum para Admin.

```
Conceitos (educacional):
├─ AutoElevate: binários Microsoft que elevam sem prompt (em certos contextos)
├─ DLL / path abuse em processos auto-elevados
├─ Abuso de interfaces COM registradas
└─ Políticas UAC fracas (ex.: ConsentPromptBehaviorAdmin = 0)
```

⚠️ Sem implementações weaponizadas. Em lab autorizado, estude comportamento e detecção; em engajamentos reais, documente risco e impacto.

### Detecção / defesa
```
Blue team:
├─ Filhos inesperados de binaries auto-elevados
├─ Eventos de elevação / falhas de consent
├─ Mudanças em Policies\System (UAC)
└─ Telemetria EDR parent-child anômala

Hardening: UAC no máximo prático; não desabilitar prompts;
restringir escrita em paths de apps elevados.
```

---

## ⚙️ Serviços Vulneráveis

Serviços frequentemente rodam como **LocalSystem**. Misconfigs em path, ACLs ou instaladores são vetores clássicos.

### 1. Unquoted Service Path

**Conceito:** `PathName` com espaços e **sem aspas** pode fazer o Windows tentar executáveis intermediários na busca.

```
Exemplo teórico:
C:\Program Files\Vulnerable App\service.exe

Busca possível (conceito):
C:\Program.exe
C:\Program Files\Vulnerable.exe
C:\Program Files\Vulnerable App\service.exe
```

```cmd
wmic service get Name,PathName,StartName,StartMode | findstr /i /v "C:\Windows\\"
sc qc SERVICENAME
```

```powershell
Get-CimInstance Win32_Service |
  Where-Object { $_.PathName -notmatch '^"' -and $_.PathName -match ' ' } |
  Select-Object Name, PathName, StartName, StartMode
```

**Checklist:** path sem aspas + espaço + diretório gravável por low-priv + serviço reiniciável/auto-start.

---

### 2. Weak Permissions (serviço / binário)

**Conceito:** Se low-priv modifica o binário, `sc config`, ou ACLs da pasta, pode redirecionar execução privilegiada.

```cmd
sc qc SERVICENAME
sc sdshow SERVICENAME
icacls "C:\Path\To\Service"
accesschk.exe -uwcqv %USERNAME% *
```

```powershell
Get-Acl "C:\Path\To\ServiceFolder" | Format-List
```

**Procurar:** `SERVICE_CHANGE_CONFIG` / `WRITE_DAC`; Modify/FullControl no binário/pasta; `StartName` = LocalSystem; capacidade de restart/reboot.

Ferramentas de enum em lab: `accesschk` (Sysinternals), PowerUp, WinPEAS.

---

### 3. AlwaysInstallElevated

**Conceito:** Se **ambas** as chaves estão em `0x1`, MSI pode instalar com privilégios elevados — misconfig grave e rara, clássica em CTFs.

```cmd
reg query HKLM\SOFTWARE\Policies\Microsoft\Windows\Installer /v AlwaysInstallElevated
reg query HKCU\SOFTWARE\Policies\Microsoft\Windows\Installer /v AlwaysInstallElevated
```

⚠️ Não incluímos construção de MSI malicioso — foque em detectar e reportar.

---

### 4. Registro do serviço com ACL fraca
```
Teoria:
└─ Escrita em ImagePath / parâmetros + serviço SYSTEM = caminho de elevação.
```

```cmd
reg query HKLM\SYSTEM\CurrentControlSet\Services\SERVICENAME
```

Validar ACLs com accesschk / WinPEAS — não assumir escrita.

---

## 🎫 Token Privileges e Família "Potato" (Teoria)

### Tokens
Um **access token** descreve identidade, grupos e privilégios. Impersonation permite que um thread atue com o token de outro usuário.

```
Access Token:
├─ SID do usuário / grupos
├─ Privilegios (Se*)
├─ Integrity Level
└─ Tipo (Primary / Impersonation levels)
```

### SeImpersonate / SeAssignPrimaryToken

Muitos service accounts possuem `SeImpersonatePrivilege`. Em teoria, se o processo pode **forçar autenticação local privilegiada** e impersonar o token resultante, há caminho para SYSTEM.

```
Família "Potato" (overview educacional):
├─ Conceito: abuse de autenticação local + impersonation
├─ Variantes históricas: Rotten/Juicy/Sweet/GodPotato etc.
├─ Pré-condição típica: SeImpersonate (ou AssignPrimaryToken) + canal local
└─ Objetivo didático: tokens, pipes, NTLM local, coercion
```

⚠️ **Sem PoCs.** Em labs, use materiais oficiais da plataforma e documente pré-condições.

### Outros privilégios perigosos (teoria)
```
SeDebugPrivilege     → interagir com processos de outros (incl. SYSTEM)
SeBackup/Restore     → ler/escrever ignorando várias DACLs
SeTakeOwnership      → ownership + reescrever ACLs
SeLoadDriver         → carregar drivers (risco alto; lab only)
```

```cmd
whoami /priv
```

**Defesa:** reduzir SeImpersonate desnecessário; monitorar impersonation anômala e spawns SYSTEM; harden serviços coercíveis localmente.

---

## ⏰ Scheduled Tasks e Autoruns Abusáveis

Tasks podem rodar como SYSTEM/Admin. Binário/script gravável ou task modificável = vetor clássico.

```cmd
schtasks /query /fo LIST /v
schtasks /query /tn "TASKNAME" /fo LIST /v
reg query HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Run
reg query HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Run
dir "%ProgramData%\Microsoft\Windows\Start Menu\Programs\Startup"
dir "%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup"
```

```powershell
Get-ScheduledTask | Select-Object TaskName, TaskPath, State
Get-ScheduledTask | Where-Object {$_.Principal.UserId -match "SYSTEM|Administrator"} |
  Get-ScheduledTaskInfo
```

**Procurar:** actions em paths graváveis; `.bat/.ps1/.vbs` em pastas fracas; tasks de software de terceiros com ACLs ruins; triggers frequentes.

Ferramenta clássica: **Autoruns** (Sysinternals) — excelente para lab e defesa.

---

## 📦 DLL Hijacking — Overview

### Conceito
Processo privilegiado carrega DLL sem caminho absoluto seguro → ordem de busca do Windows. Se low-priv coloca DLL no local pesquisado **antes** da legítima, o código roda no contexto do processo.

```
Ideia (teoria):
App privilegiado → LoadLibrary("helper.dll")
└─ busca em diretórios graváveis? → risco de hijack
```

### Cenários educacionais
```
├─ App em path com pasta gravável por Users
├─ Missing DLL / phantom DLL / sideloading
└─ PATH ou CWD inseguro
```

### Enum (alto nível) e defesa
```
Labs: Procmon (Sysinternals), pastas WRITE para low-priv,
correlacionar com serviços/tasks que reiniciam.

Defesa: paths protegidos; ACLs corretas; caminhos absolutos;
SafeDllSearchMode; WDAC quando viável; monitorar DLLs em paths sensíveis.
```

⚠️ Construção de DLL maliciosa **não** entra neste guia.

---

## 🔑 Credential Leftovers (Perspectiva Educacional)

Credenciais residuais frequentemente **viram** PrivEsc sem bug de kernel.

### SAM / LSA — teoria
```
SAM  → hashes de contas locais
LSA / DPAPI / LSASS → segredos de serviço, cached creds, tickets, etc.
```

Dump de SAM/LSASS exige privilégios elevados ou condições especiais — em labs, costuma ser **após** Admin/SYSTEM (ou cenário específico autorizado).

```
Leitura educacional:
├─ Hash local ≠ senha em claro
├─ Cached domain logons podem existir no host
├─ DPAPI protege muitos segredos por usuário
└─ Ferramentas ofensivas: só em lab autorizado
```

### cmdkey e leftovers comuns
```cmd
cmdkey /list
dir /a %USERPROFILE%\Desktop
dir /a %USERPROFILE%\Documents
dir /s /b C:\Users\*password* 2>nul
reg query "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon" /v DefaultUserName
reg query "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon" /v AutoAdminLogon
```

```powershell
Get-ChildItem -Path C:\Users -Recurse -Include *.txt,*.xml,*.config,*.ini,*.ps1 -ErrorAction SilentlyContinue |
  Select-String -Pattern "password|passwd|pwd|connectionString" -ErrorAction SilentlyContinue |
  Select-Object -First 50
```

**Arquivos clássicos em CTFs:** `unattend.xml` / sysprep, `web.config`, scripts de deploy, Autologon no registro.

⚠️ Em engajamentos reais: minimize coleta, redija dados sensíveis no relatório.

---

## 🧩 Kernel / Drivers — Notas High Level

```
Quando entra em jogo:
├─ Host desatualizado / patches faltando
├─ Drivers de terceiros vulneráveis
└─ Outras vias de userland falharam

Riscos:
⚠️ BSOD / corrupção
⚠️ Em pentest: alinhar risco operacional com o cliente
⚠️ Em CTF: preferir misconfigs antes de kernel
```

```cmd
systeminfo
wmic qfe list brief
driverquery /v
```

```powershell
Get-HotFix
Get-CimInstance Win32_PnPSignedDriver |
  Select-Object DeviceName, DriverVersion, Manufacturer | Sort-Object Manufacturer
```

**Defesa:** patch management; HVCI / drivers assinados quando possível; reduzir drivers de terceiros; EDR com detecção de exploração de kernel.

Este guia **não** lista CVEs weaponizados nem passos de exploração.

---

## 📋 Checklist de Enumeração

```
Identidade e token:
[ ] whoami /all
[ ] whoami /priv (SeImpersonate, SeDebug, SeBackup, etc.)
[ ] Grupos locais e de domínio
[ ] Integrity Level / admin filtrado (UAC)?

Sistema:
[ ] systeminfo / build / arquitetura
[ ] Hotfixes / domínio vs workgroup
[ ] AV/EDR visível?

Serviços:
[ ] Unquoted paths
[ ] Weak ACLs (binário/pasta/serviço/registro)
[ ] AlwaysInstallElevated (HKLM + HKCU)
[ ] Serviços SYSTEM com paths suspeitos

Tasks / autoruns:
[ ] Tasks privilegiadas com paths graváveis
[ ] Run keys HKLM / Startup folders

Credenciais:
[ ] cmdkey /list
[ ] Configs / unattend / scripts / autologon
[ ] Shares locais interessantes

Outros:
[ ] Software desatualizado (lab)
[ ] Drivers / kernel só se necessário
[ ] Permissões em C:\, Program Files, ProgramData
```

---

## 🛠️ Ferramentas de Enumeração (Links Oficiais)

Use **somente** em labs autorizados. Prefira releases oficiais.

### WinPEAS (PEASS-ng)
```
https://github.com/peass-ng/PEASS-ng
```

```cmd
winPEASx64.exe
winPEASx64.exe quiet cmd searchfast
```

### Seatbelt (GhostPack)
```
https://github.com/GhostPack/Seatbelt
```

```cmd
Seatbelt.exe -group=system
Seatbelt.exe -group=user
Seatbelt.exe -group=all
```

### PowerUp (PowerSploit)
```
https://github.com/PowerShellMafia/PowerSploit
Nota: muitos ambientes detectam — use em lab isolado
```

```powershell
Import-Module .\PowerUp.ps1
Invoke-AllChecks
```

### Outras úteis
```
Sysinternals AccessChk / Autoruns / Procmon
https://learn.microsoft.com/sysinternals

SharpUp — https://github.com/GhostPack/SharpUp
Watson — https://github.com/rasta-mouse/Watson
wesng — https://github.com/bitsadmin/wesng
HackTricks Windows PrivEsc — https://book.hacktricks.xyz/windows-hardening/windows-local-privilege-escalation
LOLBAS — https://lolbas-project.github.io/
```

---

## 🧪 Labs Recomendados

### TryHackMe
```
Windows PrivEsc / Privilege Escalation rooms
└─ Enumeração guiada: serviços, tokens, UAC, creds
```
- [TryHackMe](https://tryhackme.com/) — busque rooms oficiais de **Windows Privilege Escalation**

### Hack The Box
```
Máquinas Windows easy/medium com PrivEsc local
└─ Documente: enum → finding → elevação ética
```
- [Hack The Box](https://www.hackthebox.com/)

### GOAD (Game of Active Directory)
```
Lab complexo de AD (múltiplos hosts Windows)
└─ PrivEsc local como etapa antes do domínio
└─ Une este guia + windows_lateral_movement_teoria.md
```
- [Orange-Cyberdefense / GOAD](https://github.com/Orange-Cyberdefense/GOAD)

### Boas práticas de lab
```
1. Snapshot antes de mudanças
2. Documentar enum e evidências
3. Preferir misconfigs a kernel crashes
4. Reverter alterações após o exercício
```

---

## 🛡️ Defesa / Hardening

```
Princípios:
├─ Least privilege (usuários e service accounts)
├─ Patch management contínuo
├─ Application control (WDAC/AppLocker) quando viável
├─ Credencial hygiene (sem senhas em scripts/autologon)
└─ Telemetria: Sysmon + EDR + auditoria de privilégios

Controles concretos:
[ ] Paths de serviço entre aspas; ACLs corretas
[ ] Contas de serviço com privilégios mínimos
[ ] Remover AlwaysInstallElevated
[ ] Não desabilitar UAC; evitar uso diário como Admin (JIT/PAM)
[ ] Reduzir SeImpersonate desnecessário
[ ] Credential Guard / LSA Protection / LAPS onde compatível
[ ] Auditar scheduled tasks privilegiadas
[ ] ACLs em ProgramData e pastas de app

Eventos (ponto de partida):
4624 / 4672 → logons e privilégios especiais
4688       → criação de processo
7045       → novo serviço
4698/4702  → scheduled tasks
Sysmon 1/7/11 → process / image load / file create
```

---

## 🎯 MITRE ATT&CK (Mapeamento Educacional)

Referência: [https://attack.mitre.org/](https://attack.mitre.org/)

| Técnica | ID | Relação com este guia |
|--------|----|------------------------|
| Abuse Elevation Control Mechanism | T1548 | UAC bypass concepts |
| Exploitation for Privilege Escalation | T1068 | Kernel/driver / software vulns (high level) |
| Valid Accounts | T1078 | Credenciais válidas / leftovers / reuso |
| Access Token Manipulation | T1134 | Impersonation, token privs, potato-class |
| Hijack Execution Flow | T1574 | DLL hijacking / path interception |
| Create or Modify System Process: Windows Service | T1543.003 | Serviços vulneráveis / weak perms |
| Scheduled Task/Job | T1053 | Tasks abusáveis |
| OS Credential Dumping | T1003 | SAM/LSASS theory (pós-elevação / lab) |
| Credentials from Password Stores | T1555 | Credential Manager / cmdkey |
| Boot or Logon Autostart Execution | T1547 | Autoruns / Run keys |

### Subtécnicas úteis
```
T1548.002  Bypass User Account Control
T1574.001  DLL Search Order Hijacking
T1574.010  Services File Permissions Weakness
T1574.011  Services Registry Permissions Weakness
T1053.005  Scheduled Task
T1003.001  LSASS Memory (teoria / defesa)
T1003.002  Security Account Manager (teoria / defesa)
T1134.001  Token Impersonation/Theft (conceito)
```

**No relatório:** finding → técnica ATT&CK → evidência de enum → impacto → remediação.

---

## 💡 Fluxo Mental Recomendado

```
1. whoami /all + systeminfo
2. Privs interessantes? (SeImpersonate / SeDebug / Backup...)
3. Serviços (unquoted, ACLs, AlwaysInstallElevated)
4. Tasks / autoruns com paths graváveis
5. Cred leftovers (cmdkey, configs, autologon)
6. DLL / app misconfig (Procmon em lab)
7. Patches / drivers (último recurso consciente)
8. Documentar + mapear ATT&CK + hardening
```

```
Dicas:
├─ 90% é encontrar; exploração vem depois (só com autorização)
├─ Evite kernel crashes sem snapshot
└─ Todo vetor achado deve virar recomendação de hardening
```

---

## 📚 Recursos

### Guias
- [HackTricks — Windows Local Privilege Escalation](https://book.hacktricks.xyz/windows-hardening/windows-local-privilege-escalation)
- [LOLBAS Project](https://lolbas-project.github.io/)
- [MITRE ATT&CK](https://attack.mitre.org/)
- [Microsoft Sysinternals](https://learn.microsoft.com/sysinternals)

### Ferramentas
- [PEASS-ng / WinPEAS](https://github.com/peass-ng/PEASS-ng)
- [Seatbelt](https://github.com/GhostPack/Seatbelt)
- [SharpUp](https://github.com/GhostPack/SharpUp)
- [PowerSploit (histórico)](https://github.com/PowerShellMafia/PowerSploit)

### Labs
- [TryHackMe](https://tryhackme.com/)
- [Hack The Box](https://www.hackthebox.com/)
- [GOAD](https://github.com/Orange-Cyberdefense/GOAD)

### Relacionado neste repo
- `06-Cheatsheets/linux_privesc_teoria.md`
- `06-Cheatsheets/windows_lateral_movement_teoria.md`
- `06-Cheatsheets/powershell_cheatsheet.md`

---

<div align="center">

**🪟 Enumeração é a chave**

*Entenda o token, mapeie misconfigs, eleve com ética — e endureça o que encontrar*

---

*Conteúdo educacional | Use apenas em ambientes autorizados*

</div>
