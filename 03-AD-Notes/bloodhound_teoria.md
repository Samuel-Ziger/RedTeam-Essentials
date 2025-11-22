# 🩸 BloodHound - Teoria Completa

> Mapeamento visual de Active Directory para identificar attack paths e vulnerabilidades

---

## 📚 O que é BloodHound?

**BloodHound** é uma ferramenta de análise de Active Directory que usa teoria de grafos para revelar relacionamentos ocultos e caminhos de ataque (attack paths) dentro de ambientes AD.

### Por que BloodHound é poderoso?
- 🗺️ Mapeia visualmente toda a estrutura AD
- 🎯 Identifica caminhos para Domain Admin
- 🔍 Revela relações ocultas entre objetos
- 📊 Análise automatizada de ACLs
- ⚡ Processa milhões de objetos rapidamente

**Metáfora:** Se AD é uma cidade, BloodHound é o mapa que mostra todos os caminhos secretos para o banco central.

---

## 🏗️ Arquitetura do BloodHound

### Componentes Principais

```
┌─────────────────────────────────────────────┐
│           COLETA (Ingestors)                │
├─────────────────────────────────────────────┤
│ - SharpHound.exe (C#)                       │
│ - SharpHound.ps1 (PowerShell)               │
│ - AzureHound (Azure AD)                     │
└─────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────┐
│        ARMAZENAMENTO (Database)             │
├─────────────────────────────────────────────┤
│ - Neo4j (Graph Database)                    │
│ - Armazena nodes e edges                    │
└─────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────┐
│       VISUALIZAÇÃO (Interface)              │
├─────────────────────────────────────────────┤
│ - BloodHound GUI (Electron app)             │
│ - Cypher queries                            │
│ - Análise de caminhos                       │
└─────────────────────────────────────────────┘
```

---

## 🗂️ Conceitos Fundamentais

### Nodes (Nós)

**Nodes** representam objetos no Active Directory:

```
Tipos de Nodes:
├─ 👤 User (Usuário)
├─ 💻 Computer (Computador)
├─ 👥 Group (Grupo)
├─ 🏢 Domain (Domínio)
├─ 🌲 GPO (Group Policy Object)
├─ 📁 OU (Organizational Unit)
└─ 🎫 Container
```

---

### Edges (Arestas)

**Edges** representam relacionamentos e permissões entre nodes:

```
Tipos de Edges (Relações):
├─ MemberOf (pertence ao grupo)
├─ AdminTo (administrador de)
├─ HasSession (tem sessão em)
├─ TrustedBy (confiado por)
├─ CanRDP (pode RDP em)
├─ CanPSRemote (pode usar PSRemoting)
├─ GenericAll (controle total sobre)
├─ GenericWrite (pode modificar)
├─ WriteOwner (pode mudar dono)
├─ WriteDACL (pode modificar ACL)
├─ AddMember (pode adicionar membros)
├─ ForceChangePassword (pode forçar mudança de senha)
├─ AllExtendedRights (todos os direitos estendidos)
└─ ... e muitos outros
```

---

### Attack Paths

**Attack Path** é uma sequência de edges que leva de um node inicial até um alvo de alto valor.

**Exemplo:**
```
Você (User)
    ↓ MemberOf
Grupo_TI (Group)
    ↓ AdminTo
Servidor_X (Computer)
    ↓ HasSession
Domain_Admin (User)
    ↓ MemberOf
Domain Admins (Group)
```

---

## 🔧 Instalação e Configuração

### 1. Instalar Neo4j

#### Windows
```powershell
# Baixar Neo4j Community Edition
# https://neo4j.com/download-center/

# Extrair e iniciar
.\neo4j.bat console

# Acessar interface web
# http://localhost:7474

# Login padrão:
# Usuário: neo4j
# Senha: neo4j
# (será solicitado mudar na primeira vez)
```

#### Linux
```bash
# Instalar Java
sudo apt update
sudo apt install openjdk-11-jre

# Baixar e instalar Neo4j
wget -O - https://debian.neo4j.com/neotechnology.gpg.key | sudo apt-key add -
echo 'deb https://debian.neo4j.com stable latest' | sudo tee /etc/apt/sources.list.d/neo4j.list
sudo apt update
sudo apt install neo4j

# Iniciar serviço
sudo neo4j start

# Acessar http://localhost:7474
```

---

### 2. Instalar BloodHound

```powershell
# Baixar do GitHub
# https://github.com/BloodHoundAD/BloodHound/releases

# Executar (Windows)
.\BloodHound.exe

# Conectar ao Neo4j
Database URL: bolt://localhost:7687
Username: neo4j
Password: [sua senha]
```

---

### 3. Download SharpHound

```powershell
# SharpHound.exe (compilado)
# https://github.com/BloodHoundAD/BloodHound/tree/master/Collectors

# SharpHound.ps1 (PowerShell)
IEX (New-Object Net.WebClient).DownloadString('https://raw.githubusercontent.com/BloodHoundAD/BloodHound/master/Collectors/SharpHound.ps1')
```

---

## 📊 Coletando Dados (Ingestão)

### Usando SharpHound.exe

```powershell
# Coleta padrão (recomendado)
.\SharpHound.exe -c All

# Opções de coleta específicas
.\SharpHound.exe -c DCOnly          # Apenas do Domain Controller
.\SharpHound.exe -c Group           # Apenas grupos
.\SharpHound.exe -c Session         # Apenas sessões
.\SharpHound.exe -c LocalAdmin      # Apenas administradores locais
.\SharpHound.exe -c LoggedOn        # Apenas usuários logados
.\SharpHound.exe -c Trusts          # Apenas trusts
.\SharpHound.exe -c ACL             # Apenas ACLs
.\SharpHound.exe -c Container       # Apenas containers
.\SharpHound.exe -c GPO             # Apenas GPOs
.\SharpHound.exe -c ObjectProps     # Propriedades de objetos

# Combinar métodos
.\SharpHound.exe -c Group,LocalAdmin,Session

# Especificar domínio
.\SharpHound.exe -c All -d exemplo.local

# Loop de coleta (para capturar sessões variáveis)
.\SharpHound.exe -c All --Loop --LoopDuration 02:00:00  # 2 horas
```

---

### Usando SharpHound.ps1 (PowerShell)

```powershell
# Importar módulo
Import-Module .\SharpHound.ps1

# Executar coleta
Invoke-BloodHound -CollectionMethod All

# Com opções
Invoke-BloodHound -CollectionMethod All -Domain exemplo.local -OutputDirectory C:\Temp

# Métodos específicos
Invoke-BloodHound -CollectionMethod Session,Group
```

---

### Outputs da Coleta

```
Arquivos gerados:
├─ 20250122_BloodHound.zip (arquivo principal)
│  ├─ computers.json
│  ├─ users.json
│  ├─ groups.json
│  ├─ domains.json
│  ├─ gpos.json
│  └─ containers.json
└─ 20250122_BloodHound_timestamp.cache (cache)
```

---

## 📥 Importando Dados no BloodHound

### Passo a Passo

```
1. Abrir BloodHound GUI
2. Conectar ao Neo4j
3. Clicar em "Upload Data" (ícone de upload no lado direito)
4. Selecionar arquivo .zip gerado pelo SharpHound
5. Aguardar importação
6. Dados aparecerão no Database Info
```

### Via Linha de Comando (alternativo)

```bash
# Usando Neo4j Cypher Shell
cypher-shell -u neo4j -p senha < import_script.cypher
```

---

## 🔍 Análise com BloodHound

### Interface Principal

```
BloodHound UI:
├─ Search Bar (barra de pesquisa)
│  └─ Buscar nodes por nome
├─ Database Info (painel esquerdo)
│  ├─ Users count
│  ├─ Groups count
│  ├─ Computers count
│  └─ Etc.
├─ Node Info (quando seleciona um node)
│  ├─ Properties
│  ├─ Inbound/Outbound edges
│  └─ Info de segurança
├─ Graph View (visualização central)
│  └─ Representação visual dos caminhos
└─ Pre-Built Queries (queries prontas)
```

---

### Pre-Built Queries (Análises Prontas)

#### Domain Information
```
1. Find all Domain Admins
   └─ Mostra todos os Domain Admins

2. Find Shortest Paths to Domain Admins
   └─ Caminhos mais curtos para se tornar DA

3. Find Principals with DCSync Rights
   └─ Quem pode fazer DCSync
```

#### Dangerous Rights
```
4. Users with Foreign Domain Group Membership
   └─ Usuários em outros domínios

5. Groups with Foreign Domain Group Membership
   └─ Grupos com membros de outros domínios

6. Shortest Paths to High Value Targets
   └─ Caminhos para alvos importantes
```

#### Kerberos
```
7. List all Kerberoastable Accounts
   └─ Contas vulneráveis a Kerberoasting

8. Find Kerberoastable Members of High Value Groups
   └─ Membros kerberoastable de grupos importantes

9. Shortest Paths to Unconstrained Delegation Systems
   └─ Caminhos para sistemas com delegação irrestrita
```

---

### Cypher Queries Personalizadas

**Cypher** é a linguagem de query do Neo4j.

#### Queries Úteis

```cypher
// 1. Encontrar usuários com AdminCount=1
MATCH (u:User {admincount:true}) RETURN u

// 2. Encontrar computadores onde Domain Admins tem sessão
MATCH (u:User)-[:MemberOf*1..]->(g:Group {name:"DOMAIN ADMINS@EXEMPLO.LOCAL"})
MATCH (c:Computer)-[:HasSession]->(u)
RETURN c

// 3. Usuários com caminho para Domain Admins
MATCH p=shortestPath((u:User)-[*1..]->(g:Group {name:"DOMAIN ADMINS@EXEMPLO.LOCAL"}))
RETURN p

// 4. Todos os caminhos de um usuário específico para DA
MATCH p=(u:User {name:"JOAO@EXEMPLO.LOCAL"})-[*1..]->(g:Group {name:"DOMAIN ADMINS@EXEMPLO.LOCAL"})
RETURN p

// 5. Computadores com Unconstrained Delegation
MATCH (c:Computer {unconstraineddelegation:true}) RETURN c

// 6. Usuários que podem forçar mudança de senha
MATCH p=(u:User)-[:ForceChangePassword]->(u2:User)
RETURN p

// 7. Usuários com GenericAll sobre grupos
MATCH p=(u:User)-[:GenericAll]->(g:Group)
RETURN p

// 8. Computadores onde você é admin local
MATCH p=(u:User {name:"VOCE@EXEMPLO.LOCAL"})-[:AdminTo]->(c:Computer)
RETURN p

// 9. SPNs (Kerberoastable)
MATCH (u:User {hasspn:true}) RETURN u

// 10. Usuários que nunca fazem logon
MATCH (u:User {enabled:true})
WHERE u.lastlogon < (datetime().epochseconds - (90 * 86400))
RETURN u
```

---

## 🎯 Identificando Attack Paths

### Cenário Típico

```
Situação Inicial:
└─ Você tem credenciais de: joao@exemplo.local

Objetivo:
└─ Tornar-se Domain Admin
```

### Passo a Passo no BloodHound

```
1. Buscar seu usuário
   └─ Search: "joao@exemplo.local"
   └─ Right-click → Mark User as Owned

2. Buscar Domain Admins
   └─ Search: "Domain Admins@exemplo.local"
   └─ Right-click → Mark Group as High Value

3. Executar query
   └─ Pre-Built Queries → "Shortest Paths from Owned Principals"
   
4. Analisar caminho mostrado
   └─ Exemplo:
       JOAO@EXEMPLO.LOCAL
           ↓ MemberOf
       IT-SUPPORT@EXEMPLO.LOCAL
           ↓ GenericAll
       BACKUP-ADMINS@EXEMPLO.LOCAL
           ↓ MemberOf
       DOMAIN ADMINS@EXEMPLO.LOCAL
       
5. Explorar cada edge
   └─ Clicar em cada relação para ver como explorar
```

---

## 🔓 Explorando Edges Comuns

### GenericAll (Controle Total)

```
Se você tem GenericAll sobre um objeto, você pode:

Sobre User:
├─ Forçar mudança de senha
├─ Adicionar SPN (Kerberoast)
├─ Modificar propriedades
└─ Modificar ACLs

Sobre Group:
├─ Adicionar membros
├─ Remover membros
└─ Modificar propriedades

Sobre Computer:
├─ RBCD (Resource-Based Constrained Delegation)
├─ Modificar msDS-AllowedToActOnBehalfOfOtherIdentity
└─ Shadow Credentials attack
```

**Como explorar:**
```powershell
# Adicionar-se a um grupo
net group "Backup Admins" joao /add /domain

# Ou com PowerView
Add-DomainGroupMember -Identity 'Backup Admins' -Members 'joao'
```

---

### WriteDACL (Modificar ACL)

```
Se você tem WriteDACL:
└─ Pode conceder a si mesmo qualquer permissão
```

**Como explorar:**
```powershell
# Importar PowerView
Import-Module .\PowerView.ps1

# Conceder GenericAll a si mesmo
Add-DomainObjectAcl -TargetIdentity "alvo" -PrincipalIdentity "voce" -Rights All
```

---

### ForceChangePassword

```
Se você tem ForceChangePassword:
└─ Pode redefinir senha sem saber a atual
```

**Como explorar:**
```powershell
# PowerShell nativo
Set-ADAccountPassword -Identity "usuario_alvo" -Reset -NewPassword (ConvertTo-SecureString -AsPlainText "NovaSenh@123" -Force)

# PowerView
Set-DomainUserPassword -Identity "usuario_alvo" -AccountPassword (ConvertTo-SecureString 'NovaSenh@123' -AsPlainText -Force)
```

---

### AddMember (Adicionar Membros)

```
Se você tem AddMember sobre um grupo:
└─ Pode se adicionar ao grupo
```

**Como explorar:**
```powershell
net group "Domain Admins" joao /add /domain

# PowerView
Add-DomainGroupMember -Identity 'Domain Admins' -Members 'joao'
```

---

## 🛡️ Defesa e Mitigação

### Hardening AD

```
Medidas Preventivas:
├─ Implementar Tiered Admin Model
│  └─ Tier 0: Domain Controllers
│  └─ Tier 1: Servidores
│  └─ Tier 2: Workstations
│
├─ Remover permissões desnecessárias
│  └─ Auditar ACLs regularmente
│  └─ Princípio do menor privilégio
│
├─ Configurar Admin Tiers corretamente
│  └─ DAs não fazem logon em workstations
│  └─ Usar PAWs (Privileged Access Workstations)
│
├─ Monitorar delegações
│  └─ Evitar Unconstrained Delegation
│  └─ Usar Constrained Delegation ou RBCD
│
└─ Protected Users Group
   └─ Adicionar usuários privilegiados
   └─ Previne delegação e downgrade de encryption
```

---

### Usando BloodHound como Blue Team

```
Análises Defensivas:
1. Identificar caminhos de ataque ANTES dos atacantes
2. Auditar ACLs problemáticas
3. Encontrar delegações perigosas
4. Mapear onde admins fazem logon
5. Identificar stale accounts
6. Verificar grupos aninhados (nested)
```

#### Queries Defensivas

```cypher
// Encontrar usuários com caminhos curtos para DA
MATCH p=shortestPath((u:User)-[*1..3]->(g:Group {name:"DOMAIN ADMINS@EXEMPLO.LOCAL"}))
WHERE u.enabled = true
RETURN p

// Computadores com delegação irrestrita
MATCH (c:Computer {unconstraineddelegation:true})
WHERE c.enabled = true
RETURN c

// Usuários com AdminCount mas não em grupos protegidos
MATCH (u:User {admincount:true})
WHERE NOT (u)-[:MemberOf*1..]->(:Group {name:"DOMAIN ADMINS@EXEMPLO.LOCAL"})
RETURN u

// Objetos com ACLs modificáveis por todos
MATCH p=(g:Group {name:"DOMAIN USERS@EXEMPLO.LOCAL"})-[:GenericAll|WriteDACL|WriteOwner]->(n)
RETURN p
```

---

## 📊 Custom Queries Avançadas

### Análise de Sessões

```cypher
// Onde Domain Admins estão logados
MATCH (u:User)-[:MemberOf*1..]->(g:Group {name:"DOMAIN ADMINS@EXEMPLO.LOCAL"})
MATCH (c:Computer)-[:HasSession]->(u)
RETURN u.name AS Admin, COLLECT(c.name) AS ComputersWithSession

// Usuários logados em múltiplos computadores (possível admin)
MATCH (c:Computer)-[:HasSession]->(u:User)
WITH u, COUNT(c) AS SessionCount
WHERE SessionCount > 5
RETURN u.name, SessionCount
ORDER BY SessionCount DESC
```

---

### Análise de Grupos

```cypher
// Grupos com mais de 100 membros
MATCH (g:Group)
WITH g, SIZE((g)<-[:MemberOf]-()) AS MemberCount
WHERE MemberCount > 100
RETURN g.name, MemberCount
ORDER BY MemberCount DESC

// Nested groups (grupos dentro de grupos)
MATCH p=(g1:Group)-[:MemberOf*2..]->(g2:Group)
RETURN p
```

---

### Análise de Kerberos

```cypher
// Todos os SPNs
MATCH (u:User {hasspn:true})
RETURN u.name, u.serviceprincipalnames

// Kerberoastable members de grupos privilegiados
MATCH (u:User {hasspn:true})
MATCH (u)-[:MemberOf*1..]->(g:Group)
WHERE g.highvalue = true
RETURN u.name, g.name
```

---

## 💡 Dicas e Truques

### Para Red Team

```
1. Sempre colete sessões
   └─ Loop de coleta durante horas para capturar mais sessões

2. Mark owned principals
   └─ Facilita encontrar próximos passos

3. Use Custom Queries
   └─ Adapte para seu cenário específico

4. Combine com outras ferramentas
   └─ BloodHound + PowerView + Rubeus

5. Exporte attack paths
   └─ Screenshot para documentação
```

---

### Para Blue Team

```
1. Execute BloodHound regularmente
   └─ Identifique problemas antes dos atacantes

2. Use PlumHound
   └─ Gera relatórios automatizados do BloodHound

3. Corrija ACLs problemáticas
   └─ Use Remove-DomainObjectAcl (PowerView)

4. Monitore mudanças em ACLs
   └─ Event ID 5136, 4662

5. Implemente Tiering
   └─ Separe administrativamente por tiers
```

---

## 🔧 Ferramentas Relacionadas

| Ferramenta | Descrição | Uso |
|------------|-----------|-----|
| **PlumHound** | Relatórios automatizados | Defesa |
| **BARK** | BloodHound Attack Research Kit | Pesquisa |
| **AzureHound** | BloodHound para Azure AD | Cloud |
| **SharpHound** | Coletor de dados | Coleta |
| **Max** | BloodHound extendido | Análise |

---

## 🎓 Recursos de Aprendizado

### Labs Práticos

```
HackTheBox:
├─ Forest (fácil)
├─ Sauna (fácil)
├─ Resolute (médio)
└─ BlackField (difícil)

TryHackMe:
├─ Attacktive Directory
├─ Post-Exploitation Basics
└─ Holo
```

---

### Documentação Oficial

- [BloodHound Docs](https://bloodhound.readthedocs.io/)
- [SharpHound GitHub](https://github.com/BloodHoundAD/SharpHound)
- [Cypher Query Language](https://neo4j.com/docs/cypher-manual/)

---

### Blogs Essenciais

- **SpecterOps Blog** - Criadores do BloodHound
- **harmj0y's Blog** - Will Schroeder
- **wald0's Blog** - Andy Robbins
- **_ropnop blog** - Ropnop

---

## 🚨 Detecção de BloodHound

### Como detectar SharpHound

```
Sinais de execução:
├─ Múltiplas queries LDAP em curto período
├─ Enumeração de ACLs (Event 4662)
├─ Queries para "objectClass=*"
├─ Processos: SharpHound.exe
├─ Network traffic para DCs intensivo
└─ Arquivos .zip/.json com naming pattern específico
```

### Event IDs Importantes

```
- Event 4662: Operation performed on object
- Event 4661: Handle to an object requested
- Event 4624: Logon (muitos em curto período)
- Event 4634: Logoff
```

---

<div align="center">

**🩸 BloodHound revela o invisível no Active Directory**

*"Know your network better than the attackers do"*

---

*Para Red Team: Encontre o caminho*

*Para Blue Team: Feche o caminho*

---

*Conteúdo educacional | Use apenas em ambientes autorizados*

</div>
