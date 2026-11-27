"""Require exact text-hash and explicit claim-scope support for every report PMID."""
import json,hashlib
from pathlib import Path
root=Path(__file__).resolve().parents[1]
def load(p):return json.loads(p.read_text())
S={s['id']:s for s in load(root/'data/sources.json')};audit=load(root/'data/citation-audit.json');records={};genes=load(root/'data/gene-index.json')
for g in genes:
 for part,s in g['report_summary'].items():records['gene:'+g['id']+':'+part]=s
for file,prefix in [('hotspots.json','site:'),('hotspot-alleles.json','allele:'),('disruption-comments.json','disruption:')]:
 for r in load(root/'data'/file):records[prefix+r['id']]=r['report_comment']
for id,s in load(root/'data/report-comment-overrides.json').items():records['pilot:'+id]=s
assert audit['genes_checked']==len(genes)
for id,s in records.items():
 binding=audit['bindings'][id];assert binding['text_sha256']==hashlib.sha256(s['text'].encode()).hexdigest(),id
 for sid in s['source_ids']:
  if S[sid].get('pmid'):assert any(v['source_id']==sid and v['pmid']==S[sid]['pmid'] and v['scope'] for v in binding['verified_pmids']),(id,sid)
# Previously over-broad examples must stay excluded from copyable report text.
for g in genes:
 for part,s in g['report_summary'].items():
  pmids={S[i].get('pmid') for i in s['source_ids']}
  if g['symbol'] in ['BRCA1','BRCA2'] and part=='somatic':assert '23000897' not in pmids
  if g['symbol']=='BRCA2' and part=='somatic':assert '25719666' not in pmids
assert load(root/'data/primary-citation-review.json')['status']=='superseded_by_claim_specific_citation_audit'
print(f'Validated claim-specific PMID support bindings for {len(records)} report sections across {len(genes)} genes; changed prose or unreviewed PMID insertion fails validation.')
