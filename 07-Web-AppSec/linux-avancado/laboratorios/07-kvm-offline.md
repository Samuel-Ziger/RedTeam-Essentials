# Lab 07 — KVM/QEMU offline

**Classe:** B/C. **Duração:** 12–18 h.

## Pré-requisitos e gate

Conclua o Lab 06 e os capítulos 27–29. Registre suporte de virtualização, CPU,
kernel, QEMU, formato da base e espaço disponível. A base deve ser cópia
descartável ou artefato verificável; nenhum comando recebe bloco do host.

## Objetivo

Construir uma VM com console serial, ISO local, overlay qcow2, virtio-blk e
balloon, explicitamente sem dispositivo de rede.

## Procedimento

1. Execute `kvm_probe` e registre API/capabilities.
2. Crie base qcow2 e marque como somente leitura.
3. Crie overlay com backing format explícito.
4. Inicie com `-nic none` e `-nographic`.
5. Instale workload previamente incluído na ISO.
6. Meça TCG e KVM com a mesma carga de CPU.
7. Limite processo QEMU em um scope systemd.
8. Desligue guest, rode `qemu-img check` e descarte overlay.

## Matriz de execução

Execute TCG e KVM com mesma imagem, vCPU, RAM, workload, aquecimento e número de
repetições. Compare resultado funcional, wall clock, task-clock do QEMU, threads
vCPU, switches e RSS/PSS. Não trate a diferença como benchmark de hardware:
firmware, host e virtualização continuam como confundidores.

Audite a linha de comando antes do boot. Use configuração explícita sem NIC,
console serial e paths absolutos para overlay e ISO. Dentro do guest, inventarie
devices e prove ausência de interface ou controlador de rede, sem configurar
rede para realizar a prova.

## Falhas controladas

1. Tente iniciar overlay com backing path ausente em uma cópia e preserve erro.
2. Aplique cgroup estreito, mas seguro, e observe throttling sem OOM do host.
3. Interrompa o guest sem shutdown apenas no overlay descartável e valide imagem.
4. Execute health check local após boot e após recuperação.

Explique quais eventos geram VM exit e por que virtio reduz emulação sem eliminar
driver e protocolo. Balloon depende de cooperação do guest; memória configurada,
RSS e residência não são equivalentes.

## Observações

Registre threads de vCPU, RSS/PSS, cgroup, page faults, CPU e tamanho alocado da
imagem. Explique diferença entre tamanho virtual e físico.

## Restrições

- não use `-net`, `-nic user`, bridge, tap ou libvirt network;
- não use passthrough de dispositivo do host;
- não aponte QEMU a bloco real;
- não delete a base antes de verificar a cadeia.

## Entrega

Comando completo, grafo da cadeia qcow2, comparação TCG/KVM e prova de que a VM
não possui NIC.

Inclua hashes da base, backing chain antes e depois, inventário de recursos,
controle TCG/KVM e cleanup. A aprovação exige que outra pessoa recrie apenas o
overlay e reproduza o boot offline.

## Perguntas para defesa

- Quais responsabilidades pertencem a KVM, QEMU e libvirt?
- Por que snapshot qcow2 não substitui backup?
- O que acontece se a base for alterada?
- Qual métrica pertence ao guest e qual pertence ao processo QEMU?
