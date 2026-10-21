# 17 — I/O assíncrona, epoll e io_uring

## Objetivos

- separar blocking, nonblocking, readiness e completion;
- construir event loop local com descritores;
- entender rings, SQE, CQE e lifetime no io_uring;
- avaliar segurança e compatibilidade da interface.

## Modelos

**Blocking:** a thread espera a operação. Simples e frequentemente suficiente.

**Nonblocking:** a syscall retorna quando não pode progredir; o chamador decide
quando tentar novamente.

**Readiness:** `poll`/`epoll` indicam que uma operação provavelmente progride sem
bloquear. Estado pode mudar entre notificação e uso.

**Completion:** a operação é submetida e um evento informa o resultado final.

Este capítulo usa pipes, `eventfd`, `timerfd` e arquivos locais. Sockets de rede
não fazem parte do módulo.

## epoll

Um epoll instance observa conjuntos grandes de descritores. Level-triggered
continua sinalizando enquanto a condição existe; edge-triggered exige drenar até
`EAGAIN` para não perder progresso. `EPOLLONESHOT` exige rearme.

Desenhe ownership de descritores. Fechar e reutilizar números, duplicar file
descriptions e processar eventos atrasados geram bugs sutis.

## io_uring

Submission Queue Entries descrevem operações; Completion Queue Entries retornam
resultado e `user_data`. Rings compartilhados reduzem syscalls e permitem
batching. Recursos registrados e modos de polling trocam setup, privilégio, CPU
e latência por throughput.

Regras essenciais:

- buffers e metadados devem viver até a completion;
- resultado negativo na CQE é `-errno`;
- short I/O continua possível;
- cancelamento tem corrida com conclusão;
- opcode e flags dependem da versão do kernel;
- nunca reutilize `user_data` sem uma estratégia de geração.

## Segurança

io_uring amplia a interface do kernel e teve evolução rápida. Containers e
sandboxes podem restringi-lo conforme threat model. Isso não implica que a API
seja insegura por definição; implica manter kernel atualizado, reduzir opcodes e
testar a política real.

## Máquina de estados do event loop

Cada operação deve ter estado e ownership explícitos: registrada, pronta,
parcialmente consumida, cancelando, concluída ou encerrada. O número do descritor
pode ser reutilizado; associe eventos a objeto com geração e não a um inteiro
antigo. Em edge-triggered, leia ou escreva até `EAGAIN`; processar uma unidade e
voltar a dormir pode perder a única borda.

`EPOLLHUP` e `EPOLLERR` precisam ser tratados mesmo quando não foram solicitados.
Half-close, descritores duplicados e remoção concorrente alteram o lifecycle.
Teste shutdown enquanto eventos estão pendentes e garanta que callback atrasado
não acessa objeto liberado.

## Submission e completion

No io_uring, submissão aceita uma descrição, não garante execução imediata. A
CQE informa resultado por operação; `res` negativo codifica erro e positivo pode
ser parcial. Buffers, iovecs, pathnames e metadados apontados precisam permanecer
válidos conforme o opcode. Registered resources mudam custo e regras de update.

Cancelamento compete com conclusão: ambos os resultados devem convergir para um
único cleanup. Use identificador único por geração, contabilize operações em voo
e só libere o contexto quando todas possuírem estado terminal. Timeout linkado
também pode produzir mais de uma completion relevante ao protocolo.

## Falhas comuns

- bloquear depois de receber readiness sem drenar corretamente;
- supor que evento significa mensagem inteira;
- reutilizar fd ou `user_data` sem geração;
- liberar buffer após submit e antes da CQE;
- tratar cancelamento solicitado como cancelamento garantido;
- ignorar backpressure na fila de completions.

## Prática A

Implemente um loop com `timerfd` e `eventfd` monitorados por epoll. Gere dez
eventos, encerre deterministicamente e trate `EINTR/EAGAIN`. Em seguida desenhe
uma versão io_uring, incluindo ownership e cancelamento, mesmo sem liburing.

## Exercícios

1. Modele estados de um descritor epoll com leitura parcial, `EAGAIN`, HUP e
   fechamento concorrente.
2. Implemente timerfd e eventfd com encerramento determinístico e testes de dez
   eventos em level e edge-triggered.
3. Desenhe ownership de SQE, buffer, contexto, CQE e cancelamento.
4. Injete short write em uma abstração de teste e confirme que nenhum byte é
   duplicado ou perdido.

## Checklist de domínio

- [ ] Distingo blocking, nonblocking, readiness e completion.
- [ ] Dreno edge-triggered até `EAGAIN`.
- [ ] Trato fd e `user_data` reutilizados com geração.
- [ ] Mantenho buffers vivos até a conclusão correta.
- [ ] Explico por que readiness e completion admitem progresso parcial.

Fontes: [`epoll(7)`](https://man7.org/linux/man-pages/man7/epoll.7.html) e
[io_uring](https://man7.org/linux/man-pages/man7/io_uring.7.html).
