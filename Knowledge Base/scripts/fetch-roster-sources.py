"""Download and verify frozen public inventory inputs; requires curl and pdftotext."""
import concurrent.futures,hashlib,json,subprocess,sys
from pathlib import Path
root=Path(__file__).resolve().parents[1]
out=Path(sys.argv[1]);out.mkdir(parents=True,exist_ok=True)
sources=json.loads((root/'inventory/roster.json').read_text())['sources']
def fetch(s):
 filename=s.get('file') or {'hgnc':'hgnc.tsv','driver-atlas':'drivers.html'}[s['id']]
 dest=out/filename
 subprocess.run(['curl','-sSL','--fail','--max-time','120',s['url'],'-o',str(dest)],check=True)
 digest=hashlib.sha256(dest.read_bytes()).hexdigest()
 if digest!=s['sha256']:raise RuntimeError(f"Source changed: {s['id']}; review its new version before rebuilding")
 if s['kind']=='amp':subprocess.run(['pdftotext','-layout',str(dest),str(out/(s['id']+'.txt'))],check=True)
 print('Verified',s['id'])
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:list(pool.map(fetch,sources))
(out/'fetch-sources.json').write_text(json.dumps([s for s in sources if s['id'] not in ['hgnc','driver-atlas']],indent=2)+'\n')
