# 18 — Capacidade e projeto final

Capacidade liga demanda, recursos e SLO. Meça baseline, sazonalidade, headroom,
saturação e crescimento. CPU média baixa não exclui picos; espaço livre não
mede latência; memória usada não implica pressão.

## Indicadores locais

- CPU por workload e fila;
- commit, available memory, paging;
- latência/queue/IOPS/throughput de disco;
- erros de serviço e duração de jobs;
- crescimento de volume/log;
- tempo de boot/update/backup/restore.

## Projeto: servidor standalone recuperável

Construa Server Core sem NIC que hospeda um job local de processamento de
fixtures. Entregue:

1. decisão de edition/Core e mapa de componentes;
2. baseline JSON e estado desejado idempotente;
3. volumes separados, ACLs e quota;
4. tarefa/serviço com conta e direitos mínimos;
5. auditoria, Defender, update e health checks;
6. capacidade medida com carga sintética;
7. backup e restore em clone com RPO/RTO;
8. runbook de rebuild e cleanup.

## Rubrica

Arquitetura 20%, segurança 20%, automação 20%, observabilidade 15%, restore
20%, documentação/cleanup 5%. Sem restauração testada, o projeto não conclui.

