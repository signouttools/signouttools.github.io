"""Validate complete hotspot representation, source links, and browser derivatives.
Pass original input cache as optional argument to check every workbook row.
"""
import json,hashlib,collections,re,sys
from pathlib import Path
root=Path(__file__).resolve().parents[1]
def load(p):return json.loads(p.read_text())
r=load(root/'data/hotspot-import.json');genes=load(root/'data/gene-index.json');geneids={g['id'] for g in genes};sources={s['id']:s for s in load(root/'data/sources.json')};diseases={d['id'] for d in load(root/'data/diseases.json')};sites=load(root/'data/hotspots.json');alleles=load(root/'data/hotspot-alleles.json');disruptions=load(root/'data/disruption-comments.json');fda=load(root/'data/fda-references.json');refs={x['id']:x for x in fda};by_site={s['id']:s for s in sites};by_allele={a['id']:a for a in alleles};index=load(root/'data/hotspot-index.json')
schema=load(root/'schemas/hotspot.schema.json')
def shape(value,rule,at):
 if '$ref' in rule:return shape(value,schema['$defs'][rule['$ref'].split('/')[-1]],at)
 actual='null' if value is None else 'boolean' if isinstance(value,bool) else 'integer' if isinstance(value,int) else 'number' if isinstance(value,float) else 'string' if isinstance(value,str) else 'array' if isinstance(value,list) else 'object'
 types=rule.get('type');types=[types] if isinstance(types,str) else types
 assert not types or actual in types or actual=='integer' and 'number' in types,(at,actual,types)
 if 'const' in rule:assert value==rule['const'],at
 if 'enum' in rule:assert value in rule['enum'],at
 if actual=='string':
  assert len(value)>=rule.get('minLength',0),at
  if 'pattern' in rule:assert re.search(rule['pattern'],value),at
 if actual in ['number','integer'] and 'minimum' in rule:assert value>=rule['minimum'],at
 if actual=='array':
  assert len(value)>=rule.get('minItems',0),at
  for i,v in enumerate(value):shape(v,rule.get('items',{}),f'{at}[{i}]')
 if actual=='object':
  assert set(rule.get('required',[]))<=set(value),(at,'missing properties')
  for key,v in value.items():
   child=rule.get('properties',{}).get(key)
   if child is not None:shape(v,child,at+'.'+key)
   else:
    additional=rule.get('additionalProperties',True);assert additional is not False,(at,key)
    if isinstance(additional,dict):shape(v,additional,at+'.'+key)
for kind,records in [('site',sites),('allele',alleles),('disruption',disruptions)]:
 for item in records:shape(item,schema['$defs'][kind],kind+':'+item['id'])
assert len(by_site)==len(sites)==r['site_count'];assert len(by_allele)==len(alleles)==r['allele_count']
assert len({x['gene_id'] for x in sites})==r['canonical_hotspot_gene_count']
assert len(genes)==1133+len(r['added_genes'])
assert r['unrepresented_genes']==[]
assert all(m['gene_id'] in geneids for m in r['symbol_mapping'].values())
for receipt in r['original_files']:
 p=root/receipt['file'];assert p.exists() and p.stat().st_size==receipt['bytes'];assert hashlib.sha256(p.read_bytes()).hexdigest()==receipt['sha256']
assert len(r['original_files'])==3
rows=collections.Counter()
for s in sites:
 assert s['gene_id'] in geneids and s['comment']['source_ids']
 assert set(s['disease_ids'])<=diseases
 for obs in s['observations']:
  assert obs['release'] in ['v1','v2','v3'];rows[(obs['workbook'],obs['sheet'])]+=1
  assert obs['row']>=2
  assert all(isinstance(n,int) and n>=0 for n in obs['tumor_counts'].values())
 assert len(s['allele_ids'])==len(set(s['allele_ids']))
 for aid in s['allele_ids']:assert by_allele[aid]['site_id']==s['id'] and by_allele[aid]['gene_id']==s['gene_id']
for sheet in r['sheets']:assert rows[(sheet['workbook'],sheet['sheet'])]==sheet['imported_rows'],sheet
for a in alleles:
 assert a['gene_id'] in geneids and a['site_id'] in by_site
 for obs in a['observations']:assert any(o['workbook']==obs['workbook'] and o['sheet']==obs['sheet'] and o['row']==obs['row'] for o in by_site[a['site_id']]['observations'])
for x in sites+alleles+disruptions:
 assert x['editorial']['status']=='draft' and x['editorial']['reviewer'] is None
 assert x['editorial']['disclaimer']==r['disclaimer']
 assert all(sid in sources for sid in x['comment']['source_ids'])
 if 'report_comment' in x:
  assert all(sid in sources and sources[sid]['kind']!='panel_reference' for sid in x['report_comment']['source_ids'])
 assert x['gene_id'] in geneids
 for refid in x.get('fda_reference_ids',[])+x.get('fda_exclusion_reference_ids',[]):
  assert refid in refs and x['gene_id'] in refs[refid]['gene_ids']
for ref in fda:
 assert not ref['eligibility_asserted']
 assert ref['review_status']=='current_label_and_allele_review_needed'
 assert all(g in geneids for g in ref['gene_ids']) and all(s in sources for s in ref['source_ids'])
 assert all(link['url'].startswith('https://') for link in ref['links'])
for a in alleles:
 for rid in a.get('fda_reference_ids',[]):
  ref=refs[rid];assert 'negative_or_exclusion_biomarker_possible' not in ref['evidence_types'];assert re.search(r'(?<![A-Za-z0-9])'+re.escape(a['label'])+r'(?![A-Za-z0-9])',ref['criteria'])
assert {i['gene_id'] for i in index}=={s['gene_id'] for s in sites}
for i in index:
 shard=load(root/'data'/i['file']);expected=[s for s in sites if s['gene_id']==i['gene_id']];assert len(shard)==i['site_count']==len(expected)
 assert {s['id'] for s in shard}=={s['id'] for s in expected}
 for item in shard:
  original=by_site[item['id']];assert item['comment']==original['comment'];assert item.get('report_comment')==original.get('report_comment');assert item['fda_reference_ids']==original['fda_reference_ids'];assert {a['id'] for a in item['alleles']}==set(original['allele_ids'])
  for a in item['alleles']:assert a=={k:v for k,v in by_allele[a['id']].items() if k!='observations'}
if len(sys.argv)>1:
 cache=Path(sys.argv[1]);sys.path.insert(0,str(cache/'python-deps'));import xlrd,openpyxl
 observed={(o['workbook'],o['sheet'],o['row']) for s in sites for o in s['observations']}
 expected=set()
 for v in [1,2,3]:
  book=xlrd.open_workbook(str(cache/f'v{v}.xls')) if v<3 else openpyxl.load_workbook(cache/'v3.xlsx',read_only=True,data_only=True)
  sheets=[(s.name,[s.row_values(i) for i in range(s.nrows)]) for s in book.sheets()] if v<3 else [(s.title,list(s.iter_rows(values_only=True))) for s in book.worksheets]
  for name,rs in sheets:
   header=next(i for i,row in enumerate(rs) if str(row[0]).lower().replace(' ','_')=='hugo_symbol')
   for n,row in enumerate(rs[header+1:],header+2):
    if row[0] and re.fullmatch('[A-Z][A-Za-z0-9-]*',str(row[0])):expected.add((f'v{v}',name,n))
 assert expected==observed,('Missing workbook rows',expected-observed,'Unexpected rows',observed-expected)
 api=load(cache/'api-v3.json');keys={(s['gene_id'],s['residue'],s['kind']) for s in sites}
 for a in api:
  kind='indel_region' if 'indel' in a['type'].lower() else 'single_residue';assert (r['symbol_mapping'][a['hugoSymbol']]['gene_id'],a['residue'],kind) in keys
print(f'Validated {len(sites)} sites, {len(alleles)} allele drafts, {len(disruptions)} disruption drafts, {len(fda)} FDA references, {len(index)} covered genes, original-file hashes, row completeness, and browser shards. No therapy eligibility is asserted.')
