# 📋 Windows Event Logs - Guia Completo

> Análise de logs do Windows para detecção de atividades maliciosas e forense digital

---

## 📚 Introdução

**Windows Event Logs** são registros detalhados de atividades do sistema operacional, essenciais para análise forense e detecção de intrusões.

### Por que são importantes?
- 🔍 Detectar atividades maliciosas
- 📊 Investigar incidentes
- 🕵️ Rastrear comportamento de atacantes
- ⏰ Estabelecer timeline de eventos

---

## 📁 Localização dos Logs

```
Caminho no disco:
C:\Windows\System32\winevt\Logs\

Principais arquivos:
├─ Security.evtx (logs de segurança)
├─ System.evtx (eventos do sistema)
├─ Application.evtx (aplicações)
├─ PowerShell-Operational.evtx
└─ Microsoft-Windows-Sysmon-Operational.evtx (se Sysmon instalado)
```

---

## 🔑 Event IDs Críticos para Segurança

### Autenticação (Logon/Logoff)

| Event ID | Descrição | Importância |
|----------|-----------|-------------|
| **4624** | Logon bem-sucedido | ⭐⭐⭐ |
| **4625** | Falha de logon | ⭐⭐⭐ |
| **4634** | Logoff | ⭐⭐ |
| **4648** | Logon com credenciais explícitas | ⭐⭐⭐ |
| **4672** | Privilégios especiais atribuídos | ⭐⭐⭐ |

#### Event ID 4624 - Logon Types

```
Logon Type 2  : Interativo (console físico)
Logon Type 3  : Network (acesso remoto, shares)
Logon Type 4  : Batch (tarefas agendadas)
Logon Type 5  : Service (serviços)
Logon Type 7  : Unlock (desbloqueio de tela)
Logon Type 8  : NetworkCleartext (credenciais em texto claro!)
Logon Type 9  : NewCredentials (RunAs)
Logon Type 10 : RemoteInteractive (RDP)
Logon Type 11 : CachedInteractive (cached credentials)
```

**Red Flags:**
- Logon Type 10 de IPs incomuns (RDP suspeito)
- Logon Type 3 fora do horário comercial
- Múltiplos Event 4625 seguidos (brute force)

---

### Active Directory

| Event ID | Descrição | Uso |
|----------|-----------|-----|
| **4768** | Kerberos TGT solicitado | Kerberoasting detection |
| **4769** | Kerberos Service Ticket | Kerberoasting detection |
| **4771** | Kerberos pre-auth falhou | AS-REP Roasting |
| **4776** | NTLM authentication | Monitorar NTLM usage |

---

### Alterações de Objetos

| Event ID | Descrição | Importância |
|----------|-----------|-------------|
| **4720** | Conta de usuário criada | ⭐⭐⭐ |
| **4722** | Conta de usuário habilitada | ⭐⭐ |
| **4724** | Tentativa de reset de senha | ⭐⭐⭐ |
| **4728** | Membro adicionado a grupo | ⭐⭐⭐ |
| **4732** | Membro adicionado a grupo local | ⭐⭐⭐ |
| **4756** | Membro adicionado a grupo universal | ⭐⭐ |

---

### Processo e Serviços

| Event ID | Descrição | Importância |
|----------|-----------|-------------|
| **4688** | Novo processo criado | ⭐⭐⭐ |
| **4689** | Processo terminado | ⭐⭐ |
| **7045** | Novo serviço instalado | ⭐⭐⭐ |

**Configuração importante:**
```powershell
# Habilitar logging de linha de comando no Event 4688
# Computer Configuration → Policies → Administrative Templates → 
# System → Audit Process Creation → Include command line in process creation events
```

---

### PowerShell

| Event ID | Descrição | Log |
|----------|-----------|-----|
| **4103** | Module logging | PowerShell-Operational |
| **4104** | Script Block logging | PowerShell-Operational |
| **4105** | Script start | PowerShell-Operational |
| **4106** | Script stop | PowerShell-Operational |

---

## 🔍 Queries Úteis com PowerShell

### Buscar Event IDs Específicos

```powershell
# Buscar todos os logons bem-sucedidos (últimas 24h)
Get-WinEvent -FilterHashtable @{
    LogName='Security'
    ID=4624
    StartTime=(Get-Date).AddDays(-1)
}

# Falhas de logon (possível brute force)
Get-WinEvent -FilterHashtable @{
    LogName='Security'
    ID=4625
    StartTime=(Get-Date).AddHours(-1)
} | Group-Object {$_.Properties[5].Value} | Sort-Object Count -Descending

# RDP Logons
Get-WinEvent -FilterHashtable @{
    LogName='Security'
    ID=4624
} | Where-Object {$_.Properties[8].Value -eq 10}

# Processos criados
Get-WinEvent -FilterHashtable @{
    LogName='Security'
    ID=4688
    StartTime=(Get-Date).AddHours(-1)
} | Select-Object TimeCreated, @{n='Process';e={$_.Properties[5].Value}}
```

---

### Detectar Atividades Suspeitas

```powershell
# Kerberoasting detection (múltiplos TGS requests RC4)
Get-WinEvent -FilterHashtable @{
    LogName='Security'
    ID=4769
} | Where-Object {$_.Properties[7].Value -eq '0x17'} | Group-Object {$_.Properties[0].Value} | Where-Object {$_.Count -gt 10}

# Novos usuários criados
Get-WinEvent -FilterHashtable @{
    LogName='Security'
    ID=4720
    StartTime=(Get-Date).AddDays(-7)
}

# Adições a grupos privilegiados
Get-WinEvent -FilterHashtable @{
    LogName='Security'
    ID=4728,4732,4756
    StartTime=(Get-Date).AddDays(-7)
}

# PowerShell suspeito
Get-WinEvent -FilterHashtable @{
    LogName='Microsoft-Windows-PowerShell/Operational'
    ID=4104
} | Where-Object {$_.Message -match 'Invoke-|Download|IEX|Net.WebClient'}
```

---

## 🛠️ Ferramentas de Análise

### Event Viewer (Nativo)
```powershell
# Abrir Event Viewer
eventvwr.msc

# Filtrar por Event ID
# Right-click no log → Filter Current Log → Event IDs
```

### PowerShell
```powershell
# Get-WinEvent é mais rápido que Get-EventLog
Get-WinEvent -ListLog *

# Exportar para CSV
Get-WinEvent -LogName Security -MaxEvents 1000 | Export-Csv events.csv
```

### Sysmon (Sysinternals)

```powershell
# Instalar Sysmon
sysmon64.exe -accepteula -i sysmonconfig.xml

# Event IDs importantes do Sysmon:
# 1  : Process Creation
# 3  : Network Connection
# 7  : Image Loaded
# 8  : CreateRemoteThread
# 10 : ProcessAccess
# 11 : FileCreate
# 22 : DNS Query
```

---

## 🚨 Indicadores de Comprometimento (IOCs)

### Sinais de Pass-the-Hash
```
Event 4624 (Logon Type 3) com:
- Logon Process: NtLmSsp
- Package Name: NTLM
- Sem Event 4625 anterior
- De IPs internos inesperados
```

### Sinais de Kerberoasting
```
Múltiplos Event 4769:
- Ticket Encryption: 0x17 (RC4)
- Service Name: não é krbtgt
- Em curto período de tempo
- Do mesmo account
```

### Sinais de Golden Ticket
```
Event 4624 (Logon Type 3) com:
- Sem Event 4768 correspondente (TGT request)
- Lifetime do ticket incomum
- De contas privilegiadas
```

---

## 📊 Timeline de Ataque Típico

```
1. Reconhecimento
   └─ Event 5156 (Windows Filtering Platform)
   └─ Sysmon Event 22 (DNS Queries)

2. Initial Access
   └─ Event 4624 (Logon bem-sucedido)
   └─ Event 4648 (Explicit credentials)

3. Execution
   └─ Event 4688 (Process creation)
   └─ PowerShell Event 4104 (Script block)

4. Privilege Escalation
   └─ Event 4672 (Special privileges)
   └─ Event 4732 (Member added to local admin)

5. Lateral Movement
   └─ Event 4624 Type 3 (Network logon)
   └─ Event 4648 (RunAs)
   └─ Sysmon Event 3 (Network connection)

6. Persistence
   └─ Event 7045 (Service installed)
   └─ Event 4698 (Scheduled task created)

7. Exfiltration
   └─ Sysmon Event 3 (Connections para fora)
   └─ Event 5156 (Network connections)
```

---

## 💡 Dicas de Análise

### 1. Correlacione Eventos
Não analise eventos isoladamente. Exemplo:
```
Event 4625 (failed logon) → Event 4624 (success) = Possível brute force bem-sucedido
```

### 2. Baseline Normal
Estabeleça o que é normal no ambiente:
- Horários de logon
- IPs comuns
- Processos típicos

### 3. Foque em Anomalias
```
Red Flags:
├─ Logons fora do horário
├─ De IPs geograficamente distantes
├─ Processos iniciados de locais incomuns
├─ PowerShell codificado (Base64)
└─ Múltiplas falhas seguidas de sucesso
```

---

## 🔐 Hardening e Melhores Práticas

### Habilitar Audit Policies

```powershell
# Via GPO ou localmente
auditpol /set /subcategory:"Logon" /success:enable /failure:enable
auditpol /set /subcategory:"Process Creation" /success:enable
auditpol /set /subcategory:"Security Group Management" /success:enable
```

### PowerShell Logging

```powershell
# Habilitar Module Logging
Set-ItemProperty -Path "HKLM:\SOFTWARE\Policies\Microsoft\Windows\PowerShell\ModuleLogging" -Name "EnableModuleLogging" -Value 1

# Habilitar Script Block Logging
Set-ItemProperty -Path "HKLM:\SOFTWARE\Policies\Microsoft\Windows\PowerShell\ScriptBlockLogging" -Name "EnableScriptBlockLogging" -Value 1
```

### Aumentar Tamanho dos Logs

```powershell
# Evitar que logs importantes sejam sobrescritos
wevtutil sl Security /ms:1073741824  # 1GB
wevtutil sl "Microsoft-Windows-PowerShell/Operational" /ms:524288000  # 500MB
```

---

## 📚 Recursos Adicionais

### Ferramentas
- **Event Log Explorer** - Análise visual
- **Chainsaw** - Análise de logs do Windows
- **Hayabusa** - Timeline generation
- **EvtxECmd** - Eric Zimmerman Tools

### Documentação
- Microsoft Security Auditing
- MITRE ATT&CK Event IDs
- SANS DFIR Posters

---

<div align="center">

**📋 Logs são a memória do sistema**

*Saber ler logs é essencial para Blue Team e DFIR*

---

*Conteúdo educacional*

</div>
