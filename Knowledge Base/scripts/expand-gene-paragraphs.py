"""Apply source-reviewed functional prose and report soft word-target decisions.
The curated file is the authoring source. PMID-bound functions require separate
claim adjudication; inherited, mosaic, and somatic sections are never rewritten.
"""
import hashlib,json
from pathlib import Path
root=Path(__file__).resolve().parents[1]
def load(p):return json.loads(p.read_text())
def save(p,d):p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
def digest(s):return hashlib.sha256(s.encode()).hexdigest()
def words(g):return len(' '.join(s['text'] for s in g['report_summary'].values()).split())
source_map={s['id']:s for s in load(root/'data/sources.json')}
curated=load(root/'curation/gene-paragraph-expansions.json')
projections=curated['function_by_symbol'];projection_sources=curated.get('function_sources_by_symbol',{})
review_path=root/'curation'/curated.get('complete_source_review_file','gene-paragraph-source-review.json')
review=load(review_path) if review_path.exists() else {'records':[]}
reviews={r['gene_id']:r for r in review['records']}
audit_path=root/'data/citation-audit.json';policy_path=root/'curation/citation-audit-policy.json'
audit=load(audit_path);policy=load(policy_path)
rows=[];changed=[];genes=[]
for relative in load(root/'data/manifest.json')['gene_files']:
 path=root/'data'/relative;g=load(path);sec=g['report_summary']['function'];before=words(g);key='gene:'+g['id']+':function';old=sec['text']
 text=projections.get(g['symbol'],old);ids=projection_sources.get(g['symbol'],sec['source_ids'])
 protected=any(source_map[s].get('pmid') for s in sec['source_ids']) or audit['bindings'][key]['verified_pmids']
 if text!=old or ids!=sec['source_ids']:
  renewal=curated.get('renewed_function_claims',{}).get(g['symbol'])
  if protected or any(source_map[s].get('pmid') for s in ids):
   if not renewal or renewal['text_sha256']!=digest(text):raise ValueError(f'{g["symbol"]}: changed PMID-bound function needs explicit claim review')
   for sid in ids:
    if source_map[sid].get('pmid') and not any(v['source_id']==sid and v['pmid']==source_map[sid]['pmid'] and v['scope'] for v in renewal['verified_pmids']):raise ValueError('Unreviewed publication citation')
   audit['bindings'][key]['verified_pmids']=renewal['verified_pmids']
   policy['bindings'][key]['verified_pmids']=renewal['verified_pmids']
  sec['text']=text;sec['source_ids']=ids
  # Database-backed functions have no PMID. The one renewed primary claim
  # above requires its own exact-text approval; approvals are never inherited.
  audit['bindings'][key]['text_sha256']=digest(text)
  policy['bindings'][key]['text_sha256']=digest(text)
  save(path,g);changed.append(g['symbol'])
 after=words(g);r=reviews.get(g['id'])
 rows.append(dict(gene_id=g['id'],symbol=g['symbol'],before_words=r['before_words'] if r else before,after_words=after,expanded=r['decision'].startswith('expanded_') if r else text!=old,source_reviewed=bool(r) or g['symbol'] in projections,source_review_complete=bool(r and r['review_complete']),reason=r['reason'] if r else 'Existing paragraph outside the remaining short-entry source-review scope.',decision=r['decision'] if r else 'outside_remaining_short_scope',below_soft_target=after<80,above_soft_target=after>300,report_gaps=g.get('report_gaps',[])))
 genes.append(g)
save(root/'data/gene-index.json',genes);save(audit_path,audit);save(policy_path,policy)
report=dict(reviewed_on='2026-11-27',target_words=[80,300],target_is_soft=True,genes_screened=len(genes),source_review_target=review.get('target_gene_count',0),source_review_complete=review.get('review_complete',False),expanded_in_completed_source_pass=sum(r['expanded'] for r in rows if r['gene_id'] in reviews),within_target=sum(80<=r['after_words']<=300 for r in rows),below_target=sum(r['after_words']<80 for r in rows),above_target=sum(r['after_words']>300 for r in rows),scope=review.get('scope',''),records=rows)
save(root/'data/gene-paragraph-review.json',report)
lines=['# Gene paragraph source review','',f'Completed the source pass for all **{report["source_review_target"]:,} remaining short entries**. **{report["expanded_in_completed_source_pass"]:,} paragraphs were expanded or materially clarified**; each remaining entry has an explicit retention decision.','',f'Across the full {len(genes):,}-gene library, **{report["within_target"]:,} paragraphs are 80–300 words**, **{report["below_target"]:,} are shorter**, and **{report["above_target"]:,} are longer. The range is a soft editorial target. A short paragraph is not an unfinished source-review task.','', '## Sources and scope','', 'The pass compared NCBI Gene/RefSeq functional descriptions with reviewed UniProtKB entries matched by HGNC ID. Missing NCBI snapshots were retrieved, and a current reviewed human UniProt functional snapshot was acquired. Source text, selected functional propositions, qualifiers, per-gene URLs, and hashes are preserved in `curation/gene-paragraph-source-review.json`. Curated report projections are stored in `curation/gene-paragraph-expansions.json`.','', 'This was a source-backed molecular-function expansion pass, not new full-text adjudication of every inherited or somatic association. Those sections and their claim-specific publication approvals are preserved. Existing disease-evidence gaps remain explicitly recorded outside report prose.','', 'Entries were retained when the supported concise function was already represented, additional descriptions were uncertain or isoform-dependent, protein identity was not uniquely resolved, or explanatory function remained unknown. Predicted or similarity-based roles are not promoted to established human experimental findings. No minimum word count is enforced.','', 'Targeted editorial checks distinguish AIP from AHR; the CTLH substrate-recognition role of GID4; nicastrin from the catalytic gamma-secretase assembly; Delta ligands from NOTCH receptors in MIB1 signaling; RNA translation from transcription in MSI2; the GDP-to-GTP exchange promoted by SOS1; and the predominant in-vivo reductase role of HSD11B1. Noncoding RNAs, antigen-receptor loci, and pseudogenes are handled separately from protein products.','', '## Reuse and regeneration','', 'Includes selected, adapted UniProtKB functional descriptions. Attribution: UniProt Consortium, [CC BY 4.0](https://www.uniprot.org/help/license). Changes include selection, condensation, and harmonization with the existing paragraph. Individual UniProt entry links accompany each relevant report section.','', 'Run `python3 "Knowledge Base/scripts/expand-gene-paragraphs.py"`, then `python3 "Knowledge Base/scripts/write-hotspot-review.py"`. The expansion step is also invoked after the citation audit by `prepare-report-comments.py`. It does not require the temporary source-download cache.','', '## Per-gene decisions','', '| Gene | Before | After | Source-review decision |','| --- | ---: | ---: | --- |']
lines += [f'| {r["symbol"]} | {r["before_words"]} | {r["after_words"]} | {r["decision"].replace("_"," ")} |' for r in rows if r['gene_id'] in reviews]
(root/'GENE-PARAGRAPH-REVIEW.md').write_text('\n'.join(lines)+'\n')
print(json.dumps({k:v for k,v in report.items() if k not in ['records','scope']}));print('Files updated:',len(changed))
