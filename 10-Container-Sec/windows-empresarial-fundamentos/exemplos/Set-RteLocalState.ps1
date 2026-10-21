[CmdletBinding(SupportsShouldProcess, ConfirmImpact = 'Medium')]
param(
    [Parameter(Mandatory)]
    [ValidateScript({ Test-Path -LiteralPath $_ -PathType Leaf })]
    [string]$ManifestPath
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$manifest = Get-Content -LiteralPath $ManifestPath -Raw | ConvertFrom-Json
if ($manifest.schema -ne 'rte.windows.local-state/v1') {
    throw 'Schema de manifesto desconhecido.'
}
if ($null -eq $manifest.directories) {
    throw 'Manifesto precisa declarar directories.'
}

$results = foreach ($entry in $manifest.directories) {
    $path = [string]$entry.path
    if (-not [System.IO.Path]::IsPathRooted($path)) {
        throw "O caminho precisa ser absoluto: $path"
    }

    $changed = $false
    if (-not (Test-Path -LiteralPath $path -PathType Container)) {
        if ($PSCmdlet.ShouldProcess($path, 'Criar diretório desejado')) {
            New-Item -ItemType Directory -Path $path | Out-Null
            $changed = $true
        }
    }
    [pscustomobject]@{
        Path = $path
        Changed = $changed
        Exists = [bool](Test-Path -LiteralPath $path -PathType Container)
    }
}

$results

