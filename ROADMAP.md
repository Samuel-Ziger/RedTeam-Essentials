# 🗺️ ROADMAP - Red Team Essentials

> **Trilha de Aprendizado Estruturada e Progressiva**

Este documento apresenta uma roadmap completa para estudar Red Team de forma gradual, organizada e eficiente, com integração ao framework **MITRE ATT&CK**.

---

## 📊 Visão Geral do Roadmap

```
┌──────────────────────────────────────────────────────────────┐
│                    NÍVEL DE PROFICIÊNCIA                     │
├──────────────────────────────────────────────────────────────┤
│ TIER 1: FUNDAMENTOS     │ TIER 2: INTERMEDIÁRIO              │
│ (Iniciantes)            │ (Com experiência)                  │
│ ├─ Recon                │ ├─ Active Directory                │
│ ├─ OSINT                │ ├─ Lateral Movement                │
│ └─ Ferramentas Básicas  │ ├─ Privilege Escalation            │
│                         │ └─ Post-Exploitation               │
│                         │                                    │
│ TIER 3: AVANÇADO        │ TIER 4: PROFISSIONAL               │
│ (Praticantes)           │ (Red Team Real)                    │
│ ├─ Evasion              │ ├─ C2 Infrastructure               │
│ ├─ Persistence          │ ├─ Operações Complexas             │
│ ├─ DFIR Evasion         │ ├─ Report Writing                  │
│ └─ Custom Tooling       │ └─ Full Engagement                 │
└──────────────────────────────────────────────────────────────┘
```

---

## 🎯 TIER 1: Fundamentos (Iniciantes)

**Pré-requisitos:** Conhecimento básico de redes e sistemas operacionais  
**Tempo estimado:** 4-6 semanas  
**Objetivo:** Compreender os fundamentos de reconhecimento e coleta de informações

### Módulo 1.1: Reconhecimento Passivo (01-Recon)
- **Duração:** 1-2 semanas
- **Objetivos de Aprendizado:**
  - Entender a diferença entre reconhecimento passivo e ativo
  - Aprender técnicas de OSINT básicas
  - Dominar ferramentas de DNS enumeration
  - Compreender footprinting de aplicações web

- **Conteúdo:**
  - `passive_recon_cheatsheet.md` - Teoria e comandos
  - `dns_enum.ps1` - Script automatizado de DNS
  - `web_recon_notes.md` - Reconhecimento web

- **MITRE ATT&CK Mapping:**
  - TA0043 - Reconnaissance
    - T1592 - Gather Victim Host Information
    - T1590 - Gather Victim Network Information
    - T1596 - Search Open Technical Databases

- **Tarefas Práticas:**
  1. ✅ Executar reconhecimento passivo em um domínio de teste
  2. ✅ Enumerar subdomínios usando múltiplas técnicas
  3. ✅ Criar um mapa de infraestrutura de um alvo fictício
  4. ✅ Documentar fontes de informação descobertas

- **Recursos de Prática:**
  - TryHackMe: "Passive Reconnaissance" room
  - HackTheBox: Máquinas tier 0 e 1

---

### Módulo 1.2: OSINT Avançado (02-OSINT)
- **Duração:** 1-2 semanas
- **Objetivos de Aprendizado:**
  - Coletar informações de fontes públicas
  - Automatizar processos de OSINT
  - Correlacionar dados de múltiplas fontes
  - Entender limites éticos e legais

- **Conteúdo:**
  - `osint-tools-list.md` - Ferramentas essenciais
  - `osint_automation.ps1` - Automação de coleta

- **MITRE ATT&CK Mapping:**
  - TA0043 - Reconnaissance
    - T1593 - Search Open Websites/Domains
    - T1594 - Search Victim-Owned Websites
    - T1598 - Phishing for Information

- **Tarefas Práticas:**
  1. ✅ Criar perfil de organização usando apenas fontes abertas
  2. ✅ Automatizar coleta de informações de funcionários
  3. ✅ Identificar tecnologias utilizadas por um alvo
  4. ✅ Gerar relatório OSINT profissional

- **Recursos de Prática:**
  - TryHackMe: "OSINT" learning path
  - OSINT Framework: https://osintframework.com/

---

### Módulo 1.3: Fundamentos de Scripts e Automação (04-Automation)
- **Duração:** 1 semana
- **Objetivos de Aprendizado:**
  - Entender automação com PowerShell e Bash
  - Aprender a organizar evidências e logs
  - Criar scripts seguros e reutilizáveis

- **Conteúdo:**
  - `windows_setup_clean.ps1` - Setup de ambiente Windows
  - `linux_postinstall.sh` - Setup de ambiente Linux
  - `organize_logs.ps1` - Organização de logs

- **Tarefas Práticas:**
  1. ✅ Configurar ambiente de teste automatizado
  2. ✅ Criar script de organização de evidências
  3. ✅ Implementar validações e tratamento de erros
  4. ✅ Documentar scripts criados

- **Recursos de Prática:**
  - PowerShell Gallery: Estudar módulos existentes
  - GitHub: Analisar scripts de automação

---

### Módulo 1.4: Introdução ao DFIR (05-DFIR)
- **Duração:** 1 semana
- **Objetivos de Aprendizado:**
  - Compreender perspectiva defensiva
  - Analisar logs e artefatos
  - Entender detecção de ataques

- **Conteúdo:**
  - `windows_event_logs.md` - Logs do Windows
  - `forensics_artifacts.md` - Artefatos forenses
  - `memory_analysis_teoria.md` - Análise de memória

- **MITRE ATT&CK Mapping (Perspectiva de Detecção):**
  - Entender como ataques são detectados
  - Aprender a evitar deixar rastros óbvios

- **Tarefas Práticas:**
  1. ✅ Analisar Event Logs de um ataque simulado
  2. ✅ Identificar artefatos de execução de malware
  3. ✅ Criar timeline de incidente
  4. ✅ Estudar como Blue Team detecta Red Team

---

## 🔥 TIER 2: Intermediário

**Pré-requisitos:** Completar TIER 1  
**Tempo estimado:** 8-12 semanas  
**Objetivo:** Dominar técnicas de exploração e pós-exploração

### Módulo 2.1: Active Directory Fundamentals (03-AD-Notes)
- **Duração:** 3-4 semanas
- **Objetivos de Aprendizado:**
  - Entender arquitetura do Active Directory
  - Dominar técnicas de enumeração
  - Compreender ataques clássicos (Kerberoasting, AS-REP Roasting)
  - Usar BloodHound para mapeamento

- **Conteúdo:**
  - `ad_enum_commands.md` - Comandos de enumeração
  - `kerberoasting_teoria.md` - Teoria de Kerberoasting
  - `bloodhound_teoria.md` - Uso do BloodHound

- **MITRE ATT&CK Mapping:**
  - TA0007 - Discovery
    - T1087 - Account Discovery
    - T1069 - Permission Groups Discovery
    - T1482 - Domain Trust Discovery
  - TA0006 - Credential Access
    - T1558.003 - Kerberoasting
    - T1558.004 - AS-REP Roasting

- **Tarefas Práticas:**
  1. ✅ Montar laboratório AD completo
  2. ✅ Enumerar usuários, grupos e GPOs
  3. ✅ Executar Kerberoasting em ambiente controlado
  4. ✅ Mapear caminhos de ataque com BloodHound
  5. ✅ Identificar configurações inseguras

- **Recursos de Prática:**
  - TryHackMe: "Attacking Kerberos", "AD Basics"
  - HackTheBox: Máquinas com AD (Forest, Cascade, Blackfield)
  - GOAD (Game of Active Directory): Lab completo

---

### Módulo 2.2: Privilege Escalation (06-Cheatsheets)
- **Duração:** 2-3 semanas
- **Objetivos de Aprendizado:**
  - Identificar vetores de escalação
  - Explorar misconfigurations
  - Abusar de privilégios

- **Conteúdo:**
  - `linux_privesc_teoria.md` / `linux_privesc_modern.md` - Escalação Linux
  - `windows_privesc_teoria.md` - Escalação Windows (enum, UAC, services, tokens)

- **MITRE ATT&CK Mapping:**
  - TA0004 - Privilege Escalation
    - T1068 - Exploitation for Privilege Escalation
    - T1548 - Abuse Elevation Control Mechanism
    - T1078 - Valid Accounts
    - T1134 - Access Token Manipulation

- **Tarefas Práticas:**
  1. [ ] Enumerar sistema para vetores de privesc (Linux e Windows)
  2. [ ] Explorar SUID/SUDO em Linux
  3. [ ] Identificar serviços/unquoted paths/AlwaysInstallElevated em Windows
  4. [ ] Praticar em THM PrivEsc / HTB / GOAD (ambiente autorizado)

- **Recursos de Prática:**
  - TryHackMe: "Linux PrivEsc", "Windows PrivEsc"
  - VulnHub: Máquinas de privesc

---

### Módulo 2.3: Lateral Movement (06-Cheatsheets)
- **Duração:** 2-3 semanas
- **Objetivos de Aprendizado:**
  - Mover-se lateralmente em rede
  - Usar credenciais obtidas
  - Evitar detecção durante movimento

- **Conteúdo:**
  - `windows_lateral_movement_teoria.md` - Movimento lateral Windows

- **MITRE ATT&CK Mapping:**
  - TA0008 - Lateral Movement
    - T1021.001 - Remote Desktop Protocol
    - T1021.002 - SMB/Windows Admin Shares
    - T1021.006 - Windows Remote Management
    - T1550 - Use Alternate Authentication Material

- **Tarefas Práticas:**
  1. ✅ Executar Pass-the-Hash
  2. ✅ Usar PsExec para movimento lateral
  3. ✅ Explorar WMI e WinRM
  4. ✅ Pivotar através de múltiplos hosts

- **Recursos de Prática:**
  - HackTheBox: Pro Labs (Dante, Offshore)
  - CRTP/CRTE labs

---

### Módulo 2.4: Post-Exploitation (14-Post-Exploitation)
- **Duração:** 2 semanas
- **Objetivos de Aprendizado:**
  - Manter acesso de forma documentada e etica
  - Coletar e staging de evidencias
  - Exfiltrar dados de forma controlada em lab

- **Conteúdo:**
  - `collection-exfil.md` - staging, tunnels (chisel/ligolo), OPSEC de loot
  - `persistence-overview.md` - Run keys, tasks, cron/systemd; ponte para AD

- **MITRE ATT&CK Mapping:**
  - TA0009 - Collection
  - TA0003 - Persistence
  - TA0010 - Exfiltration

- **Tarefas Práticas:**
  1. [ ] Montar tunnel lab (chisel ou ligolo-ng) entre duas VMs suas
  2. [ ] Documentar loot com checklist de cleanup
  3. [ ] Mapear persistencia encontrada vs deteccao (Sysmon)

### Módulo 2.5: Initial Access (13-Initial-Access)
- **Duração:** 1-2 semanas
- **Objetivos de Aprendizado:**
  - Compreender vetores T1566 / T1190 / T1133 sem weaponization
  - Avaliar superfícies externas (VPN/RDP/OWA) com ética
  - Ligar web public-facing ao módulo 07

- **Conteúdo:**
  - `phishing-teoria.md`
  - `external-services.md`

- **MITRE ATT&CK Mapping:**
  - TA0001 - Initial Access (T1566, T1190, T1133, T1078)

- **Tarefas Práticas:**
  1. ✅ Configurar persistência
  2. ✅ Dump de credenciais (Mimikatz, LSASS)
  3. ✅ Simular exfiltração de dados
  4. ✅ Estabelecer C2 básico

---

## ⚡ TIER 3: Avançado

**Pré-requisitos:** Completar TIER 2 + Experiência prática  
**Tempo estimado:** 12-16 semanas  
**Objetivo:** Dominar técnicas avançadas de evasão e persistência

### Módulo 3.1: Evasion Techniques
- **Duração:** 4 semanas
- **Objetivos:**
  - Evitar EDR/AV
  - Ofuscação de payloads
  - Living off the Land (LOLBAS)
  - AMSI/ETW bypass

- **MITRE ATT&CK Mapping:**
  - TA0005 - Defense Evasion
    - T1027 - Obfuscated Files or Information
    - T1055 - Process Injection
    - T1140 - Deobfuscate/Decode Files or Information
    - T1562 - Impair Defenses

---

### Módulo 3.2: Advanced Persistence
- **Duração:** 3 semanas
- **Objetivos:**
  - Backdoors persistentes
  - Rootkits básicos
  - Golden Ticket / Silver Ticket
  - Skeleton Key

- **MITRE ATT&CK Mapping:**
  - TA0003 - Persistence
    - T1547 - Boot or Logon Autostart Execution
    - T1546 - Event Triggered Execution
    - T1098 - Account Manipulation

---

### Módulo 3.3: Custom Tooling Development
- **Duração:** 4 semanas
- **Objetivos:**
  - Desenvolver ferramentas customizadas
  - Bypass de assinaturas
  - Shellcode development
  - Malware development (educacional)

---

### Módulo 3.4: DFIR Evasion
- **Duração:** 3 semanas
- **Objetivos:**
  - Limpar logs e rastros
  - Anti-forensics
  - Timestomping
  - Entender como forense funciona para evadir

---

## 🏆 TIER 4: Profissional

**Pré-requisitos:** Completar TIER 3 + Certificações intermediárias  
**Tempo estimado:** 16-24 semanas  
**Objetivo:** Executar operações Red Team completas e realistas

### Módulo 4.1: C2 Infrastructure
- **Duração:** 4 semanas
- **Objetivos:**
  - Configurar Cobalt Strike / Sliver / Havoc
  - Domain fronting
  - Redirectors
  - Malleable C2 profiles

---

### Módulo 4.2: Full Red Team Engagement
- **Duração:** 8 semanas
- **Objetivos:**
  - Planejamento de operação
  - Execução de engagement completo
  - Evitar detecção por Blue Team
  - Cumprir objetivos (flags, crown jewels)

---

### Módulo 4.3: Professional Reporting
- **Duração:** 2 semanas
- **Objetivos:**
  - Escrever relatórios executivos
  - Relatórios técnicos detalhados
  - Recomendações de remediação
  - Apresentação para stakeholders

---

### Módulo 4.4: Specialized Tracks
- **Duração:** Variável
- **Já no repo:**
  - Cloud Red Teaming → `08-Cloud-RedTeam/`
  - Web Application Security → `07-Web-AppSec/` (+ labs)
  - Container Security → `10-Container-Sec/`
- **Em aberto (sem modulo ainda):**
  - Mobile Pentesting
  - IoT / OT Security
  - Wireless

---

## 📈 Progressão de Certificações Recomendadas

```
TIER 1 (Fundamentos)
└─ eJPT (eLearnSecurity Junior Penetration Tester)
└─ CompTIA PenTest+

TIER 2 (Intermediário)
└─ OSCP (Offensive Security Certified Professional) ⭐
└─ eCPPT (eLearnSecurity Certified PPT)
└─ CRTP (Certified Red Team Professional)

TIER 3 (Avançado)
└─ OSEP (Offensive Security Experienced Penetration Tester)
└─ CRTE (Certified Red Team Expert)
└─ OSWE (Offensive Security Web Expert)

TIER 4 (Profissional)
└─ OSCE³ (Offensive Security Certified Expert)
└─ PACES (Pentester Academy Certified Enterprise Specialist)
└─ GXPN (GIAC Exploit Researcher and Advanced Penetration Tester)
```

---

## 🎯 Integração com MITRE ATT&CK Framework

Este roadmap está totalmente mapeado com o **MITRE ATT&CK Framework**, permitindo que você:

1. **Entenda a tática e técnica** que está estudando
2. **Correlacione com ataques reais** (APTs documentadas)
3. **Aprenda detecção e mitigação** simultaneamente
4. **Documente seus testes** usando IDs oficiais

### Como Usar o MITRE ATT&CK:
```
1. Acesse: https://attack.mitre.org/
2. Para cada técnica estudada, leia:
   - Descrição detalhada
   - Procedimentos de APTs
   - Métodos de detecção
   - Mitigações possíveis
3. Use IDs nas suas notas (ex: T1558.003 - Kerberoasting)
```

---

## 📊 Tracking de Progresso

### Checklist de Progresso
```
TIER 1 - Fundamentos
[ ] Módulo 1.1: Reconhecimento Passivo
[ ] Módulo 1.2: OSINT Avançado
[ ] Módulo 1.3: Automação
[ ] Módulo 1.4: Introdução DFIR

TIER 2 - Intermediário
[ ] Módulo 2.1: Active Directory
[ ] Módulo 2.2: Privilege Escalation (Linux + Windows)
[ ] Módulo 2.3: Lateral Movement
[ ] Módulo 2.4: Post-Exploitation (14)
[ ] Módulo 2.5: Initial Access (13)
[ ] Módulo 2.6: Web AppSec + labs docker (07)

TIER 3 - Avançado
[ ] Módulo 3.1: Evasion Techniques
[ ] Módulo 3.2: Advanced Persistence
[ ] Módulo 3.3: Custom Tooling
[ ] Módulo 3.4: DFIR Evasion

TIER 4 - Profissional
[ ] Módulo 4.1: C2 Infrastructure
[ ] Módulo 4.2: Full Engagement
[ ] Módulo 4.3: Professional Reporting
[ ] Módulo 4.4: Specialized Tracks
```

---

## 🔄 Proximos Passos (planejamento realista)

### Feito na v2.0 / v2.1
- [x] Modulos Cloud, Web, C2 (teoria), Container, Python/Java tools
- [x] Lab Docker web/API
- [x] Windows Privesc, Initial Access, Post-Exploitation
- [x] Labs guiados Web (DVWA / Juice / VAmPI)
- [x] Sync NetExec + BloodHound CE + MITRE expandido

### Em aberto
- [ ] Labs IaC (Terraform/Ansible) quando houver codigo no repo
- [ ] Mobile / Wireless tracks
- [ ] Purple-team exercises pareados
- [ ] CTF / videos proprios (somente com artefatos versionados)

---

## 📚 Recursos Complementares

### Livros Essenciais por TIER
**TIER 1:**
- "The Web Application Hacker's Handbook"
- "Red Team Field Manual (RTFM)"

**TIER 2:**
- "The Hacker Playbook 3"
- "Attacking Network Protocols"
- "Active Directory Security"

**TIER 3:**
- "Advanced Penetration Testing" - Wil Allsopp
- "The Art of Memory Forensics"
- "Practical Malware Analysis"

**TIER 4:**
- "Red Team Development and Operations"
- "Adversarial Tradecraft in Cybersecurity"

---

## ⚠️ Lembretes Importantes

1. **Sempre pratique em ambientes autorizados**
2. **Documente tudo** - notas detalhadas são essenciais
3. **Não pule tiers** - fundamentos são críticos
4. **Aprenda defesa também** - entender Blue Team te torna melhor Red Team
5. **Mantenha-se atualizado** - segurança evolui rapidamente

---

<div align="center">

### 🎯 Sua Jornada Começa Aqui

**De iniciante a profissional: um passo de cada vez**

*"The only way to do great work is to love what you do." - Steve Jobs*

---

**Próximo passo:** Começar pelo **TIER 1 - Módulo 1.1: Reconhecimento Passivo**

</div>
