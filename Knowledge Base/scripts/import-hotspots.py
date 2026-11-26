"""Import all three original Cancer Hotspots workbooks; add missing genes.
Usage: bundled-python import-hotspots.py HOTSPOT_CACHE DRAFT_CACHE HGNC_CACHE
Dependencies: xlrd, openpyxl. Input workbooks retained unmodified under hotspots/.
Never infers genomic HGVS, clinical pathogenicity, or treatment eligibility.
"""
import csv,json,re,sys,hashlib,collections,shutil
from pathlib import Path
if (Path(sys.argv[1])/'python-deps').exists():sys.path.insert(0,str(Path(sys.argv[1])/'python-deps'))
import xlrd,openpyxl
root=Path(__file__).resolve().parents[1];cache=Path(sys.argv[1]);draft=Path(sys.argv[2]);hc=Path(sys.argv[3]);date='2026-11-26'
def load(p):return json.loads(p.read_text())
def save(p,d):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def section(t,ids):return dict(text=t,source_ids=ids)
disclaimer='Pathologist review needed — LLM-generated summary/review.'
genes=load(root/'data/gene-index.json');byid={g['id']:g for g in genes};h=list(csv.DictReader((hc/'hgnc.tsv').open(),delimiter='\t'));primary={r['symbol']:r for r in h};aliases=collections.defaultdict(list)
for r in h:
 for a in r['prev_symbol'].split('|')+r['alias_symbol'].split('|'):
  if a:aliases[a].append(r)
def resolve(s):
 if s in primary:return primary[s]
 rows=aliases[s];assert len(rows)==1,(s,[r['symbol'] for r in rows]);return rows[0]
sources={s['id']:s for s in load(root/'data/sources.json')};diseases={d['id']:d for d in load(root/'data/diseases.json')}
def source(id,title,url,kind='gene_reference',publisher='NCBI',pmid=None,label=None):
 s=dict(id=id,title=title,publisher=publisher,url=url,kind=kind,accessed_on=date,reuse_notes='Factual source-linked draft; specialist review pending.',citation_label=label or (f'PMID {pmid}' if pmid else title))
 if pmid:s['pmid']=str(pmid)
 sources[id]=s
for v,pmid,title in [(1,26619011,'Identifying recurrent mutations in cancer reveals widespread lineage diversity and mutational specificity'),(2,29247016,'Accelerating Discovery of Functional Mutant Alleles in Cancer'),(3,41895280,'Cancer type-specific variation in patterns of driver alterations across 50,000 tumors')]:
 source(f'hotspots-v{v}',title,f'https://pubmed.ncbi.nlm.nih.gov/{pmid}/','primary_study','Cancer Hotspots / MSK',pmid)
source('hotspots-download','Cancer Hotspots original release downloads','https://www.cancerhotspots.org/#/download','variant_reference','Cancer Hotspots / MSK',label='Cancer Hotspots downloads')
# Source-specific tumor codes are deliberately retained, without inventing ontology mappings.
tumor_names={'skcm':'Cutaneous melanoma','thca':'Thyroid carcinoma','coadread':'Colorectal carcinoma','coad':'Colon adenocarcinoma','read':'Rectal adenocarcinoma','luad':'Lung adenocarcinoma','lusc':'Lung squamous cell carcinoma','gbm':'Glioblastoma','mmyl':'Multiple myeloma','hgg':'High-grade glioma','lgg':'Low-grade glioma','kirp':'Papillary renal cell carcinoma','kirc':'Clear cell renal cell carcinoma','kich':'Chromophobe renal cell carcinoma','hnsc':'Head and neck squamous cell carcinoma','paad':'Pancreatic adenocarcinoma','ucec':'Endometrial carcinoma','stad':'Gastric adenocarcinoma','ucs':'Uterine carcinosarcoma','cesc':'Cervical carcinoma','ov':'Ovarian carcinoma','brca':'Breast carcinoma','blca':'Bladder urothelial carcinoma','laml':'Acute myeloid leukemia','esca':'Esophageal carcinoma','prad':'Prostate adenocarcinoma','npc':'Nasopharyngeal carcinoma','mds':'Myelodysplastic neoplasm','lihc':'Hepatocellular carcinoma','mbl':'Medulloblastoma','acc':'Adrenocortical carcinoma','dlbcl':'Diffuse large B-cell lymphoma','all':'Acute lymphoblastic leukemia','cll':'Chronic lymphocytic leukemia','skin':'Skin tumors','lung':'Lung tumors','bowel':'Bowel tumors','breast':'Breast tumors','brain':'CNS tumors','blood':'Hematologic neoplasms','lymph':'Lymphoid neoplasms','thyroid':'Thyroid tumors','uterus':'Uterine tumors','ovary':'Ovarian tumors','pancreas':'Pancreatic tumors','prostate':'Prostate tumors','bladder':'Bladder tumors','kidney':'Kidney tumors','stomach':'Gastric tumors','liver':'Liver tumors','biliary_tract':'Biliary tract tumors','head_neck':'Head and neck tumors','soft_tissue':'Soft tissue tumors','bone':'Bone tumors','testis':'Testicular tumors','thymus':'Thymic tumors','adrenal_gland':'Adrenal gland tumors','cervix':'Cervical tumors','unk':'Unspecified tumor site'}
def composition(text):
 result={}
 for pair in str(text or '').split('|'):
  pieces=pair.split(':')
  if len(pieces)>1:
   try:result[pieces[0]]=int(float(pieces[-1]))
   except ValueError:pass
 return result
def disease_for(code):
 did='hotspots-cohort-'+code
 if did not in diseases:
  name=tumor_names.get(code,f'Cancer Hotspots source tumor code: {code}')
  cat='hematologic' if code in ['blood','lymph','laml','mds','mmyl','dlbcl','all','cll'] else 'cns' if code in ['brain','gbm','hgg','lgg','mbl'] else 'pan_cancer' if code=='unk' else 'solid'
  diseases[did]=dict(id=did,name=name+' (hotspot cohort)',category=cat,parent_id=None,synonyms=[code],ontology_mappings=[],mapping_status='local_unmapped')
 return did
sites={};alleles={};receipts=[];symbol_map={};sheet_stats=[]
def add_site(symbol,codon,kind,release,origin,fields,tumors,transcript=None):
 r=resolve(symbol);gid=r['hgnc_id'];symbol_map[symbol]=dict(gene_id=gid,symbol=r['symbol']);key=(gid,str(codon),kind)
 if key not in sites:sites[key]=dict(id='chs-'+hashlib.sha256('|'.join(key).encode()).hexdigest()[:16],gene_id=gid,symbol=r['symbol'],source_symbols=[],residue=str(codon),kind=kind,observations=[],allele_ids=[])
 site=sites[key]
 if symbol not in site['source_symbols']:site['source_symbols'].append(symbol)
 site['observations'].append(dict(release=release,**origin,fields=fields,tumor_counts=tumors,transcript=transcript));return site
# Preserve each workbook row separately, including synonymous/stop and unexpected allele annotations.
for v in [1,2,3]:
 filename=f'v{v}.xls' if v<3 else 'v3.xlsx';p=cache/filename;dest=root/'hotspots'/'original'/filename;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,dest)
 url='https://www.cancerhotspots.org/files/'+{1:'hotspots.xls',2:'hotspots_v2.xls',3:'hotspots_v3.xlsx'}[v]
 receipts.append(dict(release=f'v{v}',file='hotspots/original/'+filename,url=url,sha256=sha(p),bytes=p.stat().st_size))
 book=xlrd.open_workbook(str(p)) if v<3 else openpyxl.load_workbook(p,read_only=True,data_only=True)
 sheets=[(s.name,[s.row_values(i) for i in range(s.nrows)]) for s in book.sheets()] if v<3 else [(s.title,list(s.iter_rows(values_only=True))) for s in book.worksheets]
 for name,rows in sheets:
  headerrow=next(i for i,r in enumerate(rows) if str(r[0]).lower().replace(' ','_')=='hugo_symbol');header=rows[headerrow];count=0
  for rownum,row in enumerate(rows[headerrow+1:],start=headerrow+2):
   symbol=str(row[0] or '')
   if not re.fullmatch(r'[A-Z][A-Za-z0-9-]*',symbol):continue
   count+=1;r={str(k):val for k,val in zip(header,row) if k};origin=dict(workbook=f'v{v}',sheet=name,row=rownum)
   # V1 Per Allele rows support individual alleles but may not match chosen canonical numbering.
   if v==1 and name=='Per Allele':codon=str(r['Reference_Amino_Acid'])+str(r['Amino_Acid_Position']);kind='single_residue';release='v1';tum=composition(r['Tumor_Type_Composition']);allele=str(r['Reference_Amino_Acid'])+str(r['Amino_Acid_Position'])+str(r['Variant_Amino_Acid'])
   elif v==1:codon=str(r['Codon']);kind='single_residue';release='v1';tum=composition(r['Tumor Type Composition']);allele=None
   elif v==2:codon=(str(r['Reference_Amino_Acid']).split(':')[0]+str(r['Amino_Acid_Position'])) if name=='SNV-hotspots' else str(r['Amino_Acid_Position']);kind='single_residue' if name=='SNV-hotspots' else 'indel_region';release='v2';tum=composition(r['Samples']);raw=str(r['Variant_Amino_Acid']).rsplit(':',1)[0];allele=codon+raw if kind=='single_residue' else raw
   elif name=='Hotspot_Residues':codon=str(r['Codon']);kind='single_residue';release='v3';tum=composition(r['Samples']);allele=None
   else:codon=str(r['Codon']);kind='indel_region' if name=='INDEL_Variants' else 'single_residue';release=str(r['Hotspot_Version']);tum=composition(r['Samples']);allele=codon+str(r['Variant_Amino_Acid']) if kind=='single_residue' else str(r['Variant_Amino_Acid'])
   fields={k:r[k] for k in r if k not in ['Allele_Freq_Rank','Samples']}
   site=add_site(symbol,codon,kind,release,origin,fields,tum)
   if allele:
    key=(site['id'],allele)
    if key not in alleles:alleles[key]=dict(id='cha-'+hashlib.sha256('|'.join(key).encode()).hexdigest()[:16],site_id=site['id'],gene_id=site['gene_id'],label=allele,observations=[])
    alleles[key]['observations'].append(dict(release=release,**origin,tumor_counts=tum))
    if alleles[key]['id'] not in site['allele_ids']:site['allele_ids'].append(alleles[key]['id'])
  sheet_stats.append(dict(workbook=f'v{v}',sheet=name,imported_rows=count))
# API enriches transcript identity only when source gene + residue + event type agree.
api=load(cache/'api-v3.json');transcripts={}
for row in api:
 gid=resolve(row['hugoSymbol'])['hgnc_id'];kind='indel_region' if 'indel' in row['type'].lower() else 'single_residue';transcripts[(gid,row['residue'],kind)]=row['transcriptId']
for key,site in sites.items():site['source_transcript']=transcripts.get(key);site['transcript_status']='unversioned_source_transcript' if site['source_transcript'] else 'not_supplied';site['disease_ids']=sorted({disease_for(code) for o in site['observations'] for code in o['tumor_counts']})
# Extend the dictionary by HGNC ID; preserve historical symbols in searchable aliases.
newids={resolve(s)['hgnc_id'] for s in symbol_map}-set(byid);assertions=collections.defaultdict(list);proteins=collections.defaultdict(list);ncbi={}
for p in cache.glob('ncbi-extra-*.json'):
 result=load(p)['result'];ncbi.update({k:v for k,v in result.items() if k!='uids'})
for row in csv.DictReader((draft/'gencc.csv').open()):
 if row['gene_curie'] in newids:assertions[row['gene_curie']].append(row)
for row in csv.DictReader((draft/'uniprot.tsv').open(),delimiter='\t'):
 for gid in map(str.strip,row['HGNC'].split(';')):
  if gid in newids:proteins[gid].append(row)
prior=load(root/'data/hotspot-import.json') if (root/'data/hotspot-import.json').exists() else {}
newgenes=prior.get('added_genes',[])[:];new_evidence=load(root/'data/hotspot-gene-evidence.json') if (root/'data/hotspot-gene-evidence.json').exists() else {}
for gid in sorted(newids):
 hrow=next(r for r in h if r['hgnc_id']==gid);sym=hrow['symbol'];nid=hrow['entrez_id'];record=ncbi.get(nid);assert record,(sym,nid);sid='ncbi-'+nid
 source(sid,sym+' — NCBI Gene / RefSeq','https://www.ncbi.nlm.nih.gov/gene/'+nid,label='NCBI Gene '+nid)
 func=f'{sym} is the approved symbol for {hrow["name"]}.';fids=[sid];terms=[]
 if proteins[gid]:
  protein=sorted(proteins[gid],key=lambda r:(r['Entry'] not in hrow['uniprot_ids'].split('|'),r['Gene Names (primary)']!=sym))[0];usid='uniprot-'+protein['Entry'];source(usid,sym+' — reviewed UniProtKB functional annotations','https://www.uniprot.org/uniprotkb/'+protein['Entry']+'/entry',publisher='UniProtKB / Gene Ontology',label='UniProt '+protein['Entry']);fids.append(usid)
  for field in ['Gene Ontology (molecular function)','Gene Ontology (biological process)']:
   labels=re.findall(r'(?:^|;)\s*([^;]+?)\s*\[GO:\d+\]',protein[field]);labels=[t for t in labels if t not in ['protein binding','ATP binding','DNA binding','RNA binding','metal ion binding','identical protein binding'] and len(t.split())<=12];terms+=labels[:2]
  if terms:func+=' Reviewed functional annotations implicate its product in '+ '; '.join(dict.fromkeys(terms[:3]))+'.'
  else:func+=' The detailed molecular activity is not resolved by the functional annotations collected for this draft.'
 else:func+=' Its function requires manual review of the linked RefSeq summary; a protein activity is not assigned from its name alone.'
 # Relationship-specific conservative GenCC adjudication; never accept an opposing condition.
 rows=assertions[gid];opposed={(r['disease_curie'],r['moi_curie']) for r in rows if r['classification_title'] in ['Disputed Evidence','Refuted Evidence']};supports=collections.defaultdict(set)
 for r in rows:
  if r['classification_title'] in ['Strong','Definitive']:supports[(r['disease_curie'],r['moi_curie'])].add(r['submitter_title'])
 chosen={}
 for r in sorted(rows,key=lambda r:r['submitter_title']!='ClinGen'):
  key=(r['disease_curie'],r['moi_curie'])
  if r['classification_title'] in ['Strong','Definitive'] and key not in opposed and r['moi_title']!='Unknown' and (r['submitter_title']=='ClinGen' or len(supports[key])>=2):chosen.setdefault(key,r)
 ga=[];ma=[];gnames=[]
 for r in chosen.values():
  mosaic=bool(re.search('mosaic|nevus|naevus|overgrowth spectrum',r['disease_title'],re.I));did='hotspots-gencc-'+hashlib.sha256(r['disease_curie'].encode()).hexdigest()[:12]
  diseases[did]=dict(id=did,name=r['disease_title'],category='mosaic' if mosaic else 'constitutional',parent_id=None,synonyms=[],ontology_mappings=[],mapping_status='local_unmapped');a=dict(disease_id=did,mechanism=r['moi_title']+'; '+r['classification_title']+' GenCC assertion, '+r['submitter_title']+'. Allele-specific review required.',source_ids=['gencc-snapshot']);(ma if mosaic else ga).append(a)
  if not mosaic:gnames.append(r['disease_title']+' ('+r['moi_title'].lower()+')')
 germ='Retained strong or definitive GenCC associations include '+ '; '.join(gnames[:2])+'. Allele and inheritance require review.' if gnames else 'No conflict-free strong or definitive constitutional disease relationship met the source-selection criteria for this draft; this does not exclude a germline association.'
 own=[s for s in sites.values() if s['gene_id']==gid];releases=sorted({o['release'] for s in own for o in s['observations']});dids=sorted({did for s in own for did in s['disease_ids']});srcids=['hotspots-'+v for v in releases];names=list(dict.fromkeys(diseases[d]['name'].replace(' (hotspot cohort)','') for d in dids))
 som='Cancer Hotspots '+', '.join(releases)+' reports recurrent residue-level observations in '+('; '.join(names[:3]) if names else 'the analyzed tumor cohorts')+'. This is statistical recurrence evidence; it does not establish that every variant in this gene is a driver or a clinically actionable alteration.'
 if releases==['v1']:som+=' Evidence in this collection is restricted to the historical V1 release.'
 g=dict(id=gid,symbol=sym,name=hrow['name'],ncbi_gene_id=nid,aliases=sorted(set(filter(None,(hrow['alias_symbol']+'|'+hrow['prev_symbol']).split('|')))),roles=['other'],pathways=[],summary=dict(function=section(func,fids),germline=section(germ,['gencc-snapshot']),somatic=section(som,srcids)),germline_status='uncertain' if rows else 'not_established_in_reviewed_sources',germline_associations=ga,somatic_associations=[dict(disease_id=d,mechanism='Historical hotspot cohort observation; individual-allele significance and tumor-specific oncogenicity require review.',source_ids=srcids) for d in dids],mosaic_associations=ma,panel_memberships=[],selection_reason='Added to ensure complete representation of genes in the three Cancer Hotspots original release workbooks.',editorial=dict(status='draft',author='Codex — LLM source-linked hotspot supplement',reviewer=None,reviewed_on=None,sources_checked_on=date,revision=1,change_note='Initial Cancer Hotspots dictionary supplement. '+disclaimer,disclaimer=disclaimer))
 if opposed:g['review_notes']=section('Opposed germline disease/inheritance relationships were excluded from the retained associations and require manual adjudication. Independently supported relationships are assessed separately. '+disclaimer,['gencc-snapshot'])
 byid[gid]=g;genes.append(g);newgenes.append(dict(id=gid,symbol=sym,releases=releases));new_evidence[gid]=dict(ncbi_summary_sha256=hashlib.sha256(record.get('summary','').encode()).hexdigest(),gencc_assertions=[{k:r[k] for k in ['sgc_id','version_number','disease_curie','disease_title','classification_title','moi_title','submitter_title','submitted_as_public_report_url','submitted_as_date']} for r in rows])
for old,mapping in symbol_map.items():
 g=byid[mapping['gene_id']]
 if old!=g['symbol'] and old not in g['aliases']:g['aliases'].append(old)
# Site comments are transparent recurrence summaries, separate from allele/pathogenicity calls.
byallele={a['id']:a for a in alleles.values()}
for site in sites.values():
 releases=sorted({o['release'] for o in site['observations']});labels=[byallele[i]['label'] for i in site['allele_ids']];names=[diseases[d]['name'].replace(' (hotspot cohort)','') for d in site['disease_ids']];context='; '.join(names[:5]) or 'the analyzed cancer cohorts'
 text=f'{site["symbol"]} {site["residue"]} is represented as a '+('recurrent in-frame indel region' if site['kind']=='indel_region' else 'recurrently mutated residue')+' in Cancer Hotspots '+', '.join(releases)+'. Source observations include '+context+'.'
 if len(names)>5:text+=' Additional source tumor types are retained in the structured record.'
 text+=' Statistical enrichment supports review as a candidate somatic hotspot; it does not establish the functional effect, pathogenicity, or treatment sensitivity of every alteration at this position.'
 if releases==['v1']:text+=' This site is present only in the historical V1 material in this collection.'
 site['comment']=section(text,['hotspots-'+v for v in releases]);site['applicability_notes']=['Confirm the exact allele and reference transcript: source protein numbering is not a validated clinical HGVS assertion.','Tumor counts describe source cohorts and may overlap between releases and sheets; they must not be added together.','An observed synonymous or stop allele is retained for source fidelity and is not automatically classified as oncogenic.','FDA references are separate gene-level evidence until the exact biomarker, tumor, setting, and current label have been checked.'];site['editorial']=dict(status='draft',disclaimer=disclaimer,sources_checked_on=date,reviewer=None)
for allele in alleles.values():
 site=next(s for s in sites.values() if s['id']==allele['site_id']);rs=sorted({o['release'] for o in allele['observations']});allele['comment']=section(f'{site["symbol"]} {allele["label"]} is an allele annotation observed in Cancer Hotspots '+', '.join(rs)+f' at the {site["residue"]} hotspot or indel region. This documents recurrence in the source cohorts; allele-specific function, tumor-specific significance, reference-sequence mapping, and clinical actionability require independent review.',['hotspots-'+v for v in rs]);allele['editorial']=dict(status='draft',disclaimer=disclaimer,sources_checked_on=date,reviewer=None)
genes.sort(key=lambda g:g['symbol'])
for g in genes:save(root/'data/genes'/(g['id'].split(':')[1]+'.json'),g)
save(root/'data/gene-index.json',genes);save(root/'data/sources.json',list(sources.values()));save(root/'data/diseases.json',list(diseases.values()));save(root/'data/hotspots.json',list(sites.values()));save(root/'data/hotspot-alleles.json',list(alleles.values()));save(root/'data/hotspot-gene-evidence.json',new_evidence)
newgenes=list({g['id']:g for g in newgenes}.values())
report=dict(built_on=date,license='ODbL-1.0',disclaimer=disclaimer,original_files=receipts,sheets=sheet_stats,symbol_mapping=symbol_map,hotspot_gene_count=len(symbol_map),canonical_hotspot_gene_count=len({m['gene_id'] for m in symbol_map.values()}),added_genes=newgenes,site_count=len(sites),allele_count=len(alleles),unrepresented_genes=[],limitations=['All comments are LLM-generated recurrence drafts; specialist allele-specific review is pending.','V3 includes 164 new residues and cumulative allele sheets; workbook identity and release membership are stored separately.','V1 and V2 API responses were identical at retrieval; release membership comes from original workbooks.','No genomic coordinate or exact-variant HGVS is inferred from a codon.'])
save(root/'data/hotspot-import.json',report)
m=load(root/'data/manifest.json');m.update(data_version='0.4.0-hotspot-draft',gene_files=['genes/'+g['id'].split(':')[1]+'.json' for g in genes],hotspot_file='hotspots.json',hotspot_allele_file='hotspot-alleles.json',hotspot_report_file='hotspot-import.json');save(root/'data/manifest.json',m)
# Keep the stage-one unresolved queue honest after supplementing the dictionary.
r=load(root/'data/evidence-curation.json');r['stage_two_authorized_on']=date;r['stage_two_authorization']='User requested full Cancer Hotspots import and comments while stage-one gaps remain open.';existing={x['symbol'] for x in r['remaining_somatic_gaps']}
for g in genes:
 if not g['somatic_associations'] and g['symbol'] not in existing:r['remaining_somatic_gaps'].append(dict(id=g['id'],symbol=g['symbol'],reason='No source tumor composition supplied in hotspot workbook.'))
save(root/'data/evidence-curation.json',r)
print(json.dumps({k:report[k] for k in ['canonical_hotspot_gene_count','site_count','allele_count']}));print('Added genes',len(newgenes),'total',len(genes))
