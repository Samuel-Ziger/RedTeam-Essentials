import java.util.Set;

/** Entrada de aplicacao com precedencia, validacao e dois formatos de saida. */
public final class AppConfig {
    private static final Set<String> PROFILES = Set.of("development", "testing", "production");

    private AppConfig() {}

    private static void help() {
        System.out.println("Usage: AppConfig [--profile development|testing|production] [--format text|json]");
    }

    private static int fail(String message) {
        System.err.println("error: " + message);
        return 2;
    }

    public static void main(String[] args) {
        String profile = null;
        String format = "text";
        for (int index = 0; index < args.length; index++) {
            switch (args[index]) {
                case "--help":
                    help();
                    return;
                case "--profile":
                    if (++index == args.length) {
                        System.exit(fail("--profile exige um valor"));
                    }
                    profile = args[index];
                    break;
                case "--format":
                    if (++index == args.length) {
                        System.exit(fail("--format exige um valor"));
                    }
                    format = args[index];
                    break;
                default:
                    System.exit(fail("opcao desconhecida: " + args[index]));
            }
        }

        String source;
        if (profile != null) {
            source = "cli";
        } else if (System.getenv("APP_PROFILE") != null) {
            profile = System.getenv("APP_PROFILE");
            source = "environment";
        } else {
            profile = "development";
            source = "default";
        }

        if (!PROFILES.contains(profile)) {
            System.exit(fail("profile invalido: " + profile));
        }
        if (!format.equals("text") && !format.equals("json")) {
            System.exit(fail("format invalido: " + format));
        }

        if (format.equals("json")) {
            System.out.printf("{\"profile\":\"%s\",\"source\":\"%s\"}%n", profile, source);
        } else {
            System.out.printf("profile=%s source=%s%n", profile, source);
        }
    }
}
