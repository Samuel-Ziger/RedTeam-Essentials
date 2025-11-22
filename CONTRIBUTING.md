# 🤝 Guia de Contribuição - Red Team Essentials

Obrigado por considerar contribuir para o **Red Team Essentials**! Este documento fornece diretrizes para garantir contribuições de alta qualidade, éticas e educacionais.

---

## 📜 Código de Conduta

### Princípios Fundamentais

Este projeto é **exclusivamente educacional** e segue princípios éticos rigorosos:

✅ **PERMITIDO:**
- Conteúdo educacional e didático
- Scripts com comentários detalhados
- Teoria fundamentada e referenciada
- Técnicas documentadas com disclaimer ético
- Ferramentas defensivas e de análise
- Melhorias de documentação
- Correções de erros

❌ **NÃO PERMITIDO:**
- Ferramentas ofensivas diretas (exploits prontos para uso malicioso)
- Código malicioso sem propósito educacional claro
- Técnicas sem contexto ético
- Conteúdo que viole leis locais ou internacionais
- Material que promova atividades ilegais
- Bypass de segurança sem disclaimer adequado

### Responsabilidade

Ao contribuir, você concorda que:
1. Seu conteúdo é original ou devidamente atribuído
2. Você não está violando propriedade intelectual de terceiros
3. O conteúdo tem propósito educacional claro
4. Você entende os riscos éticos e legais do material compartilhado

---

## 🚀 Como Contribuir

### 1. Tipos de Contribuição

#### 📝 Documentação
- Corrigir erros de ortografia ou gramática
- Melhorar explicações técnicas
- Adicionar referências e fontes
- Traduzir conteúdo (futuro)
- Criar diagramas e visualizações

#### 💻 Scripts e Automação
- Adicionar novos scripts educacionais
- Melhorar scripts existentes (performance, segurança)
- Adicionar validações e tratamento de erros
- Documentar código linha por linha
- Criar testes automatizados

#### 🎓 Conteúdo Educacional
- Adicionar novos módulos teóricos
- Expandir cheatsheets existentes
- Criar exercícios práticos
- Adicionar estudos de caso
- Mapear técnicas para MITRE ATT&CK

#### 🐛 Correções
- Reportar bugs em scripts
- Corrigir problemas de compatibilidade
- Atualizar dependências obsoletas
- Melhorar mensagens de erro

---

### 2. Processo de Contribuição

#### Passo 1: Fork e Clone
```bash
# Fork o repositório pelo GitHub
# Clone seu fork
git clone https://github.com/SEU-USUARIO/RedTeam-Essentials.git
cd RedTeam-Essentials

# Adicione o repositório original como upstream
git remote add upstream https://github.com/Samuel-Ziger/RedTeam-Essentials.git
```

#### Passo 2: Crie uma Branch
```bash
# Atualize seu fork
git checkout main
git pull upstream main

# Crie uma branch descritiva
git checkout -b feature/nome-da-feature
# ou
git checkout -b fix/nome-do-bug
# ou
git checkout -b docs/melhoria-documentacao
```

**Convenção de Nomes de Branch:**
- `feature/` - Nova funcionalidade ou conteúdo
- `fix/` - Correção de bugs
- `docs/` - Melhorias de documentação
- `refactor/` - Refatoração de código
- `test/` - Adição de testes

#### Passo 3: Faça as Alterações

Siga os padrões de código e documentação (veja seções abaixo).

#### Passo 4: Commit
```bash
# Adicione os arquivos modificados
git add .

# Commit com mensagem descritiva
git commit -m "tipo: descrição breve"
```

**Convenção de Mensagens de Commit:**
```
feat: Adiciona novo módulo sobre lateral movement
fix: Corrige erro no script de DNS enumeration
docs: Atualiza README com novas seções
refactor: Melhora estrutura do script de OSINT
test: Adiciona validação para organize_logs.ps1
style: Padroniza headers dos scripts PowerShell
```

**Formato Detalhado:**
```
tipo: Resumo em uma linha (máx 72 caracteres)

Descrição mais detalhada, se necessário.
Explique WHAT e WHY, não HOW.

- Pode usar bullet points
- Para listar mudanças específicas

Refs: #123 (se relacionado a uma issue)
```

#### Passo 5: Push
```bash
git push origin feature/nome-da-feature
```

#### Passo 6: Pull Request

1. Acesse seu fork no GitHub
2. Clique em "Compare & pull request"
3. Preencha o template de PR (veja abaixo)
4. Aguarde review

---

### 3. Template de Pull Request

```markdown
## 📋 Descrição

[Descreva de forma clara e concisa o que este PR faz]

## 🎯 Tipo de Mudança

- [ ] 📝 Documentação (correções, melhorias)
- [ ] ✨ Nova feature (script, módulo, conteúdo)
- [ ] 🐛 Bug fix (correção de erro)
- [ ] 🔨 Refatoração (melhoria de código existente)
- [ ] 🧪 Testes (adição de validações)

## ✅ Checklist

- [ ] Código segue os padrões do projeto
- [ ] Scripts têm headers padronizados
- [ ] Documentação foi atualizada
- [ ] Comentários adequados foram adicionados
- [ ] Testado em ambiente local
- [ ] Disclaimer ético incluído (se aplicável)
- [ ] Referências adicionadas (se aplicável)

## 🧪 Como Testar

[Instruções de como testar as mudanças]

## 📸 Screenshots (se aplicável)

[Adicione screenshots se houver mudanças visuais]

## 📚 Referências

[Links, artigos, documentação relevante]

## ⚠️ Notas Adicionais

[Qualquer informação adicional relevante]
```

---

## 📏 Padrões de Código

### PowerShell Scripts

#### Header Obrigatório
```powershell
<#
.SYNOPSIS
    Breve descrição do que o script faz

.DESCRIPTION
    Descrição detalhada do propósito e funcionamento do script.
    Explique o contexto educacional e casos de uso.

.PARAMETER ParameterName
    Descrição do parâmetro

.EXAMPLE
    .\script.ps1 -ParameterName "valor"
    Descrição do exemplo

.NOTES
    File Name      : script.ps1
    Author         : Nome do Autor
    Prerequisite   : PowerShell 5.1+
    Version        : 1.0
    Creation Date  : DD/MM/YYYY
    Last Modified  : DD/MM/YYYY

.LINK
    https://github.com/Samuel-Ziger/RedTeam-Essentials

.WARNING
    ⚠️ USO APENAS EM AMBIENTES AUTORIZADOS
    Este script é para fins educacionais.
    Uso não autorizado pode violar leis locais/internacionais.
    Sempre obtenha permissão explícita antes de executar.
#>

[CmdletBinding()]
param (
    [Parameter(Mandatory=$true)]
    [string]$ParameterName
)

# Configuração de erro
$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

# Validações de segurança
if (-not (Test-Path "C:\LabEnvironment")) {
    Write-Error "⚠️ AVISO: Execute apenas em ambiente de laboratório!"
    exit 1
}

# Função de logging
function Write-Log {
    param([string]$Message, [string]$Level = "INFO")
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    Write-Host "[$timestamp] [$Level] $Message"
}

# Código principal
try {
    Write-Log "Iniciando script..."
    
    # Seu código aqui
    
    Write-Log "Script concluído com sucesso" -Level "SUCCESS"
}
catch {
    Write-Log "Erro: $_" -Level "ERROR"
    exit 1
}
```

#### Boas Práticas PowerShell
- ✅ Use `[CmdletBinding()]` para funções avançadas
- ✅ Defina `$ErrorActionPreference = "Stop"`
- ✅ Use `Try/Catch` para tratamento de erros
- ✅ Valide parâmetros com `[Parameter(Mandatory=$true)]`
- ✅ Adicione `Set-StrictMode -Version Latest`
- ✅ Comente código complexo
- ✅ Use funções para código reutilizável
- ✅ Implemente logging adequado
- ✅ Adicione validações de ambiente (ex: detectar se é lab)

---

### Bash Scripts

#### Header Obrigatório
```bash
#!/bin/bash

################################################################################
# Script Name    : script.sh
# Description    : Breve descrição do script
# Author         : Nome do Autor
# Email          : email@example.com
# Created        : DD/MM/YYYY
# Last Modified  : DD/MM/YYYY
# Version        : 1.0
# Usage          : ./script.sh [options]
# Requirements   : bash 4.0+, tool1, tool2
################################################################################

################################################################################
# ⚠️  AVISO DE SEGURANÇA
# Este script é para fins EDUCACIONAIS apenas.
# Execute APENAS em ambientes autorizados e controlados.
# O uso não autorizado pode violar leis locais e internacionais.
# O autor não se responsabiliza pelo uso indevido.
################################################################################

# Configuração de erro rigorosa
set -euo pipefail
IFS=$'\n\t'

# Cores para output
readonly RED='\033[0;31m'
readonly GREEN='\033[0;32m'
readonly YELLOW='\033[1;33m'
readonly NC='\033[0m' # No Color

# Função de logging
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1" >&2
}

# Validação de ambiente
check_environment() {
    if [[ ! -f "/etc/lab_environment" ]]; then
        log_error "⚠️ Execute apenas em ambiente de laboratório!"
        exit 1
    fi
}

# Função principal
main() {
    log_info "Iniciando script..."
    
    # Verificações de segurança
    check_environment
    
    # Seu código aqui
    
    log_info "Script concluído com sucesso"
}

# Trap para cleanup em caso de erro
cleanup() {
    log_warn "Executando cleanup..."
}
trap cleanup EXIT

# Executar
main "$@"
```

#### Boas Práticas Bash
- ✅ Use `set -euo pipefail` (fail fast)
- ✅ Adicione shebang `#!/bin/bash`
- ✅ Valide dependências no início
- ✅ Use funções para organização
- ✅ Implemente logging com cores
- ✅ Adicione trap para cleanup
- ✅ Valide inputs de usuário
- ✅ Documente variáveis importantes
- ✅ Use `readonly` para constantes

---

### Documentação Markdown

#### Estrutura de Arquivo .md
```markdown
# 🎯 Título Principal

> Descrição breve e objetiva do conteúdo

---

## 📚 Introdução

Contexto e propósito do documento.

---

## 🎯 Objetivos de Aprendizado

Ao completar este módulo, você será capaz de:
- [ ] Objetivo 1
- [ ] Objetivo 2
- [ ] Objetivo 3

---

## 📋 Pré-requisitos

- Conhecimento de X
- Experiência com Y
- Acesso a Z

---

## 🔍 Conteúdo Principal

### Seção 1

Explicação detalhada...

#### Subseção 1.1

```bash
# Exemplo de código
comando --option valor
```

**Explicação:**
- `comando`: descrição
- `--option`: descrição

---

## 🧪 Prática

### Exercício 1

**Objetivo:** [descrição]

**Passos:**
1. Passo 1
2. Passo 2
3. Passo 3

**Validação:**
- Como saber se deu certo

---

## 🛡️ Considerações de Segurança

⚠️ **IMPORTANTE:**
- Sempre executar em ambiente isolado
- Obter autorização prévia
- Documentar todas as ações

---

## 📚 Referências

- [Título do Link](URL) - Descrição
- [Livro/Artigo](URL) - Descrição

---

## 🔗 Recursos Adicionais

- Ferramenta 1: [Link](URL)
- Ferramenta 2: [Link](URL)

---

## ❓ FAQ

**P: Pergunta comum?**
R: Resposta detalhada.

---

## 📝 Notas do Autor

Observações adicionais, dicas ou contexto.

---

<div align="center">

**Próximo:** [Próximo Módulo](link.md)  
**Anterior:** [Módulo Anterior](link.md)

---

*Parte do projeto [RedTeam Essentials](../../README.md)*

</div>
```

#### Boas Práticas Markdown
- ✅ Use emojis para hierarquia visual
- ✅ Adicione TOC (Table of Contents) em docs longos
- ✅ Use code blocks com syntax highlighting
- ✅ Adicione links de navegação (anterior/próximo)
- ✅ Inclua exemplos práticos
- ✅ Referencie fontes externas
- ✅ Use tabelas para comparações
- ✅ Adicione disclaimer ético quando relevante

---

## 🧪 Testes e Validação

### Scripts PowerShell

Crie arquivo de teste: `script.Tests.ps1`

```powershell
Describe "Nome do Script" {
    Context "Validação de Parâmetros" {
        It "Deve aceitar parâmetro válido" {
            { .\script.ps1 -Param "valor" } | Should -Not -Throw
        }
        
        It "Deve rejeitar parâmetro inválido" {
            { .\script.ps1 -Param "" } | Should -Throw
        }
    }
    
    Context "Funcionamento" {
        It "Deve criar arquivo de output" {
            .\script.ps1 -Param "teste"
            Test-Path "output.txt" | Should -Be $true
        }
    }
}
```

### Validação Manual

Antes de submeter PR:
1. Execute em ambiente limpo (VM fresca)
2. Teste com diferentes parâmetros
3. Verifique mensagens de erro
4. Valide outputs gerados
5. Confirme que disclaimer aparece

---

## 📂 Estrutura de Diretórios

Ao adicionar novo conteúdo, siga a estrutura:

```
01-Recon/
├── README.md                    # Visão geral do módulo
├── passive_recon_cheatsheet.md  # Documentação
├── dns_enum.ps1                 # Script
├── dns_enum.Tests.ps1           # Testes (opcional)
└── examples/                    # Exemplos de uso
    └── dns_enum_example.txt
```

### Convenções de Nomenclatura

- **Scripts:** `snake_case.ps1` ou `snake_case.sh`
- **Documentação:** `snake_case_teoria.md` ou `snake_case_cheatsheet.md`
- **Exemplos:** `nome_example.txt`
- **Testes:** `nome.Tests.ps1`

---

## 🏷️ Issues e Bug Reports

### Template de Issue

```markdown
## 🐛 Descrição do Bug

[Descrição clara e concisa do problema]

## 🔄 Como Reproduzir

Passos:
1. Execute '...'
2. Com parâmetro '...'
3. Veja erro

## ✅ Comportamento Esperado

[O que deveria acontecer]

## ❌ Comportamento Atual

[O que está acontecendo]

## 💻 Ambiente

- OS: [Windows 10, Kali Linux, etc]
- PowerShell Version: [5.1, 7.2]
- Script Version: [1.0]

## 📸 Screenshots

[Se aplicável]

## 📝 Notas Adicionais

[Contexto adicional]
```

---

## 🎓 Recursos para Contribuidores

### Ferramentas Recomendadas

- **VS Code** com extensões:
  - PowerShell
  - Markdown All in One
  - Code Spell Checker
  - GitLens

- **Linters:**
  - PSScriptAnalyzer (PowerShell)
  - ShellCheck (Bash)
  - markdownlint

### Leitura Recomendada

- [PowerShell Best Practices](https://learn.microsoft.com/powershell/scripting/dev-cross-plat/performance/script-authoring-considerations)
- [Google Shell Style Guide](https://google.github.io/styleguide/shellguide.html)
- [Markdown Guide](https://www.markdownguide.org/)

---

## 🎖️ Reconhecimento de Contribuidores

Contribuidores serão reconhecidos:
- No README principal (seção Contributors)
- No CHANGELOG do release
- Em commit de agradecimento
- Badge de contributor no GitHub

---

## ⚖️ Licenciamento de Contribuições

### Developer Certificate of Origin (DCO)

Ao contribuir, você concorda com o DCO:

```
Developer Certificate of Origin
Version 1.1

By making a contribution to this project, I certify that:

(a) The contribution was created in whole or in part by me and I
    have the right to submit it under the open source license
    indicated in the file; or

(b) The contribution is based upon previous work that, to the best
    of my knowledge, is covered under an appropriate open source
    license and I have the right under that license to submit that
    work with modifications; or

(c) The contribution was provided directly to me by some other
    person who certified (a), (b) or (c) and I have not modified it.

(d) I understand and agree that this project and the contribution
    are public and that a record of the contribution is maintained
    indefinitely.
```

### Como Assinar

Adicione ao final da mensagem de commit:

```
Signed-off-by: Seu Nome <seu.email@example.com>
```

Ou use:
```bash
git commit -s -m "sua mensagem"
```

---

## 📞 Contato

### Dúvidas sobre Contribuição?

- Abra uma [Discussion](https://github.com/Samuel-Ziger/RedTeam-Essentials/discussions)
- Entre em contato via [Issues](https://github.com/Samuel-Ziger/RedTeam-Essentials/issues)

---

## 🙏 Agradecimentos

Obrigado por dedicar seu tempo para melhorar este projeto educacional!

Cada contribuição, por menor que seja, ajuda a comunidade de segurança da informação a crescer de forma ética e responsável.

---

<div align="center">

### 🎯 Juntos, construímos conhecimento seguro e ético

**Pronto para contribuir? Faça seu primeiro fork!**

---

*Documento mantido pela comunidade RedTeam Essentials*  
*Última atualização: Novembro 2025*

</div>
