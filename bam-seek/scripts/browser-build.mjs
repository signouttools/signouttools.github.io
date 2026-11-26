import { build } from "esbuild";
import { writeFile } from "node:fs/promises";
import { resolve, dirname } from "node:path";
import { fileURLToPath } from "node:url";
import { buildBamSeek } from "../build.mjs";
const root = resolve(dirname(fileURLToPath(import.meta.url)), "..");
await buildBamSeek();
await build({
  entryPoints: [resolve(root, "tests/browser.js")],
  bundle: true,
  format: "iife",
  outfile: resolve(root, "tests/browser-bundle.js"),
  platform: "browser",
});
await writeFile(
  resolve(root, "tests/browser.html"),
  '<!doctype html><html><head><meta charset="utf-8"><title>BAM Seek browser verification</title><style>body{font:16px system-ui;margin:24px}button{padding:12px;margin:6px}pre{white-space:pre-wrap}iframe{width:100%;height:600px}</style></head><body><h1>BAM Seek browser verification</h1><p>Synthetic local fixtures only. Launch each viewer from its button.</p><button id="run-tests" disabled>Run packaged application checks</button><button id="open-bai" disabled>Open high-depth BAI viewer</button><button id="open-csi" disabled>Open high-depth CSI viewer</button><button id="fallback-test" disabled>Test popup fallback</button><button id="open-twobit" disabled>Open 2bit reference viewer</button><button id="lifecycle-test" disabled>Test opener closure</button><div id="lifecycle-host"></div><pre id="report" role="status"></pre><div id="fallback"></div><iframe id="app" src="../../tools/bam-seek.html" title="Packaged BAM Seek"></iframe><script src="browser-bundle.js"></script></body></html>',
);
await build({
  entryPoints: [resolve(root, "tests/lifecycle.js")],
  bundle: true,
  format: "iife",
  outfile: resolve(root, "tests/lifecycle-bundle.js"),
  platform: "browser",
});
await writeFile(
  resolve(root, "tests/lifecycle.html"),
  '<button id="launch" disabled>Open lifecycle viewer</button><p id="status"></p><div id="fallback"></div><script src="lifecycle-bundle.js"></script>',
);
console.log("Browser harness: /bam-seek/tests/browser.html");
