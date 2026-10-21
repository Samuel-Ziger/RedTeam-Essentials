# 20 — Logs, observabilidade e troubleshooting

## Objetivos

- transformar um sintoma vago em janela, impacto e hipótese falsificável;
- correlacionar logs, métricas, estado e mudanças sem destruir evidência;
- distinguir uso, saturação, erro, latência e capacidade;
- produzir diagnóstico saneado, reproduzível e proporcional ao risco.

## Observar antes de alterar

Troubleshooting é reduzir hipóteses com evidência. Reiniciar, aumentar limites
ou apagar cache antes de observar destrói estado e pode apenas adiar a falha.

Use o ciclo:

1. descreva esperado versus observado;
2. determine início, frequência e impacto;
3. registre mudanças e alcance;
4. construa linha do tempo;
5. meça as camadas relevantes;
6. teste uma hipótese falsificável por vez;
7. aplique a menor correção reversível;
8. valide sintoma e efeitos colaterais;
9. documente causa e prevenção.

## Logs tradicionais e journal

Arquivos podem aparecer em `/var/log`; nomes variam (`syslog`, `messages`,
`auth.log`, `secure`). systemd-journald recebe mensagens estruturadas e pode
encaminhar para syslog.

```bash
journalctl --list-boots
journalctl -b -p warning..alert
journalctl -u app.service --since '2026-09-30 10:00:00'
journalctl _PID=1234
journalctl -o json-pretty -n 1
```

Relógio incorreto destrói correlação. Confira sincronização:

```bash
timedatectl status
chronyc tracking 2>/dev/null || true
```

## Retenção e rotação

`logrotate` renomeia/comprime/remove arquivos conforme política. `copytruncate`
pode perder linhas em corrida; preferir sinal para o processo reabrir o arquivo
quando ele suporta. Para journal:

```bash
journalctl --disk-usage
systemd-analyze cat-config systemd/journald.conf 2>/dev/null
```

Defina retenção por capacidade, investigação, privacidade e conformidade.
Centralize logs importantes com transporte autenticado e controle de acesso.

## Quatro sinais

- latência: distribuição, não só média;
- tráfego: trabalho por unidade de tempo;
- erros: explícitos e resultados incorretos;
- saturação: fila/pressão quando o recurso aproxima limite.

CPU 100% pode ser trabalho útil. Load average inclui tarefas executáveis e em
espera ininterruptível; não é percentual de CPU.

## Visão do sistema

```bash
uptime
vmstat 1 5
mpstat -P ALL 1 3 2>/dev/null
iostat -xz 1 3 2>/dev/null
pidstat -dur 1 3 2>/dev/null
cat /proc/pressure/{cpu,memory,io}
```

Colete intervalo, não uma foto. `sar` preserva histórico quando `sysstat` foi
configurado, mas frequência e retenção determinam o que é visível.

## Por recurso

### CPU

```bash
top -H
ps -eo pid,ppid,ni,psr,stat,%cpu,comm --sort=-%cpu | head
perf stat -- comando 2>/dev/null
```

Separe user, system, iowait, steal, IRQ e fila. `iowait` não mede diretamente
quanto todos os processos esperaram por disco.

### Memória

Use `free`, PSI, `vmstat`, `smaps_rollup`, faults, swap I/O e logs de OOM, como
explicado no capítulo 12.

### Armazenamento

```bash
iostat -xz 1 5 2>/dev/null
findmnt
df -hT
df -ih
```

Interprete latência, fila e throughput no contexto do dispositivo e da carga.
Percentual `util` tem limitações em dispositivos paralelos.

### Fronteira com conectividade

Neste módulo, a observação termina no processo, no socket local e no estado
exposto pelo host. Métricas de enlace, DNS, transporte e caminho entre hosts
são desenvolvidas nos módulos 14 a 18. Registre o resultado local e encaminhe
o caso com horário, origem, destino e mensagem exata.

## Inspeção de processo

```bash
lsof -p PID
strace -f -tt -T -p PID
```

`strace` observa syscalls e pode alterar timing/desempenho. Use por janela curta
e filtre (`-e trace=file,network`) quando possível. Ele pode exibir dados
sensíveis. `perf`, eBPF e tracing do kernel também têm overhead e requisitos de
privilégio; comece pela ferramenta menos invasiva.

## Core dumps

Core dump preserva memória do processo após falha e pode conter chaves, senhas e
dados pessoais. Controle coleta, criptografia, acesso e retenção.

```bash
coredumpctl list 2>/dev/null | head
coredumpctl info PID 2>/dev/null
```

Analise binário e símbolos correspondentes com `gdb`; versão divergente engana.

## Evidência reproduzível

O script `exemplos/diagnostico.sh` coleta informações somente leitura e remove
campos sensíveis por padrão. Um bom bundle registra versões, tempo, boot ID,
estado de unidades, recursos, montagens e mensagens relevantes, mas não copia
segredos ou todos os logs indiscriminadamente.

## Exercícios

1. Colete uma série curta de CPU, memória e armazenamento e explique tendência,
   intervalo e limitações de cada medida.
2. Crie uma unit que falha por caminho inexistente, construa uma linha do tempo
   pelo journal e corrija apenas a causa comprovada.
3. Compare log textual e campos estruturados; defina quais campos permitem
   correlacionar uma execução sem registrar segredos.
4. Receba o sintoma “está lento” e escreva três hipóteses mutuamente
   distinguíveis, cada uma com teste, risco e critério de encerramento.

## Checklist de domínio

Receba um relato “o Linux está lento” e produza hipótese, janela, medições e
teste capaz de distinguir CPU, memória, armazenamento e aplicação local.
