# Sistemas, memória e concorrência

Todo programa executa sobre recursos finitos: CPU, memória, arquivos, sockets,
processos e tempo. Concorrência introduz ainda mais estados possíveis. Este
capítulo fornece um modelo prático para raciocinar sobre esses recursos, tornar
falhas observáveis e escrever programas que encerram corretamente.

## Objetivos de aprendizagem

Ao final, você deverá conseguir:

- diferenciar programa, processo, thread, tarefa assíncrona e event loop;
- diferenciar concorrência, paralelismo e assincronicidade;
- explicar memória virtual, stack, heap, referência e tempo de vida;
- demonstrar e corrigir uma condição de corrida;
- reconhecer deadlock, starvation e livelock;
- usar fila limitada para aplicar backpressure;
- escolher threads, processos ou `async` conforme a carga;
- aplicar timeout, cancelamento e encerramento gracioso;
- medir desempenho antes de otimizar;
- investigar vazamento, travamento e uso excessivo de recursos.

Pré-requisitos: funções, exceções, coleções e execução pelo terminal.
Os exemplos principais usam Python 3.12+ e biblioteca padrão.

## 1. Do arquivo ao processo

Um **programa** é código e dados armazenados. Um **processo** é uma instância
em execução, com espaço de endereçamento virtual, descritores/handles, estado,
credenciais e pelo menos uma thread.

```text
Arquivo executável/script
          |
          | carregar/inicializar
          v
Processo
  +-- memória virtual
  +-- arquivos e sockets abertos
  +-- variáveis de ambiente e argumentos
  +-- thread principal
       +-- stack própria
```

Processos são isolados por padrão: um não acessa diretamente a memória de
outro. Eles se comunicam por mecanismos explícitos, como pipe, socket, arquivo,
memória compartilhada ou fila fornecida pelo sistema.

Uma **thread** é um fluxo de execução dentro do processo. Threads do mesmo
processo compartilham heap, variáveis globais e descritores; cada uma possui
stack e registradores de execução próprios. Compartilhar torna comunicação
barata e sincronização obrigatória.

### Observe no sistema

Execute um processo temporário:

```bash
python3 -c 'import os,time; print("pid", os.getpid()); time.sleep(30)'
```

Enquanto ele espera, em outro terminal:

```bash
ps -o pid,ppid,stat,etime,command -p PID_EXIBIDO
```

`PID` identifica o processo; `PPID`, o processo pai; `STAT`, seu estado; `ETIME`,
tempo decorrido. O comando termina após 30 segundos. Não reutilize um PID antigo:
o sistema pode atribuir o número a outro processo.

## 2. Concorrência, paralelismo e assincronicidade

- **Concorrência:** várias tarefas fazem progresso em períodos sobrepostos.
- **Paralelismo:** duas ou mais tarefas executam literalmente ao mesmo tempo.
- **Assincronicidade:** uma operação permite que o chamador prossiga e receba o
  resultado depois.

Um único núcleo pode alternar threads e produzir concorrência sem paralelismo.
Vários núcleos podem executar threads/processos em paralelo. Um event loop pode
coordenar milhares de operações de I/O concorrentes em uma thread, desde que as
tarefas cedam controle ao esperar.

```text
Thread A: [CPU][espera I/O........][CPU]
Thread B:      [CPU][espera....][CPU]

Event loop: [A inicia I/O][B inicia I/O][B pronto][A pronto]
```

**CPU-bound** gasta a maior parte do tempo calculando. **I/O-bound** gasta a
maior parte esperando disco, rede, banco ou usuário. Essa classificação orienta
a ferramenta:

| Carga | Opção inicial | Motivo |
|-------|----------------|--------|
| Poucas operações bloqueantes | execução sequencial | menor complexidade |
| Muitas esperas com API bloqueante | threads | simples para I/O independente |
| Muitas esperas com biblioteca assíncrona | event loop/`async` | muitas tarefas com menos threads |
| Cálculo pesado independente | processos/worker nativo | usa múltiplos núcleos |

Meça: uma escolha arquitetural não substitui perfil da carga real.

## 3. Memória virtual, stack e heap

Cada processo enxerga um espaço de endereços virtual. O sistema operacional e o
hardware mapeiam páginas virtuais para memória física ou outros armazenamentos.
Isso fornece isolamento e permite que endereços iguais em processos diferentes
representem dados distintos.

Modelo conceitual:

```text
endereços altos
+----------------------+
| stack da thread      | chamadas, variáveis locais; cresce/encolhe
+----------------------+
| região livre/mapas  |
+----------------------+
| heap                 | objetos/alocação dinâmica
+----------------------+
| dados e código       |
+----------------------+
endereços baixos
```

O desenho é uma simplificação; runtimes e sistemas variam.

### Stack

Cada chamada cria um frame com informação necessária para retornar, parâmetros
e variáveis locais conforme a linguagem/runtime. Recursão sem caso-base ou muito
profunda pode esgotar a stack.

```python
def regressiva(n: int) -> None:
    print(n)
    regressiva(n - 1)  # não possui caso-base


regressiva(3)  # termina com RecursionError, não com uma contagem completa
```

O defeito lógico é a ausência de condição de parada; aumentar o limite de
recursão esconderia a causa.

### Heap e gerenciamento de vida

Objetos de tamanho/vida dinâmicos costumam residir na heap. Em C, o programa
aloca e libera explicitamente. Python, Java, C# e JavaScript usam coleta de lixo
para objetos inalcançáveis.

Garbage collector não resolve tudo:

- uma lista global ainda referencia cada objeto e cresce sem limite;
- arquivo/socket aberto é recurso do sistema e deve ser fechado prontamente;
- callback registrado pode manter um objeto alcançável;
- buffer/fila sem limite acumula dados mais rápido do que os consome.

Use gerenciamento determinístico quando existir:

```python
from pathlib import Path

with Path("entrada.txt").open(encoding="utf-8") as stream:
    first_line = stream.readline()

# O arquivo foi fechado mesmo se readline levantou uma exceção.
```

Em Java, use `try-with-resources`; em C#, `using`; em JavaScript/Node.js, feche
handles conforme a API; em C, desenhe um caminho de cleanup para cada alocação.

## 4. Ponteiros, referências e propriedade

Um ponteiro armazena um endereço. C permite aritmética de ponteiros e acesso
direto, logo um erro pode resultar em acesso fora do limite, uso após liberação,
double free ou comportamento indefinido.

```c
#include <stdio.h>
#include <stdlib.h>

int main(void) {
    size_t count = 4;
    int *values = calloc(count, sizeof *values);
    if (values == NULL) {
        fputs("falha de alocacao\n", stderr);
        return 1;
    }

    for (size_t i = 0; i < count; i++) {
        values[i] = (int)(i * i);
        printf("%d\n", values[i]);
    }

    free(values);
    values = NULL;
    return 0;
}
```

Compile com diagnósticos em ambiente de estudo:

```bash
cc -std=c17 -Wall -Wextra -Wpedantic -Werror \
  -fsanitize=address,undefined -g memoria.c -o memoria
./memoria
```

AddressSanitizer e UndefinedBehaviorSanitizer ajudam a detectar classes de
falha durante aquela execução; não provam ausência de todos os defeitos.

Linguagens gerenciadas usam referências sem expor normalmente o endereço e a
aritmética. Ainda é preciso entender aliasing: duas variáveis podem referenciar o
mesmo objeto mutável, portanto alterar por uma delas afeta a outra.

```python
a = [1, 2]
b = a
b.append(3)
print(a)  # [1, 2, 3]

c = list(a)  # cópia rasa: novo contêiner, elementos ainda podem ser compartilhados
```

## 5. Operações compostas e condição de corrida

Uma condição de corrida ocorre quando o resultado depende de uma intercalação
não controlada. `contador += 1` conceitualmente lê, soma e escreve; outras
execuções podem intercalar entre as etapas.

Exemplo controlado que força duas threads a ler o mesmo valor:

```python
import threading

counter = 0
both_read = threading.Barrier(2)


def unsafe_increment() -> None:
    global counter
    local = counter
    both_read.wait(timeout=2)
    counter = local + 1


threads = [threading.Thread(target=unsafe_increment) for _ in range(2)]
for thread in threads:
    thread.start()
for thread in threads:
    thread.join()

print("esperado 2; obtido", counter)  # obtido 1
```

A barreira existe apenas para tornar o defeito observável. O problema real é a
sequência read–modify–write sem sincronização.

### Correção com exclusão mútua

```python
import threading

counter = 0
counter_lock = threading.Lock()


def safe_increment() -> None:
    global counter
    with counter_lock:
        counter += 1


threads = [threading.Thread(target=safe_increment) for _ in range(2)]
for thread in threads:
    thread.start()
for thread in threads:
    thread.join()

print(counter)  # 2
```

A região protegida é a **seção crítica**. Mantenha-a pequena, mas completa:
proteger somente a escrita e deixar a leitura fora não tornaria o incremento
atômico. Não dependa de detalhes acidentais de um runtime, como a presença de
um lock global do interpretador; a invariante precisa ser explícita.

Alternativas ao lock:

- operação atômica fornecida pelo runtime/banco;
- estrutura thread-safe;
- imutabilidade e troca de valores completos;
- particionar estado para que cada worker tenha um dono;
- enviar mensagens por fila em vez de compartilhar memória;
- remover a concorrência quando ela não traz benefício.

## 6. Deadlock, starvation e livelock

**Deadlock**: tarefas esperam indefinidamente por recursos que o grupo retém.
Um caso clássico:

```text
Thread A possui lock_conta_1 e espera lock_conta_2
Thread B possui lock_conta_2 e espera lock_conta_1
```

Reduza o risco:

- adquira locks sempre na mesma ordem global, por exemplo menor ID primeiro;
- não execute I/O lento mantendo um lock;
- evite locks aninhados;
- use timeout quando a API permitir e trate a falha;
- prefira um dono para cada estado mutável.

**Starvation** ocorre quando uma tarefa nunca recebe recurso/tempo suficiente.
**Livelock** ocorre quando tarefas continuam reagindo uma à outra, mas nenhuma
progride. CPU ativa não prova progresso.

Ao investigar um travamento, capture stacks das threads ou dump do runtime antes
de reiniciar, se isso for seguro; o estado de espera é a evidência principal.

## 7. Filas e backpressure

Se produtores geram 1.000 itens/s e consumidores processam 100 itens/s, uma fila
ilimitada cresce 900 itens/s. Mais memória apenas adia a falha. **Backpressure**
faz o produtor desacelerar, rejeitar ou degradar de forma definida.

```python
import queue
import threading
import time

work: queue.Queue[int | None] = queue.Queue(maxsize=4)


def consumer(name: str) -> None:
    while True:
        item = work.get()
        try:
            if item is None:
                return
            time.sleep(0.05)  # simula I/O/trabalho
            print(name, item * item)
        finally:
            work.task_done()


workers = [threading.Thread(target=consumer, args=(f"w{i}",)) for i in range(2)]
for worker in workers:
    worker.start()

for value in range(10):
    work.put(value, timeout=1)  # bloqueia quando a capacidade está cheia

for _ in workers:
    work.put(None, timeout=1)

work.join()
for worker in workers:
    worker.join()
```

Pontos importantes:

- `maxsize` torna capacidade uma decisão explícita;
- `put(..., timeout=1)` evita espera infinita;
- `task_done()` fica em `finally`, inclusive em falha;
- existe um sentinela por consumidor;
- `join()` espera que cada item retirado seja finalizado.

Em serviços reais, defina a política quando a fila lotar: esperar, devolver
`429/503`, descartar somente dados permitidos ou persistir em sistema apropriado.

## 8. `async`/`await`, timeout e cancelamento

Uma função `async` retorna uma coroutine. Ela só progride quando agendada e deve
ceder o controle em `await`. Cálculo pesado ou chamada bloqueante dentro do event
loop congela todas as demais tarefas.

```python
import asyncio


async def fetch_simulated(name: str, delay: float) -> str:
    await asyncio.sleep(delay)  # representa I/O não bloqueante
    return f"{name}:ok"


async def main() -> None:
    calls = [
        asyncio.wait_for(fetch_simulated("a", 0.1), timeout=0.5),
        asyncio.wait_for(fetch_simulated("b", 1.0), timeout=0.2),
    ]
    results = await asyncio.gather(*calls, return_exceptions=True)
    for result in results:
        print(type(result).__name__, result)


asyncio.run(main())
```

A primeira operação conclui; a segunda produz `TimeoutError`. O timeout limita
cada chamada. Em um fluxo real, também limite o orçamento total da operação.

Cancelamento é cooperativo. Use `try/finally` para liberar recursos e, em geral,
não engula a exceção de cancelamento.

```python
async def worker() -> None:
    resource = await acquire_resource()
    try:
        await process(resource)
    finally:
        await release_resource(resource)
```

`asyncio` não torna automaticamente uma biblioteca bloqueante em assíncrona.
Escolha clientes compatíveis ou mova a operação bloqueante para executor com
limites bem definidos.

## 9. Threads versus processos em Python

No CPython tradicional, o GIL limita a execução simultânea de bytecode Python
por threads em um mesmo interpretador, embora I/O e extensões possam liberar o
GIL. Threads ainda são úteis para I/O. Para CPU-bound puro, processos costumam
ser a opção inicial:

```python
from concurrent.futures import ProcessPoolExecutor


def count_divisors(number: int) -> int:
    return sum(number % candidate == 0 for candidate in range(1, number + 1))


if __name__ == "__main__":
    values = [200_003, 200_009, 200_017, 200_023]
    with ProcessPoolExecutor() as executor:
        print(list(executor.map(count_divisors, values)))
```

O bloco `if __name__ == "__main__"` é importante para criação de processos em
plataformas que importam novamente o módulo filho. Processos têm custo de criação
e serialização; não são melhoria automática para trabalhos pequenos.

Outras linguagens/runtimes possuem modelos diferentes. Meça e consulte a
documentação da versão usada.

## 10. Sinais e encerramento gracioso

Encerrar corretamente significa:

1. receber solicitação de parada;
2. parar de aceitar trabalho novo;
3. permitir que trabalho em andamento termine até um prazo;
4. cancelar o restante de forma conhecida;
5. confirmar/abortar transações;
6. fechar arquivos, sockets e threads;
7. sair com código coerente.

Modelo simplificado:

```python
import signal
import threading
import time

stop_requested = threading.Event()


def request_stop(signum, frame) -> None:
    del signum, frame
    stop_requested.set()


signal.signal(signal.SIGINT, request_stop)
signal.signal(signal.SIGTERM, request_stop)

while not stop_requested.wait(timeout=0.5):
    print("trabalhando")

print("encerrando recursos")
```

Handlers de sinal possuem restrições por plataforma/runtime; mantenha-os
mínimos. Em containers, a forma JSON de `CMD` ajuda o processo da aplicação a
receber sinais diretamente.

## 11. Bytes, texto e representação binária

Texto é uma sequência de caracteres; arquivo/rede transporta bytes. Encoding
define a conversão:

```python
text = "ação"
payload = text.encode("utf-8")
print(payload, len(text), len(payload))
print(payload.decode("utf-8"))
```

O número de caracteres pode diferir do número de bytes. Protocolos binários
precisam definir tamanho, sinal, ordem dos bytes e limites:

```python
import struct

payload = struct.pack("!I", 1_000)  # ! = ordem de rede; I = inteiro de 32 bits
print(payload.hex())                 # 000003e8
print(struct.unpack("!I", payload)[0])
```

Não grave uma `struct` C bruta e espere formato portável: padding, alinhamento,
tamanho dos tipos e endianness podem variar.

## 12. Desempenho: latência, throughput e capacidade

- **Latência:** tempo de uma operação.
- **Throughput:** operações concluídas por unidade de tempo.
- **Concorrência:** trabalho simultaneamente em progresso.
- **Utilização:** proporção de um recurso ocupada.

Média esconde caudas; registre percentis como p50, p95 e p99 quando apropriado.

Processo de otimização:

1. defina uma carga representativa e um objetivo;
2. confirme correção;
3. estabeleça baseline repetível;
4. use profiler/medição para localizar o gargalo;
5. altere uma coisa;
6. compare tempo, memória e correção;
7. registre o trade-off.

Exemplo de medição local:

```bash
python3 -m timeit -s 'values=list(range(10000))' '9999 in values'
python3 -m timeit -s 'values=set(range(10000))' '9999 in values'
```

Isso compara apenas membership nesse ambiente. Construir o `set` também custa;
inclua esse custo se a estrutura for usada uma única vez.

## 13. Diagnóstico por sintoma

| Sintoma | Hipóteses iniciais | Evidência |
|---------|--------------------|-----------|
| Memória cresce continuamente | retenção, fila ilimitada, cache, leak nativo | perfil por tipo/alocação e tamanho da fila |
| CPU em 100% sem throughput | loop ocupado, contenção, serialização | profiler e stacks |
| Processo parado | deadlock, I/O sem timeout, fila vazia | dump de threads e descritores |
| Erro intermitente | race, dependência, teste compartilhado | correlação, repetição e sincronização controlada |
| Muitos arquivos abertos | recurso não fechado | contagem de descritores e caminho de cleanup |
| Latência cresce sob carga | saturação/fila | throughput, tamanho de fila, CPU/I/O e percentis |

Colete evidência antes de reiniciar quando for seguro. Reiniciar restaura o
serviço, mas pode apagar o estado necessário para descobrir a causa.

## 14. Segurança e robustez de recursos

- imponha limite de tamanho, fila, concorrência, memória e tempo;
- trate comprimento recebido como não confiável antes de alocar;
- verifique overflow ao calcular `quantidade * tamanho` em linguagens de baixo nível;
- inicialize memória e nunca use após liberar;
- não mantenha lock durante chamada externa controlada por terceiro;
- propague cancelamento sem deixar estado parcial;
- use usuário e permissões mínimas;
- faça cleanup em caminhos de sucesso e erro;
- evite logar buffers e dados sensíveis durante diagnóstico;
- teste sob repetição e carga limitada, não apenas uma execução feliz.

## 15. Laboratórios por nível

### Nível 1: memória e recursos

1. Execute o exemplo C com sanitizers.
2. Remova temporariamente `free`, observe o diagnóstico se leak detection estiver
   disponível e restaure a correção.
3. Em Python, abra 1.000 arquivos com e sem context manager em um diretório
   temporário e observe descritores sem usar dados reais.
4. Explique a diferença entre objeto inalcançável e recurso fechado.

**Critério:** versão final encerra sem alerta do sanitizer e fecha recursos em falha.

### Nível 2: concorrência controlada

1. Execute a corrida com `Barrier` e prove a atualização perdida.
2. Corrija com lock.
3. Reestruture para que uma única thread seja dona do contador e receba mensagens.
4. Compare complexidade e throughput das duas soluções.

**Critério:** 100 execuções preservam o valor esperado e todas as threads terminam.

### Nível 3: serviço com pressão

1. Crie dois produtores e dois consumidores com fila limitada.
2. Injete lentidão no consumidor.
3. Defina o que ocorre quando `put` excede o timeout.
4. Registre tamanho da fila, itens concluídos e rejeitados.
5. Envie sinal de encerramento e drene ou cancele conforme contrato.

**Critério:** memória permanece limitada, o programa não trava e a soma de
concluídos + rejeitados corresponde aos itens produzidos.

## 16. Exercícios

### Essenciais

1. Explique processo e thread com dois exemplos do seu sistema.
2. Desenhe stack e heap durante três chamadas de função.
3. Demonstre aliasing com lista aninhada e cópia rasa.
4. Compare CPU-bound e I/O-bound com medição.
5. Adicione timeout a três tarefas assíncronas.

### Intermediários

1. Implemente fila limitada com shutdown e tratamento de erro no consumidor.
2. Crie intencionalmente lock order inversion em teste isolado, detecte por
   timeout e depois imponha ordem global.
3. Substitua busca O(n) repetida por conjunto e meça construção + consultas.
4. Implemente framing binário `tamanho + payload` com limite antes da alocação.
5. Capture e compare latência p50/p95 de uma operação simulada.

### Avançados

1. Implemente cancelamento cooperativo em uma pipeline de três estágios.
2. Compare thread pool, process pool e `asyncio` para cargas apropriadas.
3. Gere perfil de alocação de uma fila crescente e corrija a causa.
4. Escreva um plano de encerramento com prazo e estado das tarefas restantes.
5. Modele uma invariante concorrente no SQLite e prove-a com teste simultâneo.

## Critério de conclusão

- [ ] Diferencio concorrência, paralelismo e assincronicidade com exemplos.
- [ ] Explico quais recursos pertencem ao processo e quais pertencem à thread.
- [ ] Demonstro uma race de forma controlada e justifico a correção.
- [ ] Reconheço deadlock e aplico ordem/escopo de locks.
- [ ] Construo fila limitada com backpressure e shutdown.
- [ ] Uso timeout e cancelamento sem abandonar recursos.
- [ ] Sei quando escolher execução sequencial, threads, processos ou `async`.
- [ ] Meço antes/depois e preservo correção durante otimização.
- [ ] O programa final termina, libera recursos e permanece correto sob repetição.
