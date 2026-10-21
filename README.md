# 🎯 RedTeam Essentials v2.1

> Formação educacional em português, do zero ao avançado, sobre programação,
> sistemas operacionais, redes, criptografia, privacidade e Purple Team, seguida
> por uma especialização prática em segurança. O projeto combina teoria
> autocontida, código real, laboratórios autorizados, defesa, testes
> automatizados e mapeamento MITRE ATT&CK.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Educational](https://img.shields.io/badge/Purpose-Educational-green.svg)]()
[![Ethical](https://img.shields.io/badge/Content-Ethical-brightgreen.svg)]()
[![Version](https://img.shields.io/badge/Version-2.1.0-blue.svg)]()
[![Modules](https://img.shields.io/badge/Modules-41%20active-6f42c1.svg)](MODULE-CATALOG.json)
[![PowerShell](https://img.shields.io/badge/PowerShell-5.1%2B%20%7C%207%2B-blue.svg)]()
[![Bash](https://img.shields.io/badge/Bash-4.0%2B-green.svg)]()
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)]()
[![Java](https://img.shields.io/badge/Java-17%2B-orange.svg)]()
[![MITRE ATT&CK](https://img.shields.io/badge/MITRE-ATT%26CK-red.svg)](https://attack.mitre.org/)

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

## 📊 Estado atual

Os 41 módulos, de `00` a `40`, estão ativos no catálogo canônico. Eles formam
duas etapas deliberadas:

- **Base obrigatória (`00`–`26`)**: programação, sistemas operacionais, redes,
  criptografia, privacidade e fundamentos Purple Team.
- **Especialização em segurança (`27`–`40`)**: governança, ferramentas,
  reconhecimento, AppSec, identidade, cloud, containers, operações ofensivas
  autorizadas, DFIR, threat intelligence e capstone integrado.

O módulo `27` é o gate entre as etapas: a especialização pressupõe que a
base `00`–`26` já foi concluída.

| Indicador | Estado atual |
|---|---:|
| Módulos ativos | 41 |
| Documentos Markdown | 1.011 |
| Fixtures/datasets locais | 42 |
| Arquivos de teste inventariados | 67 |
| Workflows de CI | 22 |
| Contratos editoriais completos | 41 de 41 |
| Vídeos em português | pelo menos 5 por módulo da base `00`–`26` |

Os números estruturais podem ser recalculados localmente:

```bash
python3 scripts/project_metrics.py --format json
python3 rte.py modules --status active
```

---

## 🖥️ Aplicacao visual de estudos

Todo o curriculo tambem pode ser estudado em uma interface React local. A area
**Formacao** apresenta os 41 modulos em uma jornada unica de `00` a `40`, com
sete areas tematicas como filtros secundarios e o bloqueio pedagogico entre a
base e a especializacao. A **Biblioteca completa** reune referencias, solucoes,
documentacao global e materiais complementares que nao pertencem a uma rota
curricular. O leitor abre Markdown, codigo, configuracoes, datasets e imagens
sem executar esses arquivos.

A aplicacao registra o ultimo conteudo visitado, permite marcar leituras e
mostra quais laboratorios foram desbloqueados. Somente as leituras obrigatorias
da Formacao entram no percentual geral; referencias, solucoes e materiais
complementares permanecem disponiveis sem inflar ou bloquear o progresso.

```bash
bash estudo.sh
```

O launcher gera o catalogo diretamente dos arquivos do repositorio, instala as
dependencias com `npm ci --ignore-scripts` na primeira execucao, inicia o Vite somente em
`127.0.0.1` e abre Chrome/Chromium. Nao ha login, backend ou telemetria: o
progresso permanece no armazenamento local do navegador.

Use `bash estudo.sh --check` para verificar o ambiente sem instalar ou iniciar
nada, `--no-open` para nao abrir o navegador e `--port 4173` para escolher outra
porta local. Requisitos e detalhes de desenvolvimento estao no
**[guia da aplicacao](study-app/README.md)**.

---

## 📚 O que mudou na v2.1

Alem da base v2.0 (stack poliglota, `lib/`, CI, docker-lab):

- **Programação do zero à engenharia de APIs** (`00`–`05`), com Python,
  Java, C, C#, JavaScript, SQL/NoSQL, testes, arquitetura, aplicações,
  automação, Docker e Nginx.
- **Linux do zero ao kernel** (`06-Cheatsheets/linux-do-zero-ao-avancado/`),
  com 31 capítulos, 64 práticas, seis labs e exemplos executáveis.
- **Linux avançado e engenharia de kernel** (`07-Web-AppSec/linux-avancado/`),
  com 35 capítulos aprofundados, 72 práticas, nove gates, projeto de appliance,
  tracing, eBPF local, KVM, integridade e builds reproduzíveis, sem redes.
- **Windows doméstico do zero aos internals** (`08` e `09`), com instalação,
  Defender, PowerShell, PE/DLL, Sysinternals, performance e debugging.
- **Windows empresarial e Windows Server** (`10` e `11`), com Server Core,
  imagens, políticas, identidade, App Control, compliance e recuperação.
- **macOS do zero à engenharia empresarial** (`12` e `13`), com APFS,
  Darwin/XNU, Mach-O/dylibs, segurança, observabilidade, MDM e compliance.
- **Redes do zero à engenharia empresarial** (`14`–`18`), com IP, DNS, DHCP,
  HTTP, Wi-Fi, VLANs, switching, roteamento, OSPF/BGP, VPN, operações e um
  protocolo binário implementado. Os conteúdos anteriores foram preservados.
- **Criptografia do zero à engenharia pós-quântica** (`19`–`22`), com
  matemática, hashes/MAC/KDF, AEAD, RSA/ECC, PKI/TLS, gestão de chaves,
  criptoinventário e os padrões NIST ML-KEM, ML-DSA e SLH-DSA.
- **Privacidade, VPN e atribuição responsável** (`23`–`25`), com modelos de
  ameaça, metadados, WireGuard, telemetria, correlação e cadeia de custódia.
- **Purple Team na borda de aplicações** (`26`), com firewalls, WAF, OWASP CRS,
  Cloudflare, BunkerWeb, bots, rate limiting, Turnstile, MFA/passkeys e sete
  laboratórios pareados entre teste autorizado e defesa.
- **Especialização em segurança** (`27`–`40`), que transforma o acervo de
  Recon, OSINT, AD, Web/AppSec, cloud, containers, plataformas, C2, elevação de
  privilégios, movimento lateral, DFIR e CTI em uma sequência curricular com
  pré-requisitos e um capstone Purple Team. Os arquivos originais foram
  preservados e adotados pela nova rota, sem duplicação.
- **Aplicacao visual local em React**, com jornada sequencial `00` a `40`,
  filtros tematicos, busca, leitor Markdown,
  Biblioteca Completa, visualizador seguro de codigo/arquivos, progresso
  persistido no navegador e desbloqueio pedagogico de laboratorios.
- **Web deep-dives** SQLi/SSRF + labs guiados DVWA / Juice Shop / VAmPI.
- **BloodHound CE + NetExec** na documentacao operacional (substitui CME legado).
- **MITRE layer** alinhado à especialização avançada dos módulos 27–40.
- READMEs em todos os modulos; ROADMAP/CHANGELOG sincronizados.

Veja [CHANGELOG.md](CHANGELOG.md) para diff completo.

---

## 📁 Estrutura

```text
RedTeam-Essentials/
├── README.md / rte.py                 (documentacao e CLI unificada)
├── estudo.sh                         (launcher local da interface visual)
├── study-app/                        (React, Vite e catalogo gerado dos Markdown)
├── MODULE-CATALOG.json                (fonte canonica dos 41 modulos)
├── STUDY-CONTENT.json                 (cursos, acervos, colecoes e exclusoes explicitas)
├── CHANGELOG.md / ROADMAP.md / CONTRIBUTING.md / CODE_OF_CONDUCT.md / LICENSE
├── RESOURCES.md / REPORT-TEMPLATE.md / LAB-SETUP.md
├── report/                            (generate-pdf.sh → PDF via pandoc)
├── ATTACK_MAPPING_GUIDE.md / MITRE-ATTACK-MAPPING.json
├── validate_scripts.ps1               (lint + PSSA + checagens custom)
│
├── 00-Fundamentos/
│   └── programacao/                   (programação do zero, testes, API, SQLite, Docker e Nginx)
├── lib/                               NOVO em v2.0
│   ├── powershell/RTECommon.psm1      (logging, validacao, export)
│   ├── bash/rte_common.sh             (logging, traps, helpers)
│   └── python/rte_common.py           (logging, validacao, export)
│
├── 01-Recon/
│   └── programacao-avancada/          (SQL, NoSQL, MongoDB, APIs e projeto integrado)
├── 02-OSINT/
│   └── engenharia-software/           (17 capítulos, 5 labs e Dependency Planner)
├── 03-AD-Notes/
│   └── desenvolvimento-aplicacoes/    (17 capítulos, 5 labs e Study Desk)
├── 04-Automation/
│   └── automacao-profissional/        (15 capítulos, 5 labs, 30 práticas e FileFlow)
├── 05-DFIR/
│   └── engenharia-apis/               (REST, OpenAPI, GraphQL, gRPC e Contract Lab API)
├── 06-Cheatsheets/
│   └── linux-do-zero-ao-avancado/     (31 capítulos, labs, Bash/C e projeto)
├── 07-Web-AppSec/
│   └── linux-avancado/                (35 capítulos, labs, C/Bash e projeto)
├── 08-Cloud-RedTeam/
│   └── windows-domestico-fundamentos/ (18 capítulos, 48 práticas e 6 gates)
├── 09-C2-Evasion/
│   └── windows-domestico-avancado/    (20 capítulos, 56 práticas e 6 gates)
├── 10-Container-Sec/
│   └── windows-empresarial-fundamentos/ (Windows Server, 19 capítulos)
├── 11-Python-Tools/
│   └── windows-empresarial-avancado/  (identidade, políticas, 22 capítulos)
├── 12-Java-Tools/
│   └── macos-fundamentos/             (20 capítulos, seis labs e Python)
├── 13-Initial-Access/
│   └── macos-avancado/                (24 capítulos, sete labs e C/Python)
├── 14-Post-Exploitation/redes-fundamentos/           (Redes I)
├── 15-Hybrid-Identity/redes-domesticas/              (Redes II)
├── 16-CICD-Supply-Chain/switching-vlans/             (Redes III)
├── 17-macOS-Security/roteamento-vpns/                 (Redes IV)
├── 18-Mobile-Security/redes-empresariais-protocolos/ (Redes V)
├── 19-Wireless-Security/criptografia-fundamentos/    (Criptografia I)
├── 20-Offensive-Labs/criptografia-moderna/           (Criptografia II)
├── 21-Network-Pivoting/criptografia-aplicada/        (Criptografia III)
├── 22-Secure-Code-Review/engenharia-criptografica/   (Criptografia IV)
├── 23-Threat-Intel-Emulation/privacidade-anonimato-fundamentos/ (Privacidade I)
├── 24-Lateral-Movement/vpn-propria-operacao-segura/  (Privacidade II)
├── 25-Cursos/atribuicao-defensiva/                   (Privacidade III)
├── 26-Ofensivo-Defensivo/defesa-perimetro-aplicacoes/ (Purple Team: edge, WAF, bots e identidade)
│
├── 27-Operacoes-Seguranca-Avancadas/  (governança, RoE, laboratório e evidência)
│   └── acervo/                        (governança, histórico e scope guard)
├── 28-Engenharia-Ferramentas-Seguranca/
│   └── acervo/                        (automação, Python e Java)
├── 29-Reconhecimento-OSINT/            (Recon/OSINT, DNS e superficie de ataque)
│   ├── dns_enum.ps1 / dns_enum.sh
│   ├── passive_recon_cheatsheet.md / web_recon_notes.md
│   └── acervo/osint/
├── 30-Web-API-AppSec/                  (Web, APIs e code review)
│   ├── acervo/                         (Web/AppSec, labs e code review)
│   └── docker-lab/                     (alvos vulneráveis locais isolados)
├── 31-Active-Directory-Identidade/active-directory-identidade-hibrida/
├── 32-Cloud-Security/cloud-red-team/   (AWS, Azure e GCP)
├── 33-Containers-Supply-Chain/containers-kubernetes-cicd/
├── 34-Seguranca-Plataformas/macos-mobile-wireless/
├── 35-Acesso-Inicial-C2/acesso-inicial-c2-opsec/
├── 36-Escalacao-Privilegios/acervo/   (Linux e Windows)
├── 37-Pos-Exploracao-Movimento-Lateral/acervo/ (pós-exploração, pivoting e lateralidade)
├── 38-DFIR-Resposta-Incidentes/acervo/ (forense e resposta)
├── 39-Threat-Intel-Emulacao/acervo/    (CTI e adversary emulation)
├── 40-Capstone-Purple-Team/acervo/     (operação integrada final)
│
└── .github/workflows/
    ├── linguagens, Markdown, metadados e supply chain
    └── workflows dedicados para todas as formações
```

---

## 🚀 Quick Start

### 1. Clone

```bash
git clone https://github.com/Samuel-Ziger/RedTeam-Essentials.git
cd RedTeam-Essentials
```

### 2. Validar o projeto e consultar a trilha

```bash
python3 -m pip install -r requirements-crypto.txt
python3 rte.py modules --status active
python3 rte.py validate --all
```

A dependência fixada é necessária para os exemplos dos módulos 20–22.

### 3. Subir o lab local

```bash
python3 rte.py lab config
python3 rte.py lab up --build
python3 rte.py lab status
```

Acesse apenas os serviços do perfil escolhido, sempre em `localhost`:

| Perfil | Alvos |
|--------|-------|
| `basic` (padrão) | DVWA `:8081`, Juice Shop `:8082` e atacante |
| `api` | básico + VAmPI `:8087` |
| `extended` | básico + bWAPP `:8083` e WebGoat `:8084` |
| `full` | todos os serviços |

Por exemplo, `python3 rte.py lab up --profile api --build`. Os alvos permanecem
somente na rede interna e sem egress. Um gateway HTTP separado publica as URLs
em `127.0.0.1`; somente a estação atacante possui uma rede de egress para
instalar dependências. O isolamento limita exposição acidental, mas não
substitui RoE.

Labs Web do módulo 30, consolidados em `30-Web-API-AppSec/acervo/labs/`. Conecte na
estacao Kali:

```bash
docker compose -f 30-Web-API-AppSec/docker-lab/docker-compose.yml exec attacker bash
```

### 4. Use as ferramentas

**PowerShell (Windows ou PWSh em Linux):**

```powershell
Import-Module ./lib/powershell/RTECommon.psm1
./29-Reconhecimento-OSINT/dns_enum.ps1 -Domain lab.example -IncludeSubdomains -DryRun
./28-Engenharia-Ferramentas-Seguranca/acervo/automacao/organize_logs.ps1 -SourcePath ~/Downloads -TargetName HTB_Forest
```

**Bash:**

```bash
./29-Reconhecimento-OSINT/dns_enum.sh -d lab.example --subs --whois --dry-run -o ./output
sudo ./28-Engenharia-Ferramentas-Seguranca/acervo/automacao/linux_postinstall.sh --extra "ghidra"
```

**Python:**

```bash
python3 28-Engenharia-Ferramentas-Seguranca/acervo/python/subdomain_enum.py -d lab.example --resolve
python3 28-Engenharia-Ferramentas-Seguranca/acervo/python/port_scanner.py -t 127.0.0.1 -p 8081,8082 --banner
python3 28-Engenharia-Ferramentas-Seguranca/acervo/python/jwt_analyzer.py -t "$JWT"
```

**Java (ferramenta adotada pelo módulo 28):**

```bash
cd 28-Engenharia-Ferramentas-Seguranca/acervo/java
mkdir -p build
javac -d build src/main/java/io/redteam/essentials/PayloadGenerator.java
java -cp build io.redteam.essentials.PayloadGenerator --type xss --count 20
```

### 5. Executar as validações Purple Team da base

As demonstrações do módulo 26 processam apenas fixtures locais e não enviam
tráfego para a Internet:

```bash
python3 rte.py analyze edge-risk \
  26-Ofensivo-Defensivo/defesa-perimetro-aplicacoes/fixtures/requests-sinteticas.json
python3 rte.py analyze edge-policy \
  26-Ofensivo-Defensivo/defesa-perimetro-aplicacoes/fixtures/politica-edge.json
python3 rte.py analyze rate-limit \
  26-Ofensivo-Defensivo/defesa-perimetro-aplicacoes/fixtures/eventos-rate-limit.json
bash 26-Ofensivo-Defensivo/defesa-perimetro-aplicacoes/testar-curso.sh
```

---

## 🎓 Trilha de Aprendizado

Comece pelo **[Módulo 00](00-Fundamentos/README.md)** se ainda não domina
programação, terminal, testes, depuração e operação local segura. A formação
vai do primeiro `if/else` a exemplos nas cinco linguagens e a uma aplicação
com API, SQLite, JavaScript, Docker e Nginx, acompanhada por cinco laboratórios
progressivos.

Depois, o **[Módulo 01](01-Recon/README.md)** aprofunda engenharia de dados e
APIs: PostgreSQL, SQL avançado, NoSQL/MongoDB, contratos HTTP, concorrência,
idempotência, outbox, testes e uma API executável com dois bancos.

Os **[módulos 02](02-OSINT/README.md)** a
**[04](04-Automation/README.md)** concluem a base de engenharia: algoritmos,
estruturas de dados, arquitetura, refatoração, CLI/GUI/web, acessibilidade,
distribuição, idempotência, jobs, pipelines, integrações e automação
profissional nas cinco linguagens.

O **[Módulo 05](05-DFIR/README.md)** é a especialização em APIs: semântica HTTP,
REST, OpenAPI, identidade, segurança, resiliência, observabilidade, webhooks,
eventos, GraphQL, gRPC, streaming, SDKs e governança. A rota intercala 26
capítulos com 45 práticas, cinco laboratórios progressivos, diagnóstico e a
Contract Lab API executável.

O **[Módulo 06](06-Cheatsheets/README.md)** inicia a formação de sistemas
operacionais com Linux do zero ao kernel: distribuições, instalação, arquivos,
processos, memória, armazenamento, boot, systemd, segurança, containers,
drivers e desempenho. A rota intercala 31 capítulos, 64 práticas, seis
laboratórios, diagnóstico por evidências e código real em Bash, AWK, Python e
C. Redes ficam nos módulos 14–18; aqui a conectividade limita-se ao host.

O **[Módulo 07](07-Web-AppSec/README.md)** aprofunda Linux em nível de engenharia:
fonte e ABI do kernel, scheduler/RCU, MM/NUMA, VFS/bloco, boot confiável,
systemd/cgroups, perf/tracing/eBPF local, debugging, KVM, LSM, integridade,
distribuições e contribuição. Redes foram reservadas para um módulo próprio.

Os **[módulos 08](08-Cloud-RedTeam/README.md)** e
**[09](09-C2-Evasion/README.md)** formam a trilha Windows doméstica: começam na
instalação, arquivos, contas, configuração, Defender e PowerShell; avançam para
arquitetura NT, processos, memória, PE/DLL, ETW, Sysinternals, VBS e WinDbg.
O módulo 08 inclui agora guia de diagnóstico, scripts PowerShell testados,
progressão semântica de laboratórios e capstone de recuperação por terceiro.
O módulo 09 acrescenta parser PE com validação de limites, DLL C com ABI segura,
guia de tracing/debugging, 56 práticas, seis gates e o Diagnostic Workbench.

Os **[módulos 10](10-Container-Sec/README.md)** e
**[11](11-Python-Tools/README.md)** formam a trilha empresarial: Windows Server,
Server Core, storage, servicing, backup, Hyper-V, imagens, deployment, AD/GPO,
LAPS/gMSA, PKI, JEA, App Control, Defender, compliance e continuidade. Partes
distribuídas são modeladas offline e podem ser aprofundadas na trilha 14–18.

Os **[módulos 12](12-Java-Tools/README.md)** e
**[13](13-Initial-Access/README.md)** formam a trilha macOS: começam em Finder,
APFS, contas, Terminal, backup e proteções nativas; avançam para Darwin/XNU,
Mach-O/`dyld`, assinatura, TCC, observabilidade, perfis, MDM/DDM, identidade e
compliance. Integrações distribuídas podem ser aprofundadas na trilha 14–18.

Os **[módulos 14](14-Post-Exploitation/README.md)** a
**[18](18-Mobile-Security/README.md)** formam a trilha de redes: fundamentos,
IPv4/IPv6, DNS, DHCP e HTTP; redes domésticas e Wi-Fi; switching/VLANs; OSPF,
BGP e VPNs; arquitetura empresarial, observabilidade, automação e engenharia
de protocolos. Todos os exercícios iniciais funcionam offline.

Os **[módulos 19](19-Wireless-Security/README.md)** a
**[22](22-Secure-Code-Review/README.md)** formam a trilha de criptografia:
fundamentos matemáticos, aleatoriedade, hash/MAC/KDF; AES-GCM,
ChaCha20-Poly1305, RSA, X25519 e Ed25519; PKI, X.509, TLS, SSH, proteção de
senhas/dados; engenharia de protocolos, HSM/KMS, agilidade e pós-quântica.

Os **[módulos 23](23-Threat-Intel-Emulation/README.md)** a
**[25](25-Cursos/README.md)** formam a trilha de privacidade: modelos de ameaça,
metadados, VPN, proxy, Tor e fingerprinting; implantação e operação segura de
WireGuard em VPS própria; telemetria, NAT/CGNAT, correlação, cadeia de custódia
e atribuição defensiva responsável.

O **[Módulo 26](26-Ofensivo-Defensivo/README.md)** fecha a base obrigatória com
uma introdução Purple Team em borda de aplicações: firewalls de rede/host/cloud,
CDN e origem, DDoS, WAF/OWASP CRS, Cloudflare, BunkerWeb, detecção de bots,
rate limiting, CAPTCHA/Turnstile, 2FA, WebAuthn/passkeys, observabilidade e
resposta. Cada controle é avaliado no laboratório pelo Red Team e validado,
ajustado e retestado com o Blue Team.

### Especialização em segurança (`27`–`40`)

Depois da base completa, siga a especialização nesta ordem. Os arquivos do
acervo anterior permanecem em seus caminhos originais para preservar links,
histórico e automações; os novos módulos são a camada curricular que os organiza.

| Módulo | Tema | Papel na sequência |
|---:|---|---|
| [27](27-Operacoes-Seguranca-Avancadas/README.md) | Governança, laboratório e evidência | Gate obrigatório após `00`–`26`. |
| [28](28-Engenharia-Ferramentas-Seguranca/README.md) | Engenharia de ferramentas | Converte programação em automação segura e auditável. |
| [29](29-Reconhecimento-OSINT/README.md) | Reconhecimento e OSINT | Mapeia superfície com proveniência e escopo. |
| [30](30-Web-API-AppSec/README.md) | Web, APIs e code review | Liga teste local, causa-raiz, patch e regressão. |
| [31](31-Active-Directory-Identidade/README.md) | Active Directory e identidade híbrida | Analisa grafos de identidade e caminhos de privilégio. |
| [32](32-Cloud-Security/README.md) | AWS, Azure e GCP | Aplica identidade e telemetria a ambientes cloud. |
| [33](33-Containers-Supply-Chain/README.md) | Containers, Kubernetes e CI/CD | Estende o modelo à cadeia de entrega e workloads. |
| [34](34-Seguranca-Plataformas/README.md) | macOS, mobile e wireless | Compara fronteiras e controles de plataformas. |
| [35](35-Acesso-Inicial-C2/README.md) | Acesso inicial, C2, evasão e OPSEC | Planeja emulação controlada e observável. |
| [36](36-Escalacao-Privilegios/README.md) | Elevação de privilégios | Valida e corrige caminhos locais em Linux e Windows. |
| [37](37-Pos-Exploracao-Movimento-Lateral/README.md) | Pós-exploração, pivoting e lateralidade | Mede alcance, segmentação e contenção. |
| [38](38-DFIR-Resposta-Incidentes/README.md) | DFIR e resposta a incidentes | Preserva e interpreta a evidência produzida. |
| [39](39-Threat-Intel-Emulacao/README.md) | Threat intelligence e emulação | Transforma inteligência em hipóteses testáveis. |
| [40](40-Capstone-Purple-Team/README.md) | Capstone Purple Team | Integra escopo, execução, defesa, correção e reteste. |

As ferramentas principais também estão disponíveis pela CLI:

```bash
python3 rte.py analyze privacy 23-Threat-Intel-Emulation/privacidade-anonimato-fundamentos/fixtures/cenario-pesquisa.json
python3 rte.py analyze vpn-plan 24-Lateral-Movement/vpn-propria-operacao-segura/fixtures/vpn-plan.json
python3 rte.py analyze telemetry 25-Cursos/atribuicao-defensiva/fixtures/eventos-sinteticos.json
python3 rte.py analyze edge-risk 26-Ofensivo-Defensivo/defesa-perimetro-aplicacoes/fixtures/requests-sinteticas.json
python3 rte.py analyze edge-policy 26-Ofensivo-Defensivo/defesa-perimetro-aplicacoes/fixtures/politica-edge.json
```

### Mapa da formação principal

| Etapa | Módulos | Resultado esperado |
|---|---|---|
| Programação e software | 00–05 | construir, testar, distribuir e operar aplicações e APIs |
| Sistemas operacionais | 06–13 | administrar e compreender Linux, Windows e macOS até internals |
| Redes | 14–18 | projetar redes domésticas e empresariais e implementar protocolos |
| Criptografia | 19–22 | aplicar primitivas, PKI/TLS, gestão de chaves e criptoagilidade |
| Privacidade | 23–25 | modelar rastros, operar VPN própria e investigar com responsabilidade |
| Purple Team fundamental | 26 | avaliar e defender firewalls, WAF, bots, desafios e identidade |
| Especialização em segurança | 27–40 | conduzir operações autorizadas, produzir evidência e concluir o capstone Purple Team |

### Trilhas por objetivo

| Objetivo | Ordem sugerida |
|----------|----------------|
| Formação completa | 00 → 01 → … → 26 → 27 → 28 → … → 40 |
| Engenharia de APIs | 00 → 01 → 02 → 03 → 04 → 05/engenharia-apis |
| Linux e engenharia de sistemas | 00 → 01 → 02 → 03 → 04 → 05 → 06 → 07 |
| AppSec e APIs | Base 00–26 → 27 → 28 → 29 → 30 |
| Engenharia de software | 00 → 01 → 02/engenharia-software → projeto autoral |
| Aplicações profissionais | 00 → 01 → 02 → 03/desenvolvimento-aplicacoes |
| Automação profissional | 00 → 01 → 02 → 03 → 04/automacao-profissional |
| Windows do zero ao empresarial | 00 → 08 → 09 → 10 → 11 |
| macOS do zero ao empresarial | 00 → 12 → 13 |
| Active Directory | Base 00–26 → 27 → 28 → 29 → 31 |
| Redes do zero à engenharia | 00 → 14 → 15 → 16 → 17 → 18 |
| Criptografia do zero à engenharia | 00 → 02 → 19 → 20 → 21 → 22 |
| Privacidade, VPN e atribuição defensiva | 00 → 06 → 14–18 → 19–22 → 23 → 24 → 25 |
| Cloud e containers | Base 00–26 → 27 → 29 → 31 → 32 → 33 |
| Operações Red/Purple Team | Base 00–26 → 27 → 28 → … → 39 → 40 |
| DFIR e threat intelligence | Base 00–26 → 27 → 31–37 → 38 → 39 → 40 |
| WAF, firewalls, bots e identidade | 00 → 05 → 14 → 18 → 21 → 25 → 26 → 27 → 30 → 40 |

Veja **[ROADMAP.md](ROADMAP.md)** para detalhes por semana.

### Cursos e conteúdo em vídeo

Cada módulo da base `00`–`26` contém uma seção com pelo menos cinco vídeos em
português sobre seu próprio tema. Na especialização `27`–`40`, os materiais
adotados mantêm suas referências originais, enquanto os novos READMEs definem a
ordem, os pré-requisitos e as entregas curriculares.

---

## 🛠️ Stack Tecnologica

| Camada | Tecnologia |
|--------|-----------|
| Shell | PowerShell 7+, Bash 4+ |
| Backend / scripts | Python 3.10+, Java 17+ |
| Interface de estudos | React 19, Vite 8, Markdown sanitizado e `localStorage` |
| Containers | Docker, Docker Compose, Kubernetes (manifests) |
| Borda de aplicações | Nginx, OWASP CRS, Cloudflare e BunkerWeb |
| Identidade | TOTP, WebAuthn/passkeys, OAuth/OIDC e mTLS |
| CI/CD | GitHub Actions (22 workflows) |
| Linters | PSScriptAnalyzer, ShellCheck, Ruff, markdownlint, Lychee |
| Frameworks de pentest | Nmap, Impacket, NetExec, BloodHound, Burp Suite |

---

## 🎯 MITRE ATT&CK Coverage

| Tatica | Tecnicas | Modulos |
|--------|----------|---------|
| Reconnaissance (TA0043) | T1590, T1592, T1593, T1594, T1596, T1598 | 29 |
| Initial Access (TA0001) | T1078, T1133, T1190, T1566 | 30, 35 |
| Execution (TA0002) | T1059, T1610 | 06 |
| Persistence (TA0003) | T1098, T1547, T1053, T1543 | 31, 37 |
| Privilege Escalation (TA0004) | T1078, T1611, T1068, T1548, T1134 | 31, 33, 36 |
| Stealth / Defense Impairment | T1027, T1055, T1070, T1685 | 35, 38 |
| Credential Access (TA0006) | T1003, T1110, T1552, T1558.003, T1558.004 | 31, 36 |
| Discovery (TA0007) | T1069, T1083, T1087, T1482, T1580, T1613 | 29, 31, 32, 33 |
| Lateral Movement (TA0008) | T1021, T1550 | 37 |
| Collection (TA0009) | T1119, T1530, T1005 | 37, 38 |
| Exfiltration (TA0010) | T1041, T1048 | 37 |
| Command & Control (TA0011) | T1071, T1573, T1090 | 35, 37 |

Layer JSON pronto para o **ATT&CK Navigator**: [`MITRE-ATTACK-MAPPING.json`](MITRE-ATTACK-MAPPING.json). Detalhes em [`ATTACK_MAPPING_GUIDE.md`](ATTACK_MAPPING_GUIDE.md).

---

## 🤝 Contribuindo

Veja [CONTRIBUTING.md](CONTRIBUTING.md). Resumo:

1. Fork + branch (`feature/<topico>`).
2. Siga padroes - PowerShell com `Set-StrictMode`, Bash com `set -euo pipefail`, Python passa `ruff check`.
3. Rode `python3 rte.py validate --all` antes do PR.
4. PR com descricao clara, mapeamento ATT&CK se aplicavel.

---

## 📚 Documentacao Expandida

- 🖥️ **[study-app/README.md](study-app/README.md)** - Executar, validar e
  desenvolver a interface visual local de estudos.
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

MIT. Veja [LICENSE](LICENSE). A postura operacional está em
[ETHICAL-USE.md](ETHICAL-USE.md) e a divulgação responsável em
[SECURITY.md](SECURITY.md).

---

## ⭐ Apoie

Se este repositorio te ajudou, deixe uma estrela e compartilhe com quem esta aprendendo seguranca ofensiva.

> **Com grandes poderes vem grandes responsabilidades. Use este conhecimento para o bem.**
