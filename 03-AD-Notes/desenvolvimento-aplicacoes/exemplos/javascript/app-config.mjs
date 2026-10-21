import { parseArgs } from "node:util";
import { pathToFileURL } from "node:url";

const profiles = new Set(["development", "testing", "production"]);

export function resolveProfile(cliValue, environment) {
  if (cliValue !== undefined) {
    if (!profiles.has(cliValue)) throw new Error(`profile invalido: ${cliValue}`);
    return { profile: cliValue, source: "cli" };
  }
  if (Object.hasOwn(environment, "APP_PROFILE")) {
    const profile = environment.APP_PROFILE;
    if (!profiles.has(profile)) throw new Error(`APP_PROFILE invalido: ${profile}`);
    return { profile, source: "environment" };
  }
  return { profile: "development", source: "default" };
}

export function main(args = process.argv.slice(2), environment = process.env) {
  try {
    const { values } = parseArgs({
      args,
      options: {
        help: { type: "boolean" },
        profile: { type: "string" },
        format: { type: "string", default: "text" },
      },
      strict: true,
    });
    if (values.help) {
      console.log("Usage: app-config [--profile development|testing|production] [--format text|json]");
      return 0;
    }
    if (values.profile !== undefined && !profiles.has(values.profile)) {
      throw new Error(`profile invalido: ${values.profile}`);
    }
    if (!new Set(["text", "json"]).has(values.format)) {
      throw new Error(`format invalido: ${values.format}`);
    }
    const result = resolveProfile(values.profile, environment);
    console.log(
      values.format === "json"
        ? JSON.stringify(result)
        : `profile=${result.profile} source=${result.source}`,
    );
    return 0;
  } catch (error) {
    console.error(`error: ${error.message}`);
    return 2;
  }
}

if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) {
  process.exitCode = main();
}
