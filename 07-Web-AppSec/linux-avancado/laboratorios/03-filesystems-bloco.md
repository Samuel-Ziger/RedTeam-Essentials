# Lab 03 — VFS, filesystems e bloco

**Classe:** B/C. **Duração:** 18–24 h.

## Pré-requisitos e gate

Conclua o Lab 02 e os capítulos 13–18. Tire snapshot, abra console e inventarie
loops, mappings e mounts antes de criar qualquer recurso. Todos os paths e
devices retornados são copiados para o caderno; não use glob para identificá-los.

## Ambiente

Crie três arquivos de imagem esparsos na VM sacrificável. Resolva cada um para
loop device separadamente e registre a associação. Nunca use disco real.

## Matriz

Compare ext4, XFS e Btrfs com a mesma capacidade e quatro workloads locais:

- criação de muitos arquivos pequenos;
- escrita sequencial de arquivo grande;
- sobrescrita aleatória limitada;
- protocolo temp + `fsync` + rename + `fsync` de diretório.

Registre features, mount options, tempo, percentis, bytes, syscalls e
`/proc/diskstats`. Cache frio é opcional e deve ser obtido por remontagem da
imagem, não por `drop_caches` global.

Fixe tamanho de bloco, número de arquivos, profundidade, duração e seed. Registre
versão das ferramentas, features do filesystem e opções efetivas de mount.
Apresente throughput junto com p50/p95/p99 e erro. Um ranking sem workload e
protocolo não será aceito.

## Protocolo de durabilidade

Implemente o caso temp + `fsync` + rename + `fsync` de diretório e injete
falha entre etapas usando cópias da imagem. Declare invariantes: saída antiga
completa ou nova completa, nunca conteúdo parcial. Compare crash do processo com
parada do guest e deixe explícito que a VM não reproduz toda falha de energia de
um dispositivo físico.

## Camadas e diagnóstico

Desenhe VFS, page cache, filesystem, bio, request, driver e device virtual.
Relacione uma métrica a cada camada. Explique por que `fsync` concluído depende
de flush abaixo e por que diskstats do guest não mede a fila do host.

Opcionalmente componha thin volume somente sobre loops do laboratório. Monitore
data e metadata separadamente e pare muito antes do limite. Este extra não pode
alterar os três casos base.

## Consistência

Use cópia do arquivo de imagem para simular parada em pontos definidos. Rode
ferramentas de check primeiro em modo não destrutivo. Não prometa que desligar
bruscamente uma VM modela toda falha elétrica de SSD real.

Execute scrub ou check somente em cópia e primeiro no modo não destrutivo.
Preserve imagem anterior, ferramenta, código de saída e arquivos afetados.
“Repair terminou” não demonstra consistência lógica da aplicação.

## Cleanup

1. pare cargas;
2. sincronize quando o cenário exigir;
3. desmonte paths explícitos;
4. remova mappings Device Mapper, se houver;
5. destaque loops;
6. compare `losetup --list` ao inventário inicial.

## Entrega

Matriz de escolha por workload, laudo de consistência e explicação de por que
benchmark na VM não generaliza automaticamente ao hardware.

Inclua protocolo de durabilidade, inventário antes e depois, hashes das imagens
de falha e decisão por workload. A aprovação exige diferenciar snapshot, mirror,
checksum e backup.

## Perguntas para defesa

- Por que unlink não libera um arquivo ainda aberto?
- Como queue depth aumenta vazão e piora cauda?
- Qual diferença entre atomicidade de rename e persistência?
- Que evidência prova que o cleanup removeu todas as camadas?
