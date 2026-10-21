# 06 — Roles, features e Component Store

Roles entregam funções de servidor; role services refinam; features apoiam. O
Component Store mantém payloads, manifests e capacidade de servicing.

```powershell
Get-WindowsFeature | Select-Object Name, InstallState, FeatureType
Get-WindowsOptionalFeature -Online |
  Where-Object State -eq Enabled |
  Select-Object FeatureName, State
dism.exe /Online /Cleanup-Image /AnalyzeComponentStore
```

## Mudança de feature

1. confirme suporte e dependências;
2. teste em clone;
3. exporte features atuais;
4. use `Install-WindowsFeature`/`Uninstall-WindowsFeature` com plano;
5. registre reinício requerido;
6. valide serviço, evento e workload;
7. remova payload somente se a estratégia de recuperação o permitir.

Instalar uma role não é configurar seu serviço. Algumas roles dependem
intrinsecamente de identidade/conectividade e serão praticadas após redes.

## Exercício

Em clone, instale uma feature local inofensiva, valide, remova e compare o
inventário. Não use roles que abram serviços de comunicação.

