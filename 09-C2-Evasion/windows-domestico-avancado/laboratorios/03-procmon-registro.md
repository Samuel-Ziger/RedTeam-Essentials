# Lab 03 — Registro, serviços e investigação com ProcMon

**Classe:** B — mudanças limitadas a uma chave HKCU e uma tarefa fixture da conta atual.

## Propósito

Investigar uma falha de configuração por sequência de eventos, sem capturar o sistema inteiro e sem classificar cada `NAME NOT FOUND` como problema. O gate integra Registro, NTFS, I/O, inicialização, PowerShell e Sysinternals.

## Pré-condições

- Lab 02 e capítulos 08–13 concluídos;
- ProcMon e Autoruns obtidos da fonte oficial e assinaturas conferidas;
- conta comum, snapshot e diretório `%LOCALAPPDATA%\RTE-Lab\lab03`;
- nenhuma chave `HKCU\Software\RTECourse\Advanced` preexistente.

Se a chave ou tarefa já existir, pare e escolha outro nome registrado. Nunca apague um objeto que não foi criado por este laboratório.

## Preparação da fixture

Crie uma chave HKCU com valores sintéticos `Mode = baseline` e `BatchSize = 25`. Escreva uma função PowerShell que recebe o caminho da chave, lê os valores com `-ErrorAction Stop` e devolve objeto com schema, modo e tamanho. A função não deve criar valor ausente automaticamente.

Crie também a tarefa `RTE-Fixture-Timestamp` descrita no capítulo 11, executada pela conta atual e sem elevação. Exporte sua definição e registre o próximo horário. O arquivo gerado deve ficar apenas no diretório do laboratório.

## Captura mínima

Pare a captura do ProcMon, limpe eventos e configure estes filtros:

- `Process Name is powershell.exe Include`;
- `Path begins with HKCU\Software\RTECourse\Advanced Include` quando a representação permitir;
- categoria Registry para a fase de leitura.

Inicie a captura, execute uma leitura saudável e pare. Depois renomeie somente o valor `Mode` para `ModeMissing`, limpe a captura, execute novamente e pare. Restaure o nome e faça uma terceira leitura sem captura longa.

Se o filtro por caminho não casar devido à representação interna do hive, observe uma execução curta, descubra o prefixo efetivo e refine. Não remova o filtro de processo para compensar.

## Interpretação

Selecione no máximo dez eventos que expliquem abertura da chave, consulta dos valores e resultado. Ordene por sequência e relacione com o fluxo da função. Um `NAME NOT FOUND` só é causal se corresponde ao valor exigido, antecede a exceção e a restauração isolada recupera a função.

Compare o evento ausente com sondagens opcionais que o PowerShell ou runtime fazem e que não alteram o resultado. Explique por que “vermelho” não é sinônimo de causa. Use horário, PID e caminho para evitar misturar execuções.

No Autoruns, localize somente a tarefa fixture e confirme comando, publisher quando aplicável, caminho e conta. Não desabilite outras entradas. O objetivo é reconhecer cobertura e contexto.

## Evidência

Entregue a função e testes para: valores válidos, `Mode` ausente, `BatchSize` inválido e chave ausente. Inclua filtro exportado, tabela dos eventos relevantes, hipótese prevista, evidência contra e conclusão. O CSV público deve remover usuário e caminhos desnecessários.

Compare também ACL e timestamps da pasta antes/depois. Não atribua alteração de timestamp a uma causa sem repetir o teste e identificar a operação correspondente.

## Critérios de aceite

- todas as mudanças estão em HKCU e diretório fixture;
- a captura contém somente janela e processo necessários;
- a causa é demonstrada por falha e recuperação com uma variável;
- a função falha explicitamente em vez de inventar default;
- testes não dependem do Registro real do usuário.

## Cleanup e revisão

Remova a tarefa com `Unregister-ScheduledTask`, apague somente a chave criada e o diretório fixture. Confirme ausência por consulta. Remova PML bruto após produzir evidência sanitizada.

Responda: que parte da conclusão vem do ProcMon e qual vem do código? Por que HKCU depende da identidade? Que diferença existe entre desregistrar a tarefa e apagar seu script? Como provar que o cleanup não atingiu objeto anterior ao lab?

