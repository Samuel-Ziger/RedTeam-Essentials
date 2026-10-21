import { pathToFileURL } from "node:url";
import { parseArgs } from "node:util";

export function plan(raw) {
  const values = raw?.split(",") ?? [];
  if (raw !== undefined && Buffer.byteLength(raw, "utf8") > 1023) {
    throw new Error("items excede 1023 bytes");
  }
  if (values.length > 64) throw new Error("items excede 64 IDs");
  if (values.length === 0 || values.some((value) => !/^[A-Za-z0-9_-]+$/.test(value))) {
    throw new Error("items deve conter IDs separados por virgula");
  }
  return [...new Set(values)].sort();
}

export function main(args = process.argv.slice(2)) {
  try {
    const { values } = parseArgs({
      args,
      options: { items: { type: "string" }, format: { type: "string", default: "text" } },
      strict: true,
    });
    const items = plan(values.items);
    if (!new Set(["text", "json"]).has(values.format)) throw new Error("format invalido");
    console.log(
      values.format === "json"
        ? JSON.stringify({ count: items.length, items })
        : `count=${items.length} items=${items.join(",")}`,
    );
    return 0;
  } catch (error) {
    console.error(`error: ${error.message}`);
    return 2;
  }
}

if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) process.exitCode = main();
