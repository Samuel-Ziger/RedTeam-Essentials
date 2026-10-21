using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Net.Http;
using System.Net.Http.Json;
using System.Text.Json;
using System.Text.Json.Serialization;
using System.Threading;
using System.Threading.Tasks;

try
{
    var baseUrl = Environment.GetEnvironmentVariable("INVENTORY_URL")
        ?? "http://127.0.0.1:8101";
    using var cancellation = new CancellationTokenSource(TimeSpan.FromSeconds(3));
    using var handler = new HttpClientHandler { AllowAutoRedirect = false };
    using var client = new HttpClient(handler)
    {
        BaseAddress = new Uri(baseUrl.TrimEnd('/') + "/", UriKind.Absolute),
        Timeout = Timeout.InfiniteTimeSpan,
        MaxResponseContentBufferSize = 1_000_000,
    };
    client.DefaultRequestHeaders.Accept.ParseAdd("application/json");
    client.DefaultRequestHeaders.UserAgent.ParseAdd("rte-csharp-client/1");

    using var response = await client.GetAsync("health/live", cancellation.Token);
    if (!response.IsSuccessStatusCode)
    {
        var problem = await response.Content.ReadAsStringAsync(cancellation.Token);
        throw new HttpRequestException($"HTTP {(int)response.StatusCode}: {problem}");
    }

    var health = await response.Content.ReadFromJsonAsync<HealthResponse>(
        cancellationToken: cancellation.Token
    ) ?? throw new InvalidDataException("resposta de health vazia");

    if (health.Status != "ok")
    {
        throw new InvalidDataException("contrato de health incompatível");
    }

    using var productsResponse = await client.GetAsync(
        "api/v1/products?limit=5",
        cancellation.Token
    );
    productsResponse.EnsureSuccessStatusCode();
    var page = await productsResponse.Content.ReadFromJsonAsync<ProductPage>(
        cancellationToken: cancellation.Token
    ) ?? throw new InvalidDataException("página vazia");

    var requestId = response.Headers.TryGetValues("X-Request-ID", out var values)
        ? values.FirstOrDefault()
        : "-";
    Console.WriteLine($"health={health.Status} request_id={requestId}");
    Console.WriteLine($"produtos={page.Items.Count} proximo_cursor={page.NextCursor}");
    foreach (var product in page.Items)
    {
        if (string.IsNullOrWhiteSpace(product.Sku) || string.IsNullOrWhiteSpace(product.Name))
        {
            throw new InvalidDataException("item de produto incompatível com o contrato");
        }
        Console.WriteLine($"- {product.Sku}: {product.Name} (estoque={product.Stock})");
    }
}
catch (Exception error) when (
    error is HttpRequestException
        or InvalidDataException
        or OperationCanceledException
        or JsonException
        or UriFormatException
)
{
    Console.Error.WriteLine($"erro: {error.Message}");
    return 1;
}

return 0;

internal sealed record HealthResponse(
    [property: JsonPropertyName("status")] string Status
);

internal sealed record ProductPage(
    [property: JsonPropertyName("items")] IReadOnlyList<Product> Items,
    [property: JsonPropertyName("nextCursor")] string? NextCursor
);

internal sealed record Product(
    [property: JsonPropertyName("sku")] string Sku,
    [property: JsonPropertyName("name")] string Name,
    [property: JsonPropertyName("stock")] int Stock
);
