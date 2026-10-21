[CmdletBinding()]
param(
    [switch]$AsJson,
    [string]$OutputPath
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$operatingSystem = Get-CimInstance -ClassName Win32_OperatingSystem
$computerSystem = Get-CimInstance -ClassName Win32_ComputerSystem
$systemDrive = Get-Volume -DriveLetter ($env:SystemDrive.TrimEnd(':'))

$secureBoot = [ordered]@{
    QueryStatus = 'unknown'
    Enabled = $null
}
try {
    $secureBoot.QueryStatus = 'available'
    $secureBoot.Enabled = [bool](Confirm-SecureBootUEFI)
}
catch [System.UnauthorizedAccessException] {
    $secureBoot.QueryStatus = 'access-denied'
}
catch {
    $secureBoot.QueryStatus = 'unavailable'
}

$tpm = [ordered]@{
    QueryStatus = 'cmdlet-missing'
    Present = $null
    Ready = $null
}
if (Get-Command -Name Get-Tpm -ErrorAction SilentlyContinue) {
    try {
        $tpmStatus = Get-Tpm
        $tpm.QueryStatus = 'available'
        $tpm.Present = [bool]$tpmStatus.TpmPresent
        $tpm.Ready = [bool]$tpmStatus.TpmReady
    }
    catch [System.UnauthorizedAccessException] {
        $tpm.QueryStatus = 'access-denied'
    }
    catch {
        $tpm.QueryStatus = 'unavailable'
    }
}

$defender = [ordered]@{
    QueryStatus = 'cmdlet-missing'
    AntivirusEnabled = $null
    RealTimeProtectionEnabled = $null
    SignatureLastUpdated = $null
}
if (Get-Command -Name Get-MpComputerStatus -ErrorAction SilentlyContinue) {
    try {
        $status = Get-MpComputerStatus
        $defender.QueryStatus = 'available'
        $defender.AntivirusEnabled = [bool]$status.AntivirusEnabled
        $defender.RealTimeProtectionEnabled = [bool]$status.RealTimeProtectionEnabled
        $defender.SignatureLastUpdated = $status.AntivirusSignatureLastUpdated
    }
    catch [System.UnauthorizedAccessException] {
        $defender.QueryStatus = 'access-denied'
    }
    catch {
        $defender.QueryStatus = 'unavailable'
    }
}

$inventory = [pscustomobject][ordered]@{
    Schema = 'rte.windows.local-inventory/v1'
    CollectedAtUtc = (Get-Date).ToUniversalTime().ToString('o')
    OperatingSystem = [ordered]@{
        Caption = $operatingSystem.Caption
        Version = $operatingSystem.Version
        Build = $operatingSystem.BuildNumber
        Architecture = $operatingSystem.OSArchitecture
    }
    Hardware = [ordered]@{
        LogicalProcessors = [int]$computerSystem.NumberOfLogicalProcessors
        MemoryGiB = [math]::Round($computerSystem.TotalPhysicalMemory / 1GB, 2)
        SecureBoot = $secureBoot
        Tpm = $tpm
    }
    SystemVolume = [ordered]@{
        FileSystem = $systemDrive.FileSystem
        HealthStatus = [string]$systemDrive.HealthStatus
        SizeGiB = [math]::Round($systemDrive.Size / 1GB, 2)
        FreeGiB = [math]::Round($systemDrive.SizeRemaining / 1GB, 2)
    }
    Defender = $defender
}

if ($AsJson -or $OutputPath) {
    $json = $inventory | ConvertTo-Json -Depth 6
    if ($OutputPath) {
        $parent = Split-Path -Parent $OutputPath
        if ($parent -and -not (Test-Path -LiteralPath $parent)) {
            New-Item -ItemType Directory -Path $parent -Force | Out-Null
        }
        $json | Set-Content -LiteralPath $OutputPath -Encoding UTF8
    }
    if ($AsJson) {
        $json
    }
}
else {
    $inventory
}
