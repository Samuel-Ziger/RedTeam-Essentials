<#
.SYNOPSIS
    Setup automatizado de uma estacao Windows para pentest/red team labs.

.DESCRIPTION
    Provisiona uma VM Windows limpa com as ferramentas e ajustes mais
    comuns para um operador de Red Team / pentester:

      * Configura ExecutionPolicy (Scope: CurrentUser) para RemoteSigned.
      * Habilita WSL2 (opcional) e Windows Terminal.
      * Instala Chocolatey + pacotes da lista padrao (Git, Python, Go,
        Sysinternals, Wireshark, Burp Community, etc.).
      * Cria a estrutura ~/Pentest com pastas padrao.
      * Aplica tweaks de qualidade-de-vida (file extensions, hidden files).
      * Suporta -DryRun, -SkipTools, -SkipFolders e -OnlyChoco.

    ATENCAO: Apenas em VMs de teste. Nao rode em maquinas de producao.

.PARAMETER DryRun       Apenas simula as acoes (nao instala nada).
.PARAMETER SkipTools    Pula instalacao de pacotes via Chocolatey.
.PARAMETER SkipFolders  Nao cria a estrutura de pastas.
.PARAMETER OnlyChoco    Apenas instala/atualiza Chocolatey e sai.
.PARAMETER ExtraPackages Lista adicional de pacotes Chocolatey.

.EXAMPLE
    ./windows_setup_clean.ps1 -DryRun

.EXAMPLE
    ./windows_setup_clean.ps1 -ExtraPackages ghidra,radare2

.NOTES
    Autor:    Samuel Ziger - RedTeam Essentials
    Versao:   2.0.0
    Licenca:  MIT
#>
[CmdletBinding()]
param(
    [switch]$DryRun,
    [switch]$SkipTools,
    [switch]$SkipFolders,
    [switch]$OnlyChoco,
    [string[]]$ExtraPackages = @()
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

Import-Module (Join-Path $PSScriptRoot "../lib/powershell/RTECommon.psm1") -Force
Write-RTEBanner -Title "Windows Clean Setup" -Version "2.0.0"

if (-not (Test-RTEAdmin)) {
    Write-RTELog -Level WARN -Message "Sem privilegios admin. Algumas etapas podem falhar."
    if (-not $DryRun) {
        Write-Host "Continuar mesmo assim? (s/N): " -ForegroundColor Yellow -NoNewline
        if ((Read-Host) -ne 's') { exit 1 }
    }
}

# --- Pacotes padrao via Chocolatey ------------------------------------------
$defaultPackages = @(
    # Core
    'git','python','nodejs-lts','golang','vscode','7zip','curl','wget',
    # Pentest / Recon
    'nmap','wireshark','burp-suite-free-edition','sysinternals','putty',
    'powertoys','windows-terminal',
    # Containers / virtualization
    'docker-desktop',
    # Crypto / forensics
    'openssl.light','hashcat','autopsy','ghidra'
)
$packages = $defaultPackages + $ExtraPackages

function Invoke-Step {
    param([string]$Name, [scriptblock]$Action)
    Write-RTELog -Level INFO -Message ">>> $Name"
    if ($DryRun) {
        Write-RTELog -Level WARN -Message "    [DRY-RUN] pulando."
        return
    }
    try   { & $Action; Write-RTELog -Level SUCCESS -Message "    OK." }
    catch { Write-RTELog -Level ERROR -Message ("    Falhou: {0}" -f $_.Exception.Message) }
}

# --- 1. PowerShell config ---------------------------------------------------
Invoke-Step -Name "ExecutionPolicy = RemoteSigned (CurrentUser)" -Action {
    Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser -Force
}

# --- 2. Chocolatey ----------------------------------------------------------
function Install-Chocolatey {
    if (Get-Command choco -ErrorAction SilentlyContinue) {
        Write-RTELog -Level INFO -Message "Chocolatey ja instalado: $((choco --version) 2>&1)"
        return
    }
    Write-RTELog -Level INFO -Message "Instalando Chocolatey..."
    Set-ExecutionPolicy Bypass -Scope Process -Force
    [System.Net.ServicePointManager]::SecurityProtocol =
        [System.Net.ServicePointManager]::SecurityProtocol -bor 3072
    Invoke-Expression ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
}

Invoke-Step -Name "Chocolatey" -Action { Install-Chocolatey }

if ($OnlyChoco) {
    Write-RTELog -Level SUCCESS -Message "OnlyChoco solicitado. Encerrando."
    exit 0
}

# --- 3. Pacotes -------------------------------------------------------------
if (-not $SkipTools) {
    Invoke-Step -Name ("Instalando pacotes: {0}" -f ($packages -join ', ')) -Action {
        choco install -y $packages --no-progress --limit-output
    }
}

# --- 4. Estrutura de pastas -------------------------------------------------
if (-not $SkipFolders) {
    Invoke-Step -Name "Estrutura ~/Pentest" -Action {
        $root = Join-Path $env:USERPROFILE 'Pentest'
        $dirs = 'Tools','Scripts','Wordlists','Exploits','Notes','Labs','Reports','Logs','Evidence'
        foreach ($d in $dirs) {
            $p = Join-Path $root $d
            if (-not (Test-Path $p)) { New-Item -ItemType Directory -Path $p -Force | Out-Null }
        }
    }
}

# --- 5. Tweaks de Explorer --------------------------------------------------
Invoke-Step -Name "Tweaks Explorer (extensions/hidden)" -Action {
    $key = 'HKCU:\Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced'
    Set-ItemProperty -Path $key -Name HideFileExt -Value 0 -Force
    Set-ItemProperty -Path $key -Name Hidden      -Value 1 -Force
}

Write-RTELog -Level SUCCESS -Message "Setup concluido. Reinicie o terminal para aplicar PATH."
