# Ferramentas offline

| Arquivo | Finalidade |
|---|---|
| `Compare-RteBaseline.ps1` | Compara settings desejados/observados sem corrigir |
| `Test-RteEnterpriseModel.ps1` | Valida identidades, grupos, owners e ciclos |
| `fixtures/*.json` | Dados empresariais totalmente sintéticos |
| `tests/WindowsEnterpriseAdvanced.Tests.ps1` | Testes Pester |

```powershell
.\Compare-RteBaseline.ps1 `
  -DesiredPath .\fixtures\desired-baseline.json `
  -ActualPath .\fixtures\actual-baseline.json

.\Test-RteEnterpriseModel.ps1 -Path .\fixtures\enterprise-model.json
Invoke-Pester .\tests
```

Os scripts não acessam domínio, tenant, rede, Registro ou serviços. Eles ensinam
contratos e validação antes de automação com autoridade real.

