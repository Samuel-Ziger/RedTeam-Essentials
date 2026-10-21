# 03 — Instalação e Server Core

Server Core reduz componentes gráficos e superfície de servicing; Desktop
Experience atende workloads/ferramentas que exigem GUI. A escolha normalmente
é feita na instalação e não deve depender de preferência visual.

## Planejamento

1. valide hardware/virtualização e ISO;
2. separe sistema, dados, logs e backup conforme risco;
3. escolha idioma/edição/opção corretamente;
4. defina conta administrativa temporária protegida;
5. aplique baseline, update e inventário;
6. instale apenas roles necessárias;
7. capture imagem/snapshot de referência.

`SConfig` fornece tarefas locais em Server Core. PowerShell e ferramentas de
linha de comando devem ser o caminho principal; gerenciamento remoto será
retomado após redes.

```powershell
Get-ComputerInfo
Get-WindowsFeature | Where-Object InstallState -eq Installed
Get-Volume
```

## Exercício

Instale Core e Desktop Experience lado a lado, compare processos, uso de disco,
roles disponíveis, ciclo de update e operações que realmente exigem GUI.

