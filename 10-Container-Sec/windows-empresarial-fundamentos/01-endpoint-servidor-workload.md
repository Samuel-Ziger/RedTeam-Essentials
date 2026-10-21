# 01 — Endpoint, servidor, role e workload

Endpoint atende uma pessoa/dispositivo. Servidor hospeda capacidades para uma
organização. Role é função do Windows Server; feature apoia roles. Workload é
o serviço de negócio completo, que pode combinar SO, aplicação, dados e pessoas.

## Decisões

Antes de instalar pergunte:

- qual resultado de negócio e owner?
- quais dados, criticidade, RPO e RTO?
- qual edição e direito de virtualização?
- GUI é realmente necessária?
- como atualizar, observar, fazer backup e aposentar?
- qual dependência será tratada somente após redes?

Servidor não deve acumular roles por conveniência. Separar workloads reduz
blast radius e facilita servicing, capacidade e ownership.

## Inventário

```powershell
Get-ComputerInfo | Select-Object WindowsProductName, OsVersion, OsBuildNumber
Get-WindowsFeature | Where-Object InstallState -eq Installed |
  Select-Object Name, DisplayName, FeatureType
```

## Exercício

Modele três servidores standalone fictícios por workload, sem conectividade.
Justifique edição, instalação, armazenamento, proteção e recuperação.

