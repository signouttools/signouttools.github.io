# Cancer Hotspots import and FDA evidence review

Pathologist review needed — LLM-generated summary/review.

Updated 2026-11-26. The user authorized stage-two drafting while unresolved stage-one evidence remains open. No entry is approved for clinical use.

## Coverage

- **1,305 gene drafts**: original 848 + 285 roster, plus 172 hotspot supplement genes.
- **432 distinct HGNC genes** from 433 submitted symbols across all three original release workbooks. **Zero unrepresented genes.**
- **1,633 residue/indel-region records** and **4,468 source allele annotations**, each with a cited recurrence draft.
- **112 conditional disruption/truncation comments** for genes selected for loss-of-function review. These do not classify every truncation as pathogenic.
- The original two disease-specific pilot comments are preserved byte-for-byte.
- The union is not a count of independently validated drivers; some V1-only observations are historical.

## Release provenance

| Workbook | Sheet | Data rows imported |
| --- | --- | ---: |
| v1 | Per Residue | 470 |
| v1 | Per Allele | 1,168 |
| v2 | SNV-hotspots | 3,004 |
| v2 | INDEL-hotspots | 495 |
| v3 | Hotspot_Residues | 164 |
| v3 | SNV_Variants | 3,532 |
| v3 | INDEL_Variants | 495 |

Source membership is recorded separately from workbook location. V3 has 164 new hotspot residues plus cumulative SNV and indel allele sheets, including rows labeled V2. The V1 and V2 API responses were identical at retrieval, so release membership is derived from the original workbooks. Observations from different sheets and releases overlap and must not be summed.

V1: [PMID 26619011](https://pubmed.ncbi.nlm.nih.gov/26619011/). V2: [PMID 29247016](https://pubmed.ncbi.nlm.nih.gov/29247016/). V3: [PMID 41895280](https://pubmed.ncbi.nlm.nih.gov/41895280/). Original files and SHA-256 receipts are retained under `hotspots/original/` and `data/hotspot-import.json`.

## Interpretation boundaries

Hotspot-site comments describe statistical recurrence. Allele comments document an observed source annotation. Neither assigns pathogenicity, oncogenicity, diagnostic criteria, prognostic significance, or therapy sensitivity. Source transcripts can be unversioned; protein annotations are not converted into validated clinical HGVS. Synonymous and stop annotations are retained for source fidelity. Alternative V1 protein numbering is preserved rather than silently collapsed.

New gene drafts use HGNC identity, NCBI/RefSeq references, reviewed UniProt/GO function, and conservative relationship-specific GenCC selection. Strong/definitive assertions require ClinGen support or agreement of two independent submitters; opposed disease/inheritance relationships are excluded from retained assertions pending review. Original assertions are retained in `data/hotspot-gene-evidence.json`.

Conditional disruption comments require a relevant transcript, credible loss of function, gene/disease mechanism, and allelic-state review. Exceptions are stated for genes such as DICER1, EZH2, NOTCH1/2, RUNX1, DNMT3A, MUTYH, and TP53. Terminal neomorphic truncation mechanisms such as ASXL1 and PPM1D are excluded from this generic set. The set is an editorial selection, not an exhaustive tumor-suppressor catalog.

## FDA evidence: source index complete; label adjudication incomplete

The index contains **788 FDA reference rows**, with gene-level links for **81 genes**: all 235 rows from the specific companion-diagnostic table, 9 group-label rows, 333 Oncology rows from the pharmacogenomic-labeling table, and 211 approval notifications present at retrieval. **48 allele annotations** match exact allele text in FDA criteria/notification descriptions.

The browser displays therapy names, source biomarker criteria, tumor context, FDA source links, and available label/approval-record links. Exact allele text matches are shown alongside the allele and copied with their criteria. This is a reference match, not an eligibility determination. Negative/exclusion contexts are separated from candidate positive criteria. Expression and rearrangement criteria are not treated as point-mutation approval.

- FDA notifications are not a complete list of approvals or label updates.
- The companion-diagnostic list does not replace a therapeutic label and may retain historic diagnostics.
- Pharmacogenomic-labeling biomarkers include resistance, exclusions, metabolism, expression, and study observations; not every entry is a positive treatment-selection biomarker.
- Current marketing/withdrawal status, full indication, combinations, line of therapy, age, germline/somatic restrictions, and exact variant eligibility have not been adjudicated for every row.
- Drug targets without an explicitly named molecular biomarker may not map to a gene. This is not a claim of exhaustive FDA targeted-therapy coverage.

**The request for exhaustive, current FDA targeted-therapy adjudication is not yet complete.** This release provides a broad official-source index and explicit review queue; it must not be described as an exhaustive, label-verified indication database. The next evidence pass must verify current therapeutic labels and withdrawals, resolve row-level biomarker semantics, and link disease/allele-specific approvals without broadening their criteria.

FDA sources: [companion diagnostics](https://www.fda.gov/medical-devices/in-vitro-diagnostics/list-fda-authorized-companion-diagnostic-devices-in-vitro-and-imaging-tools), [labeling biomarkers](https://www.fda.gov/drugs/science-and-research-drugs/table-pharmacogenomic-biomarkers-drug-labeling), [oncology notifications](https://www.fda.gov/drugs/cancer-approvals/oncology-cancerhematologic-malignancies-approval-notifications), and [current labels at Drugs@FDA](https://www.accessdata.fda.gov/scripts/cder/daf/).

## Added gene drafts

| HGNC ID | Approved symbol | Source releases |
| --- | --- | --- |
| HGNC:52 | [ABCC10](?q=ABCC10&gene=HGNC%3A52) | v1 |
| HGNC:23844 | [ABTB3](?q=ABTB3&gene=HGNC%3A23844) | v1 |
| HGNC:90 | [ACADS](?q=ACADS&gene=HGNC%3A90) | v1 |
| HGNC:29609 | [ACP6](?q=ACP6&gene=HGNC%3A29609) | v1 |
| HGNC:24174 | [ACSBG2](?q=ACSBG2&gene=HGNC%3A24174) | v1 |
| HGNC:20822 | [ADGRL4](?q=ADGRL4&gene=HGNC%3A20822) | v1 |
| HGNC:21575 | [AHI1](?q=AHI1&gene=HGNC%3A21575) | v1 |
| HGNC:468 | [AMPD1](?q=AMPD1&gene=HGNC%3A468) | v1 |
| HGNC:25527 | [ANKZF1](?q=ANKZF1&gene=HGNC%3A25527) | v1 |
| HGNC:24087 | [APOBR](?q=APOBR&gene=HGNC%3A24087) | v1 |
| HGNC:25509 | [ARHGAP28](?q=ARHGAP28&gene=HGNC%3A25509) | v1 |
| HGNC:23085 | [ARHGAP33](?q=ARHGAP33&gene=HGNC%3A23085) | v1 |
| HGNC:689 | [ARIH1](?q=ARIH1&gene=HGNC%3A689) | v1 |
| HGNC:27902 | [ARL16](?q=ARL16&gene=HGNC%3A27902) | v1 |
| HGNC:20996 | [ASF1B](?q=ASF1B&gene=HGNC%3A20996) | v1 |
| HGNC:30988 | [BNC2](?q=BNC2&gene=HGNC%3A30988) | v1 |
| HGNC:14310 | [BRD7](?q=BRD7&gene=HGNC%3A14310) | v1 |
| HGNC:2687 | [BRINP1](?q=BRINP1&gene=HGNC%3A2687) | v1 |
| HGNC:33731 | [C3orf70](?q=C3orf70&gene=HGNC%3A33731) | v1 |
| HGNC:1339 | [C6](?q=C6&gene=HGNC%3A1339) | v1 |
| HGNC:19721 | [CANT1](?q=CANT1&gene=HGNC%3A19721) | v1 |
| HGNC:1623 | [CCT8](?q=CCT8&gene=HGNC%3A1623) | v1 |
| HGNC:1850 | [CELSR1](?q=CELSR1&gene=HGNC%3A1850) | v1 |
| HGNC:25815 | [CEP63](?q=CEP63&gene=HGNC%3A25815) | v1 |
| HGNC:25907 | [CEP89](?q=CEP89&gene=HGNC%3A25907) | v1 |
| HGNC:29523 | [CFAP20](?q=CFAP20&gene=HGNC%3A29523) | v1 |
| HGNC:25631 | [CFAP44](?q=CFAP44&gene=HGNC%3A25631) | v1 |
| HGNC:27028 | [CFAP90](?q=CFAP90&gene=HGNC%3A27028) | v1 |
| HGNC:1918 | [CHD3](?q=CHD3&gene=HGNC%3A1918) | v1 |
| HGNC:1936 | [CHIT1](?q=CHIT1&gene=HGNC%3A1936) | v1 |
| HGNC:17423 | [CHST12](?q=CHST12&gene=HGNC%3A17423) | v1 |
| HGNC:16744 | [CIZ1](?q=CIZ1&gene=HGNC%3A16744) | v1 |
| HGNC:19832 | [CLEC14A](?q=CLEC14A&gene=HGNC%3A19832) | v1 |
| HGNC:24462 | [CLECL1](?q=CLECL1&gene=HGNC%3A24462) | v1 |
| HGNC:10445 | [CNOT9](?q=CNOT9&gene=HGNC%3A10445) | v1 |
| HGNC:22199 | [COBL](?q=COBL&gene=HGNC%3A22199) | v1 |
| HGNC:2334 | [CR1](?q=CR1&gene=HGNC%3A2334) | v1 |
| HGNC:2343 | [CRB1](?q=CRB1&gene=HGNC%3A2343) | v1 |
| HGNC:15762 | [CRNKL1](?q=CRNKL1&gene=HGNC%3A15762) | v1 |
| HGNC:2467 | [CSPG5](?q=CSPG5&gene=HGNC%3A2467) | v1 |
| HGNC:2622 | [CYP2C8](?q=CYP2C8&gene=HGNC%3A2622) | v1 |
| HGNC:2642 | [CYP4A11](?q=CYP4A11&gene=HGNC%3A2642) | v1 |
| HGNC:2652 | [CYP7B1](?q=CYP7B1&gene=HGNC%3A2652) | v1 |
| HGNC:24535 | [DCAF13](?q=DCAF13&gene=HGNC%3A24535) | v1 |
| HGNC:17330 | [DDX28](?q=DDX28&gene=HGNC%3A17330) | v1 |
| HGNC:16985 | [DHRS4](?q=DHRS4&gene=HGNC%3A16985) | v1 |
| HGNC:2953 | [DNAH9](?q=DNAH9&gene=HGNC%3A2953) | v1 |
| HGNC:20277 | [DTD2](?q=DTD2&gene=HGNC%3A20277) | v1 |
| HGNC:17909 | [DUSP16](?q=DUSP16&gene=HGNC%3A17909) | v1 |
| HGNC:19090 | [EBF2](?q=EBF2&gene=HGNC%3A19090) | v1 |
| HGNC:24650 | [EHMT1](?q=EHMT1&gene=HGNC%3A24650) | v1 |
| HGNC:3503 | [EVPL](?q=EVPL&gene=HGNC%3A3503) | v1 |
| HGNC:3522 | [EYA4](?q=EYA4&gene=HGNC%3A3522) | v1 |
| HGNC:23527 | [FANK1](?q=FANK1&gene=HGNC%3A23527) | v1 |
| HGNC:24886 | [FRMD4B](?q=FRMD4B&gene=HGNC%3A24886) | v1 |
| HGNC:19839 | [FRMD6](?q=FRMD6&gene=HGNC%3A19839) | v1 |
| HGNC:4039 | [FZD10](?q=FZD10&gene=HGNC%3A4039) | v1 |
| HGNC:23730 | [GPRIN2](?q=GPRIN2&gene=HGNC%3A23730) | v1 |
| HGNC:26307 | [HEXD](?q=HEXD&gene=HGNC%3A26307) | v1 |
| HGNC:5028 | [HNMT](?q=HNMT&gene=HGNC%3A5028) | v1 |
| HGNC:19885 | [HOOK2](?q=HOOK2&gene=HGNC%3A19885) | v1 |
| HGNC:5113 | [HOXB2](?q=HOXB2&gene=HGNC%3A5113) | v1 |
| HGNC:5208 | [HSD11B1](?q=HSD11B1&gene=HGNC%3A5208) | v1 |
| HGNC:6062 | [ING1](?q=ING1&gene=HGNC%3A6062) | v1 |
| HGNC:6069 | [INMT](?q=INMT&gene=HGNC%3A6069) | v1 |
| HGNC:25067 | [INTS12](?q=INTS12&gene=HGNC%3A25067) | v1 |
| HGNC:17933 | [KAT8](?q=KAT8&gene=HGNC%3A17933) | v1 |
| HGNC:6254 | [KCNH5](?q=KCNH5&gene=HGNC%3A6254) | v1 |
| HGNC:6258 | [KCNJ12](?q=KCNJ12&gene=HGNC%3A6258) | v1 |
| HGNC:6269 | [KCNJ8](?q=KCNJ8&gene=HGNC%3A6269) | v1 |
| HGNC:6299 | [KCNQ5](?q=KCNQ5&gene=HGNC%3A6299) | v1 |
| HGNC:25484 | [KIF26B](?q=KIF26B&gene=HGNC%3A25484) | v1 |
| HGNC:6492 | [LAMC1](?q=LAMC1&gene=HGNC%3A6492) | v1 |
| HGNC:29459 | [LCE1A](?q=LCE1A&gene=HGNC%3A29459) | v1 |
| HGNC:29467 | [LCE1F](?q=LCE1F&gene=HGNC%3A29467) | v1 |
| HGNC:15500 | [LENG8](?q=LENG8&gene=HGNC%3A15500) | v1 |
| HGNC:6692 | [LRP1](?q=LRP1&gene=HGNC%3A6692) | v1 |
| HGNC:6697 | [LRP5](?q=LRP5&gene=HGNC%3A6697) | v1 |
| HGNC:26556 | [LRRC71](?q=LRRC71&gene=HGNC%3A26556) | v1 |
| HGNC:24489 | [LSM14A](?q=LSM14A&gene=HGNC%3A24489) | v1 |
| HGNC:13082 | [LTN1](?q=LTN1&gene=HGNC%3A13082) | v1 |
| HGNC:6812 | [MAGEC1](?q=MAGEC1&gene=HGNC%3A6812) | v1 |
| HGNC:6815 | [MAGOH](?q=MAGOH&gene=HGNC%3A6815) | v1 |
| HGNC:6880 | [MAPK7](?q=MAPK7&gene=HGNC%3A6880) | v1 |
| HGNC:26655 | [MARCHF10](?q=MARCHF10&gene=HGNC%3A26655) | v1 |
| HGNC:24628 | [MED28](?q=MED28&gene=HGNC%3A24628) | v1 |
| HGNC:6993 | [MEF2A](?q=MEF2A&gene=HGNC%3A6993) | v1 |
| HGNC:29330 | [METTL14](?q=METTL14&gene=HGNC%3A29330) | v1 |
| HGNC:7090 | [MICA](?q=MICA&gene=HGNC%3A7090) | v1 |
| HGNC:7539 | [MXRA5](?q=MXRA5&gene=HGNC%3A7539) | v1 |
| HGNC:18150 | [MYO18B](?q=MYO18B&gene=HGNC%3A18150) | v1 |
| HGNC:7608 | [MYO9A](?q=MYO9A&gene=HGNC%3A7608) | v1 |
| HGNC:7623 | [MYT1L](?q=MYT1L&gene=HGNC%3A7623) | v1 |
| HGNC:7639 | [NAP1L3](?q=NAP1L3&gene=HGNC%3A7639) | v1 |
| HGNC:6731 | [NCR1](?q=NCR1&gene=HGNC%3A6731) | v1 |
| HGNC:7786 | [NFIC](?q=NFIC&gene=HGNC%3A7786) | v1 |
| HGNC:7820 | [NHS](?q=NHS&gene=HGNC%3A7820) | v1 |
| HGNC:7870 | [NOL4](?q=NOL4&gene=HGNC%3A7870) | v1 |
| HGNC:7894 | [NPAS1](?q=NPAS1&gene=HGNC%3A7894) | v1 |
| HGNC:17820 | [NT5C3A](?q=NT5C3A&gene=HGNC%3A17820) | v1 |
| HGNC:23381 | [OBP2B](?q=OBP2B&gene=HGNC%3A23381) | v1 |
| HGNC:8524 | [OVGP1](?q=OVGP1&gene=HGNC%3A8524) | v1 |
| HGNC:8526 | [OXA1L](?q=OXA1L&gene=HGNC%3A8526) | v1 |
| HGNC:23794 | [PACS2](?q=PACS2&gene=HGNC%3A23794) | v1 |
| HGNC:19365 | [PANK3](?q=PANK3&gene=HGNC%3A19365) | v1 |
| HGNC:20686 | [PASD1](?q=PASD1&gene=HGNC%3A20686) | v1 |
| HGNC:8664 | [PCDHA10](?q=PCDHA10&gene=HGNC%3A8664) | v1 |
| HGNC:28255 | [PCED1B](?q=PCED1B&gene=HGNC%3A28255) | v1 |
| HGNC:30483 | [PCMTD1](?q=PCMTD1&gene=HGNC%3A30483) | v1 |
| HGNC:8747 | [PCSK5](?q=PCSK5&gene=HGNC%3A8747) | v1 |
| HGNC:8806 | [PDHA1](?q=PDHA1&gene=HGNC%3A8806) | v1 |
| HGNC:9056 | [PLCB3](?q=PLCB3&gene=HGNC%3A9056) | v1 |
| HGNC:23492 | [PNLIPRP3](?q=PNLIPRP3&gene=HGNC%3A23492) | v1 |
| HGNC:9171 | [PODXL](?q=PODXL&gene=HGNC%3A9171) | v1 |
| HGNC:19702 | [POM121](?q=POM121&gene=HGNC%3A19702) | v1 |
| HGNC:9452 | [PROCR](?q=PROCR&gene=HGNC%3A9452) | v1 |
| HGNC:15475 | [PRSS27](?q=PRSS27&gene=HGNC%3A15475) | v1 |
| HGNC:9521 | [PSG4](?q=PSG4&gene=HGNC%3A9521) | v1 |
| HGNC:9630 | [PTN](?q=PTN&gene=HGNC%3A9630) | v1 |
| HGNC:29676 | [PUM3](?q=PUM3&gene=HGNC%3A29676) | v1 |
| HGNC:15923 | [RBM39](?q=RBM39&gene=HGNC%3A15923) | v1 |
| HGNC:29289 | [RELCH](?q=RELCH&gene=HGNC%3A29289) | v1 |
| HGNC:17282 | [RIMS1](?q=RIMS1&gene=HGNC%3A17282) | v1 |
| HGNC:17283 | [RIMS2](?q=RIMS2&gene=HGNC%3A17283) | v1 |
| HGNC:21390 | [RIPPLY2](?q=RIPPLY2&gene=HGNC%3A21390) | v1 |
| HGNC:17976 | [RPL10L](?q=RPL10L&gene=HGNC%3A17976) | v1 |
| HGNC:24765 | [RSBN1L](?q=RSBN1L&gene=HGNC%3A24765) | v1 |
| HGNC:19364 | [RTKN2](?q=RTKN2&gene=HGNC%3A19364) | v1 |
| HGNC:10493 | [S100A3](?q=S100A3&gene=HGNC%3A10493) | v1 |
| HGNC:10498 | [S100A8](?q=S100A8&gene=HGNC%3A10498) | v1 |
| HGNC:10730 | [SEMA4B](?q=SEMA4B&gene=HGNC%3A10730) | v1 |
| HGNC:10838 | [SHB](?q=SHB&gene=HGNC%3A10838) | v1 |
| HGNC:24084 | [SHROOM1](?q=SHROOM1&gene=HGNC%3A24084) | v1 |
| HGNC:31037 | [SLC16A13](?q=SLC16A13&gene=HGNC%3A31037) | v1 |
| HGNC:10999 | [SLC27A5](?q=SLC27A5&gene=HGNC%3A10999) | v1 |
| HGNC:16438 | [SLC4A11](?q=SLC4A11&gene=HGNC%3A16438) | v1 |
| HGNC:32934 | [SLCO1B7](?q=SLCO1B7&gene=HGNC%3A32934) | v1 |
| HGNC:24764 | [SMTNL2](?q=SMTNL2&gene=HGNC%3A24764) | v1 |
| HGNC:11160 | [SNRPD3](?q=SNRPD3&gene=HGNC%3A11160) | v1 |
| HGNC:15674 | [SSBP3](?q=SSBP3&gene=HGNC%3A15674) | v1 |
| HGNC:31412 | [SWI5](?q=SWI5&gene=HGNC%3A31412) | v1 |
| HGNC:14962 | [SYT13](?q=SYT13&gene=HGNC%3A14962) | v1 |
| HGNC:11569 | [TARBP2](?q=TARBP2&gene=HGNC%3A11569) | v1 |
| HGNC:11597 | [TBX2](?q=TBX2&gene=HGNC%3A11597) | v1 |
| HGNC:11631 | [TCF20](?q=TCF20&gene=HGNC%3A11631) | v1 |
| HGNC:28399 | [TENT5D](?q=TENT5D&gene=HGNC%3A28399) | v1 |
| HGNC:16836 | [TGFBRAP1](?q=TGFBRAP1&gene=HGNC%3A16836) | v1 |
| HGNC:11784 | [THBD](?q=THBD&gene=HGNC%3A11784) | v1 |
| HGNC:11796 | [THRA](?q=THRA&gene=HGNC%3A11796) | v1 |
| HGNC:29348 | [THSD7B](?q=THSD7B&gene=HGNC%3A29348) | v1 |
| HGNC:30366 | [TMEM131](?q=TMEM131&gene=HGNC%3A30366) | v1 |
| HGNC:30414 | [TMEM147](?q=TMEM147&gene=HGNC%3A30414) | v1 |
| HGNC:37208 | [TMEM200C](?q=TMEM200C&gene=HGNC%3A37208) | v1 |
| HGNC:11990 | [TOP2B](?q=TOP2B&gene=HGNC%3A11990) | v1 |
| HGNC:14118 | [TPSD1](?q=TPSD1&gene=HGNC%3A14118) | v1 |
| HGNC:17299 | [TPTE2](?q=TPTE2&gene=HGNC%3A17299) | v1 |
| HGNC:27316 | [TRIM65](?q=TRIM65&gene=HGNC%3A27316) | v1 |
| HGNC:12327 | [TROAP](?q=TROAP&gene=HGNC%3A12327) | v1 |
| HGNC:16060 | [TRUB1](?q=TRUB1&gene=HGNC%3A16060) | v1 |
| HGNC:29095 | [TSC22D2](?q=TSC22D2&gene=HGNC%3A29095) | v1 |
| HGNC:16691 | [TUBGCP4](?q=TUBGCP4&gene=HGNC%3A16691) | v1 |
| HGNC:18127 | [TUBGCP6](?q=TUBGCP6&gene=HGNC%3A18127) | v1 |
| HGNC:12476 | [UBE2D3](?q=UBE2D3&gene=HGNC%3A12476) | v1 |
| HGNC:30600 | [UBXN11](?q=UBXN11&gene=HGNC%3A30600) | v1 |
| HGNC:12513 | [UCHL1](?q=UCHL1&gene=HGNC%3A12513) | v1 |
| HGNC:25754 | [VPS37B](?q=VPS37B&gene=HGNC%3A25754) | v1 |
| HGNC:25928 | [WDR73](?q=WDR73&gene=HGNC%3A25928) | v1 |
| HGNC:19733 | [XPO6](?q=XPO6&gene=HGNC%3A19733) | v1 |
| HGNC:15935 | [ZHX3](?q=ZHX3&gene=HGNC%3A15935) | v1 |
| HGNC:28990 | [ZNF516](?q=ZNF516&gene=HGNC%3A28990) | v1 |
| HGNC:29084 | [ZNF623](?q=ZNF623&gene=HGNC%3A29084) | v1 |
| HGNC:25741 | [ZNF649](?q=ZNF649&gene=HGNC%3A25741) | v1 |

## Conditional disruption genes

AMER1, APC, ARID1A, ARID1B, ARID2, ASXL2, ATM, ATRX, AXIN1, AXIN2, BAP1, BARD1, BCOR, BCORL1, BMPR1A, BRCA1, BRCA2, BRIP1, CASP8, CBFB, CBL, CDC73, CDH1, CDK12, CDKN1A, CDKN1B, CDKN1C, CDKN2A, CDKN2B, CDKN2C, CHEK2, CIC, CREBBP, CUL3, CYLD, DDX41, DICER1, DIS3, DNMT3A, EED, EP300, EZH2, FAS, FAT1, FBXW7, FH, FLCN, GATA2, INPP4B, KDM5C, KDM6A, KEAP1, LATS1, LATS2, LZTR1, MAP2K4, MAP3K1, MAX, MEN1, MGA, MLH1, MSH2, MSH6, MUTYH, NBN, NF1, NF2, NOTCH1, NOTCH2, PALB2, PBRM1, PHF6, PMS2, PRDM1, PRKAR1A, PTCH1, PTEN, PTPRD, PTPRT, RAD51C, RAD51D, RB1, RBM10, RNF43, RUNX1, SDHA, SDHB, SDHC, SDHD, SETD2, SMAD2, SMAD4, SMARCA4, SMARCB1, SMARCE1, SOCS1, SOX9, SPEN, STAG2, STK11, SUFU, SUZ12, TET2, TNFAIP3, TP53, TSC1, TSC2, VHL, WT1, ZFHX3, ZNF292, ZNRF3.

## Files and reproducibility

- `data/hotspots.json`: source-preserving site records, original row provenance, statistical fields and contexts, cited drafts.
- `data/hotspot-alleles.json`: all observed allele annotations and cited recurrence drafts.
- `data/hotspot-import.json`: coverage, aliases, original-file receipts, and added genes.
- `data/hotspot-index.json` / `data/hotspot-genes/`: generated compact search index and per-gene browser shards.
- `data/disruption-comments.json`: conditional loss-of-function comments.
- `data/fda-references.json` / `data/fda-review.json`: complete source-row index and unresolved label-review status.

```sh
python3 "Knowledge Base/scripts/fetch-hotspot-sources.py" /path/to/hotspot-cache
# Read-only spreadsheet import requires xlrd and openpyxl; FDA parsing requires lxml.
python3 "Knowledge Base/scripts/import-hotspots.py" /path/to/hotspot-cache /path/to/draft-cache /path/to/hgnc-cache
python3 "Knowledge Base/scripts/import-fda-references.py" /path/to/hotspot-cache
python3 "Knowledge Base/scripts/draft-disruptions.py"
python3 "Knowledge Base/scripts/link-hotspot-fda.py"
python3 "Knowledge Base/scripts/build-hotspot-browser.py"
python3 "Knowledge Base/scripts/write-hotspot-review.py"
node "Knowledge Base/scripts/validate.mjs"
python3 "Knowledge Base/scripts/validate-curation.py"
python3 "Knowledge Base/scripts/validate-hotspots.py" /path/to/hotspot-cache
```

Initial new-gene drafting additionally requires NCBI Gene ESummary JSON batches named `ncbi-extra-*.json` in the hotspot cache, the HGNC complete TSV, and the existing GenCC/UniProt source snapshots. Source-specific artifacts are not substitutes for clinical review.

Cancer Hotspots-derived database portions are made available under [ODbL 1.0](hotspots/LICENSE-ODbL-1.0.txt), with [attribution](hotspots/ATTRIBUTION.md). Other source licenses continue to apply to their respective material.
