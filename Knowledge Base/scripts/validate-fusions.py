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
audit=load('curation/fusions/audit-decisions.json')
approved_claims={(d['label'],d['section_kind'],d.get('replacement_text') or d['original_text']) for d in audit['decisions'] if d['decision']!='remove'}
sources=load('data/fusion-sources.json')
source_map={s['id']:s for s in sources}
check(len(source_map)==len(sources),'Duplicate source IDs')
for s in sources:
    check(s['url'].startswith('https://'),s['id']+' has invalid URL')
    check(bool(s['review_scope']) and bool(s['access_level']),s['id']+' missing provenance')
records=[load('data/'+path) for path in index['record_files']]
browser=load('data/fusion-browser.json')
check(browser['records']==records,'Runtime browser differs from authoritative records')
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
    check(listing['evidence_scope']==r['evidence_scope'],label+' index lost evidence scope')
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
        check(s['fulltext_audit_status'] in ['primary_fulltext_supported','official_regulatory_supported','reference_supported'],label+' unaudited claim in runtime')
        check(s.get('evidence_review_status',s['fulltext_audit_status'])==s['fulltext_audit_status'],label+' conflicting legacy evidence status')
        check(s['claim_sha256']==hashlib.sha256(s['text'].encode()).hexdigest(),label+' stale claim hash')
        check(s.get('audit_evidence') and all(e.get('location') and e.get('url') for e in s['audit_evidence']),label+' missing exact evidence location')
        check(all(e.get('source_id') in s['source_ids'] for e in s['audit_evidence']),label+' audit evidence is not in the section citation list')
        if s['kind']!='partner_function':
            check(any(source_map[i]['kind'] not in ['gene_reference','identity_reference'] for i in s['source_ids']),label+' fusion claim supported only by gene identity/function')
            check((label,s['kind'],s['text']) in approved_claims,label+' changed text bypassed source audit')
            if s['fulltext_audit_status']=='primary_fulltext_supported':check(any(e['access_level']=='primary_fulltext' for e in s['audit_evidence']),label+' primary status without primary-body evidence')
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
held.update(r['label'] for r in stats['held_entries'])
check(not (held & written),'Deferred pair received a blurb')
check(original <= written|held,'Unaccounted original pair')
check(stats['original_pairs_not_drafted']==sorted(original-written),'Coverage gaps do not match roster')
check(stats['by_event_class']==dict(collections.Counter(r['event_class'] for r in records)),'Event class counts differ')
if audit.get('followup_passes'):
    targets={e['label'] for e in load('curation/fusions/followup-baseline.json')['entries']}
    assignments=[label for p in audit['followup_passes'] for label in p['labels']]
    check(targets<=set(assignments),'Follow-up omitted a requested target')
    check(len(assignments)==len(set(assignments)),'Follow-up has overlapping entry assignments')
    followup=stats['followup_review']
    check(followup['target_count']==len(targets),'Follow-up target count mismatch')
    check(followup['primary_supported_count']==sum(r['label'] in targets and r['audit']['status']=='primary_fulltext_supported' for r in records),'Follow-up primary evidence count mismatch')
    check(followup['integrated_count']==len(targets & written),'Follow-up integration count mismatch')
manifest=load('data/manifest.json')
check(manifest.get('fusion_index_file')=='fusion-index.json' and manifest.get('fusion_browser_file')=='fusion-browser.json','Fusion corpus not integrated in runtime manifest')
check(manifest.get('fusion_source_file')=='fusion-sources.json' and manifest.get('fusion_disease_file')=='fusion-diseases.json','Fusion runtime references missing')
diseases=load('data/diseases.json')+load('data/fusion-diseases.json');disease_map={d['id']:d for d in diseases}
check(len(disease_map)==len(diseases),'Duplicate runtime disease IDs')
for r in records:
    check(r['disease_ids'] and set(r['disease_ids'])<=disease_map.keys(),r['label']+' unknown disease link')
    check(all(disease_map[i]['category'] not in ['constitutional','mosaic'] for i in r['disease_ids']),r['label']+' inherited disease used as fusion tumor scope')
for d in diseases:
    if d['parent_id']:check(d['parent_id'] in disease_map,d['name']+' missing parent')
expansion_path=ROOT/'curation/fusions/expansion-observations.json'
if expansion_path.exists():
    expansion=json.loads(expansion_path.read_text())
    pairs=expansion['pediatric']['pairs']
    check(len(pairs)==expansion['pediatric']['published_pairs']==272,'Pediatric extraction pair total differs from study')
    check(len({p['label'] for p in pairs})==len(pairs),'Normalized pediatric pair collision')
    additions={p['label']:p for p in pairs if p['disposition']=='new_cohort_observation_draft'}
    observed={r['label']:r for r in records if r['evidence_scope']=='cohort_observation'}
    check(observed.keys()==additions.keys(),'Cohort additions differ from source extraction')
    check(len(observed)==expansion['new_runtime_entries'],'Incorrect expansion count')
    for label,r in observed.items():
        p=additions[label]
        check(r['event_class']=='fusion_transcript',label+' observation incorrectly assumes a protein fusion')
        check(r['tumor_contexts']==p['tumor_contexts'],label+' occurrence tumor scope changed')
        sections=[s for s in r['sections'] if s['kind']!='partner_function']
        check(len(sections)==1 and sections[0]['kind']=='tumor_relevance',label+' observation acquired clinical/mechanistic claims')
        s=sections[0]
        check(s['source_ids']==[p['source_id']],label+' observation was re-sourced')
        check(s['audit_evidence'][0]['source_rows']==[row['row'] for row in p['source_rows']],label+' source row evidence mismatch')
        check(s['audit_evidence'][0]['document_sha256']==expansion['receipts']['pediatric_workbook_sha256'],label+' workbook provenance mismatch')
    wgs=expansion['wgs']
    check(len(wgs['pairs'])==wgs['distinct_directed_pairs']==178,'WGS pair count mismatch')
    check(all(p['report_eligible'] is False for p in wgs['pairs']),'WGS observation incorrectly cleared for report prose')
    check(not any(p.get('source_id')=='van-belzen-2023-wgs' for r in records for s in r['sections'] for p in s.get('audit_evidence',[])),'WGS candidates bypassed review queue')
    check(stats['evidence_scope_counts']['cohort_observation']==len(observed),'Scope statistics mismatch')
print(f'Validated {len(records)} draft entries, {len(sources)} sources and {len(claims)} exact-hash claim-review placements.')
print('Checked partner IDs, retained-source evidence, exact audit hashes, runtime/index/export consistency, held-candidate exclusion and disease filters.')
