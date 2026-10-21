# Respostas comentadas e critérios

Consulte somente depois de tentar. Muitas atividades não possuem uma única
saída; estas respostas mostram o raciocínio que deve aparecer.

## Distribuições

**Notebook antigo:** uma distro leve não é apenas ISO pequena. Avalie driver de
Wi-Fi/GPU, RAM, ambiente desktop, ciclo de suporte e atualização. Debian com
Xfce pode ser boa escolha quando o hardware é suportado; Alpine desktop exige
mais integração e não é automaticamente melhor.

**Servidor de banco:** previsibilidade, suporte, filesystem, vendor e equipe
pesam mais que pacote mais novo. Debian stable, Ubuntu LTS ou RHEL/derivado podem
ser respostas corretas quando justificadas.

**Container pequeno:** Alpine reduz tamanho, mas musl/BusyBox podem exigir
adaptação. Uma imagem slim baseada na mesma família do aplicativo pode ser
menor operacionalmente por evitar incompatibilidades.

## Arquivos e links

Hard links compartilham inode. Se `base` é removido, `hard` ainda referencia os
dados e o contador cai. O symlink cujo texto era `base` fica quebrado. Se um
novo `base` for criado, o symlink passa a resolvê-lo, mas `hard` continua no
inode antigo.

`mv novo base` no mesmo filesystem substitui a entrada de diretório; processos
com o inode antigo aberto continuam lendo o antigo. Editar in-place preserva o
inode. Essa diferença explica reloads e arquivos de log removidos ainda abertos.

## Permissões

Para acessar `/a/b/c`, o processo precisa `x` nos diretórios do caminho e a
permissão apropriada no alvo. `r` em `/a/b` lista nomes; sem `x`, não acessa os
inodes por esses nomes. Com `x` sem `r`, um nome conhecido pode ser acessado,
mas o diretório não pode ser listado.

Com base `0666` e umask `027`, arquivo comum recebe `0640`. Diretório parte de
`0777` e recebe `0750`. A operação correta é `base & ~umask`, não subtração
decimal.

## Pipeline e status

Sem `pipefail`, o status de `grep ERROR arquivo-inexistente | wc -l` costuma ser
o de `wc`, que conseguiu contar zero linhas. O diagnóstico aparece em stderr,
mas automação que olha apenas `$?` pode aceitar. Com pipefail, o pipeline
propaga falha de um componente, sujeito à semântica da shell.

## Processos

Um arquivo removido permanece enquanto um descritor o referencia. `lsof +L1`
mostra link count menor que um; reiniciar/reabrir de forma controlada libera
blocos. Matar processo sem entender pode causar indisponibilidade.

Zombie já terminou e não recebe um sinal útil. O pai precisa chamar `wait`; se o
pai terminar, um reaper coleta o status. Muitos zombies indicam bug/supervisão.

## Memória

VIRT inclui reservas, bibliotecas e mapeamentos; não representa RAM consumida.
RSS conta páginas residentes e pode duplicar compartilhadas entre processos.
PSS rateia compartilhamento. `MemAvailable` é mais útil que `MemFree` para
capacidade imediata porque parte do cache é recuperável.

Swap ocupada pode conter páginas frias e não indicar pressão atual. Procure
`si`/`so`, PSI, faults, latência e OOM no intervalo.

## `df` diferente de `du`

Possíveis causas: arquivo removido aberto, blocos reservados, snapshot,
metadados, sparse/compressão, permissão impedindo `du` ou dados sob um mount.
O diagnóstico usa `lsof +L1`, mounts, privilégio equivalente e ferramentas do
filesystem.

## systemd

`enabled` instala links/dependências para ativação futura. `active` descreve o
estado atual. `start` não habilita e `enable` normalmente não inicia sem `--now`.
Uma unit oneshot pode estar `active (exited)`; um socket pode ativar serviço sob
demanda.

`After=network.target` ordena duas units se ambas forem ativadas; não testa DNS,
rota externa ou aplicação remota. Serviços robustos usam retry/backoff e uma
dependência coerente com o gerenciador de rede.

## Conectividade local e handoff

Um listener local deve ser associado ao PID, à identidade, à unit e a um teste
funcional. Se não existe, o diagnóstico permanece no processo e na
configuração. Se loopback funciona e outro host falha, registre horário, origem,
destino, socket esperado e mensagem exata e continue nos módulos 14 a 18.

Getent representa a resolução via NSS usada por muitas aplicações. Ferramentas
que consultam DNS diretamente respondem a outra pergunta; essa diferença será
aprofundada na trilha de Redes.

## Backup

RAID mantém serviço após algumas falhas de membro; snapshot congela referência
local; replicação copia estado, inclusive corrupção; backup retém pontos
recuperáveis independentes. Uma solução pode combinar os quatro.

## Avaliação

Uma resposta é aceita quando:

1. declara suposições e versões;
2. coleta estado antes;
3. usa alvo exato e privilégio mínimo;
4. prevê falha e rollback;
5. valida resultado observável;
6. explica mecanismo, não apenas comando.
