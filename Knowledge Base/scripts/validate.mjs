import { readFile, readdir } from 'node:fs/promises';
import { fileURLToPath } from 'node:url';
import path from 'node:path';

const root = fileURLToPath(new URL('../', import.meta.url));
const schema = JSON.parse(await readFile(path.join(root, 'schemas/knowledge-base.schema.json'), 'utf8'));
const errors = [];
const fail = (at, message) => errors.push(`${at}: ${message}`);
const same = (a, b) => JSON.stringify(a) === JSON.stringify(b);
const typeOf = value => value === null ? 'null' : Array.isArray(value) ? 'array' : typeof value === 'number' && Number.isInteger(value) ? 'integer' : typeof value;

// Dependency-free validation for this contract's explicit keyword subset.
// Fail on new unsupported keywords so schema changes cannot silently bypass checks.
const keywords = new Set(['$schema', '$id', '$defs', '$ref', 'title', 'description', 'type', 'properties', 'required', 'additionalProperties', 'items', 'minItems', 'uniqueItems', 'minLength', 'minimum', 'pattern', 'enum', 'const', 'allOf', 'if', 'then']);
function inspectSchema(node) {
  for (const key of Object.keys(node)) if (!keywords.has(key)) throw new Error(`Unsupported schema keyword: ${key}`);
  for (const child of Object.values(node.properties || {})) inspectSchema(child);
  for (const child of Object.values(node.$defs || {})) inspectSchema(child);
  if (node.items) inspectSchema(node.items);
  for (const child of node.allOf || []) inspectSchema(child);
  if (node.if) inspectSchema(node.if);
  if (node.then) inspectSchema(node.then);
}
inspectSchema(schema);
function validate(value, rule, at, output = errors) {
  const error = message => output.push(`${at}: ${message}`);
  if (rule.$ref) {
    const name = rule.$ref.replace('#/$defs/', '');
    if (!schema.$defs[name]) throw new Error(`Unknown schema reference: ${rule.$ref}`);
    validate(value, schema.$defs[name], at, output); return;
  }
  const actualType = typeOf(value);
  if (rule.type && ![rule.type].flat().some(t => t === actualType || (t === 'number' && actualType === 'integer'))) { error(`expected ${JSON.stringify(rule.type)}, received ${actualType}`); return; }
  if (Object.hasOwn(rule, 'const') && !same(value, rule.const)) error('unexpected constant');
  if (rule.enum && !rule.enum.some(item => same(item, value))) error('value outside enum');
  if (typeof value === 'string') {
    if (value.length < (rule.minLength || 0)) error('string too short');
    if (rule.pattern && !new RegExp(rule.pattern).test(value)) error(`does not match ${rule.pattern}`);
  }
  if (typeof value === 'number' && value < rule.minimum) error('number below minimum');
  if (Array.isArray(value)) {
    if (value.length < (rule.minItems || 0)) error('array too short');
    if (rule.uniqueItems && new Set(value.map(item => JSON.stringify(item))).size !== value.length) error('duplicate array items');
    if (rule.items) value.forEach((item, index) => validate(item, rule.items, `${at}[${index}]`, output));
  }
  if (actualType === 'object') {
    for (const key of rule.required || []) if (!Object.hasOwn(value, key)) error(`missing ${key}`);
    for (const [key, item] of Object.entries(value)) {
      if (rule.properties?.[key]) validate(item, rule.properties[key], `${at}.${key}`, output);
      else if (rule.additionalProperties === false) error(`unexpected property ${key}`);
    }
  }
  for (const child of rule.allOf || []) validate(value, child, at, output);
  if (rule.if) {
    const conditionErrors = [];
    validate(value, rule.if, at, conditionErrors);
    if (!conditionErrors.length && rule.then) validate(value, rule.then, at, output);
  }
}
async function readData(relative) {
  const resolved = path.resolve(root, 'data', relative);
  if (!resolved.startsWith(path.join(root, 'data') + path.sep)) throw new Error(`Unsafe manifest path: ${relative}`);
  return JSON.parse(await readFile(resolved, 'utf8'));
}
const manifest = await readData('manifest.json');
validate(manifest, schema.$defs.manifest, 'manifest');
if (errors.length) throw new Error(errors.join('\n'));
const [genes, variants, diseases, sources, panels] = await Promise.all([
  Promise.all(manifest.gene_files.map(readData)), Promise.all(manifest.variant_files.map(readData)),
  readData(manifest.disease_file), readData(manifest.source_file), readData(manifest.panel_file)
]);
validate({manifest, genes, variants, diseases, sources, panels}, schema, 'dataset');
if (manifest.gene_index_file) {
  const index = await readData(manifest.gene_index_file);
  if (!same(index, genes)) fail('gene_index_file', 'generated index differs from authoritative gene files');
}
if (errors.length) throw new Error(errors.join('\n'));
for (const [label, records] of Object.entries({genes, variants, diseases, sources, panels})) {
  if (new Set(records.map(item => item.id)).size !== records.length) fail(label, 'duplicate record IDs');
}
if (new Set(genes.map(g => g.symbol)).size !== genes.length) fail('genes', 'duplicate approved symbols');
const maps = Object.fromEntries(Object.entries({genes, diseases, sources, panels}).map(([key, records]) => [key, new Map(records.map(r => [r.id, r]))]));
function walk(value, at) {
  if (Array.isArray(value)) return value.forEach((v, i) => walk(v, `${at}[${i}]`));
  if (!value || typeof value !== 'object') return;
  for (const [key, item] of Object.entries(value)) {
    if (key === 'source_ids') for (const id of item) if (!maps.sources.has(id)) fail(at, `unknown source ${id}`);
    if (key === 'disease_id' && !maps.diseases.has(item)) fail(at, `unknown disease ${item}`);
    if (key === 'gene_id' && !maps.genes.has(item)) fail(at, `unknown gene ${item}`);
    if (key === 'panel_id' && !maps.panels.has(item)) fail(at, `unknown panel ${item}`);
    if (key.endsWith('_on') && typeof item === 'string') {
      const parsed = new Date(item);
      if (!Number.isFinite(parsed.getTime()) || parsed.toISOString().slice(0, 10) !== item) fail(at, `invalid calendar date ${item}`);
    }
    walk(item, `${at}.${key}`);
  }
}
walk({genes, variants, diseases, sources, panels, manifest}, 'dataset');
for (const d of diseases) {
  const seen = new Set([d.id]); let parent = d.parent_id;
  while (parent) {
    if (!maps.diseases.has(parent)) { fail(d.id, `unknown parent ${parent}`); break; }
    if (seen.has(parent)) { fail(d.id, 'disease hierarchy cycle'); break; }
    seen.add(parent); parent = maps.diseases.get(parent).parent_id;
  }
}
for (const g of genes) {
  if (g.germline_status === 'established' && !g.germline_associations.length) fail(g.id, 'established germline status requires a disease association');
  if (g.germline_status === 'not_established_in_reviewed_sources' && g.germline_associations.length) fail(g.id, 'germline status conflicts with disease associations');
  for (const [key, category] of [['germline_associations', 'constitutional'], ['mosaic_associations', 'mosaic']]) {
    for (const a of g[key]) if (maps.diseases.get(a.disease_id)?.category !== category) fail(g.id, `${key} contains an incorrectly typed disease`);
  }
  for (const a of g.somatic_associations) if (['constitutional', 'mosaic'].includes(maps.diseases.get(a.disease_id)?.category)) fail(g.id, 'non-somatic disease in tumor associations');
  for (const m of g.panel_memberships) {
    const panel = maps.panels.get(m.panel_id);
    if (panel && (panel.acquisition_status === 'candidate' || !panel.exact_list_url || panel.version !== m.panel_version)) fail(g.id, 'panel membership requires an acquired exact list and matching version');
  }
}
for (const v of variants) {
  const gene = maps.genes.get(v.gene_id);
  if (gene && !gene.somatic_associations.some(a => a.disease_id === v.disease_id)) fail(v.id, 'comment context must have a cited gene-level somatic association');
  if (['constitutional', 'mosaic'].includes(maps.diseases.get(v.disease_id)?.category)) fail(v.id, 'variant comment requires a tumor context');
}
if (manifest.release_status === 'approved' && [...genes, ...variants].some(r => r.editorial.status !== 'approved')) fail('manifest', 'approved release contains unapproved records');
for (const [folder, files] of [['genes', manifest.gene_files], ['variants', manifest.variant_files]]) {
  const actual = (await readdir(path.join(root, 'data', folder))).filter(f => f.endsWith('.json')).map(f => `${folder}/${f}`);
  if (actual.some(f => !files.includes(f))) fail(folder, 'JSON record omitted from manifest');
}
if (errors.length) { console.error(errors.join('\n')); process.exitCode = 1; }
else console.log(`Validated ${genes.length} genes, ${variants.length} comments, ${diseases.length} diseases, ${sources.length} sources, and ${panels.length} panel definitions. All entries remain drafts.`);
