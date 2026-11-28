"""Check source-review coverage, scoped evidence, and biological role regressions."""
import hashlib,json,re
from pathlib import Path
root=Path(__file__).resolve().parents[1]
def load(p):return json.loads(p.read_text())
def sha(s):return hashlib.sha256(s.encode()).hexdigest()
review=load(root/'curation/gene-paragraph-source-review.json');report=load(root/'data/gene-paragraph-review.json');curated=load(root/'curation/gene-paragraph-expansions.json')
genes=load(root/'data/gene-index.json');by={g['id']:g for g in genes};symbols={g['symbol']:g for g in genes};sources={s['id']:s for s in load(root/'data/sources.json')}
assert review['review_complete'] and review['target_gene_count']==1251
assert len(review['records'])==len({r['gene_id'] for r in review['records']})==1251
for r in review['records']:
 assert r['review_complete'] and r['reason'] and r['source_urls']
 assert 'pending' not in r['decision'] and 'requires' not in r['decision']
 assert sha(r['ncbi_summary'])==r['ncbi_summary_sha256']
 u=r['uniprot_row']
 if u:
  assert r['gene_id'] in {i.strip() for i in u['HGNC'].split(';')}
  assert sha(json.dumps(u,sort_keys=True))==r['uniprot_row_sha256']
 g=by[r['gene_id']]
 for k,h in r['unchanged_disease_section_hashes'].items():
  assert sha(json.dumps(g['report_summary'][k],sort_keys=True))==h,(r['symbol'],k,'Disease section changed during function-only expansion')
 if r['decision'].startswith('expanded_'):
  sec=g['report_summary']['function']
  assert sec['text']==curated['function_by_symbol'][r['symbol']]==r['new_function']
  assert all(i in sources for i in sec['source_ids'])
  if u:assert 'uniprot-'+u['Entry'] in sec['source_ids']
  assert not re.search(r'ECO:|PubMed:|FUNCTION:|\bIt is (?:a|an) (?:also|they|the |during|each|it |typically)',sec['text'])
  if r['source_qualifier_by_similarity'] and r['decision']=='expanded_from_reviewed_protein_function':assert 'Based in part on similarity' in sec['text']
  assert not re.search(r'\.\s+\.|\baTP\b|\bdNA\b|\brNA\b|\bgTP',sec['text'])
# These distinctions cannot be preserved by a word-count-only check.
func=lambda sym:symbols[sym]['report_summary']['function']['text']
assert 'receptor-interacting' in func('AIP') and 'rather than the aryl-hydrocarbon receptor itself' in func('AIP')
assert 'substrate-recognition' in func('GID4') and 'CTLH' in func('GID4')
assert 'component' in func('NCSTN') and 'complex' in func('NCSTN')
assert 'ligands' in func('MIB1')
assert 'translation' in func('MSI2') and 'RNA-binding' in func('MSI2')
assert 'replacement of RAS-bound GDP with GTP' in func('SOS1')
assert 'cortisone to cortisol' in func('HSD11B1')
assert 'TRA is the T-cell receptor alpha locus' in func('TRA')
assert 'TRB is the T-cell receptor beta locus' in func('TRB')
assert 'M1-specific' not in func('TRA')+func('TRB')
assert 'MATH' in func('SPOP') and 'CUL3' in func('SPOP')
lengths=[len(' '.join(s['text'] for s in g['report_summary'].values()).split()) for g in genes]
assert report['within_target']==sum(80<=n<=300 for n in lengths)
assert report['below_target']==sum(n<80 for n in lengths)
assert report['above_target']==sum(n>300 for n in lengths)
assert report['expanded_in_completed_source_pass']==sum(r['decision'].startswith('expanded_') for r in review['records'])
print(f'Validated all {len(review["records"])} completed source-review decisions, evidence identities, preserved disease sections, qualifiers, word-count reports, and biological role regressions.')
