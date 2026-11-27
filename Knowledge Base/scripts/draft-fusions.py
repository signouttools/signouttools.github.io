"""Build fusion drafts from explicit, claim-scoped curation; no inference from panel membership.
Usage: python3 'Knowledge Base/scripts/draft-fusions.py'
"""
import json, hashlib, re, collections
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
CUR=ROOT/'curation/fusions'
def load(p): return json.loads(p.read_text())
def save(p,obj): p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n')
def main():
    c=load(CUR/'draft-content.json'); sources={s['id']:s for s in load(CUR/'sources.json')}; partners=load(CUR/'partners.json')
    roster=load(ROOT/'inventory/fusion-roster.json'); proposed={r['label']:r for r in roster['fusion_candidates']}
    records=[]; ids=set()
    for item in c['entries']:
        label=item['label']; ident='fusion-'+re.sub(r'[^a-z0-9]+','-',label.lower()).strip('-')
        if ident in ids: raise ValueError('Duplicate '+ident)
        ids.add(ident)
        sections=[]
        for symbol in item['partners']:
            p=partners[symbol]
            sections.append({'kind':'partner_function','partner':symbol,'text':symbol+' '+p['description'],'source_ids':p['source_ids']})
        sections+=item['sections']
        for section in sections:
            if not section['text'].strip():raise ValueError('Empty '+label)
            for sid in section['source_ids']:
                if sid not in sources: raise ValueError(label+' unknown source '+sid)
            if not section['source_ids']: raise ValueError(label+' missing evidence')
            section['claim_sha256']=hashlib.sha256(section['text'].encode()).hexdigest()
            section['fulltext_audit_status']='pending'
        text=' '.join(s['text'] for s in sections)
        if re.search(r'context matters|clinical significance depends|interpret.{0,20}context|further studies are needed',text,re.I):raise ValueError('Generic filler '+label)
        record={'id':ident,'label':label,'event_class':item.get('event_class','chimeric_fusion'),'partners':[{'symbol':s,'hgnc_id':partners[s]['hgnc_id'],'ncbi_gene_id':partners[s]['ncbi_gene_id']} for s in item['partners']], 'aliases':item.get('aliases',proposed.get(label,{}).get('aliases',[])), 'tumor_contexts':item['tumor_contexts'],'sections':sections,'report_comment':{'text':text,'source_ids':list(dict.fromkeys(sid for s in sections for sid in s['source_ids']))},'evidence_scope':item.get('evidence_scope','Draft synthesis from cited sources; primary abstract/search-excerpt and selected full-text review. Not a completed claim-level full-text audit.'),'curation_notes':item.get('curation_notes',[]),'editorial':{'status':'draft','revision':1,'drafted_on':c['drafted_on'],'reviewer':None,'pathologist_review':'pending','disclaimer':'Pathologist review needed — LLM-generated summary/review.'},'text_sha256':hashlib.sha256(text.encode()).hexdigest()}
        records.append(record)
    out=ROOT/'data/fusions';out.mkdir(exist_ok=True)
    for r in records:save(out/(r['id']+'.json'),r)
    save(ROOT/'data/fusion-sources.json',list(sources.values()))
    index=[{k:r[k] for k in ['id','label','event_class','partners','aliases','tumor_contexts','editorial']} for r in records]
    save(ROOT/'data/fusion-index.json',{'schema_version':'0.1.0','built_on':c['drafted_on'],'status':'draft_not_in_live_manifest','records':index,'record_files':['fusions/'+r['id']+'.json' for r in records],'source_file':'fusion-sources.json'})
    md=['# Fusion draft library','', 'Pathologist review needed — LLM-generated summary/review.','',f"Drafted {c['drafted_on']}. **{len(records)} entries**. Biological and clinical statements have separate source links. Clinical statements specify tumor, age or treatment setting when relevant. US regulatory evidence is dated; this is not a treatment guideline. Full-text citation adjudication and specialist review remain pending. These drafts are not connected to the live browser or its approved-content pipeline.",'','[Curation and coverage notes](FUSION-REVIEW.md)','']
    for r in records:
        md += ['## '+r['label'],'','**Tumor scope:** '+ '; '.join(r['tumor_contexts'])+'.','']
        if r['event_class']!='chimeric_fusion':md+=['**Event type:** '+r['event_class'].replace('_',' ')+'.','']
        prose=[]
        for s in r['sections']:
            links=', '.join('['+sources[sid].get('citation_label',sources[sid]['title'])+']('+sources[sid]['url']+')' for sid in s['source_ids'])
            prose.append(s['text']+' ('+links+').')
        md+=[' '.join(prose),'']
    (ROOT/'FUSION-DRAFTS.md').write_text('\n'.join(md)+'\n')
    missing=sorted(set(proposed)-{r['label'] for r in records})
    stats={'drafted_on':c['drafted_on'],'total_entries':len(records),'by_event_class':dict(collections.Counter(r['event_class'] for r in records)),'original_pair_roster':len(proposed),'original_pairs_drafted':len(set(proposed)&{r['label'] for r in records}),'original_pairs_not_drafted':missing,'additional_pair_entries':sorted({r['label'] for r in records if r['event_class'] not in ['regulatory_rearrangement']}-set(proposed)),'source_count':len(sources),'partner_count':len(partners),'clinical_sections':dict(collections.Counter(s['kind'] for r in records for s in r['sections'])),'deferred':c['deferred'],'status':'all_written_entries_are_unreviewed_drafts'}
    save(ROOT/'data/fusion-drafting-review.json',stats)
    queue=[{'fusion_id':r['id'],'label':r['label'],'section_kind':s['kind'],'text':s['text'],'claim_sha256':s['claim_sha256'],'source_ids':s['source_ids'],'review_status':'pending','reviewer':None} for r in records for s in r['sections']]
    save(ROOT/'data/fusion-evidence-review-queue.json',{'built_on':c['drafted_on'],'status':'pending_claim_level_adjudication','claim_count':len(queue),'claims':queue})
    print(json.dumps(stats,indent=2))
if __name__=='__main__':main()
