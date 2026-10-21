# 05 — Jobs, agendamento, leases e checkpoints

O agendador decide quando tentar iniciar. Ele não garante exclusividade, sucesso,
ordem nem execução exatamente no horário. O job continua responsável por contrato,
idempotência, retomada e evidência.

## Objetivos

- modelar o ciclo de vida de uma execução;
- definir janela lógica separada do horário real;
- controlar sobreposição com locks, leases e fencing;
- persistir checkpoints apenas após efeitos confirmados;
- tratar atraso, horário sazonal, catch-up e cancelamento.

## 1. Estado explícito

~~~text
scheduled -> claimed -> running -> succeeded
                    |          -> partial
                    |          -> failed -> retryable | terminal
                    |          -> cancelling -> cancelled
                    -> expired
~~~

Registre run ID, job ID, versão do contrato, janela lógica, scheduledAt,
startedAt, attempt, owner, deadline e checkpoint. Estado terminal não deve voltar
a running; uma nova tentativa recebe novo run ID e preserva a mesma chave lógica.

## 2. Horário de agenda e janela lógica

Um job diário “das vendas de ontem em São Paulo” precisa de data civil, zona IANA
e regra de calendário. O momento em que iniciou pode estar atrasado e não muda a
janela processada.

~~~json
{
  "jobId": "daily-sales",
  "window": {"date": "2026-10-04", "zone": "America/Sao_Paulo"},
  "scheduledAt": "2026-10-05T06:00:00Z",
  "startedAt": "2026-10-05T06:03:12Z"
}
~~~

Use instante UTC para eventos e data/hora/zona para intenção civil. Offset fixo
não representa regras históricas e futuras da zona.

## 3. Agenda não é garantia

Defina comportamento para:

- disparo duplicado;
- disparo atrasado;
- execução perdida durante indisponibilidade;
- vários horários perdidos ao retornar;
- job anterior ainda ativo;
- relógio alterado;
- agenda suspensa e retomada.

Catch-up pode executar todas as janelas, apenas a mais recente ou nenhuma. Processar
cem janelas de uma vez pode derrubar a dependência; aplique limite e backpressure.

## 4. Sobreposição

Políticas comuns:

| Política | Uso | Risco |
|---|---|---|
| allow | partições independentes | competição por recurso |
| forbid | apenas um por vez | janelas podem atrasar |
| queue | preservar todas as janelas | backlog crescente |
| replace | resultado novo torna antigo inútil | efeitos antigos já podem existir |
| partition | uma execução por chave | chave errada causa colisão |

Replace solicita cancelamento; não desfaz o que foi confirmado.

## 5. Lock, lease e fencing token

Um lock sem expiração pode ficar órfão. Uma lease expira e precisa ser renovada.
Mas um worker pausado pode acordar depois de perder a lease e continuar escrevendo.

Fencing token resolve quando o recurso de destino rejeita tokens antigos:

~~~text
worker A recebe token 41 -> pausa
lease expira
worker B recebe token 42 -> escreve
worker A retorna com 41 -> destino rejeita
~~~

Sem suporte do sink ao fencing, lease reduz sobreposição, mas não prova exclusão
sob pausa longa e partição de rede.

## 6. Checkpoint correto

Checkpoint representa efeito confirmado:

~~~text
ler item 500
calcular transformação
publicar com chave idempotente
confirmar publicação
gravar checkpoint 500
~~~

Gravar antes da publicação perde item se o processo cair. Gravar depois permite
repetição, portanto o sink precisa ser idempotente.

O checkpoint inclui versão do schema, identidade da fonte, posição e digest da
configuração relevante. Retomar com regra nova sobre metade do lote pode produzir
resultado inconsistente; recuse ou inicie execução nova.

## 7. Unidade de commit

Checkpoint por item maximiza precisão e custo de persistência. Por lote reduz custo,
mas repete até N itens. Escolha pelo custo do replay e capacidade do sink.

~~~text
batch 1: items 1..100 -> commit -> checkpoint 100
batch 2: items 101..200 -> falha no 173
retomada: recomeça 101 com deduplicação
~~~

Não atualize checkpoint com max(item_id) se processamento paralelo puder concluir
fora de ordem. Use watermark contíguo ou conjunto/ranges de confirmação.

## 8. Heartbeat e detecção de job travado

Heartbeat indica que o worker ainda progride. Inclua currentPhase, lastProgressAt e
contadores, sem payload sensível. Atualizar heartbeat em thread separada pode fazer
um job travado parecer saudável; associe-o ao progresso ou exponha ambos.

Um watchdog distingue:

- sem heartbeat: processo possivelmente morto;
- heartbeat sem progresso: dependência ou deadlock;
- progresso lento: degradação;
- checkpoint antigo com sucesso aparente: commit/evidência inconsistente.

## 9. Cancelamento e encerramento

Ao receber cancelamento:

1. pare de reivindicar novos itens;
2. sinalize adapters canceláveis;
3. conclua ou abandone com segurança a unidade atual;
4. grave estados confirmados;
5. libere lease somente se ainda for sua;
6. emita relatório cancelled/partial.

Evite handler que executa operação complexa e insegura no sinal do SO. Use o
mecanismo do runtime para converter o sinal em pedido cooperativo.

## 10. Timezone e horário sazonal

Uma hora civil pode não existir ou ocorrer duas vezes. Para agendas de negócio,
defina regra para gaps e folds: pular, mover para próximo instante válido ou escolher
primeira/segunda ocorrência. Teste com uma zona que tenha transição, mesmo que a
zona do produto atualmente não tenha.

Intervalo técnico “a cada 15 minutos desde a conclusão” é diferente de cron
“nos minutos 0, 15, 30, 45”. Declare qual semântica deseja.

## Falhas e diagnóstico

| Sintoma | Causa provável | Evidência |
|---|---|---|
| mesmo dia processado duas vezes | chave usa run ID | janela e chave idempotente |
| item desapareceu | checkpoint antecipado | eventos commit/checkpoint |
| dois workers escrevem | lease expirada sem fencing | owner, token e versão |
| backlog explode ao retomar | catch-up ilimitado | missed schedules e fila |
| job parece vivo sem avançar | heartbeat desacoplado | lastProgressAt |

## Exercícios

### Nível 1 — estados

Modele transições e eventos inválidos. **Aceite:** terminal é imutável e cada
tentativa tem identidade sem perder a janela lógica.

### Nível 2 — retomada

Falhe no item 501 antes e depois do commit. **Aceite:** checkpoint nunca afirma
efeito ausente e replay não duplica.

### Nível 3 — sobreposição

Simule dois workers, expiração e retorno do antigo. **Aceite:** fencing rejeita o
token antigo e o relatório identifica o owner efetivo.

## Checklist

- [ ] Agenda, janela lógica e instante real são distintos.
- [ ] Duplicata, atraso, catch-up e sobreposição têm política.
- [ ] Lease possui expiração e, se necessário, fencing.
- [ ] Checkpoint segue efeito confirmado e inclui versão.
- [ ] Paralelismo não avança watermark sobre lacunas.
- [ ] Cancelamento preserva evidência e não promete rollback.

