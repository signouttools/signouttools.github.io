// Run production grouping/filtering against every source tumor ID in the corpus.
import assert from 'node:assert/strict';
import fs from 'node:fs';
import vm from 'node:vm';
const root = new URL('../', import.meta.url);
const read = file => JSON.parse(fs.readFileSync(new URL(file, root), 'utf8'));
function node(tag, attrs = {}) {
  return {tag, ...attrs, value: '', children: [], setAttribute(k, v) { this[k] = v; },
    append(...items) { this.children.push(...items); }, addEventListener() {},
    replaceChildren(...items) { this.children = items; this.value = ''; },
    get options() { return this.children; }};
}
const fields = Object.fromEntries(['search', 'category', 'tumor'].map(id => [id, node('select')]));
const context = vm.createContext({document: {getElementById: id => fields[id] ||= node('div'), createElement: node}, URLSearchParams});
vm.runInContext(fs.readFileSync(new URL('app.js', root), 'utf8').replace(/\ninit\(\);\s*$/, '\n'), context);
context.genes = read('data/gene-index.json');
context.records = read('data/fusion-browser.json').records;
context.hotspots = read('data/hotspot-index.json');
context.originals = [...read('data/diseases.json'), ...read('data/fusion-diseases.json')];
context.registry = read('data/tumor-type-aliases.json');
const run = code => vm.runInContext(code, context);
run(`state.genes = genes; state.fusions = records; state.hotspots = hotspots;
state.diseases = originals; state.diseaseMap = new Map(originals.map(d => [d.id, d]));
state.hotspotMap = new Map(hotspots.map(h => [h.gene_id, h]));
state.searchMap = new Map(genes.map(g => [g.id, '']));
populateTumors();`);
const before = fields.tumor.options.slice(1).map(o => o.value);
assert.equal(before.length, context.registry.reviewed_dropdown_entries);
run('configureTumorTypes(registry); populateTumors();');
const after = fields.tumor.options.slice(1);
const aliases = new Map(context.registry.groups.flatMap(g => g.member_ids.map(id => [id, g.canonical_id])));
const expected = new Set(before.map(id => aliases.get(id) || id));
assert.deepEqual(new Set(after.map(o => o.value)), expected);
assert.equal(after.length, before.length - context.registry.groups.reduce((n, g) => n + g.member_ids.length - 1, 0));
assert.equal(after.filter(o => /wilms/i.test(o.textContent)).length, 1);
assert.equal(after.find(o => /wilms/i.test(o.textContent)).textContent, 'Wilms tumor');
const key = s => s.toLowerCase().replace(/ \(hotspot cohort\)/g, '').replace(/[^a-z0-9]/g, '');
assert.equal(new Set(after.map(o => key(o.textContent))).size, after.length, 'No remaining spelling/punctuation/cohort-label duplicates');
for (const group of context.registry.groups) {
  fields.tumor.value = group.canonical_id;
  for (const id of group.member_ids) {
    context.sourceID = id;
    assert(run('matchesDisease(sourceID)'), `Canonical filter must include ${id}`);
    assert(run('siteInContext({disease_ids:[sourceID]})'), `Hotspot filter must include ${id}`);
    assert(run('fusionInContext({disease_ids:[sourceID]})'), `Fusion filter must include ${id}`);
    assert(run('variantInContext({disease_id:sourceID,includes_descendants:false})'), `Variant filter must include ${id}`);
    assert.equal(run('disease(sourceID).id'), group.canonical_id, 'Existing URL alias resolves');
    context.canonicalID = group.canonical_id;
    assert(run('isWithin(canonicalID, sourceID)'), 'Legacy alias works as ancestor');
  }
  const expectedGenes = context.genes.filter(g => g.somatic_associations.some(a => group.member_ids.includes(a.disease_id))).map(g => g.id);
  const matched = new Set(JSON.parse(run('JSON.stringify(matchingGenes().map(g=>g.id))')));
  for (const id of expectedGenes) assert(matched.has(id), `Merged filter lost gene ${id}`);
}
// A narrow filter still excludes broader categories and sibling subtypes.
fields.tumor.value = 'atlas-e-cxadeno';
context.sourceID = 'atlas-e-cxscc';
assert(!run('matchesDisease(sourceID)'));
context.sourceID = 'curation-b39cd30b0226';
assert(!run('matchesDisease(sourceID)'));
fields.tumor.value = 'aml';
context.sourceID = 'fusion-context-cda6797b5406';
assert(run('matchesDisease(sourceID)'), 'Canonical AML still includes fusion subtype');
fields.category.value = 'hematologic'; fields.tumor.value = '';
run('populateTumors();');
assert(fields.tumor.options.some(o => o.value === 'hotspots-cohort-lymph'), 'Lymphoid neoplasms use the hematologic category');
context.sourceID = 'curation-intogen-LNM';
assert(run('matchesDisease(sourceID)'), 'Alias inherits canonical category');
fields.category.value = ''; run(`state.mode='fusions'; populateTumors();`);
assert.equal(new Set(fields.tumor.options.map(o => o.textContent)).size, fields.tumor.options.length);
// Merging leukemia into leukemia/lymphoma must preserve children without self-cycles.
for (const id of ['atlas-h-ball', 'atlas-h-tall']) {
  fields.tumor.value = id; context.sourceID = id;
  assert(run('matchesDisease(sourceID)'));
}
for (const d of context.originals) {
  context.sourceID = d.id;
  assert(run(`(() => {let id=disease(sourceID).id;const seen=new Set();while(id){if(seen.has(id))return false;seen.add(id);id=disease(disease(id)?.parent_id)?.id;}return true;})()`), `Canonical parent cycle at ${d.id}`);
}
// Exercise actual initialization, including the registry load and old URL values.
context.loadFixture = file => Promise.resolve(read(`data/${file}`));
context.location = {search: '?tumor=curation-intogen-WT'};
await run(`loadJSON = loadFixture; render = () => {}; init();`);
assert.equal(fields.tumor.value, 'atlas-e-wilms', 'Bookmarked Wilms alias selects the merged option');
assert(!fields.entry, 'Initialization must finish without a load error');
assert(run(`state.searchMap.get(state.genes.find(g=>g.symbol==='WT1').id).includes("wilms' tumor")`), 'Original tumor wording remains searchable');
context.location.search = '?mode=fusions&tumor=fusion-context-ea801e61035d';
await run('init();');
assert.equal(fields.tumor.value, 'fusion-context-db1c59b8f11b', 'Fusion URL alias selects the merged option');
assert(!fields.entry, 'Fusion initialization must finish without a load error');
console.log(`Passed full tumor review: ${before.length} source options → ${after.length} options; all ${context.registry.groups.length} groups retain gene, hotspot, fusion, variant, category, parent and legacy-ID matching.`);
