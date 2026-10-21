# 14 — Atualização, servicing e reinício

Servidor atualizado ainda pode falhar por incompatibilidade; servidor não
atualizado acumula risco. O processo precisa de inventário, anéis, teste,
janela, backup, reinício, health checks e rollback suportado.

## Classifique

- security/quality cumulative update;
- servicing stack e componentes;
- .NET cumulative update;
- driver/firmware;
- feature/versão do SO;
- intelligence/plataforma do Defender.

```powershell
Get-HotFix | Sort-Object InstalledOn -Descending
Get-WindowsPackage -Online | Where-Object PackageState -eq Installed
dism.exe /Online /Cleanup-Image /ScanHealth
```

Hotpatch reduz reinícios em cenários/licenças suportados, mas não elimina
servicing tradicional. Confirme requisitos atuais; não prometa zero downtime.

## Runbook

Prechecks → backup/checkpoint adequado → drain local do workload → aplicar →
reiniciar → validar SO/role/app/dados → observar → encerrar ou reverter.

## Exercício

Crie plano de patch do lab com critérios mensuráveis e simule rollback de uma
feature em snapshot. Não desinstale KB de segurança do host real.

