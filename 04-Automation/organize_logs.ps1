# ================================================================
# Script: Organize Logs
# Descrição: Organizador de logs de pentests e CTFs
# Autor: RedTeam Essentials
# Versão: 1.0
# ================================================================

<#
.SYNOPSIS
    Organiza logs e evidências de testes de penetração

.DESCRIPTION
    Este script ajuda a organizar logs, screenshots e evidências
    de pentests e CTFs de forma estruturada.

.PARAMETER SourcePath
    Pasta contendo arquivos desorganizados

.PARAMETER TargetName
    Nome do projeto/alvo

.EXAMPLE
    .\organize_logs.ps1 -SourcePath "C:\Temp\Downloads" -TargetName "HackTheBox_Forest"
#>

param(
    [Parameter(Mandatory=$true)]
    [string]$SourcePath,
    
    [Parameter(Mandatory=$true)]
    [string]$TargetName
)

Clear-Host

Write-Host "╔═══════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║      Log Organizer - RedTeam Essentials                  ║" -ForegroundColor Cyan
Write-Host "╚═══════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# Criar estrutura
$basePath = "$env:USERPROFILE\Pentest\Labs\$TargetName"
$folders = @(
    "$basePath\Screenshots",
    "$basePath\Scans",
    "$basePath\Exploits",
    "$basePath\Loot",
    "$basePath\Notes"
)

Write-Host "[*] Criando estrutura em: $basePath" -ForegroundColor Cyan

foreach ($folder in $folders) {
    New-Item -ItemType Directory -Path $folder -Force | Out-Null
    Write-Host "[+] $folder" -ForegroundColor Green
}

# Organizar arquivos por extensão
if (Test-Path $SourcePath) {
    $files = Get-ChildItem -Path $SourcePath -File
    
    foreach ($file in $files) {
        switch -Regex ($file.Extension) {
            '\.(png|jpg|jpeg|gif|bmp)$' {
                Move-Item $file.FullName "$basePath\Screenshots\" -Force
            }
            '\.(xml|nmap|gnmap)$' {
                Move-Item $file.FullName "$basePath\Scans\" -Force
            }
            '\.(py|sh|ps1|c|cpp|exe)$' {
                Move-Item $file.FullName "$basePath\Exploits\" -Force
            }
            '\.(txt|md|doc|docx|pdf)$' {
                Move-Item $file.FullName "$basePath\Notes\" -Force
            }
            default {
                Move-Item $file.FullName "$basePath\Loot\" -Force
            }
        }
    }
    
    Write-Host ""
    Write-Host "[✓] Arquivos organizados!" -ForegroundColor Green
} else {
    Write-Host "[!] Caminho de origem não encontrado" -ForegroundColor Red
}

Write-Host ""
Write-Host "Projeto organizado em: $basePath" -ForegroundColor Cyan
