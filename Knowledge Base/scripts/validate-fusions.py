"""Validate the separate fusion draft corpus and prevent evidence/scope regressions."""
import collections
import hashlib
import json
import re
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
def load(path):return json.loads((ROOT/path).read_text())
def check(condition,message):
    if not condition:raise ValueError(message)

index=load('data/fusion-index.json')
sources=load('data/fusion-sources.json')
source_map={s['id']:s for s in sources}
check(len(source_map)==len(sources),'Duplicate source IDs')
for s in sources:
    check(s['url'].startswith('https://'),s['id']+' has invalid URL')
    check(bool(s['review_scope']) and bool(s['access_level']),s['id']+' missing provenance')
records=[load('data/'+path) for path in index['record_files']]
check(len({r['id'] for r in records})==len(records),'Duplicate record IDs')
check(len({r['label'] for r in records})==len(records),'Duplicate labels')
check(len(records)==len(index['records']),'Index count mismatch')
check({p.name for p in (ROOT/'data/fusions').glob('*.json')}=={Path(p).name for p in index['record_files']},'Unindexed fusion file')
text_export=(ROOT/'FUSION-DRAFTS.md').read_text()
claims=[]
for r,listing in zip(records,index['records']):
    label=r['label']
    check(r['editorial']['status']=='draft' and r['editorial']['reviewer'] is None,label+' incorrectly promoted')
    check(listing['id']==r['id'] and listing['partners']==r['partners'],label+' index mismatch')
    check(len(r['partners'])>=2,label+' missing partners')
    check(bool(r['tumor_contexts']),label+' missing tumor scope')
    function_sections=[s for s in r['sections'] if s['kind']=='partner_function']
    check([s['partner'] for s in function_sections]==[p['symbol'] for p in r['partners']],label+' partner sentence mismatch')
    for p in r['partners']:
        if p['symbol']=='TCR loci':
            check(r['event_class']=='regulatory_rearrangement' and p['hgnc_id'] is None,label+' invalid categorical locus')
        else:check(re.fullmatch(r'HGNC:\d+',p['hgnc_id'] or ''),label+' invalid HGNC ID')
    for s in r['sections']:
        check(s['source_ids'] and set(s['source_ids'])<=source_map.keys(),label+' dangling citation')
        check(s['fulltext_audit_status']=='pending',label+' unsupported audit status')
        check(s['claim_sha256']==hashlib.sha256(s['text'].encode()).hexdigest(),label+' stale claim hash')
        if s['kind']!='partner_function':
            check(any(source_map[i]['kind'] not in ['gene_reference','identity_reference'] for i in s['source_ids']),label+' fusion claim supported only by gene identity/function')
        claims.append((r['id'],s['kind'],s['claim_sha256']))
    text=' '.join(s['text'] for s in r['sections'])
    check(r['report_comment']['text']==text,label+' report projection mismatch')
    check(r['text_sha256']==hashlib.sha256(text.encode()).hexdigest(),label+' stale report hash')
    check(r['report_comment']['source_ids']==list(dict.fromkeys(i for s in r['sections'] for i in s['source_ids'])),label+' citation union mismatch')
    check('\n## '+label+'\n' in text_export,label+' missing from export')
    check(not re.search(r'context matters|clinical significance depends|interpret.{0,20}context|further studies are needed',text,re.I),label+' generic filler')
queue=load('data/fusion-evidence-review-queue.json')
check(queue['claim_count']==len(claims),'Review queue count mismatch')
check(collections.Counter((c['fusion_id'],c['section_kind'],c['claim_sha256']) for c in queue['claims'])==collections.Counter(claims),'Review queue does not match exact claims')
stats=load('data/fusion-drafting-review.json')
check(stats['total_entries']==len(records),'Coverage count mismatch')
original={r['label'] for r in load('inventory/fusion-roster.json')['fusion_candidates']}
written={r['label'] for r in records}
held={r['label'] for r in stats['deferred']}
check(not (held & written),'Deferred pair received a blurb')
check(original <= written|held,'Unaccounted original pair')
check(stats['original_pairs_not_drafted']==sorted(original-written),'Coverage gaps do not match roster')
check(stats['by_event_class']==dict(collections.Counter(r['event_class'] for r in records)),'Event class counts differ')
manifest=load('data/manifest.json')
check('fusion-index.json' not in json.dumps(manifest),'Draft corpus unexpectedly connected to runtime manifest')
print(f'Validated {len(records)} draft entries, {len(sources)} sources and {len(claims)} exact-hash claim-review placements.')
print('Checked partner IDs/sentences, sources, index/export consistency, roster accounting, pending review status and separate runtime boundary.')
