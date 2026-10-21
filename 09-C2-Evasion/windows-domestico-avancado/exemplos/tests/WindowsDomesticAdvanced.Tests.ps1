$examples = Split-Path -Parent $PSScriptRoot

Describe 'Windows doméstico II' {
    It 'interpreta um PE nativo sem alterar o arquivo' {
        $target = Join-Path $env:SystemRoot 'System32\notepad.exe'
        $before = (Get-FileHash -LiteralPath $target -Algorithm SHA256).Hash
        $result = & (Join-Path $examples 'Get-RtePeSummary.ps1') -Path $target
        $after = (Get-FileHash -LiteralPath $target -Algorithm SHA256).Hash

        $result.Format | Should -Match '^PE32\+?$'
        $result.SectionCount | Should -BeGreaterThan 0
        $result.SchemaVersion | Should -BeExactly 'rte.pe-summary/v1'
        $result.SizeOfImage | Should -BeGreaterThan 0
        $result.Sections.Count | Should -BeExactly $result.SectionCount
        $after | Should -BeExactly $before
    }

    It 'rejeita section table truncada antes de interpretar seções' {
        $target = Join-Path $env:SystemRoot 'System32\notepad.exe'
        $truncated = Join-Path $TestDrive 'truncated.exe'
        $bytes = [System.IO.File]::ReadAllBytes($target)
        $peOffset = [BitConverter]::ToInt32($bytes, 0x3C)
        $sectionCount = [BitConverter]::ToUInt16($bytes, $peOffset + 6)
        $optionalSize = [BitConverter]::ToUInt16($bytes, $peOffset + 20)
        $requiredEnd = $peOffset + 24 + $optionalSize + ($sectionCount * 40)
        [System.IO.File]::WriteAllBytes($truncated, $bytes[0..($requiredEnd - 2)])

        { & (Join-Path $examples 'Get-RtePeSummary.ps1') -Path $truncated } |
            Should -Throw
    }

    It 'impõe limite antes de ler o arquivo inteiro' {
        $target = Join-Path $env:SystemRoot 'System32\notepad.exe'
        $oversized = Join-Path $TestDrive 'oversized.exe'
        $source = [System.IO.File]::ReadAllBytes($target)
        $expanded = [byte[]]::new(1MB + 1)
        [Array]::Copy($source, $expanded, [Math]::Min($source.Length, $expanded.Length))
        [System.IO.File]::WriteAllBytes($oversized, $expanded)

        { & (Join-Path $examples 'Get-RtePeSummary.ps1') -Path $oversized `
                -MaximumFileSizeMiB 1 } | Should -Throw
    }

    It 'rejeita arquivo que não é PE' {
        $text = Join-Path $TestDrive 'texto.txt'
        Set-Content -LiteralPath $text -Value 'nao e PE'
        { & (Join-Path $examples 'Get-RtePeSummary.ps1') -Path $text } |
            Should -Throw
    }

    It 'carrega somente a DLL ao lado do consumidor' {
        $source = Get-Content -LiteralPath (Join-Path $examples 'dll\dll_consumer.c') -Raw
        $source | Should -Match 'GetModuleFileNameW'
        $source | Should -Match 'LoadLibraryExW'
        $source | Should -Match 'LOAD_LIBRARY_SEARCH_DLL_LOAD_DIR'
        $source | Should -Match 'unsupported_api_version'
        $source | Should -Not -Match '(OpenProcess|WriteProcessMemory|CreateRemoteThread)'
    }
}

