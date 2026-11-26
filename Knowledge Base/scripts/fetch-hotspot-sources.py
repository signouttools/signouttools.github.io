"""Download the three original releases and FDA reference snapshots.
Usage: python3 fetch-hotspot-sources.py OUTPUT_DIRECTORY
Uses curl with normal TLS certificate verification. Does not execute remote code.
"""
import subprocess,sys,concurrent.futures
from pathlib import Path
p=Path(sys.argv[1]);p.mkdir(parents=True,exist_ok=True)
urls={'v1.xls':'https://www.cancerhotspots.org/files/hotspots.xls','v2.xls':'https://www.cancerhotspots.org/files/hotspots_v2.xls','v3.xlsx':'https://www.cancerhotspots.org/files/hotspots_v3.xlsx','api-v3.json':'https://www.cancerhotspots.org/api/hotspots/single?version=v3','fda-cdx.html':'https://www.fda.gov/medical-devices/in-vitro-diagnostics/list-fda-authorized-companion-diagnostic-devices-in-vitro-and-imaging-tools','fda-pgx.html':'https://www.fda.gov/drugs/science-and-research-drugs/table-pharmacogenomic-biomarkers-drug-labeling','fda-notifications.html':'https://www.fda.gov/drugs/cancer-approvals/oncology-cancerhematologic-malignancies-approval-notifications'}
def fetch(item):
 name,url=item;subprocess.run(['curl','-sSL','--fail','--retry','3','--max-time','120',url,'-o',str(p/name)],check=True);return name,(p/name).stat().st_size
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
 for name,size in pool.map(fetch,urls.items()):print(name,size)
