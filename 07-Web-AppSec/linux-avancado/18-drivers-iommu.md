# 18 — Dispositivos, drivers, DMA e IOMMU

## Objetivos

- entender device/driver/bus e binding;
- acompanhar descoberta, probe, remove e power management;
- explicar DMA, cache coherence e IOMMU;
- escrever um módulo didático sem tocar hardware real.

## Driver model

O kernel representa dispositivos e drivers em uma hierarquia ligada por buses.
Quando identificadores combinam, o core tenta `probe`; remoção precisa encerrar
I/O, impedir novos acessos e liberar recursos na ordem inversa. `devm_*` ajuda no
lifetime vinculado ao device, mas não resolve protocolos concorrentes.

```bash
find /sys/bus -maxdepth 2 -type d | head
readlink /sys/class/block/*/device 2>/dev/null | head
udevadm info --query=all --name=/dev/null
```

## Sysfs, uevent e udev

Sysfs exporta objetos e atributos do kernel; não é banco permanente. Uevents
notificam user space, e udev aplica políticas de nome, permissão e links. Uma
regra deve usar atributos estáveis e ser testada com evento simulado antes de
afetar a VM.

## DMA

Dispositivos podem transferir dados diretamente para memória. Drivers usam a DMA
API para obter endereços apropriados ao device, mapear buffers e sincronizar em
arquiteturas não coerentes. Endereço virtual de CPU, físico e DMA address não são
intercambiáveis.

## IOMMU

A IOMMU traduz endereços de DMA e limita quais páginas um dispositivo alcança.
Isso viabiliza isolamento e passthrough, mas a granularidade real depende de
grupos e topologia. ACS e firmware influenciam isolamento; forçar separação
artificial pode criar uma fronteira falsa.

```bash
find /sys/kernel/iommu_groups -maxdepth 2 -type l 2>/dev/null
dmesg | grep -Ei 'iommu|dmar|amd-vi' | head
```

Não configure passthrough de hardware no computador principal. O curso usa
somente inspeção e dispositivos virtuais.

## Módulo didático

O exemplo [`rte_seqfile.c`](exemplos/kernel/rte_seqfile.c) cria uma entrada
somente leitura em procfs e demonstra init, exit, seq_file e cleanup. O teste
automático não compila nem carrega o módulo. Faça isso apenas na VM D com headers
correspondentes ao kernel em execução.

## Probe, erro e remoção

Probe adquire recursos em estágios: habilita device, mapeia registers, configura
DMA, registra IRQ e publica interfaces. Cada falha precisa desfazer somente o que
foi adquirido, na ordem inversa. Recursos `devm_*` automatizam parte do cleanup
quando o device é removido, mas trabalhos, timers e acessos de user space ainda
precisam ser interrompidos antes que memória desapareça.

Remove correto impede novas operações, marca estado, acorda esperadores, cancela
trabalho assíncrono, sincroniza IRQ e DMA e só então libera. Hot-unplug transforma
esse caminho em operação comum, não exceção teórica. Teste unbind apenas em
dispositivo virtual descartável com console disponível.

## DMA e coerência

A DMA API retorna endereço compreendido pelo device e pela IOMMU. Mappings
coherent e streaming possuem contratos distintos; o segundo pode exigir sync
entre ownership de CPU e device. Mesmo numa arquitetura coerente, barriers e
ordem de descriptors continuam relevantes. Nunca derive DMA address de
`virt_to_phys` como regra geral.

IOMMU limita DMA por domínio, mas isolamento efetivo depende do grupo, firmware,
ACS e dispositivos que compartilham funções. Passthrough transfere superfície do
driver para guest e exige reset seguro. O laboratório apenas inspeciona essa
topologia.

## Falhas comuns

- publicar interface antes de concluir inicialização;
- liberar memória antes de cancelar IRQ, timer ou work;
- misturar endereço virtual, físico e DMA;
- assumir coerência em toda arquitetura;
- considerar grupo IOMMU uma propriedade puramente de software;
- carregar módulo sem headers e vermagic correspondentes.

## Prática C/D

1. Trace o binding de um dispositivo virtual de bloco.
2. Relacione modalias, módulo e driver em sysfs.
3. Compile o módulo fora da árvore.
4. Revise fonte e `modinfo` antes de carregar.
5. Leia `/proc/rte_advanced`, descarregue e confirme cleanup.

## Exercícios

1. Desenhe probe em cinco estágios com unwind de cada ponto de falha.
2. Modele remove concorrente com I/O, IRQ e workqueue e determine a ordem segura.
3. Diferencie endereços virtual, físico, DMA e IOVA para um buffer.
4. Inspecione apenas a topologia de um dispositivo virtual e explique por que
   grupo compartilhado enfraquece passthrough isolado.

## Checklist de domínio

- [ ] Entendo binding entre bus, device e driver.
- [ ] Projeto probe e remove com lifetime e unwind completos.
- [ ] Uso DMA API em vez de converter endereços manualmente.
- [ ] Interpreto grupo IOMMU como limite dependente da topologia.
- [ ] Só carrego módulo didático na VM D e com build correspondente.

Fonte: [driver model](https://docs.kernel.org/driver-api/driver-model/index.html).
