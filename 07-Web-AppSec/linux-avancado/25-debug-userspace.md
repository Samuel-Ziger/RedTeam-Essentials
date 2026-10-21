# 25 — Depuração de user space

## Objetivos

- preservar evidência antes de alterar o processo;
- usar core dump, GDB, strace, sanitizers e rr quando aplicável;
- depurar deadlock, crash e corrupção;
- produzir um relatório que não dependa da máquina original.

## Ordem de coleta

1. versão exata de executável e bibliotecas;
2. argumentos, ambiente sanitizado e limites;
3. timestamp, PID/TID e estado das threads;
4. core dump e logs;
5. símbolos/debug packages correspondentes;
6. input mínimo que reproduz;
7. somente então, instrumentação adicional.

Anexar debugger pausa threads e muda timing. Em deadlock, isso pode ser aceitável;
em race, pode esconder o defeito.

## Core dumps

```bash
ulimit -c
coredumpctl list 2>/dev/null | head
coredumpctl info PID 2>/dev/null
coredumpctl debug PID 2>/dev/null
```

Core pode conter secrets, buffers, chaves e dados pessoais. Controle acesso,
retenção e sanitização; não anexe dump bruto a issue pública.

## GDB

Com symbols corretos:

```gdb
set pagination off
info threads
thread apply all bt full
info registers
x/16gx $sp
```

Otimização pode eliminar variáveis, inlinear funções e reordenar. Isso não
torna o dump falso; exige interpretar o binário compilado, não a fonte idealizada.

## Syscall tracing

`strace -f -ttt -T -yy` ajuda a ver espera e descritores, mas overhead e volume
são altos. Filtre syscalls e processo. Uma syscall lenta pode estar bloqueada em
filesystem, lock, timer ou scheduler; o trace não identifica sozinho a causa.

## Sanitizers

- ASan: acessos fora de limites e use-after-free;
- UBSan: comportamento indefinido selecionado;
- TSan: data races, com custo alto;
- LSan: leaks em cenários suportados.

Build sanitizado não é necessariamente representativo de performance. Use-o
para correção e reprodução.

## Reproduzir antes de explicar

Defina sintoma, frequência, primeira versão afetada, input mínimo e ambiente. Um
core isolado mostra um estado, mas não necessariamente a sequência que o criou.
Faça redução preservando a falha e mantenha teste determinístico. Se a reprodução
some sob GDB, registre a mudança de timing como evidência de possível race.

Build ID liga executável e debug info. Bibliotecas também precisam corresponder;
uma stack com símbolos de outra build parece plausível e pode apontar linha
errada. Arquive mapa de módulos, hashes e pacotes. Para binário otimizado,
variável “optimized out” e frames inlined exigem desmontagem e CFI, não suposição.

## Classes de investigação

Crash pede sinal, fault address, registradores, stack e ownership do objeto.
Deadlock pede todas as threads, locks esperados e grafo de espera. Corrupção pede
primeiro write incorreto, frequentemente anterior ao crash; ASan, watchpoint ou
rr podem aproximá-lo. Leak pede tendência, allocation sites e distinção entre
memória ainda alcançável e perdida.

Uma causa raiz completa contém condição de entrada, invariante violada, trecho
que permitiu a violação e por que os testes não detectaram. A correção precisa de
regressão que falha antes e passa depois, além de revisão de caminhos semelhantes.

## Falhas comuns

- depurar com executável ou símbolos recompilados depois do incidente;
- concluir pelo último frame sem examinar o estado;
- anexar debugger antes de preservar evidência;
- publicar core com credenciais;
- corrigir sintoma sem teste de regressão;
- usar sanitizer como perfil de performance.

## Prática A

Crie três bugs pequenos: acesso fora do array, deadlock AB/BA e descritor vazado.
Encontre cada um com ferramenta diferente, corrija, adicione teste de regressão
e escreva causa raiz em vez de apenas o sintoma.

## Exercícios

1. Para crash controlado, preserve build ID, core, módulos e input; reproduza em
   build normal e ASan.
2. Construa grafo de wait-for de um deadlock AB/BA usando stacks de todas as
   threads.
3. Reduza um input mantendo a falha e documente cada hipótese descartada.
4. Diante de stack parada em `read()`, separe descritor, alvo, bloqueio, tempo
   de syscall, scheduler e aplicação antes de atribuir causa ao disco.

## Checklist de domínio

- [ ] Preservo evidência e build ID antes de instrumentar.
- [ ] Distingo crash, deadlock, corrupção e leak.
- [ ] Interpreto código otimizado a partir do binário real.
- [ ] Produzo causa raiz e teste de regressão.
- [ ] Sanitizo dumps antes de compartilhar.

Fonte: [userspace debugging guide](https://docs.kernel.org/process/debugging/userspace_debugging_guide.html).
