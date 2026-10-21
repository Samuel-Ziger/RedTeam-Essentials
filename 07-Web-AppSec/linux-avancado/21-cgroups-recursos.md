# 21 — cgroup v2, PSI e OOM

## Objetivos

- entender hierarquia única e distribuição top-down;
- diferenciar weights, limits, protections e allocations;
- configurar limites por systemd;
- diagnosticar throttling, pressão e OOM por cgroup.

## Modelo v2

Todo processo pertence exatamente a um cgroup na hierarquia unificada. Controllers
distribuem recursos entre filhos. Para controllers de domínio, o cgroup que
distribui recursos não deve manter processos internos: mova workloads para folhas.

```bash
findmnt -t cgroup2
cat /sys/fs/cgroup/cgroup.controllers
cat /proc/self/cgroup
systemd-cgls
```

## Quatro modelos

- **weight:** proporção quando há competição, como `cpu.weight`;
- **limit:** teto, como `memory.max` ou `io.max`;
- **protection:** reserva best-effort ou dura, como `memory.low/min`;
- **allocation:** recurso exclusivo que não pode ser superalocado.

`memory.high` aplica pressão e throttling antes do limite fatal.
`memory.max` é a fronteira dura que pode culminar em OOM no cgroup. Uma estratégia
com margem entre ambos permite observar degradação antes da morte.

## Contabilidade

```bash
CG=/sys/fs/cgroup/PATH
cat "$CG/memory.current"
cat "$CG/memory.events"
cat "$CG/cpu.stat"
cat "$CG/io.stat"
cat "$CG/memory.pressure"
```

Os arquivos dependem de controller habilitado e permissão. Use `systemd-run
--user --scope` para testes sem editar diretamente a hierarquia gerenciada.

## OOM

OOM global e memcg OOM têm escopos distintos. `oom_score_adj` influencia seleção,
mas não deve proteger tudo. `memory.oom.group=1` permite tratar o workload como
unidade de falha em vez de matar um worker arbitrário e deixar estado parcial.

## Delegação

Delegar cgroup não significa dar escrita em todos os arquivos do pai. O modelo
preserva contenção: o delegado organiza e restringe sua subárvore sem escapar dos
limites ancestrais. systemd é o single writer recomendado para a árvore que gere.

## Distribuição hierárquica

Controllers trabalham de cima para baixo. O pai habilita um controller em
`cgroup.subtree_control` para que filhos o usem; limites ancestrais continuam
valendo. Weight só distribui capacidade quando irmãos competem. Quota cria teto
por período e pode deixar CPU ociosa mesmo que a aplicação queira usá-la depois
de ser throttled.

Na memória, `memory.low` é proteção best-effort e `memory.min` proteção dura
dentro do que os ancestrais conseguem oferecer. `memory.high` induz reclaim e
throttling; `memory.max` é último limite. Configure high abaixo de max, observe
degradação e deixe margem para o supervisor e para coleta de diagnóstico.

## Leitura orientada a eventos

Snapshots de `memory.current` não contam a história. Compare deltas de
`memory.events` e `cpu.stat`, PSI na mesma janela e resultado funcional.
`oom` indica tentativa de OOM; `oom_kill` registra vítima. `memory.oom.group`
trata o workload como unidade, mas o gerenciador fora do cgroup precisa detectar
falha, preservar evidência e decidir restart.

Para I/O, peso e limites dependem do dispositivo real resolvido por major:minor.
Uma pilha Device Mapper pode exigir identificar o ponto em que a política é
aplicada. Não copie números entre VM, SSD e disco rotacional.

## Falhas comuns

- escrever diretamente na árvore que o systemd gerencia;
- comparar weights sem concorrência;
- confundir quota com participação relativa;
- definir `memory.max` sem margem e sem tratamento de OOM;
- observar contador acumulado sem delimitar a janela;
- delegar arquivos do pai e permitir escape da contenção.

## Prática A/C

```bash
systemd-run --user --scope \
  -p MemoryHigh=256M -p MemoryMax=384M -p TasksMax=64 \
  bash
```

Dentro do shell, execute carga sintética limitada. Observe `memory.events`, PSI,
RSS e resultado. Comece abaixo de `high`, ultrapasse-o gradualmente e pare antes
de ameaçar o host.

## Exercícios

1. Compare dois scopes com weights distintos isolados e concorrentes; explique
   por que o resultado muda.
2. Aplique quota e registre períodos, tempo throttled e capacidade ociosa.
3. Eleve uma carga lentamente por `memory.high`, colete PSI/events e pare antes
   de ameaçar o sistema.
4. Modele OOM de grupo, restart e preservação de dados incompletos.

## Checklist de domínio

- [ ] Distingo weight, quota, protection, limit e allocation.
- [ ] Entendo distribuição top-down e limites ancestrais.
- [ ] Leio deltas de eventos e PSI na janela correta.
- [ ] Projeto margem entre `memory.high` e `memory.max`.
- [ ] Explico `CPUQuota=50%` versus `CPUWeight=50` com e sem competidor.

Fonte: [cgroup v2](https://docs.kernel.org/admin-guide/cgroup-v2.html).
