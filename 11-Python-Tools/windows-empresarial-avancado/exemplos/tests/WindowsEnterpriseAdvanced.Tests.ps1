$examples = Split-Path -Parent $PSScriptRoot
$fixtures = Join-Path $examples 'fixtures'

Describe 'Windows empresarial II' {
    It 'classifica compliant, drift e missing' {
        $parameters = @{
            DesiredPath = Join-Path $fixtures 'desired-baseline.json'
            ActualPath = Join-Path $fixtures 'actual-baseline.json'
        }
        $result = & (Join-Path $examples 'Compare-RteBaseline.ps1') @parameters

        ($result | Where-Object Status -eq 'compliant').Count | Should -Be 2
        ($result | Where-Object Status -eq 'drift').Count | Should -Be 1
        ($result | Where-Object Status -eq 'missing').Count | Should -Be 1
    }

    It 'aceita o modelo empresarial válido' {
        $path = Join-Path $fixtures 'enterprise-model.json'
        $result = & (Join-Path $examples 'Test-RteEnterpriseModel.ps1') -Path $path
        $result.Valid | Should -BeTrue
        $result.Errors.Count | Should -Be 0
    }

    It 'detecta ciclo e membro desconhecido' {
        $path = Join-Path $TestDrive 'invalid-model.json'
        @{
            schema = 'rte.windows.enterprise-model/v1'
            identities = @()
            groups = @(
                @{ id = 'group.a'; owner = 'owner'; members = @('group.b') },
                @{ id = 'group.b'; owner = 'owner'; members = @('group.a', 'ghost') }
            )
            permissions = @()
        } | ConvertTo-Json -Depth 6 | Set-Content -LiteralPath $path

        $result = & (Join-Path $examples 'Test-RteEnterpriseModel.ps1') -Path $path
        $result.Valid | Should -BeFalse
        ($result.Errors -join "`n") | Should -Match 'ciclo de grupos'
        ($result.Errors -join "`n") | Should -Match 'membro desconhecido'
    }
}
