"""Merge explicit primary/reference audit decisions into the fusion curation source.
Never treats retrieval, term matching, or an abstract as primary full-text support.
"""
import collections,hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];CUR=ROOT/'curation/fusions'
def load(p):return json.loads(p.read_text())
def save(p,d):p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
def digest(t):return hashlib.sha256(t.encode()).hexdigest()
base=load(CUR/'pre-audit-content.json');original={e['label']:e for e in base['entries']}
source_map={s['id']:s for s in load(CUR/'sources.json')};revised={};decisions=[];held=[]
for name in ['audit-heme.json','audit-sarcoma.json','audit-solid-cns.json']:
    fragment=load(CUR/name)
    for s in fragment.get('added_sources',[]):source_map[s['id']]=s
    for e in fragment['entries']:
        if e['label'] in revised:raise ValueError('Duplicate audit assignment '+e['label'])
        revised[e['label']]=e
    decisions+=fragment['decisions'];held+=fragment.get('held_entries',[])
if revised.keys()!=original.keys():raise ValueError('Audit assignment coverage differs from original corpus')
# Later passes replace complete entry assignments while keeping the first pass
# and frozen original prose available for comparison and reproducibility.
followup_passes=[]
for path in sorted(CUR.glob('audit-followup-*.json')):
    fragment=load(path)
    labels={e['label'] for e in fragment['entries']}
    if not labels or not labels<=original.keys():raise ValueError('Invalid follow-up assignment '+path.name)
    if any(labels & set(p['labels']) for p in followup_passes):raise ValueError('Overlapping follow-up assignments '+path.name)
    expected={(e['label'],s['kind'],digest(s['text'])) for e in base['entries'] if e['label'] in labels for s in e['sections']}
    observed=[(d['label'],d['section_kind'],d['original_text_sha256']) for d in fragment['decisions']]
    if len(observed)!=len(set(observed)) or set(observed)!=expected:raise ValueError('Incomplete follow-up decisions '+path.name)
    for s in fragment.get('added_sources',[]):source_map[s['id']]=s
    revised.update({e['label']:e for e in fragment['entries']})
    decisions=[d for d in decisions if d['label'] not in labels]+fragment['decisions']
    held=[e for e in held if e['label'] not in labels]+fragment.get('held_entries',[])
    followup_passes.append({'file':path.name,'labels':sorted(labels),'decision_count':len(observed)})
original_claims={(e['label'],s['kind'],digest(s['text'])):s for e in base['entries'] for s in e['sections']}
by_original={}
for d in decisions:
    k=(d['label'],d['section_kind'],d['original_text_sha256'])
    if k not in original_claims:raise ValueError('Decision does not match original claim: '+str(k))
    if k in by_original:raise ValueError('Duplicate claim decision '+str(k))
    by_original[k]=d
    d['original_text']=original_claims[k]['text']
if by_original.keys()!=original_claims.keys():raise ValueError('Missing decisions: '+str(original_claims.keys()-by_original.keys()))
expansion_batches=[]
for path in sorted(CUR.glob('expansion-cohort*.json')):
    fragment=load(path)
    labels=[e['label'] for e in fragment['entries']]
    if len(labels)!=len(set(labels)) or set(labels)&revised.keys():raise ValueError('Expansion overlaps existing audit '+path.name)
    claims={(e['label'],s['kind'],digest(s['text'])) for e in fragment['entries'] for s in e['sections']}
    reviewed=[(d['label'],d['section_kind'],d['original_text_sha256']) for d in fragment['decisions']]
    if len(reviewed)!=len(set(reviewed)) or set(reviewed)!=claims:raise ValueError('Expansion audit coverage mismatch '+path.name)
    for d in fragment['decisions']:
        if digest(d['original_text'])!=d['original_text_sha256']:raise ValueError('Stale expansion decision '+d['label'])
    for s in fragment['added_sources']:source_map[s['id']]=s
    revised.update({e['label']:e for e in fragment['entries']})
    decisions+=fragment['decisions']
    expansion_batches.append({'file':path.name,'entry_count':len(labels),'claim_count':len(reviewed),'scope':'cohort_observation'})
accepted_access={'primary_fulltext','official_regulatory','guideline','gene_reference','identity_reference','authoritative_reference'}
for label,e in revised.items():
    retained=[]
    for s in e['sections']:
        candidates=[d for d in decisions if d['label']==label and d['section_kind']==s['kind'] and d['decision']!='remove' and (d.get('replacement_text') or d['original_text'])==s['text']]
        if len(candidates)!=1:raise ValueError('Retained text lacks unique exact decision '+label+' '+s['kind'])
        d=candidates[0];evidence=[a for a in d.get('evidence',[]) if a.get('access_level') in accepted_access and a.get('location') and a.get('url')]
        if not evidence:raise ValueError('Retained claim lacks inspected evidence '+label)
        if any(i not in source_map for i in s['source_ids']):raise ValueError('Unknown retained source '+label)
        levels={a['access_level'] for a in evidence}
        status='primary_fulltext_supported' if 'primary_fulltext' in levels else 'official_regulatory_supported' if 'official_regulatory' in levels else 'reference_supported'
        if 'evidence_review_status' in s:s['evidence_review_status']=status
        s['audit']={'status':status,'audited_on':'2026-11-27','claim_sha256':digest(s['text']),'decision':d['decision'],'evidence':evidence,'rationale':d['rationale']}
        retained.append(s)
    e['sections']=retained
    if not any(s['kind'] in ['fusion_mechanism','tumor_relevance'] for s in retained):
        e['integration_status']='held';continue
    e['integration_status']='eligible'
    biological=[s for s in retained if s['kind'] in ['fusion_mechanism','tumor_relevance','prognosis']]
    primary=any(s['audit']['status']=='primary_fulltext_supported' for s in biological)
    e['audit']={'status':'primary_fulltext_supported' if primary else 'reference_supported','audited_on':'2026-11-27','summary':('Primary body/results support the retained fusion claims identified below. ' if primary else 'The retained fusion association is supported by the named authoritative references; primary full-text confirmation remains incomplete. ')+'Gene-partner descriptions were checked separately against gene or identity references. Unsupported subclaims were removed. Specialist approval remains pending.'}
    if e.get('evidence_scope')=='cohort_observation':
        e['audit']['summary']='The cited primary supplementary table supports the reported directed fusion and specimen labels. This is a cohort observation; independent functional validation, diagnostic specificity, prognosis and treatment response have not been adjudicated. Partner descriptions use gene/identity references. Specialist approval remains pending.'
base['entries']=[revised[e['label']] for e in base['entries']]
base['entries'] += [revised[label] for label in revised if label not in original]
base['audit_status']='claim_review_applied_with_explicit_primary_access_gaps'
save(CUR/'draft-content.json',base);save(CUR/'sources.json',list(source_map.values()))
result={'audited_on':'2026-11-27','status':'claim_review_applied_with_access_limits','method':'Explicit inspection of primary body/results or designated regulatory/guideline evidence; no term matching or abstract-only verification.','original_claim_count':len(original_claims),'decisions':decisions,'held_entries':held,'limitations':['Normal partner descriptions use gene/identity references, not a primary full-text audit.','Retained guideline/reference-only disease associations are distinguished from primary-supported claims.','Regulatory eligibility statements are checked against official sources, not labeled primary biological evidence.','Some primary full texts were inaccessible; these are not certified and unsupported language is excluded.']}
result['followup_passes']=followup_passes
result['expansion_batches']=expansion_batches
save(CUR/'audit-decisions.json',result)
print('Applied',len(decisions),'fusion-section decisions;',collections.Counter(d['decision'] for d in decisions))
