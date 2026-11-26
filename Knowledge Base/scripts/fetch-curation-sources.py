"""Fetch IntOGen snapshots for this review; reuse GenCC from fetch-draft-sources.py."""
import hashlib,json,subprocess,sys
from pathlib import Path
root=Path(__file__).resolve().parents[1];dest=Path(sys.argv[1]);dest.mkdir(parents=True,exist_ok=True)
r=json.loads((root/'data/evidence-curation.json').read_text());digests={s['file']:s['sha256'] for s in r['source_receipts']}
for file,url in {'intogen-drivers.zip':'https://www.intogen.org/download?file=IntOGen-Drivers-20240920.zip','intogen-cohorts.zip':'https://www.intogen.org/download?file=IntOGen-Cohorts-20240920.zip'}.items():
 path=dest/file
 if not path.exists():subprocess.run(['curl','-sSL','--fail','--retry','2','--max-time','120',url,'-o',str(path)],check=True)
 assert hashlib.sha256(path.read_bytes()).hexdigest()==digests[file], 'Source changed; review snapshot before updating receipts: '+file
 print('Verified',file)
