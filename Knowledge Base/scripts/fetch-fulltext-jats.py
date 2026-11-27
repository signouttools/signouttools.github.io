"""Alternate public PMC API retrieval. Usage: python3 fetch-fulltext-jats.py FULLTEXT_CACHE
Downloading a document is not a claim-support decision.
"""
import json,subprocess,time,concurrent.futures,hashlib,xml.etree.ElementTree as ET,sys
from pathlib import Path
root=Path(__file__).resolve().parents[1];p=root/'data/fulltext-review-queue.json';q=json.load(open(p));cache=Path(sys.argv[1]);todo=[a for a in q['articles'] if a.get('pmcid') and a['access_status']!='public_fulltext_downloaded']
def fetch(a):
 pmc=a['pmcid'];path=cache/(pmc+'-jats.xml');url='https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pmc&retmode=xml&id='+pmc.replace('PMC','')
 if not path.exists():
  subprocess.run(['curl','-sSL','--fail','--retry','1','--max-time','40',url,'-o',str(path)],capture_output=True);time.sleep(.75)
 try:
  r=ET.parse(path).getroot();article=r.find('.//article');body=article.find('body') if article is not None else None;text=''.join(body.itertext()) if body is not None else '';pmid=article.findtext(".//article-id[@pub-id-type='pmid']") if article is not None else None
  if len(text)>1000 and pmid==a['pmid']:return dict(a,access_status='public_fulltext_downloaded',format='jats',access_url=url,cache_file=path.name,fulltext_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),body_characters=len(text))
 except (ET.ParseError,FileNotFoundError):pass
 return dict(a,jats_fallback_status='fulltext_not_returned_or_not_matched',jats_access_url=url)
results={}
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
 for i,a in enumerate(pool.map(fetch,todo)):
  results[a['pmid']]=a
  if i%25==0:
   q['articles']=[results.get(x['pmid'],x) for x in q['articles']];p.write_text(json.dumps(q,indent=2)+'\n');print('PMC alternate API assessed',i+1,'of',len(todo),flush=True)
q['articles']=[results.get(x['pmid'],x) for x in q['articles']];p.write_text(json.dumps(q,indent=2)+'\n');print('Finished',len(todo),flush=True)
