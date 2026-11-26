"""Apply auditable stage-one evidence adjudication; never marks clinical approval.
Usage: python3 curate-evidence.py /path/to/draft-input-cache
Reapply after draft-genes.py. IntOGen additions are cohort-level sequence evidence.
"""
import csv,json,re,sys,io,zipfile,hashlib,collections,copy
from pathlib import Path
root=Path(__file__).resolve().parents[1];cache=Path(sys.argv[1]);date='2026-11-26'
DISCLAIMER='Pathologist review needed — LLM-generated summary/review.'
def load(p):return json.loads(p.read_text())
def save(p,d):p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
manifest=load(root/'data/manifest.json');genes=[load(root/'data'/p) for p in manifest['gene_files']];by={g['symbol']:g for g in genes};baseline=load(root/'curation/baseline.json')
sources={s['id']:s for s in load(root/'data/sources.json')};diseases={d['id']:d for d in load(root/'data/diseases.json')}
def source(id,title,url,kind='gene_reference',publisher='Evidence curation',pmid=None,label=None,version=None):
 s=dict(id=id,title=title,publisher=publisher,url=url,kind=kind,accessed_on=date,reuse_notes='Factual evidence and original LLM synthesis. '+DISCLAIMER)
 if pmid:s['pmid']=str(pmid)
 if label:s['citation_label']=label
 if version:s['version']=version
 sources[id]=s;return id

def disease(name,category,code=None):
 for d in diseases.values():
  if d['name'].casefold()==name.casefold() and d['category']==category:return d['id']
 id='curation-'+(code or hashlib.sha256((category+name).encode()).hexdigest()[:12])
 diseases[id]=dict(id=id,name=name,category=category,parent_id=None,synonyms=[],ontology_mappings=[],mapping_status='local_unmapped');return id

def category(name):
 if re.search(r'glioma|glioblastoma|medulloblastoma|ependymoma|brain|central nervous|pineoblastoma|astrocytoma',name,re.I):return 'cns'
 if re.search(r'lymphoma|leuk[ae]mia|myeloma|myeloid|myelodysplas|histiocyt|mastocyt|hematol|haematol|polycythemia',name,re.I):return 'hematologic'
 return 'solid'

def attach(g,name,sid,mechanism,cat=None,code=None):
 did=disease(name,cat or category(name),code);a=next((a for a in g['somatic_associations'] if a['disease_id']==did),None)
 if a:
  if sid not in a['source_ids']:a['source_ids'].append(sid)
 else:g['somatic_associations'].append(dict(disease_id=did,mechanism=mechanism,source_ids=[sid]))
 return did

def article(pmid,title):return source('pmid-'+str(pmid),title,'https://pubmed.ncbi.nlm.nih.gov/'+str(pmid)+'/',kind='primary_study',publisher='PubMed / primary study',pmid=pmid)
# Source identifiers and titles were checked against PubMed; no inferred PMIDs.
papers={
 'ddx41':article(25920683,'Inherited and Somatic Defects in DDX41 in Myeloid Neoplasms'),
 'h3':article(24162739,'Distinct H3F3A and H3F3B driver mutations define chondroblastoma and giant cell tumor of bone'),
 'mgmt':article(15758010,'MGMT gene silencing and benefit from temozolomide in glioblastoma'),
 'ccnd2':article(23255553,'CCND2 rearrangements are the most frequent genetic events in cyclin D1-negative mantle cell lymphoma'),
 'usp6':article(15509545,'USP6 and CDH11 oncogenes identify the neoplastic cell in primary aneurysmal bone cysts'),
 'btk':article(24869598,"Resistance mechanisms for the Bruton's tyrosine kinase inhibitor ibrutinib"),
 'npm1':article(31570891,"Germline NPM1 mutations lead to altered rRNA 2'-O-methylation and cause dyskeratosis congenita"),
 'terc':article(11574891,'The RNA component of telomerase is mutated in autosomal dominant dyskeratosis congenita'),
 'sf3b1':article(21995386,'Somatic SF3B1 mutation in myelodysplasia with ring sideroblasts'),
 'u2af1':article(22158538,'Recurrent mutations in the U2AF1 splicing factor in myelodysplastic syndromes'),
 'srsf2':article(22389253,'Frequency and prognostic impact of mutations in SRSF2, U2AF1, and ZRSR2 in myelodysplastic syndromes')}
# Strictly filtered cohort associations; the unfiltered results are never imported.
z=zipfile.ZipFile(cache/'intogen-drivers.zip');path=next(n for n in z.namelist() if n.endswith('Compendium_Cancer_Genes.tsv'));raw=list(csv.DictReader(io.StringIO(z.read(path).decode()),delimiter='\t'))
cz=zipfile.ZipFile(cache/'intogen-cohorts.zip');cp=next(n for n in cz.namelist() if n.endswith('cohorts.tsv'));cohorts={r['COHORT']:r for r in csv.DictReader(io.StringIO(cz.read(cp).decode()),delimiter='\t')}
intogen_id=source('intogen-20240920','IntOGen driver compendium — download 20240920','https://www.intogen.org/download?file=IntOGen-Drivers-20240920.zip',publisher='IntOGen / BBGLab',label='IntOGen 20240920',version='Download 20240920; archive directory 2024-06-18; README retains 20230531 header. SHA256 recorded in evidence-curation.json.')
aliases=collections.defaultdict(set)
for g in genes:
 for a in g['aliases']:aliases[a].add(g['symbol'])
cohort_evidence=collections.defaultdict(list);pending_before={g['symbol'] for g in genes if not g['somatic_associations']};new_genes=set()
for r in raw:
 symbol=r['SYMBOL'] if r['SYMBOL'] in by else next(iter(aliases[r['SYMBOL']])) if len(aliases[r['SYMBOL']])==1 else None
 if not symbol or r.get('IS_DRIVER')!='True':continue
 try:eligible=float(r['QVALUE_COMBINATION'])<.1 and float(r['SAMPLES'])>=3
 except ValueError:eligible=False
 if not eligible:continue
 c=cohorts[r['COHORT']];g=by[symbol];name=c['CANCER_NAME'];refs=[intogen_id]
 # The cohort publication is provenance for the underlying samples; IntOGen is the
 # source of the statistical driver call. Do not substitute a cohort PMID for it.
 cohort_evidence[g['id']].append(dict(submitted_symbol=r['SYMBOL'],cohort=r['COHORT'],cancer_code=r['CANCER_TYPE'],cancer_name=name,qvalue=float(r['QVALUE_COMBINATION']),mutated_samples=int(float(r['SAMPLES'])),total_samples=int(float(r['TOTAL_SAMPLES'])),research_role=r['ROLE'],cohort_reference=c['REFERENCE'],age=c['AGE'],sample_type=c['TYPE']))
 attach(g,name,intogen_id,'Cohort-level candidate sequence driver in IntOGen (combined q<0.1; at least 3 mutated samples). Statistical association does not classify an individual allele.',code='intogen-'+r['CANCER_TYPE'])
 if symbol in pending_before:new_genes.add(symbol)
for symbol in new_genes:
 g=by[symbol];rows=cohort_evidence[g['id']];counts=collections.Counter(r['cancer_name'] for r in rows)
 names=sorted(counts,key=lambda n:(-counts[n],n))[:3]
 g['summary']['somatic']=dict(text='Somatic sequence alterations have cohort-level candidate-driver evidence in '+ '; '.join(names)+'. This gene-level statistical evidence requires allele-specific review and does not establish the effect of every variant.',source_ids=[intogen_id])
# Individual primary-literature refinements, kept within gene-level stage-one scope.
manual={
 'DDX41':('Acquired DDX41 mutations occur in myeloid neoplasms, including myelodysplastic neoplasms and acute myeloid leukemia, and may coexist with an inherited predisposing allele. Tumor-only testing cannot establish the constitutional origin of a finding.',['Myelodysplastic neoplasm','Acute myeloid leukemia'],'ddx41'),
 'H3-3B':('Somatic H3-3B (formerly H3F3B) mutations are characteristic of chondroblastoma. Their alteration spectrum differs from the H3-3A-associated spectrum in giant cell tumor of bone; these are distinct gene–lesion associations.',['Chondroblastoma'],'h3'),
 'MGMT':('MGMT promoter methylation is a tumor-associated epigenetic mechanism of gene silencing studied in glioblastoma. A sequence variant, promoter methylation, and protein-expression result are different observations and should not be treated as interchangeable.',['Glioblastoma'],'mgmt'),
 'CCND2':('CCND2 rearrangements, often involving immunoglobulin regulatory elements, occur in a subset of cyclin D1-negative mantle cell lymphomas. Rearrangement-associated deregulation should be distinguished from an isolated CCND2 sequence variant.',['Mantle cell lymphoma'],'ccnd2'),
 'USP6':('USP6 rearrangements can produce promoter-driven overexpression in primary aneurysmal bone cysts. These alterations support a neoplastic process in this lesion and should not, by themselves, be interpreted as evidence of malignancy.',['Aneurysmal bone cyst'],'usp6'),
 'CDH11':('CDH11 can act as a promoter-donating partner in USP6 rearrangements in primary aneurysmal bone cysts. This fusion context is distinct from an arbitrary CDH11 sequence alteration.',['Aneurysmal bone cyst'],'usp6'),
 'BTK':('Acquired BTK mutations are documented in chronic lymphocytic leukemia under BTK-inhibitor selective pressure. This treatment-associated somatic context is distinct from constitutional BTK loss of function causing immunodeficiency.',['Chronic lymphocytic leukemia'],'btk'),
 'SF3B1':('Somatic SF3B1 mutations occur in myelodysplastic neoplasms, particularly those with ring sideroblasts. The gene-level association does not replace integrated morphologic, molecular, and classification review.',['Myelodysplastic neoplasm'],'sf3b1'),
 'U2AF1':('Recurrent somatic U2AF1 mutations occur in myelodysplastic neoplasms. Their significance depends on the specific allele, accompanying abnormalities, and the integrated myeloid disease context.',['Myelodysplastic neoplasm'],'u2af1'),
 'SRSF2':('Somatic SRSF2 mutations occur in myelodysplastic and myelodysplastic/myeloproliferative neoplasms. Disease classification requires the accompanying clinical, morphologic, and molecular findings.',['Myelodysplastic neoplasm','Myelodysplastic/myeloproliferative neoplasm'],'srsf2'),
 'ZRSR2':('Somatic ZRSR2 mutations occur in myelodysplastic neoplasms and can disrupt splicing regulation. An isolated mutation does not independently establish an integrated myeloid diagnosis.',['Myelodysplastic neoplasm'],'srsf2')}
for symbol,(text,names,key) in manual.items():
 g=by[symbol];sid=papers[key];g['summary']['somatic']=dict(text=text,source_ids=[sid])
 for name in names:attach(g,name,sid,'Gene-level alteration context supported by primary literature; pathologist review needed.')
# Additional common-gene mechanisms not covered by a sequence-driver screen.
extra_papers={
 'cdk8':article(18794900,'CDK8 is a colorectal cancer oncogene that regulates beta-catenin activity'),
 'amp':article(20164920,'The landscape of somatic copy-number alteration across human cancers'),
 'hr':article(24240112,'Germline and somatic mutations in homologous recombination genes in ovarian, fallopian tube, and peritoneal carcinomas'),
 'ezhip':article(31086175,'PFA ependymoma-associated protein EZHIP inhibits PRC2 activity through a H3 K27M-like mechanism'),
 'igf2':article(19957330,'Loss of imprinting and marked gene elevation are 2 forms of aberrant IGF2 expression in colorectal cancer'),
 'terc_gain':article(17054308,'Genomic integration of oncogenic HPV and gain of the human telomerase gene TERC in cervical cancer progression')}
extra={
 'CDK8':('CDK8 amplification and increased activity have been described in colorectal cancer, with experimental evidence linking CDK8 to beta-catenin-dependent tumor-cell proliferation. This amplification-associated context is distinct from an isolated sequence variant.',['Colorectal carcinoma'],'cdk8'),
 'MCL1':('Focal MCL1 amplification has been observed across multiple cancer types, including lung and breast cancers. Functional studies support an anti-apoptotic survival role in amplified tumor models; an arbitrary sequence variant is a different finding.',['Multiple cancer types','Lung carcinoma','Breast carcinoma'],'amp'),
 'BCL2L1':('BCL2L1 lies in a recurrent focal amplification region in human cancers, with evidence that amplified tumor models depend on its anti-apoptotic activity. Copy-number gain should be distinguished from sequence mutation.',['Multiple cancer types','Lung carcinoma'],'amp'),
 'BRIP1':('Somatic BRIP1 loss-of-function mutations have been documented in ovarian carcinoma. This tumor association is distinct from the gene-specific germline risk assessment and does not establish a clinical implication for every variant.',['Ovarian carcinoma'],'hr'),
 'RAD51C':('Somatic RAD51C loss-of-function mutations have been documented in ovarian carcinoma. Interpretation requires assessment of the specific allele and tumor context.',['Ovarian carcinoma'],'hr'),
 'MRE11':('Somatic MRE11 alterations have been reported in ovarian carcinoma. Somatic involvement in a tumor is distinct from the separately assessed, refuted hereditary breast/ovarian cancer-predisposition claims.',['Ovarian carcinoma'],'hr'),
 'EZHIP':('EZHIP overexpression is associated with posterior fossa group A ependymoma and can inhibit PRC2-mediated H3K27 methylation. This expression-associated mechanism does not establish pathogenicity of an arbitrary EZHIP sequence variant.',['Posterior fossa group A ependymoma'],'ezhip'),
 'IGF2':('Loss of imprinting and increased IGF2 expression have been documented in colorectal cancer. These epigenetic/expression-associated observations are distinct from a somatic coding mutation.',['Colorectal carcinoma'],'igf2'),
 'TERC':('Somatic copy-number gain involving the TERC region has been associated with progression of cervical neoplasia to invasive carcinoma. Regional gain is distinct from the constitutional loss-of-function mechanisms underlying telomere biology disorders.',['Cervical carcinoma'],'terc_gain')}
for symbol,(prose,names,key) in extra.items():
 g=by[symbol];sid=extra_papers[key];g['summary']['somatic']=dict(text=prose,source_ids=[sid])
 for name in names:attach(g,name,sid,'Primary-study gene-level somatic/epigenetic context; alteration class explicitly stated in the paragraph.',cat='pan_cancer' if name=='Multiple cancer types' else None)
# RefSeq statements establish broad amplification, without inventing a tumor list.
for symbol in ['FGF3','FGF4']:
 g=by[symbol];sid='ncbi-'+g['ncbi_gene_id']
 g['summary']['somatic']=dict(text='Amplification of '+symbol+' has been reported in human tumors. A regional copy-number gain does not by itself identify the contribution of this gene relative to neighboring co-amplified genes.',source_ids=[sid])
 attach(g,'Multiple cancer types',sid,'Amplification reported by RefSeq; no specific tumor subtype inferred.',cat='pan_cancer')

# Adjudicate relationship-level disagreements. Keep original assertions and curators.
rows=list(csv.DictReader((cache/'gencc.csv').open()));assertions=collections.defaultdict(list)
for r in rows:
 if r['gene_symbol'] in by:assertions[r['gene_symbol']].append(r)
def cluster(name,curie=None):
 t=name.lower()
 if 'breast' in t and ('cancer' in t or 'carcinoma' in t):return 'hereditary-breast-cancer'
 if 'ovarian' in t and ('cancer' in t or 'carcinoma' in t):return 'hereditary-ovarian-cancer'
 if 'lynch syndrome' in t or 'nonpolyposis colon' in t:return 'lynch-syndrome'
 if 'colorectal cancer' in t or 'colon cancer' in t:return 'colorectal-cancer'
 return curie or re.sub(r'[^a-z0-9]+','-',t).strip('-')
def mode(text):
 for m in ['autosomal dominant','autosomal recessive','x-linked recessive','x-linked','semidominant']:
  if m in text.lower():return m
 return 'unknown'
def assertion_source(r):
 id='gencc-'+r['sgc_id']+'.'+r['version_number'];label=r['submitter_title']+' '+r['sgc_id']+'.'+r['version_number']
 source(id,r['gene_symbol']+' / '+r['disease_title']+' — '+r['classification_title'],r['submitted_as_public_report_url'] if r['submitted_as_public_report_url'].startswith('https://') else 'https://thegencc.org/submissions/'+r['sgc_id']+'.'+r['version_number'],kind='germline_reference',publisher=r['submitter_title'],label=label,version='Assertion '+r['submitted_as_date']);return id
prior_flagged={g['symbol'] for g in baseline['baseline_gene_flags'] if 'gencc_conflicting_assertions' in g['flags']}
resolutions=[];gene_decisions=collections.defaultdict(list)
for symbol in sorted(prior_flagged):
 rr=assertions[symbol];neg=[r for r in rr if r['classification_title'] in ['Disputed Evidence','Refuted Evidence']];seen=set()
 for n in neg:
  key=(cluster(n['disease_title'],n['disease_curie']),mode(n['moi_title']))
  if key in seen:continue
  seen.add(key)
  relevant=[r for r in rr if cluster(r['disease_title'],r['disease_curie'])==key[0] and (mode(r['moi_title'])==key[1] or mode(r['moi_title'])=='unknown' or key[1]=='unknown')]
  expert=[r for r in relevant if r['submitter_title']=='ClinGen'];chosen=max(expert,key=lambda r:r['submitted_as_date'][:10]) if expert else n
  pos=[r for r in relevant if r['classification_title'] in ['Strong','Definitive']]
  if expert:
   decision='withhold_relationship_expert_'+chosen['classification_title'].lower().replace(' ','_')
   rationale='Use the condition-specific ClinGen expert curation for draft inclusion; a positive assertion for another disorder does not rescue this relationship. This is an LLM editorial decision, not pathologist approval.'
  elif pos:
   decision='unresolved_nonexpert_disagreement';rationale='Conflicting nonexpert assertions lack a decisive expert curation; withhold and retain an unresolved review flag.'
  else:
   decision='withhold_unestablished_relationship';rationale='The disputed/refuted relationship has no opposing strong/definitive assertion in the reviewed snapshot; withhold this specific claim, retaining separately supported disorders.'
  sid=assertion_source(chosen)
  record=dict(symbol=symbol,disease=n['disease_title'],disease_cluster=key[0],inheritance=key[1],selected_classification=chosen['classification_title'],decision=decision,rationale=rationale,selected_source_id=sid,selected_sgc=chosen['sgc_id']+'.'+chosen['version_number'],selected_date=chosen['submitted_as_date'],has_opposing_strong_assertion=bool(pos),assertions=[dict(sgc=r['sgc_id']+'.'+r['version_number'],disease=r['disease_title'],classification=r['classification_title'],submitter=r['submitter_title'],date=r['submitted_as_date'],curation_url=r['submitted_as_public_report_url']) for r in relevant])
  if symbol=='FANCM' and n['disease_curie']=='MONDO:0019391':record['rationale']='ClinGen split conventional Fanconi anemia from the recessive FANCM Fanconi-like genomic-instability disorder. The original FA proband also had biallelic FANCA variants. Retain the separately curated Fanconi-like disorder; withhold a conventional FA claim despite later differently labeled submitter assertions. Pathologist review needed.'
  resolutions.append(record);gene_decisions[symbol].append(record)
 # Remove unsupported claims, including breast/ovarian disease-label aliases.
 g=by[symbol];kept=[];removed=[]
 for a in g['germline_associations']:
  d=diseases[a['disease_id']];c=cluster(d['name'],a['disease_id'].removeprefix('gencc-').replace('MONDO-','MONDO:'));m=mode(a['mechanism'])
  matches=[r for r in gene_decisions[symbol] if r['disease_cluster']==c and (m==r['inheritance'] or m=='unknown' or r['inheritance']=='unknown')]
  (removed if matches else kept).append(a)
 g['germline_associations']=kept
 # Reconcile prose from the retained links; don't keep a superseded positive claim in text.
 if kept:
  names=list(dict.fromkeys(diseases[a['disease_id']]['name']+' ('+mode(a['mechanism'])+')' for a in kept))
  g['summary']['germline']=dict(text='Retained constitutional disease associations include '+ '; '.join(names[:2])+'. Pathogenicity and inheritance depend on the specific allele and disorder.',source_ids=list(dict.fromkeys(s for a in kept for s in a['source_ids'])))
 else:g['summary']['germline']=dict(text='No established constitutional disease association is assigned after the condition-specific evidence review; disputed or limited relationships are withheld rather than treated as positive findings.',source_ids=[r['selected_source_id'] for r in gene_decisions[symbol]])
 g['germline_status']='uncertain'
 notes=[]
 for r in gene_decisions[symbol]:notes.append(r['disease']+': '+r['selected_classification'].lower()+' ('+sources[r['selected_source_id']]['publisher']+'); not presented as an established association.')
 g['review_notes']=dict(text=' '.join(notes)+' Separately supported conditions remain listed. '+DISCLAIMER,source_ids=list(dict.fromkeys(r['selected_source_id'] for r in gene_decisions[symbol])))
# Named common-gene refinements avoid misleading umbrella labels or confidence voting.
npm=by['NPM1'];expert=next(r for r in assertions['NPM1'] if r['submitter_title']=='ClinGen');sid=assertion_source(expert)
npm['germline_associations']=[];npm['germline_status']='uncertain';npm['summary']['germline']=dict(text='Rare germline NPM1 variants have been reported in dyskeratosis congenita, but ClinGen rates the broader bone-marrow-failure association as limited. This is distinct from the established acquired NPM1-mutant AML context.',source_ids=[papers['npm1'],sid])
terc=by['TERC'];t=next(r for r in assertions['TERC'] if r['submitter_title']=='ClinGen' and r['classification_title']=='Definitive');ts=assertion_source(t)
terc['summary']['germline']=dict(text='Pathogenic constitutional TERC variants cause autosomal dominant telomere biology disorders, including dyskeratosis congenita. Marrow failure and myeloid malignancy risk occur within this inherited disease context; a tumor-only result does not establish constitutional origin.',source_ids=[papers['terc'],ts])
# Keep one umbrella TERC telomere-disorder association instead of an isolated AML syndrome.
terc['germline_associations']=[a for a in terc['germline_associations'] if 'leukemia' not in diseases[a['disease_id']]['name'].lower()]
# Canonical CMMRD display names prevent gene-specific syndrome-number artifacts.
for symbol in ['MLH1','MSH2','MSH6','PMS2']:
 g=by[symbol];out=[]
 for a in g['germline_associations']:
  name=diseases[a['disease_id']]['name']
  if 'mismatch repair cancer syndrome' in name.lower():a=copy.deepcopy(a);a['disease_id']=disease('Constitutional mismatch repair deficiency','constitutional','cmmrd')
  if a['disease_id'] not in {x['disease_id'] for x in out}:out.append(a)
 g['germline_associations']=out
# Explicitly leave all stage-two examples untouched, and approval status unchanged.
for name,original in baseline['variant_files'].items():assert (root/'data/variants'/name).read_text()==original,'Unexpected stage-two change: '+name
for g in genes:
 g['editorial']['disclaimer']=DISCLAIMER
 if g['symbol'] in gene_decisions or g['symbol'] in manual or g['symbol'] in new_genes or g['symbol'] in ['NPM1','TERC','FGF3','FGF4'] or g['symbol'] in extra:
  g['editorial'].update(revision=max(2,g['editorial']['revision']),change_note='Stage-one LLM evidence review: disease-specific source adjudication and/or cohort-level somatic evidence. '+DISCLAIMER)
 assert g['editorial']['status']=='draft' and g['editorial']['reviewer'] is None
 save(root/'data/genes'/(g['id'].split(':')[1]+'.json'),g)
# Every formerly missing gene is screened, including those with no eligible signal.
old_missing={g['symbol'] for g in baseline['baseline_gene_flags'] if 'somatic_association_unassigned' in g['flags']}
remaining=[dict(symbol=s,id=by[s]['id'],status='targeted_literature_review_required',catalog_screen='No eligible IntOGen sequence-driver call or individually added primary association in this pass. Catalog absence does not exclude fusions, CNVs, epigenetic effects, or rare disease associations.') for s in sorted(old_missing) if not by[s]['somatic_associations']]
report=dict(date=date,disclaimer=DISCLAIMER,stage_two_ready=False,stage_two_hold_reason='Remaining somatic literature gaps and pathologist review; no new stage-two comments authorized by this pass.',germline_decisions=resolutions,previous_germline_flagged_genes=sorted(prior_flagged),remaining_somatic_gaps=remaining,newly_assigned_somatic_genes=sorted(s for s in old_missing if by[s]['somatic_associations']),source_receipts=[dict(file=n,sha256=hashlib.sha256((cache/n).read_bytes()).hexdigest()) for n in ['intogen-drivers.zip','intogen-cohorts.zip','gencc.csv']],intogen_import_rules='Compendium file only; IS_DRIVER=True; combined q<0.1; >=3 mutated samples. No inferred therapy, allele class, prevalence, or fusion coverage.',intogen_version_note='Download named 20240920; archive directory says 2024-06-18; README retains 20230531 header. Preserve all three labels rather than silently equating them.')
save(root/'data/evidence-curation.json',report);save(root/'data/somatic-cohort-evidence.json',dict(cohort_evidence));save(root/'data/sources.json',list(sources.values()));save(root/'data/diseases.json',list(diseases.values()));save(root/'data/gene-index.json',genes)
manifest['data_version']='0.3.0-evidence-review';save(root/'data/manifest.json',manifest)
# Named citation labels for all remaining sources, without fabricating a PMID.
for s in sources.values():
 if s.get('citation_label'):continue
 if s.get('pmid'):s['citation_label']='PMID '+s['pmid']
 elif 'ncbi.nlm.nih.gov/gene/' in s['url']:s['citation_label']='NCBI Gene '+s['url'].rstrip('/').split('/')[-1]
 elif 'uniprotkb/' in s['url']:s['citation_label']='UniProt '+s['url'].split('uniprotkb/')[1].split('/')[0]
 elif s['id']=='gencc-snapshot':s['citation_label']='GenCC snapshot'
 elif s['id']=='atlas-draft':s['citation_label']='Tumor Driver Atlas'
 elif s['id'].startswith('panel-'):s['citation_label']=s['title'].replace(' exact gene-list snapshot','')
 elif 'GeneReviews' in s['title']:s['citation_label']='GeneReviews: '+s['title'].split(' — ')[0]
 elif 'AMP' in s['publisher'] or 'Association for Molecular Pathology' in s['publisher']:s['citation_label']=s['title']
 else:s['citation_label']=s['title']
save(root/'data/sources.json',list(sources.values()))
old_review=load(root/'data/drafting-review.json');resolution_symbols=set(gene_decisions);unresolved_symbols={r['symbol'] for r in resolutions if r['decision']=='unresolved_nonexpert_disagreement'}
for r in old_review['genes']:
 g=by[r['symbol']];r['flags']=[f for f in r['flags'] if f not in ['somatic_association_unassigned','gencc_conflicting_assertions','germline_evidence_unresolved']]
 if not g['somatic_associations']:r['flags'].append('somatic_association_unassigned')
 if not g['germline_associations']:r['flags'].append('germline_evidence_unresolved')
 if r['symbol'] in unresolved_symbols:r['flags'].append('gencc_conflicting_assertions')
 if r['symbol'] in resolution_symbols:r['flags'].append('relationship_adjudication_pathologist_review')
 r['word_count']=len(' '.join(g['summary'][k]['text'] for k in ['function','germline','somatic']).split())
old_review['disclaimer']=DISCLAIMER;old_review['curation_report']='evidence-curation.json';save(root/'data/drafting-review.json',old_review)
def cite(sid):
 s=sources[sid];return '['+s['citation_label']+']('+s['url']+')'
parts=[]
for g in genes:
 paragraph=' '.join(g['summary'][k]['text']+' ('+', '.join(cite(s) for s in g['summary'][k]['source_ids'])+').' for k in ['function','germline','somatic'])
 parts.append('## '+g['symbol']+'\n\n'+DISCLAIMER+'\n\n'+paragraph+('\n\nEvidence review: '+g['review_notes']['text']+' ('+', '.join(cite(s) for s in g['review_notes']['source_ids'])+').' if g.get('review_notes') else ''))
(root/'DRAFTS.md').write_text('# Gene paragraph drafts\n\n'+DISCLAIMER+'\n\nAll 1,133 entries remain drafts. See EVIDENCE-REVIEW.md for adjudications and remaining gaps.\n\n'+'\n\n'.join(parts)+'\n')
print('Previously missing somatic genes assigned:',len(report['newly_assigned_somatic_genes']))
print('Remaining somatic gaps:',len(remaining))
print('Germline decisions:',len(resolutions),'across',len(prior_flagged),'genes;',len(unresolved_symbols),'unresolved nonexpert disagreements')
