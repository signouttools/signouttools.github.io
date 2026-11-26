import { test } from "node:test";
import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import { createHash } from "node:crypto";
import vm from "node:vm";
import { buildBamSeek } from "./build.mjs";
test("standalone and child script hashes match actual HTML and parse", async () => {
  const { html, viewerHtml } = await buildBamSeek();
  for (const doc of [html, viewerHtml]) {
    const policy = doc.match(
      /http-equiv="Content-Security-Policy" content="([^"]+)"/,
    )[1];
    assert.match(policy, /connect-src 'none'/);
    assert.doesNotMatch(doc, /<script[^>]+src=|<link[^>]+href=/);
    const scripts = [...doc.matchAll(/<script>([\s\S]*?)<\/script>/g)];
    assert.equal(scripts.length, 1);
    for (const [, body] of scripts) {
      new vm.Script(body);
      assert.ok(
        policy.includes(
          "sha256-" + createHash("sha256").update(body).digest("base64"),
        ),
        "script hash must match exact script bytes",
      );
    }
  }
  const worker = await readFile(
    new URL("./worker-bundle.js", import.meta.url),
    "utf8",
  );
  assert.doesNotMatch(worker, /WebAssembly|instantiateStreaming|\.wasm/);
  assert.match(html, /About BAM Seek/);
  assert.match(html, /Third-party notices/);
});
