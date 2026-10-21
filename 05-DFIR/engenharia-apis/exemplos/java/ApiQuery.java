import java.util.ArrayList;
import java.util.List;
import java.util.regex.Pattern;

public final class ApiQuery {
    private static final Pattern TOKEN = Pattern.compile("[A-Za-z0-9_-]+");

    private ApiQuery() {}

    static String build(int limit, String after, String status) {
        if (limit < 1 || limit > 100) throw new IllegalArgumentException("limit invalido");
        if (after != null && (after.length() > 512 || !TOKEN.matcher(after).matches())) {
            throw new IllegalArgumentException("after invalido");
        }
        if (status != null && !status.equals("active") && !status.equals("archived")) {
            throw new IllegalArgumentException("status invalido");
        }
        List<String> parts = new ArrayList<>();
        parts.add("limit=" + limit);
        if (after != null) parts.add("after=" + after);
        if (status != null) parts.add("status=" + status);
        return "GET /v1/items?" + String.join("&", parts);
    }

    public static void main(String[] args) {
        Integer limit = null;
        String after = null;
        String status = null;
        for (int i = 0; i < args.length; i += 2) {
            if (i + 1 >= args.length) fail("valor ausente");
            switch (args[i]) {
                case "--limit":
                    if (limit != null) fail("argumento repetido");
                    try {
                        limit = Integer.valueOf(args[i + 1]);
                    } catch (NumberFormatException error) {
                        fail("limit invalido");
                    }
                    break;
                case "--after":
                    if (after != null) fail("argumento repetido");
                    after = args[i + 1];
                    break;
                case "--status":
                    if (status != null) fail("argumento repetido");
                    status = args[i + 1];
                    break;
                default:
                    fail("argumento desconhecido");
            }
        }
        if (limit == null) fail("--limit obrigatorio");
        try {
            System.out.println(build(limit, after, status));
        } catch (IllegalArgumentException error) {
            fail(error.getMessage());
        }
    }

    private static void fail(String message) {
        System.err.println(message);
        System.exit(2);
    }
}
