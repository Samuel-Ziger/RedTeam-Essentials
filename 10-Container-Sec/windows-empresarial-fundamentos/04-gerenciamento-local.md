# 04 — Gerenciamento local

Server Manager agrega inventário/roles na experiência gráfica. MMC hospeda
snap-ins. SConfig, PowerShell, DISM e comandos específicos funcionam em Core.
Windows Admin Center será apenas reconhecido aqui; uso remoto depende de redes.

## Escolha de interface

- tarefa única exploratória: GUI pode ajudar;
- operação repetível: PowerShell com teste e log;
- servicing de imagem: DISM/PowerShell offline;
- diagnóstico: evento, counter, trace e ferramenta especializada;
- emergência: runbook testado, não improviso.

```powershell
Get-WindowsFeature
Get-Service
Get-ScheduledTask
Get-WinEvent -LogName System -MaxEvents 20
```

## Controle de mudança

Um comando elevado deve declarar alvo, motivo, impacto, owner, janela,
validação e rollback. Capture `Get-History` apenas como apoio: segredos em
comando podem persistir no history e nunca devem ser passados em texto claro.

## Exercício

Realize a mesma consulta de roles por Server Manager e PowerShell. Exporte JSON
ordenado e compare reprodutibilidade.

