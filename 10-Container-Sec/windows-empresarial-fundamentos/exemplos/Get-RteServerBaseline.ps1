[CmdletBinding()]
param(
    [string]$OutputPath
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$os = Get-CimInstance Win32_OperatingSystem
$volumes = Get-Volume |
    Sort-Object DriveLetter |
    ForEach-Object {
        [ordered]@{
            DriveLetter = [string]$_.DriveLetter
            FileSystem = $_.FileSystem
            HealthStatus = [string]$_.HealthStatus
            SizeGiB = [math]::Round($_.Size / 1GB, 2)
            FreeGiB = [math]::Round($_.SizeRemaining / 1GB, 2)
        }
    }

$features = @()
$getWindowsFeature = Get-Command Get-WindowsFeature -ErrorAction SilentlyContinue
if ($getWindowsFeature) {
    $features = Get-WindowsFeature |
        Where-Object InstallState -eq Installed |
        Sort-Object Name |
        ForEach-Object { $_.Name }
}

$defender = [ordered]@{ Available = $false }
if (Get-Command Get-MpComputerStatus -ErrorAction SilentlyContinue) {
    $status = Get-MpComputerStatus
    $defender = [ordered]@{
        Available = $true
        AntivirusEnabled = [bool]$status.AntivirusEnabled
        RealTimeProtectionEnabled = [bool]$status.RealTimeProtectionEnabled
        SignatureLastUpdated = $status.AntivirusSignatureLastUpdated
    }
}

$baseline = [pscustomobject][ordered]@{
    Schema = 'rte.windows.server-baseline/v1'
    CollectedAtUtc = (Get-Date).ToUniversalTime().ToString('o')
    OperatingSystem = [ordered]@{
        Caption = $os.Caption
        Version = $os.Version
        Build = $os.BuildNumber
        Architecture = $os.OSArchitecture
    }
    InstalledFeatures = $features
    Volumes = $volumes
    ServiceSummary = Get-Service | Group-Object Status |
        Sort-Object Name |
        ForEach-Object { [ordered]@{ Status = $_.Name; Count = $_.Count } }
    Defender = $defender
}

if ($OutputPath) {
    $parent = Split-Path -Parent $OutputPath
    if ($parent -and -not (Test-Path -LiteralPath $parent)) {
        New-Item -ItemType Directory -Path $parent -Force | Out-Null
    }
    $baseline | ConvertTo-Json -Depth 8 |
        Set-Content -LiteralPath $OutputPath -Encoding UTF8
}

$baseline

