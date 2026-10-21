# Laboratórios do Linux avançado

## Regras

- Não conecte as VMs a redes.
- A e B podem ocorrer na VM de análise; C e D somente na sacrificável.
- Crie snapshot antes de C/D e valide console.
- Use somente processos, imagens e dispositivos virtuais do laboratório.
- Registre comando, versão, código de saída, dado bruto e reversão.
- Pare se o alvo resolvido não for exatamente o previsto.

## Sequência

| Lab | Pré-requisitos | Classe | Resultado |
|-----|----------------|--------|-----------|
| [Fonte, ABI e ELF](01-fonte-abi-elf.md) | capítulos 00–06 e exemplos | A/B | mapa de uma syscall e laudo ELF |
| [Scheduler, memória e PSI](02-scheduler-memoria.md) | Lab 01 e capítulos 07–12 | A/C | experimento controlado com percentis |
| [VFS, filesystems e bloco](03-filesystems-bloco.md) | Lab 02 e capítulos 13–18 | B/C | matriz de consistência em imagens |
| [Boot, systemd e cgroups](04-boot-systemd-cgroups.md) | Lab 03 e capítulos 19–21 | C/D | entrada paralela e serviço limitado |
| [Tracing e eBPF local](05-tracing-ebpf.md) | Lab 04, capítulos 22–24 e guia | C | trace curto com teardown comprovado |
| [Depuração e kdump](06-debug-kdump.md) | Lab 05 e capítulos 25–26 | C/D | causa raiz user/kernel |
| [KVM/QEMU offline](07-kvm-offline.md) | Lab 06 e capítulos 27–29 | B/C | VM sem NIC com overlay descartável |
| [Pacote e imagem reproduzível](08-distribuicao.md) | Lab 07 e capítulos 30–33 | B | hashes, SBOM e diffoscope |
| [Projeto final](09-projeto-final.md) | Labs 01–08, práticas, capítulo 34 e projeto de referência | B–D | appliance offline defendido |

## Regra de aprovação

Cada lab exige artefato funcional, dados brutos, interpretação, reversão e defesa
das perguntas. Um comando que termina com zero não aprova sozinho. O próximo gate
só fica disponível quando todos os pré-requisitos acima estiverem marcados como
concluídos na aplicação local.

## Template de evidência

```markdown
# EXP-ID — pergunta

- Ambiente:
- Kernel/config:
- Snapshot:
- Hipótese:
- Controle negativo:
- Comandos:
- Dados brutos e SHA-256:
- Resultado:
- Limitações:
- Reversão:
```

## Cleanup mínimo

Ao final, prove que não restaram:

- mounts ou loop devices do lab;
- tracing/eventos habilitados;
- programas BPF, maps ou links fixados;
- unidades transitórias;
- processos QEMU;
- overlays necessários para dados que deveriam ser preservados.

O cleanup é parte da nota, não um detalhe operacional.
