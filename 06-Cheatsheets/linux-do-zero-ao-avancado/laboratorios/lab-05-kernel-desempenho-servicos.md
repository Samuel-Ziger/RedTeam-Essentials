# Laboratório 05 — kernel, desempenho e serviço profissional

## Missão

Explicar o caminho de uma carga pelo kernel, observar sem causar instabilidade
e entregar um runbook de capacidade e atualização. Módulo carregável e troca de
kernel são opcionais e exclusivos da VM descartável.

## Pré-requisitos

Laboratório 04 e capítulos 24 a 29. Use clone descartável para qualquer etapa de
kernel. Duração esperada: oito a doze horas.

## Parte 1 — syscall ao subsistema

Compile [syscalls.c](../exemplos/c/syscalls.c), copie um arquivo sintético e
trace somente openat, read, write e close. Associe cada evento a:

- chamada no código;
- descritor e objeto;
- transição user space para kernel;
- VFS, page cache e filesystem;
- retorno, erro possível e tratamento.

Explique leitura curta, escrita parcial e EINTR. Compare tamanho e hash da cópia.

## Parte 2 — configuração e dispositivo

Registre release, origem e configuração do kernel. Para um dispositivo não
essencial, relacione barramento, sysfs, driver, módulo e nó. Saneie serial e
identificadores.

Siga [laboratório de kernel](kernel.md) até a compilação do módulo didático.
Carregamento é opcional. Se assinatura, vermagic ou política recusarem, registre
a causa e pare; desativar Secure Boot não é solução.

## Parte 3 — matriz de observação

Compare journal do kernel, strace, perf stat e um tracepoint disponível:

| Ferramenta | Pergunta | Escopo | Privilégio | Overhead | Dado sensível |
|------------|----------|--------|------------|----------|---------------|
| journal | completar | completar | completar | completar | completar |
| strace | completar | completar | completar | completar | completar |
| perf | completar | completar | completar | completar | completar |
| tracepoint | completar | completar | completar | completar | completar |

Cada coleta possui duração e critério de parada. Não habilite debug global nem
capture payload real.

## Parte 4 — desempenho orientado a hipótese

Defina workload sintético limitado e um SLO. Colete pelo menos cinco intervalos
de CPU, memória, armazenamento e PSI. Escolha uma hipótese principal e escreva
antes do experimento:

~~~text
Se a causa for:
Então espero observar:
Ao mudar somente:
O sintoma deve:
O resultado que refuta é:
~~~

Não ajuste sysctl, scheduler ou cache por receita. Compare baseline, experimento
e recuperação.

## Parte 5 — serviço e desktop

Para servidor, produza runbook com configuração efetiva, saúde, logs, backup,
atualização, rollback e capacidade. Para desktop, faça uma prática separada de
sessão, compositor ou áudio e mostre como isolou estado do usuário de estado do
sistema.

## Parte 6 — atualização e fallback

Planeje atualização por pacote oficial. Verifique espaço, backup, processos que
usam bibliotecas antigas e necessidade de reboot. Se testar segundo kernel,
mantenha a entrada anterior e demonstre o retorno pelo console antes de
considerar a etapa concluída.

## Falhas obrigatórias

- destino já existe no copiador por syscalls;
- configuração de serviço inválida;
- workload excede o SLO sem esgotar recursos;
- dispositivo ou módulo inexistente consultado somente por leitura.

## Critérios de aprovação

- código e trace são relacionados linha por linha;
- interface de user space é separada da API interna do kernel;
- ferramenta de observação foi escolhida por pergunta e risco;
- hipótese de desempenho pode ser refutada;
- serviço tem runbook executável;
- fallback funciona e nenhuma etapa remove o único kernel inicializável.
