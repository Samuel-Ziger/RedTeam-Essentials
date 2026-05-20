# 🎯 RedTeam Essentials v2.0

> Repositorio educacional completo sobre Red Team, pentest e seguranca defensiva. Conteudo etico, scripts profissionais e mapeamento MITRE ATT&CK.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Educational](https://img.shields.io/badge/Purpose-Educational-green.svg)]()
[![Ethical](https://img.shields.io/badge/Content-Ethical-brightgreen.svg)]()
[![Version](https://img.shields.io/badge/Version-2.0.0-blue.svg)]()
[![PowerShell](https://img.shields.io/badge/PowerShell-5.1%2B%20%7C%207%2B-blue.svg)]()
[![Bash](https://img.shields.io/badge/Bash-4.0%2B-green.svg)]()
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)]()
[![Java](https://img.shields.io/badge/Java-17%2B-orange.svg)]()
[![MITRE ATT&CK](https://img.shields.io/badge/MITRE-ATT%26CK%20v14-red.svg)](https://attack.mitre.org/)

---

## ⚠️ Disclaimer

```
Este repositorio e EXCLUSIVAMENTE EDUCACIONAL.

OK   - Estudo, pesquisa, treinamento, certificacoes (OSCP, CRTP, OSEP, PNPT).
OK   - Ambientes proprios (labs locais, docker-lab incluso).
OK   - Engagements profissionais com autorizacao escrita.

NAO  - Atacar sistemas de terceiros sem autorizacao.
NAO  - Usar este conteudo para atividades ilegais.

Voce e responsavel por suas acoes. Respeite leis locais (LGPD, GDPR, CFAA, etc.).
```

---

## 📚 O que mudou na v2.0

Comparado a v1.x:

- **Cross-platform.** Scripts PowerShell rodam em Windows e Linux (PowerShell 7+).
- **Lib comum** (`lib/`): logging unificado, validacao etica, export padronizado.
- **Novos modulos**: Web AppSec, Cloud Red Team, C2/Evasion (teoria), Container Security.
- **Stack poliglota**: alem de PowerShell + Bash, agora Python e Java.
- **Lab Docker** local (`docker-lab/`) com DVWA, Juice Shop, WebGoat, VAmPI, NodeGoat + estacao Kali.
- **CI/CD** completo: PSScriptAnalyzer, ShellCheck, Ruff, Markdownlint, Lychee.
- **Conteudo atualizado** para tecnicas 2024-2026: ADCS, RBCD, Shadow Credentials, CVEs kernel recentes.

Veja [CHANGELOG.md](CHANGELOG.md) para diff completo.

---

## 📁 Estrutura

```text
RedTeam-Essentials/
├── README.md                          (voce esta aqui)
├── CHANGELOG.md / ROADMAP.md / CONTRIBUTING.md / CODE_OF_CONDUCT.md / LICENSE
├── RESOURCES.md / REPORT-TEMPLATE.md / LAB-SETUP.md
├── ATTACK_MAPPING_GUIDE.md / MITRE-ATTACK-MAPPING.json
├── validate_scripts.ps1               (lint + PSSA + checagens custom)
│
├── lib/                               NOVO em v2.0
│   ├── powershell/RTECommon.psm1      (logging, validacao, export)
│   ├── bash/rte_common.sh             (logging, traps, helpers)
│   └── python/rte_common.py           (logging, validacao, export)
│
├── 01-Recon/
│   ├── dns_enum.ps1                   (refactored: cross-platform + crt.sh + JSON)
│   ├── dns_enum.sh                    NOVO
│   ├── passive_recon_cheatsheet.md
│   └── web_recon_notes.md
├── 02-OSINT/
│   ├── osint-tools-list.md
│   └── osint_automation.ps1
├── 03-AD-Notes/
│   ├── ad_enum_commands.md
│   ├── kerberoasting_teoria.md        (typo fix + secao 2024-2026)
│   ├── bloodhound_teoria.md
│   └── modern-ad-attacks-2026.md      NOVO (ADCS, RBCD, Shadow Creds, SCCM)
├── 04-Automation/
│   ├── windows_setup_clean.ps1        (refactored)
│   ├── linux_postinstall.sh           (refactored: dry-run, distro detect)
│   ├── organize_logs.ps1              (refactored: INDEX.md + SHA-256)
│   └── ad_recon.sh                    NOVO (nmap + nxc + Impacket wrapper)
├── 05-DFIR/
│   ├── FORENSIC_REPORT_TEMPLATE.md
│   ├── PLAYBOOK_RANSOMWARE.md
│   ├── forensics_artifacts.md
│   ├── memory_analysis_teoria.md
│   └── windows_event_logs.md
├── 06-Cheatsheets/
│   ├── powershell_cheatsheet.md
│   ├── linux_privesc_teoria.md
│   ├── linux_privesc_modern.md        NOVO (CVEs 2022-2026, eBPF, namespaces)
│   └── windows_lateral_movement_teoria.md
│
├── 07-Web-AppSec/                     NOVO modulo
│   ├── owasp-top10-2021.md
│   ├── api-security-checklist.md
│   ├── recon-web-pratico.md
│   ├── xss-deep-dive.md
│   └── auth-bypass-patterns.md
├── 08-Cloud-RedTeam/                  NOVO modulo
│   ├── aws-attack-paths.md
│   ├── azure-attack-paths.md
│   ├── gcp-attack-paths.md
│   └── cloud-recon-tools.md
├── 09-C2-Evasion/                     NOVO modulo (apenas teoria)
│   ├── c2-overview.md
│   ├── evasion-fundamentals.md
│   └── opsec-checklist.md
├── 10-Container-Sec/                  NOVO modulo
│   ├── docker-escape-techniques.md
│   ├── kubernetes-attack-paths.md
│   └── hardening-baseline.md
├── 11-Python-Tools/                   NOVO modulo
│   ├── subdomain_enum.py              (crt.sh + HackerTarget + OTX + asyncio resolve)
│   ├── port_scanner.py                (asyncio TCP scan + banner grab)
│   ├── jwt_analyzer.py                (static analysis + HS* bruteforce)
│   └── hash_identifier.py
├── 12-Java-Tools/                     NOVO modulo
│   └── src/main/java/io/redteam/essentials/PayloadGenerator.java
│
├── docker-lab/                        NOVO
│   ├── docker-compose.yml             (DVWA, Juice Shop, WebGoat, VAmPI, NodeGoat, Kali)
│   ├── Dockerfile.kali-pentest
│   └── README.md
│
└── .github/workflows/                 NOVO (CI/CD)
    ├── powershell.yml (PSScriptAnalyzer)
    ├── bash.yml       (ShellCheck)
    ├── python.yml     (Ruff + py_compile)
    ├── java.yml       (javac -Xlint:all -Werror)
    └── markdown.yml   (markdownlint + Lychee link check)
```

---

## 🚀 Quick Start

### 1. Clone

```bash
git clone https://github.com/Samuel-Ziger/RedTeam-Essentials.git
cd RedTeam-Essentials
```

### 2. Subir o lab local

```bash
cd docker-lab
docker compose up -d
docker compose ps
```

Acesse:

- DVWA -> http://127.0.0.1:8081
- Juice Shop -> http://127.0.0.1:8082
- WebGoat -> http://127.0.0.1:8084

Conecte na estacao Kali do lab:

```bash
docker exec -it rte-attacker bash
```

### 3. Use as ferramentas

**PowerShell (Windows ou PWSh em Linux):**

```powershell
Import-Module ./lib/powershell/RTECommon.psm1
./01-Recon/dns_enum.ps1 -Domain example.com -IncludeSubdomains
./04-Automation/organize_logs.ps1 -SourcePath ~/Downloads -TargetName HTB_Forest
```

**Bash:**

```bash
./01-Recon/dns_enum.sh -d example.com --subs --whois -o ./output
sudo ./04-Automation/linux_postinstall.sh --extra "ghidra"
```

**Python:**

```bash
python3 11-Python-Tools/subdomain_enum.py -d example.com --resolve
python3 11-Python-Tools/port_scanner.py -t scanme.nmap.org -p top100 --banner
python3 11-Python-Tools/jwt_analyzer.py -t "$JWT"
```

**Java:**

```bash
cd 12-Java-Tools
mkdir -p build
javac -d build src/main/java/io/redteam/essentials/PayloadGenerator.java
java -cp build io.redteam.essentials.PayloadGenerator --type xss --count 20
```

---

## 🎓 Trilha de Aprendizado

| Tier | Foco | Modulos | Tempo |
|------|------|---------|-------|
| **1 - Iniciante** | Recon, OSINT, conceitos | 01, 02, RESOURCES.md | 2-3 semanas |
| **2 - Intermediario** | AD, privesc, lateral, web | 03, 06, 07 | 6-8 semanas |
| **3 - Avancado** | Cloud, container, DFIR | 05, 08, 10 | 8-12 semanas |
| **4 - Profissional** | C2 (teoria), full engagement | 09, REPORT-TEMPLATE | continuo |

Veja **[ROADMAP.md](ROADMAP.md)** para detalhes por semana.

---

## 🛠️ Stack Tecnologica

| Camada | Tecnologia |
|--------|-----------|
| Shell | PowerShell 7+, Bash 4+ |
| Backend / scripts | Python 3.10+, Java 17+ |
| Containers | Docker, Docker Compose, Kubernetes (manifests) |
| CI/CD | GitHub Actions (5 workflows) |
| Linters | PSScriptAnalyzer, ShellCheck, Ruff, markdownlint, Lychee |
| Frameworks de pentest | Nmap, Impacket, NetExec, BloodHound, Burp Suite |

---

## 🎯 MITRE ATT&CK Coverage

| Tatica | Tecnicas | Modulos |
|--------|----------|---------|
| Reconnaissance (TA0043) | T1590, T1592, T1593, T1594, T1596, T1598 | 01, 02 |
| Initial Access (TA0001) | T1078, T1133, T1190, T1199, T1566 | 07, 08 |
| Execution (TA0002) | T1059, T1610 | 06, 10 |
| Persistence (TA0003) | T1098, T1136, T1547, T1543 | 03, 09 |
| Privilege Escalation (TA0004) | T1078, T1611, T1068 | 06, 10 |
| Defense Evasion (TA0005) | T1027, T1055, T1070, T1140, T1562 | 09 |
| Credential Access (TA0006) | T1003, T1110, T1552, T1558.003, T1558.004 | 03, 07 |
| Discovery (TA0007) | T1069, T1083, T1087, T1482, T1580 | 03, 08, 10 |
| Lateral Movement (TA0008) | T1021, T1550 | 06 |
| Collection (TA0009) | T1119, T1530 | 04, 08 |
| Command & Control (TA0011) | T1071, T1573 | 09 |

Layer JSON pronto para o **ATT&CK Navigator**: [`MITRE-ATTACK-MAPPING.json`](MITRE-ATTACK-MAPPING.json). Detalhes em [`ATTACK_MAPPING_GUIDE.md`](ATTACK_MAPPING_GUIDE.md).

---

## 🤝 Contribuindo

Veja [CONTRIBUTING.md](CONTRIBUTING.md). Resumo:

1. Fork + branch (`feature/<topico>`).
2. Siga padroes - PowerShell com `Set-StrictMode`, Bash com `set -euo pipefail`, Python passa `ruff check`.
3. Rode `validate_scripts.ps1` antes do PR (ou deixe o CI rodar).
4. PR com descricao clara, mapeamento ATT&CK se aplicavel.

---

## 📚 Documentacao Expandida

- 🗺️ **[ROADMAP.md](ROADMAP.md)** - Trilha de estudos (Tier 1 - 4) com MITRE ATT&CK.
- 🧪 **[LAB-SETUP.md](LAB-SETUP.md)** - VMs, AD lab, plataformas online.
- 📄 **[REPORT-TEMPLATE.md](REPORT-TEMPLATE.md)** - Template profissional de relatorio Red Team.
- 🔗 **[RESOURCES.md](RESOURCES.md)** - Mapas de ameacas, CVE DBs, plataformas de treino.
- 🎯 **[ATTACK_MAPPING_GUIDE.md](ATTACK_MAPPING_GUIDE.md)** - Como usar o layer ATT&CK.

---

## 👤 Autor

**Samuel Ziger**
GitHub: [@Samuel-Ziger](https://github.com/Samuel-Ziger)

Dev Fullstack + Pentester. Stack: Vue, Java, Python, Bash, PowerShell.

---

## 📜 Licenca

MIT. Veja [LICENSE](LICENSE).

---

## ⭐ Apoie

Se este repositorio te ajudou, deixe uma estrela e compartilhe com quem esta aprendendo seguranca ofensiva.

> **Com grandes poderes vem grandes responsabilidades. Use este conhecimento para o bem.**
