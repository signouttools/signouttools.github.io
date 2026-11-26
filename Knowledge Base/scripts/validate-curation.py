"""Check evidence boundaries, source decisions, disclaimers, and the stage-two hold."""
import json,re
from pathlib import Path
root=Path(__file__).resolve().parents[1]
def load(p):return json.loads(p.read_text())
r=load(root/'data/evidence-curation.json');genes=load(root/'data/gene-index.json');by={g['symbol']:g for g in genes};sources={s['id']:s for s in load(root/'data/sources.json')};diseases={d['id']:d for d in load(root/'data/diseases.json')};baseline=load(root/'curation/baseline.json')
supplement=load(root/'data/hotspot-import.json') if (root/'data/hotspot-import.json').exists() else {'added_genes':[]}
assert len(genes)==1133+len(supplement['added_genes'])
assert not r['stage_two_ready']
assert r['disclaimer']=='Pathologist review needed — LLM-generated summary/review.'
assert all(g['editorial']['disclaimer']==r['disclaimer'] for g in genes)
assert all(g['editorial']['status']=='draft' and g['editorial']['reviewer'] is None for g in genes)
assert all(s.get('citation_label') for s in sources.values())
assert len(r['germline_decisions'])==79
assert set(r['previous_germline_flagged_genes'])=={d['symbol'] for d in r['germline_decisions']}
assert len(r['previous_germline_flagged_genes'])==59
for d in r['germline_decisions']:
 assert d['selected_source_id'] in sources
 assert d['selected_date'] and d['selected_sgc'] and d['rationale']
 assert d['selected_classification'] in ['Disputed Evidence','Refuted Evidence','Limited']
for id,rows in load(root/'data/somatic-cohort-evidence.json').items():
 assert id in {g['id'] for g in genes}
 for row in rows:
  assert row['qvalue']<.1 and row['mutated_samples']>=3
  assert row['mutated_samples']<=row['total_samples']
  assert row['cohort'] and row['cancer_name']
for symbol in ['BRIP1','EPCAM','MRE11','NBN','RAD50','RINT1','SLX4','XRCC2']:
 assert not any('breast' in diseases[a['disease_id']]['name'].lower() for a in by[symbol]['germline_associations']),symbol
assert not any('ovarian' in diseases[a['disease_id']]['name'].lower() for a in by['BARD1']['germline_associations'])
assert any('ovarian' in diseases[a['disease_id']]['name'].lower() for a in by['BRIP1']['germline_associations'])
assert any('fanconi-like' in diseases[a['disease_id']]['name'].lower() for a in by['FANCM']['germline_associations'])
assert not any(diseases[a['disease_id']]['name']=='Fanconi anemia' for a in by['FANCM']['germline_associations'])
assert by['NPM1']['germline_associations']==[] and 'limited' in by['NPM1']['summary']['germline']['text']
for sym in ['DDX41','H3-3B','MGMT','CCND2','USP6','CDK8','MCL1','BCL2L1','BRIP1','RAD51C','MRE11','EZHIP','IGF2','TERC']:
 assert by[sym]['somatic_associations'],sym
for name,text in baseline['variant_files'].items():assert (root/'data/variants'/name).read_text()==text
remaining={g['symbol'] for g in genes if not g['somatic_associations']}
assert remaining=={g['symbol'] for g in r['remaining_somatic_gaps']}
old_missing={g['symbol'] for g in baseline['baseline_gene_flags'] if 'somatic_association_unassigned' in g['flags']}
assert old_missing-remaining==set(r['newly_assigned_somatic_genes'])
assert '`[${' not in (root/'app.js').read_text() and 'Source ${number}' not in (root/'app.js').read_text()
print(f'Validated {len(r["newly_assigned_somatic_genes"])} newly assigned genes, 79 relationship decisions across 59 genes, named citation metadata, disclaimers, and unchanged stage-two examples. {len(remaining)} somatic gaps remain open.')
