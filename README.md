# 🎯 RedTeam Essentials v2.1

> Repositorio educacional completo sobre Red Team, pentest e seguranca defensiva. Conteudo etico, scripts profissionais e mapeamento MITRE ATT&CK.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Educational](https://img.shields.io/badge/Purpose-Educational-green.svg)]()
[![Ethical](https://img.shields.io/badge/Content-Ethical-brightgreen.svg)]()
[![Version](https://img.shields.io/badge/Version-2.1.0-blue.svg)]()
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

## 📚 O que mudou na v2.1

Alem da base v2.0 (stack poliglota, `lib/`, CI, docker-lab):

- **Windows Privilege Escalation** (`06-Cheatsheets/windows_privesc_teoria.md`).
- **Initial Access** (modulo 13) e **Post-Exploitation** (modulo 14).
- **Web deep-dives** SQLi/SSRF + labs guiados DVWA / Juice Shop / VAmPI.
- **BloodHound CE + NetExec** na documentacao operacional (substitui CME legado).
- **MITRE layer** expandido para modulos 07-14.
- READMEs em todos os modulos; ROADMAP/CHANGELOG sincronizados.

Veja [CHANGELOG.md](CHANGELOG.md) para diff completo.

---

## 📁 Estrutura

```text
RedTeam-Essentials/
├── README.md                          (voce esta aqui)
├── CHANGELOG.md / ROADMAP.md / CONTRIBUTING.md / CODE_OF_CONDUCT.md / LICENSE
├── RESOURCES.md / REPORT-TEMPLATE.md / LAB-SETUP.md
├── report/                            (generate-pdf.sh → PDF via pandoc)
├── ATTACK_MAPPING_GUIDE.md / MITRE-ATTACK-MAPPING.json
├── validate_scripts.ps1               (lint + PSSA + checagens custom)
│
├── 00-Fundamentos/                    (redes, sistemas, identidade, RoE e lab seguro)
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
│   ├── linux_privesc_modern.md
│   ├── windows_privesc_teoria.md      NOVO v2.1
│   └── windows_lateral_movement_teoria.md
│
├── 07-Web-AppSec/
│   ├── owasp-top10-2021.md / api-security-checklist.md / recon-web-pratico.md
│   ├── xss-deep-dive.md / sqli-deep-dive.md / ssrf-deep-dive.md
│   ├── auth-bypass-patterns.md
│   └── labs/                          (DVWA SQLi, Juice XSS, VAmPI API)
├── 08-Cloud-RedTeam/                  (AWS / Azure / GCP + exercicios)
├── 09-C2-Evasion/                     (apenas teoria)
├── 10-Container-Sec/                  (Docker / K8s + exercicios)
├── 11-Python-Tools/
├── 12-Java-Tools/
├── 13-Initial-Access/                 NOVO v2.1
├── 14-Post-Exploitation/              NOVO v2.1
├── 15-Hybrid-Identity/                 (AD + Entra + workload identities)
├── 16-CICD-Supply-Chain/               (pipelines, OIDC, artefatos e provenance)
├── 17-macOS-Security/                   (endpoint, TCC, MDM e DFIR)
├── 18-Mobile-Security/                  (Android/iOS, MASVS e privacidade)
├── 19-Wireless-Security/                (Wi-Fi defensivo e análise offline)
├── 20-Offensive-Labs/                   (operações ofensivas integradas e seguras)
├── 21-Network-Pivoting/                 (rotas, segmentação e teardown)
├── 22-Secure-Code-Review/               (source-to-sink e autorização)
├── 23-Threat-Intel-Emulation/           (CTI orientada a hipóteses)
├── 24-Lateral-Movement/                 (attack paths, protocolos e telemetria)
├── 25-Cursos/                            (cursos completos em português)
│
├── docker-lab/
│   ├── docker-compose.yml
│   ├── Dockerfile.kali-pentest        (build do attacker)
│   └── README.md
│
└── .github/workflows/
    ├── powershell.yml / bash.yml / python.yml / java.yml
    └── markdown.yml
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

Acesse (somente localhost):

| Alvo | URL |
|------|-----|
| DVWA | http://127.0.0.1:8081 |
| Juice Shop | http://127.0.0.1:8082 |
| bWAPP | http://127.0.0.1:8083 |
| WebGoat | http://127.0.0.1:8084 |
| Vulnerable WordPress | http://127.0.0.1:8085 |
| NodeGoat | http://127.0.0.1:8086 |
| VAmPI (API) | http://127.0.0.1:8087 |

Labs guiados: `07-Web-AppSec/labs/`. Conecte na estacao Kali:

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

Comece pelo **[Módulo 00](00-Fundamentos/README.md)** se ainda não domina redes,
terminal, identidade, escopo e operação segura do laboratório.

| Tier | Foco | Modulos | Tempo |
|------|------|---------|-------|
| **1 - Iniciante** | Recon, OSINT, automacao | 01, 02, 04 | 4-6 semanas |
| **2 - Intermediario** | AD, privesc, lateral, web, initial access, post-ex | 03, 06, 07, 13, 14 | 8-12 semanas |
| **3 - Avancado** | Cloud, container, DFIR | 05, 08, 10 | 8-12 semanas |
| **4 - Profissional** | C2 (teoria), reporting, engagement | 09, 11, 12, REPORT-TEMPLATE | continuo |

### Trilhas por objetivo

| Objetivo | Ordem sugerida |
|----------|----------------|
| Red Team geral | 00 → 01 → 02 → 04 → 07 → 06 → 03 → 13 → 14 → 09 |
| AppSec e APIs | 00 → 01 → 07 → 11 → 12 → REPORT-TEMPLATE |
| Active Directory | 00 → 04 → 06 → 03 → 05 → 14 |
| Cloud e containers | 00 → 01 → 07 → 08 → 10 → 05 |
| Purple Team / DFIR | 00 → 05 → 03 → 07 → 09 → 13 → 14 |

Veja **[ROADMAP.md](ROADMAP.md)** para detalhes por semana.

### Cursos e conteúdo em vídeo

Cada módulo de 00 a 24 contém uma seção com pelo menos cinco vídeos em português
sobre seu próprio tema. O **[Módulo 25 — Cursos em português](25-Cursos/README.md)**
centraliza cursos completos, começando pelas trilhas da Solyd Offensive Security
e da DESEC Security.

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
| Initial Access (TA0001) | T1078, T1133, T1190, T1566 | 07, 13 |
| Execution (TA0002) | T1059, T1610 | 06, 10 |
| Persistence (TA0003) | T1098, T1547, T1053, T1543 | 03, 14 |
| Privilege Escalation (TA0004) | T1078, T1611, T1068, T1548, T1134 | 06, 10 |
| Defense Evasion (TA0005) | T1027, T1055, T1070, T1562 | 09 |
| Credential Access (TA0006) | T1003, T1110, T1552, T1558.003, T1558.004 | 03, 07 |
| Discovery (TA0007) | T1069, T1083, T1087, T1482, T1580, T1613 | 03, 08, 10 |
| Lateral Movement (TA0008) | T1021, T1550 | 06 |
| Collection (TA0009) | T1119, T1530, T1005 | 04, 08, 14 |
| Exfiltration (TA0010) | T1041, T1048 | 14 |
| Command & Control (TA0011) | T1071, T1573, T1090 | 09, 14 |

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

- 🔎 **[PROJECT-AUDIT.md](PROJECT-AUDIT.md)** - Diagnostico do conteudo atual e backlog priorizado de melhorias e novos temas.
- ⚔️ **[docs/OFFENSIVE-CONTENT-ROADMAP.md](docs/OFFENSIVE-CONTENT-ROADMAP.md)** - Entregas e próximos labs ofensivos seguros.
- 🗺️ **[ROADMAP.md](ROADMAP.md)** - Trilha de estudos (Tier 1 - 4) com MITRE ATT&CK.
- 🧪 **[LAB-SETUP.md](LAB-SETUP.md)** - VMs, AD lab, plataformas online.
- 📄 **[REPORT-TEMPLATE.md](REPORT-TEMPLATE.md)** - Template profissional de relatorio Red Team.
- 🖨️ **[report/](report/)** - Gerar PDF (pandoc + eisvogel) a partir do template.
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
