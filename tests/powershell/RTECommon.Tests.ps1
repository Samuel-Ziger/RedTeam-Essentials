$ModulePath = Join-Path $PSScriptRoot '../../lib/powershell/RTECommon.psm1'
Import-Module $ModulePath -Force

Describe 'RTECommon validations' {
    It 'accepts valid domains' {
        Test-RTEDomain 'api.example.com' | Should -BeTrue
    }

    It 'rejects invalid domains' {
        Test-RTEDomain 'localhost' | Should -BeFalse
        Test-RTEDomain '-bad.example.com' | Should -BeFalse
    }

    It 'accepts and rejects IPv4 values correctly' {
        Test-RTEIPv4 '127.0.0.1' | Should -BeTrue
        Test-RTEIPv4 '256.1.1.1' | Should -BeFalse
        Test-RTEIPv4 '1.2.3' | Should -BeFalse
    }
}

Describe 'RTECommon export' {
    It 'exports valid JSON to a new directory' {
        $dir = Join-Path $TestDrive 'nested'
        $path = Export-RTEResult -Data @{ ok = $true } -Path $dir -Name result -Format json
        Test-Path $path | Should -BeTrue
        (Get-Content $path -Raw | ConvertFrom-Json).ok | Should -BeTrue
    }
}

