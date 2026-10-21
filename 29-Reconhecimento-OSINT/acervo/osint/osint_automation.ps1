<#
.SYNOPSIS
    Coleta OSINT basica e auditavel para dominios autorizados.

.DESCRIPTION
    Consulta DNS por resolver nativo ou dig, Certificate Transparency via
    crt.sh, WHOIS local quando disponivel e headers HTTP/HTTPS. A saida usa o
    contrato comum RTE e separa observacoes de candidatos inferidos.

.PARAMETER Domain
    Dominio alvo em formato FQDN.

.PARAMETER OutputDir
    Diretorio para o resultado JSON ou TXT.

.PARAMETER IncludeSubdomains
    Consulta nomes publicados em Certificate Transparency.

.PARAMETER DeepScan
    Inclui Certificate Transparency e WHOIS. Nao faz port scan ou fuzzing.

.PARAMETER DnsServer
    Resolver DNS opcional.

.PARAMETER Format
    Formato de saida: json ou txt.

.PARAMETER DryRun
    Valida a entrada e exibe o plano sem rede nem escrita.

.PARAMETER Force
    Pula a confirmacao interativa; use somente em automacao autorizada.

.EXAMPLE
    ./osint_automation.ps1 -Domain example.com -IncludeSubdomains

.EXAMPLE
    ./osint_automation.ps1 -Domain example.com -DeepScan -Format json -Force

.NOTES
    Autor: RedTeam Essentials
    Versao: 2.1.0
    Licenca: MIT
    AVISO: use somente fontes publicas dentro de um escopo autorizado.
#>
[CmdletBinding()]
param(
    [Parameter(Mandatory)][ValidateNotNullOrEmpty()][string]$Domain,
    [string]$OutputDir = './output',
    [switch]$IncludeSubdomains,
    [switch]$DeepScan,
    [string]$DnsServer,
    [ValidateSet('json', 'txt')][string]$Format = 'json',
    [switch]$DryRun,
    [switch]$Force
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$modulePath = Join-Path $PSScriptRoot '../../../lib/powershell/RTECommon.psm1'
Import-Module $modulePath -Force

function Resolve-OSINTRecord {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory)][string]$Name,
        [Parameter(Mandatory)][string]$Type,
        [string]$Server
    )

    if (Get-Command Resolve-DnsName -ErrorAction SilentlyContinue) {
        $parameters = @{ Name = $Name; Type = $Type; ErrorAction = 'Stop' }
        if ($Server) { $parameters.Server = $Server }
        return @(Resolve-DnsName @parameters | ForEach-Object {
            $value = switch ($Type) {
                'A' { $_.IPAddress }
                'AAAA' { $_.IPAddress }
                'MX' { $_.NameExchange }
                'NS' { $_.NameHost }
                'TXT' { $_.Strings -join ' ' }
                'SOA' { $_.PrimaryServer }
            }
            [pscustomobject]@{ type = $Type; value = $value }
        } | Where-Object { $_.value })
    }

    if (Get-Command dig -ErrorAction SilentlyContinue) {
        $digArgs = @('+short')
        if ($Server) { $digArgs += "@$Server" }
        $digArgs += @($Type, $Name)
        return @(& dig @digArgs 2>$null | Where-Object { $_ } | ForEach-Object {
            [pscustomobject]@{ type = $Type; value = $_.Trim() }
        })
    }

    if ($Type -in @('A', 'AAAA')) {
        $family = if ($Type -eq 'A') { 'InterNetwork' } else { 'InterNetworkV6' }
        return @([System.Net.Dns]::GetHostAddresses($Name) |
            Where-Object { $_.AddressFamily -eq $family } |
            ForEach-Object { [pscustomobject]@{ type = $Type; value = $_.IPAddressToString } })
    }

    Write-RTELog -Level WARN -Message "Sem resolver para registro $Type"
    return @()
}

function Get-OSINTCertificateNames {
    [CmdletBinding()]
    param([Parameter(Mandatory)][string]$TargetDomain)

    $url = "https://crt.sh/?q=%25.$TargetDomain&output=json"
    try {
        $response = Invoke-RTEWithRetry -Retries 3 -ScriptBlock {
            Invoke-RestMethod -Uri $url -TimeoutSec 30 -UserAgent 'RTE-OSINT/2.1'
        }
        return @($response |
            ForEach-Object { $_.name_value -split "`n" } |
            ForEach-Object { $_.Trim().TrimStart('*.').ToLowerInvariant() } |
            Where-Object { $_ -eq $TargetDomain -or $_ -like "*.$TargetDomain" } |
            Sort-Object -Unique)
    } catch {
        Write-RTELog -Level WARN -Message "crt.sh indisponivel: $($_.Exception.Message)"
        return @()
    }
}

function Get-OSINTWhois {
    [CmdletBinding()]
    param([Parameter(Mandatory)][string]$TargetDomain)

    if (-not (Get-Command whois -ErrorAction SilentlyContinue)) {
        return [pscustomobject]@{ available = $false; lines = @(); note = 'cliente whois ausente' }
    }
    $lines = @(& whois $TargetDomain 2>$null | Select-Object -First 100)
    return [pscustomobject]@{ available = $true; lines = $lines; note = 'saida limitada a 100 linhas' }
}

function Get-OSINTWebFingerprint {
    [CmdletBinding()]
    param([Parameter(Mandatory)][string]$TargetDomain)

    foreach ($scheme in @('https', 'http')) {
        $url = "${scheme}://$TargetDomain/"
        try {
            $response = Invoke-WebRequest -Uri $url -Method Head -TimeoutSec 10 -UseBasicParsing -ErrorAction Stop
            $headers = [ordered]@{}
            foreach ($name in @('Server', 'X-Powered-By', 'X-AspNet-Version', 'X-Generator')) {
                if ($response.Headers[$name]) { $headers[$name] = [string]$response.Headers[$name] }
            }
            return [pscustomobject]@{
                url = $url
                status = [int]$response.StatusCode
                headers = $headers
            }
        } catch {
            Write-RTELog -Level DEBUG -Message "HEAD $url falhou: $($_.Exception.Message)"
        }
    }
    return [pscustomobject]@{ url = $null; status = $null; headers = [ordered]@{} }
}

Write-RTEBanner -Title 'OSINT Automation' -Version '2.1.0'

$Domain = $Domain.Trim().TrimEnd('.').ToLowerInvariant()
if (-not (Test-RTEDomain $Domain)) {
    Write-RTELog -Level FATAL -Message "Dominio invalido: $Domain"
    exit 1
}

if ($DryRun) {
    Write-RTELog -Level WARN -Message '[DRY-RUN] Nenhuma consulta ou escrita sera realizada.'
    Write-RTELog -Level INFO -Message "Dominio: $Domain"
    Write-RTELog -Level INFO -Message 'DNS: A, AAAA, MX, NS, TXT, SOA'
    Write-RTELog -Level INFO -Message "CT: $($IncludeSubdomains -or $DeepScan); WHOIS: $DeepScan; Web HEAD: sim"
    exit 0
}

Confirm-RTEAuthorization -Force:$Force

$records = [ordered]@{}
foreach ($type in @('A', 'AAAA', 'MX', 'NS', 'TXT', 'SOA')) {
    try {
        $records[$type] = @(Resolve-OSINTRecord -Name $Domain -Type $type -Server $DnsServer)
    } catch {
        Write-RTELog -Level WARN -Message "DNS $type falhou: $($_.Exception.Message)"
        $records[$type] = @()
    }
}

$subdomains = if ($IncludeSubdomains -or $DeepScan) {
    @(Get-OSINTCertificateNames -TargetDomain $Domain)
} else { @() }

$whois = if ($DeepScan) {
    Get-OSINTWhois -TargetDomain $Domain
} else {
    [pscustomobject]@{ available = $false; lines = @(); note = 'use -DeepScan para coletar' }
}

$web = Get-OSINTWebFingerprint -TargetDomain $Domain
$emailCandidates = @('contact', 'security', 'support', 'abuse') | ForEach-Object { "$_@$Domain" }

$result = [ordered]@{
    metadata = [ordered]@{
        tool = 'osint_automation.ps1'
        version = '2.1.0'
        target = $Domain
        timestampUtc = [DateTime]::UtcNow.ToString('o')
        mode = if ($DeepScan) { 'deep-passive' } else { 'basic' }
    }
    observations = [ordered]@{
        dns = $records
        certificateTransparency = $subdomains
        whois = $whois
        web = $web
    }
    inferences = [ordered]@{
        emailCandidates = $emailCandidates
        warning = 'Candidatos nao foram verificados e nao devem ser tratados como pessoas ou contas reais.'
    }
    summary = [ordered]@{
        dnsRecords = ($records.Values | ForEach-Object { $_.Count } | Measure-Object -Sum).Sum
        certificateNames = $subdomains.Count
        webReachable = $null -ne $web.status
    }
}

$output = Export-RTEResult -Data $result -Path $OutputDir -Name "osint_$Domain" -Format $Format
Write-RTELog -Level SUCCESS -Message "Coleta concluida: $output"
