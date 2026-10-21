# 23 — ftrace, tracepoints, kprobes e uprobes

## Objetivos

- escolher ponto de instrumentação com menor acoplamento;
- usar tracefs sem confundir trace com log permanente;
- entender filtros, buffers, perda e overhead;
- investigar um processo próprio de ponta a ponta.

## Tracefs e ftrace

Tracefs costuma estar em `/sys/kernel/tracing`. `nop`, function e
function_graph são tracers comuns conforme config. Ativar tracing global de
função pode produzir volume e overhead enormes; filtre PID e função primeiro.

```bash
TR=/sys/kernel/tracing
cat "$TR/available_tracers" 2>/dev/null
head "$TR/available_events" 2>/dev/null
```

Leitura de `trace_pipe` consome eventos em fluxo. O buffer é finito; eventos
perdidos precisam aparecer na conclusão.

## Tracepoints

Tracepoints são pontos declarados com formato exposto. Em geral são preferíveis
a probes em funções internas porque têm intenção de observação mais clara.

```bash
cat "$TR/events/sched/sched_process_exec/format" 2>/dev/null
```

Formato ainda deve ser consultado no kernel real. Campos, disponibilidade e
permissão variam.

## Kprobes e uprobes

Kprobes instrumentam endereços/funções do kernel; uprobes instrumentam user
space. Ambos dependem de símbolos, otimização, inlining e assinatura real.
Retprobes observam retorno, mas recursion, funções que não retornam e tail calls
exigem cuidado.

Não trate função interna como ABI estável. Revalide probe após update.

## Hist triggers e synthetic events

O tracing pode agregar chaves, valores e latências no kernel, reduzindo volume
enviado ao user space. Comece com uma dimensão e confirme cardinalidade; chaves
descontroladas esgotam tabelas ou tornam o resultado inútil.

## Procedimento seguro C

1. salve tracer, eventos e tamanho de buffer atuais;
2. desabilite tracing;
3. configure filtro para PID da carga;
4. habilite somente um evento;
5. execute por janela curta;
6. desabilite antes de ler;
7. restaure configuração mesmo em erro.

Use trap no script de laboratório. Nunca deixe eventos globalmente ativos por
esquecimento.

## Escolha do ponto de observação

Comece pela fronteira mais estável que ainda responde à pergunta. Eventos da
aplicação preservam semântica; tracepoints oferecem contrato de observação do
kernel; kprobe acessa implementação interna e precisa ser revalidado a cada
build. Uprobe depende do ELF realmente carregado, offset, inlining, PIE e build
ID. Quanto mais interno o ponto, maior o poder e o acoplamento.

Antes de habilitar, leia o arquivo `format`, determine unidade e tipo de cada
campo e estime taxa. Filtro por PID pode não cobrir filhos futuros ou trabalho em
outro contexto; filtro por cgroup pode ser melhor quando suportado. Declare o que
ficou fora do escopo.

## Buffer, relógio e perda

Tracing usa buffers finitos geralmente per-CPU. Ordenar eventos exige timestamps
e conhecimento do clock selecionado; a leitura pode observar CPUs em ordem
diferente. Aumentar buffer reduz perda, mas consome memória e não corrige
consumidor lento. Registre `entries-in-buffer/overrun` e duração.

`trace_pipe` é stream destrutivo; `trace` é snapshot. Desabilitar antes de ler
cria janela final clara. Para latência, synthetic events e hist triggers podem
calcular deltas no kernel, porém chaves de alta cardinalidade precisam de limite.

## Falhas comuns

- ativar function tracer global sem filtro;
- usar nome de função interna como interface estável;
- ignorar eventos perdidos ou clock;
- interpretar sequência como causalidade;
- esquecer estado anterior e deixar probes ativos;
- publicar argumentos que contêm dados sensíveis.

## Exercícios

1. Escolha tracepoint para uma pergunta local, leia `format` e documente tipos,
   unidade, filtro e volume esperado.
2. Execute janela de dez segundos, prove ausência de overrun e restaure todo o
   estado mesmo após erro injetado.
3. Compare tracepoint e kprobe para o mesmo fenômeno e liste acoplamentos.
4. Crie hist trigger de cardinalidade limitada e explique seu orçamento.

## Checklist de domínio

- [ ] Seleciono a fronteira mais estável que responde à pergunta.
- [ ] Leio formato e unidade no kernel executado.
- [ ] Controlo filtro, clock, buffer, duração e perda.
- [ ] Diferencio stream destrutivo de snapshot.
- [ ] Sempre desabilito e restauro tracing no cleanup.

Fonte: [ftrace](https://docs.kernel.org/trace/ftrace.html).
