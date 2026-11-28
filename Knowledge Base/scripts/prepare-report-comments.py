"""Build concise report-language projections without overwriting evidence records.
All projections remain unreviewed drafts. Dataset/selection provenance stays in
canonical evidence fields and About/review documentation, outside report prose.
"""
import json,re,collections,sys
from pathlib import Path
root=Path(__file__).resolve().parents[1]
def load(p):return json.loads(p.read_text())
def save(p,d):p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
genes=load(root/'data/gene-index.json');by={g['id']:g for g in genes};sources={s['id']:s for s in load(root/'data/sources.json')};diseases={d['id']:d for d in load(root/'data/diseases.json')};sites=load(root/'data/hotspots.json');alleles=load(root/'data/hotspot-alleles.json');disruptions=load(root/'data/disruption-comments.json')
def clean_report_text(text):
 # Editorial safeguards remain outside copyable prose. Keep disease-specific
 # mechanisms and exceptions; remove generic interpretation instructions.
 remove=[
  'Recurrence alone does not establish the oncogenicity of an individual variant.',
  'The functional and clinical significance depend on the specific alteration and tumor type.',
  'Its functional and clinical significance require allele- and tumor-specific assessment.',
  'Clinical implications depend on the tumor type and treatment setting.',
  'Clinical interpretation depends on the tumor type and accompanying histologic and molecular findings.',
  'The effect depends on the affected transcript, variant position, and allelic context.',
  'The biological effect varies by alteration, and a tumor-detected TP53 variant alone does not establish a germline diagnosis.',
  'Interpretation requires the actual fusion structure and disease context.',
  'Variant-level interpretation is required.',
  'Interpretation depends on the specific alteration and tumor context; a generic BRAF finding does not establish a V600E mechanism.',
  'Interpretation requires assessment of the specific allele and tumor context.',
  'Tumor-only testing cannot establish the constitutional origin of a finding.',
  'Tumor-only detection cannot distinguish an acquired event from an inherited predisposition allele.',
  'Disease classification requires the accompanying clinical, morphologic, and molecular findings.',
  'Their significance depends on the specific allele, accompanying abnormalities, and the integrated myeloid disease context.',
  'An isolated mutation does not independently establish an integrated myeloid diagnosis.',
  'Its allele-specific effects require careful distinction from acquired clonal changes.',
  'These observations should be distinguished from an established effect of an arbitrary sequence variant.',
  'This expression-associated mechanism does not establish pathogenicity of an arbitrary EZHIP sequence variant.',
  'Somatic involvement in a tumor is distinct from the separately assessed, refuted hereditary breast/ovarian cancer-predisposition claims.',
  'A regional copy-number gain does not by itself identify the contribution of this gene relative to neighboring co-amplified genes.',
  'Protein-expression loss or an MSI phenotype does not by itself establish a somatic sequence mutation.',
  'Copy-number gain should be distinguished from sequence mutation.',
  'The fusion context should be distinguished from an isolated AFF1 sequence variant.',
  'Rearrangement-associated deregulation should be distinguished from an isolated CCND2 sequence variant.',
  'A sequence variant, promoter methylation, and protein-expression result are different observations and should not be treated as interchangeable.',
  'These alterations support a neoplastic process in this lesion and should not, by themselves, be interpreted as evidence of malignancy.',
  'The R882 mechanism and non-R882 loss of function must be distinguished.',
  'RUNX1 loss-of-function, dominant-negative alleles, and RUNX1 rearrangements require distinct interpretation.'
 ]
 for phrase in remove:text=text.replace(phrase,'')
 replacements={
  '; their presence alone does not establish a uniform functional or clinical effect.':'.',
  '; these findings should not be equated with the effect of every sequence variant.':'.',
  '; not every truncation reproduces the pathogenic linker/RING-domain mechanism.':'.',
  '; a generic truncation does not establish the full tumor genotype.':'.',
  'Sequence homology makes it relevant to assay specificity and variant-mapping review; it should not be assumed to encode the functional SBDS protein.':'Sequence homology with SBDS can complicate variant mapping.',
  '; their significance must be interpreted within the specific disease context.':'.',
  '; expression and sequence-mutation findings require separate interpretation.':'.',
  ', although individual findings require functional and clinical assessment.':'.',
  '; a tumor-only result does not establish constitutional origin.':'.',
  '; allelic state and clonal hematopoiesis may affect interpretation.':'.',
  '; this generic loss-of-function comment must not be applied to those alleles.':'.',
  '; a single variant does not establish biallelic inactivation.':'.',
  ' and should be interpreted with the histologic and molecular findings.':'.',
  '; its clinical implications depend on the tumor type and treatment setting.':'.'
 }
 for old,new in replacements.items():text=text.replace(old,new)
 return re.sub(r'\s+',' ',text).strip()

def section(text,ids):
 seen=set();unique=[]
 for i in ids:
  if sources[i]['kind']=='panel_reference':continue
  key=sources[i].get('pmid') or sources[i]['url'].rstrip('/')
  if key not in seen:seen.add(key);unique.append(i)
 return dict(text=clean_report_text(text),source_ids=unique)
def sentence_list(names):return names[0] if len(names)==1 else ', '.join(names[:-1])+', and '+names[-1] if len(names)>2 else ' and '.join(names)
def name(did):
 n=diseases[did]['name'].replace(' (hotspot cohort)','')
 if n.startswith('Cancer Hotspots source tumor code:') or n=='Unspecified tumor site':return None
 proper={'Ewing','Wilms','Hodgkin','Burkitt','Langerhans','Merkel','Sertoli','Leydig'}
 return ' '.join(w if w in proper or re.match(r'[A-Z0-9]{2,}',w) else w[0].lower()+w[1:] for w in n.split())
# Select representative tumor contexts from already cited structured associations.
# Ranking changes emphasis, not the set of supported associations or their evidence.
priorities={
 'KRAS':['Pancreatic ductal','Colorectal adenocarcinoma','Lung adenocarcinoma'],
 'NRAS':['Melanoma','Acute myeloid','Thyroid'],
 'HRAS':['Head and neck','Bladder','Salivary'],
 'PIK3CA':['Invasive breast carcinoma of no special','Endometrioid carcinoma of endometrium','Colorectal adenocarcinoma'],
 'BRCA1':['High-grade serous','Invasive Breast','Pancreatic ductal'],
 'BRCA2':['Invasive Breast','High-grade serous','Prostate','Pancreatic ductal'],
 'CTNNB1':['Hepatocellular','Endometrioid carcinoma of endometrium','Desmoid','Medulloblastoma'],
 'TET2':['Myelodysplastic neoplasm','Chronic myelomonocytic','Acute myeloid','Nodal T-follicular'],
 'SMARCA4':['Small cell carcinoma of ovary','Thoracic SMARCA4','Lung adenocarcinoma','SMARCA4-deficient uterine'],
 'STAG2':['Urothelial carcinoma','Acute myeloid','Ewing sarcoma'],
 'NPM1':['Acute myeloid leukemia','Myeloid sarcoma','Anaplastic large cell'],
 'DNMT3A':['Acute myeloid','Myelodysplastic','T-cell'],
 'PTEN':['Endometrioid carcinoma of endometrium','Prostate','Glioblastoma','Invasive breast'],
 'APC':['Colorectal adenocarcinoma','Small intestinal','Gastric'],
 'EGFR':['Lung adenocarcinoma','Glioblastoma'],
 'IDH1':['Astrocytoma','Oligodendroglioma','Acute myeloid','Intrahepatic cholangiocarcinoma'],
 'IDH2':['Acute myeloid','Angioimmunoblastic','Sinonasal undifferentiated'],
 'NF1':['Malignant peripheral nerve sheath','Glioblastoma','Pilocytic','Juvenile myelomonocytic'],
 'NF2':['Meningioma','Mesothelioma','Schwannoma'],
 'VHL':['Clear cell renal','Renal Clear Cell','Pheochromocytoma'],
 'RB1':['Retinoblastoma','Small cell lung','Osteosarcoma'],
}
def contexts(g,limit=3):
 def rank(a):
  n=diseases[a['disease_id']]['name'];preferred=priorities.get(g['symbol'],[])
  score=next((i for i,t in enumerate(preferred) if t.lower() in n.lower()),len(preferred)+1)
  clinical=any(i not in ['intogen-20240920'] and not i.startswith('hotspots-') for i in a['source_ids'])
  return score,not clinical,len(n),n
 picked=[];seen=set()
 for a in sorted(g['somatic_associations'],key=rank):
  n=name(a['disease_id'])
  if not n or n.lower() in seen:continue
  seen.add(n.lower());picked.append((n,a['source_ids']))
  if len(picked)==limit:break
 return picked

def function_text(g):
 text=g['summary']['function']['text']
 match=re.match(r'(.+?) is the approved symbol for (.+?)\. Reviewed functional annotations implicate its product in (.+?)\.$',text)
 if match:
  product=match[2];activities=match[3].split('; ')
  text=f'{g["symbol"]} encodes {product}. Its functions include '+sentence_list(activities[:2])+'.'
 elif 'Annotated molecular activities include ' in text:
  first=text.split(' Annotated molecular activities include ')[0]
  process=re.search(r' It participates in (.+?)\.$',text)
  text=first+(' It participates in '+process[1]+'.' if process else ' Its functions include '+text.split('Annotated molecular activities include ')[1])
 text=re.sub(r'^([A-Za-z0-9-]+) is the approved symbol for (.+?)\.',r'\1 encodes \2.',text)
 text=text.replace('The detailed molecular activity is not resolved by the functional annotations collected for this draft.','Its molecular function remains incompletely characterized.').replace('Its molecular function is insufficiently characterized in the functional sources collected for this draft.','Its molecular function remains incompletely characterized.')
 text=text.replace('Its detailed molecular activity is not resolved by the reviewed annotations collected for this draft.','Its molecular function remains incompletely characterized.')
 return text.replace('encodes fanconi','encodes Fanconi')

generated_somatic=('Reported somatic alteration contexts include','Somatic alterations are described across multiple tumor groups','Somatic sequence alterations have cohort-level candidate-driver evidence','Cancer Hotspots ')
literature=load(root/'data/primary-citation-review.json').get('added_links',[]) if (root/'data/primary-citation-review.json').exists() else []
no_germline=0;no_somatic=0
for g in genes:
 parts={'function':section(function_text(g),g['summary']['function']['source_ids'])};gaps=[]
 germ=g['summary']['germline']
 if g['germline_associations']:
  text=germ['text'].replace('Strong or definitive GenCC assertions link constitutional variants to ','Pathogenic germline variants are associated with ').replace('Retained constitutional disease associations include ','Germline disease associations include ').replace('Retained strong or definitive GenCC associations include ','Germline disease associations include ')
  text=text.replace(' Additional curated associations are listed below.','').replace(' Pathogenicity and inheritance depend on the specific allele and disorder.','').replace(' Postzygotic mosaic associations are recorded separately.','').replace(' Allele and inheritance require review.','')
  parts['germline']=section(text,germ['source_ids'])
 elif g['symbol']=='NPM1':parts['germline']=section('Rare germline NPM1 variants have been reported in dyskeratosis congenita; evidence for a broader inherited bone-marrow-failure syndrome is limited.',germ['source_ids'])
 elif g['symbol']=='TERC':parts['germline']=germ
 else:gaps.append('germline_association_requires_curation');no_germline+=1
 # Mosaic disorders are a distinct mechanism, never silently relabeled germline.
 if g['mosaic_associations']:
  selected=g['mosaic_associations'][:2];ns=[diseases[a['disease_id']]['name'] for a in selected];ids=[s for a in selected for s in a['source_ids']]
  parts['mosaic']=section('Postzygotic mosaic variants are associated with '+sentence_list(ns)+'.',ids)
 som=g['summary']['somatic']
 if g['somatic_associations']:
  text=som['text']
  if text.startswith(generated_somatic):
   picked=contexts(g);ns=[n for n,_ in picked];ids=[i for _,ss in picked for i in ss]
   if ns:
    text=f'Somatic alterations involving {g["symbol"]} have been reported in '+sentence_list(ns)+'.'
    if all(i=='intogen-20240920' or i.startswith('hotspots-') for i in ids):text+=' Recurrence alone does not establish the oncogenicity of an individual variant.'
    parts['somatic']=section(text,ids)
   else:gaps.append('somatic_association_requires_curation');no_somatic+=1
  else:
   text=text.replace(' The gene-level association does not replace integrated morphologic, molecular, and classification review.','')
   text=text.replace(' This tumor association is distinct from the gene-specific germline risk assessment and does not establish a clinical implication for every variant.','')
   parts['somatic']=section(text,som['source_ids'])
 else:gaps.append('somatic_association_requires_curation');no_somatic+=1
 # Reapply audited citation links after regenerating the prose projection.
 for link in literature:
  if link['gene_id']==g['id'] and link['part'] in parts:
   sid=next((i for i,src in sources.items() if str(src.get('pmid'))==link['pmid']),None)
   if sid and sid not in parts[link['part']]['source_ids']:parts[link['part']]['source_ids'].append(sid)
 g['report_summary']=parts;g['report_gaps']=gaps
 save(root/'data/genes'/(g['id'].split(':')[1]+'.json'),g)
save(root/'data/gene-index.json',genes)
# Source-specific counts permit representative contexts for the individual
# observed allele, rather than inheriting all cancers from its gene or codon.
code_names={d['id'].replace('hotspots-cohort-',''):name(d['id']) for d in diseases.values() if d['id'].startswith('hotspots-cohort-')}
def observation_context(obs,limit=3):
 counts={}
 for o in obs:
  for code,n in o['tumor_counts'].items():counts[code]=max(counts.get(code,0),n)
 # Distinct source codes can describe overlapping broad/specific contexts.
 families=[['skcm','skin'],['coadread','coad','read','bowel'],['thca','thyroid'],['luad','lusc','lung'],['brca','breast'],['gbm','hgg','lgg','brain'],['blca','bladder'],['paad','pancreas'],['prad','prostate'],['stad','stomach'],['ov','ovary'],['lihc','liver'],['ucec','ucs','uterus']]
 family_by_code={c:i for i,codes in enumerate(families) for c in codes};groups={}
 for code,n in counts.items():
  family=family_by_code.get(code,code);groups.setdefault(family,[]).append((code,n))
 ns=[]
 for family,entries in sorted(groups.items(),key=lambda v:(-max(n for c,n in v[1]),str(v[0]))):
  codes=families[family] if isinstance(family,int) else [family]
  available={c for c,n in entries};code=next((c for c in codes if c in available and code_names.get(c)),None)
  label=code_names.get(code)
  if label and label not in ns:ns.append(label)
  if len(ns)==limit:break
 return ns
for s in sites:
 ns=observation_context(s['observations']);where=' in '+sentence_list(ns) if ns else ' in human cancers'
 event='the '+s['residue']+' region' if s['kind']=='indel_region' else 'a splice-associated site' if 'splice' in s['residue'].lower() else 'residue '+s['residue']
 text=f'Somatic alterations affecting {s["symbol"]} {event} have been observed'+where+'. The functional and clinical significance depend on the specific alteration and tumor type.'
 s['report_comment']=section(text,s['comment']['source_ids'])
for a in alleles:
 ns=observation_context(a['observations']);where=' in '+sentence_list(ns) if ns else ' in human cancers'
 event=f'The {by[a["gene_id"]]["symbol"]} {a["label"]} alteration' if 'splice' not in a['label'].lower() else f'A splice-associated alteration involving {by[a["gene_id"]]["symbol"]}'
 text=event+' has been observed'+where+'. Its functional and clinical significance require allele- and tumor-specific assessment.'
 extra=[]
 if by[a['gene_id']]['symbol']=='BRAF' and a['label']=='V600E':
  text='BRAF V600E is an activating kinase-domain substitution that promotes MAPK signaling. This alteration has been observed'+where+'. Clinical implications depend on the tumor type and treatment setting.';extra=['ncbi-braf','davies-2002']
 if by[a['gene_id']]['symbol']=='IDH1' and a['label']=='R132H':
  text='IDH1 R132H produces neomorphic enzyme activity and accumulation of D-2-hydroxyglutarate. This alteration has been observed'+where+'. Clinical interpretation depends on the tumor type and accompanying histologic and molecular findings.';extra=['dang-2009']
 a['report_comment']=section(text,a['comment']['source_ids']+extra)
for d in disruptions:
 g=by[d['gene_id']];parts=g['report_summary'];som=parts.get('somatic');text=f'Truncating or disruptive {g["symbol"]} alterations may result in loss of gene function. '
 if som:text+=som['text'].replace(' The biological effect varies by alteration, and a tumor-detected TP53 variant alone does not establish a germline diagnosis.','')+' '
 text+='The effect depends on the affected transcript, variant position, and allelic context.'
 # Retain meaningful gene-specific exceptions from the evidence comment.
 old=d['comment']['text'];original_som=g['summary']['somatic']['text'];suffix=old.split(original_som,1)[-1] if original_som in old else ''
 suffix=suffix.split(' Tumor-only testing does not establish germline origin.')[0].strip()
 if suffix:text+=' '+suffix
 d['report_comment']=section(text,d['comment']['source_ids']+([sid for sid in som['source_ids'] if sources[sid].get('pmid')] if som else []))
save(root/'data/hotspots.json',sites);save(root/'data/hotspot-alleles.json',alleles);save(root/'data/disruption-comments.json',disruptions)
# Keep historical pilot evidence files intact while supplying report-language projections.
pilots={
 'braf-v600e-melanoma': 'BRAF p.Val600Glu (V600E) is an activating kinase-domain substitution that promotes MAPK signaling. This alteration occurs in melanoma; its clinical implications depend on the tumor type and treatment setting.',
 'idh1-r132h-glioma': 'IDH1 p.Arg132His (R132H) produces neomorphic enzyme activity and accumulation of D-2-hydroxyglutarate. This alteration is associated with IDH-mutant diffuse gliomas and should be interpreted with the histologic and molecular findings.'}
overlays={}
for file in (root/'data/variants').glob('*.json'):
 v=load(file)
 if file.stem in pilots:overlays[v['id']]=section(pilots[file.stem],v['comment']['source_ids'])
save(root/'data/report-comment-overrides.json',overlays)
m=load(root/'data/manifest.json');m['report_comment_override_file']='report-comment-overrides.json';save(root/'data/manifest.json',m)
save(root/'data/report-style-review.json',dict(genes=len(genes),hotspot_sites=len(sites),alleles=len(alleles),disruption_comments=len(disruptions),germline_gaps=no_germline,somatic_gaps=no_somatic,method='Report-language projections preserve evidence records, exclude panel-selection citations, and omit unresolved disease assertions from copyable paragraphs. Gaps remain visible outside report prose.',status='draft'))
print(f'Prepared report language for {len(genes)} genes, {len(sites)} sites, {len(alleles)} alleles, and {len(disruptions)} disruption comments. Germline gaps: {no_germline}; somatic gaps: {no_somatic}.')

# Enforce the claim-specific citation gate after every regenerated projection.
if (root/'data/citation-audit.json').exists():
 import subprocess
 subprocess.run([sys.executable,str(root/'scripts/audit-report-citations.py')],check=True)

# Restore source-backed functional detail under the soft 80–300-word guidance.
import subprocess
subprocess.run([sys.executable,str(root/'scripts/expand-gene-paragraphs.py')],check=True)
