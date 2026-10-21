# Respostas orientativas

Estas respostas mostram o tipo de raciocínio esperado. Saídas exatas variam com
kernel, arquitetura, configuração, distribuição e carga.

## ABI versus API interna

A syscall publicada para user space faz parte de um contrato de compatibilidade
muito mais forte que uma função C interna do kernel. Um módulo fora da árvore
pode precisar de adaptação entre releases mesmo quando os aplicativos continuam
funcionando sem recompilação.

## RSS não é consumo exclusivo

RSS inclui páginas residentes que podem ser compartilhadas. Para atribuição
proporcional, PSS é mais informativo; para impacto no sistema, também observe
page cache, reclaim, swap, `memory.current` e PSI. Nenhum número isolado responde
todas as perguntas.

## O cache não é memória desperdiçada

O kernel usa RAM ociosa para cachear dados de arquivo e pode recuperar grande
parte dela. O problema é pressão sustentada, latência de reclaim ou working set
maior que a memória disponível, não o campo `used` alto por si só.

## Lock, atomic ou RCU

Escolha depende de invariantes, contenção, contexto e proporção leitura/escrita.
Atômico não torna uma operação composta correta. RCU acelera leituras, mas exige
publicação segura e liberação somente após grace period.

## EEVDF, nice e latência

Nice altera peso relativo da entidade fair quando há competição; não reserva uma
fração fixa de CPU. EEVDF acompanha lag, seleciona entidades elegíveis e usa
deadline virtual. Uma tarefa com 20 ms fim a fim e 2 ms de task-clock passou o
restante runnable ou bloqueada. Wakeup/switch separa espera de runqueue; stacks,
syscalls e eventos do subsistema ajudam a localizar bloqueio.

## Ordem de remoção em RCU

O writer primeiro remove o ponteiro da visão de novos readers. Depois aguarda o
grace period para leitores anteriores terminarem e só então libera. Esperar antes
de despublicar permite entrada de novos leitores e não resolve lifetime. Campos
mutáveis internos ainda podem exigir lock, atomic ou nova versão imutável.

## Page fault não é falha do programa

Demand paging, copy-on-write e carregamento de arquivo usam page faults como
mecanismo normal. Minor fault normalmente não exige I/O; major fault exigiu I/O,
mas não prova swap. Endereço fora de VMA ou acesso incompatível pode resultar em
sinal. VSZ mede reserva, RSS residência sem ratear compartilhamento e PSS divide
páginas compartilhadas.

## Rename não basta para durabilidade

Rename no mesmo filesystem fornece troca atômica de nome para observadores, mas
uma queda pode ocorrer antes de dados e metadata chegarem à camada persistente.
O protocolo típico grava temporário, verifica todos os retornos, sincroniza o
arquivo, renomeia e sincroniza o diretório. O contrato ainda depende de
filesystem, flush, dispositivo e energia.

## Thin provisioning

Um volume pode anunciar 100 GiB sobre pool de 20 GiB porque blocos são alocados
sob demanda. Isso é overprovision intencional, não criação de capacidade.
Monitore data e metadata separadamente, taxa de crescimento e margem de expansão.
Antes do esgotamento, a política deve impedir novas alocações ou expandir com
storage real; falha silenciosa é inaceitável.

## Readiness e completion

Readiness indica que tentar a operação provavelmente fará algum progresso. Entre
o evento e o uso, o estado pode mudar, e short I/O continua válido. Completion
informa resultado de uma submissão, mas o resultado também pode ser parcial ou
erro. Em io_uring, buffer e contexto permanecem válidos até a CQE correspondente;
cancelamento compete com conclusão.

## Secure Boot e measured boot

Secure Boot verifica autorização de componentes antes de executar. Measured boot
estende hashes em PCRs; um verifier ou política interpreta as medidas. Medir não
bloqueia por si só, e nenhuma das duas propriedades cifra disco. Sealing precisa
aceitar updates legítimos, limitar rollback e possuir recovery autenticado.

## Weight, quota e pressão

CPUWeight distribui capacidade entre irmãos quando competem; sem competidor, uma
tarefa pode usar a CPU disponível. CPUQuota limita tempo por período mesmo se
houver capacidade ociosa. Na memória, high aplica reclaim e throttling; max é
fronteira dura. Events e PSI na mesma janela mostram perda de progresso melhor
que um snapshot isolado de uso.

## Menos instruções, mais tempo

Contagem menor não garante execução menor. As instruções podem custar mais
ciclos, sofrer cache misses, misprediction, dependência, frequência reduzida ou
espera fora da CPU. Verifique task-clock, cycles, wall clock, eventos de cache,
frequência, runqueue e repetição. Multiplexing e overhead também podem tornar a
comparação inconclusiva.

## CO-RE não cria uma ABI interna

BTF e CO-RE adaptam tipos, offsets, tamanhos e algumas variações de campos no
alvo. Eles não criam hook ou helper ausente, não habilitam config e não preservam
significado de função interna. Feature probing, tracepoints e fallback continuam
necessários. O loader também precisa desfazer maps e links se o attach falhar no
meio.

## Símbolos exatos para vmcore

Config, compilador, backports e módulos mudam layout e endereços mesmo sob a mesma
release nominal. Ferramentas de dump interpretam bytes usando tipos e símbolos;
um par incorreto pode produzir nomes plausíveis e campos falsos. Preserve build
ID ou hashes de vmcore, `vmlinux`, módulos, `System.map` e config.

## KVM, QEMU e VM exit

KVM fornece API e execução virtualizada no kernel. QEMU oferece modelo de
máquina, firmware, dispositivos e tratamento em user space. Acesso a dispositivo
emulado pode causar VM exit para QEMU processar e devolver resultado. TCG traduz
instruções sem depender de aceleração KVM. Por isso dizer que “KVM é o emulador”
omite as demais camadas.

## Autenticação do root hash

dm-verity detecta bloco incompatível com uma Merkle tree, mas alguém precisa
autenticar o root hash. Se imagem e hash ocupam o mesmo local mutável sem
assinatura ou boot confiável, ambos podem ser substituídos em conjunto. A âncora
de confiança fica fora desse par e possui rotação, revogação e recovery.

## Trace não demonstra causalidade sozinho

Um evento ocorrer perto do sintoma cria correlação. Demonstre causalidade com
experimento controlado, repetição, controle negativo e uma previsão que possa
falhar.

## Snapshot não é backup

Snapshot compartilha domínio de falha com o volume original. Ele ajuda em
rollback rápido; backup exige cópia independente, retenção e restauração
testada.

## Build reproduzível

Duas compilações independentes do mesmo fonte e ambiente declarado devem gerar
artefatos bit a bit iguais. Fixar apenas o timestamp não basta: ordem, locale,
caminhos, toolchain e dados gerados também podem introduzir variação.

## Patch aceitável

Um patch pequeno resolve um problema descrito, compila em configurações
relevantes, inclui teste ou justificativa, respeita estilo, identifica
mantenedores e carrega `Signed-off-by` somente se o autor entende o DCO.

## Avaliação

Uma resposta é aceita quando declara versão e suposições, separa fato de
inferência, nomeia a invariante, escolhe evidência capaz de refutar a hipótese,
trata caminhos de erro e lifetime, define reversão e reconhece o que a VM ou a
ferramenta não consegue provar.
