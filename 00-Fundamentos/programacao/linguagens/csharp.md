# C# e .NET: fundamentos tipados até aplicações modernas

C# combina tipagem estática, orientação a objetos, recursos funcionais e
gerenciamento automático de memória. O SDK .NET compila código para IL
(Intermediate Language); o runtime carrega, verifica e otimiza esse código para
a plataforma. O coletor de lixo cuida de memória gerenciada, mas você continua
responsável por invariantes, arquivos, sockets, concorrência e limites.

O projeto do exemplo mira `net10.0`. Se sua máquina possui outro SDK, confira os
frameworks instalados antes de alterar o alvo do projeto.

## 1. SDK, runtime e primeiro ciclo

```bash
dotnet --info
dotnet --list-sdks
dotnet new console -n MinhaApp --framework net10.0
cd MinhaApp
dotnet run
dotnet build --configuration Release
```

O arquivo `.csproj` descreve alvo e opções:

```xml
<Project Sdk="Microsoft.NET.Sdk">
  <PropertyGroup>
    <OutputType>Exe</OutputType>
    <TargetFramework>net10.0</TargetFramework>
    <ImplicitUsings>enable</ImplicitUsings>
    <Nullable>enable</Nullable>
    <TreatWarningsAsErrors>true</TreatWarningsAsErrors>
  </PropertyGroup>
</Project>
```

Nullable e warnings como erro transformam ambiguidades em feedback cedo. Uma
solução (`.sln`) agrupa projetos; cada `.csproj` é uma unidade de build e
dependência.

Top-level statements tornam a entrada curta:

```csharp
Console.WriteLine("Olá, C#");
return 0;
```

O compilador gera a classe/método de entrada. Em aplicações maiores, ainda use
namespaces, classes e métodos para separar responsabilidades.

## 2. Variáveis, tipos e inferência

```csharp
int count = 3;
long totalCents = 19_900L;
double average = 7.5;
decimal price = 19.90m;
bool active = true;
string name = "Ana";
var inferredCount = 3; // continua sendo int estaticamente
```

`var` pede inferência ao compilador; não cria tipo dinâmico. Use quando o tipo é
óbvio ou verboso. `dynamic` adia resolução para runtime e deve ficar restrito a
interop que realmente exige isso.

### Value types e reference types

`int`, `bool`, enums e structs são value types: atribuição normalmente copia o
valor. Classes, arrays, delegates e strings são reference types: a referência é
copiada e pode apontar para o mesmo objeto.

```csharp
int a = 1;
int b = a;
b++;
// a ainda é 1

var first = new List<int> { 1 };
var second = first;
second.Add(2);
// first também contém 2
```

Não reduza isso a “value sempre stack, reference sempre heap”; JIT, boxing,
closures e campos mudam a alocação. O contrato importante é semântica de cópia.

### Nullability

Com nullable reference types:

```csharp
string required = "texto";
string? optional = Console.ReadLine();

if (optional is not null)
{
    Console.WriteLine(optional.Length);
}
```

O compilador analisa fluxo e avisa dereference potencial. Isso não valida dados
externos em runtime e bibliotecas sem anotações podem quebrar a promessa. Use
`ArgumentNullException.ThrowIfNull(value)` em APIs públicas quando apropriado.

## 3. Números, conversões e overflow

Conversão textual é uma fronteira:

```csharp
if (!int.TryParse(
        text,
        NumberStyles.Integer,
        CultureInfo.InvariantCulture,
        out int value))
{
    Console.Error.WriteLine("inteiro inválido");
}
```

`TryParse` representa uma falha esperada sem exceção. Defina cultura: `1,5` e
`1.5` têm significados diferentes conforme locale.

Inteiros podem overflow. Use `checked` quando isso é erro de domínio:

```csharp
long total = checked(current + delta);
```

`double`/`float` são ponto flutuante binário. `decimal` é base decimal e costuma
ser mais adequado a dinheiro, junto com escala/arredondamento definidos.
`double.IsFinite` rejeita infinito e NaN.

## 4. Texto, interpolação e Unicode

`string` é imutável e usa UTF-16:

```csharp
string message = $"Olá, {name.Trim()}";
bool same = string.Equals(a, b, StringComparison.Ordinal);
```

Escolha comparação conscientemente:

- `Ordinal`/`OrdinalIgnoreCase`: identificadores, protocolos e chaves técnicas;
- regras culturais: texto apresentado a humanos quando o requisito pede.

`Length` conta unidades UTF-16, não grafemas. Use APIs de `System.Globalization`
para texto humano complexo.

Concatenação repetida em laço cria objetos; use `StringBuilder` quando o volume
for significativo e medido.

## 5. Decisão, pattern matching e laços

```csharp
string Concept(double score)
{
    if (!double.IsFinite(score) || score is < 0 or > 10)
        throw new ArgumentOutOfRangeException(nameof(score));

    return score switch
    {
        >= 9 => "A",
        >= 7 => "B",
        >= 5 => "C",
        _ => "D",
    };
}
```

Switch expression deve cobrir entradas; padrões tornam tipo, forma e guardas
explícitos:

```csharp
string Describe(object? value) => value switch
{
    null => "ausente",
    int number when number < 0 => "inteiro negativo",
    int => "inteiro",
    string { Length: 0 } => "texto vazio",
    string => "texto",
    _ => "outro",
};
```

Laços:

```csharp
for (int index = 0; index < values.Count; index++) { }
foreach (string value in values) { }
while (queue.Count > 0) { queue.Dequeue(); }
```

Não modifique estruturalmente `List<T>` durante `foreach`. Produza outra coleção,
use `RemoveAll` ou controle índice/iterador conscientemente.

## 6. Métodos, parâmetros e contratos

```csharp
static long CalculateTotal(
    IReadOnlyCollection<long> values,
    int discountPercent = 0)
{
    ArgumentNullException.ThrowIfNull(values);
    if (discountPercent is < 0 or > 100)
        throw new ArgumentOutOfRangeException(nameof(discountPercent));

    long subtotal = 0;
    foreach (long value in values) subtotal = checked(subtotal + value);
    return checked(subtotal * (100 - discountPercent)) / 100;
}
```

O padrão é passagem por valor. `ref`, `out` e `in` mudam a semântica:

- `ref`: lê/escreve a variável do chamador;
- `out`: deve atribuir antes de retornar;
- `in`: referência somente leitura, útil com structs grandes em casos medidos.

Prefira retorno claro a múltiplos `out`; tuples nomeadas podem agrupar resultados:

```csharp
static (int Minimum, int Maximum) Limits(IEnumerable<int> values) { /* ... */ }
```

Parâmetros opcionais são gravados no call site; mudar o default de uma biblioteca
pode exigir recompilar consumidores. Um options object escala melhor.

## 7. Arrays e coleções genéricas

```csharp
int[] scores = [10, 8, 4];
var names = new List<string> { "Ana", "Bia" };
var tags = new HashSet<string>(StringComparer.OrdinalIgnoreCase);
var byId = new Dictionary<long, TaskItem>();
var queue = new Queue<TaskItem>();
```

- array: tamanho fixo, acesso por índice O(1);
- `List<T>`: sequência dinâmica, append amortizado O(1);
- `Dictionary<TKey,TValue>`: lookup médio O(1);
- `HashSet<T>`: unicidade/pertencimento médio O(1);
- `Queue<T>`/`Stack<T>`: fila/pilha.

Escolha o comparador de string explicitamente em conjuntos/dicionários técnicos.
Exponha `IReadOnlyList<T>`/`IReadOnlyDictionary` quando o consumidor só lê. Isso
impede mutação pela interface, mas não é snapshot nem imutabilidade profunda.

Coleções em `System.Collections.Immutable` são outra opção quando a dependência
e o custo fazem sentido.

## 8. LINQ e execução adiada

```csharp
IEnumerable<string> activeNames = users
    .Where(user => user.Active)
    .Select(user => user.Name)
    .OrderBy(name => name, StringComparer.Ordinal);
```

Muitas operações LINQ são lazy: a fonte só é percorrida no `foreach`, e pode ser
percorrida novamente a cada enumeração. Se precisa de snapshot:

```csharp
List<string> snapshot = activeNames.ToList();
```

Materializar consome memória. Evite enumerar `IEnumerable<T>` múltiplas vezes
quando ele representa banco, arquivo, rede ou gerador com efeitos. Documente se
o método consome uma vez.

`Select` transforma, `Where` filtra, `Aggregate` reduz. Um laço explícito é
melhor para fluxo ramificado, contexto de erro ou otimização comprovada.

## 9. Records, classes, structs e invariantes

Record para dados com igualdade por valor:

```csharp
public sealed record Product
{
    public string Code { get; }
    public long PriceCents { get; }

    public Product(string code, long priceCents)
    {
        if (string.IsNullOrWhiteSpace(code))
            throw new ArgumentException("código obrigatório", nameof(code));
        if (priceCents < 0)
            throw new ArgumentOutOfRangeException(nameof(priceCents));
        Code = code.Trim();
        PriceCents = priceCents;
    }
}
```

As propriedades somente de leitura obrigam toda construção a passar pelo
construtor validado. Um `init` público permitiria que um inicializador ou uma
expressão `with` substituísse o valor depois da validação. `with` faz cópia rasa:
quando um record realmente expõe membros inicializáveis, uma lista interna
continua compartilhada entre original e cópia.

Classe para identidade e estado protegido:

```csharp
public sealed class Account
{
    public long BalanceCents { get; private set; }

    public Account(long initial)
    {
        if (initial < 0) throw new ArgumentOutOfRangeException(nameof(initial));
        BalanceCents = initial;
    }

    public void Deposit(long amount)
    {
        if (amount <= 0) throw new ArgumentOutOfRangeException(nameof(amount));
        BalanceCents = checked(BalanceCents + amount);
    }
}
```

Struct tem semântica de valor. Mantenha-o pequeno e preferencialmente imutável;
struct mutável copiado produz mudanças em uma cópia inesperada. `record struct`
combina valor com membros gerados.

## 10. Interfaces, delegates e composição

```csharp
public interface ITaskRepository
{
    Task<TaskItem?> FindAsync(long id, CancellationToken cancellationToken);
    Task SaveAsync(TaskItem item, CancellationToken cancellationToken);
}

public sealed class TaskService(ITaskRepository repository, TimeProvider clock)
{
    private readonly ITaskRepository _repository = repository;
    private readonly TimeProvider _clock = clock;
}
```

Passe dependências pelo construtor. Interface deve representar necessidade real
do consumidor, não espelhar toda uma implementação.

Delegates são referências tipadas a funções. `Func<T,...>`, `Action<T>` e events
permitem callbacks; listeners mantêm referências e precisam ser removidos quando
o ciclo de vida exige.

Prefira composição a herança para reuso. Herança exige relação substituível e
contrato estável, não apenas métodos em comum.

## 11. Exceções e resultados esperados

Use exceção quando o método não cumpre o contrato:

```csharp
try
{
    return ParseConfiguration(text);
}
catch (FormatException exception)
{
    throw new ConfigurationException("configuração inválida", exception);
}
```

Capture tipos específicos e preserve `InnerException`. Não use `catch
(Exception) {}` para esconder bugs. Para uma falha comum esperada, `TryParse`,
resultado discriminado ou coleção vazia pode ser mais adequado.

Filtros permitem decidir sem perder stack:

```csharp
catch (IOException exception) when (exception.HResult == KnownCode)
{
    // recuperação específica
}
```

`throw;` relança preservando stack; `throw exception;` a reinicia e deve ser
evitado.

## 12. IDisposable e vida útil de recursos

GC não fecha arquivo/socket em momento previsível. `using` garante `Dispose`:

```csharp
using FileStream stream = File.OpenRead(path);
using var reader = new StreamReader(stream);
string content = reader.ReadToEnd();
```

Para recursos assíncronos:

```csharp
await using FileStream stream = new(
    path,
    FileMode.Open,
    FileAccess.Read,
    FileShare.Read,
    bufferSize: 4096,
    useAsync: true);
```

Quem cria normalmente possui e descarta, salvo contrato explícito. Não descarte
dependência injetada se o chamador controla seu ciclo.

## 13. Async/await, cancelamento e concorrência

```csharp
public static async Task<string> ReadTextAsync(
    HttpClient client,
    Uri uri,
    CancellationToken cancellationToken)
{
    using HttpResponseMessage response =
        await client.GetAsync(uri, cancellationToken);
    response.EnsureSuccessStatusCode();
    return await response.Content.ReadAsStringAsync(cancellationToken);
}
```

`async` não cria thread automaticamente. A máquina de estados libera a thread
durante I/O aguardável. Evite `.Result`/`.Wait()`; propague async até a entrada.

Receba `CancellationToken` e passe adiante. Cancelamento é cooperativo, não
garantia de rollback. Defina timeout e estado após cancelamento.

`Task.WhenAll` coordena tarefas concorrentes, mas não limita quantas foram
iniciadas. Use `SemaphoreSlim`, `Channel<T>` ou worker pool para backpressure.
CPU-bound pode usar paralelismo após medição; estado compartilhado ainda exige
locks, atomics ou desenho sem compartilhamento.

Reutilize `HttpClient` ou use factory apropriada em aplicações hospedadas; criar
um cliente por requisição pode desperdiçar conexões.

## 14. Arquivos e JSON

```csharp
string json = await File.ReadAllTextAsync(path, cancellationToken);
TaskItem[]? raw = JsonSerializer.Deserialize<TaskItem[]>(json);
TaskItem[] tasks = raw ?? throw new InvalidDataException("JSON sem tarefas");
```

Desserialização não substitui validação de domínio. Limite tamanho/profundidade,
aceite propriedades previstas e valide cada objeto.

Escrita mais segura:

```csharp
string temporary = path + ".tmp";
await File.WriteAllTextAsync(temporary, json, Encoding.UTF8, cancellationToken);
File.Move(temporary, path, overwrite: true);
```

Substituição no mesmo volume reduz arquivo parcial, mas durabilidade, locks e
backup precisam de desenho próprio.

Use `Path.GetFullPath(Path.Combine(root, userPart))` e confirme que o resultado
permanece sob a raiz autorizada antes de acessar caminho derivado do usuário.

## 15. Organização de solução

```text
Agenda.sln
├── src/
│   ├── Agenda.Domain/
│   ├── Agenda.Application/
│   ├── Agenda.Infrastructure/
│   └── Agenda.Cli/
└── tests/
    └── Agenda.Tests/
```

```bash
dotnet new sln -n Agenda
dotnet new classlib -n Agenda.Domain
dotnet new mstest -n Agenda.Tests
dotnet sln add Agenda.Domain Agenda.Tests
dotnet add Agenda.Tests reference Agenda.Domain
dotnet test
```

Domínio não deve depender de console, banco, web ou framework. Infraestrutura
implementa contratos. Evite criar projetos/camadas sem dependência real; a
separação serve ao código, não ao diagrama.

Fixe dependências e versione lockfile quando a política exigir builds
reproduzíveis. Revise pacotes transitivos e não adicione biblioteca para função
que a BCL resolve claramente.

## 16. Modelo de memória e GC

O runtime rastreia objetos gerenciados alcançáveis e coleta os demais por
gerações. Pontos importantes:

- objeto vivo em cache/event handler não é coletado;
- Large Object Heap tem custos próprios;
- finalizer é fallback caro, não método normal de cleanup;
- `IDisposable` resolve recurso externo, não “libera qualquer objeto”;
- boxing converte value type para objeto e pode alocar;
- spans (`Span<T>`) permitem views de memória com regras restritas de vida útil.

Não escolha `struct`, pool ou `Span<T>` por moda. Primeiro meça com ferramentas;
depois otimize preservando correção e limites.

Concorrência segue o modelo de memória .NET: sem sincronização, outra thread
pode observar estado fora da ordem esperada. `lock`, `Interlocked`, `volatile`
e coleções concorrentes têm garantias distintas.

## 17. Testes, debugging e qualidade

Teste unitário com MSTest:

```csharp
[TestMethod]
public void Classify_RejectsScoreAboveTen()
{
    Assert.ThrowsException<ArgumentOutOfRangeException>(
        () => GradeAnalyzer.Classify(10.1));
}
```

Cubra caminho feliz, cada fronteira, null/vazio, NaN/infinito, overflow,
cancelamento e I/O em diretório temporário. Injete `TimeProvider` para tempo e
fake/repositório em memória para isolamento.

```bash
dotnet test
dotnet test --configuration Release
dotnet format --verify-no-changes
dotnet build -warnaserror
```

Use debugger para breakpoints, watch e exceptions; `dotnet-counters` e
`dotnet-trace` para comportamento do runtime. Logs devem ser estruturados e não
conter tokens, senhas ou dados sensíveis.

## 18. Leitura guiada do exemplo real

Abra [`exemplos/csharp/Program.cs`](../exemplos/csharp/Program.cs):

1. top-level statement apenas delega e devolve status;
2. `Concept` fecha o conjunto de classificações;
3. `GradeSummary` nomeia um resultado imutável;
4. `GradeAnalyzer.Validate` centraliza a invariante;
5. `Analyze` materializa conscientemente um `IEnumerable` uma vez;
6. `ReadOnlyDictionary` impede mutação pelo consumidor;
7. `GradeCli` recebe `TextWriter`, permitindo teste sem console global;
8. parsing usa cultura invariável e acrescenta posição ao erro;
9. código 2 representa uso/entrada inválida.

```bash
dotnet run \
  --project 00-Fundamentos/programacao/exemplos/csharp/CursoFundamentos.csproj \
  -- 10 8 4
```

Provoque `11`, `NaN`, texto e lista vazia. Observe `stderr` e status.

## 19. Exercícios progressivos

1. Adicione conceito `A+` e teste cada fronteira.
2. Calcule mediana sem mutar a coleção recebida.
3. Serialize `GradeSummary` com `System.Text.Json` e valide leitura.
4. Extraia biblioteca de domínio e projeto de testes.
5. Implemente repositórios em memória e arquivo para a mesma interface.
6. Faça uma CLI assíncrona com cancelamento e escrita temporária.
7. Crie Minimal API somente após estabilizar domínio e serviços.
8. Meça alocações antes/depois de uma otimização com span/pooling.

Critério de conclusão: o projeto compila sem warnings, nullability permanece
ativa, recursos são descartados, operações async aceitam cancelamento e toda
regra de domínio tem testes de limites.
