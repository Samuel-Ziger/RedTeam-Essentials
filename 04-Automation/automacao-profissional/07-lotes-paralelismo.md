# 07 — Lotes, concorrência e cancelamento

Paralelismo aumenta throughput apenas até o primeiro gargalo. Depois disso,
aumenta fila, contenção, rate limit e impacto. A pergunta correta não é “quantas
threads?”, mas “qual recurso limita o sistema e qual semântica deve ser preservada?”.

## Objetivos

- escolher sequencial, threads, async ou processos conforme a carga;
- limitar concorrência e preservar backpressure;
- reconciliar ordem, falha parcial e cancelamento;
- reconhecer races, deadlocks e recursos não thread-safe;
- medir throughput, latência e uso antes de ajustar workers.

## 1. Concorrência, paralelismo e async

- **concorrência:** trabalhos progridem em intervalos sobrepostos;
- **paralelismo:** trabalhos executam ao mesmo tempo;
- **async:** modelo de suspensão eficiente para espera; não torna CPU mais rápida;
- **threads:** compartilham memória e facilitam I/O bloqueante, com races;
- **processos:** isolam memória e usam múltiplos núcleos, com custo de IPC.

Para I/O, async ou pool limitado costuma funcionar. Para CPU, meça processos ou
recursos nativos do runtime. Para poucos itens ou efeito sensível, sequencial pode
ser a melhor engenharia.

## 2. Particionamento

Itens podem executar juntos apenas se suas invariantes forem independentes.
Particione por chave que preserve ordem onde necessário:

~~~text
customerId -> mesma partição e ordem
clientes diferentes -> podem progredir em paralelo
~~~

Chave com distribuição desigual cria hot partition. Meça tamanho e latência por
partição. Reparticionar muda ordem e ownership; trate como migração.

## 3. Concorrência limitada

Use pool ou semáforo, nunca uma tarefa irrestrita por item.

~~~python
import asyncio

async def map_limited(items, worker, limit: int):
    semaphore = asyncio.Semaphore(limit)

    async def one(index, item):
        async with semaphore:
            return index, await worker(item)

    tasks = [asyncio.create_task(one(i, item)) for i, item in enumerate(items)]
    return await asyncio.gather(*tasks)
~~~

Esse exemplo ainda materializa todas as tasks; para milhões de itens, use fila
limitada e N workers persistentes. Limitar execução sem limitar tasks pendentes não
limita toda a memória.

## 4. Little e medição prática

Como aproximação, concorrência necessária cresce com throughput desejado vezes
latência. Mas rate limit, variação, CPU e conexões impõem teto. Experimente 1, 2,
4 e 8 workers com o mesmo conjunto e registre:

- itens por segundo;
- latência p50/p95/p99;
- erros, retries e 429;
- CPU, memória e conexões;
- idade da fila.

Pare de aumentar quando throughput estabilizar ou erro/latência degradar.

## 5. Ordem de conclusão e de saída

Concorrência termina fora de ordem. Associe índice e ID. Escolha:

- emitir assim que termina: menor latência, ordem não determinística;
- bufferizar e ordenar: determinismo, mais memória;
- preservar ordem por partição: compromisso comum;
- escrever resultados independentes com chave: ordem irrelevante.

Não use ordem de conclusão como identidade. Um relatório final pode ordenar por
índice original mesmo que a execução tenha sido concorrente.

## 6. Estado compartilhado e races

Um incremento, check-then-act ou append pode não ser atômico. Prefira:

- estado imutável por tarefa;
- filas para transferir ownership;
- agregação em uma etapa dedicada;
- tipos concorrentes da biblioteca;
- locks pequenos com ordem global documentada.

Não segure lock durante I/O remoto. Isso alonga seção crítica e pode bloquear o
sistema. Nunca assuma thread-safety de client, parser ou formatter sem contrato.

## 7. Falha parcial

Políticas:

- **fail-fast:** sinaliza cancelamento ao primeiro erro;
- **best-effort:** todos terminam e cada item recebe resultado;
- **threshold:** cancela ao atingir N ou percentual de falhas;
- **partition fail:** interrompe apenas a chave afetada.

Fail-fast não desfaz tasks já iniciadas. Colete seus resultados e efeitos. Exceção
de uma tarefa não deve desaparecer porque outra falhou primeiro.

~~~text
total = succeeded + skipped + failed + cancelled + uncertain
~~~

## 8. Cancelamento cooperativo

Cancelamento tem três fases:

1. parar de aceitar trabalho;
2. sinalizar tarefas em espera e adapters;
3. aguardar prazo de encerramento e registrar o restante.

Uma task cancelada durante escrita externa pode ficar uncertain. Proteja somente
a pequena fase de commit quando interrompê-la corromperia estado; não ignore
cancelamento indefinidamente.

## 9. Deadlock, starvation e livelock

- **deadlock:** A espera B e B espera A;
- **starvation:** trabalho nunca obtém recurso;
- **livelock:** todos reagem, mas ninguém progride;
- **priority inversion:** tarefa importante espera recurso retido por menos importante.

Use ordem única de locks, timeout diagnóstico, fairness quando necessária e métrica
de tempo de espera. Timeout libera o chamador, mas não corrige a causa.

## 10. Recursos externos

Pool de conexões, file descriptors, memória e limite do serviço devem ser maiores
ou iguais à concorrência efetiva, com margem. Se existem três camadas com pool 20,
o sistema pode produzir muito mais que 20 chamadas. Propague limites de ponta a
ponta.

## Falhas e diagnóstico

| Sintoma | Hipótese | Experimento |
|---|---|---|
| mais workers pioram | gargalo externo | curva 1/2/4/8 |
| memória cresce | tasks pendentes ilimitadas | fila com capacidade |
| relatório muda | ordem de conclusão | ordenar por chave total |
| cancelou mas houve efeito | commit em voo | estado uncertain e reconcile |
| trava rara | ordem de locks | dump e teste de interleaving |

## Exercícios

### Nível 1 — pool limitado

Processe lote com no máximo quatro ativos. **Aceite:** um contador fake prova que
o limite nunca é excedido e o relatório final é ordenado.

### Nível 2 — curva de capacidade

Meça 1, 2, 4 e 8 workers. **Aceite:** relatório justifica o limite por throughput,
p95, erros e recurso limitante.

### Nível 3 — cancelamento

Injete falha e cancelamento durante commit. **Aceite:** nenhum item desaparece;
cada um termina reconciliável e efeitos confirmados não são chamados de rollback.

## Checklist

- [ ] O modelo escolhido corresponde a I/O ou CPU.
- [ ] Tasks pendentes e ativas possuem limites.
- [ ] Ordem e particionamento preservam invariantes.
- [ ] Estado compartilhado tem ownership ou sincronização.
- [ ] Falha e cancelamento reconciliam todos os itens.
- [ ] O número de workers foi medido, não adivinhado.

