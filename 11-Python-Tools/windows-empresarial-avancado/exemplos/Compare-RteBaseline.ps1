[CmdletBinding()]
param(
    [Parameter(Mandatory)]
    [ValidateScript({ Test-Path -LiteralPath $_ -PathType Leaf })]
    [string]$DesiredPath,

    [Parameter(Mandatory)]
    [ValidateScript({ Test-Path -LiteralPath $_ -PathType Leaf })]
    [string]$ActualPath
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$desired = Get-Content -LiteralPath $DesiredPath -Raw | ConvertFrom-Json
$actual = Get-Content -LiteralPath $ActualPath -Raw | ConvertFrom-Json

if ($desired.schema -ne 'rte.windows.baseline/v1' -or
    $actual.schema -ne 'rte.windows.observation/v1') {
    throw 'Schema de baseline ou observação desconhecido.'
}
if ($null -eq $desired.settings -or $null -eq $actual.settings) {
    throw 'Os documentos precisam declarar settings.'
}

foreach ($property in $desired.settings.PSObject.Properties | Sort-Object Name) {
    $observedProperty = $actual.settings.PSObject.Properties[$property.Name]
    if ($null -eq $observedProperty) {
        [pscustomobject][ordered]@{
            Setting = $property.Name
            Status = 'missing'
            Desired = $property.Value
            Actual = $null
        }
        continue
    }

    $desiredValue = $property.Value | ConvertTo-Json -Compress -Depth 10
    $actualValue = $observedProperty.Value | ConvertTo-Json -Compress -Depth 10
    $status = if ($desiredValue -ceq $actualValue) { 'compliant' } else { 'drift' }
    [pscustomobject][ordered]@{
        Setting = $property.Name
        Status = $status
        Desired = $property.Value
        Actual = $observedProperty.Value
    }
}

