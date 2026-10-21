# 🗺️ ROADMAP - Red Team Essentials

> **Trilha de Aprendizado Estruturada e Progressiva**

Este documento apresenta uma roadmap completa para estudar Red Team de forma gradual, organizada e eficiente, com integração ao framework **MITRE ATT&CK**.

---

## Jornada canônica atual

O currículo possui **41 módulos em sete áreas**. A base obrigatória vai de
**00 a 26**; somente depois dela começa a especialização em segurança, com
**14 módulos de 27 a 40**:

1. **27:** governança, laboratório e evidência;
2. **28:** automação e ferramentas de segurança;
3. **29:** reconhecimento, OSINT e superfície de ataque;
4. **30:** Web, APIs e revisão segura de código;
5. **31:** Active Directory e identidade híbrida;
6. **32:** segurança em AWS, Azure e GCP;
7. **33:** containers, Kubernetes, CI/CD e supply chain;
8. **34:** segurança de macOS, mobile e wireless;
9. **35:** acesso inicial, C2, evasão e OPSEC;
10. **36:** elevação de privilégios em Linux e Windows;
11. **37:** pós-exploração, pivoting e movimentação lateral;
12. **38:** DFIR e resposta a incidentes;
13. **39:** threat intelligence e adversary emulation;
14. **40:** capstone Purple Team de operações integradas.

Os acervos avançados foram realocados fisicamente para essa sequência; os
módulos 00–26 mantêm apenas seus cursos-base. Os tiers abaixo permanecem como
referência temática e de proficiência; a ordem curricular oficial é 00–40.

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

**Pré-requisitos:** Concluir o [Módulo 00](00-Fundamentos/README.md) ou demonstrar
os mesmos conhecimentos de redes, sistemas, identidade, RoE e laboratório seguro.
**Tempo estimado:** 4-6 semanas  
**Objetivo:** Compreender os fundamentos de reconhecimento e coleta de informações

### Módulo 29: Reconhecimento Passivo e OSINT
- **Duração:** 1-2 semanas
- **Objetivos de Aprendizado:**
  - Entender a diferença entre reconhecimento passivo e ativo
  - Aprender técnicas de OSINT básicas
  - Dominar ferramentas de DNS enumeration
  - Compreender footprinting de aplicações web

- **Conteúdo:**
  - `29-Reconhecimento-OSINT/passive_recon_cheatsheet.md` - Teoria e comandos
  - `29-Reconhecimento-OSINT/dns_enum.ps1` - Script automatizado de DNS
  - `29-Reconhecimento-OSINT/web_recon_notes.md` - Reconhecimento web

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

### Módulo 02: Engenharia de software e algoritmos (`02-OSINT/engenharia-software`)

- **Duração:** 260–380 horas.
- **Pré-requisitos:** programação, dados e APIs dos módulos 00 e 01.
- **Objetivos de aprendizagem:**
  - transformar problemas ambíguos em contratos e invariantes verificáveis;
  - analisar tempo, memória e hipóteses de estruturas e algoritmos;
  - aplicar listas, hashes, árvores, heaps, tries e grafos conscientemente;
  - dominar busca, ordenação, recursão, backtracking, DP e estratégias gulosas;
  - projetar módulos, portas, adapters e arquiteturas orientadas por requisitos;
  - evoluir legado com testes, ADRs, revisão, documentação e rollback.

- **Prática e evidência:**
  - exemplos equivalentes em Python, Java, C17, C# e JavaScript;
  - cinco laboratórios progressivos com gates objetivos;
  - caderno com 32 experimentos e guia de diagnóstico;
  - Dependency Planner com CLI, JSON rigoroso, ordem/lotes, caminho crítico,
    limites de recursos, testes de propriedades, runbook e ADRs.

Reconhecimento e OSINT não fazem parte deste módulo-base. Esses temas pertencem
exclusivamente ao [módulo 29](29-Reconhecimento-OSINT/README.md), depois da base
00–26.

---

### Módulo 03: Desenvolvimento de aplicações profissionais (`03-AD-Notes/desenvolvimento-aplicacoes`)

- **Duração:** 360–520 horas.
- **Pré-requisitos:** módulos 00, 01 e 02.
- **Objetivos de aprendizagem:**
  - converter código e requisitos em contratos de produto verificáveis;
  - projetar CLI, GUI desktop e web sobre o mesmo núcleo de domínio;
  - evoluir configuração, estado e documentos locais sem perda silenciosa;
  - construir acessibilidade, responsividade, offline e i18n como requisitos;
  - diagnosticar, estender, empacotar, medir, publicar e recuperar aplicações.

- **Prática e evidência:**
  - exemplos equivalentes em Python, Java, C17, C# e JavaScript;
  - cinco laboratórios cumulativos com gates no aplicativo de estudos;
  - caderno com 32 práticas e guia de diagnóstico por fronteiras;
  - Study Desk local-first com schema versionado, rollback, 35 testes, ADRs e
    runbook;
  - capstone instalável com teclado, migração, diagnóstico, orçamento e rollback.

Active Directory não faz parte deste módulo-base. O acervo histórico foi
transferido para o [módulo 31](31-Active-Directory-Identidade/README.md), após a
conclusão da base 00–26.

---

### Módulo 04: Automação profissional

- **Duração:** 220–320 horas
- **Pré-requisitos:** módulos 00–03
- **Formação:** 15 capítulos, 30 práticas e cinco laboratórios progressivos
- **Competências:** decisão de automação, plan/apply, idempotência, arquivos,
  pipelines, HTTP/webhooks, jobs, checkpoints, retry, backpressure, concorrência,
  documentos, segurança, observabilidade, testes, CI/CD e distribuição
- **Projeto:** FileFlow com limites, manifesto/digest, audit JSONL, 16 testes,
  arquitetura, ADRs e runbook
- **Conclusão:** artifact operável e game day reproduzível; 75% na rubrica sem
  zerar dry-run/idempotência, segurança de efeitos, testes de falha ou operação

Ferramentas especializadas de segurança foram transferidas para o módulo 28 e não
integram esta formação-base.

---

### Módulo 1.4: Engenharia de APIs (05-DFIR/engenharia-apis)

- **Duração:** 300–440 horas
- **Formação:** 26 capítulos, 45 práticas e cinco laboratórios progressivos
- **Objetivos de Aprendizado:**
  - Projetar contratos HTTP e modelos de erro
  - Implementar APIs seguras, observáveis e evolutivas
  - Comparar REST, eventos, GraphQL e gRPC

- **Conteúdo:**
  - semântica HTTP, recursos, schemas, paginação e compatibilidade
  - autenticação, autorização, OWASP API Security e threat modeling
  - OpenAPI, arquitetura, consistência, resiliência e testes
  - webhooks, AsyncAPI, GraphQL, gRPC, streaming, SDKs e governança

- **Projeto integrador:**
  - Contract Lab API com idempotência, ETag, cursor assinado e Problem Details
  - clientes nas cinco linguagens e contrato OpenAPI
  - 32 testes de unidade, componente, contrato, abuso e compatibilidade

- **Tarefas Práticas:**
  1. ✅ Projetar e revisar um contrato antes do código
  2. ✅ Testar autorização, limites, concorrência e compatibilidade
  3. ✅ Definir SLI, SLO, alertas e runbook
  4. ✅ Entregar cliente, guia de migração e política de retirada

---

## 🔥 TIER 2: Intermediário

**Pré-requisitos:** Completar TIER 1  
**Tempo estimado:** 8-12 semanas  
**Objetivo:** Dominar técnicas de exploração e pós-exploração

### Módulo 31: Active Directory e identidade híbrida
- **Duração:** 3-4 semanas
- **Objetivos de Aprendizado:**
  - Entender arquitetura do Active Directory
  - Dominar técnicas de enumeração
  - Compreender ataques clássicos (Kerberoasting, AS-REP Roasting)
  - Usar BloodHound para mapeamento

- **Conteúdo:**
  - `31-Active-Directory-Identidade/active-directory-identidade-hibrida/`
  - comandos de enumeração, teoria de Kerberos e análise de caminhos;
  - identidade híbrida e controles defensivos no estágio avançado.

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

### Módulo 2.2: Linux do zero ao kernel (06-Cheatsheets)

- **Duração:** 240–360 horas.
- **Objetivos de aprendizagem:**
  - escolher, instalar e recuperar uma distribuição;
  - dominar arquivos, texto, permissões, contas, pacotes e processos;
  - compreender memória virtual, armazenamento, boot e systemd;
  - administrar SSH local, serviços, logs, backups e hardening;
  - explicar namespaces, cgroups, syscalls, kernel, módulos e drivers;
  - diagnosticar desempenho por evidência.

- **Conteúdo:**
  - `linux-do-zero-ao-avancado/` — 31 capítulos autocontidos;
  - exemplos seguros em Bash, AWK, Python e C;
  - unidades systemd e módulo de kernel didáticos;
  - 64 práticas, guia de diagnóstico e seis laboratórios progressivos;
  - projeto final reproduzível com restore e defesa das decisões.

- **Tarefas práticas:**
  1. [ ] Instalar e inventariar as VMs do curso.
  2. [ ] Concluir os cinco marcos intermediários na ordem do catálogo.
  3. [ ] Administrar serviço local com systemd, SSH e menor privilégio.
  4. [ ] Praticar armazenamento, boot e kernel somente em clone descartável.
  5. [ ] Restaurar o capstone em VM vazia e medir RPO/RTO.
  6. [ ] Encaminhar redes aos módulos 14–18 com evidência do estado local.

O acervo anterior de privilege escalation e movimento lateral permanece fora da
rota. Uma eventual formação específica deverá ter área própria e não integra o
escopo de firewalls/WAF do módulo 26.

---

### Módulo 2.3: Linux avançado e engenharia de kernel (07-Web-AppSec)

- **Duração:** 420–620 horas.
- **Pré-requisito:** concluir os módulos 00–06.
- **Objetivos de aprendizagem:**
  - ler fonte, ABI, ELF, syscalls e internals de processos;
  - explicar scheduler/EEVDF, SMP, atomics, RCU, MM e NUMA;
  - investigar VFS, filesystems, block layer, I/O e drivers;
  - operar boot verificável, systemd, cgroup v2 e KVM offline;
  - diagnosticar com perf, ftrace, eBPF local, core e kdump;
  - aplicar LSM, seccomp, verity e assinatura;
  - produzir pacotes, imagens e patches reproduzíveis.

- **Conteúdo:**
  - `linux-avancado/` — 35 capítulos com exercícios e checklists;
  - 72 práticas, guia de diagnóstico e projeto de referência;
  - exemplos reais em C/Bash, systemd, eBPF e módulo didático;
  - nove gates de laboratório por risco e appliance offline como projeto final;
  - rota semântica na aplicação, validação curricular e workflow dedicado.

- **Limite:** redes não pertencem a este módulo. Roteamento, firewall,
  namespaces de rede, tráfego e eBPF de rede terão formação própria.

- **Tarefas práticas:**
  1. [ ] Mapear uma syscall da ABI ao código do kernel.
  2. [ ] Reproduzir um experimento de scheduler/memória com percentis.
  3. [ ] Diagnosticar um gargalo usando perf e tracing por hipótese.
  4. [ ] Construir VM KVM/QEMU sem NIC e com imagem verificável.
  5. [ ] Entregar pacote reproduzível e patch didático revisável.
  6. [ ] Defender o appliance final com rollback e recuperação.

O conteúdo Web AppSec historicamente armazenado em `07-Web-AppSec/` continua
acessível para preservar links, mas é acervo legado e não integra esta rota.

---

### Módulo 2.4: Windows doméstico I (08-Cloud-RedTeam)

- **Duração:** 240–360 horas.
- **Conteúdo:** 18 capítulos aprofundados em
  `windows-domestico-fundamentos/`, do ciclo de suporte e boot UEFI/TPM à
  instalação suportada, NTFS/BitLocker, SID/ACL/UAC, processos/serviços,
  pacotes, servicing, Registro, Event Log, backup, Defender, PowerShell,
  diagnóstico, WinRE e projeto final.
- **Prática:** 48 atividades, guia transversal, três scripts PowerShell reais,
  seis gates semânticos, restore por manifesto, falha cega e computador local
  recuperável testado por terceiro.
- **Qualidade:** capítulos com objetivos/exercícios/checklists, teste curricular,
  Pester, análise estática e rota intercalada na aplicação.
- **Limite:** sem redes, compartilhamentos, firewall, identidade empresarial,
  técnicas ofensivas ou internals reservados ao módulo 09.

### Módulo 2.5: Windows doméstico II (09-C2-Evasion)

- **Duração:** 300–440 horas.
- **Conteúdo:** 20 capítulos em `windows-domestico-avancado/` sobre Windows NT,
  processos/threads/tokens, memória, PE/COFF, DLL/loader, NTFS/Registro internals,
  drivers, PowerShell, ETW/WER, Sysinternals, performance, VBS e WinDbg.
- **Prática:** 56 atividades, guia transversal de tracing/debugging, seis gates
  semânticos, DLL nativa C com ABI validada, parser PE com limites, Pester,
  WPR/WPA, mini dump próprio e Diagnostic Workbench reproduzido por terceiro.
- **Qualidade:** todos os capítulos possuem objetivos, exercícios e checklists;
  rota explícita, pré-requisitos dos labs e profundidade são testados em CI.
- **Limite:** sem injeção, bypass, malware, evasão ou redes.

### Módulo 2.6: Windows empresarial I (10-Container-Sec)

- **Duração:** 180–280 horas.
- **Conteúdo:** 19 capítulos em `windows-empresarial-fundamentos/` sobre
  Windows Server, Core, roles/features, identidades locais, baselines,
  NTFS/ReFS/Storage Spaces/FSRM, Defender, servicing, VSS, backup, Hyper-V,
  containers locais, DSC e capacidade.
- **Projeto:** Server Core standalone, sem NIC, reconstruído por estado desejado
  e recuperado por backup testado.

### Módulo 2.7: Windows empresarial II (11-Python-Tools)

- **Duração:** 240–360 horas.
- **Conteúdo:** 22 capítulos em `windows-empresarial-avancado/` sobre imagens
  WIM/WinPE/DISM, unattend, deployment rings, AD/GPO, gMSA/LAPS, PKI, JEA,
  App Control, Defender, VBS/BitLocker, Sysmon, compliance e continuidade.
- **Prática:** pipeline read-only, comparador de baseline, validador de modelo
  de identidade, sete labs e arquitetura empresarial final.
- **Continuação:** componentes distribuídos são projetados offline e os
  fundamentos de DNS, roteamento, VPN e infraestrutura estão nos módulos 14–18.

Os acervos Cloud, C2, Container e Python anteriores continuam preservados nos
diretórios 08–11, mas não fazem parte da rota Windows principal.

---

### Módulo 2.8: macOS I (12-Java-Tools)

- **Duração:** 140–220 horas.
- **Conteúdo:** 20 capítulos em `macos-fundamentos/` sobre Apple Silicon/Intel,
  boot/Recovery, Finder, APFS, contas, permissões, bundles, processos, `launchd`,
  plists, Terminal/zsh, logs, backup e proteções nativas.
- **Prática:** seis labs, inventário sem identificadores, backup SHA-256,
  restauração e projeto de Mac local recuperável.
- **Limite:** nenhuma configuração de rede ou redução de SIP/Gatekeeper/TCC.

### Módulo 2.9: macOS II (13-Initial-Access)

- **Duração:** 260–380 horas.
- **Conteúdo:** 24 capítulos em `macos-avancado/` sobre Darwin/XNU,
  Mach/BSD/IOKit, memória, Mach-O/`dyld`, APFS/SSV, assinatura/notarização,
  sandbox/TCC, Endpoint Security, observabilidade, LLDB, perfis, MDM/DDM,
  Platform SSO e compliance.
- **Prática:** sete labs, parser Mach-O, dylib segura em C, auditor de perfis,
  comparador de baseline e projeto de frota offline.
- **Continuação:** serviços distribuídos são aprofundados nos módulos 14–18.

O acervo Java anterior no 12 e o material Initial Access anterior no 13 foram
preservados como legados, fora da rota macOS.

---

### Módulo 2.10: Redes I (14-Post-Exploitation)

- **Duração:** 120–180 horas.
- **Conteúdo:** 18 capítulos sobre tipos de rede, topologias, OSI/TCP-IP,
  Ethernet, MAC/ARP/NDP, IPv4/IPv6, CIDR, DNS, DHCP, ICMP, TCP/UDP/QUIC,
  HTTP/TLS, endereços públicos/privados e NAT.
- **Prática:** cinco labs, calculadora IP, classificador HTTP e projeto ponta a
  ponta inteiramente offline.

### Módulo 2.11: Redes II (15-Hybrid-Identity)

- **Duração:** 120–180 horas.
- **Conteúdo:** 16 capítulos de redes domésticas/SOHO, modem/ONT, roteador,
  switches/APs, Wi-Fi, WPA2/WPA3, convidados/IoT, firewall, NAT, IPv6,
  cobertura, performance, privacidade e recuperação.
- **Prática:** auditor de baseline, cinco labs e projeto residencial/SOHO.

### Módulo 2.12: Redes III (16-CICD-Supply-Chain)

- **Duração:** 150–220 horas.
- **Conteúdo:** 17 capítulos sobre switching, tabela MAC, VLANs, 802.1Q,
  inter-VLAN, STP/RSTP/MSTP, LACP, LLDP/PoE, 802.1X/NAC, QoS, multicast,
  virtualização e campus.
- **Prática:** validador de plano de VLAN, cinco labs e projeto de campus.

### Módulo 2.13: Redes IV (17-macOS-Security)

- **Duração:** 180–280 horas.
- **Conteúdo:** 19 capítulos sobre RIB/FIB, rotas, OSPF, BGP/RPKI, ECMP,
  FHRP, VRF, ACL/firewall, WAN, IPsec, WireGuard, acesso remoto e operações.
- **Prática:** simulador de longest-prefix/ACL, cinco labs e projeto WAN/VPN.

### Módulo 2.14: Redes V (18-Mobile-Security)

- **Duração:** 240–360 horas.
- **Conteúdo:** 21 capítulos de arquitetura empresarial, DDI, NTP, PKI, AAA,
  proxies/load balancers, serviços, observabilidade, SLO/capacidade, HA/DR,
  zero trust, automação e engenharia de protocolos.
- **Prática:** seis labs, auditor de arquitetura e especificação/implementação
  testada do protocolo binário RNP/1.

Os conteúdos anteriores de Post-Exploitation, identidade híbrida, CI/CD,
segurança macOS e mobile foram preservados nos respectivos arquivos `LEGADO-*`.

### Módulo 2.15: Criptografia I (19-Wireless-Security)

- **Duração:** 120–180 horas.
- **Conteúdo:** 18 capítulos de representação, matemática modular, entropia,
  CSPRNG, cifras clássicas, hashes, colisões, HMAC, HKDF, KDFs de senha,
  compromissos, Merkle e canais laterais.
- **Prática:** cinco labs e implementações testadas de teoria dos números,
  SHA-256/HMAC e registros scrypt.

### Módulo 2.16: Criptografia II (20-Offensive-Labs)

- **Duração:** 160–240 horas.
- **Conteúdo:** 19 capítulos de AES, modos, AEAD, AES-GCM,
  ChaCha20-Poly1305, RSA-OAEP/PSS, Diffie–Hellman, ECC, X25519, Ed25519,
  envelopes e agilidade.
- **Prática:** cinco labs, envelope autenticado, acordo de chaves e assinaturas
  reais com testes de adulteração.

### Módulo 2.17: Criptografia III (21-Network-Pivoting)

- **Duração:** 180–280 horas.
- **Conteúdo:** 20 capítulos de PKI/X.509, CAs, validação, revogação, ACME,
  TLS 1.3, mTLS, HTTPS, SSH, OpenPGP/S/MIME, senhas, dados em repouso, JOSE e
  gestão de segredos.
- **Prática:** seis labs, mini-PKI descartável e auditores X.509/TLS offline.

### Módulo 2.18: Criptografia IV (22-Secure-Code-Review)

- **Duração:** 220–340 horas.
- **Conteúdo:** 21 capítulos de composição, protocolos, replay/downgrade,
  constant-time, memória, parsing, testes/fuzzing, métodos formais, HSM/KMS,
  criptoinventário, incidentes, agilidade e padrões pós-quânticos NIST.
- **Prática:** seis labs, inventário priorizado e protocolo AES-GCM ordenado
  com proteção contra replay e testes negativos.

Os materiais anteriores de wireless, operações ofensivas, pivoting e code
review mantêm seus caminhos e integram curricularmente os módulos 34, 40, 37
e 30, respectivamente.

### Módulo 2.19: Privacidade I (23-Threat-Intel-Emulation)

- **Duração:** 140–220 horas.
- **Conteúdo:** 19 capítulos sobre modelos de ameaça, metadados, roteamento,
  NAT/CGNAT, DNS, TLS, VPN, proxies, Tor, navegador, fingerprinting,
  identidade, dispositivos móveis, vazamentos e correlação de tráfego.
- **Prática:** cinco labs e analisador offline de risco residual, sem coleta de
  terceiros nem promessa de anonimato absoluto.

### Módulo 2.20: Privacidade II (24-Lateral-Movement)

- **Duração:** 160–240 horas.
- **Conteúdo:** 20 capítulos para planejar, implantar e operar WireGuard em
  VPS própria: chaves, rotas, nftables, DNS, IPv6, kill switch, MTU, logs,
  rotação, revogação e recuperação.
- **Prática:** seis labs, gerador de templates sem segredos e auditor de
  política. O material de movimentação lateral integra o módulo 37.

### Módulo 2.21: Privacidade III (25-Cursos)

- **Duração:** 180–280 horas.
- **Conteúdo:** 20 capítulos de telemetria, relógio, endpoint, identidade,
  rede, NAT/CGNAT, VPN/Tor, aplicação, cloud, correlação, integridade,
  evidência, confiança, privacidade e resposta.
- **Prática:** seis labs, correlator que nunca atribui por IP isolado e
  manifesto SHA-256. O catálogo anterior integra o módulo 27.

### Módulo 2.22: Purple Team de borda (26-Ofensivo-Defensivo)

- **Duração:** 220–340 horas.
- **Conteúdo:** 22 capítulos sobre firewalls L3/L4, host e cloud,
  segmentação/egress, CDN/origem, DDoS, WAF, parsing HTTP, OWASP CRS,
  Cloudflare, BunkerWeb, ameaças automatizadas, rate limiting,
  CAPTCHA/Turnstile, MFA, WebAuthn/passkeys, APIs e resposta.
- **Prática:** sete labs pareados Red/Blue, score de risco explicável, auditor
  de controles, simulador token bucket, 12 testes e CI totalmente offline.
- **Método:** hipótese autorizada, baseline, teste local, evidência, tuning,
  rollback e reteste. O plano original de ofensiva/defesa integra os módulos
  27 e 40.

### Referência temática: Initial Access (módulo canônico 35)
- **Duração:** 1-2 semanas
- **Objetivos de Aprendizado:**
  - Compreender vetores T1566 / T1190 / T1133 sem weaponization
  - Avaliar superfícies externas (VPN/RDP/OWA) com ética
  - Ligar web public-facing ao acervo Web AppSec legado e ao módulo 22

- **Conteúdo:**
  - `phishing-teoria.md`
  - `external-services.md`

- **MITRE ATT&CK Mapping:**
  - TA0001 - Initial Access (T1566, T1190, T1133, T1078)

- **Estado:** preservado em `LEGADO-INITIAL-ACCESS.md`, `phishing-teoria.md` e
  `external-services.md`; não integra a rota principal e não contém weaponization.

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
  - Stealth / Defense Impairment (ATT&CK 19.2)
    - T1027 - Obfuscated Files or Information
    - T1055 - Process Injection
    - T1140 - Deobfuscate/Decode Files or Information
    - T1685 - Disable or Modify Tools

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

Trilhas especializadas implementadas inicialmente:

- [14–18 — Redes](14-Post-Exploitation/README.md) — fundamentos, Wi-Fi,
  switching/VLANs, roteamento/VPN e infraestrutura/protocolos empresariais.
- [19–22 — Criptografia](19-Wireless-Security/README.md) — fundamentos,
  primitivas modernas, PKI/TLS, engenharia e pós-quântica.
- [APIs modernas](05-DFIR/engenharia-apis/README.md) — OAuth/OIDC, GraphQL e gRPC.
- [Microemulação Purple Team](docs/PURPLE-TEAM-MICRO-EMULATION.md) — cenário offline reproduzível.
- [23–25 — Privacidade](23-Threat-Intel-Emulation/README.md) — fundamentos,
  VPN própria e atribuição defensiva.
- **Duração:** Variável
- **Especializações adotadas sem mover os arquivos:**
  - Cloud Red Teaming → módulo 32, a partir de `08-Cloud-RedTeam/`;
  - Web Application Security → módulo 30, a partir de `07-Web-AppSec/`;
  - Container Security → módulo 33, a partir de `10-Container-Sec/`.
  `contentPaths` preserva esses diretórios, links e histórico enquanto os
  apresenta na sétima área curricular.
- **Em aberto (sem modulo ainda):**
  - IoT / OT Security

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
[ ] Módulo 29: Reconhecimento Passivo e OSINT
[ ] Módulo 1.2: OSINT Avançado
[ ] Módulo 1.3: Automação
[ ] Módulo 1.4: Introdução DFIR

TIER 2 - Intermediário
[ ] Módulo 2.1: Active Directory
[ ] Módulo 2.2: Linux do zero ao kernel
[ ] Módulo 2.3: Linux avançado e engenharia de kernel
[ ] Módulo 2.4: Windows doméstico I (08)
[ ] Módulo 2.5: Windows doméstico II (09)
[ ] Módulo 2.6: Windows empresarial I (10)
[ ] Módulo 2.7: Windows empresarial II (11)
[ ] Módulo 2.8: macOS I (12)
[ ] Módulo 2.9: macOS II (13)
[ ] Módulo 2.10: Redes I — fundamentos (14)
[ ] Módulo 2.11: Redes II — domésticas e Wi-Fi (15)
[ ] Módulo 2.12: Redes III — switching e VLANs (16)
[ ] Módulo 2.13: Redes IV — roteamento e VPN (17)
[ ] Módulo 2.14: Redes V — empresa e protocolos (18)
[ ] Módulo 2.15: Criptografia I — fundamentos (19)
[ ] Módulo 2.16: Criptografia II — primitivas modernas (20)
[ ] Módulo 2.17: Criptografia III — PKI e TLS (21)
[ ] Módulo 2.18: Criptografia IV — engenharia e pós-quântica (22)
[ ] Módulo 2.19: Privacidade I — fundamentos e anonimato (23)
[ ] Módulo 2.20: Privacidade II — VPN própria e operação (24)
[ ] Módulo 2.21: Privacidade III — atribuição defensiva (25)
[ ] Módulo 2.22: Purple Team — firewalls, WAF, bots e identidade (26)

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
- [x] Windows Privesc; acervos Initial Access e Post-Exploitation preservados
- [x] Labs guiados Web (DVWA / Juice / VAmPI)
- [x] Linux avançado no módulo 07, sem redes e com CI dedicada
- [x] Windows doméstico nos módulos 08–09, do uso básico a NT internals/DLL
- [x] Windows empresarial nos módulos 10–11, de Server Core a identidade/compliance
- [x] macOS nos módulos 12–13, do primeiro uso a XNU/Mach-O e gestão empresarial
- [x] redes nos módulos 14–18, dos fundamentos à infraestrutura empresarial
  e engenharia de protocolos, com validação offline
- [x] criptografia nos módulos 19–22, dos fundamentos à engenharia
  pós-quântica, com 78 capítulos, 22 labs e validação offline
- [x] privacidade nos módulos 23–25, de modelos de ameaça e VPN própria à
  correlação defensiva, com 59 capítulos, 17 labs e validação offline
- [x] Purple Team no módulo 26, com 22 capítulos, sete labs pareados,
  ferramentas offline, testes e CI para borda de aplicações
- [x] Sync NetExec + BloodHound CE + MITRE expandido

### Em aberto
- [ ] Labs IaC (Terraform/Ansible) quando houver codigo no repo
- [ ] Aprofundar mobile e wireless no módulo 34; seus fundamentos continuam nos
  módulos 15–16
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

**Próximo passo:** Começar pelo **módulo 00** e seguir a ordem canônica até o
**módulo 40**.

</div>
