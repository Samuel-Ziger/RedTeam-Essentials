# Lab 06 — Depuração e kdump

**Classe:** C/D. **Duração:** 16–24 h.

## Pré-requisitos e gate

Conclua o Lab 05 e os capítulos 25–26. Separe a fase user space na VM de análise
e a fase kernel na sacrificável. Para kdump, console serial, snapshot restaurado,
memória reservada, destino local e espaço livre são gates; qualquer falha impede
acionar o teste.

## User space

Crie programa com use-after-free controlado em dados sintéticos. Compile versões
normal, debug e ASan. Preserve input, hashes, core e build ID. Produza:

- stack trace simbolizado;
- causa raiz;
- correção mínima;
- teste que falha antes e passa depois;
- observação sobre efeito da otimização.

Registre sinal, fault address, todas as threads, mapas, build IDs e bibliotecas.
Reduza o input mantendo o defeito. Depois da correção, execute regressão nas
versões normal, debug e sanitizada. O relatório explica a primeira escrita ou
lifetime incorreto, não apenas o frame do crash.

Acrescente um deadlock sintético: colete stacks de todas as threads, construa
grafo wait-for e prove o ciclo. Não use timeout como correção.

## Kernel

Na VM sacrificável, configure kdump e valide `crashkernel`. Acione apenas o
mecanismo oficial de teste da distribuição. O snapshot e console devem ter sido
testados antes.

Preserve juntos:

- vmcore;
- `vmlinux` com debug;
- `System.map` e `.config`;
- módulos correspondentes;
- journal anterior;
- identificador exato do pacote/commit.

Use `crash` ou `drgn` para identificar panic task, comando, CPU e call trace.
Não compartilhe dump sem revisar secrets.

Antes do panic de teste, verifique que o crash kernel está carregado e que seu
initramfs contém driver e configuração do destino. Use somente o mecanismo
oficial documentado pela distribuição. Após captura, restaure snapshot antes de
repetir qualquer experimento.

Na análise, identifique tipo de falha, taint, CPU, tarefa, instruction pointer,
primeira call trace e mensagens secundárias. Verifique hashes ou build IDs entre
vmcore, `vmlinux`, módulos e config. Versão nominal igual não é correspondência
suficiente.

## Critério

Aprova se o relatório diferencia primeira falha de mensagens secundárias,
explica taint, usa symbols correspondentes e demonstra que o crash kernel
consegue gravar o dump no destino local.

Também deve provar que symbols são exatos, que a primeira falha foi separada da
cascata e que dumps receberam controle de acesso e retenção. Uma segunda pessoa
deve conseguir abrir o artefato com o comando documentado.

## Perguntas para defesa

- Como debugger pode esconder uma race?
- Por que taint não identifica a causa?
- Qual etapa perderia o vmcore se o storage não existir no crash kernel?
- O que um frame de stack demonstra e o que ainda precisa ser provado?

## Cleanup

Restaure a VM D, remova cores sintéticos fora da retenção e confirme que nenhum
limit, debugger ou processo de teste permaneceu. Preserve somente dumps
sanitizados, hashes e relatório em armazenamento controlado.
