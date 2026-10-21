# Caderno de práticas Linux

Use este caderno para transformar leitura em habilidade. São 64 práticas
curtas e cumulativas. Elas não substituem os seis laboratórios avaliativos:
preparam para eles.

## Como entregar cada prática

Registre objetivo, previsão, ambiente, comandos, saída relevante, explicação,
falha segura, reversão e conclusão. Saída sem interpretação não vale como
evidência. Toda mudança de classe B ou C exige snapshot e console.

| Classe | Regra |
|--------|-------|
| A | usuário comum e diretório temporário |
| B | VM própria, snapshot e alteração administrativa limitada |
| C | clone descartável; armazenamento, boot, módulo ou kernel |

Se uma variável estiver vazia, apontar para raiz, home inteira ou dispositivo
não criado pela própria prática, pare. Nunca adapte uma prática C ao host.

## Bloco 1 — ambiente, distribuição e instalação

### P01 — diário reproduzível · A

Execute uma coleta mínima duas vezes, registre versões e remova identificadores
desnecessários. Outra pessoa deve conseguir entender o ambiente sem conhecer sua
máquina.

### P02 — restauração de snapshot · B

Crie, altere e restaure um arquivo sintético. Meça o tempo e explique por que o
snapshot da VM não substitui uma cópia independente.

### P03 — matriz de distribuições · A

Compare Ubuntu LTS, Debian stable, Fedora e Alpine por ciclo, pacotes, init,
libc, política MAC, documentação e caso de uso. Confirme dados nas fontes
oficiais no dia da prática.

### P04 — kernel versus user space · A

Em dois containers ou VMs, compare release da distribuição, libc, shell, PID 1
e kernel. Explique quais diferenças pertencem ao user space e por que containers
podem compartilhar a mesma release de kernel.

### P05 — procedência da imagem · A

Desenhe o fluxo de verificação de assinatura do arquivo de checksums e do hash
da imagem. Identifique o canal usado para obter a chave e o que cada etapa não
garante.

### P06 — inventário pós-instalação · B

Registre firmware, arquitetura, mapa de disco, mounts, relógio, unidades com
falha e política de atualização. Compare o estado antes e depois da primeira
atualização.

## Bloco 2 — shell e sistema de arquivos

### P07 — descoberta de comandos · A

Escolha cinco nomes e descubra se cada um resolve para alias, função, builtin ou
executável. Registre ordem de resolução e caminho real.

### P08 — manual como ferramenta · A

Encontre synopsis, opções, status de saída e seção de exemplos de três comandos
sem pesquisar a web. Explique colchetes, alternativas e argumento repetível.

### P09 — quoting · A

Passe espaço, asterisco, cifrão, newline e hífen inicial como dados. Mostre a
quantidade real de argumentos recebida em cada variante.

### P10 — diretório e montagem · A

Para dez caminhos conhecidos, determine tipo, inode, filesystem e ponto de
montagem. Inclua proc, sys, dev, run e tmp.

### P11 — normalização de caminho · A

Compare caminho absoluto, relativo, link simbólico e resolução física. Mostre
como trocar o diretório atual altera apenas o relativo.

### P12 — nomes difíceis · A

Crie arquivos com espaço, tabulação, newline e prefixo de hífen em diretório
temporário. Liste, conte e remova usando delimitador NUL e fim explícito de
opções.

### P13 — hard link e symlink · A

Compare inode e conteúdo antes e depois de alterar, renomear, substituir e
remover o nome original. Explique qual objeto sobrevive em cada caso.

### P14 — arquivo esparso · A

Crie arquivo esparso pequeno o bastante para seu laboratório. Compare tamanho
aparente, blocos alocados e efeito de copiá-lo com ferramentas diferentes.

### P15 — archive não é backup · A

Empacote, liste, extraia em destino vazio e compare conteúdo. Depois enumere
retenção, independência, autenticação e restauração que ainda faltam.

### P16 — sincronização previsível · A

Compare origem com e sem barra final em uma simulação de rsync. Não use remoção.
Explique a árvore de destino prevista antes de executar.

## Bloco 3 — texto, permissões e identidades

### P17 — descritores padrão · A

Produza resultado em stdout, aviso em stderr e códigos distintos para sucesso e
falha. Capture cada fluxo separadamente e depois em ordem combinada.

### P18 — falha em pipeline · A

Crie pipeline cujo primeiro programa falha. Compare o status com e sem pipefail
e explique a consequência para automação.

### P19 — relatório AWK · A

Estenda o agregador de logs para recusar registro com menos de três campos e
contabilizar linhas inválidas, sem interpretar o texto livre como código.

### P20 — regex ancorada · A

Teste padrões ancorados e não ancorados em dados sintéticos. Documente um falso
positivo produzido por padrão amplo.

### P21 — parser correto · A

Leia o mesmo conjunto em texto delimitado e JSON. Explique por que grep não é
um parser confiável para reescrever estrutura aninhada.

### P22 — bits de diretório · A

Demonstre separadamente listar nomes, atravessar o diretório, ler um arquivo e
remover uma entrada. Não use modo universal.

### P23 — umask calculada · A

Preveja modos de arquivo e diretório com umask 022, 027 e 077; crie objetos e
compare. Investigue qualquer diferença antes de continuar.

### P24 — diretório de equipe · B

Crie grupo e diretório de laboratório com setgid, umask e ACL padrão. Prove
colaboração entre duas contas fictícias e bloqueio para outra identidade.

### P25 — diagnóstico de acesso · A

Em uma árvore temporária, provoque negação em um ancestral. Localize a primeira
camada incorreta com identidade, namei, stat, ACL e montagem.

### P26 — ciclo de conta · B

Crie conta humana e conta de serviço, diferencie shell e home, atribua grupo,
execute uma tarefa e faça offboarding incluindo processos, arquivos e chaves.

### P27 — sudo por função · B

Escreva política fictícia de menor privilégio e revise programas que permitem
shell, editor, carregamento de arquivo ou comando arbitrário. Não instale uma
regra até validá-la em snapshot com console.

### P28 — caminho de login · A

Desenhe terminal, daemon, PAM, NSS, autorização, sessão e shell. Para cada
camada, indique um log ou estado que confirme sua participação.

## Bloco 4 — software, processos e memória

### P29 — dono do arquivo · A

Encontre o pacote responsável por cinco arquivos e liste versão, repositório e
arquitetura. Inclua um arquivo não pertencente a pacote e explique a diferença.

### P30 — transação simulada · A

Simule instalação ou atualização, leia pacotes adicionados e removidos e
identifique como reverter. Não confirme a transação.

### P31 — build em staging · A

Compile um programa pequeno para diretório de staging. Produza inventário dos
arquivos sem gravar em diretório do sistema.

### P32 — árvore de processos · A

Execute o exemplo C, desenhe pai, filho, pipe, fechamento de descritores e
wait. Explique como surgiria um zombie.

### P33 — sinais e cleanup · A

Crie processo que trate TERM, grave confirmação e remova temporário. Compare
com KILL e explique o estado que não pôde ser limpo.

### P34 — arquivo removido aberto · A

Abra um arquivo por um processo, remova o nome e observe descritor, uso de disco
e liberação após fechar. Relacione a diferença entre df e du.

### P35 — limites · A

Compare limites da shell, de um processo e de uma unit. Escolha um limite baixo
e seguro para demonstrar falha controlada.

### P36 — reserva e residência · A

Execute o exemplo de memória com dois tamanhos permitidos. Compare faults antes
e depois de tocar páginas e correlacione com mapas e RSS.

### P37 — série de memória · A

Colete MemAvailable, swap I/O e PSI em cinco intervalos. Diferencie valor
acumulado, taxa e tempo de pressão.

### P38 — cgroup seguro · A

Crie escopo de usuário com limites pequenos, observe arquivos de contabilidade
e encerre-o sem tentar provocar OOM.

## Bloco 5 — armazenamento, boot e systemd

### P39 — mapa de armazenamento · A

Desenhe dispositivo, partição, mapeamento, filesystem e ponto de montagem da
raiz. Use identificadores persistentes, não apenas o nome detectado no boot.

### P40 — entrada de montagem · C

Em clone descartável, crie montagem baseada em arquivo-imagem e UUID. Valide a
entrada, simule e confirme antes do reboot.

### P41 — pilha LUKS e LVM · C

Execute o roteiro de armazenamento loop. Em cada etapa, pare e prove a relação
entre a camada criada e a anterior.

### P42 — crescimento · C

Cresça o volume e depois o filesystem da prática. Explique a ordem e não tente
redução.

### P43 — anatomia do boot · A

Desenhe firmware, entrada, bootloader, kernel, initramfs, raiz e PID 1 da VM.
Associe um arquivo ou comando de evidência a cada seta.

### P44 — rescue temporário · C

Inicie uma vez em target de resgate por edição temporária da entrada. Registre
serviços e mounts disponíveis e retorne sem persistir a alteração.

### P45 — unit validada · A

Valide as unidades de exemplo, introduza erro em uma cópia e explique a
mensagem. O arquivo original permanece inalterado.

### P46 — timer · A

Calcule próximas execuções de um calendário, aplique atraso aleatório e explique
o comportamento persistente após uma janela perdida.

### P47 — falha de contexto · B

Execute uma tarefa manualmente e depois sob unit com usuário e ambiente
restritos. Diagnostique caminho, diretório, permissão e variável.

## Bloco 6 — operação e segurança do host

### P48 — socket local · A

Inicie serviço apenas em loopback, encontre PID e socket e execute healthcheck.
Não altere rota nem firewall; esses assuntos pertencem à trilha de Redes.

### P49 — SSH local · B

Valide host key por console, use chave exclusiva do lab e conecte a localhost.
Remova chave, agente e autorização no teardown.

### P50 — script idempotente · A

Execute sua automação duas vezes. A segunda execução deve produzir o mesmo
estado e explicar claramente que não havia mudança.

### P51 — interrupção e lock · A

Execute duas instâncias e interrompa uma durante operação segura. Prove que não
sobrou arquivo parcial nem concorrência silenciosa.

### P52 — linha do tempo · A

Provoque falha de unit em cópia, correlacione journal, horário, status e última
mudança. Corrija somente a causa demonstrada.

### P53 — backup restaurado · A

Use o exemplo versionado, verifique checksum e restaure em destino vazio.
Meça RPO e RTO observados.

### P54 — baseline de hardening · B

Inventarie pacotes, units, contas, privilégios, montagens e controles MAC.
Escolha três mudanças de alto retorno, cada uma com teste e rollback.

### P55 — sandbox incremental · B

Acrescente uma diretiva systemd de isolamento por vez à unit didática. Execute
teste funcional após cada passo e registre incompatibilidades.

### P56 — container explicado · A

Mapeie namespaces, cgroup, mounts, UID, capabilities e seccomp de uma carga
rootless. Declare explicitamente o kernel compartilhado.

## Bloco 7 — kernel, dispositivos e desempenho

### P57 — syscall no código · A

Trace o copiador em C e associe open, read, write e close às linhas do código.
Inclua comportamento de leitura curta, escrita parcial e EINTR.

### P58 — VFS e durabilidade · A

Desenhe dentry, inode, objeto file, page cache e filesystem para uma gravação.
Explique por que retorno de write não equivale automaticamente a persistência.

### P59 — dispositivo ao driver · A

Escolha dispositivo não essencial e ligue barramento, sysfs, driver, módulo e
nó. Saneie serial antes de registrar.

### P60 — metadados de módulo · C

Compile o módulo didático e leia licença, vermagic e dependências. Carregamento
é opcional e somente no clone descartável.

### P61 — ferramenta de observação · A

Para uma pergunta de CPU, uma de syscall e uma de kernel, escolha entre log,
strace, perf e tracepoint. Justifique overhead e privilégio.

### P62 — baseline de desempenho · A

Defina carga e SLO, colete intervalos e localize saturação. Não ajuste parâmetro
até escrever resultado que falsificaria a hipótese.

### P63 — sessão desktop · A

Mapeie login, sessão, compositor, áudio e aplicação. Teste perfil temporário e
compare logs do usuário e do sistema.

### P64 — runbook executável · B

Entregue operação da unit a outra pessoa: saúde, logs, mudança, rollback e
restore. Toda pergunta necessária vira uma melhoria antes do capstone.

## Checklist antes dos laboratórios avaliativos

- [ ] Sei prever o resultado antes de executar.
- [ ] Minhas evidências contêm versões e horário, mas não segredos.
- [ ] Consigo distinguir leitura, mudança reversível e destruição.
- [ ] Uso VM descartável para disco, boot, módulo e kernel.
- [ ] Toda mudança administrativa tem console, snapshot, teste e rollback.
- [ ] Consigo explicar o mecanismo sem depender do nome do comando.
