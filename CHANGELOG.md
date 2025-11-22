# Changelog

Todas as mudanças notáveis neste projeto serão documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/),
e este projeto adere ao [Semantic Versioning](https://semver.org/lang/pt-BR/).

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

## [Unreleased] - Roadmap Futuro

### 🔮 Planejado para Próximas Versões

#### v1.1.0 - Q1 2026
- [ ] Módulo de Evasion Techniques expandido
- [ ] Módulo de Cloud Red Team (AWS, Azure, GCP)
- [ ] Vídeos tutoriais para cada módulo
- [ ] CI/CD com GitHub Actions

#### v1.2.0 - Q2 2026
- [ ] Labs automatizados com Terraform/Ansible
- [ ] CTF baseado no repositório
- [ ] Playbooks de engagements reais (anonimizados)
- [ ] Integração com plataformas de treinamento

#### v1.3.0 - Q3 2026
- [ ] Módulo de post-exploitation avançado
- [ ] Templates de relatórios em múltiplos formatos (HTML, PDF)
- [ ] Comunidade Discord oficial
- [ ] Certificação própria (opcional)

#### v2.0.0 - 2027
- [ ] Restruturação completa para multi-idioma
- [ ] Plataforma web interativa
- [ ] Sistema de badges e gamificação
- [ ] Marketplace de scripts comunitários

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
