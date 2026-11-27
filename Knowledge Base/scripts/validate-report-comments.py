"""Check report-language scope, biological citations, and retained evidence gaps."""
import json,re
from pathlib import Path
root=Path(__file__).resolve().parents[1]
def load(p):return json.loads(p.read_text())
genes=load(root/'data/gene-index.json');sources={s['id']:s for s in load(root/'data/sources.json')};report=load(root/'data/report-style-review.json');by={g['symbol']:g for g in genes}
forbidden=re.compile(r'\b(?:draft|GenCC|reviewed|retrieved|panel|cohort|snapshot|this example|our|we)\b',re.I)
def check(section):
 assert section['text'].strip() and section['source_ids']
 assert not forbidden.search(section['text']),section['text']
 assert not re.search(r'clinical implications depend|biological effect varies|effect depends on the affected transcript|functional and clinical significance (?:depend|require)|tumor-detected .+ alone does not establish a germline diagnosis|recurrence alone does not establish',section['text'],re.I),section['text']
 assert all(i in sources and sources[i]['kind']!='panel_reference' for i in section['source_ids'])
for g in genes:
 assert g['report_summary']['function'] and g['editorial']['status']=='draft'
 for part in g['report_summary'].values():check(part)
 if 'germline_association_requires_curation' in g['report_gaps']:assert 'germline' not in g['report_summary']
 if 'somatic_association_requires_curation' in g['report_gaps']:assert 'somatic' not in g['report_summary']
assert report['germline_gaps']==sum('germline_association_requires_curation' in g['report_gaps'] for g in genes)
assert report['somatic_gaps']==sum('somatic_association_requires_curation' in g['report_gaps'] for g in genes)
assert 'breast' not in by['BRIP1']['report_summary']['germline']['text'].lower()
assert 'Fanconi-like' in by['FANCM']['report_summary']['germline']['text']
assert 'limited' in by['NPM1']['report_summary']['germline']['text']
for file in ['hotspots.json','hotspot-alleles.json','disruption-comments.json']:
 for r in load(root/'data'/file):check(r['report_comment'])
for section in load(root/'data/report-comment-overrides.json').values():check(section)
# Rewrites preserve retained evidence; unresolved relationships are not invented.
assert all(g['summary'] and 'somatic_associations' in g for g in genes)
print(f'Validated report-language projections for {len(genes)} genes, all hotspot/allele/disruption comments, source references, and separately flagged evidence gaps. No panel citations or dataset/editorial prose in report comments.')
