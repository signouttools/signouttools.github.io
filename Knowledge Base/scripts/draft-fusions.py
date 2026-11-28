"""Build audited fusion drafts. Only explicit, exact-text audit decisions enter runtime."""
import collections,hashlib,json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];CUR=ROOT/'curation/fusions'
def load(p):return json.loads(p.read_text())
def save(p,d):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
def digest(t):return hashlib.sha256(t.encode()).hexdigest()
def ident(label):return 'fusion-'+re.sub(r'[^a-z0-9]+','-',label.lower()).strip('-')
def main():
    c=load(CUR/'draft-content.json'); sources={s['id']:s for s in load(CUR/'sources.json')};partners=load(CUR/'partners.json')
    audit=load(CUR/'audit-decisions.json');dmap=load(CUR/'disease-mapping.json')
    roster=load(ROOT/'inventory/fusion-roster.json');proposed={r['label']:r for r in roster['fusion_candidates']}
    partner_audit=load(CUR/'audit-partners.json')
    for path in sorted(CUR.glob('expansion-cohort*.json')):
        expansion=load(path)
        for symbol,p in expansion['added_partners'].items():
            if symbol in partners and partners[symbol]!=p:raise ValueError('Expansion partner conflict '+symbol)
            partners[symbol]=p
        for context,disease in expansion['disease_mapping'].items():
            if context in dmap['mapping'] and dmap['mapping'][context]!=disease:raise ValueError('Expansion context conflict '+context)
            dmap['mapping'][context]=disease
        known={d['id'] for d in dmap['new_diseases']}
        dmap['new_diseases'] += [d for d in expansion['new_diseases'] if d['id'] not in known]
    partner_audit=partner_audit|{'expansion_identity_checks':[{'symbol':symbol,'evidence':p['reference_audit']} for path in sorted(CUR.glob('expansion-cohort*.json')) for symbol,p in load(path)['added_partners'].items()]}
    records=[];held=[]
    for item in c['entries']:
        label=item['label']
        if item.get('integration_status')!='eligible':
            held.append({'id':ident(label),'label':label,'reason':'No audited fusion biology/disease section retained; excluded from runtime and report export.'});continue
        sections=[]
        for symbol in item['partners']:
            p=partners[symbol];pa=p['reference_audit'];text=symbol+' '+p['description']
            sections.append({'kind':'partner_function','partner':symbol,'text':text,'source_ids':p['source_ids'],'claim_sha256':digest(text),'fulltext_audit_status':'reference_supported','audit_evidence':[{'source_id':p['source_ids'][0],'url':pa['url'],'location':pa['location'],'scope':pa['scope'],'access_level':pa['basis'],'document_sha256':pa.get('document_sha256')}]})
        for s in item['sections']:
            a=s['audit']
            if a['claim_sha256']!=digest(s['text']):raise ValueError('Stale audit decision '+label)
            sections.append({k:v for k,v in s.items() if k!='audit'}|{'claim_sha256':digest(s['text']),'fulltext_audit_status':a['status'],'audit_evidence':a['evidence']})
        for s in sections:
            if not s['source_ids'] or not set(s['source_ids'])<=sources.keys():raise ValueError('Missing source '+label)
        text=' '.join(s['text'] for s in sections)
        if re.search(r'context matters|clinical significance depends|interpret.{0,20}context|further studies are needed',text,re.I):raise ValueError('Generic filler '+label)
        record={'id':ident(label),'label':label,'event_class':item.get('event_class','chimeric_fusion'),'partners':[{'symbol':s,'hgnc_id':partners[s]['hgnc_id'],'ncbi_gene_id':partners[s]['ncbi_gene_id']} for s in item['partners']], 'aliases':item.get('aliases',proposed.get(label,{}).get('aliases',[])),'tumor_contexts':item['tumor_contexts'],'disease_ids':list(dict.fromkeys(dmap['mapping'][t] for t in item['tumor_contexts'])),'sections':sections,'report_comment':{'text':text,'source_ids':list(dict.fromkeys(i for s in sections for i in s['source_ids']))},'evidence_scope':item.get('evidence_scope','Retained claims carry explicit audit evidence; reference and regulatory evidence is not labeled primary full text.'),'curation_notes':item.get('curation_notes',[]),'editorial':{'status':'draft','revision':2,'drafted_on':c['drafted_on'],'reviewer':None,'pathologist_review':'pending','disclaimer':'Pathologist review needed — LLM-generated summary/review.'},'audit':item['audit'],'text_sha256':digest(text)}
        records.append(record)
    out=ROOT/'data/fusions';out.mkdir(exist_ok=True)
    previous=load(ROOT/'data/fusion-index.json') if (ROOT/'data/fusion-index.json').exists() else {'record_files':[]}
    paths=['fusions/'+r['id']+'.json' for r in records]
    for path in set(previous['record_files'])-set(paths):
        if re.fullmatch(r'fusions/fusion-[a-z0-9-]+\.json',path):(ROOT/'data'/path).unlink(missing_ok=True)
    for r in records:save(out/(r['id']+'.json'),r)
    used={i for r in records for i in r['report_comment']['source_ids']}
    save(ROOT/'data/fusion-sources.json',[s for i,s in sources.items() if i in used])
    used_diseases={i for r in records for i in r['disease_ids']}
    save(ROOT/'data/fusion-diseases.json',[d for d in dmap['new_diseases'] if d['id'] in used_diseases])
    index=[{k:r[k] for k in ['id','label','event_class','partners','aliases','tumor_contexts','disease_ids','evidence_scope','editorial','audit']} for r in records]
    save(ROOT/'data/fusion-index.json',{'schema_version':'0.2.0','built_on':'2026-11-27','status':'audited_drafts_integrated','records':index,'record_files':paths,'source_file':'fusion-sources.json','disease_file':'fusion-diseases.json','held_entries':held})
    save(ROOT/'data/fusion-browser.json',{'schema_version':'0.2.0','records':records})
    save(ROOT/'data/fusion-audit.json',audit|{'partner_audit':partner_audit,'held_entries':held,'integrated_entries':len(records)})
    md=['# Fusion draft library','','Pathologist review needed — LLM-generated summary/review.','',f"Evidence audit 2026-11-27. **{len(records)} integrated draft entries**; **{len(held)} previously drafted entries held**. Primary body/results, official regulatory evidence and authoritative references are distinguished in the audit. Unsupported subclaims have been excluded. Normal partner descriptions use gene/identity references. Specialist review remains pending.",'','[Evidence audit and coverage](FUSION-REVIEW.md) · [Browse fusions](index.html?mode=fusions)','']
    observation_count=sum(r['evidence_scope']=='cohort_observation' for r in records)
    md[5:5]=[f"The library contains **{len(records)-observation_count} interpretive drafts** and **{observation_count} cohort-observation drafts**. Cohort observations describe reported transcript detection only; functional and clinical significance are not adjudicated. See [expansion sources and limits](FUSION-COVERAGE.md).",'']
    for r in records:
        md+=['## '+r['label'],'','**Tumor scope:** '+'; '.join(r['tumor_contexts'])+'.','', '**Evidence:** '+('Primary cohort observation only; functional and clinical significance not adjudicated.' if r['evidence_scope']=='cohort_observation' else 'Primary fusion results checked.' if r['audit']['status']=='primary_fulltext_supported' else 'Authoritative reference support; primary full-text confirmation incomplete.'),'']
        prose=[]
        for s in r['sections']:
            links=', '.join('['+sources[i].get('citation_label',sources[i]['title'])+']('+sources[i]['url']+')' for i in s['source_ids'])
            prose.append(s['text']+' ('+links+').')
        md+=[' '.join(prose),'']
    (ROOT/'FUSION-DRAFTS.md').write_text('\n'.join(md)+'\n')
    integrated={r['label'] for r in records};missing=sorted(set(proposed)-integrated)
    stats={'drafted_on':c['drafted_on'],'audited_on':'2026-11-27','total_entries':len(records),'previously_drafted_entries':len(c['entries']),'held_entries':held,'by_event_class':dict(collections.Counter(r['event_class'] for r in records)),'original_pair_roster':len(proposed),'original_pairs_drafted':len(set(proposed)&integrated),'original_pairs_not_drafted':missing,'additional_pair_entries':sorted({r['label'] for r in records if r['event_class']!='regulatory_rearrangement'}-set(proposed)),'source_count':len(used),'source_registry_count':len(sources),'partner_count':len(partners),'clinical_sections':dict(collections.Counter(s['kind'] for r in records for s in r['sections'])),'deferred':c['deferred'],'audit_decision_counts':dict(collections.Counter(d['decision'] for d in audit['decisions'])),'record_audit_counts':dict(collections.Counter(r['audit']['status'] for r in records)),'status':'audited_drafts_specialist_review_pending'}
    followup_baseline=CUR/'followup-baseline.json'
    if followup_baseline.exists():
        targets={e['label'] for e in load(followup_baseline)['entries']}
        targeted=[r for r in records if r['label'] in targets]
        stats['followup_review']={'target_count':len(targets),'integrated_count':len(targeted),'primary_supported_count':sum(r['audit']['status']=='primary_fulltext_supported' for r in targeted),'reference_supported_labels':[r['label'] for r in targeted if r['audit']['status']=='reference_supported'],'held_labels':[e['label'] for e in held if e['label'] in targets],'passes':audit.get('followup_passes',[])}
    stats['evidence_scope_counts']=dict(collections.Counter('cohort_observation' if r['evidence_scope']=='cohort_observation' else 'interpretive_draft' for r in records))
    stats['expansion_batches']=audit.get('expansion_batches',[])
    stats['original_drafted_entries']=len(load(CUR/'pre-audit-content.json')['entries'])
    stats['previously_drafted_entries']=stats['original_drafted_entries']
    save(ROOT/'data/fusion-drafting-review.json',stats)
    queue=[{'fusion_id':r['id'],'label':r['label'],'section_kind':s['kind'],'text':s['text'],'claim_sha256':s['claim_sha256'],'source_ids':s['source_ids'],'review_status':s['fulltext_audit_status'],'reviewer':'LLM source audit; specialist review pending'} for r in records for s in r['sections']]
    save(ROOT/'data/fusion-evidence-review-queue.json',{'built_on':'2026-11-27','status':'source_audit_applied_specialist_review_pending','claim_count':len(queue),'claims':queue})
    print(json.dumps({k:v for k,v in stats.items() if k not in ['held_entries','additional_pair_entries','deferred']},indent=2))
if __name__=='__main__':main()
