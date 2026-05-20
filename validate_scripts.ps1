<#
.SYNOPSIS
    Validador de scripts do RedTeam-Essentials usando PSScriptAnalyzer.

.DESCRIPTION
    Executa:
      1. Parse sintatico via [System.Management.Automation.Language.Parser].
      2. Lint completo via PSScriptAnalyzer (instalado on-demand).
      3. Checagens custom (header .SYNOPSIS, disclaimer etico, etc.).

    Sai com codigo 0 se tudo passar, 1 se houver erros.

.PARAMETER Path        Script especifico (default: todos *.ps1/.psm1 do repo).
.PARAMETER Severity    Severidade minima do PSSA: Error|Warning|Information.
.PARAMETER NoCustom    Pula as checagens customizadas (lint puro).
.PARAMETER InstallDeps Forca (re)instalacao de PSScriptAnalyzer.

.EXAMPLE
    ./validate_scripts.ps1

.EXAMPLE
    ./validate_scripts.ps1 -Path ./01-Recon/dns_enum.ps1 -Severity Warning

.NOTES
    Autor:   Samuel Ziger - RedTeam Essentials
    Versao:  2.0.0
    Licenca: MIT
#>
[CmdletBinding()]
param(
    [string]$Path,
    [ValidateSet('Error','Warning','Information')][string]$Severity = 'Warning',
    [switch]$NoCustom,
    [switch]$InstallDeps
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

Import-Module (Join-Path $PSScriptRoot "lib/powershell/RTECommon.psm1") -Force
Write-RTEBanner -Title "Script Validator" -Version "2.0.0"

# --- 1. PSScriptAnalyzer ----------------------------------------------------
function Ensure-PSScriptAnalyzer {
    if ((Get-Module -ListAvailable PSScriptAnalyzer) -and -not $InstallDeps) {
        return
    }
    Write-RTELog -Level INFO -Message "Instalando PSScriptAnalyzer (CurrentUser)..."
    Install-Module PSScriptAnalyzer -Scope CurrentUser -Force -SkipPublisherCheck
}
Ensure-PSScriptAnalyzer
Import-Module PSScriptAnalyzer -Force

# --- 2. Coleta scripts ------------------------------------------------------
if ($Path) {
    if (-not (Test-Path $Path)) { Write-RTELog -Level FATAL -Message "Nao existe: $Path"; exit 1 }
    $scripts = @((Get-Item $Path))
} else {
    $scripts = Get-ChildItem -Path $PSScriptRoot -Recurse -Include *.ps1,*.psm1 |
        Where-Object { $_.FullName -notmatch '\\\.git\\' }
}
Write-RTELog -Level INFO -Message "Scripts a validar: $($scripts.Count)"

# --- 3. Funcoes auxiliares --------------------------------------------------
function Test-Syntax {
    param([string]$File)
    $errors = $null
    [System.Management.Automation.Language.Parser]::ParseFile($File, [ref]$null, [ref]$errors) | Out-Null
    if ($errors -and $errors.Count -gt 0) {
        foreach ($e in $errors) {
            Write-RTELog -Level ERROR -Message ("Sintaxe: L{0}: {1}" -f $e.Extent.StartLineNumber, $e.Message)
        }
        return $false
    }
    return $true
}

function Test-CustomRules {
    param([string]$File)
    $c = Get-Content -Path $File -Raw
    $issues = @()
    if ($c -notmatch '\.SYNOPSIS')                    { $issues += 'Falta .SYNOPSIS' }
    if ($c -notmatch '\.DESCRIPTION')                 { $issues += 'Falta .DESCRIPTION' }
    if ($c -notmatch 'IMPORTANTE|WARNING|AVISO|etico|ethical') {
        $issues += 'Falta disclaimer etico'
    }
    if ($c -notmatch 'Set-StrictMode')                { $issues += 'Falta Set-StrictMode' }
    return $issues
}

# --- 4. Execucao ------------------------------------------------------------
$total = $scripts.Count
$passed = 0; $failed = 0
$detailed = @()

foreach ($s in $scripts) {
    Write-Host ""
    Write-RTELog -Level INFO -Message ("=== {0}" -f $s.FullName)
    $ok = $true

    if (-not (Test-Syntax -File $s.FullName)) { $ok = $false }

    $pssa = Invoke-ScriptAnalyzer -Path $s.FullName -Severity $Severity -ErrorAction SilentlyContinue
    foreach ($issue in $pssa) {
        $lvl = if ($issue.Severity -eq 'Error') { 'ERROR' } else { 'WARN' }
        Write-RTELog -Level $lvl -Message ("PSSA {0}: L{1} {2}" -f $issue.RuleName, $issue.Line, $issue.Message)
        if ($issue.Severity -eq 'Error') { $ok = $false }
    }

    if (-not $NoCustom) {
        $custom = Test-CustomRules -File $s.FullName
        foreach ($c in $custom) {
            Write-RTELog -Level WARN -Message "Custom: $c"
        }
    }

    if ($ok) { Write-RTELog -Level SUCCESS -Message "OK"; $passed++ }
    else     { Write-RTELog -Level ERROR   -Message "FAIL"; $failed++ }

    $detailed += [pscustomobject]@{ file = $s.FullName; ok = $ok; pssaCount = $pssa.Count }
}

# --- 5. Resumo --------------------------------------------------------------
Write-Host ""
Write-Host ("Resumo: {0} passaram, {1} falharam de {2}." -f $passed, $failed, $total) -ForegroundColor Cyan
if ($failed -gt 0) { exit 1 } else { exit 0 }
