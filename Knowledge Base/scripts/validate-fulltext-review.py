"""Check full-text claim decisions and key clinical/experimental distinctions."""
import json,hashlib
from pathlib import Path
root=Path(__file__).resolve().parents[1]
def load(p):return json.loads(p.read_text())
G={g['symbol']:g for g in load(root/'data/gene-index.json')};S={s['id']:s for s in load(root/'data/sources.json')};decisions=load(root/'curation/fulltext-review-decisions.json')['decisions'];queue={a['pmid']:a for a in load(root/'data/fulltext-review-queue.json')['articles']}
def pmids(sym,part):return {S[i].get('pmid') for i in G[sym]['report_summary'][part]['source_ids']}
assert len({(d['record_id'],d['pmid']) for d in decisions})==len(decisions)
for d in decisions:
 assert d['support_scope'] and d['location'] and d['pmcid'] and len(d['fulltext_sha256'])==64
 assert d['fulltext_sha256']==queue[d['pmid']]['fulltext_sha256']
 if d['decision']=='supports_specific_claim':
  sec=G[d['symbol']]['report_summary'][d['part']]
  assert d['report_text_sha256']==hashlib.sha256(sec['text'].encode()).hexdigest()
  assert d['pmid'] in pmids(d['symbol'],d['part']),(d['symbol'],d['part'],d['pmid'])
assert '25472942' in pmids('BRCA1','germline')
assert '21263000' in pmids('NRAS','germline')
assert '19818708' in pmids('SPOP','function') and '19818708' not in pmids('SPOP','germline')
assert '22729224' in pmids('PIK3CA','mosaic') and '22729224' not in pmids('PIK3CA','germline')
assert '22500628' not in pmids('AKT3','germline')
assert '22729223' not in pmids('MTOR','germline')
assert '20358602' not in pmids('SMC3','germline')
assert '23379592' not in pmids('MAP2K2','germline')
assert '21240275' in pmids('SLX4','germline') and '21240276' not in pmids('SLX4','germline')
assert '23269703' in pmids('BRCA1','germline')
assert '8245783' not in pmids('FLT4','germline') and '8245783' not in pmids('KDR','germline')
assert '19567676' not in pmids('MTAP','germline')
assert '21775990' not in pmids('DMRT1','germline')
assert '19775295' not in pmids('CSF3R','germline')
assert all('21930502' not in {S[i].get('pmid') for sec in g['report_summary'].values() for i in sec['source_ids']} for g in G.values())
print(f'Validated {len(decisions)} full-text decisions, exact claim/document hashes, restored citations, and human-vs-model, mosaic-vs-germline, and function-vs-disease distinctions.')
