# 03 — Processos, threads, handles e Object Manager

Processo é contêiner de execução e recursos; thread é a unidade escalonável.
Windows representa muitos recursos como objetos, acessados por handles com
direitos. Diagnóstico melhora quando cada contador é ligado ao objeto correto.

## Objetivos

- explicar criação e término de processo e thread;
- distinguir PID, handle, objeto e nome no namespace;
- relacionar PEB/TEB ao contexto de user mode sem tratá-los como ABI pública;
- escolher primitivas de sincronização por semântica;
- reconhecer race, deadlock e vazamento em fixtures próprias.

## Ciclo do processo

A criação envolve imagem executável, espaço virtual, token primário, tabela de
handles, ambiente, PEB e thread inicial. O loader mapeia dependências e prepara
o estado antes do entry point da aplicação. Detalhes variam por build e runtime.

PEB guarda informação de processo em user mode; TEB guarda informação por thread.
São úteis em depuração, mas layouts internos não são contrato estável para
aplicações comuns. Prefira APIs documentadas.

PID identifica uma instância durante sua vida e pode ser reutilizado. Combine
PID, horário de início e imagem para correlacionar eventos. Nome sozinho é fraco.

```powershell
$target = Start-Process notepad.exe -PassThru
$target | Select-Object Id, ProcessName, StartTime, SessionId,
  HandleCount, Threads, Path
```

Algumas propriedades são coletadas em momentos diferentes; o processo pode
terminar entre consultas. Trate “process has exited” como condição de corrida da
observação, não como corrupção.

## Threads e scheduling

Uma thread possui contexto de registradores, stacks de user/kernel mode, TEB,
prioridade e estado. O scheduler seleciona threads prontas para processadores.
Prioridade alta não cria CPU e pode prejudicar responsividade. Não altere
prioridades do sistema no laboratório.

CPU de processo é soma acumulada de threads. Contagem de threads não mede
paralelismo efetivo. Observe séries temporais e stacks quando a pergunta exigir.

## Object Manager e handles

Object Manager fornece ciclo de vida, nomes e segurança a vários tipos: processo,
thread, evento, mutex, seção e alguns objetos de I/O. Um objeto pode sobreviver a
um nome enquanto houver referências. Handle pertence a uma tabela do processo e
inclui direitos concedidos.

O mesmo valor numérico em dois processos não significa o mesmo objeto. Fechar
handle reduz referência; não “apaga” necessariamente o objeto. Handle leak aparece
como crescimento sustentado durante carga repetível, não uma contagem alta
isolada.

Process Explorer/Handle podem mostrar recursos da própria fixture. Não feche
handles pela ferramenta: isso viola invariantes da aplicação e pode corromper
estado. Corrija ownership no código.

## Jobs e árvore de processos

Job objects agrupam processos e podem aplicar limites/ciclo de vida. Relação
pai-filho ajuda a narrar criação, mas o pai pode terminar e o sistema não mantém
uma árvore de ownership rígida como filesystem. Ferramentas reconstroem a árvore
com IDs e tempos; registre limitações.

## Sincronização

- mutex oferece exclusão com ownership;
- semaphore controla número de entradas;
- event sinaliza estado manual ou automaticamente resetado;
- waitable timer sinaliza tempo;
- critical section/SRW lock sincronizam threads no processo.

Race ocorre quando resultado depende do interleaving não protegido. Deadlock
surge quando esperas formam ciclo sem progresso. Starvation é espera prolongada
porque outros continuam recebendo recurso. Logging pode alterar timing e ocultar
race; reproduza muitas vezes e use tracing controlado.

## Término e cleanup

Fechamento cooperativo permite salvar, sinalizar threads e liberar handles.
Encerramento abrupto pode pular `finally`, destructors e protocolos. Para a DLL
do curso, o consumidor chama `FreeLibrary`; para arquivo, chama `CloseHandle`.
Use ferramentas de término apenas na fixture travada e após preservar evidência.

## Prática guiada

Execute o consumidor da DLL repetidamente. Colete antes/durante/depois: horário,
PID, threads, handles, módulos e código de saída. A curta duração pode impedir
observação manual; acrescente uma opção de espera documentada à fixture em vez de
anexar-se a processo alheio. Demonstre que contadores retornam à baseline.

## Exercícios

1. Desenhe imagem → processo → PEB/token/handles → threads/TEBs.
2. Explique PID versus handle versus objeto.
3. Escolha event, mutex ou semaphore para três cenários e justifique.
4. Modele um deadlock com duas travas no papel e proponha ordem global.
5. Meça handles da fixture em 100 execuções e defina critério de vazamento.

## Checklist de domínio

- [ ] PID é correlacionado com tempo de início e imagem.
- [ ] PEB/TEB são internals observados, não ABI prometida.
- [ ] Handle, objeto, nome e recurso físico são distintos.
- [ ] Contador alto isolado não é chamado de vazamento.
- [ ] Distingo race, deadlock e starvation.
- [ ] Prefiro término cooperativo e ownership explícito.
- [ ] Não fecho handles nem inspeciono memória de terceiros.
