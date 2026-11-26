"""Build source-grounded first drafts, never approvals.
Usage: python3 draft-genes.py /path/to/function-cache /path/to/inventory-cache
Requires frozen roster.json, HGNC TSV, NCBI esummary batches, reviewed UniProt
GO annotations, GenCC CSV, and the structured user-supplied tumor atlas.
"""
import csv,json,re,sys,hashlib,collections
from pathlib import Path
root=Path(__file__).resolve().parents[1];cache=Path(sys.argv[1]);inventory_cache=Path(sys.argv[2]);date='2026-11-26'
def load(p):return json.loads(p.read_text())
def save(p,d):p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
overrides=load(root/'data/draft-overrides.json')
roster=load(root/'inventory/roster.json');ids={g['id'] for g in roster['genes']}
hgnc={r['hgnc_id']:r for r in csv.DictReader((inventory_cache/'hgnc.tsv').open(),delimiter='\t')}
ncbi={}
for p in sorted(cache.glob('ncbi-*.json')):
 d=load(p)['result'];ncbi.update({k:v for k,v in d.items() if k!='uids'})
proteins=collections.defaultdict(list)
for r in csv.DictReader((cache/'uniprot.tsv').open(),delimiter='\t'):
 for id in filter(None,map(str.strip,r['HGNC'].split(';'))):
  if id in ids:proteins[id].append(r)
assert len(ncbi)==1133,len(ncbi)
assertions=collections.defaultdict(list)
for r in csv.DictReader((cache/'gencc.csv').open()):
 if r['gene_curie'] in ids:assertions[r['gene_curie']].append(r)
text=(inventory_cache/'drivers.html').read_text();atlas=json.loads(re.search(r'<script[^>]*id="atlas-data"[^>]*>(.*?)</script>',text,re.S)[1]);entities={e['name']:e for e in atlas['entities']}
sources={s['id']:s for s in load(root/'data/sources.json')};diseases={d['id']:d for d in load(root/'data/diseases.json')}
def src(id,title,url,kind='gene_reference',publisher='NCBI'):
 sources[id]=dict(id=id,title=title,publisher=publisher,url=url,kind=kind,accessed_on=date,reuse_notes='Original draft from factual annotations; specialist review pending.')
src('gencc-snapshot','GenCC gene–disease assertions, frozen download','https://thegencc.org/download','germline_reference','GenCC and contributing submitters')
src('atlas-draft','Tumor Driver Atlas — alteration context','https://mikexiong2.github.io/molecular-tumor-drivers/','gene_reference','Tumor Driver Atlas (user-supplied educational resource)')
src('hgnc-draft','HGNC approved identity and gene groups','https://www.genenames.org/','gene_reference','HGNC')
for s in roster['sources']:
 if s['kind']=='panel':src('panel-'+s['id'],s['id']+' exact gene-list snapshot',s['url'],'panel_reference','Illumina' if s['id']=='tso500' else 'cBioPortal DataHub')
def section(t,s):return dict(text=t,source_ids=s)
def new_disease(name,category,prefix,identifier=None):
 id=prefix+'-'+(re.sub(r'[^a-zA-Z0-9]+','-',identifier).strip('-') if identifier else hashlib.sha256(name.encode()).hexdigest()[:12])
 diseases[id]=dict(id=id,name=name,category=category,parent_id=None,synonyms=[],ontology_mappings=[],mapping_status='local_unmapped');return id
mosaic_terms=re.compile(r'mosaic|nevus|naevus|Ollier|Maffucci|McCune|Proteus|encephalocraniocutaneous|melorheostosis|Klippel.Trenaunay|Sturge.Weber|overgrowth spectrum|fibroadipose|vascular malformation|hemimegalencephaly|CLOVES|megalencephaly.capillary',re.I)
manual_functions={
 'CARMN':'CARMN produces a long noncoding RNA implicated in regulation of cardiac muscle cell differentiation.',
 'CDKN2B-AS1':'CDKN2B-AS1 produces an antisense long noncoding RNA at the CDKN2A/CDKN2B locus that interacts with chromatin-regulatory complexes and can influence expression of neighboring cell-cycle regulators.',
 'IGH':'IGH is the immunoglobulin heavy-chain locus; its variable, diversity, joining, and constant segments support antibody production through somatic rearrangement in B cells.',
 'IGK':'IGK is the immunoglobulin kappa light-chain locus and contributes to antibody diversity through variable-to-joining segment rearrangement in B cells.',
 'IGL':'IGL is the immunoglobulin lambda light-chain locus and contributes to antibody diversity through variable-to-joining segment rearrangement in B cells.',
 'LINC01187':'LINC01187 produces a long intergenic noncoding RNA. Its molecular function is insufficiently characterized in the functional sources collected for this draft.',
 'MALAT1':'MALAT1 produces a nuclear long noncoding RNA implicated in regulation of gene expression and ribonucleoprotein organization; processing of its precursor also generates a small cytoplasmic RNA.',
 'MIR143':'MIR143 encodes a microRNA precursor. The mature microRNA participates in post-transcriptional regulation of target transcripts through effects on mRNA stability and translation.',
 'NEAT1':'NEAT1 produces a nuclear long noncoding RNA that serves as a structural component of paraspeckles, nuclear bodies involved in regulation of RNA handling and gene expression.',
 'PVT1':'PVT1 is a noncoding locus near MYC that produces regulatory RNA transcripts. Its proximity to MYC is relevant when interpreting regional copy-number changes and rearrangements.',
 'SBDSP1':'SBDSP1 is a pseudogene related to SBDS. Sequence homology makes it relevant to assay specificity and variant-mapping review; it should not be assumed to encode the functional SBDS protein.',
 'TERC':'TERC encodes the RNA component of telomerase, providing the template used by the TERT catalytic subunit to add telomeric repeats to chromosome ends.',
 'TRG':'TRG is the T-cell receptor gamma locus. Somatic variable-to-joining segment rearrangement contributes to the antigen-receptor repertoire of gamma-delta T cells.'}
manual_roles={'TP53':'tumor_suppressor','RB1':'tumor_suppressor','PTEN':'tumor_suppressor','APC':'tumor_suppressor','BRCA1':'tumor_suppressor','BRCA2':'tumor_suppressor','NF1':'tumor_suppressor','NF2':'tumor_suppressor','VHL':'tumor_suppressor','STK11':'tumor_suppressor','CDKN2A':'tumor_suppressor','SMARCB1':'tumor_suppressor','BAP1':'tumor_suppressor','BRAF':'oncogene','KRAS':'oncogene','NRAS':'oncogene','HRAS':'oncogene','EGFR':'oncogene','ALK':'oncogene','RET':'oncogene','ROS1':'oncogene','MET':'oncogene','KIT':'oncogene','FLT3':'oncogene','IDH1':'metabolic_driver','IDH2':'metabolic_driver'}
def go_terms(text):return [(m[1].strip(),m[2]) for m in re.finditer(r'([^;]+?)\s*\[(GO:\d+)\](?:;|$)',text)]
def choose_terms(terms):
 skip={'protein binding','ATP binding','DNA binding','RNA binding','metal ion binding','identical protein binding','enzyme binding','protein-containing complex binding'}
 eligible=[t for t in terms if t[0] not in skip and len(t[0].split())<=12]
 def priority(t):
  label=t[0]
  score=0
  if 'activity' in label:score+=10
  if any(x in label for x in ['kinase activity','methyltransferase activity','DNA repair','mismatch repair','homologous recombination','RNA splicing','chromatin organization','signal transduction','transcription','telomere maintenance']):score+=20
  if 'binding' in label:score-=5
  if any(x in label for x in ['cellular response to','animal organ','circadian','lifespan']):score-=20
  return -score,len(label.split()),label
 return sorted(eligible,key=priority)[:2]
def function(g):
 sid='ncbi-'+g['ncbi_gene_id'];src(sid,g['symbol']+' — NCBI Gene / RefSeq',f"https://www.ncbi.nlm.nih.gov/gene/{g['ncbi_gene_id']}")
 if g['symbol'] in manual_functions:return section(manual_functions[g['symbol']],[sid]),[],[]
 if g['symbol'] in overrides['functions']:return section(overrides['functions'][g['symbol']],[sid]),[],[]
 rows=proteins[g['id']]; assert rows,g['symbol']
 approved=set(hgnc[g['id']]['uniprot_ids'].split('|'))
 row=sorted(rows,key=lambda r:(r['Entry'] not in approved,r['Gene Names (primary)']!=g['symbol'],r['Entry']))[0]
 usid='uniprot-'+row['Entry'];src(usid,g['symbol']+' — reviewed UniProtKB annotations','https://www.uniprot.org/uniprotkb/'+row['Entry']+'/entry',publisher='UniProtKB / Gene Ontology')
 molecular=choose_terms(go_terms(row['Gene Ontology (molecular function)']));process=choose_terms(go_terms(row['Gene Ontology (biological process)']))
 name=re.sub(r'\s+\([^)]*\)(?![-a-z])','',row['Protein names']).strip()
 sentence=f"{g['symbol']} encodes {name[0].lower()+name[1:] if not name[:3].isupper() else name}."
 if molecular:sentence+=' Annotated molecular activities include '+ ' and '.join(t[0] for t in molecular)+'.'
 if process:sentence+=' It participates in '+ ' and '.join(t[0] for t in process)+'.'
 if not molecular and not process:
  sentence+=' Its detailed molecular activity is not resolved by the reviewed annotations collected for this draft.'
 return section(sentence,[sid,usid]),molecular,process

def inherited(g):
 rows=assertions[g['id']];positive=[r for r in rows if r['classification_title'] in ['Strong','Definitive']]
 conflicts={(r['disease_curie'],r['moi_curie']) for r in rows if r['classification_title'] in ['Disputed Evidence','Refuted Evidence']}
 positive=[r for r in positive if (r['disease_curie'],r['moi_curie']) not in conflicts and r['moi_title']!='Unknown']
 # Require expert ClinGen support or independent strong/definitive support from two submitters.
 supporters=collections.defaultdict(set)
 for r in positive:supporters[(r['disease_curie'],r['moi_curie'])].add(r['submitter_title'])
 positive=[r for r in positive if r['submitter_title']=='ClinGen' or len(supporters[(r['disease_curie'],r['moi_curie'])])>=2]
 ranked=sorted(positive,key=lambda r:(r['submitter_title']!='ClinGen',r['classification_title']!='Definitive',r['disease_title'],r['moi_title']))
 chosen={}
 for r in ranked:chosen.setdefault((r['disease_curie'],r['moi_curie']),r)
 germ=[];mosaic=[];display=[]
 for r in chosen.values():
  is_mosaic=bool(mosaic_terms.search(r['disease_title']));did=new_disease(r['disease_title'],'mosaic' if is_mosaic else 'constitutional','gencc',r['disease_curie'])
  if is_mosaic:mechanism='Postzygotic/mosaic disease context; constitutional versus mosaic applicability requires allele-specific review.'
  else:mechanism=r['moi_title']+'; '+r['classification_title'].lower()+' GenCC assertion from '+r['submitter_title']+'. Allele-specific mechanism requires review.'
  a=dict(disease_id=did,mechanism=mechanism,source_ids=['gencc-snapshot'])
  (mosaic if is_mosaic else germ).append(a)
  if not is_mosaic:display.append(r['disease_title']+' ('+r['moi_title'].lower()+')')
 if display:
  # Two representative associations keep the paragraph short; all retained in structured data.
  text='Strong or definitive GenCC assertions link constitutional variants to '+ '; '.join(display[:2])+'.'
  if len(display)>2:text+=' Additional curated associations are listed below.'
  status='uncertain' # Assertion aggregation is not expert reconciliation or approval.
 elif rows:
  text='The reviewed GenCC assertions do not establish a conflict-free strong or definitive constitutional disease relationship for this draft; limited or conflicting assertions require separate review.';status='uncertain'
 else:text='No constitutional disease assertion was retrieved in the reviewed GenCC snapshot; this does not exclude a germline association.';status='not_established_in_reviewed_sources'
 if mosaic:text+=' Postzygotic mosaic associations are recorded separately.'
 return section(text,['gencc-snapshot']),status,germ,mosaic,conflicts

def somatic(g):
 if g['symbol'] in overrides['somatic']:
  prose,names=overrides['somatic'][g['symbol']];sid='ncbi-'+g['ncbi_gene_id'];links=[]
  for name in names:
   category='hematologic' if re.search('leukemia|lymphoma|hematologic',name,re.I) else 'solid'
   did=new_disease(name,category,'refseq-tumor')
   links.append(dict(disease_id=did,mechanism='Gene-specific alteration context described by NCBI/RefSeq; variant applicability requires review.',source_ids=[sid]))
  return section(prose,[sid]),links,[]
 if g['symbol'] in ['MLH1','MSH2','MSH6','PMS2']:
  sid='amp-mmr-somatic';src(sid,'AMP sporadic solid tumors — MMR deficiency','https://www.amp.org/AMP/assets/File/education/MIMP/SolidTumors_Sporadic.pdf',publisher='Association for Molecular Pathology')
  names=['Colorectal carcinoma','Endometrial carcinoma'];links=[]
  for name in names:
   did=new_disease(name,'solid','refseq-tumor');links.append(dict(disease_id=did,mechanism='Tumor mismatch-repair deficiency context; protein loss is not itself a sequence-mutation call.',source_ids=[sid]))
  prose='Loss of mismatch-repair function involving '+g['symbol']+' is relevant in colorectal and endometrial carcinomas. Protein-expression loss or an MSI phenotype does not by itself establish a somatic sequence mutation.'
  if g['symbol']=='MLH1':prose+=' MLH1 promoter methylation is a distinct mechanism of tumor-associated silencing.'
  return section(prose,[sid]),links,[]
 found={};excluded=[]
 for mention in g['coverage_mentions']:
  if mention['source_id']!='driver-atlas' or not set(mention['alteration_classes'])&{'snv','cnv','rearr'}:continue
  entity=entities[mention['context']];term=mention['submitted_symbol'];qualifying=set()
  if re.search(r'germline|predisposition',entity['name'],re.I):continue
  for field in set(mention['alteration_classes'])&{'snv','cnv','rearr'}:
   for line in entity[field]:
    expanded=re.sub(r'\b([A-Z][A-Z0-9-]*?)(\d+)((?:/\d+)+)',lambda m:' '.join(m[1]+x for x in [m[2]]+m[3].split('/')[1:]),line)
    if not re.search(r'(?<![A-Za-z0-9-])'+re.escape(term)+r'(?![A-Za-z0-9-])',expanded):continue
    if re.search(r'\b(no|not|without|wild.type|absence|absent|negative|lacks|uncommon|rarely)\b',line,re.I):
     excluded.append(dict(entity=entity['name'],field=field,reason='negative_or_qualifying_language'));continue
    qualifying.add(field)
  if qualifying:found[entity['name']]=dict(entity=entity,fields=sorted(qualifying))
 associations=[]
 labels={'snv':'sequence alteration','cnv':'copy-number alteration','rearr':'rearrangement'}
 for name,info in sorted(found.items()):
  system=info['entity']['system'];category='cns' if system=='CNS' else 'hematologic' if system in ['B-cell & plasma-cell neoplasms','T-cell & NK-cell neoplasms','Myeloid & acute leukemias','Histiocytic & dendritic neoplasms'] else 'solid'
  did=new_disease(name,category,'atlas',info['entity']['id']);mechanism='Educational atlas reports '+', '.join(labels[f] for f in info['fields'])+' context; exact allele and disease applicability require review.'
  associations.append(dict(disease_id=did,mechanism=mechanism,source_ids=['atlas-draft']))
 if associations:
  names=sorted(found,key=lambda n:(len(n),n))[:3]
  text=('Somatic alterations are described across multiple tumor groups, including ' if len(found)>=12 else 'Reported somatic alteration contexts include ')+ '; '.join(names)+'.'
  text+=' The alteration class and exact variant must be assessed in the disease context.'
  return section(text,['atlas-draft']),associations,excluded
 panel_sources=sorted(set('panel-'+m['source_id'] for m in g['memberships']))
 if panel_sources:
  text='This gene is included in cancer-panel definitions, but a disease-specific somatic association has not been assigned from the alteration-context sources reviewed for this draft.'
  return section(text,panel_sources),[],excluded
 # Education-only marker: do not turn an IHC/expression/pitfall mention into a mutation claim.
 for m in g['coverage_mentions']:
  source=next(s for s in roster['sources'] if s['id']==m['source_id']);sid='education-'+source['id']
  src(sid,source['id']+' — coverage reference',source['url'],publisher='AMP' if source['kind']=='amp' else 'Tumor Driver Atlas')
  return section('The gene appears in specialty educational coverage, but a disease-specific somatic driver relationship has not been assigned in this draft; expression-marker or assay-context mentions are not mutation evidence.',[sid]),[],excluded
 raise ValueError(g['symbol'])

panels=[]
for s in roster['sources']:
 if s['kind']=='panel':panels.append(dict(id=s['id'],name=s['id'],assay_family='MSK-IMPACT' if s['id'] in ['impact505','heme468'] else s['id'],provider='Illumina' if s['id']=='tso500' else 'cBioPortal DataHub',version='snapshot-2026-11-26-'+s['sha256'][:12],exact_list_url=s['url'],source_ids=['panel-'+s['id']],acquisition_status='acquired'))
panel_map={p['id']:p for p in panels}
pilot_ids={'HGNC:1097','HGNC:5382','HGNC:11998'};genes=[];evidence={};report=[]
for candidate in roster['genes']:
 id=candidate['id'];path=root/'data/genes'/ (id.split(':')[1]+'.json')
 f,mol,proc=function(candidate);germ,status,ga,ma,conflicts=inherited(candidate);som,sa,excluded=somatic(candidate)
 gene=dict(id=id,symbol=candidate['symbol'],name=candidate['name'],ncbi_gene_id=candidate['ncbi_gene_id'],aliases=candidate['aliases'],roles=[manual_roles.get(candidate['symbol'],'other')],pathways=[p[0] for p in proc],summary=dict(function=f,germline=germ,somatic=som),germline_status=status,germline_associations=ga,somatic_associations=sa,mosaic_associations=ma,panel_memberships=[],selection_reason=candidate['rationale']+'; user authorized the complete proposed and reserve roster.',editorial=dict(status='draft',author='Codex — source-grounded annotation draft',reviewer=None,reviewed_on=None,sources_checked_on=date,revision=1,change_note='Initial structured-annotation draft; requires specialist review of wording, allele mechanism, and disease applicability.'))
 if id in pilot_ids:
  gene=load(path) # Preserve the previously hand-composed pilot wording and cited disease links.
  gene['selection_reason']=candidate['rationale']+'; user authorized the complete roster.'
 for m in candidate['memberships']:
  gene['panel_memberships'].append(dict(panel_id=m['source_id'],panel_version=panel_map[m['source_id']]['version'],submitted_symbol=m['submitted_symbol'],alteration_classes=m['alteration_classes'],source_ids=['panel-'+m['source_id']]))
 # Re-running must not duplicate pilot memberships.
 gene['panel_memberships']=list({(m['panel_id'],m['submitted_symbol']):m for m in gene['panel_memberships']}.values())
 evidence[id]=dict(symbol=gene['symbol'],ncbi_summary_sha256=hashlib.sha256(ncbi[candidate['ncbi_gene_id']].get('summary','').encode()).hexdigest(),hgnc_locus_type=hgnc[id]['locus_type'],functional_GO_terms=[dict(label=t[0],id=t[1]) for t in mol+proc],gencc_assertions=[{k:r[k] for k in ['sgc_id','version_number','disease_curie','disease_title','classification_title','moi_title','submitter_title','submitted_as_public_report_url','submitted_as_date']} for r in assertions[id]],excluded_atlas_contexts=excluded)
 flags=[]
 if not gene['germline_associations']:flags.append('germline_evidence_unresolved')
 if not gene['somatic_associations']:flags.append('somatic_association_unassigned')
 if conflicts:flags.append('gencc_conflicting_assertions')
 if not mol and not proc and candidate['symbol'] not in manual_functions and candidate['symbol'] not in overrides['functions']:flags.append('sparse_function_annotation')
 if ma:flags.append('mosaic_applicability_review')
 words=len(' '.join(gene['summary'][k]['text'] for k in ['function','germline','somatic']).split())
 if words>180:flags.append('paragraph_over_180_words')
 report.append(dict(id=id,symbol=gene['symbol'],flags=flags,word_count=words,original_inventory_group='proposed' if candidate['proposed_inclusion'] else 'reserve',preserved_pilot=id in pilot_ids))
 save(path,gene);genes.append(gene)
manifest=load(root/'data/manifest.json');manifest.update(schema_version='0.2.0',gene_index_file='gene-index.json',data_version='0.2.0-full-draft',gene_files=['genes/'+g['id'].split(':')[1]+'.json' for g in genes],built_on=date)
save(root/'data/sources.json',list(sources.values()));save(root/'data/diseases.json',list(diseases.values()));save(root/'data/panels.json',panels);save(root/'data/manifest.json',manifest)
save(root/'data/gene-index.json',genes);save(root/'data/evidence.json',evidence)
receipts=[dict(file=p.name,sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in sorted(cache.glob('ncbi-*.json'))]+[dict(file=n,sha256=hashlib.sha256((cache/n).read_bytes()).hexdigest()) for n in ['uniprot.tsv','gencc.csv']]
save(root/'data/drafting-review.json',dict(drafted_on=date,genes=report,input_receipts=receipts,method='Annotation-backed first drafts from NCBI identity, reviewed UniProt/GO function, GenCC assertions, and cautiously extracted educational atlas alteration context. All require specialist review. Existing pilot prose preserved.'))
print('Drafted',len(genes),'genes. Flags:',collections.Counter(f for r in report for f in r['flags']))
