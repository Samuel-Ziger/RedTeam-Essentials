# Laboratório C03 — módulo, tracing e fallback de kernel

> Somente VM descartável. Tire snapshot e confirme kernel anterior no menu.

## Parte 1 — configuração e interfaces

```bash
uname -a
cat /proc/cmdline
cat /sys/kernel/security/lsm 2>/dev/null
grep -E '^(NoNewPrivs|Seccomp|Cap)' /proc/self/status
zcat /proc/config.gz 2>/dev/null | head || head "/boot/config-$(uname -r)"
```

Explique o que é ABI de user space e por que API interna de módulo pode mudar.

## Parte 2 — compilar o módulo

Instale headers exatamente da release em execução pelo gerenciador da distro.

```bash
cd exemplos/kernel
make
modinfo ./hello_safe.ko
```

Confira licença, vermagic, assinatura e dependências. A compilação é suficiente
para o curso automatizado.

## Parte 3 — carregar opcionalmente

Somente se a VM estiver isolada, o snapshot funcionar e Secure Boot/política
permitirem:

1. abra `journalctl -kf` em um console;
2. confirme que o módulo apenas registra init/exit;
3. use o caminho exato para carregar;
4. verifique `lsmod` e mensagem;
5. remova e confira exit;
6. execute `make clean`.

Não configure autoload. Se houver erro de assinatura/vermagic, explique e pare;
não desative Secure Boot como atalho.

## Parte 4 — tracing

Execute o exemplo de syscalls com:

```bash
strace -f -tt -T -e trace=openat,read,write,close ./syscalls origem destino
perf stat -- ./memoria 8
```

Se `trace-cmd` estiver disponível, registre somente o evento de exec por poucos
segundos. Compare overhead e detalhe de strace, perf e tracepoint.

## Parte 5 — fallback

Instale, pelo repositório da distro, um segundo kernel suportado sem remover o
atual. Confirme arquivos, initramfs e entrada. Reinicie, escolha-o e depois volte
ao original. Não compile um kernel completo apenas para cumprir esta parte.

## Critério

Entregue matriz ferramenta × pergunta × overhead × privilégio e prove que
consegue voltar ao kernel anterior sem apagar o novo durante diagnóstico.
