"""Create compact search index and per-gene lazy-loaded comment shards."""
import json,collections
from pathlib import Path
root=Path(__file__).resolve().parents[1]
def load(p):return json.loads(p.read_text())
def save(p,d):p.parent.mkdir(exist_ok=True,parents=True);p.write_text(json.dumps(d,ensure_ascii=False,separators=(',',':'))+'\n')
sites=load(root/'data/hotspots.json');alleles={a['id']:a for a in load(root/'data/hotspot-alleles.json')};groups=collections.defaultdict(list)
for s in sites:
 item={k:v for k,v in s.items() if k not in ['observations','allele_ids']};item['releases']=sorted({o['release'] for o in s['observations']});item['alleles']=[{k:v for k,v in alleles[i].items() if k!='observations'} for i in s['allele_ids']];item['observation_count']=len(s['observations']);groups[s['gene_id']].append(item)
index=[]
for gid,items in sorted(groups.items()):
 path='hotspot-genes/'+gid.split(':')[1]+'.json';save(root/'data'/path,items);index.append(dict(gene_id=gid,file=path,site_count=len(items),allele_count=sum(len(s['alleles']) for s in items),disease_ids=sorted({d for s in items for d in s['disease_ids']}),terms=sorted({s['residue'] for s in items}|{a['label'] for s in items for a in s['alleles']})))
save(root/'data/hotspot-index.json',index);m=load(root/'data/manifest.json');m['hotspot_index_file']='hotspot-index.json';save(root/'data/manifest.json',m)
print('Built browser shards for',len(index),'genes')
