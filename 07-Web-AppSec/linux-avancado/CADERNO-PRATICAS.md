# Caderno de práticas de Linux avançado

Estas 72 práticas curtas transformam leitura em habilidade antes dos nove
laboratórios avaliativos. Toda entrega contém pergunta, previsão, ambiente,
comandos, saída bruta, interpretação, limitação e reversão.

## Regras

- A: leitura ou processo do usuário; B: arquivos e imagens descartáveis.
- C: VM com snapshot e console; D: VM sacrificável.
- Nunca use disco físico, interface de rede ou dado real.
- Uma prática sem cleanup comprovado está incompleta.
- Se alvo, versão ou escopo não puderem ser confirmados, pare.

## Bloco 1 — método, fonte e build

### P01 — hipótese falsificável · A

Converta três sintomas em métrica, unidade, controle e condição que refutaria a
explicação inicial.

### P02 — reprodução independente · A

Entregue um caderno sem instrução oral e registre toda informação que faltou para
outra pessoa repetir a coleta.

### P03 — mapa da árvore · A

Parta de uma syscall, encontre UAPI, implementação, callers, config, mantenedor e
um selftest no mesmo checkout.

### P04 — histórico do trecho · A

Use log, blame e discussão para explicar por que uma linha existe sem atribuir
culpa ao autor mostrado.

### P05 — config até artefato · B

Escolha três símbolos Kconfig e siga valor, macro gerada, objeto, símbolo ou
módulo e evidência em runtime.

### P06 — build reproduzível · B

Compile em dois diretórios limpos, compare hashes e classifique a primeira
divergência sem instalar o resultado.

## Bloco 2 — ABI, ELF e tarefas

### P07 — retorno parcial · A

Implemente leitura e escrita completas tratando `EINTR`, short I/O, EOF e erro
sem duplicar bytes.

### P08 — syscall ou vDSO · A

Determine o caminho real de duas funções usando ELF, auxiliary vector,
desmontagem e trace filtrado.

### P09 — matriz ELF · A

Compare PIE, não PIE, RELRO parcial e completo por headers, relocations,
segmentos e mapas.

### P10 — falha de interpreter · B

Altere somente uma cópia descartável para solicitar loader ausente e diagnostique
a mensagem sem usar `ldd`.

### P11 — PID, TID e TGID · A

Crie processo multithread e correlacione `ps`, tarefas em procfs e estados.

### P12 — supervisor correto · A

Crie três filhos, receba SIGCHLD de forma segura, colete todos e prove ausência
de zombies.

## Bloco 3 — namespaces e CPU

### P13 — visão por namespace · A/C

Compare inodes de PID, mount, UTS, IPC, user, cgroup e time antes e depois de
`unshare`, sem criar namespace de rede.

### P14 — propagação de mount · C

Torne a árvore privada, monte proc no namespace, confirme ausência no pai e
desfaça na ordem inversa.

### P15 — peso sob competição · A

Execute cargas iguais isoladas e concorrentes com nice diferente; compare serviço
recebido e espera runnable.

### P16 — afinidade e locality · A

Compare mesma CPU e CPUs separadas, registrando migrations, switches e hipótese
de cache sem declarar causalidade automática.

### P17 — contextos de execução · A

Classifique dez funções do kernel quanto a processo, IRQ, capacidade de dormir e
proteção necessária.

### P18 — timer e work lifetime · A

Desenhe enfileiramento, execução, cancelamento síncrono e liberação de um objeto
referenciado por trabalho assíncrono.

## Bloco 4 — concorrência e RCU

### P19 — invariante multicampo · A

Modele uma interleaving que mantém atomics individuais corretos e viola o estado
composto.

### P20 — grafo de locks · A

Desenhe deadlock AB/BA, imponha ordem global e explique as arestas que lockdep
observaria.

### P21 — publicação acquire/release · A

Implemente exemplo pequeno de objeto imutável e trate lifetime separadamente da
visibilidade.

### P22 — ferramentas de corrida · C

Execute teste didático com ThreadSanitizer ou KCSAN em build de diagnóstico e
registre overhead e limites.

### P23 — timeline RCU · A

Desenhe dois leitores, publicação, remoção, grace period e liberação, marcando
qual versão cada leitor pode alcançar.

### P24 — RCU versus mutex · A

Compare complexidade, custo de leitura, atualização e memória para uma tabela
99% leitura.

## Bloco 5 — memória e pressão

### P25 — reserva versus residência · A

Meça VSZ, RSS, PSS e faults antes de reservar, depois de reservar e depois de
tocar cada página.

### P26 — copy-on-write · A

Após fork, altere páginas no filho e correlacione faults e PSS dos dois processos.

### P27 — reclaim controlado · A/C

Aumente working set sob limite seguro, colete PSI, faults e eventos e encerre
antes de pressionar a VM inteira.

### P28 — escopo de OOM · C

Desenhe diferenças entre OOM global e memcg e simule apenas dentro de limite
descartável com margem administrativa.

### P29 — first-touch · A

Compare inicialização serial e paralela somente em topologia com dois nós,
registrando CPU e distribuição de páginas.

### P30 — THP efetiva · A

Compare configuração com páginas realmente promovidas em smaps e meça custo e
benefício para a carga.

## Bloco 6 — VFS e filesystems

### P31 — descrição aberta · A

Compare offsets após dois open independentes e após dup; explique o objeto
compartilhado.

### P32 — unlink com referência · A

Remova o nome de arquivo mantido aberto, observe espaço e prove quando o inode é
liberado.

### P33 — substituição durável · A

Implemente temporário, fsync, rename e fsync de diretório com tratamento de todos
os retornos.

### P34 — resolução segura · A

Modele uma corrida de pathname e refaça a operação com directory fd e restrições
de resolução.

### P35 — matriz de filesystem · B/C

Em imagens, compare ext4, XFS e Btrfs pela mesma carga, features e opções.

### P36 — crash consistency · C

Teste cópias de imagens em pontos definidos e diferencie morte do processo,
queda do guest e falha elétrica não simulada.

## Bloco 7 — bloco e Device Mapper

### P37 — profundidade da fila · B

Compare quatro queue depths contra arquivo de volume descartável e apresente
throughput e percentis.

### P38 — caminho da escrita · A

Desenhe aplicação, page cache, filesystem, bio, request, driver, device, flush e
completion.

### P39 — camadas virtuais · A

Relacione métricas da aplicação, guest, dispositivo virtual e host sem misturar
seus escopos.

### P40 — persistência · B

Compare write, fdatasync, fsync e O_SYNC num protocolo controlado, sem concluir
além da camada observada.

### P41 — thin data e metadata · C

Crie pool em loops explícitos, monitore percentuais separados e pare antes do
esgotamento.

### P42 — árvore e teardown · C

Desenhe targets, mounts e loops, depois remova consumidores na ordem inversa e
compare inventário final.

## Bloco 8 — eventos e drivers

### P43 — epoll por estados · A

Use timerfd e eventfd, trate erro, HUP, EAGAIN e encerramento determinístico em
level e edge-triggered.

### P44 — cancelamento concorrente · A

Modele submit, conclusão e cancelamento chegando em ordens diferentes com um
único cleanup.

### P45 — análise io_uring · A

Desenhe SQE, CQE, buffer e user_data para short I/O sem carregar código
privilegiado.

### P46 — probe e unwind · A

Projete inicialização de driver em cinco estágios e caminho de desfazer para cada
falha.

### P47 — DMA e IOVA · A

Diferencie endereço virtual, físico, DMA e IOVA e descreva mudança de ownership
em mapping streaming.

### P48 — módulo didático · D

Compile, inspecione vermagic, carregue, leia e remova o módulo do curso apenas na
VM sacrificável.

## Bloco 9 — boot, systemd e cgroup

### P49 — cadeia de confiança · A

Desenhe signer, chave, verifier, artefato e revogação de firmware até raiz.

### P50 — boot A/B · C/D

Modele contador de tentativas, health check, promoção e retorno ao slot conhecido
em três pontos de falha.

### P51 — initramfs mínimo · B

Extraia uma cópia, classifique arquivos essenciais e procure secrets indevidos.

### P52 — grafo de unidades · A

Compare Requires/Wants com After/Before removendo uma relação por vez.

### P53 — readiness real · B

Defina ready e watchdog que provem progresso do worker, não apenas existência do
processo.

### P54 — hardening incremental · B

Aplique cinco diretivas separadamente e teste operação normal, erro, reload e
stop.

### P55 — weight e quota · A

Compare weights com e sem competidor e quota por período, incluindo throttling.

### P56 — high antes de max · C

Eleve memória sob `MemoryHigh`, colete PSI/events e preserve margem antes de
`MemoryMax`.

## Bloco 10 — performance, tracing e eBPF

### P57 — hipótese mínima · A

Escolha o menor conjunto perf que poderia refutar uma hipótese e registre
multiplexing.

### P58 — sampling e unwind · A

Compare frame pointer e DWARF em qualidade de stacks e overhead.

### P59 — tracepoint com orçamento · C

Defina clock, filtro, buffer, taxa, duração e perda antes de habilitar um evento
local.

### P60 — restauração em erro · C

Injete falha no script de tracing e prove pelo estado final que o trap restaurou
tudo.

### P61 — objeto BPF estático · A

Inspecione seções, BTF, maps, hook e helpers do exemplo sem carregá-lo.

### P62 — verifier e rollback · C

Na VM, preserve log de uma rejeição segura e prove que falha parcial do loader
não deixa link ou map.

## Bloco 11 — depuração e virtualização

### P63 — core correspondente · A

Associe core, executável, bibliotecas e debug info por build ID antes de abrir no
GDB.

### P64 — causa raiz · A

Corrija um bug didático com teste que falha antes e passa depois; descreva
invariante, condição e lacuna de teste.

### P65 — kdump validado · D

Execute o teste oficial da distribuição, abra o vmcore com símbolos exatos e
registre primeira falha.

### P66 — cadeia qcow2 · B

Crie base somente leitura e overlay, valide backing chain e prove que apenas o
overlay mudou.

### P67 — KVM versus TCG · B/C

Compare a mesma carga, versão e entrada, documentando ruído e VM exits sem
generalizar ao hardware.

### P68 — contenção do QEMU · C

Execute QEMU offline em scope, compare RAM guest com RSS/PSS e prove ausência de
NIC e bloco físico.

## Bloco 12 — plataforma, integridade e entrega

### P69 — deadline e histograma · C

Construa orçamento, meça violações sob carga e não use média como garantia.

### P70 — Device Tree e imagem · B

Valide um DTS por binding e reconstrua imagem mínima em diretórios limpos.

### P71 — sandbox e integridade · B/C

Combine UID, descritores, filesystem, LSM/Landlock, seccomp e verity, testando uma
operação permitida e uma negada.

### P72 — pacote e patch revisáveis · B

Produza pacote offline reproduzível e patch didático bisectável; gere hashes,
SBOM, testes e relatório sem enviar material externamente.

## Critério de conclusão

Uma prática vale quando a evidência permite revisar o raciocínio. Complete no
mínimo uma prática de cada par antes do laboratório da etapa e todas as 72 antes
do projeto final.
