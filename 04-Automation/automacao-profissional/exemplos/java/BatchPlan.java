import java.util.Arrays;
import java.util.List;
import java.util.TreeSet;
import java.nio.charset.StandardCharsets;
import java.util.regex.Pattern;

public final class BatchPlan {
    private static final Pattern ID = Pattern.compile("[A-Za-z0-9_-]+");
    private BatchPlan() {}

    public static void main(String[] args) {
        String raw = null;
        String format = "text";
        for (int i = 0; i < args.length; i++) {
            if (args[i].equals("--items") && i + 1 < args.length) raw = args[++i];
            else if (args[i].equals("--format") && i + 1 < args.length) format = args[++i];
            else System.exit(fail("argumento invalido"));
        }
        if (raw == null) System.exit(fail("--items obrigatorio"));
        if (raw.getBytes(StandardCharsets.UTF_8).length > 1023) {
            System.exit(fail("items excede 1023 bytes"));
        }
        List<String> source = Arrays.asList(raw.split(",", -1));
        if (source.size() > 64) System.exit(fail("items excede 64 IDs"));
        if (source.stream().anyMatch(value -> !ID.matcher(value).matches())) {
            System.exit(fail("ID invalido"));
        }
        List<String> items = List.copyOf(new TreeSet<>(source));
        if (format.equals("json")) {
            System.out.printf("{\"count\":%d,\"items\":[\"%s\"]}%n", items.size(), String.join("\",\"", items));
        } else if (format.equals("text")) {
            System.out.printf("count=%d items=%s%n", items.size(), String.join(",", items));
        } else System.exit(fail("format invalido"));
    }

    private static int fail(String message) {
        System.err.println("error: " + message);
        return 2;
    }
}
