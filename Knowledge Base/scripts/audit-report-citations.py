"""Fail-closed PMID audit of every copyable report comment.
Explicit reviewed claim scopes and original hotspot row provenance are required.
Unconfirmed references remain archived as candidates, never reported as disproved.
"""
import json,re,hashlib,collections
from pathlib import Path
root=Path(__file__).resolve().parents[1]
def load(p):return json.loads(p.read_text())
def save(p,d):p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
S={s['id']:s for s in load(root/'data/sources.json')};genes=load(root/'data/gene-index.json');G={g['id']:g for g in genes};sites=load(root/'data/hotspots.json');alleles=load(root/'data/hotspot-alleles.json');disruptions=load(root/'data/disruption-comments.json');pilots=load(root/'data/report-comment-overrides.json');D={d['id']:d for d in load(root/'data/diseases.json')}
# Each scope below was checked against the primary abstract, or specified full text.
# A paper is not asserted to support every other statement in the same comment.
scopes={
 ('TP53','germline'):{'1978757':'Germline p53 mutations in dominantly inherited Li-Fraumeni families.','8118819':'Li-Fraumeni germline p53 mutations and breast, sarcoma, brain, and adrenocortical tumor spectrum, including early onset.'},
 ('KRAS','germline'):{'16474404':'Heterozygous germline KRAS mutations in cardiofaciocutaneous syndrome.','16474405':'De novo germline KRAS mutations in Noonan syndrome and an individual with cardiofaciocutaneous syndrome.'},
 ('BRAF','germline'):{'16474404':'Heterozygous germline BRAF mutations in cardiofaciocutaneous syndrome.'},
 ('BRCA1','somatic'):{'24240112':'Somatic BRCA1 loss-of-function mutations in ovarian/fallopian/peritoneal carcinomas; Results, Somatic mutations, and Figure 1C, PMC3944197.','21720365':'Recurrent somatic BRCA1 mutations in high-grade serous ovarian carcinoma.','25719666':'BRCA1 inactivation in whole-genome-sequenced pancreatic ductal adenocarcinoma.'},
 ('BRCA2','somatic'):{'24240112':'Somatic BRCA2 loss-of-function mutations in ovarian carcinomas; Results, Somatic mutations, and Figure 1C, PMC3944197.','21720365':'Recurrent somatic BRCA2 mutations in high-grade serous ovarian carcinoma.'},
 ('BRIP1','somatic'):{'24240112':'Two somatic BRIP1 loss-of-function mutations, including a frameshift in an ovarian clear-cell carcinoma; Somatic mutations and case UW358, PMC3944197.'},
 ('MRE11','somatic'):{'24240112':'One somatic MRE11A loss-of-function event; MRE11A c.1196insTT in ovarian clear-cell case UW358, PMC3944197.'},
 ('RAD51C','somatic'):{'24240112':'One somatic RAD51C loss-of-function mutation; Results, Somatic mutations, Figure 1C, PMC3944197.'},
 ('DDX41','germline'):{'25920683':'Adult familial AML caused by germline DDX41 mutations.'},
 ('DDX41','somatic'):{'25920683':'Somatic DDX41 mutations in sporadic myeloid neoplasms and second DDX41 events in germline carriers.'},
 ('NPM1','germline'):{'31570891':'Germline NPM1 variants in dyskeratosis congenita; does not establish the separate broader syndrome-validity grade.'},
 ('TERC','germline'):{'11574891':'TERC/hTR mutations in autosomal dominant dyskeratosis congenita; not independent proof of every malignancy-risk statement.'},
 ('TERC','somatic'):{'17054308':'FISH-detected TERC copy-number gain during progression of cervical dysplasia to invasive carcinoma.'},
 ('BCL2L1','somatic'):{'20164920':'BCL2L1 focal amplification and dependence of amplified cancer cells on its anti-apoptotic product.'},
 ('MCL1','somatic'):{'20164920':'MCL1 focal amplification across cancer types and amplified-cell survival dependence.'},
 ('BTK','somatic'):{'24869598':'Acquired BTK C481S under ibrutinib treatment in relapsed CLL; not constitutional immunodeficiency evidence.'},
 ('CCND2','somatic'):{'23255553':'CCND2 rearrangements with immunoglobulin partners in cyclin D1-negative mantle-cell lymphoma.'},
 ('CDH11','somatic'):{'15509545':'CDH11 promoter donation in USP6 rearrangements in primary aneurysmal bone cysts.'},
 ('USP6','somatic'):{'15509545':'USP6/CDH11 rearrangements and promoter-driven USP6 expression in primary aneurysmal bone cysts.'},
 ('CDK8','somatic'):{'18794900':'CDK8 copy gain, kinase activity, and beta-catenin-dependent colorectal tumor-cell proliferation.'},
 ('EZHIP','somatic'):{'31086175':'EZHIP overexpression in PFA ependymoma and inhibition of PRC2/H3K27 methylation.'},
 ('H3-3B','somatic'):{'24162739':'H3F3B K36M in chondroblastoma versus H3F3A G34 alterations in giant-cell tumor of bone.'},
 ('IDH1','somatic'):{'19935646':'IDH1 R132H neomorphic production of 2-hydroxyglutarate in glioma; not AML/cholangiocarcinoma occurrence evidence.'},
 ('IGF2','somatic'):{'19957330':'IGF2 loss of imprinting and marked expression elevation in colorectal cancer.'},
 ('MGMT','somatic'):{'15758010':'MGMT promoter methylation/gene silencing in glioblastoma.'},
 ('SF3B1','somatic'):{'21995386':'Somatic SF3B1 mutations in MDS, enriched in ring-sideroblast cases.'},
 ('U2AF1','somatic'):{'22158538':'Recurrent somatic U2AF1 Ser34 mutations in de novo MDS.'},
 ('SRSF2','somatic'):{'22389253':'Somatic SRSF2 mutations in an MDS cohort; does not establish the MDS/MPN part of the broader statement.'},
 ('ZRSR2','somatic'):{'22389253':'Somatic ZRSR2 mutations in MDS; does not experimentally establish the splicing mechanism.'},
}
release_pmid={'v1':'26619011','v2':'29247016','v3':'41895280'};pmid_release={v:k for k,v in release_pmid.items()};dataset=collections.defaultdict(list)
for s in sites:
 for o in s['observations']:dataset[(s['gene_id'],release_pmid[o['release']])].append(dict(site_id=s['id'],workbook=o['workbook'],sheet=o['sheet'],row=o['row'],tumor_codes=list(o['tumor_counts'])))

def key(g,part):return 'gene:'+g['id']+':'+part
# Store the pre-audit inventory once, including automatically linked candidates.
snapshot=root/'curation/pre-citation-audit.json'
if not snapshot.exists():save(snapshot,dict(genes={key(g,p):sec for g in genes for p,sec in g['report_summary'].items()},sites={s['id']:s['report_comment'] for s in sites},alleles={a['id']:a['report_comment'] for a in alleles},disruptions={d['id']:d['report_comment'] for d in disruptions},pilots=pilots))
prior=load(snapshot);decisions=[];bindings={};changed_genes=set();seen_genes=set()
policy_file=root/'curation/citation-audit-policy.json'
frozen=load(policy_file).get('bindings',{}) if policy_file.exists() else {}
# Tighten statements for which the reviewed paper supported only a narrower finding.
tightened={('SRSF2','somatic'):'Somatic SRSF2 mutations occur in myelodysplastic neoplasms.',('ZRSR2','somatic'):'Somatic ZRSR2 mutations occur in myelodysplastic neoplasms.',('TERC','germline'):'Pathogenic constitutional TERC variants cause autosomal dominant dyskeratosis congenita, a telomere biology disorder associated with bone-marrow failure.',('MCL1','somatic'):'Focal MCL1 amplification has been observed across multiple cancer types. Functional studies demonstrate that amplified tumor cells can depend on MCL1 expression for survival.'}
for g in genes:
 for part,sec in g['report_summary'].items():
  if (g['symbol'],part) in tightened:sec['text']=tightened[(g['symbol'],part)]
fulltext_path=root/'curation/fulltext-review-decisions.json'
fulltext_decisions=load(fulltext_path).get('decisions',[]) if fulltext_path.exists() else []
fulltext={(d['record_id'],d['pmid']):d for d in fulltext_decisions if d['decision']=='supports_specific_claim'}

def apply(recordid,sec,gid,part,observations=None,allele=None):
 seen_genes.add(gid)
 # Restore only an exact, reviewed claim; downloaded text alone never qualifies.
 claim_key='gene:'+gid+':'+part
 if recordid.startswith('disruption:'):claim_key='gene:'+gid+':somatic'
 for (rid,pmid),d in fulltext.items():
  if rid!=claim_key:continue
  gene_part=G[gid]['report_summary'].get(part)
  if not gene_part or hashlib.sha256(gene_part['text'].encode()).hexdigest()!=d['report_text_sha256']:continue
  if recordid.startswith('disruption:') and gene_part['text'] not in sec['text']:continue
  sid=next((i for i,src in S.items() if str(src.get('pmid'))==pmid),None)
  if sid and sid not in sec['source_ids']:sec['source_ids'].append(sid)
 original=list(sec['source_ids']);retained=[];good=[]
 for sid in original:
  pmid=str(S[sid].get('pmid') or '')
  if not pmid:retained.append(sid);continue
  scope=scopes.get((G[gid]['symbol'],part),{}).get(pmid)
  proof=None
  if scope:proof=dict(kind='primary_text_review',scope=scope,evidence='Primary PubMed abstract; PMC3944197 full-text Results/Figure 1C for PMID 24240112.')
  elif pmid in pmid_release and part in ['somatic','observation']:
   rs=observations if observations is not None else dataset.get((gid,pmid),[])
   if observations is not None:rs=[o for o in observations if o['release']==pmid_release[pmid]]
   if rs:proof=dict(kind='original_release_data',scope='Observed alteration and source tumor contexts only; no functional/therapeutic effect inferred.',release=pmid_release[pmid],row_count=len(rs))
  if allele and G[gid]['symbol']=='BRAF' and allele=='V600E' and pmid=='12068308':proof=dict(kind='primary_text_review',scope='Kinase-domain activating BRAF mutation and melanoma; paper uses historical V599E nomenclature for current V600E.')
  if allele and G[gid]['symbol']=='IDH1' and allele=='R132H' and pmid=='19935646':proof=dict(kind='primary_text_review',scope='R132H neomorphic reduction of alpha-ketoglutarate to R-2-hydroxyglutarate in malignant glioma.')
  reviewed=fulltext.get((claim_key,pmid))
  if reviewed:
   gene_part=G[gid]['report_summary'].get(part)
   if gene_part and hashlib.sha256(gene_part['text'].encode()).hexdigest()==reviewed['report_text_sha256']:
    proof=dict(kind='primary_fulltext_claim_review',scope=reviewed['support_scope'],location=reviewed['location'],pmcid=reviewed['pmcid'],fulltext_sha256=reviewed['fulltext_sha256'],reviewed_on=reviewed['reviewed_on'])
  if frozen and (recordid not in frozen or frozen[recordid]['text_sha256']!=hashlib.sha256(sec['text'].encode()).hexdigest()):proof=None
  if proof:retained.append(sid);good.append(dict(pmid=pmid,source_id=sid,**proof));status='retained_with_specific_support'
  else:status='removed_unconfirmed_specific_support';proof=dict(scope='Abstract gene mention, assertion bibliography, or cohort membership alone is insufficient. Specific report-claim support was not confirmed; this is not a finding that the article is false or irrelevant to all uses.')
  decisions.append(dict(record_id=recordid,gene_id=gid,symbol=G[gid]['symbol'],part=part,pmid=pmid,source_id=sid,status=status,**proof))
 sec['source_ids']=retained
 if original!=retained:changed_genes.add(gid)
 bindings[recordid]=dict(text_sha256=hashlib.sha256(sec['text'].encode()).hexdigest(),verified_pmids=good)
 return sec
for g in genes:
 for part,sec in list(g['report_summary'].items()):
  apply(key(g,part),sec,g['id'],part)
  if not sec['source_ids']:
   del g['report_summary'][part]
   flag=part+'_association_requires_curation'
   if part in ['somatic','germline'] and flag not in g['report_gaps']:g['report_gaps'].append(flag)
 save(root/'data/genes'/(g['id'].split(':')[1]+'.json'),g)
for s in sites:apply('site:'+s['id'],s['report_comment'],s['gene_id'],'observation',s['observations'])
for a in alleles:apply('allele:'+a['id'],a['report_comment'],a['gene_id'],'observation',a['observations'],a['label'])
for d in disruptions:
 apply('disruption:'+d['id'],d['report_comment'],d['gene_id'],'somatic')
for vid,sec in pilots.items():
 v=next(load(p) for p in (root/'data/variants').glob('*.json') if load(p)['id']==vid)
 apply('pilot:'+vid,sec,v['gene_id'],'observation',[], 'V600E' if 'braf' in vid else 'R132H')
save(root/'data/gene-index.json',genes);save(root/'data/hotspots.json',sites);save(root/'data/hotspot-alleles.json',alleles);save(root/'data/disruption-comments.json',disruptions);save(root/'data/report-comment-overrides.json',pilots)
# Preserve the full decision history rather than losing removed citations on reruns.
history=root/'data/citation-audit.json';old=load(history).get('decisions',[]) if history.exists() else []
all_decisions=list({(d['record_id'],d['source_id']):d for d in old+decisions}.values())
report=dict(audited_on=load(fulltext_path).get('updated_on','2026-11-26') if fulltext_path.exists() else '2026-11-26',policy='Only explicitly reviewed claim scopes or verifiable original hotspot observations retain PMIDs. Unconfirmed links are removed from report prose, retained in the candidate archive, and not labeled disproved.',genes_checked=len(genes),records_checked=len(bindings),decisions=all_decisions,bindings=bindings,counts=dict(collections.Counter(d['status'] for d in all_decisions)),limitations=['This is a conservative citation-retention audit, not a completed full-text review of every candidate article or independent validation of all database-backed biological claims.','Automatically added assertion/cohort PMIDs without confirmed claim support were withdrawn, rather than presented as verified.','A retained publication supports the explicitly recorded subclaim; it is not asserted to prove every other statement in the paragraph.','Original Cancer Hotspots release rows substantiate observation claims only.','All report comments remain LLM-generated drafts requiring pathologist review.'])
save(history,report)
if not policy_file.exists():save(policy_file,dict(reviewed_on='2026-11-26',bindings=bindings,policy='Reviewed exact statement text. A changed or new statement cannot inherit a PMID without renewed review.'))
print(json.dumps({'genes_checked':len(genes),'records_checked':len(bindings),'citation_decisions':report['counts']}))
