# 🌐 Recursos Externos - Red Team Essentials

Este documento consolida todos os recursos externos essenciais para profissionais de Red Team, organizados por categoria.

---

## 📑 Índice

- [MITRE ATT&CK Framework](#-mitre-attck-framework)
- [Mapas Globais de Ameaças](#-mapas-globais-de-ameaças)
- [Bancos de Dados de Vulnerabilidades](#-bancos-de-dados-de-vulnerabilidades)
- [Motores de Busca para Segurança](#-motores-de-busca-para-segurança)
- [Plataformas de Treinamento](#-plataformas-de-treinamento)
- [Ferramentas e Frameworks](#-ferramentas-e-frameworks)
- [Comunidades e Fóruns](#-comunidades-e-fóruns)
- [Blogs e Pesquisas](#-blogs-e-pesquisas)
- [Certificações](#-certificações)

---

## 🎯 MITRE ATT&CK Framework

### MITRE ATT&CK
- **URL:** https://attack.mitre.org/
- **Descrição:** Framework de conhecimento de táticas e técnicas de adversários baseado em observações do mundo real.
- **Uso no Projeto:** Todo o conteúdo deste repositório está mapeado para técnicas do ATT&CK.

### ATT&CK Navigator
- **URL:** https://mitre-attack.github.io/attack-navigator/
- **Descrição:** Ferramenta web para navegar e visualizar técnicas do ATT&CK.
- **Arquivo do Projeto:** `MITRE-ATTACK-MAPPING.json` - Importe este arquivo no Navigator para ver cobertura do repositório.

### Recursos ATT&CK

| Recurso | URL | Descrição |
|---------|-----|-----------|
| Documentação Oficial | https://attack.mitre.org/resources/ | Guias, treinamentos e recursos |
| ATT&CK for Enterprise | https://attack.mitre.org/matrices/enterprise/ | Matriz principal (Windows, Linux, macOS, Cloud) |
| ATT&CK for ICS | https://attack.mitre.org/matrices/ics/ | Sistemas de controle industrial |
| ATT&CK for Mobile | https://attack.mitre.org/matrices/mobile/ | Android e iOS |
| Grupos APT | https://attack.mitre.org/groups/ | Grupos de ameaças conhecidos |
| Software Malicioso | https://attack.mitre.org/software/ | Malware e ferramentas mapeadas |

### Como Usar

```bash
# 1. Acesse o ATT&CK Navigator
https://mitre-attack.github.io/attack-navigator/

# 2. Clique em "Open Existing Layer"
# 3. Faça upload do arquivo MITRE-ATTACK-MAPPING.json deste repositório
# 4. Visualize a cobertura de técnicas do RedTeam-Essentials
```

---

## 🗺️ Mapas Globais de Ameaças

Visualizações em tempo real de ataques cibernéticos ao redor do mundo.

### Kaspersky Cyberthreat Real-Time Map
- **URL:** https://cybermap.kaspersky.com/
- **Descrição:** Mapa em tempo real de ameaças detectadas pela rede Kaspersky
- **Funcionalidades:**
  - Ataques em tempo real
  - Estatísticas de malware
  - Países mais atacados
  - Tipos de ameaças detectadas

### Radware Live Threat Map
- **URL:** https://livethreatmap.radware.com/
- **Descrição:** Visualização de ataques DDoS e outras ameaças
- **Funcionalidades:**
  - Ataques DDoS em tempo real
  - Origem e destino de ataques
  - Intensidade de ataques
  - Tipos de vetores de ataque

### NetScout Cyber Threat Horizon
- **URL:** https://horizon.netscout.com/
- **Descrição:** Mapa de ameaças DDoS da NETSCOUT/Arbor Networks
- **Funcionalidades:**
  - Ataques DDoS globais
  - Estatísticas de tráfego
  - Picos de ataque
  - Top alvos atacados

### Outros Mapas de Ameaças

| Mapa | URL | Foco Principal |
|------|-----|----------------|
| Fortinet Threat Map | https://threatmap.fortiguard.com/ | Malware, Intrusões, Websites maliciosos |
| Check Point ThreatCloud | https://threatmap.checkpoint.com/ | Malware, Bots, Ataques |
| Talos Intelligence | https://talosintelligence.com/ | Spam, Malware, Vulnerabilidades |
| FireEye Cyber Threat Map | https://www.fireeye.com/cyber-map/threat-map.html | APTs, Malware avançado |

### Uso para Red Team

```
✅ Pesquisa de Tendências:
   - Quais vetores de ataque estão em alta
   - Países/setores mais visados
   - Tipos de malware populares

✅ Inteligência de Ameaças:
   - Compreender campanhas ativas
   - Estudar TTPs de grupos APT
   - Antecipar técnicas emergentes

✅ Emulação Realista:
   - Simular ataques baseados em ameaças reais
   - Testar defesas contra vetores atuais
```

---

## 🔓 Bancos de Dados de Vulnerabilidades

### CVE (Common Vulnerabilities and Exposures)
- **URL:** https://www.cve.org/
- **Descrição:** Lista oficial de vulnerabilidades de segurança conhecidas publicamente
- **Mantido por:** MITRE Corporation

#### Como Usar CVE

```bash
# Estrutura de um CVE ID
CVE-YYYY-NNNNN
# Exemplo: CVE-2021-44228 (Log4Shell)

# Pesquisar CVEs
https://cve.mitre.org/cve/search_cve_list.html

# Consultar detalhes
https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-YYYY-NNNNN
```

### Recursos Relacionados ao CVE

| Recurso | URL | Descrição |
|---------|-----|-----------|
| **NVD** (National Vulnerability Database) | https://nvd.nist.gov/ | Base de dados NIST com CVEs + CVSS scores |
| **CVE Details** | https://www.cvedetails.com/ | CVEs organizados por vendor, produto, tipo |
| **Exploit DB** | https://www.exploit-db.com/ | Exploits públicos para vulnerabilidades |
| **VulDB** | https://vuldb.com/ | Database de vulnerabilidades com timeline |
| **Packet Storm** | https://packetstormsecurity.com/ | Exploits, advisories, ferramentas |

### CVSS (Common Vulnerability Scoring System)

```
Severidade CVSS v3.1:
┌──────────┬─────────┬────────────────────────┐
│ Score    │ Nível   │ Descrição              │
├──────────┼─────────┼────────────────────────┤
│ 0.0      │ None    │ Sem vulnerabilidade    │
│ 0.1-3.9  │ Low     │ Impacto baixo          │
│ 4.0-6.9  │ Medium  │ Impacto moderado       │
│ 7.0-8.9  │ High    │ Impacto alto           │
│ 9.0-10.0 │ Critical│ Impacto crítico        │
└──────────┴─────────┴────────────────────────┘
```

### Uso para Red Team

```
✅ Reconhecimento:
   - Identificar vulnerabilidades em tecnologias do alvo
   - Buscar CVEs para versões específicas de software

✅ Exploração:
   - Encontrar exploits públicos para vulnerabilidades
   - Priorizar por CVSS score

✅ Relatórios:
   - Referenciar CVEs em achados
   - Calcular CVSS para vulnerabilidades descobertas
```

---

## 🔍 Motores de Busca para Segurança

### Shodan
- **URL:** https://www.shodan.io/
- **Descrição:** Motor de busca para dispositivos conectados à Internet (IoT, servidores, câmeras, etc)
- **Tagline:** "The search engine for the Internet of Things"

#### Funcionalidades Principais

```bash
# Pesquisas Básicas
apache                    # Servidores Apache
nginx                     # Servidores Nginx
"default password"        # Dispositivos com senha padrão
port:3389                 # RDP exposto
country:"BR"              # Dispositivos no Brasil

# Pesquisas Avançadas
product:"MySQL"           # Versões MySQL
vuln:CVE-2021-44228       # Dispositivos vulneráveis ao Log4Shell
os:"Windows Server 2012"  # SO específico
org:"Nome da Empresa"     # Organização específica

# Filtros Úteis
port:                     # Filtrar por porta
country:                  # Filtrar por país
city:                     # Filtrar por cidade
org:                      # Filtrar por organização
isp:                      # Filtrar por ISP
product:                  # Filtrar por produto
version:                  # Filtrar por versão
vuln:                     # Filtrar por CVE
```

#### Planos Shodan

| Plano | Preço | Recursos |
|-------|-------|----------|
| **Free** | Grátis | 50 resultados, funcionalidades básicas |
| **Membership** | $49 (lifetime) | Resultados ilimitados, export, API |
| **Small Business** | $899/ano | 100K API queries/mês |
| **Enterprise** | Custom | Queries ilimitadas, suporte |

#### Recursos Adicionais Shodan

- **Shodan CLI:** https://cli.shodan.io/
- **Shodan API:** https://developer.shodan.io/
- **Shodan Images:** https://images.shodan.io/
- **Shodan Exploits:** https://exploits.shodan.io/

### Outros Motores de Busca

| Motor | URL | Foco |
|-------|-----|------|
| **Censys** | https://censys.io/ | Similar ao Shodan, certificados SSL/TLS |
| **ZoomEye** | https://www.zoomeye.org/ | Dispositivos e serviços expostos |
| **FOFA** | https://fofa.info/ | Motor chinês, foco em Asia |
| **Binary Edge** | https://www.binaryedge.io/ | Threat intelligence, scanning |
| **GreyNoise** | https://www.greynoise.io/ | Internet scanning noise vs ameaças |
| **Onyphe** | https://www.onyphe.io/ | Cyber defense search engine |

### Uso Ético do Shodan

```
⚠️ IMPORTANTE:

✅ PERMITIDO:
   - Pesquisar ativos da SUA organização
   - Reconhecimento passivo (apenas visualizar)
   - Pesquisa educacional
   - Bug bounty (com scope definido)

❌ NÃO PERMITIDO:
   - Acessar dispositivos sem autorização
   - Explorar vulnerabilidades de terceiros
   - Port scanning ativo sem permissão
   - Uso malicioso de informações
```

### Dorks Úteis para Red Team

```bash
# Câmeras de segurança expostas
title:"webcamXP 5"
Server: SQ-WEBCAM

# Painéis administrativos
http.title:"Dashboard" country:"BR"
http.title:"Admin Panel"

# Bancos de dados expostos
product:"MongoDB" port:27017
product:"MySQL" port:3306
product:"PostgreSQL" port:5432

# Serviços RDP
port:3389 country:"BR"

# Jenkins sem autenticação
http.title:"Dashboard [Jenkins]"

# ElasticSearch aberto
product:"Elasticsearch" port:9200

# Docker APIs expostas
port:2375 product:"Docker"

# Interfaces SCADA/ICS
tag:scada
tag:ics

# Printers
"HP LaserJet" port:9100
"CUPS" port:631
```

---

## 🎓 Plataformas de Treinamento

### Gratuitas

| Plataforma | URL | Descrição |
|------------|-----|-----------|
| **TryHackMe** | https://tryhackme.com/ | Rooms guiadas, paths, labs |
| **HackTheBox** | https://www.hackthebox.com/ | Máquinas vulneráveis, challenges |
| **PentesterLab** | https://pentesterlab.com/ | Web security, gratuito básico |
| **OverTheWire** | https://overthewire.org/wargames/ | Wargames de linha de comando |
| **PicoCTF** | https://picoctf.org/ | CTF educacional |
| **Root Me** | https://www.root-me.org/ | Challenges variados |
| **VulnHub** | https://www.vulnhub.com/ | VMs vulneráveis para download |
| **OWASP WebGoat** | https://owasp.org/www-project-webgoat/ | Aplicação web vulnerável |
| **Metasploitable** | https://sourceforge.net/projects/metasploitable/ | VM Linux vulnerável |

### Pagas

| Plataforma | URL | Preço | Descrição |
|------------|-----|-------|-----------|
| **Offensive Security** | https://www.offensive-security.com/ | Variável | OSCP, OSEP, OSWE, OSWP |
| **Pentester Academy** | https://www.pentesteracademy.com/ | $249/ano | Cursos variados, CRTP, CRTE |
| **eLearnSecurity** | https://elearnsecurity.com/ | Variável | eJPT, eCPPT, eCRE |
| **HackTheBox Academy** | https://academy.hackthebox.com/ | Cubes | Cursos estruturados |
| **Altered Security** | https://www.alteredsecurity.com/ | Variável | AD Security (ex-Pentester Academy) |

---

## 🛠️ Ferramentas e Frameworks

### Command & Control (C2)

| Ferramenta | URL | Descrição |
|------------|-----|-----------|
| **Cobalt Strike** | https://www.cobaltstrike.com/ | C2 comercial (líder de mercado) |
| **Metasploit** | https://www.metasploit.com/ | Framework de exploração |
| **Sliver** | https://github.com/BishopFox/sliver | C2 open-source moderno |
| **Havoc** | https://github.com/HavocFramework/Havoc | C2 open-source |
| **Empire** | https://github.com/BC-SECURITY/Empire | PowerShell C2 |
| **Covenant** | https://github.com/cobbr/Covenant | C2 .NET |

### OSINT

| Ferramenta | URL | Descrição |
|------------|-----|-----------|
| **theHarvester** | https://github.com/laramies/theHarvester | Email/subdomain harvesting |
| **Maltego** | https://www.maltego.com/ | OSINT data mining |
| **Recon-ng** | https://github.com/lanmaster53/recon-ng | Framework de reconhecimento |
| **SpiderFoot** | https://github.com/smicallef/spiderfoot | Automação OSINT |
| **OSINT Framework** | https://osintframework.com/ | Coleção de ferramentas |

### Active Directory

| Ferramenta | URL | Descrição |
|------------|-----|-----------|
| **BloodHound** | https://github.com/BloodHoundAD/BloodHound | Visualização de AD |
| **Mimikatz** | https://github.com/gentilkiwi/mimikatz | Extração de credenciais |
| **Rubeus** | https://github.com/GhostPack/Rubeus | Kerberos attacks |
| **PowerView** | https://github.com/PowerShellMafia/PowerSploit | AD enumeration |
| **Impacket** | https://github.com/fortra/impacket | Protocols network |
| **CrackMapExec** | https://github.com/byt3bl33d3r/CrackMapExec | AD Swiss Army Knife |

### Post-Exploitation

| Ferramenta | URL | Descrição |
|------------|-----|-----------|
| **LinPEAS** | https://github.com/carlospolop/PEASS-ng | Linux PrivEsc |
| **WinPEAS** | https://github.com/carlospolop/PEASS-ng | Windows PrivEsc |
| **GTFOBins** | https://gtfobins.github.io/ | Unix binaries bypass |
| **LOLBAS** | https://lolbas-project.github.io/ | Living Off The Land Binaries |

---

## 💬 Comunidades e Fóruns

### Discord

| Servidor | Foco |
|----------|------|
| **TryHackMe Official** | Plataforma THM |
| **HackTheBox Official** | Plataforma HTB |
| **Hacking Brasil** | Comunidade BR |
| **The Cyber Mentor** | Red Team / Pentesting |
| **Black Hat Brasil** | Segurança BR |

### Reddit

| Subreddit | URL |
|-----------|-----|
| r/netsec | https://www.reddit.com/r/netsec/ |
| r/AskNetsec | https://www.reddit.com/r/AskNetsec/ |
| r/HowToHack | https://www.reddit.com/r/HowToHack/ |
| r/redteamsec | https://www.reddit.com/r/redteamsec/ |

### Outros

| Comunidade | URL |
|------------|-----|
| **Hack The Box Forums** | https://forum.hackthebox.com/ |
| **Offensive Security Forums** | https://forums.offensive-security.com/ |
| **0x00sec** | https://0x00sec.org/ |

---

## 📚 Blogs e Pesquisas

### Blogs de Red Team

| Blog | URL |
|------|-----|
| **SpecterOps** | https://posts.specterops.io/ |
| **Red Team Notes** | https://www.ired.team/ |
| **Orange Cyberdefense** | https://www.orangecyberdefense.com/global/blog |
| **MDSec** | https://www.mdsec.co.uk/knowledge-centre/ |
| **Optiv** | https://www.optiv.com/insights/source-zero |

### Pesquisadores

| Pesquisador | Foco |
|-------------|------|
| **Sean Metcalf** | Active Directory |
| **Will Schroeder** | AD, PowerShell |
| **Didier Stevens** | Malware Analysis |
| **Carlos Polop** | PrivEsc |

---

## 🎖️ Certificações

### Entry Level
- **CompTIA Security+**
- **eJPT** (eLearnSecurity Junior Penetration Tester)

### Intermediate
- **OSCP** ⭐ (Offensive Security Certified Professional)
- **eCPPT** (eLearnSecurity Certified PPT)
- **CRTP** (Certified Red Team Professional)

### Advanced
- **OSEP** (Offensive Security Experienced PT)
- **CRTE** (Certified Red Team Expert)
- **OSWE** (Offensive Security Web Expert)

### Expert
- **OSCE³** (Offensive Security Certified Expert)
- **GXPN** (GIAC Exploit Researcher)

---

## 🔗 Links Rápidos

### Navegação Rápida

```bash
# MITRE ATT&CK
https://attack.mitre.org/

# Mapas de Ameaças
https://cybermap.kaspersky.com/
https://livethreatmap.radware.com/
https://horizon.netscout.com/

# Vulnerabilidades
https://www.cve.org/
https://nvd.nist.gov/

# Shodan
https://www.shodan.io/

# Treinamento
https://tryhackme.com/
https://www.hackthebox.com/
```

---

## ⚖️ Aviso Legal

**TODOS** os recursos listados neste documento devem ser utilizados de forma **ÉTICA e LEGAL**.

```
⚠️ RESPONSABILIDADE:

- Obtenha SEMPRE autorização explícita antes de testar sistemas
- Respeite leis locais e internacionais
- Use apenas em ambientes autorizados (labs, bug bounty, seu próprio ambiente)
- O conhecimento aqui é para DEFESA, não para ataques maliciosos
- O autor e contribuidores NÃO se responsabilizam por uso indevido
```

---

## 📝 Contribuindo

Conhece um recurso valioso que não está listado? Contribua!

1. Fork o repositório
2. Adicione o recurso neste arquivo
3. Submeta um Pull Request
4. Veja [CONTRIBUTING.md](CONTRIBUTING.md) para detalhes

---

<div align="center">

### 🎯 Use seu conhecimento para defender, não para atacar

**Recursos compilados pela comunidade RedTeam-Essentials**

---

*Última atualização: 22 de Novembro de 2025*  
*Mantido por: [Samuel Ziger](https://github.com/Samuel-Ziger)*

</div>
