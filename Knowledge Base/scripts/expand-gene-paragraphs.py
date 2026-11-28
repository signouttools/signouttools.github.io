"""Review all gene paragraph lengths and restore useful, already sourced function detail.
Run after prepare-report-comments.py. Disease claims and PMID-bound sections are
preserved. A soft word target never authorizes invented or padded biology.
"""
import hashlib,json,re
from pathlib import Path
root=Path(__file__).resolve().parents[1]
def load(p):return json.loads(p.read_text())
def save(p,d):p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
def digest(s):return hashlib.sha256(s.encode()).hexdigest()
def words(g):return len(' '.join(s['text'] for s in g['report_summary'].values()).split())
sources={s['id']:s for s in load(root/'data/sources.json')}
manual=load(root/'curation/gene-paragraph-expansions.json')['function_by_symbol']
audit_path=root/'data/citation-audit.json';policy_path=root/'curation/citation-audit-policy.json'
audit=load(audit_path);policy=load(policy_path)
# These activities alone add little useful explanation to a report paragraph.
generic={'protein binding','identical protein binding','protein homodimerization activity','protein heterodimerization activity','enzyme binding','DNA binding','RNA binding','metal ion binding','zinc ion binding','ATP binding','nucleotide binding','GTP binding'}
rows=[];changed=[]
manifest=load(root/'data/manifest.json');genes=[]
for relative in manifest['gene_files']:
 path=root/'data'/relative;g=load(path);sec=g['report_summary']['function'];before=words(g);old=sec['text'];key='gene:'+g['id']+':function';reason='Concise paragraph retained; additional source review needed before adding substantive claims.'
 # A primary PMID cannot be inherited by changed prose without renewed review.
 protected=any(sources[s].get('pmid') for s in sec['source_ids']) or audit['bindings'][key]['verified_pmids']
 text=old
 if not protected:
  if g['symbol'] in manual:
   text=manual[g['symbol']];reason='Expanded normal-function synthesis from the cited NCBI/RefSeq summary.'
  else:
   evidence=g['summary']['function']['text']
   match=re.search(r'Annotated molecular activities include (.+?)\.',evidence)
   if match and set(g['summary']['function']['source_ids']).issubset(sec['source_ids']):
    activities=[a for a in re.split('; | and ',match[1]) if a not in generic]
    activities=[a for a in activities if a.lower() not in old.lower()]
    if activities:
     # Preserve the annotation's scope; do not assign complex ATPase activity to
     # an individual subunit or turn binding annotations into enzymatic claims.
     sentence='Functional annotations also associate the protein with '+(' and '.join(activities))+'.'
     if sentence not in old:text=old+' '+sentence
     reason='Restored specific molecular-activity annotations omitted from the concise projection; no new biological inference.'
 if text!=old:
  sec['text']=text
  # Only database-backed function sections enter this path: no PMID support is
  # relabeled or expanded, and all disease-specific bindings stay untouched.
  assert not protected
  audit['bindings'][key]['text_sha256']=digest(text)
  policy['bindings'][key]['text_sha256']=digest(text)
  save(path,g);changed.append(g['symbol'])
 after=words(g)
 rows.append(dict(gene_id=g['id'],symbol=g['symbol'],before_words=before,after_words=after,expanded=text!=old,source_reviewed=g['symbol'] in manual,reason=reason,below_soft_target=after<80,above_soft_target=after>300,report_gaps=g.get('report_gaps',[])))
 genes.append(g)
save(root/'data/gene-index.json',genes);save(audit_path,audit);save(policy_path,policy)
report=dict(reviewed_on='2026-11-27',target_words=[80,300],target_is_soft=True,genes_reviewed=len(genes),expanded=len(changed),within_target=sum(80<=r['after_words']<=300 for r in rows),below_target=sum(r['after_words']<80 for r in rows),above_target=sum(r['after_words']>300 for r in rows),scope='All paragraphs screened for length, available functional detail, and existing disease-evidence gaps. This is an editorial expansion pass, not new primary-literature adjudication. Short entries are retained where additional supported content is unavailable in this pass.',records=rows)
save(root/'data/gene-paragraph-review.json',report)
lines=['# Gene paragraph expansion review','',f'Reviewed {len(genes):,} gene paragraphs against the soft 80–300-word target. Expanded {len(changed):,} in this pass. After expansion, {report["within_target"]:,} are within the target and {report["below_target"]:,} remain shorter.','', f'{len(manual)} gene-specific normal-function syntheses use the existing cached NCBI/RefSeq summaries. Other expansions restore specific molecular-activity annotations previously omitted from the report projection. Generic binding-only annotations are omitted. Disease associations and their primary-literature citation bindings are preserved.','', 'Shorter paragraphs remain permissible. Many entries have unresolved germline or somatic evidence gaps, or lack enough explanatory functional evidence to justify a longer synthesis. These entries need further source review before substantive disease or mechanism claims can be added. The machine-readable review records a decision, word counts, and existing evidence gaps for every gene. This pass does not constitute a new full-text review of 1,305 genes.','', 'Regenerate with `python3 "Knowledge Base/scripts/expand-gene-paragraphs.py"` after preparing report projections, then refresh the draft export with `write-hotspot-review.py`. Changes with retained PMID citations require separate claim-specific review.','', '| Gene | Before | After | Decision |','| --- | ---: | ---: | --- |']
lines += [f'| {r["symbol"]} | {r["before_words"]} | {r["after_words"]} | {r["reason"]} |' for r in rows if r['expanded']]
(root/'GENE-PARAGRAPH-REVIEW.md').write_text('\n'.join(lines)+'\n')
print(json.dumps({k:v for k,v in report.items() if k not in ['records','scope']}))
