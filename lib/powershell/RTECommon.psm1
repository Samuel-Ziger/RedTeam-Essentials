<#
.SYNOPSIS
    RTECommon - Modulo de utilidades comuns para scripts do RedTeam-Essentials.

.DESCRIPTION
    Centraliza logging colorido com niveis, validacao de pre-requisitos,
    sanitizacao de input, suporte a -DryRun, escrita de relatorios e helpers
    de output JSON/CSV. Importe-o no topo de cada script com:

        Import-Module "$PSScriptRoot/../lib/powershell/RTECommon.psm1" -Force

.NOTES
    Autor:    Samuel Ziger - RedTeam Essentials
    Versao:   2.0.0
    Compat:   Windows PowerShell 5.1 e PowerShell Core 7+
    Licenca:  MIT
#>

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

# --- Niveis de log (RFC 5424 simplificado) -----------------------------------
$script:LogLevels = @{
    'DEBUG' = 0
    'INFO'  = 1
    'WARN'  = 2
    'ERROR' = 3
    'FATAL' = 4
}
$script:CurrentLevel = if ($env:RTE_LOG_LEVEL) { $env:RTE_LOG_LEVEL.ToUpper() } else { 'INFO' }
$script:LogFile      = $null

function Set-RTELogLevel {
    <#
    .SYNOPSIS Define o nivel minimo de log a ser exibido.
    .EXAMPLE  Set-RTELogLevel -Level DEBUG
    #>
    [CmdletBinding()]
    param(
        [ValidateSet('DEBUG','INFO','WARN','ERROR','FATAL')]
        [string]$Level = 'INFO'
    )
    $script:CurrentLevel = $Level
}

function Set-RTELogFile {
    <#
    .SYNOPSIS  Habilita persistencia dos logs em arquivo.
    .PARAMETER Path  Caminho do arquivo de log (sera criado se nao existir).
    #>
    [CmdletBinding()]
    param([Parameter(Mandatory)][string]$Path)

    $dir = Split-Path -Parent $Path
    if ($dir -and -not (Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
    }
    $script:LogFile = $Path
}

function Write-RTELog {
    <#
    .SYNOPSIS Logger central. Imprime colorido e opcionalmente persiste em arquivo.
    .EXAMPLE  Write-RTELog -Level INFO -Message "Iniciando scan"
    #>
    [CmdletBinding()]
    param(
        [ValidateSet('DEBUG','INFO','WARN','ERROR','FATAL','SUCCESS')]
        [string]$Level = 'INFO',
        [Parameter(Mandatory, Position = 0)][string]$Message
    )

    $effective = if ($Level -eq 'SUCCESS') { 'INFO' } else { $Level }
    if ($script:LogLevels[$effective] -lt $script:LogLevels[$script:CurrentLevel]) { return }

    $color = switch ($Level) {
        'DEBUG'   { 'DarkGray' }
        'INFO'    { 'Cyan' }
        'SUCCESS' { 'Green' }
        'WARN'    { 'Yellow' }
        'ERROR'   { 'Red' }
        'FATAL'   { 'Magenta' }
    }
    $glyph = switch ($Level) {
        'DEBUG'   { '[~]' }
        'INFO'    { '[*]' }
        'SUCCESS' { '[+]' }
        'WARN'    { '[!]' }
        'ERROR'   { '[x]' }
        'FATAL'   { '[X]' }
    }
    $stamp = (Get-Date).ToString('yyyy-MM-dd HH:mm:ss')
    $line  = "$stamp $glyph $Message"

    Write-Host $line -ForegroundColor $color
    if ($script:LogFile) {
        try { Add-Content -Path $script:LogFile -Value $line -ErrorAction Stop }
        catch { Write-Host "[!] Falha ao escrever no log file: $_" -ForegroundColor Yellow }
    }
}

function Write-RTEBanner {
    <#
    .SYNOPSIS  Imprime o cabecalho padrao do RedTeam Essentials.
    .PARAMETER Title    Titulo da ferramenta.
    .PARAMETER Version  Versao do script chamador.
    #>
    [CmdletBinding()]
    param(
        [Parameter(Mandatory)][string]$Title,
        [string]$Version = '2.0.0'
    )
    $bar = ('=' * 64)
    Write-Host ""
    Write-Host $bar -ForegroundColor Cyan
    Write-Host (" RedTeam Essentials :: {0,-40} v{1}" -f $Title, $Version) -ForegroundColor Cyan
    Write-Host $bar -ForegroundColor Cyan
    Write-Host " AVISO: Uso exclusivamente educacional/autorizado." -ForegroundColor Yellow
    Write-Host $bar -ForegroundColor Cyan
    Write-Host ""
}

function Test-RTEDomain {
    <#
    .SYNOPSIS Valida se a string e um FQDN bem formado.
    .EXAMPLE  if (-not (Test-RTEDomain $Domain)) { throw "invalido" }
    #>
    [CmdletBinding()]
    [OutputType([bool])]
    param([Parameter(Mandatory)][string]$Domain)
    return $Domain -match '^(?=.{1,253}$)([a-zA-Z0-9](?:[a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}$'
}

function Test-RTEIPv4 {
    <#
    .SYNOPSIS Valida string como IPv4.
    #>
    [CmdletBinding()]
    [OutputType([bool])]
    param([Parameter(Mandatory)][string]$Address)
    return [System.Net.IPAddress]::TryParse($Address, [ref]([System.Net.IPAddress]::None)) `
        -and ($Address -match '^\d{1,3}(\.\d{1,3}){3}$')
}

function Confirm-RTEAuthorization {
    <#
    .SYNOPSIS Confirma que o operador esta autorizado.
    .DESCRIPTION
        Bloqueia a execucao ate que o operador digite "AUTORIZADO". Pode ser
        desabilitado em pipelines com -Force ou variavel RTE_SKIP_AUTH=1.
    #>
    [CmdletBinding()]
    param([switch]$Force)
    if ($Force -or $env:RTE_SKIP_AUTH -eq '1') {
        Write-RTELog -Level WARN -Message "Confirmacao de autorizacao pulada (Force/env)."
        return
    }
    Write-Host ""
    Write-Host "Voce tem autorizacao por escrito para testar este alvo?" -ForegroundColor Yellow
    Write-Host "Digite AUTORIZADO para prosseguir (qualquer outra coisa aborta):" -ForegroundColor Yellow
    $answer = Read-Host
    if ($answer -ne 'AUTORIZADO') {
        Write-RTELog -Level FATAL -Message "Autorizacao nao confirmada. Abortando."
        exit 2
    }
    Write-RTELog -Level SUCCESS -Message "Autorizacao confirmada pelo operador."
}

function Test-RTEAdmin {
    <#
    .SYNOPSIS Retorna $true se o processo esta elevado (Windows) ou root (POSIX).
    #>
    [CmdletBinding()]
    [OutputType([bool])]
    param()
    if ($IsWindows -or $PSVersionTable.PSEdition -eq 'Desktop') {
        $id = [Security.Principal.WindowsIdentity]::GetCurrent()
        return ([Security.Principal.WindowsPrincipal]::new($id)).IsInRole(
            [Security.Principal.WindowsBuiltInRole]::Administrator)
    }
    # PowerShell Core em Linux/macOS
    try { return (id -u) -eq 0 } catch { return $false }
}

function Export-RTEResult {
    <#
    .SYNOPSIS Salva um objeto como JSON, CSV ou TXT padronizado.
    .PARAMETER Data     Objeto/lista a salvar.
    .PARAMETER Path     Diretorio destino (sera criado se necessario).
    .PARAMETER Name     Nome base do arquivo (sem extensao).
    .PARAMETER Format   json, csv ou txt.
    #>
    [CmdletBinding()]
    param(
        [Parameter(Mandatory)] $Data,
        [Parameter(Mandatory)][string]$Path,
        [Parameter(Mandatory)][string]$Name,
        [ValidateSet('json','csv','txt')][string]$Format = 'json'
    )
    if (-not (Test-Path $Path)) { New-Item -ItemType Directory -Path $Path -Force | Out-Null }
    $stamp = (Get-Date).ToString('yyyyMMdd_HHmmss')
    $file  = Join-Path $Path ("{0}_{1}.{2}" -f $Name, $stamp, $Format)

    switch ($Format) {
        'json' { $Data | ConvertTo-Json -Depth 8 | Out-File -FilePath $file -Encoding UTF8 -Force }
        'csv'  { $Data | Export-Csv -Path $file -NoTypeInformation -Encoding UTF8 -Force }
        'txt'  { $Data | Out-String | Out-File -FilePath $file -Encoding UTF8 -Force }
    }
    Write-RTELog -Level SUCCESS -Message "Resultado exportado: $file"
    return $file
}

function Invoke-RTEWithRetry {
    <#
    .SYNOPSIS Executa um scriptblock com retries e backoff exponencial.
    .EXAMPLE  Invoke-RTEWithRetry -ScriptBlock { Resolve-DnsName foo.com } -Retries 3
    #>
    [CmdletBinding()]
    param(
        [Parameter(Mandatory)][scriptblock]$ScriptBlock,
        [int]$Retries  = 3,
        [int]$BaseDelayMs = 250
    )
    for ($i = 1; $i -le $Retries; $i++) {
        try { return & $ScriptBlock }
        catch {
            if ($i -eq $Retries) { throw }
            $delay = $BaseDelayMs * [math]::Pow(2, $i - 1)
            Write-RTELog -Level WARN -Message ("Tentativa {0}/{1} falhou: {2}. Retry em {3}ms" -f $i, $Retries, $_.Exception.Message, $delay)
            Start-Sleep -Milliseconds $delay
        }
    }
}

Export-ModuleMember -Function `
    Set-RTELogLevel, Set-RTELogFile, Write-RTELog, Write-RTEBanner, `
    Test-RTEDomain, Test-RTEIPv4, Confirm-RTEAuthorization, `
    Test-RTEAdmin, Export-RTEResult, Invoke-RTEWithRetry
