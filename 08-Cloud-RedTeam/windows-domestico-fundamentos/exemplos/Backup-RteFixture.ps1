[CmdletBinding(SupportsShouldProcess, ConfirmImpact = 'Medium')]
param(
    [Parameter(Mandatory)]
    [ValidateScript({ Test-Path -LiteralPath $_ -PathType Container })]
    [string]$SourcePath,

    [Parameter(Mandatory)]
    [string]$DestinationPath
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$source = (Resolve-Path -LiteralPath $SourcePath).Path
$destination = [System.IO.Path]::GetFullPath($DestinationPath)

$sourceItem = Get-Item -LiteralPath $source -Force
if ($sourceItem.Attributes -band [System.IO.FileAttributes]::ReparsePoint) {
    throw 'A origem não pode ser um reparse point.'
}
$nestedReparsePoint = Get-ChildItem -LiteralPath $source -Force -Recurse |
    Where-Object { $_.Attributes -band [System.IO.FileAttributes]::ReparsePoint } |
    Select-Object -First 1
if ($nestedReparsePoint) {
    throw "A origem contém reparse point: $($nestedReparsePoint.FullName)"
}

if ($destination.StartsWith($source + [System.IO.Path]::DirectorySeparatorChar,
        [System.StringComparison]::OrdinalIgnoreCase)) {
    throw 'O destino não pode ficar dentro da origem.'
}
if (Test-Path -LiteralPath $destination) {
    throw 'O destino já existe; escolha um diretório novo.'
}

if ($PSCmdlet.ShouldProcess($destination, "Copiar fixture de $source")) {
    New-Item -ItemType Directory -Path $destination | Out-Null
    Get-ChildItem -LiteralPath $source -Force | ForEach-Object {
        Copy-Item -LiteralPath $_.FullName -Destination $destination -Recurse
    }

    $manifest = Get-ChildItem -LiteralPath $destination -File -Recurse |
        Sort-Object FullName |
        ForEach-Object {
            [pscustomobject]@{
                RelativePath = $_.FullName.Substring($destination.Length).TrimStart('\')
                Length = $_.Length
                Sha256 = (Get-FileHash -LiteralPath $_.FullName -Algorithm SHA256).Hash
            }
        }
    @($manifest) | ConvertTo-Json -Depth 4 |
        Set-Content -LiteralPath (Join-Path $destination 'manifest.json') -Encoding UTF8
    $manifest
}

