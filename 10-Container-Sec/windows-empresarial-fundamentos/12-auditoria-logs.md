# 12 — Auditoria e logs

Auditoria define quais eventos de segurança registrar; observabilidade combina
eventos, métricas, traces e health checks. Registrar tudo sem retenção e uso
produz custo e ruído.

## Projeto

Para cada evento desejado declare pergunta, provider/channel/ID, campos,
volume esperado, retenção, acesso, alerta, teste e owner. Event IDs só têm
sentido com provider e versão.

```powershell
auditpol.exe /get /category:*
Get-WinEvent -ListLog Security,System,Application |
  Select-Object LogName, IsEnabled, MaximumSizeInBytes, RecordCount
wevtutil.exe gli System
```

Security log exige privilégio apropriado. Exporte apenas intervalo/campos
necessários e proteja EVTX, pois pode conter nomes, caminhos e atividade.

## Validação

Uma política não está pronta até um evento benigno conhecido produzir o sinal
esperado e a consulta recuperá-lo. Falha de logging também deve ser monitorada.

## Exercício

Crie uma tarefa fixture, execute-a, encontre seus eventos e produza uma linha
do tempo UTC de no máximo 20 registros.

