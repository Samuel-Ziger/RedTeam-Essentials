# Changelog

Todas as mudanças notáveis neste projeto serão documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/),
e este projeto adere ao [Semantic Versioning](https://semver.org/lang/pt-BR/).

---

## [Unreleased]

### Adicionado

- **Vídeos por módulo** - curadoria de cinco vídeos em português incorporada a
  cada README dos módulos 00–24.
- **Módulo 25** - catálogo exclusivo de cursos completos, iniciado com as
  trilhas da Solyd e DESEC e preparado para inclusões futuras.
- **Validador de vídeos** - teste offline das 25 seções distribuídas e do mínimo
  de cinco vídeos distintos por módulo.
- **00-Fundamentos** - redes, sistemas, identidade, RoE, laboratório seguro e autoavaliação.
- **Testes Python** - suite pytest offline para biblioteca comum, parsers e ferramentas.
- **Testes Bash, PowerShell e Java** - validações offline das bibliotecas e do gerador.
- **Validador ATT&CK** - invariantes do layer JSON verificadas localmente e no CI.
- **Labs reproduzíveis** - respostas/rubrica para três labs Web e datasets sintéticos para DFIR e Kubernetes.
- **Detecção verificável** - padrão comum e exemplos para AD, Web/API, cloud e containers.
- **Cloud offline** - fixtures IAM AWS/Azure/GCP, analisador normalizado e respostas orientativas sem contas ou custos.
- **Compose seguro** - healthchecks, limites de CPU/memória, profiles e validador de bindings localhost.
- **Trilhas avançadas** - identidade híbrida, APIs modernas, CI/CD supply chain e microemulação Purple Team offline.
- **Novas trilhas defensivas** - macOS, mobile e wireless com exercícios seguros e cleanup.
- **Métricas** - inventário reproduzível de módulos, contratos, testes e fixtures.
- **Operações ofensivas** - scope guard, correlação de recon, matriz BOLA/BFLA e roteiro integrado de cinco operações.
- **Módulos 21–23** - pivoting offline, code review ofensivo e threat-intel/adversary emulation.
- **Módulo 24** - movimentação lateral com grafo sintético, precondições, telemetria e cleanup.
- **Movimentação lateral Linux** - SSH/certificados, bastion, sudo, NFS, automação e sockets com path offline.
- **Contrato editorial** - template reutilizável em `docs/MODULE-TEMPLATE.md`.
- **Lab doctor** - diagnóstico do Compose, containers e endpoints HTTP locais.
- **06-Cheatsheets/windows_privesc_teoria.md** - Windows Privilege Escalation (enum, UAC, services, tokens, checklist, defesa).
- **06-Cheatsheets** - metodologia + cheatsheet Windows e PATH hijacking Linux (adaptado HexSec/MIT, PT).
- **07-Web-AppSec** - deep-dives SQLi/SSRF + labs guiados DVWA, Juice Shop e VAmPI (`labs/`).
- **07-Web-AppSec** - enum web avancado (dirs/vhosts/params/AXFR) e path traversal/LFI (adaptado HexSec/MIT, PT).
- **13-Initial-Access** - phishing teorico (T1566) e servicos externos (VPN/RDP/OWA/T1190).
- **14-Post-Exploitation** - collection/exfil e persistencia overview eticos.
- **report/** - `generate-pdf.sh` (pandoc/eisvogel) para PDF a partir do template.
- READMEs de modulo para 02-OSINT, 03-AD-Notes, 05-DFIR, 06-Cheatsheets.
- Exercicios praticos e checklists em Cloud (08) e Container (10).
- MITRE ATT&CK layer expandido para modulos 07-14 (v2.1 coverage).

### Modificado
- Python padronizado em 3.10+; CI agora executa os testes offline.
- Scanner valida faixas invertidas/vazias e a lista `top100` contém exatamente 100 portas.
- `PayloadGenerator` compila no Java 17 sem autorreferência nos valores do enum.
- README inclui trilhas por objetivo e direciona iniciantes ao módulo 00.
- Todos os READMEs de módulo agora declaram público, pré-requisitos, tempo, ambiente, evidência e conclusão.
- ROADMAP alinhado a v2.1 (Windows Privesc, Initial Access, Post-Ex; removidos checkmarks sem artefato).
- BloodHound CE (SpecterOps) documentado; CrackMapExec -> NetExec (`nxc`) em docs/scripts/lab.
- `docker-lab`: attacker usa build `Dockerfile.kali-pentest`; README raiz lista todos os alvos.
- CI Lychee com `fail: true`.
- `IMPLEMENTATION_SUMMARY.md` marcado como historico (ver CHANGELOG).

---

## [2.0.0] - 2026-05-20

### Major upgrade - estrutura, stack poliglota e cobertura ampliada

#### Adicionado

##### Biblioteca comum (`lib/`)
- `lib/powershell/RTECommon.psm1` - logger com niveis, validacao (dominio/IPv4), banner, retries, export JSON/CSV/TXT, helper de autorizacao etica, `Test-RTEAdmin` cross-platform.
- `lib/bash/rte_common.sh` - logger colorido, traps de cleanup/ERR, `require_cmd`, `require_root`, validacoes, `run_cmd` com suporte a dry-run via `RTE_DRYRUN=1`.
- `lib/python/rte_common.py` - logging colorido, `RTEContext`, `confirm_authorization`, `export_json`, sem dependencias externas.

##### Novos modulos
- **07-Web-AppSec** - OWASP Top 10 (2021), API Security Checklist (OWASP API Top 10:2023), recon web pratico (subfinder/httpx/katana/nuclei), XSS deep dive (Trusted Types, CSP bypasses, polyglots), padroes de auth bypass.
- **08-Cloud-RedTeam** - AWS (IMDS, IAM privesc com Pacu, S3, KMS), Azure (device code, ROADtools, AzureHound, Managed Identity), GCP (metadata, SA impersonation, GCS, Workload Identity), comparativo de ferramentas.
- **09-C2-Evasion** (teoria apenas) - frameworks (Sliver, Mythic, Havoc, Cobalt Strike), AMSI/ETW/EDR fundamentals, OpSec checklist.
- **10-Container-Sec** - tecnicas de Docker escape (privileged, socket, capabilities), Kubernetes attack paths (RBAC, kubelet, etcd, SSRF -> metadata), hardening baseline (PSS restricted, NetworkPolicy, Kyverno).
- **11-Python-Tools** - subdomain_enum (crt.sh + HackerTarget + OTX + asyncio resolve), port_scanner (asyncio TCP + banner grab), jwt_analyzer (analise estatica + HS\* bruteforce), hash_identifier.
- **12-Java-Tools** - PayloadGenerator (XSS/SQLi/CMDi/SSTI/SSRF/LFI/XXE com encoding URL/Base64 e amostragem aleatoria).

##### Lab Docker (`docker-lab/`)
- docker-compose com DVWA, Juice Shop, bWAPP, WebGoat, VulnerableWordPress, NodeGoat, VAmPI e estacao Kali atacante em rede isolada `172.28.0.0/24`.
- Dockerfile.kali-pentest com ferramentas pre-instaladas.
- README com exemplos de sessao end-to-end.

##### CI/CD (`.github/workflows/`)
- `powershell.yml` - PSScriptAnalyzer + parser syntax check.
- `bash.yml` - ShellCheck + `bash -n`.
- `python.yml` - Ruff (lint + format) + py_compile em Python 3.10/3.11/3.12.
- `java.yml` - javac com `-Xlint:all -Werror` + smoke test.
- `markdown.yml` - markdownlint-cli2 + Lychee link check.
- `.markdownlint.json` na raiz.

##### Conteudo atualizado (2024-2026)
- `03-AD-Notes/modern-ad-attacks-2026.md` - ADCS (ESC1, ESC8), RBCD, Shadow Credentials, SCCM abuse, PKINIT, KrbRelayUp.
- `06-Cheatsheets/linux_privesc_modern.md` - CVEs kernel 2022-2026 (DirtyPipe, OverlayFS, nf_tables UAF), capabilities modernas, eBPF post-exploitation.
- `01-Recon/dns_enum.sh` - alternativa Linux do dns_enum.ps1 com dig + crt.sh.
- `04-Automation/ad_recon.sh` - wrapper Linux para nmap + NetExec + Impacket (GetNPUsers, GetUserSPNs).

#### Modificado

- **`01-Recon/dns_enum.ps1`** - reescrito v2.0: cross-platform (Resolve-DnsName em Windows, dig fallback em Linux), Certificate Transparency via crt.sh, exportacao JSON estruturada, retries com backoff, dry-run real, validacao de dominio rigorosa.
- **`04-Automation/organize_logs.ps1`** - INDEX.md gerado com SHA-256 de cada arquivo, suporte -CopyMode, -DryRun, classificacao por regex + extensao.
- **`04-Automation/windows_setup_clean.ps1`** - integracao Chocolatey, dry-run, ExtraPackages, tweaks Explorer, validacao de admin.
- **`04-Automation/linux_postinstall.sh`** - deteccao de distro (Kali/Parrot/Ubuntu/Debian), pacotes essenciais expandidos, SecLists clone, aliases idempotentes, dry-run.
- **`validate_scripts.ps1`** - usa PSScriptAnalyzer real (instalado on-demand), severity configuravel, custom rules pluggable.
- **`README.md`** - reescrito para refletir v2.0, com tabela completa de modulos, ATT&CK coverage expandida, quick start poliglota.
- **`03-AD-Notes/kerberoasting_teoria.md`** - typo "Cracke\n\nar" corrigido; adicionada secao "Atualizacao 2024-2026" com etypes AES vs RC4 e tools modernas.

#### Corrigido

- Bug de quebra de linha em `kerberoasting_teoria.md`.
- Operadores `??` e `?:` (PS 7-only) substituidos por `if/else` para compatibilidade PS 5.1.
- Encoding consistente (UTF-8 sem BOM) em todos os arquivos.

---

## [1.0.0] - 2025-11-22

### 🎉 Lançamento Inicial Completo

Este é o primeiro lançamento oficial do RedTeam Essentials com documentação expandida, sistema de validação e recursos profissionais.

### ✨ Adicionado

#### Documentação Principal
- **ROADMAP.md** - Trilha completa de aprendizado estruturada em 4 tiers (Iniciante → Profissional)
  - Integração completa com MITRE ATT&CK Framework
  - Tempo estimado para cada módulo
  - Pré-requisitos claros para progressão
  - Mapeamento de certificações recomendadas
  - Checklist de progresso

- **CONTRIBUTING.md** - Guia detalhado de contribuição
  - Templates de Pull Request e Issues
  - Padrões de código para PowerShell e Bash
  - Convenções de commit (Conventional Commits)
  - Guidelines de documentação Markdown
  - Developer Certificate of Origin (DCO)
  - Boas práticas de desenvolvimento

- **LAB-SETUP.md** - Guia completo de configuração de laboratório
  - Setup de VMs (VMware, VirtualBox, Hyper-V)
  - Configuração de Active Directory lab
  - Projetos prontos (GOAD, BadBlood, Metasploitable)
  - Plataformas online gratuitas (TryHackMe, HTB, OWASP, etc.)
  - Scripts de configuração automatizada
  - Troubleshooting comum

- **REPORT-TEMPLATE.md** - Template profissional para relatórios Red Team
  - Sumário executivo para C-Level
  - Resumo técnico detalhado
  - Formato de achados com CVSS e MITRE ATT&CK
  - Timeline de ataque e kill chain
  - Recomendações priorizadas
  - Apêndices completos

- **README.md nos módulos** - Documentação individual para cada módulo
  - `01-Recon/README.md` - Guia completo de reconhecimento
  - Objetivos de aprendizado claros
  - Exercícios práticos com validação
  - Mapeamento MITRE ATT&CK
  - Recursos adicionais

#### Sistema de Validação e Testes
- **validate_scripts.ps1** - Sistema automatizado de validação
  - Validação de sintaxe PowerShell
  - Verificação de boas práticas
  - Detecção de headers e documentação
  - Verificação de tratamento de erros
  - Relatório consolidado de todos os scripts

#### Melhorias em Scripts Existentes
- Todos os scripts PowerShell já possuem:
  - Headers completos com `.SYNOPSIS`, `.DESCRIPTION`, `.NOTES`
  - Tratamento robusto de erros (`try/catch`)
  - Logging com cores
  - Validação de parâmetros
  - Disclaimers de segurança
  - Comentários linha por linha

#### Badges e Metadata
- Badges de versão, licença, tecnologias
- Badge do MITRE ATT&CK
- Badges de status do projeto
- Informações de versionamento

### 🔧 Melhorado

#### README.md Principal
- Reorganização completa da estrutura
- Seção de "TIER" para clarificar público-alvo
- Links para toda nova documentação
- Seção expandida de recursos online
- Processo de contribuição detalhado
- Estatísticas do projeto
- Roadmap futuro (Q1-Q3 2026)
- Créditos e atribuições claras ao autor (Samuel Ziger)
- Versionamento e changelog integrado

#### Scripts PowerShell
- `dns_enum.ps1` - Já estava bem documentado, mantido
- `osint_automation.ps1` - Já estava bem documentado, mantido
- `windows_setup_clean.ps1` - Já estava bem documentado, mantido
- `organize_logs.ps1` - Já estava bem documentado, mantido

#### Scripts Bash
- `linux_postinstall.sh` - Já estava bem documentado, mantido

### 📚 Documentação

#### Padrões Estabelecidos
- Padrão de header para scripts PowerShell
- Padrão de header para scripts Bash
- Template de documentação Markdown
- Convenções de nomenclatura
- Estrutura de diretórios

#### Mapeamento MITRE ATT&CK
- Integração completa no ROADMAP
- Mapeamento por módulo
- IDs de técnicas em achados de relatório
- Links para documentação oficial

#### Recursos de Aprendizado
- Lista expandida de plataformas online
- Labs gratuitos e pagos
- Livros recomendados por tier
- Canais do YouTube
- Comunidades e Discord

### 🛡️ Segurança

#### Disclaimers Expandidos
- Avisos éticos em todos os scripts
- Seção de limitações e restrições
- Validação de ambiente de laboratório
- Alertas sobre uso não autorizado

#### Validações de Ambiente
- Detecção de execução como administrador
- Verificação de conectividade
- Validação de formato de domínios
- Checks de pré-requisitos

### 🎯 MITRE ATT&CK

#### Cobertura de Técnicas
- TA0043 - Reconnaissance (múltiplas técnicas)
- TA0006 - Credential Access (Kerberoasting, etc.)
- TA0007 - Discovery
- TA0008 - Lateral Movement
- Total: 30+ técnicas mapeadas

### 🏗️ Infraestrutura

#### Sistema de CI/CD (Futuro)
- Preparação para GitHub Actions
- Validação automática de PRs
- Testes automatizados de scripts
- Geração automática de releases

### 📊 Métricas

#### Estatísticas do Projeto
- 5 scripts PowerShell totalmente documentados
- 1 script Bash com validações completas
- 15+ documentos Markdown (teoria e guias)
- 30+ técnicas MITRE ATT&CK cobertas
- 10+ exercícios práticos
- 40+ horas de conteúdo de estudo

### 🌍 Comunidade

#### Recursos para Comunidade
- Templates de issue
- Templates de pull request
- Discussões no GitHub habilitadas (futuro)
- Canais de suporte documentados

---

## [0.1.0] - 2025-11-01

### 🎉 Lançamento Inicial

#### ✨ Adicionado

- Estrutura inicial do repositório
- Módulos principais:
  - `01-Recon/` - Reconhecimento e DNS enumeration
  - `02-OSINT/` - OSINT automation
  - `03-AD-Notes/` - Active Directory notes
  - `04-Automation/` - Scripts de automação
  - `05-DFIR/` - Digital Forensics & Incident Response
  - `06-Cheatsheets/` - Cheatsheets de referência

#### 📝 Scripts Criados

**PowerShell:**
- `dns_enum.ps1` - Enumeração DNS automatizada
- `osint_automation.ps1` - Coleta OSINT automatizada
- `windows_setup_clean.ps1` - Setup de ambiente Windows
- `organize_logs.ps1` - Organizador de logs

**Bash:**
- `linux_postinstall.sh` - Pós-instalação Linux/Kali

#### 📚 Documentação Inicial

- README.md básico
- LICENSE (MIT)
- Documentação teoria em Markdown:
  - `passive_recon_cheatsheet.md`
  - `web_recon_notes.md`
  - `osint-tools-list.md`
  - `ad_enum_commands.md`
  - `kerberoasting_teoria.md`
  - `bloodhound_teoria.md`
  - `forensics_artifacts.md`
  - `memory_analysis_teoria.md`
  - `windows_event_logs.md`
  - `linux_privesc_teoria.md`
  - `powershell_cheatsheet.md`
  - `windows_lateral_movement_teoria.md`

---

## Planejado (pos-v2.1)

- [ ] Labs Terraform/Ansible para AD/cloud (quando houver codigo no repo)
- [ ] Deep-dives adicionais (deserialization, IDOR avancado)
- [ ] Mobile / Wireless tracks
- [ ] Purple-team exercises pareados ataque/deteccao
- [ ] Videos / CTF proprio (somente apos artefatos existirem)

---

## Tipos de Mudanças

- **✨ Adicionado** - Novas funcionalidades
- **🔧 Melhorado** - Melhorias em funcionalidades existentes
- **🐛 Corrigido** - Correções de bugs
- **🗑️ Removido** - Funcionalidades removidas
- **🔒 Segurança** - Melhorias de segurança
- **📚 Documentação** - Mudanças na documentação
- **🎨 Estilo** - Mudanças que não afetam o código
- **♻️ Refatoração** - Mudanças de código sem alterar funcionalidade
- **⚡ Performance** - Melhorias de performance
- **✅ Testes** - Adição ou correção de testes

---

## Links

- [Repositório GitHub](https://github.com/Samuel-Ziger/RedTeam-Essentials)
- [Issues](https://github.com/Samuel-Ziger/RedTeam-Essentials/issues)
- [Pull Requests](https://github.com/Samuel-Ziger/RedTeam-Essentials/pulls)
- [Releases](https://github.com/Samuel-Ziger/RedTeam-Essentials/releases)

---

<div align="center">

**Mantido por:** Samuel Ziger  
**Licença:** MIT  
**Última Atualização:** 22 de Novembro de 2025

</div>
