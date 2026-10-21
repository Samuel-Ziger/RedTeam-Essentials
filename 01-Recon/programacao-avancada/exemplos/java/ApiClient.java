import java.io.IOException;
import java.io.InputStream;
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.time.Duration;
import java.nio.charset.StandardCharsets;
import java.util.concurrent.CompletableFuture;
import java.util.concurrent.CompletionException;

final class ApiClient {
    private static final Duration TIMEOUT = Duration.ofSeconds(3);
    private static final int MAX_BODY_CHARS = 1_000_000;

    private record ApiResponse(int status, String requestId, String body) {
    }

    private ApiClient() {
    }

    public static void main(String[] args) {
        try {
            String baseUrl = System.getenv().getOrDefault(
                    "INVENTORY_URL", "http://127.0.0.1:8101");
            HttpClient client = HttpClient.newBuilder()
                    .connectTimeout(TIMEOUT)
                    .followRedirects(HttpClient.Redirect.NEVER)
                    .build();

            CompletableFuture<ApiResponse> health = get(client, baseUrl, "/health/live");
            CompletableFuture<ApiResponse> products = get(
                    client, baseUrl, "/api/v1/products?limit=5");
            CompletableFuture.allOf(health, products).join();
            ApiResponse healthResponse = health.join();
            ApiResponse productResponse = products.join();
            requireSuccess(healthResponse);
            requireSuccess(productResponse);

            if (!healthResponse.body().matches(
                    "\\s*\\{\\s*\"status\"\\s*:\\s*\"ok\"\\s*}\\s*")) {
                throw new IllegalStateException("contrato de health incompatível");
            }
            System.out.printf("health=ok request_id=%s%n", healthResponse.requestId());
            System.out.printf("pagina=%s%n", productResponse.body());
        } catch (CompletionException | IllegalArgumentException | IllegalStateException error) {
            Throwable cause = error.getCause() == null ? error : error.getCause();
            System.err.println("erro: " + cause.getMessage());
            System.exit(1);
        }
    }

    private static CompletableFuture<ApiResponse> get(
            HttpClient client, String baseUrl, String path) {
        HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create(stripTrailingSlash(baseUrl) + path))
                .timeout(TIMEOUT)
                .header("Accept", "application/json")
                .header("User-Agent", "rte-java-client/1")
                .GET()
                .build();
        return client.sendAsync(request, HttpResponse.BodyHandlers.ofInputStream())
                .thenApply(response -> {
                    String body;
                    try (InputStream stream = response.body()) {
                        byte[] bytes = stream.readNBytes(MAX_BODY_CHARS + 1);
                        if (bytes.length > MAX_BODY_CHARS) {
                            throw new IOException("resposta maior que o limite de 1 MB");
                        }
                        body = new String(bytes, StandardCharsets.UTF_8);
                    } catch (IOException error) {
                        throw new CompletionException(error);
                    }
                    String requestId = response.headers()
                            .firstValue("X-Request-ID")
                            .orElse("-");
                    return new ApiResponse(response.statusCode(), requestId, body);
                });
    }

    private static void requireSuccess(ApiResponse response) {
        if (response.status() != 200) {
            throw new IllegalStateException(
                    "HTTP " + response.status() + ": " + response.body());
        }
    }

    private static String stripTrailingSlash(String value) {
        return value.endsWith("/") ? value.substring(0, value.length() - 1) : value;
    }
}
