using System.Collections.ObjectModel;
using System.Globalization;

return GradeCli.Run(args, Console.Out, Console.Error);

internal enum Concept
{
    A,
    B,
    C,
    D,
}

internal sealed record GradeSummary(
    int Count,
    double Average,
    double Minimum,
    double Maximum,
    IReadOnlyDictionary<Concept, int> Frequencies);

internal static class GradeAnalyzer
{
    public static double Validate(double grade)
    {
        if (!double.IsFinite(grade) || grade is < 0 or > 10)
        {
            throw new ArgumentOutOfRangeException(
                nameof(grade), grade, "nota deve estar entre 0 e 10");
        }

        return grade;
    }

    public static Concept Classify(double grade) => Validate(grade) switch
    {
        >= 9 => Concept.A,
        >= 7 => Concept.B,
        >= 5 => Concept.C,
        _ => Concept.D,
    };

    public static GradeSummary Analyze(IEnumerable<double> source)
    {
        ArgumentNullException.ThrowIfNull(source);

        // Materializar uma vez permite receber qualquer IEnumerable sem
        // enumerá-lo repetidamente (importante para streams e consultas LINQ).
        double[] grades = source.Select(Validate).ToArray();
        if (grades.Length == 0)
        {
            throw new ArgumentException("informe ao menos uma nota", nameof(source));
        }

        var frequencies = Enum
            .GetValues<Concept>()
            .ToDictionary(concept => concept, _ => 0);

        foreach (double grade in grades)
        {
            frequencies[Classify(grade)]++;
        }

        return new GradeSummary(
            grades.Length,
            grades.Average(),
            grades.Min(),
            grades.Max(),
            new ReadOnlyDictionary<Concept, int>(frequencies));
    }
}

internal static class GradeCli
{
    public static int Run(IReadOnlyList<string> arguments, TextWriter output, TextWriter error)
    {
        ArgumentNullException.ThrowIfNull(arguments);
        ArgumentNullException.ThrowIfNull(output);
        ArgumentNullException.ThrowIfNull(error);

        if (arguments.Count == 0)
        {
            error.WriteLine("uso: dotnet run -- NOTA [NOTA ...]");
            return 2;
        }

        try
        {
            var grades = arguments.Select(ParseGrade).ToArray();
            GradeSummary summary = GradeAnalyzer.Analyze(grades);
            output.WriteLine(
                string.Format(
                    CultureInfo.InvariantCulture,
                    "media={0:F2} conceitos={{A:{1},B:{2},C:{3},D:{4}}}",
                    summary.Average,
                    summary.Frequencies[Concept.A],
                    summary.Frequencies[Concept.B],
                    summary.Frequencies[Concept.C],
                    summary.Frequencies[Concept.D]));
            return 0;
        }
        catch (ArgumentException exception)
        {
            error.WriteLine($"erro: {exception.Message}");
            return 2;
        }
    }

    private static double ParseGrade(string text, int index)
    {
        if (!double.TryParse(
                text,
                NumberStyles.Float,
                CultureInfo.InvariantCulture,
                out double grade))
        {
            throw new ArgumentException(
                $"argumento {index + 1} não é um número válido: {text}",
                nameof(text));
        }

        try
        {
            return GradeAnalyzer.Validate(grade);
        }
        catch (ArgumentOutOfRangeException exception)
        {
            throw new ArgumentException(
                $"argumento {index + 1} inválido ({text}): {exception.Message}",
                nameof(text),
                exception);
        }
    }
}
