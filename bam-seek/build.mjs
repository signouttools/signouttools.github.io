import { build } from "esbuild";
import { readFile, writeFile, mkdir, readdir } from "node:fs/promises";
import { createHash } from "node:crypto";
import { fileURLToPath } from "node:url";
import { dirname, resolve } from "node:path";
import { igvPlugin, inflaterPlugin } from "./igv-build.mjs";
import { about } from "../scripts/about-content.mjs";
const root = dirname(fileURLToPath(import.meta.url));
const hash = (x) => createHash("sha256").update(x).digest("base64");
const escape = (x) =>
  x.replaceAll("&", "&amp;").replaceAll("<", "&lt;").replaceAll(">", "&gt;");
export async function buildBamSeek() {
  const worker = await build({
    entryPoints: [resolve(root, "worker.js")],
    bundle: true,
    write: false,
    format: "iife",
    platform: "browser",
    minify: true,
    plugins: [inflaterPlugin()],
  });
  await writeFile(
    resolve(root, "worker-bundle.js"),
    "export default " + JSON.stringify(worker.outputFiles[0].text),
  );
  const viewer = await build({
    entryPoints: [resolve(root, "viewer.js")],
    bundle: true,
    write: false,
    format: "iife",
    platform: "browser",
    minify: true,
    plugins: [igvPlugin()],
  });
  const viewerScript = viewer.outputFiles[0].text.replace(
    /<\/script/gi,
    "<\\/script",
  );
  const policy = (script) =>
    `default-src 'none'; script-src 'sha256-${hash(script)}'; style-src 'unsafe-inline'; img-src data: blob:; worker-src blob:; connect-src 'none'; font-src data:; base-uri 'none'; form-action 'none'; frame-src blob:;`;
  const viewerHtml = `<!doctype html><html lang="en"><head><meta charset="utf-8"><meta http-equiv="Content-Security-Policy" content="${policy(viewerScript)}"><meta name="viewport" content="width=device-width,initial-scale=1"><title>BAM Seek · IGV</title><style>body{margin:24px;font:16px/1.5 system-ui;color:#192f46;background:#f3f6fa}h1{font-size:22px}button{font:inherit;padding:8px;margin:4px}#igv{background:white}#filter-note,#viewer-status{font-size:14px}#viewer-status{white-space:pre-wrap}</style></head><body><h1 id="viewer-title">BAM Seek · IGV</h1><p id="filter-note"></p><button id="resort" disabled>Re-sort at variant</button><button id="recenter">Recenter variant</button><p id="viewer-status" role="status">Connecting to BAM Seek…</p><div id="igv"></div><script>${viewerScript}</script></body></html>`;
  await writeFile(
    resolve(root, "viewer-bundle.js"),
    "export default " + JSON.stringify(viewerHtml),
  );
  const app = await build({
    entryPoints: [resolve(root, "app.js")],
    bundle: true,
    write: false,
    format: "iife",
    platform: "browser",
    minify: true,
  });
  const script = app.outputFiles[0].text.replace(/<\/script/gi, "<\\/script"),
    style = await readFile(resolve(root, "style.css"), "utf8");
  const content = about["bam-seek"];
  const aboutHtml =
    content.sections
      .map(([h, p]) => `<h3>${escape(h)}</h3><p>${escape(p)}</p>`)
      .join("") + "<p>For research use only.</p>";
  let html = (await readFile(resolve(root, "index.template.html"), "utf8"))
    .replace("STYLE", () => style)
    .replace("<!--SCRIPT-->", () => `<script>${script}</script>`)
    .replace("ABOUT", () => aboutHtml);
  const parentPolicy = policy(script).replace(
    "; style-src",
    ` 'sha256-${hash(viewerScript)}'; style-src`,
  );
  html = html.replace(
    "<head>",
    `<head><meta http-equiv="Content-Security-Policy" content="${parentPolicy}">`,
  );
  const licenses = await notices();
  html +=
    "\n<!-- Third-party notices\n" +
    licenses.replaceAll("-->", "-- >") +
    "\n-->\n";
  await writeFile(
    resolve(root, "../scripts/third-party-notices/bam-seek.txt"),
    licenses,
  );
  await writeFile(resolve(root, "../tools/bam-seek.html"), html);
  return { html, viewerHtml };
}
async function notices() {
  let out =
    "BAM Seek browser distribution\nIncludes a local igv.js patch: downsample:false disables alignment sampling.\n\n";
  async function visit(dir) {
    for (const name of await readdir(dir)) {
      if (name.startsWith(".")) continue;
      const path = resolve(dir, name);
      if (name.startsWith("@")) {
        await visit(path);
        continue;
      }
      let p;
      try {
        p = JSON.parse(await readFile(resolve(path, "package.json"), "utf8"));
      } catch {
        continue;
      }
      if (["esbuild"].includes(p.name) || p.name.startsWith("@esbuild/"))
        continue;
      out += `${p.name} ${p.version}\nLicense: ${p.license || "See upstream"}\n`;
      for (const f of await readdir(path))
        if (/^(licen[sc]e|notice|copying)([-_.]|$)/i.test(f)) {
          try {
            out += await readFile(resolve(path, f), "utf8");
            out += "\n";
          } catch {}
        }
      out += "\n";
      try {
        await visit(resolve(path, "node_modules"));
      } catch (e) {
        if (e.code !== "ENOENT") throw e;
      }
    }
  }
  await visit(resolve(root, "node_modules"));
  return out;
}
if (
  process.argv[1] &&
  resolve(process.argv[1]) === fileURLToPath(import.meta.url)
) {
  await buildBamSeek();
  console.log("Built tools/bam-seek.html");
}
