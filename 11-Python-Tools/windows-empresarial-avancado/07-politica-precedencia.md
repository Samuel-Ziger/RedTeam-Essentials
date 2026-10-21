# 07 — Política, autoridade e precedência

Configuração pode vir de default, local policy, domain GPO, MDM, application
control ou script. Resultado efetivo depende do CSP/setting, escopo e conflito;
não existe uma regra universal simples entre todos os mecanismos.

## Group Policy

No modelo clássico, Local → Site → Domain → OU compõe processamento, com
herança, link order, enforced, block inheritance, security filtering, WMI
filters e loopback. Isso descreve GPO, não toda política MDM.

```powershell
gpresult.exe /h C:\RTE-Lab\gpresult.html
Get-GPResultantSetOfPolicy -ReportType Xml -Path C:\RTE-Lab\rsop.xml
```

O segundo cmdlet exige GroupPolicy e contexto adequado. No lab sem domínio,
use `gpresult` para local policy e fixtures para calcular precedência.

## Governanção

Defina source of truth, setting ID, autoridade, valor, escopo, exceção,
evidência e owner. Drift pode ser conflito legítimo, falha de aplicação ou
mudança manual; diagnostique antes de forçar.

## Exercício

Resolva cinco cenários sintéticos de precedência e explique o resultado.

