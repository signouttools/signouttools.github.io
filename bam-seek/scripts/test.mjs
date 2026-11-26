import { build } from "esbuild";
import { execFileSync } from "node:child_process";
import { resolve, dirname } from "node:path";
import { fileURLToPath } from "node:url";
import { inflaterPlugin } from "../igv-build.mjs";
const root = resolve(dirname(fileURLToPath(import.meta.url)), "..");
await build({
  entryPoints: [resolve(root, "engine.js")],
  bundle: true,
  format: "esm",
  platform: "browser",
  outfile: resolve(root, "tests/engine-bundle.js"),
  plugins: [inflaterPlugin()],
});
execFileSync(
  process.execPath,
  [
    "--test",
    "core.test.js",
    "behavior.test.js",
    "integration.test.js",
    "build.test.js",
  ],
  { cwd: root, stdio: "inherit" },
);
