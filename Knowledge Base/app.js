/* The JSON records are authoritative. No patient data or persistent storage. */
'use strict';
const $ = id => document.getElementById(id);
const DISCLAIMER = 'Pathologist review needed — LLM-generated summary/review.';
const state = { genes: [], variants: [], diseases: [], sources: [], selected: null, letter: '', tab: 'gene', diseaseMap: new Map(), searchMap: new Map() };
Object.assign(state, {hotspots: [], hotspotMap: new Map(), hotspotCache: new Map(), disruptions: [], fda: []});
Object.assign(state, {mode: 'genes', fusions: [], fusionSources: [], fusionSearchMap: new Map(), fusionDiseases: []});
state.reportOverrides = {};
const categories = {solid: 'Solid tumors', hematologic: 'Hematologic neoplasms', cns: 'CNS tumors', pan_cancer: 'Multiple cancer types'};
const roleNames = {oncogene: 'Oncogene', tumor_suppressor: 'Tumor suppressor', metabolic_driver: 'Metabolic driver', other: 'Role not assigned'};
function el(tag, attrs = {}, text = '') {
  const node = document.createElement(tag);
  for (const [key, value] of Object.entries(attrs)) node.setAttribute(key, value);
  node.textContent = text;
  return node;
}
const normalize = text => text.toLowerCase().normalize('NFKD').replace(/[–—−]/g, '-');
const disease = id => state.diseaseMap.get(id);
function isWithin(id, ancestor) {
  const seen = new Set();
  while (id && !seen.has(id)) {
    if (id === ancestor) return true;
    seen.add(id);
    id = disease(id)?.parent_id;
  }
  return false;
}
function matchesDisease(id) {
  return (!$('category').value || disease(id)?.category === $('category').value) &&
    (!$('tumor').value || isWithin(id, $('tumor').value));
}
function variantInContext(variant) {
  if ($('category').value && disease(variant.disease_id)?.category !== $('category').value) return false;
  const selected = $('tumor').value;
  if (!selected || selected === variant.disease_id) return true;
  // A broad selection may display a more specific comment, with its own context visible.
  // A specific selection may inherit a broader comment only if explicitly permitted.
  return isWithin(variant.disease_id, selected) ||
    (variant.includes_descendants && isWithin(selected, variant.disease_id));
}
function commentsFor(gene) {
  return state.variants.filter(item => item.gene_id === gene.id && variantInContext(item));
}
function siteInContext(item) {
  return !($('category').value || $('tumor').value) || item.disease_ids.some(matchesDisease);
}
function fdaFor(gene) { return state.fda.filter(r => r.gene_ids.includes(gene.id)); }
function searchable(gene) {
  const associations = [...gene.germline_associations, ...gene.somatic_associations, ...gene.mosaic_associations];
  const terms = associations.flatMap(a => { const d = disease(a.disease_id); return d ? [d.name, ...d.synonyms] : []; });
  const variants = state.variants.filter(v => v.gene_id === gene.id).flatMap(v =>
    [v.label, v.selector.hgvs_c || '', v.selector.hgvs_p || '', ...v.selector.aliases, v.comment.text]);
  return normalize([gene.symbol, gene.name, ...gene.aliases, ...gene.roles, ...gene.pathways,
    ...Object.values(gene.report_summary || gene.summary).map(s => s.text), ...terms, ...variants,
    ...(state.hotspotMap.get(gene.id)?.terms || []),
    ...fdaFor(gene).map(r => `${r.therapy} ${r.biomarker} ${r.criteria}`),
    ...fusionsForGene(gene).flatMap(f => [f.label, ...f.aliases])].join(' '));
}
const fusionNormalize = text => normalize(text).replace(/[^a-z0-9]+/g, ' ').trim();
function fusionsForGene(gene) { return state.fusions.filter(f => f.partners.some(p => p.hgnc_id === gene.id)); }
function fusionInContext(fusion) {
  return !($('category').value || $('tumor').value) || fusion.disease_ids.some(matchesDisease);
}
function matchingFusions() {
  const tokens = fusionNormalize($('search').value).split(/\s+/).filter(Boolean);
  return state.fusions.filter(f => (!state.letter || f.label.startsWith(state.letter)) &&
    tokens.every(token => state.fusionSearchMap.get(f.id).includes(token)) && fusionInContext(f))
    .sort((a, b) => a.label.localeCompare(b.label));
}
function setMode(mode) {
  state.mode = mode === 'fusions' ? 'fusions' : 'genes'; state.letter = ''; state.selected = null;
  $('tumor').value = ''; populateTumors(); render();
}
function matchingGenes() {
  const tokens = normalize($('search').value.trim()).split(/\s+/).filter(Boolean);
  const filteringTumors = $('category').value || $('tumor').value;
  return state.genes.filter(gene => (!state.letter || gene.symbol.startsWith(state.letter)) &&
    tokens.every(token => state.searchMap.get(gene.id).includes(token)) &&
    (!filteringTumors || gene.somatic_associations.some(a => matchesDisease(a.disease_id)) ||
      state.hotspotMap.get(gene.id)?.disease_ids.some(matchesDisease) || fusionsForGene(gene).some(fusionInContext)))
    .sort((a, b) => {
      const q = normalize($('search').value.trim());
      return Number(normalize(b.symbol) === q) - Number(normalize(a.symbol) === q) || a.symbol.localeCompare(b.symbol);
    });
}
function updateURL() {
  const params = new URLSearchParams();
  for (const [key, value] of Object.entries({q: $('search').value.trim(), category: $('category').value, tumor: $('tumor').value, letter: state.letter, gene: state.selected, view: state.tab === 'variants' ? 'variants' : ''})) {
    if (value && key !== 'gene') params.set(key, value);
  }
  if (state.mode === 'genes' && state.tab === 'fusions') params.set('view', 'fusions');
  if (state.mode === 'fusions') { params.set('mode', 'fusions'); if (state.selected) params.set('fusion', state.selected); params.delete('view'); }
  else if (state.selected) params.set('gene', state.selected);
  history.replaceState(null, '', `${location.pathname}${params.size ? '?' + params : ''}`);
}
function populateTumors() {
  const previous = $('tumor').value;
  $('tumor').replaceChildren(el('option', {value: ''}, 'All tumor types'));
  const somaticIDs = new Set(state.mode === 'fusions' ? state.fusions.flatMap(f => f.disease_ids) : state.genes.flatMap(g => g.somatic_associations.map(a => a.disease_id)));
  if (state.mode === 'genes') {
    state.hotspots.forEach(h => h.disease_ids.forEach(id => somaticIDs.add(id)));
    state.fusions.forEach(f => f.disease_ids.forEach(id => somaticIDs.add(id)));
  }
  // Include the ancestors of linked somatic diseases so broad categories remain selectable.
  for (const id of [...somaticIDs]) {
    let parent = disease(id)?.parent_id;
    const seen = new Set();
    while (parent && !seen.has(parent)) { seen.add(parent); somaticIDs.add(parent); parent = disease(parent)?.parent_id; }
  }
  state.diseases.filter(d => somaticIDs.has(d.id) && (!$('category').value || d.category === $('category').value))
    .sort((a, b) => a.name.localeCompare(b.name))
    .forEach(d => $('tumor').append(el('option', {value: d.id}, d.name)));
  if ([...$('tumor').options].some(o => o.value === previous)) $('tumor').value = previous;
}
function renderAlphabet() {
  $('alphabet').replaceChildren();
  for (const letter of ['', ...'ABCDEFGHIJKLMNOPQRSTUVWXYZ']) {
    const button = el('button', {type: 'button', id: `letter-${letter || 'all'}`, 'aria-pressed': String(letter === state.letter), 'aria-label': letter ? `${state.mode === 'fusions' ? 'Fusions' : 'Genes'} starting with ${letter}` : 'All first letters'}, letter || 'All');
    button.disabled = !!letter && !(state.mode === 'fusions' ? state.fusions.some(f => f.label.startsWith(letter)) : state.genes.some(g => g.symbol.startsWith(letter)));
    button.addEventListener('click', () => { state.letter = letter; render(); });
    $('alphabet').append(button);
  }
}
function render() {
  const focusID = document.activeElement?.id;
  $('copy-status').textContent = '';
  for (const mode of ['genes', 'fusions']) $(`mode-${mode}`).setAttribute('aria-pressed', String(state.mode === mode));
  $('browse-title').textContent = state.mode === 'fusions' ? 'Browse fusions' : 'Browse genes';
  $('search').placeholder = state.mode === 'fusions' ? 'Fusion, partner, alias, tumor, or therapy…' : 'Gene, alias, pathway, disease, or hotspot…';
  $('search-help').textContent = state.mode === 'fusions' ? 'Try “EML4::ALK”, “ALK EML4”, “MLL”, or “synovial”. Either partner order finds the same catalog entry.' : 'Try “p53”, “MAPK”, “AML”, or “R132H”. All search words must match.';
  if (state.mode === 'fusions') { renderFusionBrowser(); updateURL(); return; }
  const genes = matchingGenes();
  if (!genes.some(g => g.id === state.selected)) state.selected = genes[0]?.id || null;
  $('result-count').textContent = `${genes.length} of ${state.genes.length.toLocaleString()} draft genes`;
  renderAlphabet();
  $('gene-list').replaceChildren();
  for (const gene of genes) {
    const item = el('li');
    const button = el('button', {type: 'button', id: `gene-${gene.id}`, class: 'gene-button', 'aria-current': String(state.selected === gene.id), 'aria-controls': 'entry'});
    button.append(el('strong', {}, gene.symbol), el('span', {}, gene.name), el('span', {class: 'gene-meta'}, `${roleNames[gene.roles[0]] || 'Gene'} · Draft`));
    button.addEventListener('click', () => { state.selected = gene.id; render(); });
    item.append(button); $('gene-list').append(item);
  }
  if (!genes.length) {
    $('gene-list').append(el('li', {class: 'empty'}, 'No genes match these filters.'));
    $('entry').replaceChildren(el('h2', {}, 'No matching genes'), el('p', {class: 'empty'}, 'Try a broader search or reset the filters. Tumor filters include only the disease associations currently assigned in these drafts.'));
    const reset = el('button', {type: 'button', class: 'quiet'}, 'Reset filters');
    reset.addEventListener('click', resetFilters); $('entry').append(reset);
  } else renderEntry(genes.find(g => g.id === state.selected));
  updateURL();
  if (focusID && /^(letter-|gene-)/.test(focusID)) $(focusID)?.focus({preventScroll: true});
}
function citationLabel(source) {
  return source.pmid ? `PMID ${source.pmid}` : source.citation_label || source.title;
}
function renderFusionBrowser() {
  const rows = matchingFusions();
  if (!rows.some(f => f.id === state.selected)) state.selected = rows[0]?.id || null;
  $('result-count').textContent = `${rows.length} of ${state.fusions.length} fusion drafts`;
  renderAlphabet(); $('gene-list').replaceChildren();
  for (const fusion of rows) {
    const item = el('li');
    const button = el('button', {type: 'button', class: 'gene-button', 'aria-current': String(state.selected === fusion.id), 'aria-controls': 'entry'});
    button.append(el('strong', {}, fusion.label), el('span', {}, fusion.tumor_contexts.join(' · ')), el('span', {class: 'gene-meta'}, fusion.audit?.status === 'primary_fulltext_supported' ? 'Primary results checked · Draft' : 'Reference-supported · Draft'));
    button.addEventListener('click', () => { state.selected = fusion.id; render(); });
    item.append(button); $('gene-list').append(item);
  }
  if (!rows.length) {
    $('gene-list').append(el('li', {class: 'empty'}, 'No fusion drafts match these filters.'));
    $('entry').replaceChildren(el('h2', {}, 'No matching fusions'), el('p', {class: 'empty'}, 'Try either partner name, a fusion alias, or reset the filters.'));
    const reset = el('button', {type: 'button', class: 'quiet'}, 'Reset filters'); reset.addEventListener('click', resetFilters); $('entry').append(reset); return;
  }
  const fusion = rows.find(f => f.id === state.selected), entry = $('entry'); entry.replaceChildren();
  entry.setAttribute('aria-label', `${fusion.label} fusion entry`);
  const heading = el('div', {class: 'entry-heading'});
  heading.append(el('h2', {}, fusion.label), el('span', {class: 'badge'}, 'Draft · specialist review pending')); entry.append(heading);
  entry.append(el('p', {class: 'notice entry-disclaimer'}, DISCLAIMER));
  entry.append(el('p', {class: 'context'}, fusion.tumor_contexts.join(' · ')));
  entry.append(el('p', {class: 'metadata'}, `${fusion.event_class.replaceAll('_', ' ')}${fusion.aliases.length ? ' · Also known as ' + fusion.aliases.join(', ') : ''}`));
  const partnerLinks = el('div', {class: 'tags', 'aria-label': 'Gene partners'});
  for (const partner of fusion.partners) {
    const gene = state.genes.find(g => g.id === partner.hgnc_id);
    if (gene) {
      const button = el('button', {type: 'button', class: 'quiet'}, `${partner.symbol} gene overview`);
      button.addEventListener('click', () => { state.mode = 'genes'; state.tab = 'fusions'; state.selected = gene.id; state.letter = ''; $('search').value = ''; $('category').value = ''; $('tumor').value = ''; populateTumors(); render(); });
      partnerLinks.append(button);
    } else partnerLinks.append(el('span', {class: 'tag'}, partner.symbol));
  }
  entry.append(partnerLinks);
  const sections = fusion.sections, ids = fusion.report_comment.source_ids;
  const sectionHeading = el('div', {class: 'section-heading'});
  const copy = el('button', {type: 'button', class: 'quiet'}, 'Copy fusion draft');
  copy.addEventListener('click', () => copyDraft(sections.map(s => `${s.text} ${citationText(s.source_ids, state.fusionSources)}`).join(' '), ids, state.fusionSources, fusion.audit?.audited_on || fusion.editorial.drafted_on));
  sectionHeading.append(el('h3', {}, 'Report paragraph'), copy); entry.append(sectionHeading);
  const paragraph = el('p', {class: 'paragraph'});
  sections.forEach((s, i) => { if (i) paragraph.append(document.createTextNode(' ')); paragraph.append(citeText(s, ids, 'span', state.fusionSources)); }); entry.append(paragraph);
  const audit = el('details', {class: 'association-group evidence-review'});
  audit.append(el('summary', {}, 'Evidence audit and remaining limits'));
  audit.append(el('p', {}, fusion.audit?.summary || 'Source review recorded; specialist approval remains pending.'));
  const decisions = el('ul');
  for (const s of sections) {
    const label = s.kind.replaceAll('_', ' '), status = ({primary_fulltext_supported: 'primary results checked', official_regulatory_supported: 'official regulatory evidence checked', reference_supported: 'gene, identity or authoritative reference checked'})[s.fulltext_audit_status] || 'review pending';
    const item = el('li', {}, `${label}: ${status}.`);
    for (const evidence of s.audit_evidence || []) {
      item.append(document.createTextNode(' '), el('a', {href: evidence.url, target: '_blank', rel: 'noopener noreferrer'}, evidence.location || 'Evidence location'));
    }
    decisions.append(item);
  }
  audit.append(decisions); entry.append(audit, renderSources(ids, state.fusionSources));
  entry.append(el('p', {class: 'review-line'}, `Evidence audit ${fusion.audit?.audited_on || 'pending'} · Specialist review pending. Held claims are excluded from this paragraph.`));
}
function citationText(ids, registry = state.sources) {
  return `(${ids.map(id => citationLabel(registry.find(s => s.id === id))).join(', ')})`;
}
function citeText(section, sourceIDs, tag = 'span', registry = state.sources) {
  const span = el(tag, {}, section.text);
  span.append(document.createTextNode(' ('));
  section.source_ids.forEach((id, index) => {
    const source = registry.find(s => s.id === id);
    if (index) span.append(document.createTextNode(', '));
    span.append(el('a', {href: source.url, target: '_blank', rel: 'noopener noreferrer', 'aria-label': `${citationLabel(source)}: ${source.title}`, title: source.title}, citationLabel(source)));
  });
  span.append(document.createTextNode(')'));
  return span;
}
function renderEntry(gene) {
  const entry = $('entry'); entry.replaceChildren();
  entry.setAttribute('aria-label', `${gene.symbol} gene entry`);
  const heading = el('div', {class: 'entry-heading'});
  const name = el('div');
  name.append(el('h2', {}, gene.symbol), el('p', {class: 'gene-name'}, gene.name));
  heading.append(name, el('span', {class: 'badge'}, 'Draft · unreviewed')); entry.append(heading);
  entry.append(el('p', {class: 'notice entry-disclaimer'}, DISCLAIMER));
  entry.append(el('p', {class: 'metadata'}, `${gene.id} · NCBI Gene ${gene.ncbi_gene_id} · Aliases: ${gene.aliases.join(', ')}`));
  const tags = el('div', {class: 'tags'});
  [...gene.roles.map(r => roleNames[r] || r), ...gene.pathways].forEach(text => tags.append(el('span', {class: 'tag'}, text)));
  entry.append(tags);
  const variants = commentsFor(gene);
  const tabs = el('div', {class: 'tabs', role: 'tablist', 'aria-label': 'Entry sections'});
  const extraCount = state.hotspotCache.has(gene.id) ? state.hotspotCache.get(gene.id).filter(siteInContext).length : state.hotspotMap.get(gene.id)?.site_count || 0;
  const disruptionCount = state.disruptions.filter(d => d.gene_id === gene.id && siteInContext(d)).length;
  const relatedFusions = fusionsForGene(gene).filter(fusionInContext);
  const tabEntries = [['gene', 'Gene overview'], ['variants', `Variant comments (${variants.length + extraCount + disruptionCount})`], ['fusions', `Fusions (${relatedFusions.length})`]];
  tabEntries.forEach(([tab, label], index) => {
    const button = el('button', {type: 'button', id: `tab-${tab}`, role: 'tab', 'aria-selected': String(state.tab === tab), 'aria-controls': `panel-${tab}`, tabindex: state.tab === tab ? '0' : '-1'}, label);
    button.addEventListener('click', () => { state.tab = tab; render(); $(`tab-${tab}`).focus(); });
    button.addEventListener('keydown', event => {
      if (!['ArrowLeft', 'ArrowRight', 'Home', 'End'].includes(event.key)) return;
      event.preventDefault();
      state.tab = event.key === 'Home' ? 'gene' : event.key === 'End' ? 'fusions' : tabEntries[(index + (event.key === 'ArrowLeft' ? 2 : 1)) % tabEntries.length][0];
      render(); $(`tab-${state.tab}`).focus();
    });
    tabs.append(button);
  });
  entry.append(tabs);
  const panel = el('section', {id: `panel-${state.tab}`, role: 'tabpanel', 'aria-labelledby': `tab-${state.tab}`, tabindex: '0'});
  if (state.tab === 'gene') renderGenePanel(panel, gene);
  else if (state.tab === 'fusions') {
    if (!relatedFusions.length) panel.append(el('p', {class: 'empty'}, 'No audited fusion draft for this partner matches the selected tumor scope.'));
    for (const fusion of relatedFusions) {
      const button = el('button', {type: 'button', class: 'quiet fusion-link'}, fusion.label);
      button.addEventListener('click', () => { state.mode = 'fusions'; state.selected = fusion.id; state.letter = ''; $('search').value = ''; $('category').value = ''; $('tumor').value = ''; populateTumors(); render(); });
      panel.append(button, el('p', {class: 'metadata'}, fusion.tumor_contexts.join(' · ')));
    }
  }
  else {
    if (variants.length) renderVariants(panel, variants);
    renderHotspots(panel, gene);
  }
  entry.append(panel);
  entry.append(el('p', {class: 'review-line'}, `Revision ${gene.editorial.revision} · Sources checked ${gene.editorial.sources_checked_on} · Specialist review pending`));
}
function renderGenePanel(panel, gene) {
  const sections = gene.report_summary ? Object.values(gene.report_summary) : ['function', 'germline', 'somatic'].map(key => gene.summary[key]);
  const associations = [...gene.germline_associations, ...gene.somatic_associations, ...gene.mosaic_associations];
  const sourceIDs = [...new Set([...sections.flatMap(s => s.source_ids), ...associations.flatMap(a => a.source_ids)])];
  const heading = el('div', {class: 'section-heading'});
  const copy = el('button', {type: 'button', class: 'quiet'}, 'Copy draft paragraph');
  copy.addEventListener('click', () => copyDraft(sections.map(s => `${s.text} ${citationText(s.source_ids)}`).join(' '), [...new Set(sections.flatMap(s => s.source_ids))]));
  heading.append(el('h3', {}, 'Report paragraph'), copy); panel.append(heading);
  const paragraph = el('p', {class: 'paragraph'});
  sections.forEach((section, index) => { if (index) paragraph.append(document.createTextNode(' ')); paragraph.append(citeText(section, sourceIDs)); });
  panel.append(paragraph);
  if (gene.report_gaps?.length) {
    const gaps = gene.report_gaps.map(g => g.startsWith('germline') ? 'germline' : 'somatic').join(' and ');
    panel.append(el('p', {class: 'metadata'}, `Curation pending: ${gaps} disease associations. Unsupported associations are omitted from the report paragraph.`));
  }
  const associationDetails = el('details', {class: 'association-details'});
  associationDetails.append(el('summary', {}, 'View disease associations'));
  const groups = el('div', {class: 'association-groups'});
  for (const [key, label] of [['germline_associations', 'Inherited disease'], ['somatic_associations', 'Somatic cancer associations'], ['mosaic_associations', 'Postzygotic mosaic disease']]) {
    if (key === 'mosaic_associations' && !gene[key].length) continue;
    const group = el('section', {class: `association-group${key === 'mosaic_associations' ? ' mosaic' : ''}`});
    group.append(el('h3', {}, label));
    if (!gene[key].length) group.append(el('p', {}, key === 'somatic_associations'
      ? 'No tumor-specific somatic association is assigned in this draft.'
      : 'No constitutional disease link is assigned in this draft. See the paragraph for evidence limitations.'));
    else {
      const list = el('ul');
      gene[key].forEach(a => {
        const d = disease(a.disease_id);
        const item = el('li');
        item.append(citeText({text: d.name, source_ids: a.source_ids}, sourceIDs)); list.append(item);
      });
      group.append(list);
    }
    groups.append(group);
  }
  associationDetails.append(groups); panel.append(associationDetails);
  if (gene.review_notes) {
    const notes = el('details', {class: 'association-group evidence-review'});
    notes.append(el('summary', {}, 'View curation notes'), citeText(gene.review_notes, gene.review_notes.source_ids, 'p'));
    panel.append(notes);
    for (const id of gene.review_notes.source_ids) if (!sourceIDs.includes(id)) sourceIDs.push(id);
  }
  panel.append(renderSources(sourceIDs));
  renderFDA(panel, gene);
}
function fdaSummary(refs, subject) {
  return `FDA references include ${subject}.`;
}

function renderFDAEvidence(panel, refs) {
  const details = el('details', {class: 'fda-evidence'});
  details.append(el('summary', {}, 'View supporting FDA evidence'));
  const unique = [...new Map(refs.map(ref => [[ref.therapy, ref.context, ref.criteria].join('|'), ref])).values()];
  for (const ref of unique) {
    const item = el('details', {class: 'fda-reference'});
    item.append(el('summary', {}, `${ref.therapy} · ${ref.context}`));
    item.append(citeText({text: ref.criteria, source_ids: ref.source_ids}, ref.source_ids, 'p'));
    const list = el('ul');
    ref.links.forEach(link => { const li = el('li'); li.append(el('a', {href: link.url, target: '_blank', rel: 'noopener noreferrer'}, link.title || 'FDA label / approval record')); list.append(li); });
    item.append(list); details.append(item);
  }
  panel.append(details);
}
function renderFDA(panel, gene) {
  const refs = fdaFor(gene);
  if (!refs.length) return;
  const section = el('section', {class: 'fda-references'});
  section.append(el('h3', {}, 'FDA therapy context'));
  const ids = [...new Set(refs.flatMap(r => r.source_ids))];
  section.append(citeText({text: fdaSummary(refs, `${gene.symbol}-related biomarkers`), source_ids: ids}, ids, 'p'));
  renderFDAEvidence(section, refs);
  panel.append(section);
}
function draftCard(record, title, context) {
  const card = el('details', {class: 'variant-card'});
  card.append(el('summary', {}, title), el('p', {class: 'notice'}, DISCLAIMER));
  const comment = record.report_comment || record.comment;
  card.append(citeText(comment, comment.source_ids, 'p'));
  const technical = el('details'); technical.append(el('summary', {}, 'Applicability and annotation notes'));
  if (context) technical.append(el('p', {class: 'context'}, context));
  const notes = el('ul');
  (record.applicability_notes || []).forEach(note => notes.append(el('li', {}, note)));
  technical.append(notes); card.append(technical);
  const regulatory = [...(record.fda_reference_ids || []), ...(record.fda_exclusion_reference_ids || [])];
  const regulatoryRefs = regulatory.map(id => state.fda.find(r => r.id === id));
  const alleleNames = [...new Set(regulatory.flatMap(id => record.fda_allele_labels?.[id] || [record.label]))].join(', ');
  const regulatorySummary = regulatoryRefs.length ? fdaSummary(regulatoryRefs, `the allele${alleleNames.includes(',') ? 's' : ''} ${alleleNames}`) : '';
  if (regulatoryRefs.length) {
    const ids = [...new Set(regulatoryRefs.flatMap(ref => ref.source_ids))];
    card.append(citeText({text: regulatorySummary, source_ids: ids}, ids, 'p'));
    renderFDAEvidence(card, regulatoryRefs);
  }
  const copy = el('button', {type: 'button', class: 'quiet'}, 'Copy draft comment');
  copy.addEventListener('click', () => {
    const refs = regulatory.map(id => state.fda.find(r => r.id === id));
    const fdaText = refs.length ? `\n\n${regulatorySummary} ${citationText([...new Set(refs.flatMap(r => r.source_ids))])}` : '';
    copyDraft(`${comment.text} ${citationText(comment.source_ids)}${fdaText}`, [...new Set([...comment.source_ids, ...refs.flatMap(r => r.source_ids)])]);
  });
  card.append(copy, renderSources(comment.source_ids));
  return card;
}
async function renderHotspots(panel, gene) {
  const disruptions = state.disruptions.filter(d => d.gene_id === gene.id && siteInContext(d));
  disruptions.forEach(d => panel.append(draftCard(d, d.label, 'Conditional loss-of-function interpretation · gene-level disease evidence')));
  const index = state.hotspotMap.get(gene.id);
  if (!index && !disruptions.length && !commentsFor(gene).length) panel.append(el('p', {class: 'empty'}, 'No hotspot or disruption comment is assigned to this gene in the selected context.'));
  if (index) {
    const loading = el('p', {role: 'status'}, 'Loading source-linked hotspot comments…'); panel.append(loading);
    try {
      if (!state.hotspotCache.has(gene.id)) state.hotspotCache.set(gene.id, await loadJSON(index.file));
      if (!panel.isConnected) return;
      loading.remove();
      const input = el('input', {type: 'search', id: 'site-search', placeholder: 'Filter residues or observed alleles, e.g. V600E'});
      const label = el('label', {for: 'site-search'}, 'Filter hotspot and allele comments');
      const count = el('p', {role: 'status'}); const list = el('div');
      panel.append(label, input, count, list);
      const items = state.hotspotCache.get(gene.id).filter(siteInContext);
      $('tab-variants').textContent = `Variant comments (${items.length + disruptions.length + commentsFor(gene).length})`;
      const draw = () => {
        const q = normalize(input.value.trim());
        const filtered = items.filter(s => normalize([s.residue, ...s.alleles.map(a => a.label)].join(' ')).includes(q));
        count.textContent = `${filtered.length} of ${items.length} hotspot sites in this tumor context. Open a site for its draft and observed allele comments.`;
        list.replaceChildren();
        for (const site of filtered) {
          const context = `${site.releases.join(', ').toUpperCase()} · ${site.kind.replaceAll('_', ' ')} · Source transcript: ${site.source_transcript || 'not supplied'}`;
          const card = draftCard(site, `${gene.symbol} ${site.residue} · ${site.alleles.length} observed alleles`, context);
          const contexts = el('details'); contexts.append(el('summary', {}, 'View all reported tumor contexts'), el('p', {}, site.disease_ids.map(id => disease(id).name).join('; ') || 'not supplied')); card.append(contexts);
          if (site.alleles.length) {
            const alleles = el('details'); alleles.append(el('summary', {}, `Observed allele drafts (${site.alleles.length})`));
            alleles.append(el('p', {class: 'notice'}, 'These alleles were observed across the source cohorts. A tumor filter identifies sites reported in that context; it does not establish that every listed allele was seen in the selected tumor type.'));
            let built = false;
            alleles.addEventListener('toggle', () => {
              if (!alleles.open || built) return;
              built = true;
              site.alleles.forEach(a => alleles.append(draftCard(a, `${gene.symbol} ${a.label}`, 'Source protein annotation; clinical HGVS mapping and allele-specific significance need review.')));
            });
            card.append(alleles);
          }
          list.append(card);
        }
      };
      input.addEventListener('input', draw); draw();
    } catch (error) { loading.textContent = `Hotspot comments could not load: ${error.message}`; }
  }
  renderFDA(panel, gene);
}
function renderVariants(panel, variants) {
  if (!variants.length) {
    panel.append(el('p', {class: 'empty'}, 'No pilot hotspot comments are available for this gene in the selected tumor context. This does not imply that clinically relevant alterations are absent.'));
    return;
  }
  for (const variant of variants) {
    const comment = state.reportOverrides[variant.id] || variant.comment;
    const sourceIDs = [...new Set([...variant.comment.source_ids, ...variant.selector.source_ids])];
    const card = el('section', {class: 'variant-card'});
    const top = el('div', {class: 'variant-top'});
    top.append(el('h3', {}, variant.label), el('span', {class: 'badge'}, 'Draft')); card.append(top);
    card.append(el('p', {class: 'context'}, `${disease(variant.disease_id).name} · Biological context`));
    card.append(el('p', {class: 'hgvs'}, `${variant.selector.transcript}:${variant.selector.hgvs_c} · ${variant.selector.hgvs_p}`));
    const p = el('p', {class: 'paragraph'}); p.append(citeText(comment, sourceIDs)); card.append(p);
    const notes = el('ul'); variant.applicability_notes.forEach(note => notes.append(el('li', {}, note))); card.append(notes);
    const copy = el('button', {type: 'button', class: 'quiet'}, 'Copy draft comment');
    copy.addEventListener('click', () => copyDraft(`${comment.text} ${citationText(comment.source_ids)}`, comment.source_ids));
    card.append(copy, renderSources(sourceIDs)); panel.append(card);
  }
}
function renderSources(ids, registry = state.sources) {
  const details = el('details', {class: 'source-list'});
  details.append(el('summary', {}, `Sources & provenance (${ids.length})`));
  const list = el('ul');
  ids.forEach(id => {
    const source = registry.find(s => s.id === id);
    const item = el('li');
    item.append(el('a', {href: source.url, target: '_blank', rel: 'noopener noreferrer'}, `${citationLabel(source)} — ${source.title}`));
    item.append(el('small', {}, `${source.publisher || source.kind.replaceAll('_', ' ')} · Accessed ${source.accessed_on}${source.pmid ? ' · PMID ' + source.pmid : ''}`));
    if (source.version) item.append(el('small', {}, source.version));
    list.append(item);
  });
  details.append(list); return details;
}
async function copyDraft(text, ids, registry = state.sources, checkedOn = '2026-11-26') {
  const sources = ids.map(id => { const s = registry.find(s => s.id === id); return `${citationLabel(s)} — ${s.title}: ${s.url}`; }).join('\n');
  const attribution = ids.some(id => id.startsWith('hotspots-')) ? '\n\nContains information from Cancer Hotspots (https://www.cancerhotspots.org/), made available under the Open Database License (ODbL 1.0): https://opendatacommons.org/licenses/odbl/1-0/.' : '';
  const content = `${DISCLAIMER}\nDRAFT — specialist review pending\n${text}\n\nSources checked ${checkedOn}\n${sources}${attribution}`;
  try {
    await navigator.clipboard.writeText(content);
    $('copy-status').textContent = 'Copied with draft status and source links.';
  } catch {
    $('copy-status').textContent = 'Clipboard access is unavailable. Select and copy the visible text and its sources.';
  }
}
function resetFilters() {
  $('search').value = ''; $('category').value = ''; $('tumor').value = ''; state.letter = '';
  populateTumors(); render();
}
async function loadJSON(path) {
  const url = new URL(path, new URL('data/', location.href));
  // Manifest paths must stay in the local data directory.
  const base = new URL('data/', location.href);
  if (url.origin !== base.origin || !url.pathname.startsWith(base.pathname)) throw new Error('Invalid data path');
  const response = await fetch(url);
  if (!response.ok) throw new Error(`Could not load ${path} (${response.status})`);
  return response.json();
}
async function init() {
  try {
    const manifest = await loadJSON('manifest.json');
    const [genes, variants, diseases, sources, hotspots, disruptions, fda, reportOverrides, fusionBundle, fusionSources, fusionDiseases] = await Promise.all([
      manifest.gene_index_file ? loadJSON(manifest.gene_index_file) : Promise.all(manifest.gene_files.map(loadJSON)), Promise.all(manifest.variant_files.map(loadJSON)),
      loadJSON(manifest.disease_file), loadJSON(manifest.source_file),
      manifest.hotspot_index_file ? loadJSON(manifest.hotspot_index_file) : [],
      manifest.disruption_file ? loadJSON(manifest.disruption_file) : [],
      manifest.fda_reference_file ? loadJSON(manifest.fda_reference_file) : [],
      manifest.report_comment_override_file ? loadJSON(manifest.report_comment_override_file) : {},
      manifest.fusion_browser_file ? loadJSON(manifest.fusion_browser_file) : {records: []},
      manifest.fusion_source_file ? loadJSON(manifest.fusion_source_file) : [],
      manifest.fusion_disease_file ? loadJSON(manifest.fusion_disease_file) : []
    ]);
    Object.assign(state, {genes, variants, diseases: [...diseases, ...fusionDiseases.filter(d => !diseases.some(existing => existing.id === d.id))], sources, hotspots, disruptions, fda, reportOverrides, fusions: fusionBundle.records, fusionSources, fusionDiseases});
    state.hotspotMap = new Map(hotspots.map(h => [h.gene_id, h]));
    state.diseaseMap = new Map(state.diseases.map(d => [d.id, d]));
    state.searchMap = new Map(genes.map(g => [g.id, searchable(g)]));
    state.fusionSearchMap = new Map(state.fusions.map(f => [f.id, fusionNormalize([f.label, ...f.aliases, ...f.partners.map(p => p.symbol), ...f.tumor_contexts, ...f.sections.map(s => s.text)].join(' '))]));
    const params = new URLSearchParams(location.search);
    state.mode = params.get('mode') === 'fusions' ? 'fusions' : 'genes';
    $('search').value = params.get('q') || '';
    if (Object.hasOwn(categories, params.get('category'))) $('category').value = params.get('category');
    populateTumors();
    if ([...$('tumor').options].some(o => o.value === params.get('tumor'))) $('tumor').value = params.get('tumor');
    const letter = params.get('letter') || '';
    state.letter = /^[A-Z]$/.test(letter) ? letter : '';
    state.selected = state.mode === 'fusions' ? (state.fusions.some(f => f.id === params.get('fusion')) ? params.get('fusion') : null) : (genes.some(g => g.id === params.get('gene')) ? params.get('gene') : null);
    state.tab = ['variants', 'fusions'].includes(params.get('view')) ? params.get('view') : 'gene';
    $('gene-total').textContent = genes.length.toLocaleString(); $('variant-total').textContent = (variants.length + disruptions.length + hotspots.reduce((sum, h) => sum + h.site_count, 0)).toLocaleString();
    $('search').addEventListener('input', render);
    $('fusion-total').textContent = state.fusions.length.toLocaleString();
    for (const mode of ['genes', 'fusions']) { $(`mode-${mode}`).disabled = false; $(`mode-${mode}`).addEventListener('click', () => setMode(mode)); }
    $('category').addEventListener('change', () => { populateTumors(); render(); });
    $('tumor').addEventListener('change', render);
    $('reset').addEventListener('click', resetFilters);
    for (const id of ['search', 'category', 'tumor', 'reset']) $(id).disabled = false;
    render();
  } catch (error) {
    $('result-count').textContent = 'Examples unavailable';
    $('entry').replaceChildren(el('h2', {}, 'Unable to load the pilot'), el('p', {class: 'empty'}, 'Serve this folder through HTTP using the command in the plan. If already served, check that all data files are present and reload.'), el('p', {class: 'metadata'}, error.message));
  }
}
init();
