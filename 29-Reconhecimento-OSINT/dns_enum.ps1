<#
.SYNOPSIS
    Enumeracao DNS passiva e segura para fins educacionais.

.DESCRIPTION
    Coleta registros DNS (A, AAAA, MX, NS, TXT, SOA, CNAME, SRV) de um dominio
    e, opcionalmente, enumera subdominios usando Certificate Transparency Logs
    (crt.sh). Suporta exportacao em JSON/TXT, dry-run, retries e logging
    estruturado via modulo RTECommon.

    Compatibilidade: Windows PowerShell 5.1 e PowerShell 7+ (Linux/macOS).
    O coletor de subdominios usa Invoke-RestMethod e nao depende de
    Resolve-DnsName (que e Windows-only), tornando-o util em Kali tambem.

.PARAMETER Domain
    Dominio alvo (FQDN). Ex.: exemplo.com

.PARAMETER OutputDir
    Diretorio de saida (default: ./output).

.PARAMETER IncludeSubdomains
    Enumera subdominios via crt.sh (Certificate Transparency).

.PARAMETER RecordTypes
    Lista de tipos a consultar. Default: A,AAAA,MX,NS,TXT,SOA,CNAME,SRV.

.PARAMETER Format
    Formato de saida: json (default) ou txt.

.PARAMETER DnsServer
    Servidor DNS a utilizar (default: resolver do sistema).

.PARAMETER DryRun
    Apenas mostra o que seria feito, sem fazer queries reais.

.EXAMPLE
    ./dns_enum.ps1 -Domain exemplo.com -IncludeSubdomains -Format json

.EXAMPLE
    ./dns_enum.ps1 -Domain exemplo.com -RecordTypes A,MX,TXT -DnsServer 1.1.1.1

.NOTES
    Autor:    Samuel Ziger - RedTeam Essentials
    Versao:   2.0.0
    Licenca:  MIT
    Etico:    Apenas em alvos autorizados. Dados consultados sao publicos.
#>
[CmdletBinding()]
param(
    [Parameter(Mandatory, HelpMessage = "Dominio a enumerar (ex: exemplo.com)")]
    [ValidateNotNullOrEmpty()]
    [string]$Domain,

    [string]$OutputDir = "./output",

    [switch]$IncludeSubdomains,

    [ValidateSet('A','AAAA','MX','NS','TXT','SOA','CNAME','SRV')]
    [string[]]$RecordTypes = @('A','AAAA','MX','NS','TXT','SOA','CNAME','SRV'),

    [ValidateSet('json','txt')]
    [string]$Format = 'json',

    [string]$DnsServer,

    [switch]$DryRun
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

# --- Carrega modulo comum ----------------------------------------------------
$modulePath = Join-Path $PSScriptRoot "../lib/powershell/RTECommon.psm1"
if (-not (Test-Path $modulePath)) {
    Write-Error "Modulo RTECommon nao encontrado em $modulePath"
    exit 1
}
Import-Module $modulePath -Force

Write-RTEBanner -Title "DNS Enumeration" -Version "2.0.0"

if (-not (Test-RTEDomain $Domain)) {
    Write-RTELog -Level FATAL -Message "Dominio invalido: $Domain"
    exit 1
}

if ($DryRun) {
    Write-RTELog -Level WARN -Message "[DRY-RUN] Nenhuma query real sera executada."
    Write-RTELog -Level INFO -Message "Alvo: $Domain"
    Write-RTELog -Level INFO -Message "Tipos: $($RecordTypes -join ', ')"
    if ($IncludeSubdomains) { Write-RTELog -Level INFO -Message "Subdominios: SIM (crt.sh)" }
    exit 0
}

# --- Helpers DNS cross-platform ---------------------------------------------
function Resolve-RTERecord {
    param([string]$Name, [string]$Type)

    # Prefere Resolve-DnsName (Windows) por ser mais rico.
    if (Get-Command Resolve-DnsName -ErrorAction SilentlyContinue) {
        $params = @{ Name = $Name; Type = $Type; ErrorAction = 'Stop' }
        if ($DnsServer) { $params.Server = $DnsServer }
        return Invoke-RTEWithRetry -ScriptBlock { Resolve-DnsName @params } -Retries 3
    }

    # Fallback POSIX: dig
    if (Get-Command dig -ErrorAction SilentlyContinue) {
        $serverArg = if ($DnsServer) { "@$DnsServer" } else { "" }
        $raw = & dig +short $serverArg $Type $Name 2>$null
        return ($raw | Where-Object { $_ -ne '' } | ForEach-Object {
            [pscustomobject]@{ Type = $Type; Data = $_ }
        })
    }

    # Fallback puro .NET para A/AAAA
    if ($Type -in 'A','AAAA') {
        try {
            return [System.Net.Dns]::GetHostAddresses($Name) |
                Where-Object {
                    ($Type -eq 'A'    -and $_.AddressFamily -eq 'InterNetwork') -or
                    ($Type -eq 'AAAA' -and $_.AddressFamily -eq 'InterNetworkV6')
                } | ForEach-Object {
                    [pscustomobject]@{ Type = $Type; Data = $_.IPAddressToString }
                }
        } catch { return @() }
    }

    Write-RTELog -Level WARN -Message "Nenhum resolver disponivel para tipo $Type"
    return @()
}

function Get-RTESubdomains {
    param([string]$Domain)
    Write-RTELog -Level INFO -Message "Consultando crt.sh para subdominios de $Domain ..."
    try {
        $url = "https://crt.sh/?q=%25.$Domain&output=json"
        $resp = Invoke-RTEWithRetry -ScriptBlock {
            Invoke-RestMethod -Uri $url -TimeoutSec 30 -UserAgent "RTE-DNS-Enum/2.0"
        } -Retries 3
        $names = $resp |
            ForEach-Object { $_.name_value -split "`n" } |
            ForEach-Object { $_.Trim().TrimStart('*.').ToLower() } |
            Where-Object { $_ -and $_ -like "*.$Domain" } |
            Sort-Object -Unique
        Write-RTELog -Level SUCCESS -Message ("Subdominios unicos encontrados: {0}" -f $names.Count)
        return $names
    } catch {
        Write-RTELog -Level ERROR -Message "Falha ao consultar crt.sh: $($_.Exception.Message)"
        return @()
    }
}

# --- Coleta principal --------------------------------------------------------
$result = [ordered]@{
    metadata = [ordered]@{
        tool       = "RTE dns_enum.ps1"
        version    = "2.0.0"
        target     = $Domain
        timestamp  = (Get-Date).ToString('o')
        dnsServer  = if ($DnsServer) { $DnsServer } else { 'system-default' }
        operator   = if ($env:USERNAME) { $env:USERNAME } else { $env:USER }
    }
    records     = [ordered]@{}
    subdomains  = @()
    summary     = [ordered]@{}
}

foreach ($type in $RecordTypes) {
    Write-RTELog -Level INFO -Message "Consultando registros $type ..."
    try {
        $records = Resolve-RTERecord -Name $Domain -Type $type
        $parsed  = @()
        foreach ($r in @($records)) {
            $row = [ordered]@{ type = $type }
            # Helper inline para coalescer (compat PS 5.1)
            $coalesce = { param($a, $b) if ($null -ne $a -and $a -ne '') { $a } else { $b } }
            switch ($type) {
                'A'     { $row.value = & $coalesce $r.IPAddress $r.Data }
                'AAAA'  { $row.value = & $coalesce $r.IPAddress $r.Data }
                'MX'    {
                    $row.value      = & $coalesce $r.NameExchange $r.Data
                    $row.preference = $r.Preference
                }
                'NS'    { $row.value = & $coalesce $r.NameHost $r.Data }
                'TXT'   {
                    $joined = if ($r.Strings) { $r.Strings -join ' ' } else { $null }
                    $row.value = & $coalesce $joined $r.Data
                }
                'SOA'   {
                    $row.primary = $r.PrimaryServer
                    $row.admin   = $r.Administrator
                    $row.serial  = $r.SerialNumber
                }
                'CNAME' { $row.value = & $coalesce $r.NameHost $r.Data }
                'SRV'   {
                    $row.target   = $r.NameTarget
                    $row.port     = $r.Port
                    $row.priority = $r.Priority
                    $row.weight   = $r.Weight
                }
            }
            $parsed += [pscustomobject]$row
            Write-RTELog -Level SUCCESS -Message ("{0,-5} {1}" -f $type, ($row.Values -join ' | '))
        }
        $result.records[$type] = $parsed
    } catch {
        Write-RTELog -Level WARN -Message ("Sem resposta para {0}: {1}" -f $type, $_.Exception.Message)
        $result.records[$type] = @()
    }
}

if ($IncludeSubdomains) {
    $result.subdomains = Get-RTESubdomains -Domain $Domain
}

# --- Resumo ------------------------------------------------------------------
$result.summary = [ordered]@{
    totalRecords     = ($result.records.Values | ForEach-Object { $_.Count } | Measure-Object -Sum).Sum
    subdomainCount   = $result.subdomains.Count
    typesQueried     = $RecordTypes
}

$file = Export-RTEResult -Data $result -Path $OutputDir -Name "dns_enum_$Domain" -Format $Format
Write-RTELog -Level SUCCESS -Message "Enumeracao finalizada. Arquivo: $file"
