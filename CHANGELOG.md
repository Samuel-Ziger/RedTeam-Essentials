# Changelog

Todas as mudanças notáveis neste projeto serão documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/),
e este projeto adere ao [Semantic Versioning](https://semver.org/lang/pt-BR/).

---

## [Unreleased]

### Adicionado

- **Separação física entre base e segurança avançada** - o Módulo 01 agora
  contém exclusivamente programação, dados e APIs; Recon/DNS foi transferido
  para o Módulo 29 e o laboratório web vulnerável para o Módulo 30, com
  catálogo, CLI, testes, CI e documentação atualizados para os novos caminhos.
- **Módulo 00 aprofundado** - curso-base reescrito com modelos mentais,
  contratos, invariantes, rastreamento, complexidade, depuração orientada por
  evidências, exemplos reais nas cinco linguagens, caderno de práticas e cinco
  laboratórios progressivos até a entrega do TaskBoard com API, SQLite, Docker
  e Nginx.
- **Especialização avançada nos módulos 27–40** - o acervo de segurança
  passou a integrar uma sequência curricular própria, posterior à base
  obrigatória 00–26, da governança e engenharia de ferramentas ao capstone
  Purple Team integrado.
- **Sétima área de aprendizagem** - o currículo ativo agora possui 41 módulos
  em sete áreas: 27 de base e 14 de especialização em segurança.
- **Realocação curricular sem duplicação** - os acervos avançados foram
  transferidos fisicamente dos módulos 00–26 para 27–40; manifesto, links,
  testes, CLI e CI agora apontam para os destinos canônicos.
- **CLI `rte.py`** - navegação do catálogo, validações, scope gate,
  analisadores offline, operação do lab e geração de relatório.
- **Supply chain** - scanner offline de segredos, SBOM CycloneDX, Dependabot e
  workflow dedicado com Actions fixadas por SHA.
- **Catálogo canônico** - `MODULE-CATALOG.json` e validador dos 41 módulos.
- **Aplicacao visual de estudos** - interface React/Vite local com jornada direta
  dos modulos 00 a 40, sete areas tematicas como filtros secundarios, busca,
  leitor Markdown sanitizado, retomada do ultimo conteudo, progresso por modulo
  e liberacao de laboratorios conforme as leituras concluidas.
- **Launcher `estudo.sh`** - valida Python/npm e a versao do Node.js, gera o
  catalogo, instala pelo lockfile quando necessario, limita o Vite a
  `127.0.0.1`, aguarda o health check e abre Chrome/Chromium com cleanup seguro.
- **Progresso privado e local** - nenhuma conta ou API foi adicionada; leituras,
  ultimo ponto e laboratorios concluidos ficam no `localStorage` do navegador.
- **Catalogo visual reproduzivel** - gerador Python copia conteudo permitido com
  validacao de caminhos e monta metadados deterministas diretamente dos 41
  modulos, sem versionar `public/generated`.
- **Biblioteca Completa** - separa Formacao, especializacao em seguranca,
  laboratorios/projetos, ferramentas/codigo e documentacao global, com busca e
  rotas proprias para Markdown, codigo, configuracoes, dados e imagens.
- **Cobertura verificavel do currículo** - `STUDY-CONTENT.json` identifica os
  41 cursos, nomeia Recon/OSINT/AD/DFIR/Web/Cloud/C2 e os demais domínios,
  registra exclusões de infraestrutura e exige zero material elegível sem
  coleção.
- **Progresso curricular correto** - apenas leituras obrigatorias da Formacao
  entram no percentual; legado, referencias, respostas e solucoes continuam
  pesquisaveis sem bloquear a conclusao.
- **Preservacao historica integral** - indices legados dos modulos 05-13 e
  19-22 restauram o conteudo substantivo anterior sem substituir os cursos
  atuais; links do lab Docker foram alinhados a `30-Web-API-AppSec/docker-lab/`.
- **CI da aplicacao** - validador offline, testes Python/JavaScript, build Vite e
  workflow com Actions fixadas por SHA.
- **Governança** - política de segurança, uso ético e templates de contribuição.
- **Gateway local do lab** - proxy Nginx em `127.0.0.1` mantém os alvos sem
  portas publicadas e sem egress, inclusive nas versões atuais do Docker.
- **Curso de programação no módulo 00** - trilha autocontida do zero ao
  avançado em Python, Java, C, C# e JavaScript, com algoritmos, testes, web,
  bancos, concorrência, Docker, Nginx, exemplos compiláveis e projeto TaskBoard.
- **CI do curso** - execução dos exemplos nas cinco linguagens e validação do
  Compose do projeto integrador.
- **Curso avançado no módulo 01** - formação aprofundada de 230–350 horas em
  arquitetura de dados, modelagem, SQL/PostgreSQL, concorrência, desempenho,
  NoSQL/MongoDB e APIs orientadas à consistência. Inclui caderno com 36
  práticas, guia de diagnóstico, cinco laboratórios progressivos, clientes
  testáveis em Python, Java, C, C# e JavaScript e a Inventory API com
  idempotência, ETag, outbox, gateway Nginx, 42 testes e smoke test completo.
- **Engenharia de software aprofundada no módulo 02** - 17 capítulos do
  raciocínio algorítmico à arquitetura profissional, exemplos comparados nas
  cinco linguagens, caderno com 32 práticas, guia de diagnóstico, cinco
  laboratórios progressivos e Dependency Planner com entrada limitada, teste
  de propriedades, runbook, ADRs e CI dedicada. Recon/OSINT pertence ao módulo
  29 e não integra a formação-base deste diretório.
- **Aplicações profissionais aprofundadas no módulo 03** - 17 capítulos de
  contrato de produto, CLI, GUI, web, acessibilidade, estado, dados locais,
  resiliência, i18n, diagnóstico, plugins, distribuição, desempenho e release;
  inclui cinco laboratórios progressivos, caderno com 32 práticas, guia de
  diagnóstico, exemplos nas cinco linguagens e Study Desk com schema rigoroso,
  rollback, 35 testes, ADRs e runbook. O aplicativo aplica uma rota explícita e
  gates semânticos; Active Directory permanece exclusivamente no módulo 31.
- **Automação profissional aprofundada no módulo 04** - 15 capítulos de
  decisão e plan/apply a jobs, resiliência, concorrência, segurança,
  observabilidade, CI/CD e operação; inclui 30 práticas, guia de diagnóstico,
  cinco laboratórios progressivos e exemplos equivalentes nas cinco linguagens.
  O FileFlow ganhou limites, manifesto sem caminhos absolutos, digest canônico,
  operation/run IDs, revalidação pré-efeito, audit seguro, 16 testes, ADRs e
  runbook. A aplicação de estudos agora aplica rota explícita e gates semânticos;
  ferramentas de segurança permanecem no módulo 28.
- **Engenharia de APIs aprofundada no módulo 05** - 26 capítulos reconstruídos
  com invariantes, falhas, exercícios e checklists; 45 práticas, guia de
  diagnóstico e cinco laboratórios progressivos. A Contract Lab agora possui
  cursor assinado e ligado ao filtro, cache condicional, Problem Details com
  códigos/request ID, estado irreversível, replay guard, OpenAPI comparado ao
  runtime e 32 testes. A aplicação de estudos recebeu rota e gates semânticos.
- **Purple Team no módulo 26** - especialização autocontida com 22 capítulos
  sobre firewalls, CDN/origem, DDoS, WAF/OWASP CRS, Cloudflare, BunkerWeb,
  detecção de bots, rate limiting, Turnstile, MFA/passkeys e resposta.
- **Laboratórios Purple Team** - sete exercícios pareados com hipótese Red,
  evidência Blue, tuning, rollback e reteste, sem tráfego para terceiros.
- **Ferramentas de borda testadas** - score de risco explicável, auditor de
  controles e token bucket determinístico, com 12 testes e CI offline.
- **Legado do módulo 26 preservado** - plano mais amplo de malware/exploits
  simulados continua separado da formação ativa.
- **Linux do zero ao kernel aprofundado no módulo 06** - os 31 capítulos agora
  possuem objetivos, exercícios e checklists; a rota ganhou 64 práticas, guia
  de diagnóstico, seis gates de laboratório, capstone de reconstrução e
  projeto de referência Host Observer com ferramenta Python para comparar
  baselines. Exemplos Bash/AWK/C, units e
  módulo didático continuam testados sem privilégios. Conteúdo detalhado de
  redes foi mantido nos módulos 14–18.
- **Linux avançado no módulo 07** - especialização autocontida com 35
  capítulos sobre fonte e ABI do kernel, scheduler, concorrência, RCU, MM/NUMA,
  VFS, filesystems, block layer, boot confiável, cgroup v2, tracing/eBPF local,
  depuração, KVM, tempo real, embarcados, LSM, integridade, empacotamento e
  contribuição. Todos os capítulos agora têm profundidade mínima, exercícios e
  checklists; foram adicionados 72 práticas, guia transversal, projeto de
  referência, nove gates com pré-requisitos semânticos e teste curricular em CI.
  Redes foram explicitamente reservadas para um módulo próprio; o antigo Web
  AppSec permanece preservado como acervo legado fora da rota principal.
- **Windows doméstico I no módulo 08** - os 18 capítulos foram reconstruídos
  com profundidade técnica, objetivos, exercícios e checklists, cobrindo do
  boot/instalação suportada à recuperação. A trilha ganhou 48 práticas, guia de
  diagnóstico, projeto de referência, seis gates com pré-requisitos semânticos
  e rota explícita na aplicação. O inventário agora preserva estados de consulta;
  backup e comparação de manifests possuem limites de caminho/reparse point e
  testes Pester. CI e teste curricular validam profundidade, escopo e progressão.
- **Windows doméstico II aprofundado no módulo 09** - os 20 capítulos foram
  reconstruídos com objetivos, modelos, exercícios e checklists. A trilha ganhou
  56 práticas, guia de tracing/debugging, projeto Diagnostic Workbench e seis
  gates com pré-requisitos semânticos. O parser PE agora valida tamanho, headers,
  section table e intervalos; a DLL C valida ABI e usa mitigações de build. A
  aplicação, Pester, teste curricular e CI verificam rota, profundidade, escopo
  local e mini dumps exclusivos de fixtures próprias.
- **Windows empresarial I no módulo 10** - 19 capítulos sobre Windows Server,
  Server Core, roles/features, identidade local, baselines, armazenamento,
  FSRM, auditoria, Defender, servicing, VSS, Hyper-V, containers/DSC locais e
  servidor standalone reconstruível.
- **Windows empresarial II no módulo 11** - 22 capítulos e sete laboratórios
  sobre WIM/WinPE/DISM, unattend, deployment, AD/GPO, gMSA/LAPS, PKI/JEA,
  App Control, Defender, VBS/BitLocker, Sysmon, compliance e continuidade;
  componentes distribuídos são modelados offline até a formação de redes.
- **Validação Windows** - validador estrutural/de escopo, Pester,
  PSScriptAnalyzer, build MSVC da DLL e workflow Windows dedicado. Os acervos
  Cloud, C2, Container e Python anteriores foram preservados como legado.
- **macOS I no módulo 12** - 20 capítulos e seis laboratórios sobre hardware,
  boot/Recovery, Finder, APFS, contas/permissões, apps, processos, `launchd`,
  plists, Terminal, logs, backup, FileVault, Gatekeeper, SIP, TCC e automação;
  inclui inventário sanitizado e backup verificável em Python.
- **macOS II no módulo 13** - 24 capítulos e sete laboratórios sobre Darwin/XNU,
  Mach/BSD/IOKit, arm64, memória, Mach-O/`dyld`, APFS/SSV, code signing,
  notarização, sandbox, TCC, Endpoint Security, observabilidade, LLDB,
  profiles, MDM/DDM, identidade e compliance.
- **Ferramentas e CI macOS** - parser Mach-O, auditor de `.mobileconfig`,
  comparador de baseline, dylib C segura, testes portáteis, validador de escopo
  e workflow nativo macOS com Clang/codesign. Java e Initial Access foram
  preservados como acervos legados nos diretórios originais.
- **Redes I–V nos módulos 14–18** - 91 capítulos e 26 laboratórios cobrindo
  LAN/PAN/WAN, OSI/TCP-IP, Ethernet, IPv4/IPv6, DNS, DHCP, HTTP, Wi-Fi,
  WPA2/WPA3, switching, VLANs, STP/LACP, roteamento, OSPF/BGP, VPN, DDI,
  observabilidade, zero trust, automação e infraestrutura empresarial.
- **Ferramentas e CI de redes** - calculadora IP, classificador HTTP, auditor
  residencial, validador de VLANs, simulador de rotas/ACL, auditor de
  arquitetura, validador estrutural e workflow offline dedicado.
- **Engenharia de protocolos** - especificação e implementação real do RNP/1,
  com framing binário, parser incremental limitado, máquina de estados, vetores,
  fuzzing bounded e demonstração por fluxo local.
- **Acervos 14–18 preservados** - Post-Exploitation, identidade híbrida, CI/CD
  supply chain, resumo macOS e mobile foram movidos para documentos `LEGADO-*`.
- **Criptografia I–IV nos módulos 19–22** - 78 capítulos e 22 laboratórios
  cobrindo matemática, aleatoriedade, hash/MAC/KDF, AES-GCM,
  ChaCha20-Poly1305, RSA/ECC, X25519, Ed25519, PKI/X.509, TLS 1.3, SSH,
  proteção de dados, gestão de chaves, HSM/KMS, agilidade e pós-quântica.
- **Ferramentas criptográficas testadas** - aritmética modular, SHA-256/HMAC,
  scrypt, envelope AEAD, acordo X25519/HKDF, assinaturas Ed25519, auditor de
  certificados/política TLS, mini-PKI descartável, criptoinventário e protocolo
  de registros autenticados com proteção contra replay.
- **CI de criptografia** - dependência fixada, validador estrutural/de escopo,
  26 testes unitários e execução dos quatro cursos completamente offline.
- **Acervos 19–22 preservados** - wireless, operações ofensivas, pivoting e
  code review permanecem em documentos `LEGADO-*` e caminhos compatíveis.
- **Privacidade I–III nos módulos 23–25** - 59 capítulos e 17 laboratórios
  cobrindo modelos de ameaça, metadados, VPN/proxy/Tor, WireGuard em VPS própria,
  DNS/IPv6, telemetria, NAT/CGNAT, correlação e atribuição defensiva.
- **Ferramentas de privacidade testadas** - analisador de modelo de ameaça,
  planejador WireGuard sem segredos, auditor de política, correlator que não usa
  IP isolado e gerador de manifesto SHA-256.
- **CI de privacidade** - validador de estrutura, links, escopo offline, segredos
  e instruções de evasão, além de execução completa dos três cursos.
- **Acervos 23–25 preservados** - CTI/emulação, movimentação lateral e catálogo
  de cursos continuam disponíveis como documentos legados e ferramentas
  compatíveis.

- **Vídeos por módulo** - curadoria de cinco vídeos em português incorporada a
  cada README dos módulos 00–26.
- **Validador de vídeos** - teste offline das 27 seções distribuídas e do mínimo
  de cinco vídeos distintos por módulo.
- **00-Fundamentos** - programação, redes, sistemas, identidade, RoE,
  laboratório seguro e autoavaliação.
- **Testes Python** - suite pytest offline para biblioteca comum, parsers e ferramentas.
- **Testes Bash, PowerShell e Java** - validações offline das bibliotecas e do gerador.
- **Validador ATT&CK** - invariantes do layer JSON verificadas localmente e no CI.
- **Labs reproduzíveis** - respostas/rubrica para três labs Web e datasets sintéticos para DFIR e Kubernetes.
- **Detecção verificável** - padrão comum e exemplos para AD, Web/API, cloud e containers.
- **Cloud offline** - fixtures IAM AWS/Azure/GCP, analisador normalizado e respostas orientativas sem contas ou custos.
- **Compose seguro** - healthchecks, limites de CPU/memória, profiles e validador de bindings localhost.
- **Acervos avançados** - identidade híbrida, APIs modernas, CI/CD supply chain e microemulação Purple Team offline.
- **Trilhas defensivas** - macOS com exercícios seguros; os resumos wireless e mobile foram preservados como legado.
- **Métricas** - inventário reproduzível de módulos, contratos, testes e fixtures.
- **Acervo de operações ofensivas** - scope guard, correlação de recon, matriz
  BOLA/BFLA, pivoting e code review preservados após a migração dos módulos 20–22.
- **Legado do módulo 23** - threat-intel/adversary emulation.
- **Legado do módulo 24** - movimentação lateral com grafo sintético, precondições, telemetria e cleanup.
- **Movimentação lateral Linux** - SSH/certificados, bastion, sudo, NFS, automação e sockets com path offline.
- **Contrato editorial** - template reutilizável em `docs/MODULE-TEMPLATE.md`.
- **Lab doctor** - diagnóstico do Compose, containers e endpoints HTTP locais.
- **36-Escalacao-Privilegios/acervo/windows/windows_privesc_teoria.md** - Windows Privilege Escalation (enum, UAC, services, tokens, checklist, defesa).
- **06-Cheatsheets** - metodologia + cheatsheet Windows e PATH hijacking Linux (adaptado HexSec/MIT, PT).
- **07-Web-AppSec** - deep-dives SQLi/SSRF + labs guiados DVWA, Juice Shop e VAmPI (`labs/`).
- **07-Web-AppSec** - enum web avancado (dirs/vhosts/params/AXFR) e path traversal/LFI (adaptado HexSec/MIT, PT).
- **13-Initial-Access** - phishing teorico (T1566) e servicos externos (VPN/RDP/OWA/T1190).
- **Acervo legado do 14** - collection/exfil e persistencia overview eticos.
- **report/** - `generate-pdf.sh` (pandoc/eisvogel) para PDF a partir do template.
- READMEs de modulo para 02-OSINT, 03-AD-Notes, 05-DFIR, 06-Cheatsheets.
- Exercicios praticos e checklists em Cloud (08) e Container (10).
- MITRE ATT&CK layer expandido para modulos 07-14 (v2.1 coverage).

### Modificado

- Lab separa rede interna de alvos, acesso local via gateway e egress exclusivo
  do atacante; serviços não usam nomes globais nem reinicialização automática.
- Testes Java usam compilação estrita no JDK 17+ e recorrem ao source-file mode
  quando apenas o runtime local atende ao requisito.
- Credenciais AD/JWT deixaram de aparecer em argumentos, logs e relatórios por
  padrão; exports são atômicos e restritos ao usuário.
- CI ganhou permissões mínimas, timeouts, cancelamento concorrente e cobertura.
- Layer migrado de ATT&CK 14 para 19.2 e validado offline contra um snapshot
  reduzido do dataset oficial, incluindo Stealth e Defense Impairment.
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

### Removido

- Serviços NodeGoat e Vulnerable WordPress do Compose: as imagens declaradas
  haviam desaparecido do registry. O retorno exige origem e build verificáveis.

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
- `31-Active-Directory-Identidade/active-directory-identidade-hibrida/modern-ad-attacks-2026.md` - ADCS (ESC1, ESC8), RBCD, Shadow Credentials, SCCM abuse, PKINIT, KrbRelayUp.
- `36-Escalacao-Privilegios/acervo/linux/linux_privesc_modern.md` - CVEs kernel 2022-2026 (DirtyPipe, OverlayFS, nf_tables UAF), capabilities modernas, eBPF post-exploitation.
- `29-Reconhecimento-OSINT/dns_enum.sh` - alternativa Linux do dns_enum.ps1 com dig + crt.sh.
- `28-Engenharia-Ferramentas-Seguranca/acervo/automacao/ad_recon.sh` - wrapper Linux para nmap + NetExec + Impacket (GetNPUsers, GetUserSPNs).

#### Modificado

- **`29-Reconhecimento-OSINT/dns_enum.ps1`** - reescrito v2.0: cross-platform (Resolve-DnsName em Windows, dig fallback em Linux), Certificate Transparency via crt.sh, exportacao JSON estruturada, retries com backoff, dry-run real, validacao de dominio rigorosa.
- **`28-Engenharia-Ferramentas-Seguranca/acervo/automacao/organize_logs.ps1`** - INDEX.md gerado com SHA-256 de cada arquivo, suporte -CopyMode, -DryRun, classificacao por regex + extensao.
- **`28-Engenharia-Ferramentas-Seguranca/acervo/automacao/windows_setup_clean.ps1`** - integracao Chocolatey, dry-run, ExtraPackages, tweaks Explorer, validacao de admin.
- **`28-Engenharia-Ferramentas-Seguranca/acervo/automacao/linux_postinstall.sh`** - deteccao de distro (Kali/Parrot/Ubuntu/Debian), pacotes essenciais expandidos, SecLists clone, aliases idempotentes, dry-run.
- **`validate_scripts.ps1`** - usa PSScriptAnalyzer real (instalado on-demand), severity configuravel, custom rules pluggable.
- **`README.md`** - reescrito para refletir v2.0, com tabela completa de modulos, ATT&CK coverage expandida, quick start poliglota.
- **`31-Active-Directory-Identidade/active-directory-identidade-hibrida/kerberoasting_teoria.md`** - typo "Cracke\n\nar" corrigido; adicionada secao "Atualizacao 2024-2026" com etypes AES vs RC4 e tools modernas.

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
  - `29-Reconhecimento-OSINT/LEGADO-RECON.md` - Guia histórico de reconhecimento
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
  - `29-Reconhecimento-OSINT/` - Reconhecimento e DNS enumeration
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
- [x] Mobile / Wireless tracks
- [x] Purple-team exercises pareados ataque/deteccao
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
**Última Atualização:** 29 de setembro de 2026

</div>
