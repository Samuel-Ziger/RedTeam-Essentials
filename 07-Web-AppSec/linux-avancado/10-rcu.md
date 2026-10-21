# 10 — RCU e estruturas lockless

## Objetivos

- entender read-copy-update sem tratá-lo como “sem sincronização”;
- distinguir read-side critical section, update e grace period;
- reconhecer publicação, remoção e recuperação de memória;
- saber quando RCU não é a melhor escolha.

## Ideia central

Leitores entram em uma região barata, acessam uma versão publicada e saem.
Atualizadores criam ou modificam estado de forma controlada, publicam o novo
ponteiro e aguardam um **grace period** antes de liberar o objeto antigo. Esse
intervalo garante que leitores anteriores tenham terminado.

```text
writer: allocate → initialize → publish → remove old → grace period → free
reader:             enter → dereference → use → exit
```

RCU protege lifetime e visibilidade conforme APIs usadas; ele não torna
automaticamente consistentes todos os campos mutáveis do objeto.

## Sabores e APIs

RCU clássico, SRCU e variantes para tarefas têm condições quiescentes distintas.
No caminho comum aparecem:

- `rcu_read_lock()` / `rcu_read_unlock()`;
- `rcu_dereference()` para consumir ponteiro publicado;
- `rcu_assign_pointer()` para publicar;
- `synchronize_rcu()` para aguardar;
- `call_rcu()` para callback assíncrono;
- `kfree_rcu()` para liberação adiada.

Nunca substitua essas APIs por casts porque “funcionou em x86”. Elas carregam
semântica de compilador, arquitetura, lockdep e documentação.

## RCU versus alternativas

RCU tende a beneficiar estruturas lidas com extrema frequência e atualizadas
raramente. O custo migra para writers, memória e complexidade de lifetime. Para
um objeto simples com baixa contenção, mutex pode ser mais correto e mais fácil
de revisar.

Uma estrutura “lockless” ainda depende de atomics, ordenação e protocolo. O termo
não significa wait-free, nem ausência de contenção de cache.

## Como ler um uso real

1. identifique o ponteiro protegido;
2. marque o começo e o fim de cada leitor;
3. encontre o ponto de publicação;
4. encontre a remoção da estrutura;
5. localize o grace period ou callback;
6. verifique quem protege campos mutáveis internos.

## Linha do tempo correta

Publicação e remoção são operações diferentes. O writer inicializa o objeto por
completo, publica com a primitiva RCU adequada e, quando for retirar, primeiro
remove a referência alcançável por novos leitores. Só então espera um grace
period para que leitores que já possuíam a referência terminem. Esperar antes de
despublicar permite que novos leitores continuem entrando indefinidamente.

Um grace period não espera “todos os processos” nem garante que nenhum reader
exista no sistema. Ele cobre leitores relevantes que começaram antes de um ponto
de referência e observaram as regras do sabor usado. `synchronize_rcu` bloqueia
o writer; `call_rcu` agenda callback e exige manter objeto e callback válidos até
a execução.

## Atualização e campos mutáveis

RCU funciona muito bem com objetos imutáveis após publicação: writer constrói
nova versão e troca o ponteiro. Se campos internos mudam in-place, outra
sincronização pode ser necessária. Leitor não deve guardar ponteiro além da
read-side critical section sem adquirir referência estável.

Listas RCU usam macros próprias para preservar ordenação e ajudar verificadores.
Misturar acesso comum e RCU ao mesmo ponteiro enfraquece a documentação e pode
quebrar em arquiteturas com memória mais relaxada, ainda que pareça estável em
x86.

## Diagnóstico e custo

Stalls de RCU indicam que grace periods não avançaram no prazo, mas a causa pode
ser CPU presa, IRQ desabilitada, reader excessivamente longo ou falta de
quiescent state. Colete a primeira mensagem, CPUs, stacks e flavor antes de
culpar o callback observado por último.

## Falhas comuns

- liberar objeto logo após remover o ponteiro;
- aguardar grace period antes de despublicar;
- usar ponteiro depois de sair da região de leitura;
- alterar campo interno sem proteção adicional;
- adotar RCU onde mutex simples seria mais revisável.

## Prática A

Escolha um uso pequeno de `kfree_rcu` no kernel. Desenhe dois leitores e um
writer em uma linha do tempo. Mostre qual use-after-free surgiria se o objeto
fosse liberado imediatamente e quais campos têm outra proteção.

## Exercícios

1. Desenhe publicação, dois leitores, remoção, grace period e liberação em uma
   linha do tempo, marcando quem ainda pode ver cada versão.
2. Compare `synchronize_rcu`, `call_rcu` e `kfree_rcu` quanto a bloqueio e
   ownership.
3. Encontre um campo mutável dentro de objeto protegido por RCU e identifique sua
   segunda forma de sincronização.
4. Explique um stall a partir de uma CPU presa com preempção desabilitada.

## Checklist de domínio

- [ ] Distingo publicação, remoção, grace period e recuperação de memória.
- [ ] Sei que RCU não torna campos mutáveis automaticamente consistentes.
- [ ] Não retenho ponteiro sem referência fora da região de leitura.
- [ ] Escolho o flavor de acordo com suas condições quiescentes.
- [ ] Sei quando um mutex é uma solução melhor e mais simples.

Fonte: [What is RCU?](https://docs.kernel.org/RCU/whatisRCU.html).
