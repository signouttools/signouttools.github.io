"""Draft conditional loss-of-function comments for a conservative suppressor list.
Source disease contexts remain gene-level; no truncation is automatically pathogenic.
"""
import json
from pathlib import Path
root=Path(__file__).resolve().parents[1]
def load(p):return json.loads(p.read_text())
def save(p,d):p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
genes=load(root/'data/gene-index.json');sources={s['id']:s for s in load(root/'data/sources.json')};diseases={d['id']:d for d in load(root/'data/diseases.json')}
# Excludes neomorphic terminal truncations (e.g. ASXL1, PPM1D), oncogene
# activating deletions, and genes whose suppressor role is context-dependent.
selected=set('AJUBA AMER1 APC ARID1A ARID1B ARID2 ASXL2 ATM ATRX AXIN1 AXIN2 BAP1 BARD1 BCOR BCORL1 BMPR1A BRCA1 BRCA2 BRIP1 CASP8 CBFB CBL CDC73 CDH1 CDK12 CDKN1A CDKN1B CDKN1C CDKN2A CDKN2B CDKN2C CHEK2 CIC CREBBP CUL3 CYLD DDX41 DICER1 DIS3 DNMT3A EED EP300 EZH2 FAS FAT1 FBXW7 FH FLCN GATA2 INPP4B KDM5C KDM6A KEAP1 LATS1 LATS2 LZTR1 MAP2K4 MAP3K1 MAX MEN1 MGA MLH1 MSH2 MSH6 MUTYH NBN NF1 NF2 NOTCH1 NOTCH2 PALB2 PBRM1 PHF6 PMS2 PRDM1 PRKAR1A PTCH1 PTEN PTPN13 PTPRD PTPRT RAD51C RAD51D RB1 RBM10 RNF43 RUNX1 SDHA SDHB SDHC SDHD SETD2 SMAD2 SMAD4 SMARCA4 SMARCB1 SMARCE1 SOCS1 SOX9 SPEN STAG2 STK11 SUFU SUZ12 TET2 TNFAIP3 TP53 TSC1 TSC2 VHL WT1 ZFHX3 ZNF292 ZNRF3'.split())
# These genes require restricted disease/mechanism qualifiers, retained on copy.
special={
 'CBL':'CBL cancer variants can alter E3 ligase regulation; not every truncation reproduces the pathogenic linker/RING-domain mechanism.',
 'DICER1':'DICER1-associated tumors often combine an inactivating allele with a distinct RNase IIIb hotspot allele; a generic truncation does not establish the full tumor genotype.',
 'DNMT3A':'DNMT3A alterations may reflect clonal hematopoiesis. The R882 mechanism and non-R882 loss of function must be distinguished.',
 'EZH2':'Inactivating EZH2 alterations in myeloid neoplasms differ from activating SET-domain hotspot mutations in lymphoma.',
 'GATA2':'Tumor-only detection cannot distinguish an acquired event from an inherited predisposition allele.',
 'NOTCH1':'NOTCH1 is suppressive in some squamous malignancies but activating in T-cell leukemia; the truncation position and disease determine applicability.',
 'NOTCH2':'NOTCH2 terminal truncations can activate signaling in B-cell neoplasms; this generic loss-of-function comment must not be applied to those alleles.',
 'RUNX1':'RUNX1 loss-of-function, dominant-negative alleles, and RUNX1 rearrangements require distinct interpretation.',
 'WT1':'WT1 has context-dependent biology and distinct truncating, zinc-finger, and constitutional mechanisms; do not infer a uniform effect.',
 'MUTYH':'Biallelic loss is generally required for the established repair-deficiency mechanism; a single variant does not establish biallelic inactivation.',
 'TP53':'Loss-of-function truncations differ from dominant-negative or gain-of-function missense alleles; allelic state and clonal hematopoiesis may affect interpretation.'}
records=[]
for g in genes:
 if g['symbol'] not in selected:continue
 sid='ncbi-'+g['ncbi_gene_id']
 if sid not in sources:sources[sid]=dict(id=sid,title=g['symbol']+' — NCBI Gene / RefSeq',publisher='NCBI',url='https://www.ncbi.nlm.nih.gov/gene/'+g['ncbi_gene_id'],kind='gene_reference',accessed_on='2026-11-26',reuse_notes='Source-linked draft; specialist review required.',citation_label='NCBI Gene '+g['ncbi_gene_id'])
 # Preserve the original gene summary's scope and sources; do not turn every
 # statistical cohort into an established loss-of-function disease mechanism.
 som=g['summary']['somatic'];ids=list(dict.fromkeys([sid]+som['source_ids']));dids=[a['disease_id'] for a in g['somatic_associations']]
 text=f'A truncating or disruptive {g["symbol"]} alteration may impair gene function if it affects a clinically relevant transcript and escapes technical or annotation artifacts. Its effect depends on position, splicing, nonsense-mediated decay, retained domains, and allelic state; a truncating annotation alone does not establish pathogenicity or biallelic loss. Gene-level cancer context: '+som['text']
 if g['symbol'] in special:text+=' '+special[g['symbol']]
 text+=' Tumor-only testing does not establish germline origin. Any therapy implication requires the exact biomarker and disease-specific FDA label.'
 records.append(dict(id='disruption-'+g['id'].replace(':','-'),gene_id=g['id'],symbol=g['symbol'],label=g['symbol']+' — conditional disruption / truncating alteration',selector_kind='loss_of_function',disease_ids=dids,comment=dict(text=text,source_ids=ids),applicability_notes=['Use only after gene-, disease-, transcript-, and allele-specific review supports loss of function.','Applies conditionally to nonsense, frameshift, validated splice-disrupting, or gene-disrupting events; does not classify all variants of these classes.','Reported disease contexts are gene-level evidence and may include cohort associations; they are not proof that every truncation drives every listed tumor.'],editorial=dict(status='draft',reviewer=None,sources_checked_on='2026-11-26',disclaimer='Pathologist review needed — LLM-generated summary/review.')))
save(root/'data/disruption-comments.json',records);save(root/'data/sources.json',list(sources.values()));m=load(root/'data/manifest.json');m['disruption_file']='disruption-comments.json';save(root/'data/manifest.json',m)
print('Drafted conditional disruption comments:',len(records));print('Not in dictionary:',sorted(selected-{g['symbol'] for g in genes}))
