"""Link exact source allele text to FDA references without asserting eligibility."""
import json,re
from pathlib import Path
root=Path(__file__).resolve().parents[1]
def load(p):return json.loads(p.read_text())
def save(p,d):p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
refs=load(root/'data/fda-references.json');alleles=load(root/'data/hotspot-alleles.json');sites=load(root/'data/hotspots.json');matched=0
for a in alleles:
 named=[];exclusions=[]
 for r in refs:
  if a['gene_id'] not in r['gene_ids'] or r['kind'] not in ['companion_diagnostic','companion_diagnostic_group','approval_notification']:continue
  # Do not treat a codon, a generic mutation category, or a protein target as
  # an exact match to all observed substitutions. Source notation is retained.
  if not re.search(r'(?<![A-Za-z0-9])'+re.escape(a['label'])+r'(?![A-Za-z0-9])',r['criteria']):continue
  if 'negative_or_exclusion_biomarker_possible' in r['evidence_types']:exclusions.append(r['id'])
  else:named.append(r['id'])
 a['fda_reference_ids']=named;a['fda_exclusion_reference_ids']=exclusions
 if named or exclusions:matched+=1
for s in sites:
 own=[a for a in alleles if a['site_id']==s['id']];s['fda_reference_ids']=sorted({i for a in own for i in a['fda_reference_ids']});s['fda_exclusion_reference_ids']=sorted({i for a in own for i in a['fda_exclusion_reference_ids']});s['fda_allele_labels']={rid:sorted({a['label'] for a in own if rid in a['fda_reference_ids']+a['fda_exclusion_reference_ids']}) for rid in s['fda_reference_ids']+s['fda_exclusion_reference_ids']}
save(root/'data/hotspot-alleles.json',alleles);save(root/'data/hotspots.json',sites)
r=load(root/'data/fda-review.json');r['exact_source_allele_text_matches']=matched;r['exact_match_method']='Exact allele text in FDA CDx criteria or approval description; does not resolve functional eligibility, current label, tumor, age, line, combinations, or approval status.';save(root/'data/fda-review.json',r)
print('Allele annotations with exact FDA-source text matches:',matched)
