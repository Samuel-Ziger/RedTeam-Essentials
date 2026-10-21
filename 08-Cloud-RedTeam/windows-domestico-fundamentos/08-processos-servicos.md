# 08 — Processos, threads, serviços e inicialização

Programa é código armazenado; processo é uma instância em execução. Serviços,
tarefas e aplicativos de inicialização são mecanismos diferentes que podem
produzir sintomas semelhantes. Diagnóstico começa identificando qual mecanismo
está envolvido.

## Objetivos

- diferenciar programa, processo, thread, handle, token e serviço;
- interpretar CPU, memória e tempo em vez de uma captura isolada;
- relacionar serviço ao Service Control Manager, conta e executável;
- mapear os principais mecanismos de inicialização local;
- encerrar uma fixture preservando contexto e preferindo fechamento cooperativo.

## O objeto processo

Ao iniciar um executável, o Windows cria um processo com espaço de endereçamento,
token, handles e pelo menos uma thread. A thread é a unidade que executa código.
Handles referenciam objetos do sistema e são válidos no contexto do processo.
O PID identifica aquela instância enquanto ela vive; pode ser reutilizado depois.

```powershell
Get-Process |
  Sort-Object CPU -Descending |
  Select-Object -First 10 Name, Id, CPU, WorkingSet64, StartTime
```

Algumas propriedades podem gerar erro para processos protegidos ou já encerrados.
CPU nesse objeto costuma ser tempo acumulado, não “porcentagem agora”. Working
set é memória física associada naquele momento, não toda a memória virtual nem
prova de vazamento. Colete amostras num intervalo e relacione ao sintoma.

Nome não prova caminho. Para uma fixture conhecida, observe caminho e assinatura
com privilégios mínimos:

```powershell
$process = Start-Process notepad.exe -PassThru
$process | Select-Object Id, ProcessName, StartTime, Path
Get-AuthenticodeSignature -FilePath $process.Path |
  Select-Object Status, StatusMessage, SignerCertificate
```

A disponibilidade de `Path` depende do processo e do acesso. Não eleve apenas
para preencher uma coluna não essencial.

## Serviços e o SCM

Service Control Manager registra configuração, inicia e acompanha serviços.
Um serviço pode executar sem sessão interativa, compartilhar processo com outros
serviços ou depender de componentes. `Stopped` pode ser o estado correto para um
serviço acionado sob demanda.

```powershell
Get-Service | Group-Object Status
Get-CimInstance Win32_Service |
  Select-Object Name, DisplayName, State, StartMode, StartName, ProcessId,
    PathName
```

`StartMode` e estado atual respondem perguntas diferentes. `Automatic` não prova
que está rodando, e `Running` não prova inicialização automática. `PathName` pode
incluir argumentos; não o use diretamente como caminho de arquivo sem analisar.
Conta do serviço define contexto e deve seguir o privilégio necessário ao
produto, não ser alterada por tentativa.

Antes de reiniciar um serviço, examine dependências, eventos, impacto e operação
em andamento. Alterar serviços centrais pode impedir boot, update ou login. Este
módulo apenas consulta serviços do sistema.

## Mecanismos de inicialização

Aplicativos podem iniciar pela pasta Startup, configurações de usuário,
Registro, tarefa agendada, serviço ou mecanismos do próprio pacote. Task Manager
mostra uma visão útil de aplicativos de inicialização e impacto estimado, mas
não representa todos os mecanismos.

```powershell
Get-CimInstance Win32_StartupCommand |
  Select-Object Name, Command, Location, User

Get-ScheduledTask |
  Select-Object -First 20 TaskPath, TaskName, State
```

Não desabilite itens que não reconhece. Identifique editor, origem, função,
usuário e efeito medido. “Deixar o Windows mais leve” sem baseline costuma trocar
um problema observável por falhas difíceis de atribuir.

## Diagnóstico de consumo

Defina sintoma: atraso em qual ação, durante quanto tempo e com qual impacto?
Registre horário, carga do usuário, CPU, memória, disco, versão do executável e
eventos no intervalo. Compare repouso e reprodução. Uma amostra alta pode ser
trabalho legítimo; uma média esconde picos. O módulo 09 aprofundará internals e
ferramentas Sysinternals; aqui o foco é raciocínio básico.

Encerrar o processo pode aliviar o sintoma, mas apaga estado e não prova a causa.
Primeiro tente fechar pela interface, permitindo que o aplicativo salve e libere
recursos. `Stop-Process` é apropriado para a fixture travada e explicitamente
identificada, nunca para uma lista ampla baseada apenas no nome.

## Prática guiada

Abra duas instâncias do Bloco de Notas, salve apenas fixtures e registre PID,
hora e caminho. Feche uma normalmente e observe seu desaparecimento. Na segunda,
use `Stop-Process -Id <PID> -WhatIf`, confira o alvo e então encerre apenas se
nenhum dado estiver pendente. Compare evidências e explique por que PID foi mais
preciso que nome.

Escolha também um serviço parado e um em execução. Sem alterá-los, registre
StartMode, conta, dependências e eventos relevantes. Explique por que ambos os
estados podem estar corretos.

## Exercícios

1. Desenhe executável → processo → threads/handles/token.
2. Colete cinco amostras de um processo e diferencie contador acumulado de taxa.
3. Compare estado e modo de início de três serviços sem modificá-los.
4. Classifique quatro itens entre serviço, tarefa e app de inicialização.
5. Explique quando fechamento cooperativo é preferível a encerramento forçado.

## Checklist de domínio

- [ ] Diferencio arquivo executável, processo, thread, handle e token.
- [ ] Não interpreto CPU acumulada como porcentagem instantânea.
- [ ] PID é usado apenas para a instância observada.
- [ ] Distingo estado atual de modo de inicialização do serviço.
- [ ] Não habilito ou desabilito serviços por uma lista genérica.
- [ ] Coleto contexto antes de encerrar uma fixture.
- [ ] Reconheço serviços, tarefas e aplicativos de inicialização como mecanismos distintos.
