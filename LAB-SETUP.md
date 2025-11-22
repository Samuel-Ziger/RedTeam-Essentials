# 🧪 Guia de Configuração de Laboratório

> **Setup completo de ambiente seguro para prática de Red Team**

Este guia fornece instruções detalhadas para configurar um ambiente de laboratório seguro e isolado para praticar técnicas de Red Team de forma ética e legal.

---

## ⚠️ AVISO CRÍTICO DE SEGURANÇA

```
🔒 ISOLAMENTO É ESSENCIAL

NUNCA pratique técnicas de Red Team em:
❌ Ambientes de produção
❌ Redes corporativas sem autorização
❌ Sistemas de terceiros
❌ Infraestrutura compartilhada

SEMPRE pratique em:
✅ Máquinas virtuais isoladas
✅ Redes privadas sem acesso à internet (quando possível)
✅ Ambientes CTF autorizados
✅ Plataformas de treinamento legais

O uso não autorizado pode resultar em:
- Violação de leis (Lei Carolina Dieckmann, LGPD, Computer Fraud and Abuse Act)
- Processo criminal
- Perda de emprego
- Danos à reputação profissional
```

---

## 📋 Visão Geral

### Tipos de Laboratório

```
┌─────────────────────────────────────────────────────────┐
│ Nível 1: Lab Local (Iniciante)                          │
│ └─ VM única com ferramentas instaladas                  │
│                                                          │
│ Nível 2: Lab Multi-VM (Intermediário)                   │
│ └─ Múltiplas VMs simulando rede corporativa             │
│                                                          │
│ Nível 3: Lab Active Directory (Avançado)                │
│ └─ Ambiente AD completo com DC, workstations, servers   │
│                                                          │
│ Nível 4: Labs Online (Todos os níveis)                  │
│ └─ Plataformas cloud de treinamento                     │
└─────────────────────────────────────────────────────────┘
```

---

## 🖥️ Nível 1: Lab Local Básico

### Requisitos de Hardware

**Mínimo:**
- CPU: 4 cores (Intel i5/AMD Ryzen 5)
- RAM: 8 GB
- Storage: 50 GB SSD livre
- Virtualização: Intel VT-x ou AMD-V habilitado na BIOS

**Recomendado:**
- CPU: 8+ cores (Intel i7/AMD Ryzen 7)
- RAM: 16+ GB
- Storage: 256 GB SSD NVMe
- GPU: Não necessária (exceto para password cracking)

### Software Base

#### 1. Hypervisor (escolha um)

**VMware Workstation Pro/Player** (Recomendado)
- Download: https://www.vmware.com/products/workstation-player.html
- Licença: Grátis (Player) / Pago (Pro)
- Prós: Performance superior, snapshots, cloning
- Contras: Versão free limitada

**VirtualBox** (Alternativa gratuita)
- Download: https://www.virtualbox.org/
- Licença: GPL (grátis e open-source)
- Prós: Totalmente gratuito, multi-plataforma
- Contras: Performance ligeiramente inferior

**Hyper-V** (Windows nativo)
- Incluído no Windows 10/11 Pro
- Comando: `Enable-WindowsOptionalFeature -Online -FeatureName Microsoft-Hyper-V -All`
- Prós: Integração nativa com Windows
- Contras: Não disponível em Home edition

#### 2. Sistema Operacional para Red Team

**Kali Linux** (Principal)
- Download: https://www.kali.org/get-kali/
- Versão: VM pré-configurada (recomendado)
- Credenciais padrão: `kali` / `kali`
- Ferramentas: 600+ pré-instaladas

```bash
# Após instalação, atualizar
sudo apt update && sudo apt full-upgrade -y
sudo apt install -y kali-linux-large

# Configurar ferramentas essenciais
sudo apt install -y bloodhound neo4j crackmapexec impacket-scripts \
                    responder proxychains4 chisel ligolo-ng
```

**Parrot Security OS** (Alternativa)
- Download: https://www.parrotsec.org/
- Foco: Privacidade + Pentesting
- Mais leve que Kali

**Commando VM** (Windows-based)
- Repositório: https://github.com/mandiant/commando-vm
- Descrição: Windows 10 com ferramentas de Red Team
- Uso: Ataques específicos de Windows

#### 3. Máquinas Vulneráveis para Prática

**Metasploitable 3**
- Download: https://github.com/rapid7/metasploitable3
- Descrição: Linux/Windows intencionalmente vulneráveis
- Uso: Prática de exploração

**DVWA (Damn Vulnerable Web Application)**
- Site: https://dvwa.co.uk/
- Instalação: Docker ou manual
```bash
docker run --rm -it -p 80:80 vulnerables/web-dvwa
```

**WebGoat**
- Repositório: https://github.com/WebGoat/WebGoat
- Foco: Vulnerabilidades web (OWASP Top 10)

---

## 🏢 Nível 2: Lab Multi-VM

### Arquitetura Recomendada

```
┌────────────────────────────────────────────────────────┐
│                 Red Team Lab Network                    │
│                                                         │
│  ┌──────────────┐         ┌──────────────┐            │
│  │  Kali Linux  │◄───────►│  Router/FW   │            │
│  │ (Attacker)   │         │  (pfSense)   │            │
│  └──────────────┘         └──────┬───────┘            │
│                                   │                     │
│                    ┌──────────────┼──────────────┐     │
│                    │              │              │     │
│           ┌────────▼───┐  ┌──────▼────┐  ┌─────▼────┐│
│           │ Windows 10 │  │ Win Server│  │  Linux   ││
│           │ (Client)   │  │ (Target)  │  │ (Target) ││
│           └────────────┘  └───────────┘  └──────────┘│
│                                                         │
│  Network: 192.168.100.0/24 (NAT/Host-Only)            │
└────────────────────────────────────────────────────────┘
```

### Configuração Passo a Passo

#### VM 1: Kali Linux (Atacante)
```
CPU: 2 cores
RAM: 4 GB
Disk: 40 GB
Network: Host-Only (192.168.100.10/24)
```

#### VM 2: Windows 10 (Alvo - Cliente)
```
CPU: 2 cores
RAM: 4 GB
Disk: 50 GB
Network: Host-Only (192.168.100.20/24)
Configuração: Defender desabilitado (lab only)
```

#### VM 3: Windows Server 2019 (Alvo - Servidor)
```
CPU: 2 cores
RAM: 4 GB
Disk: 60 GB
Network: Host-Only (192.168.100.30/24)
Serviços: IIS, SMB, RDP habilitados
```

#### VM 4: Ubuntu Server (Alvo - Linux)
```
CPU: 2 cores
RAM: 2 GB
Disk: 20 GB
Network: Host-Only (192.168.100.40/24)
Serviços: SSH, Apache, MySQL
```

### Script de Configuração Rápida

**VMware:**
```bash
# Clone VMs automaticamente
vmrun clone "/path/to/base.vmx" "/path/to/new.vmx" full
```

**VirtualBox:**
```bash
# Clone de VM
VBoxManage clonevm "BaseVM" --name "Target1" --register
VBoxManage modifyvm "Target1" --nic1 hostonly --hostonlyadapter1 "vboxnet0"
```

---

## 🏰 Nível 3: Active Directory Lab

### Por que um AD Lab?

- Simula ambiente corporativo real
- Pratica ataques avançados (Kerberoasting, Golden Ticket)
- Entende relações de confiança e delegação
- Essencial para certificações (OSCP, CRTP)

### Projetos Prontos de AD Lab

#### GOAD (Game of Active Directory) ⭐ Recomendado
- Repositório: https://github.com/Orange-Cyberdefense/GOAD
- Descrição: 5 domínios, 11 servidores, vulnerabilidades reais
- Deployment: Terraform + Ansible (automático)
- Requisitos: 60 GB RAM

```bash
# Instalação
git clone https://github.com/Orange-Cyberdefense/GOAD.git
cd GOAD/ansible
ansible-playbook main.yml
```

#### Microsoft Evaluation Center
- Link: https://www.microsoft.com/en-us/evalcenter/
- Download: Windows Server 2022 (trial 180 dias)
- Uso: Criar AD manualmente

**Setup Manual Básico:**

```powershell
# VM1: Domain Controller (Windows Server 2022)
# Instalar AD DS
Install-WindowsFeature AD-Domain-Services -IncludeManagementTools

# Promover a DC
Install-ADDSForest `
  -DomainName "lab.local" `
  -DomainNetbiosName "LAB" `
  -ForestMode "WinThreshold" `
  -DomainMode "WinThreshold" `
  -InstallDns:$true `
  -SafeModeAdministratorPassword (ConvertTo-SecureString "P@ssw0rd!" -AsPlainText -Force) `
  -Force:$true

# Criar usuários vulneráveis
New-ADUser -Name "SQL Service" -SamAccountName "sqlsvc" `
  -UserPrincipalName "sqlsvc@lab.local" `
  -AccountPassword (ConvertTo-SecureString "MYpassword123#" -AsPlainText -Force) `
  -Enabled $true

# Configurar SPN para Kerberoasting
setspn -A MSSQLSvc/sql.lab.local:1433 lab\sqlsvc
```

#### BadBlood
- Repositório: https://github.com/davidprowe/BadBlood
- Descrição: Popula AD com milhares de objetos
- Uso: Testar ferramentas de enumeração em escala

```powershell
# Executar no DC
Invoke-BadBlood -UsersPerGroup 5 -NumberOfGroups 100
```

---

## ☁️ Nível 4: Plataformas Online Gratuitas

### TryHackMe (Recomendado para Iniciantes)
- **Site:** https://tryhackme.com/
- **Custo:** Grátis (com limitações) / $10/mês (Premium)
- **Conteúdo:**
  - Rooms guiados passo a passo
  - Learning paths estruturados (Red Teaming, Web, AD)
  - Máquinas vulneráveis online
  - Certificados de conclusão

**Rooms Recomendados:**
```
Iniciante:
- Linux Fundamentals (1, 2, 3)
- Windows Fundamentals (1, 2, 3)
- Nmap, Metasploit, Burp Suite

Intermediário:
- Attacking Kerberos
- Active Directory Basics
- Lateral Movement and Pivoting

Avançado:
- Wreath Network
- Holo (Red Team simulated engagement)
```

**Setup:**
```bash
# Conectar via OpenVPN
sudo openvpn /path/to/tryhackme.ovpn
```

---

### HackTheBox
- **Site:** https://www.hackthebox.com/
- **Custo:** Grátis (máquinas retiradas) / $20/mês (VIP)
- **Conteúdo:**
  - Máquinas realistas (Easy → Insane)
  - Pro Labs (simulação de redes corporativas)
  - Challenges (Crypto, Forensics, Web)

**Níveis:**
```
Easy: Bom para começar
Medium: Requer conhecimento sólido
Hard: Múltiplas etapas, pivoting
Insane: Simulação de red team real
```

**Pro Labs Recomendados:**
- **Dante:** Network pivoting, AD básico ($90)
- **Offshore:** Múltiplos domínios AD, evasion ($150)
- **RastaLabs:** Red Team completo ($150)

---

### OWASP Juice Shop
- **Site:** https://owasp.org/www-project-juice-shop/
- **Repositório:** https://github.com/juice-shop/juice-shop
- **Foco:** Vulnerabilidades Web (OWASP Top 10)

**Deploy Local:**
```bash
# Docker (mais fácil)
docker run -d -p 3000:3000 bkimminich/juice-shop

# Ou Node.js
git clone https://github.com/juice-shop/juice-shop.git
cd juice-shop
npm install
npm start
```

**Acesso:** http://localhost:3000

---

### WebGoat e WebWolf
- **Site:** https://owasp.org/www-project-webgoat/
- **Foco:** Treinamento interativo de AppSec

```bash
# Docker
docker run -d -p 8080:8080 -p 9090:9090 webgoat/webgoat
```

**Acesso:**
- WebGoat: http://localhost:8080/WebGoat
- WebWolf: http://localhost:9090/WebWolf

---

### PortSwigger Web Security Academy
- **Site:** https://portswigger.net/web-security
- **Custo:** 100% Gratuito
- **Conteúdo:**
  - Labs práticos para cada vulnerabilidade
  - Teoria detalhada
  - Integração com Burp Suite

**Tópicos:**
- SQL Injection
- XSS (Cross-Site Scripting)
- CSRF, SSRF, XXE
- Authentication, Authorization
- Deserialization

---

### VulnHub
- **Site:** https://www.vulnhub.com/
- **Descrição:** VMs vulneráveis para download
- **Custo:** Grátis

**Como Usar:**
```bash
# Download de VM
wget https://download.vulnhub.com/machine/machine.ova

# Importar no VirtualBox/VMware
VBoxManage import machine.ova
```

**Máquinas Recomendadas:**
```
Iniciante:
- Mr-Robot 1
- Basic Pentesting 1 & 2
- Kioptrix Level 1

Intermediário:
- Stapler
- DC Series (DC-1 a DC-9)
- VulnOS 2

Avançado:
- HackLAB: Vulnix
- SickOs 1.2
```

---

### PentesterLab
- **Site:** https://pentesterlab.com/
- **Custo:** Grátis (básico) / $20/mês (Pro)
- **Foco:** Web exploitation, privilege escalation

---

### Root-Me
- **Site:** https://www.root-me.org/
- **Custo:** Grátis
- **Conteúdo:** Challenges categorizados (Web, Cracking, Forensics)

---

### PicoCTF
- **Site:** https://picoctf.org/
- **Descrição:** CTF educacional (Carnegie Mellon)
- **Custo:** Grátis

---

### CyberDefenders
- **Site:** https://cyberdefenders.org/
- **Foco:** Blue Team / DFIR
- **Uso:** Entender perspectiva defensiva

---

## 🛡️ Configurações de Segurança do Lab

### Isolamento de Rede

#### VMware: Host-Only Network
```
1. Edit → Virtual Network Editor
2. Add Network → VMnet2 (Host-only)
3. Subnet: 192.168.100.0/24
4. Desmarcar "Connect a host virtual adapter"
```

#### VirtualBox: Internal Network
```
1. Configurações da VM → Rede
2. Attached to: Internal Network
3. Name: redteam_lab
```

### Snapshots (Pontos de Restauração)

**Por que usar:**
- Reverter após infectar com malware
- Testar exploits destrutivos
- Experimentar sem medo

**Como criar:**

**VMware:**
```
VM → Snapshot → Take Snapshot
Nome: "Clean State - Pre Attack"
```

**VirtualBox:**
```
Machine → Take Snapshot
```

**PowerShell (Hyper-V):**
```powershell
Checkpoint-VM -Name "TargetVM" -SnapshotName "Clean"
```

---

## 📚 Configurações Específicas

### Desabilitar Windows Defender (Lab Only)

```powershell
# Temporário
Set-MpPreference -DisableRealtimeMonitoring $true

# Permanente (requer reboot)
New-ItemProperty -Path "HKLM:\SOFTWARE\Policies\Microsoft\Windows Defender" `
  -Name DisableAntiSpyware -Value 1 -PropertyType DWORD -Force
```

### Habilitar SMBv1 (para testes de EternalBlue)

```powershell
Enable-WindowsOptionalFeature -Online -FeatureName SMB1Protocol
```

### Configurar Serviços Vulneráveis

```bash
# Linux: FTP anônimo
sudo apt install vsftpd
echo "anonymous_enable=YES" | sudo tee -a /etc/vsftpd.conf
sudo systemctl restart vsftpd

# SSH com password authentication
sudo sed -i 's/PasswordAuthentication no/PasswordAuthentication yes/' /etc/ssh/sshd_config
sudo systemctl restart ssh
```

---

## 🔧 Ferramentas Essenciais

### Instalação em Kali

```bash
# Atualizar
sudo apt update && sudo apt full-upgrade -y

# Ferramentas de Rede
sudo apt install -y nmap masscan rustscan netcat-openbsd proxychains4

# Exploração
sudo apt install -y metasploit-framework exploitdb

# Web
sudo apt install -y burpsuite gobuster ffuf nikto sqlmap

# AD
sudo apt install -y bloodhound crackmapexec evil-winrm impacket-scripts

# Post-Exploitation
sudo apt install -y chisel ligolo-ng socat

# Wordlists
sudo apt install -y seclists wordlists

# Password Cracking
sudo apt install -y hashcat john hydra
```

### Configuração do BloodHound

```bash
# Instalar Neo4j
sudo apt install -y neo4j bloodhound

# Iniciar Neo4j
sudo neo4j start

# Acessar: http://localhost:7474
# Credenciais iniciais: neo4j / neo4j (mudar na primeira vez)

# Iniciar BloodHound
bloodhound
```

---

## 📊 Checklist de Setup

### Lab Básico (Nível 1)
- [ ] Hypervisor instalado (VMware/VirtualBox)
- [ ] Kali Linux VM criada
- [ ] Máquina vulnerável (Metasploitable/DVWA) configurada
- [ ] Rede isolada (host-only/internal)
- [ ] Snapshot "Clean State" criado
- [ ] Ferramentas atualizadas
- [ ] Acesso à internet desabilitado nas VMs alvo

### Lab Intermediário (Nível 2)
- [ ] Múltiplas VMs (Windows + Linux)
- [ ] Rede privada configurada (192.168.x.0/24)
- [ ] Serviços vulneráveis habilitados
- [ ] Firewall/Router (pfSense) opcional
- [ ] Documentação de IPs e serviços

### Lab AD (Nível 3)
- [ ] Domain Controller configurado
- [ ] Múltiplas workstations no domínio
- [ ] Usuários e grupos criados
- [ ] Vulnerabilidades intencionais (SPNs, delegations)
- [ ] BloodHound configurado
- [ ] Snapshot completo do ambiente

### Labs Online
- [ ] Conta TryHackMe criada
- [ ] OpenVPN configurado
- [ ] HackTheBox account (opcional)
- [ ] OWASP Juice Shop rodando localmente

---

## 🎓 Fluxo de Estudo Recomendado

```
Semana 1-2: Lab Básico
├─ Configurar Kali + DVWA
├─ Completar rooms básicos do TryHackMe
└─ Praticar reconhecimento e enumeração

Semana 3-4: Múltiplas VMs
├─ Criar rede com Windows + Linux
├─ Praticar exploração
└─ Documentar processo

Semana 5-8: Active Directory
├─ Configurar AD Lab (GOAD ou manual)
├─ Estudar teoria de AD
├─ Executar ataques (Kerberoasting, etc)
└─ Usar BloodHound para mapping

Semana 9+: Labs Online + Certificações
├─ HackTheBox (máquinas Easy → Medium)
├─ TryHackMe learning paths
└─ Preparação para OSCP
```

---

## ⚠️ Troubleshooting Comum

### VM não conecta à rede
```bash
# Verificar adapter
ip a
# Reiniciar network
sudo systemctl restart NetworkManager
```

### Kali não atualiza
```bash
# Corrigir sources.list
echo "deb http://http.kali.org/kali kali-rolling main contrib non-free non-free-firmware" | sudo tee /etc/apt/sources.list
sudo apt update
```

### Performance lenta
- Reduzir VMs simultâneas
- Alocar mais RAM
- Usar SSD ao invés de HDD
- Desabilitar GUI (usar headless)

---

## 📞 Recursos Adicionais

### Comunidades
- **Discord:** TryHackMe, HackTheBox, InfoSec
- **Reddit:** r/oscp, r/netsec, r/AskNetsec
- **Twitter:** @_JohnHammond, @IppSec, @TCM_Sec

### Documentação
- **OSCP Exam Guide:** https://help.offensive-security.com/hc/en-us/articles/360040165632
- **Red Team Notes:** https://www.ired.team/
- **HackTricks:** https://book.hacktricks.xyz/

---

## 🎯 Conclusão

Com este guia, você tem tudo para criar um laboratório completo e seguro para praticar Red Team.

**Lembre-se:**
- Sempre isolar suas VMs
- Nunca atacar sistemas reais sem autorização
- Documentar tudo
- Aprender de forma ética

---

<div align="center">

### 🏆 Seu laboratório é sua academia de hacking

**Configure, pratique, domine.**

---

**Próximo passo:** [Voltar ao ROADMAP](ROADMAP.md) para começar os módulos

</div>
