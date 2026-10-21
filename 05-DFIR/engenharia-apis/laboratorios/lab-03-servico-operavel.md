# Laboratório 03 — Serviço operável

## Pré-requisitos

- [Laboratório 02](lab-02-contrato-seguranca.md)
- [Arquitetura](../13-arquitetura-implementacao.md)
- [Dados](../14-dados-consistencia.md)
- [Resiliência](../15-resiliencia-desempenho.md)
- [Observabilidade](../16-observabilidade.md)
- [Testes](../17-testes.md)
- [Guia de diagnóstico](../GUIA-DIAGNOSTICO.md)

## Missão

Substitua comportamento acidental por arquitetura e operação explícitas. Pode
usar banco local ou fake transacional; o foco é prova de commit, falha e
recuperação.

## Requisitos

- adapter HTTP separado de aplicação/domínio;
- Clock e IdGenerator controláveis;
- escrita condicional atômica;
- alteração + outbox na mesma unidade;
- relay que pode duplicar sem duplicar efeito do consumidor;
- fake de dependência com delay, erro e corpo inválido;
- deadline, retry limitado e cancelamento;
- logs JSON, métricas RED e spans/correlação;
- dois SLIs, SLOs e alertas;
- testes de unidade, componente, contrato, propriedade e concorrência.

## Fault injection

Falhe:

1. antes da transação;
2. após mudar estado, antes do commit;
3. depois do commit, antes da resposta;
4. depois de publicar, antes de marcar outbox;
5. na dependência antes/depois de aceitar o comando;
6. no sink de auditoria.

Para cada ponto, registre estado local, evento, resposta, retry e reconciliação.

## Evidências

- diagrama com fronteiras/commits;
- testes determinísticos;
- dashboard ou especificação de painéis;
- cálculo de error budget;
- alerta e runbook;
- linha do tempo de um game day pequeno.

## Gate

Nenhuma falha produz falso sucesso ou duplicidade silenciosa. Request ID liga
resposta, log e trace. Outra pessoa diagnostica uma falha usando o runbook, sem
editar banco manualmente.

## Extensão

Execute carga local com ramp-up e compare p50/p95/p99 antes/depois de um limite
de concorrência. Defina critério de parada antes.

