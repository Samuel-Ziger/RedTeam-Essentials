using System.Text.Json;
using System.Text.RegularExpressions;
using System.Text;

string? raw = null;
var format = "text";
for (var i = 0; i < args.Length; i++)
{
    if (args[i] == "--items" && i + 1 < args.Length) raw = args[++i];
    else if (args[i] == "--format" && i + 1 < args.Length) format = args[++i];
    else return Fail("argumento invalido");
}
if (raw is null) return Fail("--items obrigatorio");
if (Encoding.UTF8.GetByteCount(raw) > 1023) return Fail("items excede 1023 bytes");
var source = raw.Split(',', StringSplitOptions.None);
if (source.Length > 64) return Fail("items excede 64 IDs");
if (source.Any(value => !Regex.IsMatch(value, "^[A-Za-z0-9_-]+$"))) return Fail("ID invalido");
var items = source.Distinct(StringComparer.Ordinal).Order(StringComparer.Ordinal).ToArray();
if (format == "json") Console.WriteLine(JsonSerializer.Serialize(new { count = items.Length, items }));
else if (format == "text") Console.WriteLine($"count={items.Length} items={string.Join(',', items)}");
else return Fail("format invalido");
return 0;

static int Fail(string message)
{
    Console.Error.WriteLine($"error: {message}");
    return 2;
}
