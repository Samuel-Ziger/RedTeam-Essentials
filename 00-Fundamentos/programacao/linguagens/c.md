# C: linguagem, memória e construção de programas seguros

C oferece controle direto sobre representação, endereços, layout e ciclo de
vida. Esse controle permite sistemas pequenos e previsíveis, mas retira várias
proteções comuns em runtimes gerenciados. Um acesso fora do array, uso após
`free` ou overflow pode produzir **comportamento indefinido**: o padrão deixa de
garantir qualquer resultado, mesmo que “funcione na minha máquina”.

Aprender C é aprender a declarar contratos de tamanho, ownership e validade.

## 1. Toolchain: do fonte ao executável

```bash
cc --version
cc -std=c17 -Wall -Wextra -Wpedantic -Werror -O2 programa.c -o programa
./programa
echo "$?"
```

Etapas conceituais:

1. pré-processador expande `#include` e macros;
2. compilador traduz cada unidade `.c`;
3. assembler produz arquivo-objeto;
4. linker resolve símbolos e bibliotecas em um executável.

Inspecione separadamente:

```bash
cc -std=c17 -E programa.c -o programa.i
cc -std=c17 -S programa.c -o programa.s
cc -std=c17 -c programa.c -o programa.o
cc programa.o -o programa
```

Durante desenvolvimento, mantenha warnings máximos. Para memória e undefined
behavior, quando o compilador suportar:

```bash
cc -std=c17 -Wall -Wextra -Wpedantic -Werror \
  -O1 -g -fsanitize=address,undefined -fno-omit-frame-pointer \
  programa.c -o programa
./programa
```

Sanitizers mudam instrumentação e não substituem testes, revisão ou execução na
plataforma-alvo. Use build separado para produção.

## 2. Primeiro programa e forma de `main`

```c
#include <stdio.h>
#include <stdlib.h>

int main(void) {
    puts("Olá, C");
    return EXIT_SUCCESS;
}
```

Para argumentos:

```c
int main(int argc, char **argv) {
    for (int i = 0; i < argc; i++) {
        printf("argv[%d]=%s\n", i, argv[i]);
    }
    return 0;
}
```

`argc` conta argumentos, inclusive o nome do programa; `argv[argc]` é ponteiro
nulo. Cada argumento é texto terminado em `\0`. Status zero representa sucesso;
defina/documente códigos não zero para classes de erro.

## 3. Tipos, tamanhos e conversões

```c
#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

bool ativo = true;
int contador = 10;
long total = 1000L;
double media = 7.5;
size_t quantidade = 3;
uint32_t campo_protocolo = UINT32_C(42);
```

O padrão define relações mínimas, não um tamanho universal para `int`/`long`.
Use:

- `size_t` para tamanhos/índices de objetos;
- `ptrdiff_t` para diferença de ponteiros do mesmo array;
- tipos de `<stdint.h>` quando largura faz parte do formato/protocolo;
- macros de `<inttypes.h>` ao imprimir inteiros de largura fixa.

`sizeof` devolve bytes do tipo `size_t`:

```c
int values[] = {10, 20, 30};
size_t count = sizeof values / sizeof values[0];
```

Isso só funciona onde `values` ainda é array. Em parâmetro de função, ele é
ajustado para ponteiro e o tamanho deve ser passado separadamente.

### Inteiros signed/unsigned e overflow

Overflow de unsigned é módulo 2^N. Overflow de signed é comportamento
indefinido. Antes de calcular tamanho:

```c
if (count > SIZE_MAX / sizeof *items) {
    /* multiplicação não cabe */
}
```

Misturar signed e unsigned em comparação pode converter o negativo em valor
enorme. Mantenha tipos coerentes e compile com warnings.

### Ponto flutuante

`double` tem arredondamento, `NaN` e infinitos. Use `<math.h>`:

```c
if (!isfinite(value)) {
    /* rejeitar no domínio */
}

if (fabs(a - b) <= 1e-9) {
    /* proximidade adequada a este domínio */
}
```

Dinheiro costuma pedir inteiro em menor unidade ou biblioteca decimal adequada.

## 4. Condições, switch e laços

```c
if (idade < 0) {
    fputs("idade inválida\n", stderr);
} else if (idade < 18) {
    puts("menor");
} else {
    puts("maior");
}
```

Zero é falso; não zero é verdadeiro. Use `<stdbool.h>` para comunicar intenção.
`&&` e `||` fazem curto-circuito.

```c
for (size_t i = 0; i < count; i++) {
    printf("%zu: %d\n", i, values[i]);
}

while (remaining > 0) {
    remaining--;
}
```

`switch` é adequado para enum/discriminante. Termine casos com `break`, `return`
ou marque fallthrough de modo aceito pelo projeto; queda acidental é bug comum.

## 5. Funções, declarações e passagem de argumentos

```c
long sum(const int *values, size_t count) {
    long total = 0;
    for (size_t i = 0; i < count; i++) total += values[i];
    return total;
}
```

C passa argumentos por valor. O valor de um ponteiro pode dar acesso ao objeto
do chamador. `const int *` impede alteração dos elementos por esse acesso e
comunica função leitora.

Contratos que a assinatura sozinha não expressa devem ser documentados:

- `values` pode ser nulo quando `count == 0`?
- o buffer tem pelo menos `count` elementos?
- ponteiros de entrada/saída podem se sobrepor?
- quem possui/libera o resultado?

Parâmetro de saída explícito:

```c
#include <limits.h>

int divide(int numerator, int denominator, int *result) {
    if (result == NULL || denominator == 0) return 0;
    if (numerator == INT_MIN && denominator == -1) return 0;
    *result = numerator / denominator;
    return 1;
}
```

Escreva a saída só no sucesso ou inicialize-a com estado seguro. O segundo
teste evita o único overflow possível da divisão inteira com sinal em complemento
de dois: `INT_MIN / -1`. Em C, esse overflow tem comportamento indefinido; não é
uma simples volta para outro valor.

## 6. Ponteiros, arrays e aritmética

```c
int value = 42;
int *pointer = &value;
*pointer = 43;
```

- `&value`: endereço;
- `*pointer`: objeto apontado;
- `NULL`: nenhum objeto válido;
- ponteiro não inicializado: valor indeterminado, não use.

Array e ponteiro são relacionados, mas não iguais. Um array contém seus
elementos; um ponteiro contém um endereço. Aritmética de ponteiro só é definida
dentro do mesmo array (ou um após o final, sem dereferenciar).

```c
for (int *current = values; current != values + count; current++) {
    printf("%d\n", *current);
}
```

Nunca aceite “há um endereço” como prova de validade. É preciso saber objeto,
tamanho, alinhamento e vida útil.

## 7. Strings, bytes e buffers

String C é uma sequência de `char` terminada por byte zero:

```c
#include <string.h>

char name[32];
if (fgets(name, sizeof name, stdin) == NULL) {
    fputs("falha de leitura\n", stderr);
    return 1;
}
name[strcspn(name, "\n")] = '\0';
```

Reserve sempre espaço para `\0`. `strlen` percorre até o terminador e conta
bytes, não capacidade nem caracteres Unicode. UTF-8 usa um ou mais bytes por
code point.

Formatação limitada:

```c
int written = snprintf(buffer, capacity, "id=%lu", id);
if (written < 0 || (size_t)written >= capacity) {
    /* erro ou truncamento */
}
```

Evite `gets`, `strcpy`, `strcat`, `sprintf` e leitura `%s` sem largura. Mesmo
funções com limite exigem entendimento de capacidade, terminador e truncamento.

Dados binários devem usar `unsigned char`/`uint8_t` conforme o contrato; não
trate buffer arbitrário como string.

## 8. Parsing numérico correto

`atoi` não distingue zero válido de erro e não reporta overflow. Use `strtol` ou
`strtod` verificando toda a fronteira:

```c
#include <errno.h>
#include <limits.h>

int parse_int(const char *text, int *output) {
    char *end = NULL;
    if (text == NULL || output == NULL || *text == '\0') return 0;

    errno = 0;
    long value = strtol(text, &end, 10);
    if (errno == ERANGE || end == text || *end != '\0' ||
        value < INT_MIN || value > INT_MAX) {
        return 0;
    }
    *output = (int)value;
    return 1;
}
```

Defina se espaços, sinal, base hexadecimal e sufixos são aceitos. Parsing seguro
é também contrato de linguagem do seu programa.

## 9. Struct, enum e invariantes

```c
typedef enum {
    TASK_PENDING,
    TASK_DONE
} task_status_t;

typedef struct {
    unsigned long id;
    char title[121];
    task_status_t status;
} task_t;
```

`struct` agrupa representação, mas não protege campos. Forneça funções que
constroem/alteram mantendo invariantes:

```c
int task_init(task_t *task, unsigned long id, const char *title);
int task_complete(task_t *task);
```

Não serialize uma struct gravando seus bytes diretamente: padding, alinhamento,
endianness e representação variam. Defina formato campo a campo.

## 10. Memória automática, estática e dinâmica

### Duração automática

```c
int *invalid(void) {
    int local = 42;
    return &local; /* erro: local deixa de existir ao retornar */
}
```

Variáveis locais comuns vivem até sair do bloco/chamada. Não retorne endereço
delas.

### Duração estática

Objetos globais e `static` vivem por todo o processo. Facilitam retenção de
estado, acoplamento e races; use apenas com intenção.

### Alocação dinâmica

```c
if (count > SIZE_MAX / sizeof(int)) return ERROR_SIZE;
int *values = calloc(count, sizeof *values);
if (values == NULL) return ERROR_MEMORY;

/* usar values dentro de [0, count) */
free(values);
values = NULL;
```

Para cada alocação, responda: quem é o dono, quando transfere, onde libera e se
`NULL` é permitido. `free(NULL)` é seguro; double free não é.

`realloc` pode mover o bloco. Não sobrescreva o único ponteiro antes de checar:

```c
void *temporary = realloc(values, new_count * sizeof *values);
if (temporary == NULL) {
    /* values original continua válido */
} else {
    values = temporary;
}
```

Cheque overflow do tamanho antes.

Erros clássicos:

- out-of-bounds;
- use-after-free;
- double free;
- vazamento;
- leitura de valor indeterminado;
- ponteiro pendente para objeto encerrado;
- desalocador incompatível.

## 11. Cleanup e tratamento de erros

C não possui exceções. Escolha convenção consistente: zero/não zero, enum de
erro, ponteiro nulo ou resultado estruturado. Preserve detalhes úteis.

Uma função com múltiplos recursos pode ter um único cleanup:

```c
int process(const char *path) {
    int status = 1;
    FILE *file = NULL;
    char *buffer = NULL;

    file = fopen(path, "rb");
    if (file == NULL) goto cleanup;

    buffer = malloc(4096);
    if (buffer == NULL) goto cleanup;

    status = 0;

cleanup:
    free(buffer);
    if (file != NULL) fclose(file);
    return status;
}
```

Aqui `goto` não cria fluxo arbitrário; concentra liberação em ordem inversa.
Outra opção são retornos curtos antes de adquirir vários recursos.

`errno` só é significativo quando uma função documentada indica falha; salve-o
antes de outra chamada se precisar. Não teste `errno` sem verificar o retorno.

## 12. Arquivos e I/O

```c
FILE *file = fopen(path, "rb");
if (file == NULL) {
    perror("fopen");
    return 1;
}

unsigned char buffer[4096];
size_t read_count;
while ((read_count = fread(buffer, 1, sizeof buffer, file)) > 0) {
    if (fwrite(buffer, 1, read_count, stdout) != read_count) {
        /* tratar erro de escrita */
    }
}
if (ferror(file)) {
    /* leitura falhou */
}
if (fclose(file) != 0) {
    /* flush/fechamento falhou */
}
```

Leitura curta não significa necessariamente erro; pode ser EOF. Escrita e
`fclose` também falham. Para formatos, defina limites antes de alocar com base
em tamanhos externos.

## 13. Headers, APIs e compilação separada

`vector.h`:

```c
#ifndef RTE_VECTOR_H
#define RTE_VECTOR_H

#include <stddef.h>

typedef struct vector vector_t; /* tipo opaco */

vector_t *vector_create(void);
int vector_push(vector_t *vector, int value);
size_t vector_size(const vector_t *vector);
void vector_destroy(vector_t *vector);

#endif
```

A representação fica em `vector.c`; consumidores veem o contrato. Compile:

```bash
cc -std=c17 -Wall -Wextra -Wpedantic -Werror -c vector.c -o vector.o
cc -std=c17 -Wall -Wextra -Wpedantic -Werror -c main.c -o main.o
cc main.o vector.o -o app
```

O header deve poder ser incluído sozinho e várias vezes. Evite definições de
objetos globais em headers. Make/CMake automatizam dependências e builds; flags
de compilação fazem parte do contrato do projeto.

## 14. Pré-processador e macros

Macros são substituição textual, não funções tipadas:

```c
#define SQUARE_BAD(x) x * x
#define SQUARE(x) ((x) * (x))
```

Mesmo a segunda avalia `x` duas vezes: `SQUARE(i++)` é problemático. Prefira
função `static inline` quando possível. Use macros para guards, configuração de
compilação e casos realmente necessários.

## 15. Modelo de memória e concorrência

O padrão fala em objetos, duração e armazenamento; “stack” e “heap” são um
modelo de implementação útil, não toda a especificação.

- acessar objeto fora de sua vida útil é inválido;
- alinhamento deve ser adequado ao tipo;
- aliasing afeta otimizações;
- bytes de padding podem ser indeterminados;
- data race sobre memória não atômica é comportamento indefinido.

C11 define atomics e threads, mas suporte prático varia. Em POSIX, pthreads são
comuns. Antes de compartilhar memória, defina ownership, lock, condição de
parada e ordem de destruição. `volatile` não torna acesso thread-safe; ele tem
usos específicos e não substitui atomics/mutex.

## 16. Testes, debugger e análise

Uma asserção simples:

```c
#include <assert.h>

static void test_parse_rejects_suffix(void) {
    int output = 0;
    assert(!parse_int("10x", &output));
}
```

`assert` pode desaparecer com `NDEBUG`; não use para validar entrada de usuário
ou condição que produção precisa tratar.

Ferramentas:

```bash
gdb ./programa
valgrind --leak-check=full ./programa    # quando disponível
```

Combine testes de unidade, sanitizers, análise estática, fuzzing de parsers e
builds em mais de um compilador/plataforma. Otimização pode revelar UB que o
build de debug parecia tolerar.

## 17. Leitura guiada do exemplo real

Abra [`exemplos/c/fundamentos.c`](../exemplos/c/fundamentos.c):

1. `conceito_t` restringe estados;
2. `resumo_notas_t` agrupa a saída;
3. `ler_nota` valida ponteiros, conversão, consumo total, finitude e faixa;
4. `analisar_notas` recebe ponteiro + tamanho e escreve saída só no sucesso;
5. `main` verifica overflow antes de `calloc`;
6. ownership do vetor começa em `main` e termina no `cleanup`;
7. `%zu` corresponde a `size_t`;
8. código 2 representa uso/entrada inválida e 1 falha operacional.

```bash
cc -std=c17 -Wall -Wextra -Wpedantic -Werror \
  00-Fundamentos/programacao/exemplos/c/fundamentos.c -lm -o /tmp/fundamentos-c
/tmp/fundamentos-c 10 8 4
/tmp/fundamentos-c 11; echo "$?"
```

## 18. Exercícios progressivos

1. Adicione conceito `A+` e testes para cada fronteira.
2. Calcule mediana em cópia ordenada, sem mutar a entrada.
3. Implemente vetor dinâmico com `size`, `capacity` e crescimento sem overflow.
4. Separe API em `.h`, implementação em `.c` e suíte de testes.
5. Leia CSV em streaming com número de linha e limite de tamanho.
6. Faça fuzz do parser e rode ASan/UBSan.
7. Implemente pilha e fila documentando ownership de cada elemento.
8. Compare builds `-O0` e `-O2` sem depender de comportamento indefinido.

Critério de conclusão: todo ponteiro tem tamanho/vida útil conhecidos, toda
alocação tem dono, toda conversão externa é validada e o programa passa warnings,
testes e sanitizers.
