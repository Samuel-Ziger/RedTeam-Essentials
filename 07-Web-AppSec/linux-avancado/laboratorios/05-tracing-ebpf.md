# Lab 05 — Tracing e eBPF local

**Classe:** C. **Duração:** 12–18 h.

## Pré-requisitos e gate

Conclua o Lab 04, os capítulos 22–24 e o guia de diagnóstico. Registre kernel,
config, BTF, clang, libbpf, tracefs, clock e estado anterior. Faça snapshot e
defina duração máxima, buffer e taxa esperada antes de ganhar privilégio.

## Alvo

Um programa próprio que cria processos, abre arquivos temporários e termina.
Nenhum socket, interface ou evento de rede entra no experimento.

## Etapa ftrace

1. Salve estado de tracefs.
2. Desabilite tracing antes de configurar.
3. Selecione `sched_process_exec` e filtro do PID/cgroup do lab.
4. Execute por no máximo 30 segundos.
5. Pare tracing, salve trace e estatística de perda.
6. Restaure estado com trap.

Leia o arquivo `format` do evento no kernel ativo e documente tipo e unidade de
cada campo usado. Um filtro por PID pode perder descendentes ou execução em outro
contexto; se usar cgroup, explique suporte e escopo. Execute controle sem tracing
para estimar overhead.

## Etapa eBPF

1. Confirme BTF e features.
2. Gere `vmlinux.h` da VM.
3. Compile `exec_counter.bpf.c` sem carregar.
4. Inspecione ELF, sections e BTF.
5. Use loader mínimo/libbpf para anexar ao tracepoint.
6. Compare contagem per-CPU agregada ao trace ftrace.
7. Desanexe e liste maps/programs para provar cleanup.

O loader deve implementar rollback de falha parcial. Provoque erro seguro depois
do primeiro recurso e demonstre que link, programa, map, pin e descritor não
permanecem. Dimensione cardinalidade e memória do map e trate contagem per-CPU
sem perder CPUs offline ou não observadas.

CO-RE deve ser explicado por relocation concreta: tipo ou campo adaptado, BTF
usado e condição de fallback. Ele não estabiliza semântica do tracepoint nem cria
helper ausente.

## Perguntas

- Qual evento pode ser perdido por buffer cheio?
- O filtro ocorre antes ou depois de reservar espaço?
- CO-RE adaptou qual acesso?
- Qual overhead foi observado com controle negativo?
- O trace demonstra causalidade ou apenas sequência?

Acrescente:

- Qual foi a razão entre eventos esperados, observados e perdidos?
- O que mudou entre contagem global e per-CPU?
- Qual é o primeiro estado no log quando o verifier rejeita?
- Qual evidência prova que a configuração anterior foi restaurada?

## Falha segura

Se o verifier rejeitar, preserve o log e explique a regra. Não desabilite
proteções do host. Ausência de privilégio encerra a etapa de carga, mas a análise
estática ainda deve ser concluída.

## Critério de aprovação

Dados brutos preservam clock, janela, perda, kernel e hashes. A conclusão
distingue sampling de tracing, tracepoint de probe interna e sequência de causa.
O inventário final deve ser igual ao inicial para eventos, tracer, programs,
maps, links e pins pertencentes ao laboratório.

Não liste ou remova recursos de terceiros de forma destrutiva. Se não houver
privilégio ou BTF, finalize análise do ELF, log esperado e plano de loader; não
altere sysctl global do host.
