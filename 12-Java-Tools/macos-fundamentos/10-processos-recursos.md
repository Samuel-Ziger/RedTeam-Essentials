# 10 — Processos, CPU, memória e energia

Programa é código armazenado; processo é uma execução com PID, credenciais,
memória e descritores. Threads compartilham o espaço do processo. Pressão de
memória considera compressão e swap, não apenas "RAM livre".

```zsh
ps -axo pid,ppid,user,state,%cpu,%mem,etime,command
top -l 1 -o cpu -stats pid,command,cpu,mem,state
vm_stat
memory_pressure
```

Activity Monitor apresenta CPU, Memory, Energy, Disk e detalhes do processo.
Colete uma janela de tempo: um pico instantâneo pode ser trabalho normal.
Encerrar com `TERM` permite limpeza; `KILL` é último recurso e perde estado.

## Método

Defina o sintoma, observe processo e filhos, correlacione tempo e recursos,
reproduza em fixture e só então altere. Não mate processos de sistema por nome.

## Prática

Execute uma tarefa local conhecida, amostre CPU/memória por um minuto e
explique wall time, CPU time e pressão. Encerre o processo normalmente.
