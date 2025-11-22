<#
.SYNOPSIS
    Script de validação para testes automatizados dos scripts PowerShell

.DESCRIPTION
    Este script valida a sintaxe e funcionalidade básica dos scripts
    PowerShell no repositório RedTeam Essentials.

.PARAMETER ScriptPath
    Caminho do script a ser testado

.PARAMETER RunTests
    Executa testes funcionais (modo dry-run)

.EXAMPLE
    .\validate_scripts.ps1 -ScriptPath ".\01-Recon\dns_enum.ps1"

.NOTES
    Autor: RedTeam Essentials
    Versão: 1.0
#>

param(
    [Parameter(Mandatory=$false)]
    [string]$ScriptPath = "",
    
    [Parameter(Mandatory=$false)]
    [switch]$RunTests
)

# Cores para output
$ColorSuccess = "Green"
$ColorInfo = "Cyan"
$ColorWarning = "Yellow"
$ColorError = "Red"

# Banner
Clear-Host
Write-Host "╔═══════════════════════════════════════════════════════════╗" -ForegroundColor $ColorInfo
Write-Host "║      Script Validator - RedTeam Essentials               ║" -ForegroundColor $ColorInfo
Write-Host "╚═══════════════════════════════════════════════════════════╝" -ForegroundColor $ColorInfo
Write-Host ""

# Função para validar sintaxe de PowerShell
function Test-PowerShellSyntax {
    param([string]$FilePath)
    
    Write-Host "[*] Validando sintaxe de: $FilePath" -ForegroundColor $ColorInfo
    
    try {
        # Tenta fazer parse do script
        $null = [System.Management.Automation.PSParser]::Tokenize((Get-Content $FilePath -Raw), [ref]$null)
        Write-Host "[✓] Sintaxe válida" -ForegroundColor $ColorSuccess
        return $true
    } catch {
        Write-Host "[!] Erro de sintaxe: $_" -ForegroundColor $ColorError
        return $false
    }
}

# Função para verificar boas práticas
function Test-BestPractices {
    param([string]$FilePath)
    
    Write-Host "[*] Verificando boas práticas..." -ForegroundColor $ColorInfo
    
    $content = Get-Content $FilePath -Raw
    $issues = @()
    
    # Verifica se tem header de documentação
    if ($content -notmatch '\.SYNOPSIS') {
        $issues += "Falta .SYNOPSIS no header"
    }
    
    # Verifica se tem CmdletBinding
    if ($content -notmatch '\[CmdletBinding\(\)\]') {
        $issues += "Falta [CmdletBinding()] para funções avançadas"
    }
    
    # Verifica se tem tratamento de erros
    if ($content -notmatch 'try\s*\{' -and $content -notmatch '\$ErrorActionPreference') {
        $issues += "Falta tratamento de erros (try/catch ou ErrorActionPreference)"
    }
    
    # Verifica disclaimer de segurança
    if ($content -notmatch 'IMPORTANTE|WARNING|AVISO') {
        $issues += "Falta disclaimer de segurança/ético"
    }
    
    if ($issues.Count -eq 0) {
        Write-Host "[✓] Todas as boas práticas seguidas" -ForegroundColor $ColorSuccess
        return $true
    } else {
        Write-Host "[!] Problemas encontrados:" -ForegroundColor $ColorWarning
        foreach ($issue in $issues) {
            Write-Host "    - $issue" -ForegroundColor $ColorWarning
        }
        return $false
    }
}

# Função principal
function Invoke-Validation {
    param([string]$Path)
    
    if ($Path -eq "") {
        # Testa todos os scripts .ps1 no repositório
        Write-Host "[*] Buscando todos os scripts PowerShell..." -ForegroundColor $ColorInfo
        $scripts = Get-ChildItem -Path "." -Filter "*.ps1" -Recurse | Where-Object { $_.Name -ne "validate_scripts.ps1" }
        
        Write-Host "[*] Encontrados $($scripts.Count) scripts" -ForegroundColor $ColorInfo
        Write-Host ""
        
        $totalPassed = 0
        $totalFailed = 0
        
        foreach ($script in $scripts) {
            Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor $ColorInfo
            Write-Host "Testando: $($script.FullName)" -ForegroundColor $ColorInfo
            Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor $ColorInfo
            
            $syntaxOK = Test-PowerShellSyntax -FilePath $script.FullName
            $practicesOK = Test-BestPractices -FilePath $script.FullName
            
            if ($syntaxOK -and $practicesOK) {
                Write-Host "[✓] $($script.Name) PASSOU em todos os testes" -ForegroundColor $ColorSuccess
                $totalPassed++
            } else {
                Write-Host "[!] $($script.Name) FALHOU em alguns testes" -ForegroundColor $ColorError
                $totalFailed++
            }
            Write-Host ""
        }
        
        # Resumo
        Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor $ColorInfo
        Write-Host "RESUMO DOS TESTES" -ForegroundColor $ColorInfo
        Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor $ColorInfo
        Write-Host "Total de scripts testados: $($scripts.Count)" -ForegroundColor $ColorInfo
        Write-Host "Passaram: $totalPassed" -ForegroundColor $ColorSuccess
        Write-Host "Falharam: $totalFailed" -ForegroundColor $(if ($totalFailed -eq 0) { $ColorSuccess } else { $ColorError })
        
        if ($totalFailed -eq 0) {
            Write-Host ""
            Write-Host "[✓] TODOS OS SCRIPTS ESTÃO VÁLIDOS!" -ForegroundColor $ColorSuccess
            exit 0
        } else {
            Write-Host ""
            Write-Host "[!] ALGUNS SCRIPTS PRECISAM DE CORREÇÃO" -ForegroundColor $ColorError
            exit 1
        }
        
    } else {
        # Testa apenas o script especificado
        if (Test-Path $Path) {
            $syntaxOK = Test-PowerShellSyntax -FilePath $Path
            $practicesOK = Test-BestPractices -FilePath $Path
            
            if ($syntaxOK -and $practicesOK) {
                Write-Host ""
                Write-Host "[✓] Script válido e segue boas práticas!" -ForegroundColor $ColorSuccess
                exit 0
            } else {
                Write-Host ""
                Write-Host "[!] Script precisa de correções" -ForegroundColor $ColorError
                exit 1
            }
        } else {
            Write-Host "[!] Script não encontrado: $Path" -ForegroundColor $ColorError
            exit 1
        }
    }
}

# Executa validação
Invoke-Validation -Path $ScriptPath
