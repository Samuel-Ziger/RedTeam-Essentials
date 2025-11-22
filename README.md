# 🎯 RedTeam Essentials

> Um repositório educacional completo sobre Red Team, focado em aprendizado ético, teoria aprofundada e automação segura com mapeamento MITRE ATT&CK.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Educational](https://img.shields.io/badge/Purpose-Educational-green.svg)]()
[![Ethical](https://img.shields.io/badge/Content-Ethical-brightgreen.svg)]()
[![Version](https://img.shields.io/badge/Version-1.0.0-blue.svg)]()
[![PowerShell](https://img.shields.io/badge/PowerShell-5.1%2B-blue.svg)]()
[![Bash](https://img.shields.io/badge/Bash-4.0%2B-green.svg)]()
[![MITRE ATT&CK](https://img.shields.io/badge/MITRE-ATT%26CK-red.svg)](https://attack.mitre.org/)
[![ATT&CK Coverage](https://img.shields.io/badge/ATT%26CK_Coverage-28%2B_Techniques-orange.svg)]()

---

## 📚 Sobre o Projeto

Este repositório foi criado com o objetivo de fornecer um **guia educacional completo** para quem está aprendendo sobre Red Team, segurança ofensiva e pentesting de forma **ética e responsável**.

**Novidades da v1.1:**
- ✅ Mapeamento completo MITRE ATT&CK ([veja layer JSON](MITRE-ATTACK-MAPPING.json))
- ✅ Templates profissionais de relatórios forenses
- ✅ Playbooks práticos de resposta a incidentes
- ✅ Scripts com validação robusta e modo dry-run
- ✅ Recursos externos consolidados (CVE, Shodan, mapas de ameaças)
- ✅ Documentação de governança (Contributing, Code of Conduct)

Desenvolvido por **Samuel Ziger** como recurso educacional para a comunidade de segurança da informação.

### 🎓 Para quem é este repositório?

**TIER 1 - Iniciantes:**
- Fundamentos de Red Team e reconhecimento
- Primeiros passos em OSINT
- Scripts básicos de automação

**TIER 2 - Intermediário:**
- Active Directory avançado
- Privilege escalation
- Lateral movement

**TIER 3 - Avançado:**
- Evasion techniques
- Custom tooling
- Full Red Team operations

**TIER 4 - Profissional:**
- C2 Infrastructure
- Professional reporting
- Real-world engagements

---

## ⚠️ IMPORTANTE: Disclaimer de Uso Ético

```
⚖️ ESTE REPOSITÓRIO É EXCLUSIVAMENTE EDUCACIONAL

Todo o conteúdo aqui presente foi desenvolvido para fins de:
✅ Aprendizado e educação em segurança da informação
✅ Pesquisa acadêmica e profissional
✅ Treinamento em ambientes controlados e autorizados
✅ Preparação para certificações (OSCP, CRTP, etc.)

❌ NUNCA utilize estas técnicas sem autorização explícita
❌ NUNCA ataque sistemas que não são seus
❌ NUNCA use este conhecimento para atividades ilegais

O autor não se responsabiliza pelo uso indevido deste material.
Sempre respeite as leis locais e internacionais sobre cibersegurança.
```

---

## 📁 Estrutura do Repositório

```
RedTeam-Essentials/
│
├── 📖 README.md (você está aqui)
│
├── 🔍 01-Recon/
│   ├── passive_recon_cheatsheet.md    # Guia completo de reconhecimento passivo
│   ├── dns_enum.ps1                    # Script para enumeração DNS segura
│   └── web_recon_notes.md              # Notas sobre reconhecimento web
│
├── 🕵️ 02-OSINT/
│   ├── osint-tools-list.md             # Lista de ferramentas OSINT legais
│   └── osint_automation.ps1            # Automação de coleta OSINT ética
│
├── 🏢 03-AD-Notes/
│   ├── ad_enum_commands.md             # Comandos de enumeração do Active Directory
│   ├── kerberoasting_teoria.md         # Teoria sobre Kerberoasting
│   └── bloodhound_teoria.md            # Como funciona o BloodHound
│
├── ⚙️ 04-Automation/
│   ├── windows_setup_clean.ps1         # Automação de configuração Windows
│   ├── linux_postinstall.sh            # Script pós-instalação Linux
│   └── organize_logs.ps1               # Organizador de logs de testes
│
├── 🔬 05-DFIR/
│   ├── windows_event_logs.md           # Análise de logs do Windows
│   ├── forensics_artifacts.md          # Artefatos forenses importantes
│   ├── memory_analysis_teoria.md       # Teoria de análise de memória
│   ├── FORENSIC_REPORT_TEMPLATE.md     # Template profissional de relatório forense
│   └── PLAYBOOK_RANSOMWARE.md          # Playbook de resposta a ransomware
│
└── 📝 06-Cheatsheets/
    ├── powershell_cheatsheet.md        # Comandos PowerShell essenciais
    ├── linux_privesc_teoria.md         # Teoria de escalação de privilégios Linux
    └── windows_lateral_movement_teoria.md  # Movimento lateral no Windows
```

---

## 📖 Documentação Expandida

### 📚 Governança e Processos

- 🗺️ **[ROADMAP.md](ROADMAP.md)** - Trilha completa de estudos (Tier 1 → Tier 4) com integração MITRE ATT&CK
- 🤝 **[CONTRIBUTING.md](CONTRIBUTING.md)** - Guia detalhado para contribuições com templates e padrões
- 📜 **[CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)** - Código de conduta e uso ético
- 📝 **[CHANGELOG.md](CHANGELOG.md)** - Histórico de mudanças e versões
- 🧪 **[LAB-SETUP.md](LAB-SETUP.md)** - Configuração de laboratório completo (VMs, AD, plataformas online)
- 📄 **[REPORT-TEMPLATE.md](REPORT-TEMPLATE.md)** - Template profissional para relatórios Red Team
- ✅ **[validate_scripts.ps1](validate_scripts.ps1)** - Sistema de validação automatizada de scripts

### 🌐 Recursos Técnicos

- 🎯 **[MITRE-ATTACK-MAPPING.json](MITRE-ATTACK-MAPPING.json)** - Layer do ATT&CK Navigator com cobertura de técnicas
- 🔗 **[RESOURCES.md](RESOURCES.md)** - Links para:
  - Mapas globais de ameaças (Kaspersky, Radware, NetScout)
  - CVE Database e bancos de vulnerabilidades
  - Shodan e motores de busca de segurança
  - Plataformas de treinamento (TryHackMe, HTB, etc)
  - Ferramentas e frameworks essenciais

---

## 🚀 Como Usar Este Repositório

### 1️⃣ Clone o Repositório
```bash
git clone https://github.com/Samuel-Ziger/RedTeam-Essentials.git
cd RedTeam-Essentials
```

### 2️⃣ Navegue pelas Pastas
Cada pasta contém conteúdo específico sobre um tópico. Comece pela ordem numérica se você for iniciante:

1. **01-Recon**: Aprenda sobre reconhecimento e coleta de informações
2. **02-OSINT**: Entenda como coletar inteligência de fontes abertas
3. **03-AD-Notes**: Estude Active Directory e ataques relacionados
4. **04-Automation**: Use scripts para automatizar tarefas legítimas
5. **05-DFIR**: Aprenda sobre forense digital e resposta a incidentes
6. **06-Cheatsheets**: Consulte guias rápidos de referência

### 3️⃣ Siga a Trilha de Aprendizado

**Recomendado:** Siga o [ROADMAP.md](ROADMAP.md) para aprendizado estruturado

```
Semana 1-2: TIER 1 - Fundamentos
├─ Módulo 01: Reconhecimento
├─ Módulo 02: OSINT
└─ Configurar laboratório (LAB-SETUP.md)

Semana 3-8: TIER 2 - Intermediário
├─ Módulo 03: Active Directory
├─ Módulo 06: Privilege Escalation
└─ Praticar em labs online

Semana 9+: TIER 3 e 4 - Avançado
├─ Técnicas de evasion
├─ Full engagement simulations
└─ Preparação para certificações (OSCP, CRTP)
```

### 4️⃣ Execute os Scripts com Segurança
Todos os scripts foram desenvolvidos para serem executados **apenas em ambientes controlados**:

```powershell
# Windows PowerShell - Validar scripts primeiro
.\validate_scripts.ps1  # Valida todos os scripts

# Executar script específico
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\01-Recon\dns_enum.ps1 -Domain "exemplo.com"
```

```bash
# Linux
chmod +x script.sh
./04-Automation/linux_postinstall.sh
```

---

## 🎯 O Que Você Vai Aprender

### 🔍 Reconhecimento (Recon)
- Técnicas de reconhecimento passivo
- Enumeração de DNS, subdomínios e serviços
- Footprinting e fingerprinting
- Coleta de informações sem interagir diretamente com o alvo

### 🕵️ OSINT (Open Source Intelligence)
- Ferramentas para coleta de informações públicas
- Técnicas de pesquisa avançada
- Automação de processos OSINT
- Correlação de dados de múltiplas fontes

### 🏢 Active Directory
- Enumeração de usuários, grupos e políticas
- Ataques teóricos: Kerberoasting, AS-REP Roasting
- Análise de relações com BloodHound
- Movimento lateral e persistência

### ⚙️ Automação
- Scripts para configuração de ambientes de teste
- Organização de logs e evidências
- Automação de tarefas repetitivas
- Melhores práticas de scripting

### 🔬 DFIR (Digital Forensics & Incident Response)
- Análise de logs do Windows
- Artefatos forenses importantes
- Análise de memória e disco
- Timeline e reconstrução de eventos

### 📝 Cheatsheets
- Comandos PowerShell essenciais
- Teoria de privilege escalation
- Lateral movement e persistência
- Referências rápidas para pentesting

---

## 🛠️ Pré-requisitos

### Conhecimentos Recomendados
- ✅ Fundamentos de redes (TCP/IP, DNS, HTTP)
- ✅ Conhecimento básico de Windows e Linux
- ✅ Conceitos de segurança da informação
- ✅ PowerShell e Bash (básico)

### Ambiente de Estudo
- **Máquina Virtual** (VMware, VirtualBox, Hyper-V)
- **Windows 10/11** ou **Linux** (Kali, Parrot, Ubuntu)
- **Active Directory Lab** (opcional, mas recomendado)
- **Conexão à Internet** (para OSINT)

### Recursos Adicionais e Labs Online

**Plataformas Gratuitas:**
- 🎓 [TryHackMe](https://tryhackme.com/) - Aprendizado guiado com labs interativos
- 🏴‍☠️ [HackTheBox](https://www.hackthebox.com/) - Máquinas realistas (Free tier disponível)
- 🧃 [OWASP Juice Shop](https://juice-shop.herokuapp.com/) - Web app vulnerável
- 🌐 [PortSwigger Web Security Academy](https://portswigger.net/web-security) - 100% gratuito
- 📚 [VulnHub](https://www.vulnhub.com/) - VMs vulneráveis para download

**Plataformas Pagas (com free tier):**
- 🏢 [PentesterLab](https://pentesterlab.com/) - Exercícios práticos
- 🔍 [Root-Me](https://www.root-me.org/) - Challenges categorizados
- 🎯 [CyberDefenders](https://cyberdefenders.org/) - Blue Team / DFIR

**Veja guia completo:** [LAB-SETUP.md](LAB-SETUP.md)

---

## 📖 Metodologia de Estudo Recomendada

```
┌─────────────────────────────────────────┐
│  1. Leia a Teoria (arquivos .md)        │
│  2. Entenda os Conceitos                │
│  3. Analise os Scripts (linha por linha)│
│  4. Pratique em Ambiente Controlado     │
│  5. Documente Seus Aprendizados         │
│  6. Revise os Cheatsheets               │
└─────────────────────────────────────────┘
```

### Dica de Ouro 💡
> **Não apenas copie e cole comandos!** 
> 
> Entenda o que cada linha faz. Leia os comentários nos scripts.
> Modifique, teste e experimente. O aprendizado real vem da prática consciente.

---

## 🤝 Contribuindo

Contribuições são muito bem-vindas! Este projeto cresce com a comunidade.

**Antes de contribuir, leia:** [CONTRIBUTING.md](CONTRIBUTING.md)

### Processo de Contribuição

1. **Fork** o projeto
2. **Clone** seu fork: `git clone https://github.com/seu-usuario/RedTeam-Essentials.git`
3. **Crie uma branch:** `git checkout -b feature/NovoConteudo`
4. **Faça suas alterações** seguindo os padrões de código
5. **Valide scripts:** `.\validate_scripts.ps1`
6. **Commit:** `git commit -m "feat: Adiciona novo conteúdo sobre X"`
7. **Push:** `git push origin feature/NovoConteudo`
8. **Abra um Pull Request** usando o template

### Padrões de Qualidade

**Scripts PowerShell:**
- ✅ Header completo com `.SYNOPSIS`, `.DESCRIPTION`, `.EXAMPLE`
- ✅ Tratamento de erros (`try/catch`)
- ✅ Validação de parâmetros
- ✅ Logging adequado
- ✅ Disclaimer de segurança

**Scripts Bash:**
- ✅ Shebang `#!/bin/bash`
- ✅ `set -euo pipefail`
- ✅ Funções de logging com cores
- ✅ Validação de ambiente
- ✅ Cleanup em caso de erro

**Documentação:**
- ✅ Markdown bem formatado
- ✅ Exemplos práticos
- ✅ Referências externas
- ✅ Mapeamento MITRE ATT&CK (quando aplicável)

### Sistema de Testes

```powershell
# Validar todos os scripts
.\validate_scripts.ps1

# Validar script específico
.\validate_scripts.ps1 -ScriptPath ".\01-Recon\dns_enum.ps1"
```

### Regras de Ouro
- ✅ Conteúdo **educacional** e **ético**
- ✅ Scripts **comentados linha por linha**
- ✅ Documentação **clara e didática**
- ❌ Exploits ofensivos prontos para uso malicioso
- ❌ Conteúdo que viole leis ou políticas

---

## 📜 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

```
MIT License

Copyright (c) 2025 RedTeam Essentials

A permissão é concedida para uso educacional e pessoal.
Sempre respeite as leis e use este conhecimento de forma ética.
```

---

## 📞 Contato e Recursos

### Canais Recomendados
- 📺 **YouTube**: IppSec, John Hammond, LiveOverflow
- 🐦 **Twitter**: @_JohnHammond, @IppSec, @TCM_Sec
- 💬 **Discord**: Comunidades de InfoSec e CTF
- 📚 **Livros**: "The Hacker Playbook", "Red Team Field Manual"

### Certificações Relacionadas
- 🎓 **OSCP** (Offensive Security Certified Professional)
- 🎓 **CRTP** (Certified Red Team Professional)
- 🎓 **PNPT** (Practical Network Penetration Tester)
- 🎓 **eCPPT** (eLearnSecurity Certified Professional Penetration Tester)

---

## 🌟 Agradecimentos

Este repositório foi criado com muito carinho para a comunidade de segurança da informação. 

Agradeço a todos que compartilham conhecimento de forma aberta e ética, contribuindo para um mundo digital mais seguro.

---

## 📊 Status do Projeto

```
[████████████████████] v1.0.0 - Lançamento Completo

✅ Todos os módulos implementados (01-06)
✅ Documentação completa e expandida
✅ Scripts comentados linha por linha
✅ ROADMAP com integração MITRE ATT&CK
✅ Guia de configuração de laboratório
✅ Template profissional de relatórios
✅ Sistema de validação automatizada
✅ Guia de contribuição detalhado
✅ Conteúdo revisado e testado
✅ Pronto para uso educacional
```

### 🗓️ Roadmap Futuro

**Q1 2026:**
- [ ] Expandir módulo de evasion techniques
- [ ] Adicionar módulo de Cloud Red Team (AWS, Azure)
- [ ] Criar vídeos tutoriais para cada módulo
- [ ] Implementar CI/CD para validação automática

**Q2 2026:**
- [ ] Labs automatizados com Terraform/Ansible
- [ ] CTF baseado no repositório
- [ ] Playbooks de engagements reais (anonimizados)
- [ ] Integração com plataformas de treinamento

**Q3 2026:**
- [ ] Módulo de post-exploitation avançado
- [ ] Templates de relatórios em múltiplos formatos
- [ ] Comunidade Discord oficial
- [ ] Certificação própria (opcional)

### 📈 Estatísticas

- **Scripts PowerShell:** 5 (totalmente documentados)
- **Scripts Bash:** 1 (com validações completas)
- **Documentos Markdown:** 15+ (teoria e guias)
- **Técnicas MITRE ATT&CK Cobertas:** 30+
- **Exercícios Práticos:** 10+
- **Horas de Conteúdo:** 40+ horas de estudo

---

## 👥 Créditos e Agradecimentos

### Autor Principal
**Samuel Ziger**  
GitHub: [@Samuel-Ziger](https://github.com/Samuel-Ziger)  
Repositório: [RedTeam-Essentials](https://github.com/Samuel-Ziger/RedTeam-Essentials)

### Contribuidores
Agradecimentos especiais a todos que contribuíram com código, documentação e feedback.

*Veja a lista completa em [Contributors](https://github.com/Samuel-Ziger/RedTeam-Essentials/graphs/contributors)*

### Recursos e Inspirações
Este projeto foi inspirado e utiliza conhecimento de:
- MITRE ATT&CK Framework
- OWASP Testing Guide
- PTES (Penetration Testing Execution Standard)
- Comunidade InfoSec global

---

## 📜 Versionamento

**Versão Atual:** 1.0.0 (Novembro 2025)

### Changelog

**v1.0.0 - 22/11/2025**
- ✨ Lançamento inicial completo
- ✨ Adicionado ROADMAP com 4 tiers de aprendizado
- ✨ Criado CONTRIBUTING.md com padrões detalhados
- ✨ Implementado LAB-SETUP.md com guias de VM e plataformas
- ✨ Template profissional de relatórios Red Team
- ✨ Sistema de validação automatizada de scripts
- ✨ READMEs individuais para cada módulo
- ✨ Mapeamento completo com MITRE ATT&CK
- 🐛 Correções de bugs em scripts existentes
- 📚 Documentação expandida em todos os módulos

**v0.1.0 - 01/11/2025**
- 🎉 Versão inicial do repositório
- 📁 Estrutura básica de módulos (01-06)
- 📝 Scripts PowerShell e Bash iniciais
- 📖 Documentação básica

---

## 🔗 Links Úteis

### Documentação
- [ROADMAP Completo](ROADMAP.md)
- [Guia de Contribuição](CONTRIBUTING.md)
- [Configuração de Laboratório](LAB-SETUP.md)
- [Template de Relatório](REPORT-TEMPLATE.md)

### Comunidade
- [Issues](https://github.com/Samuel-Ziger/RedTeam-Essentials/issues) - Reporte bugs ou sugira melhorias
- [Discussions](https://github.com/Samuel-Ziger/RedTeam-Essentials/discussions) - Tire dúvidas e compartilhe conhecimento
- [Pull Requests](https://github.com/Samuel-Ziger/RedTeam-Essentials/pulls) - Contribua com código

### Recursos Externos
- 🎯 [MITRE ATT&CK Framework](https://attack.mitre.org/)
- 🗺️ [Kaspersky Threat Map](https://cybermap.kaspersky.com/)
- 🗺️ [Radware Threat Map](https://livethreatmap.radware.com/)
- 🗺️ [NetScout Cyber Horizon](https://horizon.netscout.com/)
- 🔓 [CVE Database](https://www.cve.org/)
- 🔍 [Shodan](https://www.shodan.io/)
- 🎓 [TryHackMe](https://tryhackme.com/)
- 🎓 [HackTheBox](https://www.hackthebox.com/)
- 🌐 [OWASP](https://owasp.org/)

**Veja lista completa em:** [RESOURCES.md](RESOURCES.md)

---

## 🎯 Integração MITRE ATT&CK

Este repositório está completamente mapeado para o **MITRE ATT&CK Framework**, permitindo que você:

### Como Usar o Mapeamento

1. **Visualizar Cobertura:**
   ```bash
   # 1. Acesse https://mitre-attack.github.io/attack-navigator/
   # 2. Clique em "Open Existing Layer"
   # 3. Faça upload do arquivo MITRE-ATTACK-MAPPING.json
   # 4. Veja as 28+ técnicas cobertas pelo repositório
   ```

2. **Estudar por Tática:**
   - **Reconnaissance** (TA0043): Módulo 01-Recon, 02-OSINT
   - **Discovery** (TA0007): Módulo 03-AD-Notes
   - **Credential Access** (TA0006): Kerberoasting, AS-REP Roasting
   - **Lateral Movement** (TA0008): Módulo 06-Cheatsheets
   - **Privilege Escalation** (TA0004): Linux/Windows Privesc

3. **Mapear seus Estudos:**
   - Cada técnica estudada tem ID oficial (ex: T1558.003)
   - Use os IDs em suas notas e relatórios
   - Correlacione com APTs reais da matriz ATT&CK

### Técnicas Cobertas

| Tática | Técnicas Cobertas | Módulos |
|--------|-------------------|---------|
| **Reconnaissance** | T1590, T1592, T1593, T1594, T1596, T1598 | 01-Recon, 02-OSINT |
| **Execution** | T1059.001, T1059.004 | 06-Cheatsheets |
| **Credential Access** | T1003, T1558.003, T1558.004 | 03-AD-Notes |
| **Discovery** | T1069, T1083, T1087, T1482 | 03-AD-Notes |
| **Lateral Movement** | T1021.001, T1021.002, T1021.006, T1550 | 06-Cheatsheets |
| **Collection** | T1119 | 04-Automation |
| **Defense Evasion** | T1027, T1055, T1070, T1562 | Planejado |

**Total:** 28+ técnicas mapeadas e documentadas

---

## 🛡️ Segurança e Melhores Práticas

### ⚠️ Antes de Executar Scripts

```powershell
# 1. SEMPRE valide scripts primeiro
.\validate_scripts.ps1

# 2. Execute em ambiente ISOLADO
# - VM dedicada
# - Rede segmentada
# - Snapshots configurados

# 3. Nunca execute em produção
# 4. Sempre use modo dry-run quando disponível
```

### 🔒 Proteções Implementadas

Todos os scripts neste repositório incluem:

✅ **Validação de Entrada:** Parâmetros são validados antes da execução  
✅ **Tratamento de Erros:** Try/Catch em todas as operações críticas  
✅ **Logging Detalhado:** Ações são registradas com timestamps  
✅ **Disclaimers Éticos:** Avisos sobre uso autorizado  
✅ **Modo Dry-Run:** Simulação antes de executar (quando aplicável)  
✅ **Documentação Inline:** Comentários explicando cada passo

### 📋 Checklist de Segurança

Antes de usar qualquer técnica deste repositório:

- [ ] Você tem **autorização por escrito** para testar o sistema?
- [ ] Você está em um **ambiente de laboratório isolado**?
- [ ] Você tem **backups** de sistemas que vai testar?
- [ ] Você documentou o **escopo** do teste?
- [ ] Você conhece as **leis locais** sobre testes de penetração?
- [ ] Você tem um **plano de rollback** se algo der errado?

---

## 🚨 Resposta a Incidentes (DFIR)

### Playbooks Disponíveis

Este repositório agora inclui playbooks profissionais de resposta a incidentes:

📘 **[PLAYBOOK_RANSOMWARE.md](05-DFIR/PLAYBOOK_RANSOMWARE.md)**
- Resposta completa a incidentes de ransomware
- Timeline de 0-72 horas
- Checklist de contenção e recuperação
- Decisão sobre pagamento
- Lições aprendidas

### Templates Forenses

📄 **[FORENSIC_REPORT_TEMPLATE.md](05-DFIR/FORENSIC_REPORT_TEMPLATE.md)**
- Template completo de relatório forense
- Chain of custody
- Análise de IOCs
- Recomendações priorizadas
- Baseado em NIST SP 800-61

### Uso dos Playbooks

```bash
# 1. Em caso de incidente, acesse o playbook relevante
# 2. Siga os passos na ordem indicada
# 3. Documente TODAS as ações tomadas
# 4. Use os templates para gerar relatórios
```

---

## 🌟 Destaques do Projeto
- [HackTheBox](https://www.hackthebox.com/)

---

<div align="center">

### 🎯 Lembre-se: Com grandes poderes vêm grandes responsabilidades

**Use este conhecimento para o bem. Seja ético. Aprenda constantemente.**

---

**⭐ Se este repositório foi útil, deixe uma estrela!**

**🔄 Compartilhe com quem está aprendendo segurança ofensiva**

**🤝 Contribua e ajude a construir este recurso educacional**

---

*Desenvolvido com 💙 por **Samuel Ziger** para a comunidade de InfoSec*

*Copyright © 2025 RedTeam Essentials - Licença MIT*

[![Stargazers](https://img.shields.io/github/stars/Samuel-Ziger/RedTeam-Essentials?style=social)](https://github.com/Samuel-Ziger/RedTeam-Essentials/stargazers)
[![Forks](https://img.shields.io/github/forks/Samuel-Ziger/RedTeam-Essentials?style=social)](https://github.com/Samuel-Ziger/RedTeam-Essentials/network/members)

</div>
