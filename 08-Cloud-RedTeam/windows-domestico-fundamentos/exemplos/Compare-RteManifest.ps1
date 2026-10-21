[CmdletBinding()]
param(
    [Parameter(Mandatory)]
    [ValidateScript({ Test-Path -LiteralPath $_ -PathType Leaf })]
    [string]$ManifestPath,

    [Parameter(Mandatory)]
    [ValidateScript({ Test-Path -LiteralPath $_ -PathType Container })]
    [string]$RestoredPath
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$manifestFile = (Resolve-Path -LiteralPath $ManifestPath).Path
$restoredRoot = (Resolve-Path -LiteralPath $RestoredPath).Path
$expectedFiles = @(Get-Content -LiteralPath $manifestFile -Raw |
    ConvertFrom-Json -ErrorAction Stop)

$expected = @{}
foreach ($entry in $expectedFiles) {
    $relativePath = [string]$entry.RelativePath
    if ([string]::IsNullOrWhiteSpace($relativePath) -or
        [System.IO.Path]::IsPathRooted($relativePath) -or
        $relativePath.Split([System.IO.Path]::DirectorySeparatorChar) -contains '..') {
        throw "Caminho relativo inválido no manifesto: $relativePath"
    }
    if ($expected.ContainsKey($relativePath)) {
        throw "Caminho duplicado no manifesto: $relativePath"
    }
    $expected[$relativePath] = [string]$entry.Sha256
}

$actual = @{}
Get-ChildItem -LiteralPath $restoredRoot -File -Recurse | ForEach-Object {
    if ($_.FullName -ne $manifestFile) {
        $relativePath = $_.FullName.Substring($restoredRoot.Length).TrimStart('\')
        $actual[$relativePath] = (Get-FileHash -LiteralPath $_.FullName -Algorithm SHA256).Hash
    }
}

$missing = @($expected.Keys | Where-Object { -not $actual.ContainsKey($_) } | Sort-Object)
$unexpected = @($actual.Keys | Where-Object { -not $expected.ContainsKey($_) } | Sort-Object)
$changed = @($expected.Keys | Where-Object {
    $actual.ContainsKey($_) -and $actual[$_] -ne $expected[$_]
} | Sort-Object)

$result = [pscustomobject][ordered]@{
    Schema = 'rte.windows.manifest-comparison/v1'
    Matches = $missing.Count -eq 0 -and $unexpected.Count -eq 0 -and $changed.Count -eq 0
    ExpectedFiles = $expected.Count
    ActualFiles = $actual.Count
    Missing = $missing
    Unexpected = $unexpected
    Changed = $changed
}

$result
if (-not $result.Matches) {
    throw 'A restauração diverge do manifesto; examine Missing, Unexpected e Changed.'
}
