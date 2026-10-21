# Lab 01 — Processo, token e memória

**Classe:** B — observação e execução de fixture própria; nenhuma alteração em processo de terceiro.

## Propósito

Construir um mapa verificável de como uma aplicação própria aparece no Windows: processo, threads, handles, sessão, token e memória virtual. O objetivo não é colecionar screenshots, mas ligar cada observação ao modelo dos capítulos 01–05.

## Pré-condições

- capítulos 00–05 concluídos e exemplos revisados;
- VM em snapshot, sem dados pessoais e com conta comum;
- Bloco de Notas ou uma fixture simples criada pelo estudante;
- Process Explorer obtido da fonte oficial e assinatura conferida;
- pasta `%LOCALAPPDATA%\RTE-Lab\lab01` vazia.

Não use processo protegido, navegador, autenticação, antivírus ou software de outra pessoa. Acesso negado é um limite válido, não um convite para elevar ou contornar a proteção.

## Preparação e previsão

Antes de executar, desenhe o que espera observar: um processo com pelo menos uma thread, tabela de handles, token primário, espaço virtual e imagens mapeadas. Preveja quais campos mudam entre duas execuções: PID e endereços tendem a mudar; caminho, assinatura e arquitetura devem permanecer.

Registre build do Windows, arquitetura, conta, nível de privilégio do terminal, versão e hash da fixture. Use UTC no diário. Não inclua nome real da máquina ou usuário na entrega.

## Execução

1. Inicie a fixture como conta comum e anote horário, PID, parent PID, session ID e caminho completo.
2. No Process Explorer, confirme árvore, assinatura, usuário, nível de integridade e arquitetura. Exporte somente as propriedades necessárias.
3. Registre quantidade de threads e observe uma stack apenas quando os símbolos estiverem disponíveis. Não suspenda nem encerre threads.
4. Observe handles por tipo e contagem. Abra e feche, dentro da própria fixture, um arquivo sintético e identifique a mudança.
5. Registre working set, private bytes e tamanho virtual em cinco amostras com intervalo constante. Não declare vazamento a partir de crescimento único.
6. Feche a aplicação cooperativamente, confirme encerramento e repita. Compare identidade estável e valores efêmeros.
7. Opcionalmente, abra um terminal elevado e observe **somente o próprio terminal** com `whoami /all`. Compare grupos, privilégios e nível de integridade; não conclua que todos os privilégios estão habilitados.

Comandos somente leitura podem complementar a GUI:

```powershell
Get-Process -Id $PID | Select-Object Id, SessionId, StartTime,
    HandleCount, WorkingSet64, PrivateMemorySize64, VirtualMemorySize64
whoami /all
```

No primeiro comando, `$PID` representa o PowerShell atual. Para a fixture, passe explicitamente o PID observado.

## Evidência e análise

Produza um diagrama processo → threads/handles/token/memória e uma tabela com fonte de cada campo. Marque como **fato** o que a ferramenta mostrou, **inferência** o que deriva do modelo e **desconhecido** o que não foi coletado.

Explique por que PID não é identidade permanente, por que handle não é o objeto em si e por que working set difere de commit. Na comparação de elevação, diferencie grupos presentes, privilégios disponíveis e privilégios habilitados.

## Critérios de aceite

- duas execuções comparadas sem tocar processo externo;
- pelo menos cinco amostras de memória com unidade e intervalo;
- diagrama separa processo, objeto, handle, token e página virtual;
- acesso negado, se ocorrer, é registrado sem tentativa de contorno;
- nenhuma conclusão de vazamento depende de uma única amostra.

## Cleanup e revisão

Feche a fixture, remova apenas os arquivos sintéticos e confirme que não restou processo. Preserve o relatório sanitizado; apague exports contendo dados locais.

Responda: qual campo identifica o build? O que mudou por ASLR? Que evidência demonstraria handle leak? Por que elevar o terminal altera o experimento? Se você não consegue responder apontando para evidência, o gate ainda não foi concluído.

