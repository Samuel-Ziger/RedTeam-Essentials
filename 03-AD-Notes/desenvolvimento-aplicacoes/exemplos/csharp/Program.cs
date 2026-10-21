namespace AppConfigExample;

internal static class Program
{
    private static readonly HashSet<string> Profiles =
        new(StringComparer.Ordinal) { "development", "testing", "production" };

    private static int Fail(string message)
    {
        Console.Error.WriteLine($"error: {message}");
        return 2;
    }

    private static int Main(string[] args)
    {
        string? profile = null;
        var format = "text";

        for (var index = 0; index < args.Length; index++)
        {
            switch (args[index])
            {
                case "--help":
                    Console.WriteLine(
                        "Usage: app-config [--profile development|testing|production] [--format text|json]"
                    );
                    return 0;
                case "--profile" when index + 1 < args.Length:
                    profile = args[++index];
                    break;
                case "--profile":
                    return Fail("--profile exige um valor");
                case "--format" when index + 1 < args.Length:
                    format = args[++index];
                    break;
                case "--format":
                    return Fail("--format exige um valor");
                default:
                    return Fail($"opcao desconhecida: {args[index]}");
            }
        }

        string source;
        if (profile is not null)
        {
            source = "cli";
        }
        else if (Environment.GetEnvironmentVariable("APP_PROFILE") is { } environmentProfile)
        {
            profile = environmentProfile;
            source = "environment";
        }
        else
        {
            profile = "development";
            source = "default";
        }

        if (!Profiles.Contains(profile))
        {
            return Fail($"profile invalido: {profile}");
        }
        if (format is not ("text" or "json"))
        {
            return Fail($"format invalido: {format}");
        }

        Console.WriteLine(
            format == "json"
                ? $"{{\"profile\":\"{profile}\",\"source\":\"{source}\"}}"
                : $"profile={profile} source={source}"
        );
        return 0;
    }
}
