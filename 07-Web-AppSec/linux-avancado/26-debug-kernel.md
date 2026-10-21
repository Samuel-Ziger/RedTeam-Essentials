# 26 — Oops, panic, kdump, crash e drgn

## Objetivos

- distinguir warning, oops, panic, hang e lockup;
- preservar logs e vmcore;
- simbolizar stack com build correspondente;
- investigar sem reiniciar repetidamente o host.

## Tipos de falha

- **WARN:** invariante suspeita; o kernel pode continuar;
- **oops:** exceção em contexto do kernel; tarefa pode morrer e estado ficar degradado;
- **panic:** kernel decide que não pode prosseguir;
- **soft lockup:** CPU ficou tempo excessivo no kernel sem agendar;
- **hard lockup:** CPU deixou de responder até a mecanismos de watchdog;
- **hung task:** tarefa permaneceu bloqueada por tempo configurado.

Depois de oops, continuar usando a máquina pode corromper mais evidência. Colete
e reinicie de forma controlada.

## Primeira leitura

Registre a primeira falha, não apenas mensagens em cascata. Identifique kernel,
taint, CPU, PID/comm, registradores, instruction pointer, call trace e módulos.
Taint sinaliza condições como módulo proprietário ou warning anterior; não é
uma conclusão de causa.

```bash
journalctl -k -b -1 2>/dev/null | tail -n 200
cat /proc/sys/kernel/tainted
```

## Simbolização

Use `vmlinux` não stripado, `.config`, `System.map` e módulos exatamente do
kernel que falhou. KASLR muda endereços; logs e vmcore carregam informação para
relocalização conforme ferramenta e configuração.

`scripts/decode_stacktrace.sh` e `addr2line` ajudam em logs; `crash` e `drgn`
inspecionam estado estruturado em dump ou kernel vivo.

## Kdump

Kdump reserva memória para um crash kernel pequeno. No panic, kexec transfere
controle e o segundo kernel grava `/proc/vmcore`. Se storage, initramfs ou espaço
falharem, o dump é perdido. Teste captura antes de precisar dela.

## Preservação e triagem

A primeira mensagem costuma estar mais próxima da origem que erros em cascata.
Preserve console serial, pstore quando disponível, journal anterior e vmcore.
Registre uptime, taint, cmdline, config, módulos e build IDs. Não carregue módulo
ou repita panic para “confirmar” antes de salvar o estado original.

Leia o relatório em camadas: tipo de exceção, endereço de falha, modo de acesso,
instruction pointer, tarefa/CPU/contexto e call trace. Depois relacione instrução
ao fonte e examine argumentos e lifetime. Um frame no stack mostra participação,
não culpa automática.

## Dump correspondente

`crash` e drgn interpretam estruturas usando tipos e símbolos. Pequena mudança
de config altera layout; backport mantém versão nominal e muda código. Associe
vmcore ao `vmlinux`, módulos e debuginfo daquela build por identificadores e
hashes, não apenas por `uname -r`.

Valide o pipeline de kdump: memória reservada, crash kernel carregado, initramfs
com driver do destino, espaço, timeout e política de retenção. O destino local
deve permanecer gravável quando o kernel principal falha. Core contém memória
sensível e exige controle de acesso.

## Falhas comuns

- analisar a última cascata em vez da primeira falha;
- tratar taint como causa;
- usar símbolos de versão parecida;
- configurar kdump sem executar teste de captura;
- manter dump sem proteção ou retenção;
- testar panic no host ou sem console.

## Laboratório D

Somente na VM sacrificável:

1. habilite console serial e snapshot;
2. instale/configure kdump conforme a distribuição;
3. confirme reserva `crashkernel`;
4. acione o mecanismo de teste documentado pela distribuição;
5. preserve vmcore, kernel e symbols;
6. encontre panic task e backtrace com `crash` ou `drgn`;
7. restaure snapshot.

## Exercícios

1. Anote um oops público benigno identificando cada campo sem atribuir causa além
   da evidência.
2. Verifique o par build ID/hash de vmcore, `vmlinux` e módulos.
3. Execute checklist de kdump até a captura oficial na VM D e valide espaço e
   leitura do dump.
4. Produza triagem que separa primeira falha, efeito secundário, hipótese e dado
   ainda ausente.

## Checklist de domínio

- [ ] Distingo WARN, oops, panic, hung task e lockups.
- [ ] Preservo primeira falha e artefatos exatos da build.
- [ ] Interpreto taint como contexto, não veredito.
- [ ] Testo kdump antes de depender dele.
- [ ] Nunca acione falha deliberada fora da VM D.

Fonte: [kernel debugging](https://docs.kernel.org/process/debugging/index.html).
