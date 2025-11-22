# ================================================================
# Script: Windows Clean Setup
# Descrição: Configuração automatizada de ambiente Windows para pentest/labs
# Autor: RedTeam Essentials
# Versão: 1.0
# Data: 2025
# ================================================================

<#
.SYNOPSIS
    Automatiza configuração inicial de Windows para ambientes de pentest/lab

.DESCRIPTION
    Este script realiza configurações úteis para preparar uma máquina Windows
    para testes de segurança, desenvolvimento ou laboratórios:
    - Instala ferramentas essenciais
    - Configura PowerShell
    - Ajusta configurações do sistema
    - Organiza diretórios de trabalho
    
    ⚠️ Use apenas em máquinas de teste! Não em produção!

.PARAMETER SkipToolsInstall
    Pula a instalação de ferramentas

.PARAMETER CreateFolders
    Cria estrutura de pastas para pentest

.EXAMPLE
    .\windows_setup_clean.ps1
    
.EXAMPLE
    .\windows_setup_clean.ps1 -CreateFolders

.NOTES
    Requer privilégios administrativos para algumas configurações
#>

param(
    [Parameter(Mandatory=$false)]
    [switch]$SkipToolsInstall,
    
    [Parameter(Mandatory=$false)]
    [switch]$CreateFolders
)

# ================================================================
# VERIFICAÇÕES INICIAIS
# ================================================================

# Limpa tela
Clear-Host

# Banner
function Show-Banner {
    Write-Host ""
    Write-Host "╔═══════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
    Write-Host "║      Windows Clean Setup - RedTeam Essentials            ║" -ForegroundColor Cyan
    Write-Host "║      Configuração Automatizada v1.0                       ║" -ForegroundColor Cyan
    Write-Host "╚═══════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
    Write-Host ""
}

Show-Banner

# Verifica se está executando como administrador
function Test-Administrator {
    $currentUser = [Security.Principal.WindowsIdentity]::GetCurrent()
    $principal = New-Object Security.Principal.WindowsPrincipal($currentUser)
    return $principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
}

if (-not (Test-Administrator)) {
    Write-Host "[!] Este script requer privilégios administrativos para algumas funções" -ForegroundColor Yellow
    Write-Host "[*] Algumas configurações podem falhar sem admin" -ForegroundColor Yellow
    $continue = Read-Host "Deseja continuar assim mesmo? (S/N)"
    if ($continue -ne 'S') {
        exit 1
    }
}

# ================================================================
# CONFIGURAÇÕES DO POWERSHELL
# ================================================================

function Set-PowerShellConfig {
    Write-Host ""
    Write-Host "═══ Configurando PowerShell ═══" -ForegroundColor Cyan
    
    try {
        # Define política de execução para CurrentUser
        Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser -Force
        Write-Host "[+] ExecutionPolicy definida como RemoteSigned" -ForegroundColor Green
        
        # Habilita scripts
        Set-ItemProperty -Path "HKLM:\SOFTWARE\Microsoft\PowerShell\1\ShellIds\Microsoft.PowerShell" -Name "ExecutionPolicy" -Value "RemoteSigned" -ErrorAction SilentlyContinue
        Write-Host "[+] Scripts PowerShell habilitados" -ForegroundColor Green
        
    } catch {
        Write-Host "[!] Erro ao configurar PowerShell: $_" -ForegroundColor Red
    }
}

# ================================================================
# INSTALAÇÃO DE FERRAMENTAS
# ================================================================

function Install-ChocoAndTools {
    Write-Host ""
    Write-Host "═══ Instalando Ferramentas via Chocolatey ═══" -ForegroundColor Cyan
    
    # Verifica se Chocolatey está instalado
    if (-not (Get-Command choco -ErrorAction SilentlyContinue)) {
        Write-Host "[*] Chocolatey não encontrado. Instalando..." -ForegroundColor Yellow
        
        try {
            Set-ExecutionPolicy Bypass -Scope Process -Force
            [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072
            Invoke-Expression ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
            
            Write-Host "[+] Chocolatey instalado com sucesso!" -ForegroundColor Green
        } catch {
            Write-Host "[!] Erro ao instalar Chocolatey: $_" -ForegroundColor Red
            return
        }
    } else {
        Write-Host "[✓] Chocolatey já instalado" -ForegroundColor Green
    }
    
    # Lista de ferramentas úteis para pentest/dev
    $tools = @(
        "git",                    # Controle de versão
        "vscode",                 # Editor de código
        "python3",                # Python
        "wget",                   # Download de arquivos
        "curl",                   # Cliente HTTP
        "7zip",                   # Compactação
        "notepadplusplus",        # Editor de texto
        "sysinternals",           # Suite Sysinternals
        "wireshark"               # Análise de rede
    )
    
    Write-Host ""
    Write-Host "[*] Ferramentas que serão instaladas:" -ForegroundColor Cyan
    $tools | ForEach-Object { Write-Host "    - $_" -ForegroundColor Gray }
    Write-Host ""
    
    $confirm = Read-Host "Deseja prosseguir com a instalação? (S/N)"
    if ($confirm -eq 'S') {
        foreach ($tool in $tools) {
            Write-Host "[*] Instalando $tool..." -ForegroundColor Cyan
            choco install $tool -y --no-progress
        }
        Write-Host "[+] Instalação concluída!" -ForegroundColor Green
    } else {
        Write-Host "[*] Instalação de ferramentas pulada" -ForegroundColor Yellow
    }
}

# ================================================================
# CRIAÇÃO DE ESTRUTURA DE PASTAS
# ================================================================

function New-PentestFolders {
    Write-Host ""
    Write-Host "═══ Criando Estrutura de Pastas ═══" -ForegroundColor Cyan
    
    # Base path
    $basePath = "$env:USERPROFILE\Pentest"
    
    # Estrutura de pastas
    $folders = @(
        "$basePath\Tools",
        "$basePath\Scripts",
        "$basePath\Wordlists",
        "$basePath\Exploits",
        "$basePath\Notes",
        "$basePath\Labs",
        "$basePath\Reports",
        "$basePath\Logs"
    )
    
    foreach ($folder in $folders) {
        if (-not (Test-Path $folder)) {
            New-Item -ItemType Directory -Path $folder -Force | Out-Null
            Write-Host "[+] Criado: $folder" -ForegroundColor Green
        } else {
            Write-Host "[*] Já existe: $folder" -ForegroundColor Gray
        }
    }
    
    Write-Host ""
    Write-Host "[✓] Estrutura de pastas criada em: $basePath" -ForegroundColor Green
}

# ================================================================
# CONFIGURAÇÕES DO SISTEMA
# ================================================================

function Set-SystemConfig {
    Write-Host ""
    Write-Host "═══ Aplicando Configurações do Sistema ═══" -ForegroundColor Cyan
    
    try {
        # Mostrar extensões de arquivo
        Set-ItemProperty -Path "HKCU:\Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced" -Name "HideFileExt" -Value 0
        Write-Host "[+] Extensões de arquivo visíveis" -ForegroundColor Green
        
        # Mostrar arquivos ocultos
        Set-ItemProperty -Path "HKCU:\Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced" -Name "Hidden" -Value 1
        Write-Host "[+] Arquivos ocultos visíveis" -ForegroundColor Green
        
        # Desabilitar User Account Control para CurrentUser (apenas lab!)
        Write-Host "[!] UAC: Mantido habilitado (recomendado mesmo em labs)" -ForegroundColor Yellow
        
        Write-Host "[+] Configurações aplicadas!" -ForegroundColor Green
        
    } catch {
        Write-Host "[!] Erro ao aplicar configurações: $_" -ForegroundColor Red
    }
}

# ================================================================
# LIMPEZA E OTIMIZAÇÃO
# ================================================================

function Invoke-SystemCleanup {
    Write-Host ""
    Write-Host "═══ Limpeza do Sistema ═══" -ForegroundColor Cyan
    
    try {
        # Limpar arquivos temporários
        Write-Host "[*] Limpando arquivos temporários..." -ForegroundColor Cyan
        Remove-Item -Path "$env:TEMP\*" -Recurse -Force -ErrorAction SilentlyContinue
        Write-Host "[+] Temp limpo" -ForegroundColor Green
        
        # Limpar lixeira (requer confirmação)
        $confirm = Read-Host "Limpar lixeira? (S/N)"
        if ($confirm -eq 'S') {
            Clear-RecycleBin -Force -ErrorAction SilentlyContinue
            Write-Host "[+] Lixeira limpa" -ForegroundColor Green
        }
        
    } catch {
        Write-Host "[!] Erro durante limpeza: $_" -ForegroundColor Red
    }
}

# ================================================================
# RELATÓRIO FINAL
# ================================================================

function Show-Summary {
    Write-Host ""
    Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
    Write-Host "  CONFIGURAÇÃO CONCLUÍDA" -ForegroundColor Green
    Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Próximos passos:" -ForegroundColor Cyan
    Write-Host "1. Reinicie o PowerShell para aplicar mudanças" -ForegroundColor Gray
    Write-Host "2. Verifique se as ferramentas foram instaladas" -ForegroundColor Gray
    Write-Host "3. Configure seu ambiente de trabalho em: $env:USERPROFILE\Pentest" -ForegroundColor Gray
    Write-Host ""
    Write-Host "Ferramentas úteis instaladas:" -ForegroundColor Cyan
    Write-Host "  - Git: git --version" -ForegroundColor Gray
    Write-Host "  - Python: python --version" -ForegroundColor Gray
    Write-Host "  - VSCode: code ." -ForegroundColor Gray
    Write-Host ""
}

# ================================================================
# EXECUÇÃO PRINCIPAL
# ================================================================

Write-Host "[*] Iniciando configuração..." -ForegroundColor Cyan

# Configura PowerShell
Set-PowerShellConfig

# Instala ferramentas (se não pulado)
if (-not $SkipToolsInstall) {
    Install-ChocoAndTools
} else {
    Write-Host "[*] Instalação de ferramentas pulada" -ForegroundColor Yellow
}

# Cria pastas (se solicitado)
if ($CreateFolders) {
    New-PentestFolders
}

# Configurações do sistema
Set-SystemConfig

# Limpeza opcional
$cleanup = Read-Host "Executar limpeza do sistema? (S/N)"
if ($cleanup -eq 'S') {
    Invoke-SystemCleanup
}

# Resumo
Show-Summary

Write-Host "Script finalizado!" -ForegroundColor Green
Write-Host ""
