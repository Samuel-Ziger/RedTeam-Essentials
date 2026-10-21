namespace DependencyPlannerExample;

public sealed class DependencyGraph
{
    private readonly Dictionary<string, HashSet<string>> prerequisites = new();
    private readonly Dictionary<string, HashSet<string>> dependents = new();

    private static void ValidateNode(string node)
    {
        if (string.IsNullOrEmpty(node))
        {
            throw new ArgumentException("O identificador deve usar apenas ASCII seguro.", nameof(node));
        }
        for (var index = 0; index < node.Length; index++)
        {
            var value = node[index];
            var alphaNumeric = (value >= 'A' && value <= 'Z') ||
                (value >= 'a' && value <= 'z') || (value >= '0' && value <= '9');
            if (!alphaNumeric && (index == 0 || (value != '.' && value != '_' && value != '-')))
            {
                throw new ArgumentException(
                    "O identificador deve usar apenas ASCII seguro.", nameof(node));
            }
        }
    }

    public void AddNode(string node)
    {
        ValidateNode(node);
        prerequisites.TryAdd(node, new HashSet<string>(StringComparer.Ordinal));
        dependents.TryAdd(node, new HashSet<string>(StringComparer.Ordinal));
    }

    public void AddDependency(string task, string prerequisite)
    {
        ValidateNode(task);
        ValidateNode(prerequisite);
        AddNode(task);
        AddNode(prerequisite);
        prerequisites[task].Add(prerequisite);
        dependents[prerequisite].Add(task);
    }

    public IReadOnlyList<string> TopologicalOrder()
    {
        var indegree = prerequisites.ToDictionary(pair => pair.Key, pair => pair.Value.Count);
        var ready = new PriorityQueue<string, string>(StringComparer.Ordinal);
        foreach (var (task, degree) in indegree)
        {
            if (degree == 0)
            {
                ready.Enqueue(task, task);
            }
        }

        var result = new List<string>();
        while (ready.TryDequeue(out var task, out _))
        {
            result.Add(task);
            // A PriorityQueue decide a ordem global; ordenar a adjacencia aqui
            // seria redundante e pioraria o custo em grafos densos.
            foreach (var dependent in dependents[task])
            {
                indegree[dependent]--;
                if (indegree[dependent] == 0)
                {
                    ready.Enqueue(dependent, dependent);
                }
            }
        }

        if (result.Count != prerequisites.Count)
        {
            var blocked = indegree.Where(pair => pair.Value > 0)
                .Select(pair => pair.Key).Order(StringComparer.Ordinal);
            throw new InvalidOperationException($"ciclo detectado entre: {string.Join(", ", blocked)}");
        }
        return result;
    }
}

internal static class Program
{
    private static void RequireBefore(IReadOnlyList<string> order, string first, string second)
    {
        if (order.ToList().IndexOf(first) >= order.ToList().IndexOf(second))
        {
            throw new InvalidOperationException($"{first} deveria vir antes de {second}");
        }
    }

    private static void Main()
    {
        var graph = new DependencyGraph();
        graph.AddDependency("api", "modelo");
        graph.AddDependency("testes", "api");
        graph.AddDependency("release", "testes");
        graph.AddDependency("release", "docs");
        var order = graph.TopologicalOrder();
        RequireBefore(order, "modelo", "api");
        RequireBefore(order, "api", "testes");
        Console.WriteLine(string.Join(" -> ", order));

        var invalid = new DependencyGraph();
        try
        {
            invalid.AddDependency("api", " modelo");
            throw new InvalidOperationException("o identificador invalido deveria ser rejeitado");
        }
        catch (ArgumentException)
        {
            if (invalid.TopologicalOrder().Count != 0)
            {
                throw new InvalidOperationException("a operacao invalida nao pode mutar o grafo");
            }
        }

        var cyclic = new DependencyGraph();
        cyclic.AddDependency("A", "B");
        cyclic.AddDependency("B", "A");
        try
        {
            cyclic.TopologicalOrder();
            throw new InvalidOperationException("o ciclo deveria ser rejeitado");
        }
        catch (InvalidOperationException error) when (error.Message.StartsWith("ciclo", StringComparison.Ordinal))
        {
            Console.WriteLine(error.Message);
        }
    }
}
