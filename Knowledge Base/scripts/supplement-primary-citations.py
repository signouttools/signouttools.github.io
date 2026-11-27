"""Supplement report citations from retained relationship/cohort references.
Usage: python3 supplement-primary-citations.py PUBMED_XML_CACHE GENCC_CSV
Never introduces a disease assertion or changes report prose. Keeps provenance.
"""
import json,csv,re,sys,xml.etree.ElementTree as ET,hashlib
from pathlib import Path
root=Path(__file__).resolve().parents[1];cache=Path(sys.argv[1])
if (root/'data/citation-audit.json').exists():raise SystemExit('Automatic report PMID insertion is disabled after the claim-specific audit. Candidate references remain in primary-citation-review.json; extend the explicitly reviewed scopes in audit-report-citations.py instead.')
def load(p):return json.loads(p.read_text())
def save(p,d):p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
genes=load(root/'data/gene-index.json');by={g['id']:g for g in genes};sources={s['id']:s for s in load(root/'data/sources.json')};cohorts=load(root/'data/somatic-cohort-evidence.json');D={d['id']:d for d in load(root/'data/diseases.json')};articles={};links=load(root/'data/primary-citation-review.json').get('added_links',[]) if (root/'data/primary-citation-review.json').exists() else []
def text(e):return ''.join(e.itertext()) if e is not None else ''
for path in cache.glob('*.xml'):
 for a in ET.parse(path).getroot().findall('PubmedArticle'):
  pmid=a.findtext('MedlineCitation/PMID');types=[text(e) for e in a.findall('.//PublicationType')];title=text(a.find('.//ArticleTitle'));abstract=' '.join(text(e) for e in a.findall('.//AbstractText'))
  if any(t in types for t in ['Review','Systematic Review','Meta-Analysis','Editorial','Comment','Guideline','Practice Guideline','Published Erratum','Retraction of Publication','Retracted Publication']):continue
  if not title or not abstract:continue
  articles[pmid]=dict(title=title,abstract=abstract,publication_types=types)
def source(pmid):
 existing=next((s['id'] for s in sources.values() if str(s.get('pmid'))==pmid),None)
 if existing:return existing
 if pmid not in articles:return None
 sid='primary-pmid-'+pmid;sources[sid]=dict(id=sid,title=articles[pmid]['title'],publisher='PubMed / original study authors',url=f'https://pubmed.ncbi.nlm.nih.gov/{pmid}/',kind='primary_study',pmid=pmid,citation_label='PMID '+pmid,accessed_on='2026-11-26',reuse_notes='Primary article identified through a retained disease assertion, original somatic cohort reference, or targeted claim review; citation does not expand the supported claim.')
 return sid
def add(g,part,pmids,route,detail):
 if part not in g['report_summary']:return
 sec=g['report_summary'][part]
 for pmid in pmids:
  sid=source(str(pmid))
  if sid and not any(str(sources[i].get('pmid'))==str(pmid) for i in sec['source_ids']):
   sec['source_ids'].append(sid);links.append(dict(gene_id=g['id'],symbol=g['symbol'],part=part,pmid=str(pmid),route=route,detail=detail))
def gene_mentioned(g,article):
 terms=[g['symbol']]+[a for a in g['aliases'] if len(a)>=3];body=article['title']+' '+article['abstract']
 return any(re.search(r'(?<![A-Za-z0-9])'+re.escape(t)+r'(?![A-Za-z0-9])',body,re.I) for t in terms)
rows=list(csv.DictReader(open(sys.argv[2])));rows.sort(key=lambda r:(r['submitter_title']!='ClinGen',r['classification_title']!='Definitive'))
used={}
for r in rows:
 g=by.get(r['gene_curie'])
 if not g or 'germline' not in g['report_summary'] or r['classification_title'] not in ['Strong','Definitive']:continue
 disease=r['disease_title'];prose=g['report_summary']['germline']['text']
 if disease.lower() not in prose.lower():continue
 # Require that this condition is retained, not merely mentioned as disputed.
 retained=[a for a in g['germline_associations'] if D[a['disease_id']]['name'].lower()==disease.lower()]
 if not retained or not any(r['moi_title'].lower() in a['mechanism'].lower() for a in retained):continue
 key=(g['id'],disease);count=used.get(key,0)
 for pmid in re.findall(r'\b\d{5,9}\b',r['submitted_as_pmids'])[:3]:
  if count>=2:break
  if pmid in articles and gene_mentioned(g,articles[pmid]):
   add(g,'germline',[pmid],'retained_gencc_relationship',dict(disease=disease,inheritance=r['moi_title'],assertion=r['sgc_id'],classification=r['classification_title'],submitter=r['submitter_title']));count+=1
 used[key]=count
# Original cohort publications support observations, not inferred allele-level mechanisms.
def norm(t):return re.sub('[^a-z0-9]','',t.lower())
for g in genes:
 if 'somatic' not in g['report_summary']:continue
 sec=g['report_summary']['somatic'];prose=norm(sec['text'])
 matches={r['cohort_reference']:r for r in cohorts.get(g['id'],[]) if norm(r['cancer_name']) in prose}
 for r in list(matches.values())[:3]:
  pmids=re.findall(r'PMID:(\d+)',r['cohort_reference'])
  add(g,'somatic',[p for p in pmids if p in articles],'original_somatic_cohort',dict(cohort=r['cohort'],cancer=r['cancer_name'],claim_scope='Observed somatic alteration; no individual-allele pathogenicity inferred.'))
# Targeted claim checks for common examples, based on the original studies.
manual={'TP53':{'germline':['1978757','8118819']},'KRAS':{'germline':['16474405','16474404'],'somatic':['26619011','29247016']},'BRCA1':{'somatic':['24240112','21720365','23000897','25719666']},'BRCA2':{'somatic':['24240112','23000897','25719666']}}
for g in genes:
 for part,pmids in manual.get(g['symbol'],{}).items():add(g,part,pmids,'targeted_claim_review','Primary disease-discovery or tumor sequencing studies; claims remain unchanged.')
for g in genes:save(root/'data/genes'/(g['id'].split(':')[1]+'.json'),g)
save(root/'data/gene-index.json',genes)
# The disruption projection reuses the gene's cited tumor observations.
disruptions=load(root/'data/disruption-comments.json')
for d in disruptions:
 som=by[d['gene_id']]['report_summary'].get('somatic')
 if som:
  for sid in som['source_ids']:
   if sources[sid].get('pmid') and sid not in d['report_comment']['source_ids']:d['report_comment']['source_ids'].append(sid)
save(root/'data/disruption-comments.json',disruptions);save(root/'data/sources.json',list(sources.values()))
links=list({(r['gene_id'],r['part'],r['pmid']):r for r in links}.values())
report=dict(checked_on='2026-11-26',added_links=links,genes_supplemented=len({r['gene_id'] for r in links}),primary_articles_added=len({r['pmid'] for r in links}),limitations=['Primary-publication metadata and abstracts checked; full-text and supplementary-data claim review remains pending for automatically linked references.','GenCC candidates require a retained disease/inheritance relationship and gene mention in the publication. Reviews and other non-primary publication types are excluded.','Cohort references support observed somatic variation, not functional or clinical significance of every variant.','Database provenance is retained. Unmatched claims are not assigned unrelated PMIDs.'],pubmed_receipts=[dict(file=p.name,sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in sorted(cache.glob('*.xml'))])
save(root/'data/primary-citation-review.json',report)
print('Supplemented',report['genes_supplemented'],'genes with',report['primary_articles_added'],'primary articles;',len(links),'claim-reference links.')
