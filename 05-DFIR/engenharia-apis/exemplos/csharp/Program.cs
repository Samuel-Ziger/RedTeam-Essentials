using System.Text.RegularExpressions;

static string Build(int limit, string? after, string? status)
{
    if (limit is < 1 or > 100) throw new ArgumentException("limit invalido");
    if (after is not null && (after.Length > 512 || !Regex.IsMatch(after, "^[A-Za-z0-9_-]+$")))
        throw new ArgumentException("after invalido");
    if (status is not null && status is not ("active" or "archived"))
        throw new ArgumentException("status invalido");
    var parts = new List<string> { $"limit={limit}" };
    if (after is not null) parts.Add($"after={after}");
    if (status is not null) parts.Add($"status={status}");
    return "GET /v1/items?" + string.Join("&", parts);
}

var values = new Dictionary<string, string>();
for (var index = 0; index < args.Length; index += 2)
{
    if (index + 1 >= args.Length) return Fail("valor ausente");
    if (args[index] is not ("--limit" or "--after" or "--status"))
        return Fail("argumento desconhecido");
    if (values.ContainsKey(args[index])) return Fail("argumento repetido");
    values[args[index]] = args[index + 1];
}
try
{
    if (!values.TryGetValue("--limit", out var raw) || !int.TryParse(raw, out var limit))
        return Fail("--limit obrigatorio");
    Console.WriteLine(Build(limit, values.GetValueOrDefault("--after"), values.GetValueOrDefault("--status")));
    return 0;
}
catch (ArgumentException error) { return Fail(error.Message); }

static int Fail(string message) { Console.Error.WriteLine(message); return 2; }
