# Windows doméstico II — internals, PowerShell e defesa local

Este curso explica como o Windows executa, isola, observa e protege aplicações locais. A progressão vai da arquitetura NT até análise de mini dump, sempre usando programas próprios, dados sintéticos e diagnóstico reproduzível. O estudante termina capaz de construir uma pequena aplicação nativa, automatizar seu laboratório e demonstrar uma correção por evidência.

## Contrato de aprendizagem

| Campo | Definição |
|---|---|
| Nível | Intermediário a avançado |
| Duração | 300–440 horas |
| Pré-requisitos | Módulo 08; C, PowerShell e testes do módulo 00 |
| Ambiente | Windows 11 Pro/Enterprise em VM descartável |
| Ferramentas | Visual Studio Build Tools, Sysinternals, WPT, WinDbg, Pester |
| Evidência | parser PE, DLL/consumer, traces, mini dump próprio e capstone |
| Conclusão | seis gates, 56 práticas e projeto reproduzido por terceiro |

O tempo inclui leitura, implementação, repetição, diagnóstico e revisão. Executar comandos uma vez não equivale a concluir o conteúdo.

## Limites técnicos e éticos

O módulo é local, doméstico e não ofensivo. Não inclui redes, administração remota, Active Directory, injeção em processo, hooking, evasão, contorno de políticas, dumping de credenciais ou malware. DLL é estudada como unidade legítima de software; dump é exclusivamente da fixture própria; proteções são observadas ou testadas em piloto, nunca desligadas para facilitar o exercício.

Pare se o alvo não for inequívoco, se a captura incluir processo externo, se símbolos não corresponderem ao build, se aparecer dado real ou se uma ação sair da pasta/chave prevista. Consulte o contrato detalhado no capítulo 00.

## Como estudar

Para cada capítulo:

1. escreva o modelo e uma previsão antes de usar a ferramenta;
2. execute os exercícios em snapshot;
3. registre fatos, inferências, lacunas e limitações;
4. conclua as práticas correspondentes no caderno;
5. faça o laboratório quando ele for desbloqueado na aplicação;
6. preserve relatório sanitizado e execute cleanup.

Use [GUIA-TRACING-DEBUG.md](GUIA-TRACING-DEBUG.md) quando um sintoma atravessar fontes. [CADERNO-PRATICAS.md](CADERNO-PRATICAS.md) contém as 56 habilidades atômicas. Os laboratórios são gates integradores e possuem pré-requisitos semânticos na aplicação de estudos.

## Rota curricular

### Bloco 1 — Modelo do sistema

| # | Conteúdo |
|---:|---|
| 00 | [Método e laboratório avançado](00-laboratorio-avancado.md) |
| 01 | [Arquitetura Windows NT](01-arquitetura-nt.md) |
| 02 | [Modo usuário, kernel e syscalls](02-user-kernel-syscalls.md) |
| 03 | [Processos, threads e objetos](03-processos-threads-objetos.md) |
| 04 | [Tokens, sessões e integridade](04-tokens-sessoes-integridade.md) |
| 05 | [Memória virtual](05-memoria-virtual.md) |

Depois, conclua o [Lab 01 — processo, token e memória](laboratorios/01-processo-token-memoria.md).

### Bloco 2 — Formato e carregamento

| # | Conteúdo |
|---:|---|
| 06 | [PE/COFF](06-pe-coff.md) |
| 07 | [DLLs, ABI e loader](07-dll-loader.md) |

Construa os [exemplos executáveis](exemplos/README.md) e conclua o [Lab 02 — PE e DLL](laboratorios/02-pe-dll.md).

### Bloco 3 — Estado, I/O e automação

| # | Conteúdo |
|---:|---|
| 08 | [Registro internals](08-registro-internals.md) |
| 09 | [NTFS internals](09-ntfs-internals.md) |
| 10 | [I/O, dispositivos e drivers](10-io-drivers.md) |
| 11 | [Serviços, tarefas e inicialização](11-servicos-tarefas-startup.md) |
| 12 | [PowerShell avançado](12-powershell-avancado.md) |
| 13 | [Módulos, testes e assinatura](13-powershell-modulos-testes.md) |

Valide a integração no [Lab 03 — ProcMon e Registro](laboratorios/03-procmon-registro.md).

### Bloco 4 — Observabilidade e desempenho

| # | Conteúdo |
|---:|---|
| 14 | [ETW, Event Log e WER](14-etw-eventlog-wer.md) |
| 15 | [Sysinternals](15-sysinternals.md) |
| 16 | [Desempenho, WPR e WPA](16-performance-tracing.md) |

Leia o guia transversal e faça o [Lab 04 — ETW e desempenho](laboratorios/04-etw-performance.md).

### Bloco 5 — Proteções modernas

| # | Conteúdo |
|---:|---|
| 17 | [Defender e mitigações](17-defender-mitigacoes.md) |
| 18 | [VBS, HVCI e cadeia de confiança](18-vbs-integridade.md) |

Conclua o [Lab 05 — defesa local](laboratorios/05-defesa-local.md). Alteração de política é opcional, limitada à VM própria e depende de snapshot e rollback; o desenho do piloto já é uma entrega válida.

### Bloco 6 — Debugging e capstone

| # | Conteúdo |
|---:|---|
| 19 | [WinDbg e projeto integrador](19-windbg-projeto.md) |

Implemente o [Diagnostic Workbench](projetos/diagnostic-workbench/README.md) e defenda o [Lab 06 — dump e projeto](laboratorios/06-dump-projeto.md).

## Materiais de apoio

- [Laboratórios e classes de risco](laboratorios/README.md)
- [Exemplos PowerShell e C](exemplos/README.md)
- [Consulta rápida](CHEATSHEET.md)
- [Glossário](GLOSSARIO.md)
- [Respostas orientativas](RESPOSTAS.md)
- [Referências oficiais e vídeos](REFERENCIAS.md)

## Critério de conclusão

O módulo termina quando outra pessoa consegue, a partir de checkout limpo, reproduzir o build, executar a fixture saudável, compreender a falha, verificar a correção e limpar os artefatos sem orientação oral. A entrega deve apontar de cada conclusão para sua evidência e declarar o que permaneceu desconhecido.

