# 29 — Linux embarcado, Device Tree e Buildroot

## Objetivos

- decompor boot de uma placa em firmware, bootloader, kernel, DT e rootfs;
- ler e validar Device Tree;
- fazer cross-build de um sistema mínimo;
- planejar atualização offline, rollback e recuperação.

## O que muda no embarcado

Recursos, armazenamento, console e ciclo de vida são restritos. A imagem pode ser
imutável, o hardware fixo e o produto mantido por anos. Reproduzibilidade,
licenças, atualização atômica e recovery valem tanto quanto boot inicial.

## Sequência típica

```text
Boot ROM → SPL → bootloader → kernel + DTB + initramfs/rootfs → PID 1
```

A ROM pode carregar um pequeno primeiro estágio para inicializar DRAM. U-Boot
carrega artefatos e argumentos. O Device Tree descreve hardware que não é
autodescoberto; drivers combinam `compatible` e propriedades.

## Device Tree

Um DTS é compilado em DTB. Nodes têm endereço, interrupts, clocks, resets,
regulators e relações por phandles. Binding YAML é o contrato de propriedades.

```dts
example@1000 {
    compatible = "rte,training-device";
    reg = <0x1000 0x100>;
    status = "disabled";
};
```

`status = "disabled"` impede probe até a plataforma fornecer hardware coerente.
Um DT incorreto pode causar acesso a endereço errado; teste em emulação ou placa
de laboratório, nunca em equipamento essencial.

## Buildroot

Buildroot integra toolchain, pacotes, kernel, bootloader e rootfs. Configuração
é o produto; guarde defconfig, overlays, patches e versões. Não use o diretório
de output como fonte manual.

Yocto/OpenEmbedded resolve cenários maiores de distribuição por recipes e layers;
Buildroot é excelente para aprender uma imagem pequena. Escolha pelo produto,
não por moda.

## Atualização A/B offline

Mantenha dois slots assinados, contador de tentativas, health check e recovery
independente. Dados mutáveis devem ter migração reversível ou compatível entre
versões. Uma atualização que regride binário mas não schema não é rollback.

## Contrato entre hardware e software

Kernel, DTB, firmware e placa formam um conjunto versionado. O `compatible`
deve ir do mais específico ao fallback compatível; o driver escolhe dados de
match e interpreta propriedades conforme binding. Endereço, interrupt parent,
clock, reset e regulator incorretos podem produzir falha silenciosa ou acesso ao
hardware errado.

Valide DTS contra schemas com `dtbs_check` quando possível. Warning não deve ser
apagado sem entender se o binding ou a descrição está incorreto. Overlay resolve
algumas variações, mas aumenta combinações e precisa de mesma disciplina de
versão e teste que um DTB completo.

## Imagem como produto

Buildroot gera o conjunto a partir de defconfig, versões, hashes, patches e
overlay. O diretório de output é descartável; mudanças manuais ali desaparecem.
Fixe downloads previamente arquivados, toolchain e locale, gere manifesto e
licenças. Rebuild em diretório limpo demonstra se a configuração realmente
descreve o produto.

Rootfs mínimo reduz superfície e armazenamento, mas precisa incluir diagnóstico
e recovery suficientes. BusyBox combina applets no mesmo binário; habilitar um
applet altera recursos. PID 1 precisa montar pseudo-filesystems, tratar sinais e
reap, ou delegar a init apropriado.

## Update e energia

Escreva somente slot inativo, verifique hash/assinatura antes de marcar candidato
e atualize metadata de boot atomicamente. Simule queda em cada etapa. Recovery
deve ser independente do slot corrompido e acessível por console físico/serial.

## Falhas comuns

- usar DTB de revisão parecida sem confirmar a placa;
- editar output do Buildroot como fonte;
- permitir download não fixado durante o build;
- atualizar bootloader e ambos os slots numa única operação;
- chamar volta do binário de rollback quando schema mudou irreversivelmente;
- remover todas as ferramentas de recuperação em nome do tamanho.

## Prática B

Gere uma imagem QEMU local com Buildroot, console serial e **sem pacotes de rede**.
Inclua o `proc_snapshot` do curso, gere SBOM/lista de pacotes, inicialize, execute
health check e compare hash de dois builds.

## Exercícios

1. Leia um binding YAML e mapeie required, enum, phandle e constraints para um
   node DTS válido.
2. Gere duas vezes uma imagem QEMU offline em diretórios limpos e investigue a
   primeira divergência.
3. Faça inventário do rootfs mínimo e justifique cada ferramenta de diagnóstico.
4. Modele update A/B com queda antes, durante e depois da mudança de slot.

## Checklist de domínio

- [ ] Versiono firmware, kernel, config, DTB e rootfs como conjunto.
- [ ] Valido Device Tree contra binding e hardware correto.
- [ ] Trato defconfig, hashes, patches e overlays como fonte.
- [ ] Projeto update atômico com recovery independente.
- [ ] Não confundo rollback do binário com compatibilidade dos dados.

Fontes: [Buildroot](https://buildroot.org/downloads/manual/manual.html) e
[Devicetree specification](https://www.devicetree.org/specifications/).
