# Java: fundamentos, objetos e aplicações na JVM

Java é uma linguagem estaticamente tipada que normalmente compila para bytecode
executado pela Java Virtual Machine (JVM). O compilador verifica tipos antes da
execução; a JVM fornece carregamento de classes, otimização JIT, threads e coleta
de lixo. Isso não elimina erros de lógica, `null`, races ou uso excessivo de
memória — apenas oferece um modelo explícito para tratá-los.

Este guia usa recursos compatíveis com Java 17+ nos exemplos modernos.

## 1. JDK, JVM e primeiro ciclo

O **JDK** contém compilador e ferramentas de desenvolvimento; uma instalação
somente de runtime não basta.

```bash
java -version
javac -version
mkdir -p build
javac -Xlint:all -Werror -d build Main.java
java -cp build Main
```

O fluxo é:

```text
Main.java → javac → Main.class (bytecode) → JVM → código otimizado/executado
```

`-Xlint:all` ativa diagnósticos; `-Werror` os transforma em falha. Durante
aprendizado, warnings devem ser entendidos, não silenciados.

Um arquivo simples:

```java
public final class Main {
    private Main() {}

    public static void main(String[] args) {
        System.out.println("Olá, Java");
    }
}
```

O nome do arquivo acompanha a classe pública. `main` é a entrada do processo.
Para experimentos, Java moderno também executa um fonte diretamente:

```bash
java Main.java argumento
```

Entenda compilação e classpath antes de adotar Maven ou Gradle.

## 2. Pacotes, classes e visibilidade

```java
package br.dev.agenda.domain;

public final class Task {
    private final long id;
    private final String title;

    public Task(long id, String title) {
        if (id <= 0) throw new IllegalArgumentException("id deve ser positivo");
        if (title == null || title.isBlank()) {
            throw new IllegalArgumentException("título obrigatório");
        }
        this.id = id;
        this.title = title.strip();
    }

    public long id() { return id; }
    public String title() { return title; }
}
```

Visibilidade:

- `private`: somente a própria classe;
- sem modificador: mesmo pacote;
- `protected`: pacote e subclasses, com detalhes de acesso;
- `public`: qualquer consumidor que alcance o tipo.

Comece fechado e exponha apenas o contrato necessário. Pacotes evitam colisão
de nomes e comunicam arquitetura; não são uma barreira forte de segurança.

## 3. Primitivos, referências e wrappers

Primitivos armazenam valores diretamente:

| Tipo | Uso típico |
|---|---|
| `boolean` | verdadeiro/falso |
| `byte`, `short`, `int`, `long` | inteiros com larguras definidas |
| `float`, `double` | ponto flutuante IEEE 754 |
| `char` | unidade UTF-16, não necessariamente caractere completo |

Objetos são acessados por referências, que podem ser `null`. Wrappers como
`Integer`, `Long` e `Double` permitem usar valores em generics/coleções.

```java
int count = 3;
long totalCents = 19_900L;
double average = 7.5;
boolean active = true;
String name = "Ana";
```

Autoboxing converte `int` para `Integer` e vice-versa, mas unboxing de `null`
lança `NullPointerException`:

```java
Integer maybeCount = null;
// int count = maybeCount; // falha em runtime
```

Use `Objects.requireNonNull(value, "value")` na fronteira do construtor quando
`null` viola o contrato. Não espalhe checagens tardias.

### Overflow e números financeiros

Inteiros fazem overflow silencioso nas operações comuns:

```java
long total = Math.addExact(current, delta); // lança ArithmeticException
```

Dinheiro pode usar centavos em `long` com overflow verificado ou `BigDecimal`
com escala e `RoundingMode` explícitos. Nunca construa `BigDecimal` financeiro
diretamente de um `double` impreciso; use texto ou `BigDecimal.valueOf`.

`Double.isFinite` rejeita `NaN`/infinito. Comparações aproximadas exigem uma
tolerância definida pelo domínio.

## 4. Strings, igualdade e imutabilidade

`String` é imutável:

```java
String normalized = raw.strip().toLowerCase(Locale.ROOT);
```

Cada transformação devolve outro objeto. Para concatenação repetida em laço,
use `StringBuilder`:

```java
StringBuilder builder = new StringBuilder();
for (String part : parts) {
    if (!builder.isEmpty()) builder.append(',');
    builder.append(part);
}
String csv = builder.toString();
```

Compare conteúdo com `equals`, não `==`:

```java
"admin".equals(role);       // seguro mesmo se role for null
Objects.equals(a, b);        // aceita ambos nulos
```

`==` compara valores primitivos ou identidade de referências. Interning pode
fazer alguns textos parecerem iguais por `==`, criando um bug intermitente.

UTF-16 significa que `length()` conta code units. Use APIs de code points ou
`BreakIterator` quando o requisito é texto humano.

## 5. Condições, switch e laços

```java
static String concept(double score) {
    if (!Double.isFinite(score) || score < 0 || score > 10) {
        throw new IllegalArgumentException("score fora da faixa");
    }
    if (score >= 9) return "A";
    if (score >= 7) return "B";
    if (score >= 5) return "C";
    return "D";
}
```

Java não converte números/objetos automaticamente em boolean. Condições devem
ser booleanas. `&&` e `||` fazem curto-circuito.

Switch expression devolve valor e exige cobertura:

```java
String label = switch (status) {
    case PENDING -> "Pendente";
    case DONE -> "Concluída";
};
```

Laços:

```java
for (int i = 0; i < values.length; i++) {
    System.out.println(i + ": " + values[i]);
}

for (String value : values) {
    System.out.println(value);
}

while (!queue.isEmpty()) {
    process(queue.remove());
}
```

Use índice quando ele participa do algoritmo; enhanced for quando importa o
valor. Modificar estruturalmente uma coleção durante for-each costuma falhar;
use `Iterator.remove`, `removeIf` ou produza outra coleção.

## 6. Métodos e contratos

```java
static long total(List<Long> values, int discountPercent) {
    Objects.requireNonNull(values, "values");
    if (discountPercent < 0 || discountPercent > 100) {
        throw new IllegalArgumentException("desconto inválido");
    }
    long subtotal = 0;
    for (long value : values) subtotal = Math.addExact(subtotal, value);
    return Math.multiplyExact(subtotal, 100L - discountPercent) / 100L;
}
```

Java passa argumentos **por valor**. Para um objeto, o valor copiado é a
referência. A função pode mutar o objeto apontado, mas não religar a variável do
chamador.

Overloading permite mesmo nome com listas de parâmetros diferentes. Não abuse:
`send(String, boolean, boolean)` é menos legível que um objeto de opções.

Varargs (`String... values`) vira um array e deve ser usado na última posição.
Ele é útil para conveniência, não para esconder uma interface indefinida.

## 7. Arrays e coleções

Array tem tamanho fixo e aceita primitivos:

```java
int[] scores = {10, 8, 4};
int first = scores[0];
```

Coleções principais:

```java
List<String> names = new ArrayList<>();
Set<String> tags = new HashSet<>();
Map<Long, Task> byId = new HashMap<>();
Deque<Task> queue = new ArrayDeque<>();
```

- `ArrayList`: acesso por índice O(1), append amortizado O(1);
- `HashMap`/`HashSet`: busca média O(1), sem ordem de domínio;
- `LinkedHashMap`: preserva ordem de inserção;
- `TreeMap`/`TreeSet`: ordenados, operações O(log n);
- `ArrayDeque`: fila/pilha eficiente nas pontas.

Programe contra `List`, `Map`, `Set` quando a implementação não faz parte do
contrato. `List.of` e `List.copyOf` devolvem coleções não modificáveis, mas não
congelam objetos mutáveis contidos nelas.

## 8. Generics e variância

Generics preservam tipo no compilador:

```java
static <T> T first(List<T> values) {
    if (values.isEmpty()) throw new NoSuchElementException();
    return values.get(0);
}
```

`List<Integer>` **não** é subtipo de `List<Number>`; caso contrário seria
possível inserir um `Double` em uma lista de inteiros. Use wildcards seguindo
PECS: producer extends, consumer super.

```java
static double sum(List<? extends Number> values) { /* lê Number */ }
static void addDefaults(List<? super Integer> output) { /* escreve Integer */ }
```

Por type erasure, argumentos genéricos em geral não existem como tipos concretos
em runtime. Não é possível fazer `new T()` diretamente nem distinguir
`List<String>` de `List<Integer>` via `instanceof`.

## 9. Classes, records, enums e invariantes

Use `record` para dados transparentes com igualdade por valor:

```java
public record Product(String code, long priceCents) {
    public Product {
        if (code == null || code.isBlank()) {
            throw new IllegalArgumentException("código obrigatório");
        }
        if (priceCents < 0) throw new IllegalArgumentException("preço inválido");
        code = code.strip();
    }
}
```

Record é shallowly immutable: um componente `List` ainda poderia mudar. Faça
cópia defensiva no construtor quando necessário.

Use classe para identidade e estado protegido:

```java
public final class Account {
    private long balanceCents;

    public Account(long initial) {
        if (initial < 0) throw new IllegalArgumentException("saldo inválido");
        balanceCents = initial;
    }

    public void deposit(long amount) {
        if (amount <= 0) throw new IllegalArgumentException("valor inválido");
        balanceCents = Math.addExact(balanceCents, amount);
    }

    public long balanceCents() { return balanceCents; }
}
```

Se sobrescrever `equals`, sobrescreva `hashCode` de modo consistente; records já
fazem isso. Campos usados como chave de `HashMap` não devem mudar enquanto a
chave está inserida.

Enums modelam conjunto fechado e podem ter campos/métodos. Evite strings soltas
para estados internos.

## 10. Interfaces e composição

```java
interface TaskRepository {
    Optional<Task> findById(long id);
    void save(Task task);
}

final class TaskService {
    private final TaskRepository repository;

    TaskService(TaskRepository repository) {
        this.repository = Objects.requireNonNull(repository);
    }
}
```

O serviço conhece uma capacidade pequena. Um teste fornece repositório em
memória; produção fornece banco. Isso é composição/injeção por construtor.

Herança é apropriada para substituição real (“é um”), não apenas reuso de três
linhas. Classes `final` e interfaces pequenas reduzem estados inesperados.

`Optional<T>` comunica ausência no retorno. Não o use indiscriminadamente em
campos, parâmetros ou para esconder erro.

## 11. Exceções e recursos

Hierarquia importante:

- checked, como `IOException`: deve ser capturada ou declarada;
- unchecked, subclasses de `RuntimeException`: regra/uso inválido;
- `Error`: falha grave da JVM, normalmente não recuperada pela aplicação.

```java
static Configuration load(Path path) {
    try {
        String text = Files.readString(path, StandardCharsets.UTF_8);
        return parseConfiguration(text);
    } catch (IOException exception) {
        throw new UncheckedIOException("falha ao ler " + path, exception);
    }
}
```

Preserve a causa. Não capture `Exception` sem estratégia, e não use exceção para
fluxo comum de alto volume quando um resultado explícito é mais claro.

Try-with-resources fecha em ordem inversa mesmo quando há falha:

```java
try (BufferedReader reader = Files.newBufferedReader(path, StandardCharsets.UTF_8)) {
    return reader.lines().filter(line -> !line.isBlank()).toList();
}
```

O recurso precisa implementar `AutoCloseable`. Fechamento pode também falhar;
exceções suprimidas ficam acessíveis em `getSuppressed()`.

## 12. Arquivos, texto e serialização

```java
List<String> lines = Files.readAllLines(path, StandardCharsets.UTF_8);
Files.writeString(
        temporary,
        content,
        StandardCharsets.UTF_8,
        StandardOpenOption.CREATE,
        StandardOpenOption.TRUNCATE_EXISTING);
Files.move(temporary, target, StandardCopyOption.REPLACE_EXISTING);
```

Para arquivo grande, não carregue tudo: use `BufferedReader`/stream e processe
linha a linha. Sempre declare charset.

Não use serialização nativa de objetos para dado não confiável. Formatos como
JSON exigem biblioteca e, após parse, validação semântica. Nenhum parser substitui
limites de tamanho, campos permitidos e regras do domínio.

Use `Path.resolve`/`normalize` e verifique a raiz autorizada quando partes do
caminho vêm de usuário.

## 13. Streams e lambdas

```java
List<String> activeNames = users.stream()
        .filter(User::active)
        .map(User::name)
        .sorted()
        .toList();
```

Streams são pipelines lazy até uma operação terminal. Uma stream é consumida
uma vez. Evite efeitos em `map`, `filter` e `peek`; eles dificultam raciocínio e
paralelização.

Um laço é frequentemente melhor para lógica com vários ramos, contexto de erro
ou early return. `parallelStream()` não é “modo rápido”: usa pool compartilhado,
tem overhead e exige operações associativas/stateless. Meça e controle o pool.

## 14. Organização e builds reproduzíveis

Layout convencional:

```text
src/
├── main/java/br/dev/agenda/...
└── test/java/br/dev/agenda/...
```

Maven ou Gradle gerenciam compilação, dependências e testes. Mantenha o wrapper
do build no repositório, fixe plugins/dependências e revise o grafo. Um JAR é um
arquivo de classes/recursos; não implica que todas as dependências estão dentro.

JPMS (`module-info.java`) adiciona módulos fortes e exports explícitos em
projetos que se beneficiam disso. Não confunda módulo Java com pacote.

## 15. Modelo de memória da JVM

Modelo útil, sem tratar implementação como garantia absoluta:

- cada chamada tem frame com variáveis locais e operandos;
- objetos e arrays normalmente vivem no heap gerenciado;
- referências conectam o grafo de objetos;
- o GC recupera objetos que deixam de ser alcançáveis;
- metadados/classes têm áreas próprias da JVM.

GC gerencia memória, não fechamento determinístico de arquivo/socket. Objetos
continuam vivos se caches, listeners, threads ou estáticos mantiverem referência.

O Java Memory Model define visibilidade e ordenação entre threads. Sem uma
relação happens-before, uma thread pode não observar a escrita de outra. `final`,
locks, `volatile`, atomics e coleções concorrentes têm garantias específicas;
`volatile` não torna uma sequência `x++` atômica.

## 16. Concorrência

Prefira executors/tarefas a criar threads sem limite:

```java
ExecutorService executor = Executors.newFixedThreadPool(4);
try {
    Future<Report> future = executor.submit(() -> calculateReport());
    Report report = future.get(2, TimeUnit.SECONDS);
} finally {
    executor.shutdownNow();
}
```

Virtual threads em JDKs modernos são adequadas a muitas tarefas de I/O
bloqueante. Elas não tornam CPU-bound mais rápido, não removem races e ainda
exigem limites para bancos, sockets e APIs externas.

Evite estado mutável compartilhado. Quando necessário, documente quem escreve,
use sincronização apropriada, timeout e política de cancelamento/interrupção.

## 17. Testes e depuração

Projetos normalmente usam JUnit via Maven/Gradle:

```java
@Test
void rejectsScoreAboveTen() {
    assertThrows(IllegalArgumentException.class, () -> concept(10.1));
}
```

Teste:

- caminho feliz;
- cada limite (`0`, `5`, `7`, `9`, `10`);
- `null`, vazio, `NaN`, infinito e entrada malformada;
- igualdade/hash quando usados em coleção;
- falhas de I/O com diretório temporário.

Ferramentas úteis do JDK:

```bash
jdb -classpath build Main
jstack PID
jcmd PID VM.version
jcmd PID GC.heap_info
```

Use IDE debugger para breakpoints e inspeção, Java Flight Recorder para análise
com evidência e logging com contexto. Não registre credenciais.

## 18. Leitura guiada do exemplo real

Abra [`exemplos/java/Fundamentos.java`](../exemplos/java/Fundamentos.java):

1. `Conceito` restringe estados possíveis;
2. `Resumo` modela resultado imutável e faz cópia defensiva do mapa;
3. `validarNota` centraliza a invariante;
4. `analisar` usa `EnumMap`, apropriado para chaves enum;
5. `converterArgumentos` acrescenta posição e preserva causa;
6. `executar` devolve status e deixa `main` pequeno;
7. `Locale.ROOT` torna o separador decimal previsível.

```bash
java 00-Fundamentos/programacao/exemplos/java/Fundamentos.java 10 8 4
java 00-Fundamentos/programacao/exemplos/java/Fundamentos.java 11
```

Com JDK 17+ completo:

```bash
mkdir -p /tmp/rte-java
javac -Xlint:all -Werror -d /tmp/rte-java \
  00-Fundamentos/programacao/exemplos/java/Fundamentos.java
java -cp /tmp/rte-java Fundamentos 10 8 4
```

## 19. Exercícios progressivos

1. Adicione conceito `A+` e teste todos os limites.
2. Faça `Resumo` calcular mediana sem modificar a lista recebida.
3. Leia CSV em streaming e informe linha/coluna em falhas.
4. Modele `Student` como record com lista defensivamente copiada.
5. Crie `StudentRepository` e implementações em memória e arquivo.
6. Monte projeto Maven/Gradle com JUnit e análise de warnings.
7. Processe arquivos em executor limitado, com timeout e cancelamento.
8. Gere um runtime mínimo com `jlink` depois de estabilizar os módulos.

Critério de conclusão: compile sem warnings, explique ownership/mutabilidade,
prove invariantes nos testes e diferencie claramente falha de entrada, domínio
e infraestrutura.
