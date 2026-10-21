import java.util.ArrayList;
import java.util.Collections;
import java.util.EnumMap;
import java.util.List;
import java.util.Locale;
import java.util.Map;
import java.util.Objects;

/**
 * Analisador de notas autocontido: domínio tipado, coleções, validação e CLI.
 *
 * <p>A lógica de domínio não conhece System.in/out. Essa separação permite
 * reutilizá-la em outra interface e testá-la sem capturar o console.</p>
 */
public final class Fundamentos {
    /** Faixas em ordem pedagógica; enum evita strings inválidas no domínio. */
    public enum Conceito {
        A, B, C, D
    }

    /** Resultado imutável. O construtor defensivo impede mutação indireta. */
    public record Resumo(
            int quantidade,
            double media,
            double menor,
            double maior,
            Map<Conceito, Integer> frequencias) {
        public Resumo {
            if (quantidade <= 0) {
                throw new IllegalArgumentException("quantidade deve ser positiva");
            }
            frequencias = Collections.unmodifiableMap(new EnumMap<>(frequencias));
        }
    }

    private Fundamentos() {
        // Classe utilitária: não há estado de instância.
    }

    public static double validarNota(double nota) {
        if (!Double.isFinite(nota) || nota < 0 || nota > 10) {
            throw new IllegalArgumentException("nota deve estar entre 0 e 10");
        }
        return nota;
    }

    public static Conceito classificar(double nota) {
        double valor = validarNota(nota);
        if (valor >= 9) return Conceito.A;
        if (valor >= 7) return Conceito.B;
        if (valor >= 5) return Conceito.C;
        return Conceito.D;
    }

    /** API textual preservada para consumidores do primeiro exemplo. */
    public static String conceito(double nota) {
        return classificar(nota).name();
    }

    public static Resumo analisar(List<Double> notas) {
        Objects.requireNonNull(notas, "notas");
        if (notas.isEmpty()) {
            throw new IllegalArgumentException("informe ao menos uma nota");
        }

        Map<Conceito, Integer> frequencias = new EnumMap<>(Conceito.class);
        for (Conceito faixa : Conceito.values()) frequencias.put(faixa, 0);

        double total = 0;
        double menor = Double.POSITIVE_INFINITY;
        double maior = Double.NEGATIVE_INFINITY;
        for (Double nota : notas) {
            if (nota == null) throw new IllegalArgumentException("nota não pode ser nula");
            double valor = validarNota(nota);
            total += valor;
            menor = Math.min(menor, valor);
            maior = Math.max(maior, valor);
            frequencias.merge(classificar(valor), 1, Integer::sum);
        }

        return new Resumo(notas.size(), total / notas.size(), menor, maior, frequencias);
    }

    public static double media(List<Double> notas) {
        return analisar(notas).media();
    }

    public static Map<String, Integer> frequencias(List<Double> notas) {
        Map<String, Integer> resultado = new java.util.LinkedHashMap<>();
        analisar(notas).frequencias().forEach((chave, valor) -> resultado.put(chave.name(), valor));
        return Collections.unmodifiableMap(resultado);
    }

    public static List<Double> converterArgumentos(String[] argumentos) {
        List<Double> notas = new ArrayList<>(argumentos.length);
        for (int indice = 0; indice < argumentos.length; indice++) {
            String texto = argumentos[indice];
            try {
                notas.add(validarNota(Double.parseDouble(texto)));
            } catch (IllegalArgumentException exception) {
                throw new IllegalArgumentException(
                        "argumento " + (indice + 1) + " inválido (" + texto + "): "
                                + exception.getMessage(),
                        exception);
            }
        }
        return List.copyOf(notas);
    }

    public static int executar(String[] args) {
        if (args.length == 0) {
            System.err.println("uso: java Fundamentos NOTA [NOTA ...]");
            return 2;
        }

        try {
            Resumo resumo = analisar(converterArgumentos(args));
            System.out.printf(
                    Locale.ROOT,
                    "media=%.2f conceitos={A=%d, B=%d, C=%d, D=%d}%n",
                    resumo.media(),
                    resumo.frequencias().get(Conceito.A),
                    resumo.frequencias().get(Conceito.B),
                    resumo.frequencias().get(Conceito.C),
                    resumo.frequencias().get(Conceito.D));
            return 0;
        } catch (IllegalArgumentException exception) {
            System.err.println("erro: " + exception.getMessage());
            return 2;
        }
    }

    public static void main(String[] args) {
        int status = executar(args);
        if (status != 0) System.exit(status);
    }
}
