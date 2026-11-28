# Gene paragraph expansion review

Reviewed 1,305 gene paragraphs against the soft 80–300-word target. Expanded 22 in this pass. After expansion, 54 are within the target and 1,251 remain shorter.

Forty-six gene-specific normal-function syntheses use the existing cached NCBI/RefSeq summaries. Other expansions restore specific molecular-activity annotations previously omitted from the report projection. Generic binding-only annotations are omitted. Disease associations and their primary-literature citation bindings are preserved.

Shorter paragraphs remain permissible. Many entries have unresolved germline or somatic evidence gaps, or lack enough explanatory functional evidence to justify a longer synthesis. These entries need further source review before substantive disease or mechanism claims can be added. The machine-readable review records a decision, word counts, and existing evidence gaps for every gene. This pass does not constitute a new full-text review of 1,305 genes.

Regenerate with `python3 "Knowledge Base/scripts/expand-gene-paragraphs.py"` after preparing report projections, then refresh the draft export with `write-hotspot-review.py`. Changes with retained PMID citations require separate claim-specific review.

| Gene | Before | After | Decision |
| --- | ---: | ---: | --- |
| ALK | 46 | 90 | Expanded normal-function synthesis from the cited NCBI/RefSeq summary. |
| ATM | 51 | 91 | Expanded normal-function synthesis from the cited NCBI/RefSeq summary. |
| ATR | 44 | 83 | Expanded normal-function synthesis from the cited NCBI/RefSeq summary. |
| CDH1 | 72 | 100 | Expanded normal-function synthesis from the cited NCBI/RefSeq summary. |
| CDKN2A | 41 | 87 | Expanded normal-function synthesis from the cited NCBI/RefSeq summary. |
| CHEK2 | 44 | 85 | Expanded normal-function synthesis from the cited NCBI/RefSeq summary. |
| DICER1 | 55 | 86 | Expanded normal-function synthesis from the cited NCBI/RefSeq summary. |
| ERBB2 | 35 | 77 | Expanded normal-function synthesis from the cited NCBI/RefSeq summary. |
| KIT | 49 | 90 | Expanded normal-function synthesis from the cited NCBI/RefSeq summary. |
| MEN1 | 59 | 89 | Expanded normal-function synthesis from the cited NCBI/RefSeq summary. |
| MET | 49 | 99 | Expanded normal-function synthesis from the cited NCBI/RefSeq summary. |
| MLH1 | 57 | 97 | Expanded normal-function synthesis from the cited NCBI/RefSeq summary. |
| MSH6 | 48 | 92 | Expanded normal-function synthesis from the cited NCBI/RefSeq summary. |
| PALB2 | 49 | 93 | Expanded normal-function synthesis from the cited NCBI/RefSeq summary. |
| PMS2 | 43 | 86 | Expanded normal-function synthesis from the cited NCBI/RefSeq summary. |
| RAD51C | 58 | 91 | Expanded normal-function synthesis from the cited NCBI/RefSeq summary. |
| RAD51D | 53 | 80 | Expanded normal-function synthesis from the cited NCBI/RefSeq summary. |
| RET | 52 | 95 | Expanded normal-function synthesis from the cited NCBI/RefSeq summary. |
| SMAD4 | 51 | 88 | Expanded normal-function synthesis from the cited NCBI/RefSeq summary. |
| SMARCA4 | 57 | 95 | Expanded normal-function synthesis from the cited NCBI/RefSeq summary. |
| SMARCB1 | 53 | 96 | Expanded normal-function synthesis from the cited NCBI/RefSeq summary. |
| STK11 | 59 | 89 | Expanded normal-function synthesis from the cited NCBI/RefSeq summary. |
