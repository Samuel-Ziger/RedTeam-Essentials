$examples = Split-Path -Parent $PSScriptRoot

Describe 'Windows empresarial I' {
    It 'cria diretório uma vez e depois permanece idempotente' {
        $target = Join-Path $TestDrive 'desired'
        $manifest = Join-Path $TestDrive 'state.json'
        @{
            schema = 'rte.windows.local-state/v1'
            directories = @(@{ path = $target })
        } | ConvertTo-Json -Depth 4 | Set-Content -LiteralPath $manifest

        $parameters = @{ ManifestPath = $manifest; Confirm = $false }
        $first = & (Join-Path $examples 'Set-RteLocalState.ps1') @parameters
        $second = & (Join-Path $examples 'Set-RteLocalState.ps1') @parameters

        $first.Changed | Should -BeTrue
        $second.Changed | Should -BeFalse
        $second.Exists | Should -BeTrue
    }

    It 'respeita WhatIf' {
        $target = Join-Path $TestDrive 'whatif'
        $manifest = Join-Path $TestDrive 'whatif.json'
        @{ schema = 'rte.windows.local-state/v1'; directories = @(@{ path = $target }) } |
            ConvertTo-Json -Depth 4 | Set-Content -LiteralPath $manifest

        $parameters = @{ ManifestPath = $manifest; WhatIf = $true }
        & (Join-Path $examples 'Set-RteLocalState.ps1') @parameters
        $target | Should -Not -Exist
    }

    It 'não coleta identificadores de rede ou hardware' {
        $content = Get-Content -LiteralPath (Join-Path $examples 'Get-RteServerBaseline.ps1') -Raw
        $content | Should -Not -Match 'SerialNumber|Win32_BIOS|Get-Net(IP|Adapter)|MacAddress'
    }
}
