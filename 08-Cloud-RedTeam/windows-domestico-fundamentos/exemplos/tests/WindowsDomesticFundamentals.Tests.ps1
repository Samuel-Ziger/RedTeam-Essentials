$examples = Split-Path -Parent $PSScriptRoot

Describe 'Windows doméstico I' {
    It 'mantém o inventário livre de identificadores desnecessários' {
        $content = Get-Content -LiteralPath (Join-Path $examples 'Get-RteLocalInventory.ps1') -Raw
        $content | Should -Not -Match 'Win32_BIOS.*SerialNumber'
        $content | Should -Not -Match 'Get-Net(IP|Adapter)'
        $content | Should -Not -Match '\$env:USERNAME'
        $content | Should -Match 'QueryStatus'
        $content | Should -Match 'rte\.windows\.local-inventory/v1'
    }

    It 'respeita WhatIf no backup' {
        $source = Join-Path $TestDrive 'source'
        $destination = Join-Path $TestDrive 'destination'
        New-Item -ItemType Directory -Path $source | Out-Null
        Set-Content -LiteralPath (Join-Path $source 'fixture.txt') -Value 'seguro'

        $parameters = @{
            SourcePath = $source
            DestinationPath = $destination
            WhatIf = $true
        }
        & (Join-Path $examples 'Backup-RteFixture.ps1') @parameters

        $destination | Should -Not -Exist
    }

    It 'copia a fixture e produz manifesto SHA-256' {
        $source = Join-Path $TestDrive 'source-real'
        $destination = Join-Path $TestDrive 'destination-real'
        New-Item -ItemType Directory -Path $source | Out-Null
        Set-Content -LiteralPath (Join-Path $source 'fixture.txt') -Value 'seguro'

        $parameters = @{
            SourcePath = $source
            DestinationPath = $destination
            Confirm = $false
        }
        & (Join-Path $examples 'Backup-RteFixture.ps1') @parameters

        (Join-Path $destination 'fixture.txt') | Should -Exist
        (Join-Path $destination 'manifest.json') | Should -Exist
    }

    It 'aprova uma árvore que corresponde ao manifesto' {
        $source = Join-Path $TestDrive 'compare-source'
        $destination = Join-Path $TestDrive 'compare-destination'
        New-Item -ItemType Directory -Path $source | Out-Null
        Set-Content -LiteralPath (Join-Path $source 'fixture.txt') -Value 'seguro'

        & (Join-Path $examples 'Backup-RteFixture.ps1') `
            -SourcePath $source -DestinationPath $destination -Confirm:$false
        $result = & (Join-Path $examples 'Compare-RteManifest.ps1') `
            -ManifestPath (Join-Path $destination 'manifest.json') `
            -RestoredPath $destination

        $result.Matches | Should -BeTrue
        $result.ExpectedFiles | Should -Be 1
    }

    It 'reprova conteúdo alterado depois do backup' {
        $source = Join-Path $TestDrive 'changed-source'
        $destination = Join-Path $TestDrive 'changed-destination'
        New-Item -ItemType Directory -Path $source | Out-Null
        Set-Content -LiteralPath (Join-Path $source 'fixture.txt') -Value 'original'

        & (Join-Path $examples 'Backup-RteFixture.ps1') `
            -SourcePath $source -DestinationPath $destination -Confirm:$false
        Set-Content -LiteralPath (Join-Path $destination 'fixture.txt') -Value 'alterado'

        {
            & (Join-Path $examples 'Compare-RteManifest.ps1') `
                -ManifestPath (Join-Path $destination 'manifest.json') `
                -RestoredPath $destination
        } | Should -Throw '*diverge do manifesto*'
    }

    It 'rejeita travessia de caminho no manifesto' {
        $restored = Join-Path $TestDrive 'restored-empty'
        $manifest = Join-Path $TestDrive 'unsafe-manifest.json'
        New-Item -ItemType Directory -Path $restored | Out-Null
        @([pscustomobject]@{ RelativePath = '..\escape.txt'; Sha256 = '00' }) |
            ConvertTo-Json | Set-Content -LiteralPath $manifest

        {
            & (Join-Path $examples 'Compare-RteManifest.ps1') `
                -ManifestPath $manifest -RestoredPath $restored
        } | Should -Throw '*Caminho relativo inválido*'
    }
}
