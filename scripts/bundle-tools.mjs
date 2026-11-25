import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import { mkdir, readFile, writeFile } from 'node:fs/promises';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const site = fileURLToPath(new URL('../', import.meta.url));
const sources = resolve(process.argv[2] ?? resolve(site, '..'));
const notices = {
  fiq: await readFile(new URL('./third-party-notices/fiq.txt', import.meta.url), 'utf8'),
  phase: await readFile(new URL('./third-party-notices/phase.txt', import.meta.url), 'utf8'),
};
const tools = [
  ['CARA/index.html', 'cara', true],
  ['SARA/index.html', 'sara'],
  ['FIQ/index.html', 'fiq', true],
  ['phase/index.html', 'phase'],
  ['phase/automatic/index.html', 'phase-automatic'],
  ['phase/assembly/index.html', 'phase-assembly'],
  ['phase/specific/index.html', 'phase-specific'],
  ['sage/index.html', 'sage', true],
];

const csp = /(<meta\s+http-equiv="Content-Security-Policy"\s+content=")([^"]+)(")/i;
const scriptTag = /<script\b[^>]*?\bsrc="([^"]+)"[^>]*><\/script>/gi;
const styleTag = /<link\s+rel="stylesheet"\s+[^>]*\bhref="([^"]+)"[^>]*>/gi;

function digest(contents, algorithm = 'sha256') {
  return `${algorithm}-${createHash(algorithm).update(contents).digest('base64')}`;
}

function tightenPolicy(policy, name, hashes) {
  const directive = new RegExp(`(^|;\\s*)${name} 'self'(?=;| |$)`);
  assert.match(policy, directive, `Expected same-origin ${name} in source policy`);
  return policy.replace(directive, (_, separator) =>
    `${separator}${name} ${hashes.map(hash => `'${hash}'`).join(' ')}`);
}

function useClassicFiqWorker(contents) {
  // Chrome rejects FIQ's Blob module worker from file://. Its bundled worker
  // has no imports and can run as a classic worker under the same Blob-only CSP.
  const bootstrap = '"URL.revokeObjectURL(import.meta.url);"';
  const worker = /new Worker\((\w+),\{type:"module",name:(\w+\?\.name)\}\)/;
  assert.ok(contents.includes(bootstrap));
  assert.match(contents, worker);
  return contents
    .replace(bootstrap, '"URL.revokeObjectURL(self.location.href);"')
    .replace(worker, 'new Worker($1,{name:$2})');
}

async function bundle(source, html, name) {
  const scripts = [];
  const styles = [];
  async function asset(tag, path) {
    assert.match(path, /^(?:\.\/)?(?:[\w-]+\/)*[\w.-]+\.(?:js|css)$/);
    const bytes = await readFile(resolve(dirname(source), path));
    const integrity = tag.match(/\bintegrity="([^"]+)"/)?.[1];
    if (integrity) {
      assert.equal(digest(bytes, 'sha384'), integrity, `Integrity check failed for ${path}`);
    }
    return bytes.toString('utf8').replace(/\r\n?/g, '\n');
  }

  for (const [tag, path] of html.matchAll(styleTag)) {
    const contents = `\n${await asset(tag, path)}\n`;
    assert.doesNotMatch(contents, /<\/style\b/i);
    styles.push(digest(contents));
    html = html.replace(tag, () => `<style>${contents}</style>`);
  }

  for (const [tag, path] of html.matchAll(scriptTag)) {
    let contents = await asset(tag, path);
    assert.doesNotMatch(contents, /<\/script\b|<!--/i);
    const defer = /\sdefer(?=\s|>)/.test(tag);
    const module = /\stype="module"/.test(tag);
    if (name === 'fiq') contents = useClassicFiqWorker(contents);
    if (name === 'sage') {
      // The standalone release has no prior storage or service worker to migrate.
      const cleanup = /^  function clearLegacyBrowserPersistence\(\) \{\n[\s\S]*?^  \}\n\n/m;
      const call = /^    clearLegacyBrowserPersistence\(\);\n/m;
      assert.match(contents, cleanup);
      assert.match(contents, call);
      contents = contents.replace(cleanup, '').replace(call, '');
    }
    contents = `\n${contents}\n`;
    scripts.push(digest(contents));
    const inline = `<script${module ? ' type="module"' : ''}>${contents}</script>`;
    if (defer && !module) {
      assert.match(html, /<\/body>/i);
      html = html.replace(tag, '').replace(/<\/body>/i, end => `  ${inline}\n  ${end}`);
    } else {
      html = html.replace(tag, () => inline);
    }
  }

  assert.ok(scripts.length && styles.length, `Expected both JavaScript and CSS for ${name}`);
  assert.match(html, csp);
  return html.replace(csp, (_, open, original, close) => {
    assert.match(original, /(?:^|;\s*)connect-src 'none'(?:;|$)/);
    const style = /style-src 'self' 'unsafe-inline'(?=;|$)/;
    assert.match(original, style);
    const sheetHashes = styles.map(hash => `'${hash}'`).join(' ');
    let policy = tightenPolicy(original, 'script-src', scripts).replace(
      style,
      `style-src 'none'; style-src-elem ${sheetHashes}; style-src-attr 'unsafe-inline'`,
    );
    if (name === 'sage') {
      policy = policy
        .replace("default-src 'self'", "default-src 'none'")
        .replace("img-src 'self' data: blob:", 'img-src data: blob:')
        .replace("font-src 'self'", "font-src 'none'")
        .replace("base-uri 'self'", "base-uri 'none'");
    }
    return open + policy + close;
  });
}

function removePhaseNavigation(html, name) {
  // Other workflows are independently downloadable and linked from the directory.
  const navigation = {
    phase: /\s*<nav>\s*<a href="assembly\/index\.html">[\s\S]*?<\/nav>/,
    'phase-assembly': /\s*<a href="\.\.\/automatic\/index\.html">[^<]*<\/a\s*>/,
  }[name];
  if (!navigation) return html;
  assert.match(html, navigation);
  return html.replace(navigation, '');
}

for (const [path, name, needsBundling] of tools) {
  const source = resolve(sources, path);
  const original = await readFile(source, 'utf8');
  let html = needsBundling ? await bundle(source, original, name) : removePhaseNavigation(original, name);
  const notice = notices[name.split('-')[0]];
  if (notice) {
    assert.doesNotMatch(notice, /--!?>/);
    html += `\n<!-- Third-party notices\n\n${notice}-->\n`;
  }
  const destination = resolve(site, 'tools', `${name}.html`);
  await mkdir(dirname(destination), { recursive: true });
  await writeFile(destination, html);
  console.log(`tools/${name}.html`);
}
