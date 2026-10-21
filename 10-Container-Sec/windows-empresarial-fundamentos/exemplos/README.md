# Exemplos executáveis

| Arquivo | Finalidade |
|---|---|
| `Get-RteServerBaseline.ps1` | Baseline somente leitura e sanitizado |
| `Set-RteLocalState.ps1` | Convergência local aditiva com `-WhatIf` |
| `desired-state.example.json` | Manifesto de exemplo |
| `tests/WindowsEnterpriseFundamentals.Tests.ps1` | Pester offline |

```powershell
.\Get-RteServerBaseline.ps1 -OutputPath .\baseline.json
.\Set-RteLocalState.ps1 -ManifestPath .\desired-state.example.json -WhatIf
Invoke-Pester .\tests
```

O convergente cria somente diretórios declarados, nunca remove ou sobrescreve
conteúdo. Isso permite estudar estado desejado antes de recursos mais complexos.

