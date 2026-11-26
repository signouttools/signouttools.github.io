"""Compile a review inventory from downloaded public sources; no gene prose is generated.
Usage: python3 compile-roster.py /path/to/source-cache
Source URLs and SHA256 receipts are emitted in inventory/roster.json.
"""
import csv, json, re, sys, hashlib, zipfile
from pathlib import Path
from collections import defaultdict,Counter
import xml.etree.ElementTree as ET
cache=Path(sys.argv[1]); out=Path(__file__).resolve().parents[1]/'inventory'
out.mkdir(exist_ok=True)
read=lambda f:(cache/f).read_text()
refs=json.loads(read('fetch-sources.json'))
hgnc=list(csv.DictReader(read('hgnc.tsv').splitlines(),delimiter='\t'))
current={r['symbol']:r for r in hgnc if r['status']=='Approved'}
previous=defaultdict(set); aliases=defaultdict(set)
for r in current.values():
 for key,dest in [('prev_symbol',previous),('alias_symbol',aliases)]:
  for token in r[key].split('|'):
   if token:dest[token].add(r['symbol'])
records={}; unresolved=[]; ignored=Counter(); source_counts={}; events=[]
def resolve(token):
 if token in current:return token,'approved_symbol'
 for mapping,method in [(previous,'previous_symbol'),(aliases,'alias_symbol')]:
  if token in mapping:
   if len(mapping[token])==1:return next(iter(mapping[token])),method
   return None,'ambiguous'
 return None,'unresolved'
def add(token,sid,kind,context='',classes=None,page=None,strict=False):
 if token=='TERTa' and sid=='tso500':token='TERT' # superscript footnote flattened in the manufacturer workbook
 symbol,method=resolve(token)
 if kind!='panel' and symbol:
  allowed_aliases={'HER2','HER3','P53','P16','INI1','BAF155','BAF170'}
  if (method=='alias_symbol' and token not in allowed_aliases) or (method=='previous_symbol' and len(token)<5) or token in {'SDS','HR','CEL','FAP','MPI'}:
   ignored[token]+=1; return
 if not symbol:
  if strict or method=='ambiguous':unresolved.append(dict(term=token,source_id=sid,context=context,mapping_status=method,candidates=sorted(previous.get(token,set())|aliases.get(token,set()))))
  else:ignored[token]+=1
  return
 r=current[symbol]
 g=records.setdefault(r['hgnc_id'],dict(id=r['hgnc_id'],symbol=symbol,name=r['name'],ncbi_gene_id=r['entrez_id'] or None,aliases=sorted(set(filter(None,(r['prev_symbol']+'|'+r['alias_symbol']).split('|')))),status='candidate_for_review',memberships=[],coverage_mentions=[]))
 event=dict(source_id=sid,submitted_symbol=token,mapping_method=method)
 if kind=='panel':event.update(alteration_classes=classes or ['not_specified_in_source_list'])
 else:event.update(context=context,mention_type='educational_reference_not_validated_gene_disease_assertion',page=page,alteration_classes=classes or [])
 target=g['memberships' if kind=='panel' else 'coverage_mentions']
 if event not in target:target.append(event)
 events.append((sid,symbol))
def expand(text):
 # Expand shared-prefix slash lists, e.g. NTRK1/2/3 and IDH1/2.
 return re.sub(r'\b([A-Z][A-Z0-9-]*?)(\d+)((?:/\d+)+)',lambda m:' '.join(m[1]+x for x in [m[2]]+m[3].split('/')[1:]),text)
stop={'AND','OR','WAS','ALL','CAT','SET','REST','MET'} # Ambiguous prose words handled separately below where appropriate.
def tokens(text):return sorted(set(re.findall(r'(?<![A-Za-z0-9])([A-Z][A-Z0-9]*(?:-[A-Z0-9]+)*)(?![A-Za-z0-9])',expand(text))))
# Source lists are explicit membership, not claims about clinical validity or assay coverage.
for s in refs:
 if s['kind']!='panel' or s['id']=='tso500':continue
 text=read(s['file']); terms=re.search(r'^gene_list:\s*(.*)',text,re.M)[1].split()
 for term in terms:add(term,s['id'],'panel',strict=True)
 s['raw_gene_count']=len(terms);s['definition_header']=text.split('gene_list:')[0].strip()
z=zipfile.ZipFile(cache/'tso500.xlsx'); ns={'s':'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
strings=[''.join(x.itertext()) for x in ET.fromstring(z.read('xl/sharedStrings.xml'))]
for row in ET.fromstring(z.read('xl/worksheets/sheet1.xml')).findall('.//s:row',ns):
 cells={}
 for cell in row:
  v=cell.find('s:v',ns)
  if v is not None:cells[re.sub(r'\d','',cell.attrib['r'])]=strings[int(v.text)] if cell.attrib.get('t')=='s' else v.text
 if int(row.attrib['r'])<4 or not cells.get('A'):continue
 term=cells['A'].strip()
 if not re.fullmatch(r'[A-Za-z0-9-]+',term):continue
 classes=[c for col,c in [('B','small_variants'),('C','focal_CNV'),('D','RNA_fusion')] if cells.get(col) not in [None,'-','']]
 if classes:add(term,'tso500','panel',classes=classes,strict=True)
atlas=json.loads(re.search(r'<script[^>]*id="atlas-data"[^>]*>(.*?)</script>',read('drivers.html'),re.S)[1])
for entity in atlas['entities']:
 for field in ['snv','cnv','rearr','other']:
  for text in entity[field]:
   for token in tokens(text):
    if token in stop-{'MET','REST','SET'}:continue
    add(token,'driver-atlas','education',entity['name'],[field])
for s in refs:
 if s['kind']!='amp':continue
 for page,text in enumerate(read(s['id']+'.txt').split('\f'),1):
  # Exclude bibliography where gene names alone do not establish coverage.
  text=re.split(r'(?im)^\s*References?\s*[:\n]',text)[0]
  for token in tokens(text):
   if token in stop-{'MET','REST','SET'}:continue
   add(token,s['id'],'education',s['id'].removeprefix('amp-'),page=page)
# Manual resolutions for commonly used protein names/shorthand, with explicit provenance.
for term,symbol in [('HER2','ERBB2'),('H3F3A','H3-3A'),('H3F3B','H3-3B')]:
 assert resolve(term)[0]==symbol,(term,resolve(term))
for g in records.values():
 families=set('MSK' if m['source_id'] in ['impact505','heme468'] else m['source_id'] for m in g['memberships'])
 g['independent_panel_family_count']=len(families)
 g['selection_group']='recurrent_panel_member' if len(families)>=2 else 'single_panel_member' if families else 'educational_supplement'
 g['writing_priority']='P1' if g['coverage_mentions'] else 'P2'
 g['proposed_inclusion']=bool(g['coverage_mentions']) or len(families)>=2
 g['rationale']='Panel membership with educational coverage' if families and g['coverage_mentions'] else 'Panel membership' if families else 'Specialty educational coverage; confirm inclusion before prose'
ancillary={'AMACR','CA9','CD34','CD7','CDX2','DES','FOLR1','FOXI1','GPNMB','ICOS','L1CAM','LINC01187','MPO','MUC4','MUC6','OLIG2','RHCG','TBX21','TRPS1','VIM','VSTM2A','SBDSP1'}
for g in records.values():
 if g['selection_group']=='educational_supplement' and g['symbol'] in ancillary:
  g['proposed_inclusion']=False
  g['rationale']='Ancillary marker or assay-confounder mention; reserve pending explicit molecular inclusion rationale'
rows=sorted(records.values(),key=lambda g:g['symbol'])
for s in refs:
 s['sha256']=hashlib.sha256((cache/s['file']).read_bytes()).hexdigest()
 s['normalized_gene_count']=len({symbol for sid,symbol in events if sid==s['id']})
refs += [dict(id='driver-atlas',kind='education',url='https://mikexiong2.github.io/molecular-tumor-drivers/',sha256=hashlib.sha256((cache/'drivers.html').read_bytes()).hexdigest(),entity_count=len(atlas['entities']),normalized_gene_count=len({v for k,v in events if k=='driver-atlas'})),dict(id='hgnc',kind='identity',url='https://storage.googleapis.com/public-download-files/hgnc/tsv/tsv/hgnc_complete_set.txt',sha256=hashlib.sha256((cache/'hgnc.tsv').read_bytes()).hexdigest())]
data=dict(schema_version='1.0',compiled_on='2026-11-26',status='inventory_for_review_not_approved_content',method='Explicit panel union plus HGNC-matched educational mentions. Educational mentions are candidates, not independently validated disease associations. See REVIEW.md for extraction limits.',sources=refs,genes=rows,unresolved_terms=unresolved)
(out/'roster.json').write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')
(out/'unmatched-educational-tokens.json').write_text(json.dumps(dict(sorted(ignored.items())),indent=2)+'\n')
print('GENES',len(rows),'GROUPS',Counter(g['selection_group'] for g in rows),'PRIORITIES',Counter(g['writing_priority'] for g in rows))
print('UNRESOLVED',json.dumps(unresolved,indent=2));print('SOURCE COUNTS',[(s['id'],s.get('raw_gene_count'),s.get('normalized_gene_count')) for s in refs])

compact=[dict(symbol=g['symbol'],name=g['name'],id=g['id'],proposed=g['proposed_inclusion'],group=g['selection_group'],priority=g['writing_priority'],panels=sorted(set(m['source_id'] for m in g['memberships'])),contexts=sorted(set(m['context'] for m in g['coverage_mentions'])),aliases=g['aliases'],rationale=g['rationale']) for g in rows]
(out/'review-data.js').write_text('"use strict";\nconst REVIEW_ROSTER = '+json.dumps(compact,ensure_ascii=False)+';\n')
