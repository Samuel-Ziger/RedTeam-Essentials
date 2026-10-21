# 11 — Serviços, tarefas e operações recorrentes

Serviço de produção precisa de conta, dependências, health check, timeout,
recovery action, logs, limites e procedimento de update. Reiniciar continuamente
não corrige causa e pode amplificar falhas.

```powershell
Get-CimInstance Win32_Service |
  Select-Object Name, State, StartMode, StartName, PathName
Get-ScheduledTask | Select-Object TaskPath, TaskName, State
Get-ScheduledTaskInfo -TaskName 'NomeDaFixture'
```

## Tarefa agendada robusta

- caminho absoluto e argumentos sem segredos;
- conta e privilégio mínimo;
- trigger/timezone claros;
- limite de duração e concorrência;
- código de saída/log estruturado;
- comportamento definido para atraso, falha e reinício;
- cleanup/owner.

## Prática

Registre tarefa local que executa um script de inventário em `C:\RTE-Lab`, sem
senha embutida. Force sucesso e falha controlada, correlacione eventos/códigos e
remova a tarefa.

