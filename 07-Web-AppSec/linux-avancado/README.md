# Linux avançado — guia de estudo

Esta é a raiz didática do [módulo 07](../README.md). O módulo 06 ensinou a
usar e administrar Linux; aqui o sistema deixa de ser uma caixa-preta.

## Modelo mental

```text
programa ELF → loader/libc → ABI/syscall → subsistema do kernel
                                      │
             scheduler · MM · VFS · block · drivers · LSM · KVM
                                      │
                        hardware, firmware e dispositivos

observação: /proc · /sys · perf · ftrace · tracepoints · eBPF
controle:     systemd · cgroup v2 · seccomp · capabilities · verity
```

## Como estudar

Para cada capítulo, produza quatro itens:

1. um diagrama autoral do caminho percorrido;
2. uma previsão escrita antes do experimento;
3. a evidência bruta com versão do kernel e comandos;
4. uma conclusão que separe fato, inferência e dúvida.

Depois de cada par de capítulos, execute as atividades correspondentes no
[caderno de 72 práticas](CADERNO-PRATICAS.md). Os
[nove laboratórios](laboratorios/README.md) são gates: o seguinte só abre quando
o anterior e seus capítulos forem concluídos. Use o
[guia de experimentos e diagnóstico](GUIA-EXPERIMENTOS-DIAGNOSTICO.md) sempre
que a hipótese atravessar mais de um subsistema.

Não memorize nomes de estruturas internas. Aprenda a encontrá-las no commit e
na configuração que você realmente está estudando. A ABI de user space busca
estabilidade; APIs internas do kernel não oferecem a mesma promessa.

## Regra de escopo

Este curso não ensina redes. Um recurso que também possa ser usado com rede
aparece apenas quando o experimento é estritamente local. Não use interfaces,
endereços, pacotes, roteamento ou filtros de tráfego nos laboratórios.

## Primeira coleta

Execute como usuário comum e arquive o resultado:

```bash
uname -a
cat /proc/version
cat /proc/cmdline
zcat /proc/config.gz 2>/dev/null | head || true
systemd-detect-virt 2>/dev/null || true
findmnt -no FSTYPE,OPTIONS /
cat /sys/kernel/security/lsm 2>/dev/null || true
cat /sys/fs/cgroup/cgroup.controllers 2>/dev/null || true
```

Repita no projeto final. Diferenças fazem parte da análise; não devem ser
apagadas para fazer o resultado “bater”.

## Validação local

```bash
bash testar-curso.sh
```

O executor compila apenas exemplos de user space, usa diretório temporário e
não carrega módulo, eBPF, VM ou unidade systemd.

O [offline appliance de referência](projetos/offline-appliance/README.md) liga os
exemplos ao projeto final sem fornecer uma solução opaca ou exigir rede.
