"""Fetch public draft inputs and verify their frozen receipts before rebuilding.
Usage: python3 fetch-draft-sources.py /path/to/cache
Also requires the inventory cache produced by fetch-roster-sources.py.
"""
import hashlib,json,subprocess,sys,time
from pathlib import Path
root=Path(__file__).resolve().parents[1];dest=Path(sys.argv[1]);dest.mkdir(parents=True,exist_ok=True)
report=json.loads((root/'data/drafting-review.json').read_text());receipts={r['file']:r['sha256'] for r in report['input_receipts']}
ids=[g['ncbi_gene_id'] for g in json.loads((root/'inventory/roster.json').read_text())['genes']]
urls={'gencc.csv':'https://thegencc.org/download/action/submissions-export-csv?format=new','uniprot.tsv':'https://rest.uniprot.org/uniprotkb/stream?query=organism_id%3A9606%20AND%20reviewed%3Atrue&format=tsv&fields=accession,gene_primary,protein_name,go_f,go_p,xref_hgnc'}
for n,start in enumerate(range(0,len(ids),100)):
 urls[f'ncbi-{n}.json']='https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=gene&retmode=json&id='+','.join(ids[start:start+100])
for file,url in urls.items():
 path=dest/file
 if not path.exists():subprocess.run(['curl','-sSL','--fail','--retry','2','--max-time','120',url,'-o',str(path)],check=True)
 if hashlib.sha256(path.read_bytes()).hexdigest()!=receipts[file]:raise RuntimeError('Source changed: '+file+'; review the new snapshot before changing receipts.')
 print('Verified',file,flush=True)
 if file.startswith('ncbi-'):time.sleep(.5)
