# 26 — Compilar, observar e depurar o kernel

## Objetivos

- distinguir kernel da distribuição, mainline, stable e longterm;
- reproduzir configuração e artefatos de build em VM descartável;
- escolher log, tracepoint, perf, ftrace, eBPF ou debugger por pergunta;
- testar nova entrada mantendo kernel anterior e plano de recuperação.

## Por que compilar

Para uso normal, prefira o kernel assinado e testado pela distribuição.
Compile para aprender, desenvolver driver, testar correção ou atender requisito
mensurável. Um kernel menor não é automaticamente mais rápido ou seguro; remover
driver de storage pode impedir boot.

Todo este capítulo usa VM descartável com console e snapshot.

## Obter e autenticar a fonte

Use pacote-fonte da distro quando deseja reproduzir seus patches/configuração.
Use kernel.org e verifique assinatura quando estuda upstream. Registre tag,
commit, chave, configuração e toolchain.

```bash
git clone --depth 1 --branch TAG_OFICIAL https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git
cd linux
git log -1 --show-signature
```

Substitua `TAG_OFICIAL` por tag verificada; clone raso limita histórico e não é
adequado para bisect.

## Configuração

```bash
cp "/boot/config-$(uname -r)" .config
make olddefconfig
make menuconfig
```

`olddefconfig` aceita defaults para opções novas. `localmodconfig` remove
módulos que não estão carregados no momento e pode excluir hardware necessário
no próximo boot; use apenas com inventário e fallback.

Opções importantes de lab incluem debug symbols, frame pointers/BTF conforme
ferramentas, sanitizers em builds específicos e drivers da raiz embutidos ou no
initramfs.

## Build reproduzível e empacotado

```bash
make -j"$(getconf _NPROCESSORS_ONLN)"
make modules
```

Prefira o alvo de pacote recomendado pela distro (`bindeb-pkg`, RPM tooling ou
equivalente) em vez de copiar arquivos manualmente. Guarde `.config`, logs,
versão do compilador e artefatos. Instalação deve adicionar entrada nova sem
remover o kernel funcional.

Antes de reiniciar:

1. confirme kernel, módulos e initramfs da mesma release;
2. confira driver do root, controlador, filesystem e criptografia;
3. valide espaço em `/boot`/ESP;
4. mantenha entrada anterior selecionável;
5. habilite console serial da VM;
6. defina timeout/rollback manual.

## Logs e níveis

```bash
journalctl -k -b
dmesg --level=emerg,alert,crit,err,warn
cat /proc/sys/kernel/printk
```

`dmesg` pode ser restrito. Preserve timestamp/boot ID. Repetição de mensagem é
sintoma; busque o primeiro erro e evento anterior.

## Symbols, stack traces e debug info

```bash
grep ' T ' /proc/kallsyms | head 2>/dev/null
file "/boot/vmlinuz-$(uname -r)"
```

KASLR altera endereços; debug symbols e binário exatos permitem simbolizar.
Pacotes de debug da distro evitam build manual. Stack trace mostra caminho
observado, não necessariamente causa raiz.

## ftrace e tracefs

```bash
findmnt -t tracefs 2>/dev/null
sudo trace-cmd record -e sched:sched_process_exec -- sleep 1
sudo trace-cmd report
```

Use evento e janela restritos. Tracing pode gerar muito dado e alterar timing.
Não habilite function graph global em produção sem estimar custo.

## perf e eBPF

`perf stat` mede contadores; `perf record/report` amostra stacks. eBPF permite
programas verificados em hooks para rede, observabilidade e segurança. O
verificador reduz riscos, mas eBPF ainda é interface privilegiada e sensível;
políticas da distro podem restringi-lo.

```bash
perf stat -- sleep 1
bpftool feature probe 2>/dev/null | head
bpftrace -l 'tracepoint:syscalls:sys_enter_*' 2>/dev/null | head
```

Neste curso, eBPF é somente observabilidade sobre processos do lab. Nada de
ocultar atividade, interceptar credenciais ou manter persistência.

## Dynamic debug e fault injection

Dynamic debug ativa mensagens de sites preparados. Fault injection testa
tratamento de erro. Ambos podem degradar ou derrubar o sistema; use kernel de
teste, carga sintética e documentação exata. O curso os explica, mas não os
ativa automaticamente.

## Panic, pstore e kdump

- pstore pode preservar logs em armazenamento de firmware/ramoops;
- kdump reserva memória para iniciar capture kernel e salvar vmcore;
- `crash`/GDB analisam dump com `vmlinux` e debug info correspondentes.

Planeje armazenamento e dados sensíveis: vmcore pode conter todo segredo em
RAM. Testar kdump causa crash deliberado; faça somente em clone isolado, com
autorização e sem dados reais.

## Regressão e bisect

Se versão boa e ruim são conhecidas, `git bisect` reduz o conjunto de commits.
O teste precisa ser determinístico e cada kernel precisa bootar. Primeiro
reproduza, remova módulos externos, confira taint, hardware e configuração.

Relato de qualidade inclui:

- release/commit e `.config`;
- hardware/VM e firmware;
- comando/reprodutor mínimo;
- resultado esperado/obtido;
- primeiro kernel ruim e último bom;
- logs completos e taint;
- tentativa com kernel upstream/distro relevante.

## Exercícios

1. Identifique origem, configuração, assinatura e ciclo de suporte do kernel em
   execução usando fontes da distribuição e do projeto.
2. Compile apenas o módulo didático, examine seus metadados e explique por que
   sucesso de compilação não autoriza carregamento.
3. Construa uma matriz ferramenta, pergunta, privilégio, overhead, risco e
   duração máxima de coleta.
4. Documente o caminho de fallback para kernel anterior e demonstre-o em VM
   sem remover entradas funcionais.

## Checklist de domínio

Consigo construir um kernel como pacote, manter fallback, observar um evento
com ferramenta proporcional e produzir relato reproduzível sem experimentar em
host de trabalho.
