# 🎯 RedTeam Essentials

> Um repositório educacional completo sobre Red Team, focado em aprendizado ético, teoria aprofundada e automação segura.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Educational](https://img.shields.io/badge/Purpose-Educational-green.svg)]()
[![Ethical](https://img.shields.io/badge/Content-Ethical-brightgreen.svg)]()

---

## 📚 Sobre o Projeto

Este repositório foi criado com o objetivo de fornecer um **guia educacional completo** para quem está aprendendo sobre Red Team, segurança ofensiva e pentesting de forma **ética e responsável**.

### 🎓 Para quem é este repositório?

- **Iniciantes** que querem entender os fundamentos de Red Team
- **Estudantes** de segurança da informação buscando material de estudo
- **Profissionais** que desejam revisar conceitos e comandos
- **Entusiastas** que querem aprender sobre segurança ofensiva de forma legal

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
│   └── memory_analysis_teoria.md       # Teoria de análise de memória
│
└── 📝 06-Cheatsheets/
    ├── powershell_cheatsheet.md        # Comandos PowerShell essenciais
    ├── linux_privesc_teoria.md         # Teoria de escalação de privilégios Linux
    └── windows_lateral_movement_teoria.md  # Movimento lateral no Windows
```

---

## 🚀 Como Usar Este Repositório

### 1️⃣ Clone o Repositório
```bash
git clone https://github.com/seu-usuario/RedTeam-Essentials.git
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

### 3️⃣ Execute os Scripts com Segurança
Todos os scripts foram desenvolvidos para serem executados **apenas em ambientes controlados**:

```powershell
# Windows PowerShell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\nome-do-script.ps1
```

```bash
# Linux
chmod +x script.sh
./script.sh
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

### Recursos Adicionais
- [HackTheBox](https://www.hackthebox.com/) - Laboratórios práticos
- [TryHackMe](https://tryhackme.com/) - Aprendizado guiado
- [VulnHub](https://www.vulnhub.com/) - Máquinas vulneráveis para prática

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

Contribuições são muito bem-vindas! Se você tem sugestões, correções ou quer adicionar conteúdo:

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/NovoConteudo`)
3. Commit suas mudanças (`git commit -m 'Adiciona novo conteúdo sobre X'`)
4. Push para a branch (`git push origin feature/NovoConteudo`)
5. Abra um Pull Request

### Regras para Contribuição
- ✅ Conteúdo deve ser **educacional** e **ético**
- ✅ Scripts devem ter **comentários detalhados**
- ✅ Documentação deve ser **clara** e **didática**
- ❌ Nada de ferramentas ofensivas diretas
- ❌ Nada que viole leis ou políticas

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
[████████████████████] 100% Completo

✅ Todos os módulos implementados
✅ Documentação completa
✅ Scripts comentados linha por linha
✅ Conteúdo revisado e testado
✅ Pronto para uso educacional
```

---

<div align="center">

### 🎯 Lembre-se: Com grandes poderes vêm grandes responsabilidades

**Use este conhecimento para o bem. Seja ético. Aprenda constantemente.**

---

**⭐ Se este repositório foi útil, deixe uma estrela!**

**🔄 Compartilhe com quem está aprendendo segurança ofensiva**

---

*Desenvolvido com 💙 para a comunidade de InfoSec*

</div>
