# 24 — eBPF e CO-RE para observabilidade local

## Escopo

O programa deste capítulo observa apenas execução de processos locais. XDP, TC,
cgroups de socket e qualquer uso de rede ficam fora deste módulo.

## Objetivos

- entender instruções BPF, verifier, maps, hooks e helpers;
- explicar BTF e CO-RE;
- separar programa no kernel de loader no user space;
- controlar privilégio, volume e lifetime.

## Ciclo de vida

Uma aplicação libbpf normalmente:

1. abre e analisa o objeto ELF BPF;
2. cria maps e aplica relocations;
3. pede ao kernel que verifique e carregue programas;
4. anexa programas a hooks;
5. consome ring buffer/perf buffer ou consulta maps;
6. desanexa e libera recursos.

O verifier explora caminhos e exige acessos provadamente seguros, stack limitada,
loops verificáveis e tipos de ponteiro coerentes. “Rejeitado” significa que a
segurança não foi provada sob as regras, não necessariamente que a intenção era
maliciosa.

## BTF e CO-RE

BTF descreve tipos do kernel. CO-RE grava relocations para que libbpf ajuste
acessos a campos conforme o BTF do alvo. Isso melhora portabilidade, mas não
torna semântica de funções internas uma ABI. Prefira tracepoints quando atendem.

```bash
test -r /sys/kernel/btf/vmlinux && echo BTF=available
bpftool feature probe unprivileged 2>/dev/null || true
bpftool btf dump file /sys/kernel/btf/vmlinux format c 2>/dev/null | head
```

## Maps e eventos

Escolha map por cardinalidade, concorrência, eviction e consumo. Maps per-CPU
reduzem contenção, mas exigem agregação. Ring buffer preserva ordem global entre
CPUs melhor que buffers per-CPU em certos cenários; ambos podem perder dados se
o consumidor atrasar.

Nunca envie strings ou estruturas grandes por evento sem necessidade. Agregue
no kernel e exporte o mínimo.

## Segurança

Carregamento costuma exigir capabilities/privilégio conforme política e sysctl.
Use VM, programa próprio, janela curta e teardown. Não relaxe globalmente a
política do host para fazer um tutorial funcionar.

O exemplo [`exec_counter.bpf.c`](exemplos/bpf/exec_counter.bpf.c) é fonte
didática; o teste automático verifica o arquivo, mas nunca o carrega.

## Como raciocinar com o verifier

O verifier acompanha tipos de registradores, intervalos escalares, bounds de
ponteiros, stack e caminhos possíveis. Cada branch refina o estado; merge de
caminhos pode perder precisão. Um acesso válido para a intenção humana será
rejeitado se o programa não demonstrar limite, inicialização e lifetime pelas
regras reconhecidas. Leia o log desde o primeiro estado divergente, não apenas a
última mensagem.

Helpers têm contrato de tipos e contexto. Um ponteiro retornado por lookup pode
ficar inválido após operação que altera o map; ponteiros de contexto não podem
ser guardados arbitrariamente. Locks BPF, per-CPU maps e atomics resolvem padrões
diferentes. Defina cardinalidade e limite para que input local não esgote memória.

## Portabilidade e lifecycle

CO-RE adapta offsets, tamanhos, existência e variantes de campos descritos por
BTF. Não cria helper ausente, hook inexistente ou semântica equivalente. Use
feature probing e caminhos de fallback. Preserve build ID, BTF do alvo, log do
verifier e versões de clang/libbpf no relatório.

Objetos BPF vivem por descritores e podem persistir quando pinned em bpffs ou
referenciados por link. Cleanup precisa desanexar links, fechar descritores e
remover pins conhecidos. Liste estado antes e depois sem remover programas de
terceiros. O loader deve tratar falha parcial: se o segundo attach falhar, o
primeiro não pode ficar ativo.

## Falhas comuns

- aumentar privilégio do host apenas para carregar exemplo;
- culpar o verifier sem analisar o primeiro acesso não provado;
- usar map sem limite de cardinalidade;
- assumir que CO-RE estabiliza funções internas;
- esquecer pin ou link depois do processo sair;
- exportar argumentos ou caminhos sensíveis sem necessidade.

## Prática C

1. Gere `vmlinux.h` do BTF da VM.
2. Compile o objeto com target BPF.
3. Inspecione seções e BTF sem carregar.
4. Revise log do verifier ao carregar em VM.
5. Execute apenas um processo sintético, colete contagem e desanexe.

## Exercícios

1. Faça análise estática do programa e descreva tipos de cada map, hook, helper,
   chave, valor e limite.
2. Provoque uma rejeição segura por bound não demonstrado, leia o primeiro erro
   e corrija sem relaxar política.
3. Simule falha no segundo attach do loader e prove rollback do primeiro.
4. Monte matriz de portabilidade com BTF, hook, helper, config e permissão.

## Checklist de domínio

- [ ] Explico programa, loader, verifier, map, helper, hook e link.
- [ ] Dimensiono cardinalidade, memória, concorrência e perda.
- [ ] Sei o que BTF e CO-RE adaptam e o que permanece semântico.
- [ ] Implemento rollback em falha parcial e teardown comprovado.
- [ ] Mantenho o capítulo estritamente em observabilidade local.

Fonte: [libbpf overview](https://docs.kernel.org/bpf/libbpf/libbpf_overview.html).
