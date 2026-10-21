# 01 — Arquitetura Windows NT e fronteiras do sistema

Windows NT organiza componentes por privilégio e responsabilidade. O diagrama
é um modelo para raciocinar, não uma promessa de que cada chamada atravessa uma
caixa exatamente uma vez. Implementações mudam entre builds; contratos públicos
são mais estáveis que detalhes internos.

## Objetivos

- distinguir modo usuário, modo kernel, Executive, kernel e HAL;
- mapear uma operação Win32 até o subsistema responsável;
- explicar o papel de processos centrais sem inspecionar seu conteúdo;
- reconhecer Object Manager, Memory Manager, I/O Manager e Security Reference Monitor;
- separar interface documentada, ABI e implementação observada.

## Visão em camadas

```text
aplicação própria
   ↓ API Win32 / runtime
KernelBase, kernel32, advapi32, user32 e outras bibliotecas
   ↓ ntdll / Native API / transição controlada quando necessária
──────────────── fronteira user mode ↔ kernel mode ────────────────
Executive: objetos · processos · memória · I/O · segurança · configuração
Kernel: scheduling de baixo nível · interrupções · sincronização
HAL e drivers
   ↓
hardware ou dispositivo virtual
```

Nem toda API realiza syscall: parte do trabalho pode ocorrer em user mode,
consultar cache ou chamar outras APIs. Uma API de alto nível também pode gerar
várias transições. O objetivo do modelo é localizar responsabilidade e evidência.

## Executive, kernel e HAL

O Executive reúne gerenciadores e serviços em kernel mode. Object Manager dá
modelo comum a muitos recursos; Process/Thread Manager participa do ciclo de
execução; Memory Manager administra espaços virtuais e páginas; I/O Manager
coordena pedidos a stacks de drivers; Configuration Manager implementa o Registro;
Security Reference Monitor participa de decisões de acesso.

O kernel em sentido estrito trata scheduling, dispatch de interrupções,
sincronização e mecanismos muito próximos da CPU. A HAL abstrai detalhes de
plataforma. O binário `ntoskrnl.exe` incorpora responsabilidades de kernel e
Executive; portanto nomes conceituais não implicam um executável separado.

## Componentes em modo usuário

Aplicações usam o ambiente Win32 e serviços. Bibliotecas como KernelBase e
`ntdll.dll` fazem parte do caminho, mas suas divisões mudaram ao longo das
versões. API sets permitem que imports representem contratos encaminhados para
implementações concretas; isso explica por que “a DLL que exporta a API” nem
sempre é tão simples quanto o nome histórico.

Processos como Session Manager, Client/Server Runtime, Service Control Manager
e Local Security Authority cumprem papéis centrais. Neste curso você identifica
nome, sessão, assinatura e função documentada, mas não abre memória nem handles
de processos protegidos. O objetivo é arquitetura, não coleta sensível.

## Subsistemas e sessões

O ambiente moderno executa aplicações Win32 sobre componentes de user mode e
kernel. Sessões isolam contextos interativos; serviços normalmente operam na
Session 0. Desktop e window station são objetos adicionais. Session ID não é
identidade nem nível de privilégio.

WOW64 permite processos x86 em Windows x64 usando tradução de ambiente e
componentes específicos. Isso afeta arquitetura de módulos, paths e visualizações
do Registro. Não significa “emulação completa de outro Windows”.

## Observação segura

Use Process Explorer ou consultas do sistema para mapear somente uma aplicação
própria:

```powershell
$process = Start-Process notepad.exe -PassThru
$process | Select-Object Id, ProcessName, SessionId, StartTime, Path
Get-AuthenticodeSignature -FilePath $process.Path |
  Select-Object Status, SignerCertificate
```

Em Process Explorer, observe árvore de processos, threads, token e DLLs da
fixture. Algumas propriedades exigem arquitetura ou acesso compatível. Registre
`ACCESS DENIED` como limite esperado. Não altere segurança nem abra ferramenta
como SYSTEM.

## Do clique ao arquivo

Modele a ação “aplicação lê uma fixture”: shell inicia processo; loader mapeia a
imagem e dependências; runtime chama API documentada; a biblioteca prepara a
operação; a transição entra no kernel; Object/I/O/Security Managers resolvem
handle, acesso e stack; filesystem entrega dados; conclusão retorna. Cache pode
evitar acesso físico. Um trace serve para confirmar partes, não para afirmar que
todo detalhe interno é fixo.

## Erros comuns de modelo

- chamar todo `ntoskrnl.exe` simplesmente de “kernel” sem distinguir conceitos;
- acreditar que `kernel32.dll` executa em kernel mode por causa do nome;
- supor uma syscall por API;
- usar nomes/endereço de uma build como contrato permanente;
- tratar processo central como alvo de experimentação;
- confundir sessão, conta, desktop e privilégio.

## Exercícios

1. Desenhe a arquitetura e atribua cada responsabilidade ao componente correto.
2. Trace conceitualmente abertura/leitura/fechamento de uma fixture.
3. Explique por que KernelBase, kernel32 e API sets podem aparecer no mesmo fluxo.
4. Compare processos x64 e x86 próprios e registre módulos sem forçar acesso.
5. Dê três exemplos de contrato público e detalhe interno não contratual.

## Checklist de domínio

- [ ] Distingo user mode, Executive, kernel, HAL e driver.
- [ ] Sei por que `kernel32.dll` permanece em user mode.
- [ ] Uma API pode gerar zero, uma ou várias transições.
- [ ] Processo, sessão, identidade e privilégio não são sinônimos.
- [ ] Observação detalhada fica restrita às minhas fixtures.
- [ ] Acesso negado não é contornado.
- [ ] Meu diagrama é identificado como modelo dependente de build.
