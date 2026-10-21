# 11 — Serviços, tarefas e inicialização

O Windows possui mecanismos diferentes para executar trabalho sem uma janela aberta: serviços, tarefas agendadas, aplicativos de inicialização e extensões do shell. Eles parecem equivalentes quando vistos apenas como “algo que inicia sozinho”, mas diferem em identidade, ciclo de vida, condições e rastreabilidade. Neste capítulo, você aprenderá a administrá-los com segurança em uma máquina de laboratório.

## Objetivos

Ao concluir, você deverá ser capaz de:

- explicar estados e responsabilidades do Service Control Manager;
- distinguir serviço, tarefa agendada e inicialização por usuário;
- avaliar identidade, permissões, dependências, recuperação e logging;
- criar e remover uma tarefa inofensiva, limitada à conta atual;
- investigar uma entrada automática sem classificá-la apenas por aparência.

## Service Control Manager

O **Service Control Manager** (SCM) mantém o banco de configuração e coordena iniciar, parar, pausar e consultar serviços. Um serviço registra um ponto de entrada que recebe controles e informa transições como `START_PENDING`, `RUNNING`, `STOP_PENDING` e `STOPPED`. Informar o estado corretamente evita que operadores confundam inicialização lenta com travamento.

O tipo de inicialização descreve quando o SCM tenta iniciar o serviço: automático, automático atrasado, manual ou desabilitado. `Manual` não significa “nunca executa”; um gatilho, dependência ou aplicativo pode iniciá-lo sob demanda. Dependências explícitas devem ser raras e justificadas, pois cadeias longas aumentam impacto de uma falha.

A conta de execução define a identidade de segurança. `LocalSystem`, `LocalService`, `NetworkService`, conta virtual e usuário comum possuem capacidades diferentes. A regra é escolher a identidade menos privilegiada que permita o trabalho. Uma aplicação doméstica não deve solicitar `LocalSystem` apenas por conveniência.

```powershell
Get-CimInstance Win32_Service |
    Select-Object Name, DisplayName, State, StartMode, StartName, PathName |
    Sort-Object Name |
    Export-Csv -NoTypeInformation -Encoding utf8 .\servicos.csv
```

Ao revisar `PathName`, considere executável, argumentos, aspas e permissões do arquivo e dos diretórios. Não tente “corrigir” serviços nativos durante o estudo. O inventário é uma observação, não uma autorização para reconfiguração.

## Recuperação e observabilidade

Recovery actions podem reiniciar o serviço, executar uma ação administrativa ou reiniciar a máquina. Reinício infinito esconde defeitos e cria tempestades de eventos; use limite, atraso e escalonamento. Um serviço bem projetado responde ao controle de parada, encerra trabalho de maneira cooperativa e publica eventos que expliquem a falha sem expor segredos.

O SCM registra eventos importantes, mas o diagnóstico deve correlacionar pelo menos: horário, nome do serviço, estado anterior, código de saída, log da aplicação e mudança recente. “O serviço parou” é consequência, não causa.

## Task Scheduler

Uma tarefa combina **gatilhos**, **ações**, **condições**, **configurações** e **principal**. O gatilho diz quando considerar a execução; condições podem exigir energia AC, ociosidade ou rede; configurações tratam repetição, tempo máximo e instâncias simultâneas; o principal define a conta e o nível de execução.

Crie a seguinte fixture somente na conta atual e em um diretório do laboratório:

```powershell
$root = Join-Path $env:LOCALAPPDATA 'RTE-Lab'
New-Item -ItemType Directory -Force -Path $root | Out-Null
$script = Join-Path $root 'timestamp.ps1'
Set-Content -Encoding utf8 $script "Get-Date -Format o | Add-Content '$root\execucoes.log'"

$action  = New-ScheduledTaskAction -Execute 'powershell.exe' `
  -Argument "-NoProfile -File `"$script`""
$trigger = New-ScheduledTaskTrigger -Once -At (Get-Date).AddMinutes(2)
Register-ScheduledTask -TaskName 'RTE-Fixture-Timestamp' `
  -Action $action -Trigger $trigger -Description 'Fixture educacional descartável'
```

Após validar resultado e histórico, remova apenas a fixture:

```powershell
Unregister-ScheduledTask -TaskName 'RTE-Fixture-Timestamp' -Confirm:$false
```

Evite credenciais armazenadas e a opção de privilégios elevados. O exercício mede ciclo de vida e evidência, não persistência.

## Startup e Autoruns

Pastas Startup, chaves `Run`, extensões do Explorer e muitos outros pontos podem iniciar componentes. O Sysinternals Autoruns consolida essa visão. Uma entrada desconhecida não é automaticamente maliciosa: verifique caminho, publisher, assinatura, data, pacote de instalação e relação com software conhecido.

Desabilitar entradas em massa prejudica inicialização e apaga contexto. Primeiro exporte a linha de base, filtre itens Microsoft apenas quando souber por quê e investigue diferenças. Hashes iguais indicam conteúdo igual, não intenção; assinatura informa procedência e integridade, não necessidade operacional.

## Exercícios

1. Classifique cinco serviços por conta, modo de início e responsabilidade provável, sem modificar nenhum deles.
2. Execute a fixture, capture histórico, artefato e código de resultado; depois remova tarefa e arquivos.
3. Compare as garantias de uma tarefa “ao logon” com um serviço automático.
4. Exporte duas linhas de base do Autoruns e explique cada diferença com evidência adicional.

## Checklist

- [ ] Diferencio estado, modo de início e gatilho de serviço.
- [ ] Avalio identidade e privilégio separadamente da funcionalidade.
- [ ] Sei decompor uma tarefa em gatilho, ação, condição e principal.
- [ ] Investigo entradas automáticas antes de alterar o sistema.
- [ ] Toda fixture criada possui procedimento de remoção testado.

