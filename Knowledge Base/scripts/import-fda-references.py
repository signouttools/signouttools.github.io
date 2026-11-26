"""Extract FDA molecular-reference candidates, preserving source criteria verbatim.
Usage: bundled-python import-fda-references.py CACHE
This is an evidence index, not an approved-indication eligibility engine.
"""
import json,re,sys,hashlib
from pathlib import Path
from lxml import html
from urllib.parse import urljoin
root=Path(__file__).resolve().parents[1];cache=Path(sys.argv[1]);date='2026-11-26'
def load(p):return json.loads(p.read_text())
def save(p,d):p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
genes=load(root/'data/gene-index.json');by={g['symbol']:g for g in genes};sources={s['id']:s for s in load(root/'data/sources.json')};entries=[];receipts=[]
urls={'fda-cdx.html':'https://www.fda.gov/medical-devices/in-vitro-diagnostics/list-fda-authorized-companion-diagnostic-devices-in-vitro-and-imaging-tools','fda-pgx.html':'https://www.fda.gov/drugs/science-and-research-drugs/table-pharmacogenomic-biomarkers-drug-labeling','fda-notifications.html':'https://www.fda.gov/drugs/cancer-approvals/oncology-cancerhematologic-malignancies-approval-notifications'}
names={'fda-cdx.html':'FDA companion diagnostics','fda-pgx.html':'FDA pharmacogenomic biomarkers in drug labeling','fda-notifications.html':'FDA oncology approval notifications'}
# Only approved gene symbols and explicit, unambiguous clinical synonyms.
synonyms={g['symbol']:g['id'] for g in genes};synonyms.update({old:by[new]['id'] for old,new in {'HER2':'ERBB2','HER-2':'ERBB2','HER-2/neu':'ERBB2','MRE11A':'MRE11','STK19':'WHR1','H3F3A':'H3-3A','H3F3B':'H3-3B','PD-L1':'CD274','PDL1':'CD274','c-KIT':'KIT','BCR-ABL1':'ABL1','BCR::ABL1':'ABL1','BCR-ABL':'ABL1','c-MET':'MET'}.items() if new in by})
pattern=re.compile(r'(?<![A-Za-z0-9])('+ '|'.join(re.escape(s) for s in sorted(synonyms,key=len,reverse=True) if len(s)>=3)+r')(?![A-Za-z0-9])')
lookup={k.upper():v for k,v in synonyms.items()}
def genematches(text):return sorted({lookup[m.group(0).upper()] for m in pattern.finditer(text)})
def txt(node):return ' '.join(node.text_content().split())
def links(node,url):return list({urljoin(url,a.get('href')):dict(title=txt(a),url=urljoin(url,a.get('href'))) for a in node.xpath('.//a[@href]') if urljoin(url,a.get('href')).startswith('https://')}.values())
def source(id,title,url):sources[id]=dict(id=id,title=title,publisher='U.S. Food and Drug Administration',url=url,kind='regulatory_reference',accessed_on=date,reuse_notes='FDA public regulatory reference. Current therapeutic label controls; a gene match alone is not an indication.',citation_label=title)
for file,url in urls.items():
 path=cache/file;receipts.append(dict(url=url,sha256=hashlib.sha256(path.read_bytes()).hexdigest(),accessed_on=date));doc=html.fromstring(path.read_text());sid=file.replace('.html','');source(sid,names[file],url)
 for ti,table in enumerate(doc.xpath('//table')):
  for ri,row in enumerate(table.xpath('.//tr')[1:],start=2):
   cells=row.xpath('./td|./th');values=[txt(c) for c in cells]
   if file=='fda-pgx.html':
    if len(values)!=4 or 'Oncology' not in values[1]:continue
    drug,area,biomarker,sections=values;context='See current therapeutic label';criteria=biomarker+'; labeling sections: '+sections;kind='label_biomarker_index';search=biomarker;therapy=drug
   elif file=='fda-cdx.html':
    kind='companion_diagnostic' if ti==0 else 'companion_diagnostic_group'
    if ti==0:
     assert len(values)==6;diagnostic,context,therapy,biomarker,criteria,approval=values;search=biomarker+' '+criteria
    else:
     assert len(values)==4;diagnostic,context,approval,criteria=values;therapy='FDA group-labeled therapies';biomarker='Group-labeled test';search=criteria
   else:
    if len(values)!=3:continue
    title,criteria,approval=values;context='Exact indication described below';therapy=title;biomarker='See indication';kind='approval_notification';search=title+' '+criteria
   gids=genematches(search)
   if not gids and re.search(r'ESR\s*\(Hormone Receptor\)',search,re.I):gids=[by['ESR1']['id']]
   eid='fda-'+hashlib.sha256((file+'|'+str(ti)+'|'+str(ri)+'|'+str(values)).encode()).hexdigest()[:16]
   evidence_types=[]
   if re.search(r'wild.type|absence of|negative|without.*mutation|not.*mutation',search,re.I):evidence_types.append('negative_or_exclusion_biomarker_possible')
   if re.search(r'protein|expression|overexpress|IHC|ISH|CPS|TPS|Hormone Receptor',search,re.I):evidence_types.append('expression_or_assay_criterion')
   if re.search(r'fusion|rearrangement|translocation|BCR.?ABL',search,re.I):evidence_types.append('rearrangement_criterion')
   if re.search(r'mutation|mutated|SNV|insertion|deletion|alteration|V600|G12|L858|T790|R132|R140|R172|D842',search,re.I):evidence_types.append('sequence_alteration_criterion')
   entries.append(dict(id=eid,kind=kind,gene_ids=gids,therapy=therapy,context=context,biomarker=biomarker,criteria=criteria,evidence_types=evidence_types or ['other_label_context'],source_ids=[sid],links=links(row,url),source_table=ti+1,source_row=ri,review_status='current_label_and_allele_review_needed',eligibility_asserted=False))
 # No reference row is silently dropped because no gene can be identified.
source('fda-drugsatfda','Drugs@FDA — current therapeutic labels','https://www.accessdata.fda.gov/scripts/cder/daf/')
report=dict(checked_on=date,disclaimer='Pathologist review needed — LLM-generated summary/review.',method='Complete row extraction from FDA companion diagnostic tables, all Oncology rows in the pharmacogenomic-labeling table, and all rows in the FDA oncology notification table. Gene matching is a candidate-reference index only.',input_receipts=receipts,reference_count=len(entries),gene_linked_count=sum(bool(e['gene_ids']) for e in entries),genes_with_references=len({g for e in entries for g in e['gene_ids']}),eligibility_asserted=False,coverage_status='source_index_complete_label_adjudication_incomplete',limitations=['FDA notifications are not a complete list of approvals or label updates.','The companion-diagnostic list does not replace a therapeutic label and may retain historic diagnostics.','Pharmacogenomic-labeling biomarkers include resistance, exclusions, metabolism, expression, and study observations; not every entry is a positive treatment-selection biomarker.','Current marketing/withdrawal status, full indication, combinations, line of therapy, age, germline/somatic restrictions, and exact variant eligibility have not been adjudicated for every row.','Drug targets without an explicitly named molecular biomarker may not map to a gene. This is not a claim of exhaustive FDA targeted-therapy coverage.'])
save(root/'data/fda-references.json',entries);save(root/'data/fda-review.json',report);save(root/'data/sources.json',list(sources.values()));manifest=load(root/'data/manifest.json');manifest.update(fda_reference_file='fda-references.json',fda_review_file='fda-review.json');save(root/'data/manifest.json',manifest)
print(json.dumps({k:report[k] for k in ['reference_count','gene_linked_count','genes_with_references','coverage_status']}))
