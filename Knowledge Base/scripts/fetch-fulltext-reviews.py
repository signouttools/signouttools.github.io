"""Build the remaining PMID review queue and fetch public PMC full text.
Usage: python3 fetch-fulltext-reviews.py PUBMED_CACHE FULLTEXT_CACHE
Downloads are evidence access only, never a verification decision.
"""
import json,sys,hashlib,subprocess,concurrent.futures,xml.etree.ElementTree as ET
from pathlib import Path
root=Path(__file__).resolve().parents[1];pub=Path(sys.argv[1]);cache=Path(sys.argv[2]);cache.mkdir(parents=True,exist_ok=True)
def load(p):return json.loads(p.read_text())
def save(p,d):p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
audit=load(root/'data/citation-audit.json');rows=[d for d in audit['decisions'] if d['status'].startswith('removed')];articles={}
for p in pub.glob('*.xml'):
 try:r=ET.parse(p).getroot()
 except ET.ParseError:continue
 for a in r.findall('PubmedArticle'):
  pmid=a.findtext('MedlineCitation/PMID');ids={n.get('IdType'):n.text for n in a.findall('PubmedData/ArticleIdList/ArticleId')};articles[pmid]=dict(title=''.join(a.find('.//ArticleTitle').itertext()),pmcid=ids.get('pmc'),doi=ids.get('doi'))
priority=set('TP53 BRCA1 BRCA2 KRAS NRAS HRAS BRAF DDX41 APC PTEN RB1 NF1 NF2 VHL RET MLH1 MSH2 MSH6 PMS2 EPCAM CDH1 STK11 PALB2 BRIP1 RAD51C RAD51D CHEK2 ATM DICER1 SMARCA4 SMARCB1 TSC1 TSC2 MEN1 CDC73 SDHA SDHB SDHC SDHD FLCN BAP1 WT1 GATA2 RUNX1 ETV6 CEBPA ANKRD26'.split())
queue={}
for r in rows:
 p=r['pmid'];a=articles.get(p,{})
 queue.setdefault(p,dict(pmid=p,**a,claims=[],review_status='pending_fulltext_review',access_status='not_attempted'))['claims'].append({k:r[k] for k in ['record_id','gene_id','symbol','part']})
items=sorted(queue.values(),key=lambda a:(not any(c['symbol'] in priority for c in a['claims']),-len(a['claims']),a['pmid']))
previous=root/'data/fulltext-review-queue.json';old={x['pmid']:x for x in load(previous)['articles']} if previous.exists() else {}
for item in items:
 if item['pmid'] in old:
  for k in ['review_status','review_decisions']: 
   if k in old[item['pmid']]:item[k]=old[item['pmid']][k]
def fetch(item):
 pmcid=item.get('pmcid')
 if not pmcid:return dict(item,access_status='no_pmc_fulltext_in_pubmed_record',access_url='https://doi.org/'+item['doi'] if item.get('doi') else 'https://pubmed.ncbi.nlm.nih.gov/'+item['pmid']+'/')
 path=cache/(pmcid+'.xml');url=f'https://www.ncbi.nlm.nih.gov/research/bionlp/RESTful/pmcoa.cgi/BioC_xml/{pmcid}/unicode'
 if not path.exists():
  run=subprocess.run(['curl','-sSL','--fail','--retry','1','--max-time','35',url,'-o',str(path)],capture_output=True)
  if run.returncode:return dict(item,access_status='public_fulltext_fetch_failed',access_url=url)
 try:
  doc=ET.parse(path);passages=doc.findall('.//passage');body=[p for p in passages if (p.findtext("infon[@key='section_type']") or '').upper() not in ['ABSTRACT','TITLE','REF']];n=sum(len(p.findtext('text') or '') for p in body)
  if n<1000:return dict(item,access_status='fulltext_not_returned',access_url=url)
 except ET.ParseError:return dict(item,access_status='invalid_fulltext_response',access_url=url)
 return dict(item,access_status='public_fulltext_downloaded',access_url=url,cache_file=path.name,fulltext_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),body_characters=n)
# The first window can be reviewed while the remaining downloads continue.
results=[]
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
 for i,item in enumerate(pool.map(fetch,items)):
  results.append(item)
  if i%25==0:
   save(previous,dict(updated_on='2026-11-26',method='Full text retrieval is not verification; decisions require statement-specific evidence review.',articles=results+items[len(results):]));print('Retrieved/assessed access',len(results),'of',len(items),flush=True)
save(previous,dict(updated_on='2026-11-26',method='Full text retrieval is not verification; decisions require statement-specific evidence review.',articles=results));print('Access inventory finished',len(results),flush=True)
