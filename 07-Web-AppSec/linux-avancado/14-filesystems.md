# 14 — ext4, XFS, Btrfs e consistência

## Objetivos

- comparar filesystems por modelo, não por ranking genérico;
- entender journaling, copy-on-write, checksums e allocation groups;
- projetar testes de falha com imagens descartáveis;
- separar snapshot, scrub, redundância e backup.

## Perguntas de escolha

1. Qual é o tamanho e o padrão de arquivos?
2. Há muitas criações, renames ou fsyncs?
3. Snapshot e send/receive são requisitos?
4. Qual ferramenta de repair existe e quais são suas garantias?
5. Como a falha de energia do dispositivo é tratada?
6. Quais versões de kernel e user space serão mantidas?

## ext4

Usa journaling de metadados, extents, alocação atrasada e grupos de blocos.
Modos de dados mudam relação entre dados e journal. É uma escolha geral madura,
mas sua robustez não remove a necessidade de protocolo correto de `fsync`.

## XFS

Divide trabalho em allocation groups, escala para paralelismo e arquivos grandes
e possui ferramentas específicas de inspeção/repair. O log protege atualizações
de metadados. Grow é comum; shrink pode não estar disponível na combinação em
uso, portanto planeje layout.

## Btrfs

Usa copy-on-write, checksums de dados e metadados, subvolumes, snapshots, scrub e
send/receive. CoW pode fragmentar workloads com sobrescrita aleatória. NOCOW muda
garantias; RAID profiles e recuperação precisam ser avaliados na versão real.

Checksum detecta divergência. Correção automática exige outra cópia válida.

## Consistência e durabilidade

Crash consistency preserva estruturas após parada abrupta; application
consistency preserva invariantes da aplicação. Um snapshot instantâneo de banco
em escrita pode ser crash-consistent, mas não conter uma transação lógica
completa sem coordenação.

## Invariantes e modelos de falha

Antes de comparar desempenho, defina o que precisa sobreviver a crash: conteúdo
do arquivo, nome novo, ausência do nome antigo, ordem entre duas atualizações ou
uma transação da aplicação. Journaling normalmente protege metadados e replay;
não transforma várias operações da aplicação numa transação única. Copy-on-write
evita sobrescrever alguns blocos em uso, mas ainda depende de ordenação,
superblocks, flushes e implementação correta.

Teste falhas em cópias de imagens e registre o ponto de interrupção. Um processo
morto, um guest desligado sem shutdown e uma perda de energia do dispositivo são
modelos distintos. A VM pode validar protocolo de software, mas não prova que
firmware, cache ou controlador físico respeitam flush.

## Operação e reparo

Scrub lê e verifica checksums; com redundância válida pode reparar uma cópia.
`fsck` ou ferramentas específicas verificam estruturas e podem alterar estado.
Execute primeiro modo somente leitura em cópia. “Filesystem montou” não prova
consistência completa, e “repair terminou” não prova que todos os dados da
aplicação continuam semanticamente corretos.

Snapshots compartilham destino e domínio de falha. Backup possui cópia separada,
política de retenção e restauração testada. Mirror melhora disponibilidade diante
de falha de dispositivo, mas replica exclusão e corrupção autorizada. Checksum
detecta bytes divergentes, mas precisa de referência ou réplica para corrigi-los.

## Falhas comuns

- escolher filesystem por benchmark genérico;
- comparar opções de mount diferentes sem registrá-las;
- tratar snapshot como backup;
- executar repair destrutivo na única imagem;
- assumir que checksum implica correção automática;
- confundir crash consistency com consistência da aplicação.

## Laboratório B/C

Use somente arquivos de imagem:

```bash
truncate -s 2G fs-lab.img
sudo losetup --find --show fs-lab.img
```

O comando privilegiado é executado apenas na VM e o device retornado deve ser
registrado explicitamente. Nunca substitua por glob de `/dev`.

Para cada filesystem:

1. formate a imagem;
2. registre features e mount options;
3. execute carga idêntica;
4. sincronize e desmonte;
5. use a ferramenta de check em modo não destrutivo;
6. destrua o loop device e a imagem.

## Exercícios

1. Defina invariantes de uma atualização de dois arquivos e indique onde a
   aplicação precisa de protocolo adicional.
2. Compare ext4, XFS e Btrfs para dois workloads opostos sem declarar vencedor
   universal.
3. Modele processo morto, queda do guest e falha elétrica; liste o que cada teste
   pode ou não demonstrar.
4. Desenhe snapshot, mirror, checksum e backup contra quatro falhas diferentes.

## Checklist de domínio

- [ ] Escolho filesystem a partir de carga, operação e recuperação.
- [ ] Distingo journaling, CoW, checksum, scrub e repair.
- [ ] Testo apenas cópias e imagens descartáveis.
- [ ] Não confundo crash consistency com transação da aplicação.
- [ ] Explico por que snapshot, mirror, checksum e backup não são equivalentes.

Fontes: [ext4](https://docs.kernel.org/filesystems/ext4/index.html),
[XFS](https://docs.kernel.org/filesystems/xfs/index.html) e
[Btrfs](https://btrfs.readthedocs.io/).
