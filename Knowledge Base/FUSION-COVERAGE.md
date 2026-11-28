# Fusion coverage and source intake

2026-11-27 · Pathologist review needed — LLM-generated summary/review.

The searchable library contains **382 drafts: 186 interpretive entries and 196 new cohort observations**. The expansion adds reported directed fusion transcripts, preserving the original interpretive entries and audit follow-ups. It does not claim exhaustive coverage of all published fusions or clinical validation of every detected transcript.

[Browse fusions](index.html?mode=fusions) · [Draft library](FUSION-DRAFTS.md) · [Original evidence audit](FUSION-REVIEW.md) · [Resource-by-resource intake](curation/fusions/resource-review.json)

## What was added

| Measure | Result |
| --- | ---: |
| User-supplied links assessed for source role/access | 19 |
| Distinct resources after resolving the duplicated Nature/PMC study | 18 |
| Final pediatric cohort pairs extracted | 272 |
| Extracted pairs already in the original interpretive corpus | 76 |
| New searchable cohort-observation drafts | 196 |
| Additional partner identities from the frozen HGNC snapshot | 161 |
| RNA/WGS directed pairs retained for further review | 178 |

The main expansion uses Liu et al., *Nature Communications* 14, 1739 (2023), [doi:10.1038/s41467-023-37438-4](https://doi.org/10.1038/s41467-023-37438-4), [PMC10076316](https://pmc.ncbi.nlm.nih.gov/articles/PMC10076316/). The Nature and PMC links supplied in the request refer to the same study. The final cohort sheet, Supplementary Data 1 in `41467_2023_37438_MOESM4_ESM.xlsx`, reconciles to the paper's 272 directed fusion pairs and 2,005 fusion-positive patients among 5,190 patients.

New examples include KMT2A::ABI1, KMT2A::AFF3, KMT2A::MLLT11, NUP98::PHF23, PAX5::AUTS2, PAX5::FOXP1, AFAP1::NTRK2, MYO5A::NTRK3, AGK::BRAF, AKAP9::BRAF, RNF130::BRAF, BCAS1::RAF1, ATF7IP::JAK2, BICD2::JAK2, ZFTA::MAML2 and EWSR1::CREM.

Each new paragraph states only the directed fusion and specimen diagnoses reported in the table. It carries the source worksheet, exact row numbers, workbook SHA-256 and exact-text audit hash. The browser labels these entries **Cohort observation · Draft**, uses **Fusion observation** as the paragraph heading, and includes the observation limitation in copied text. Source occurrence is not promoted to a transforming mechanism, diagnostic assignment, prognostic conclusion or treatment indication.

Historical symbols remain searchable: C11orf95 maps to ZFTA, FAM118B to SIRAL1, FAM169B to FAM169BP, and MLL aliases remain available for new KMT2A pairs. HGNC currently annotates FAM169BP as a pseudogene; the entry does not describe it as a protein. New partner descriptions use approved HGNC names and locus types only. Existing audited descriptions retain their existing sources.

Pediatric, unspecified and historical diagnosis qualifiers are retained. A brain-cohort recruitment label does not make a sarcoma or neurofibroma a glioma. Generic solid-tumor observations do not acquire an invented organ diagnosis. Rare orientations follow the study's Supplementary Data 32; detecting ALK::BIRC6 does not establish the biological properties of BIRC6::ALK. Primary references listed in Supplementary Data 25 are preserved as follow-up candidates, without being represented as independently reviewed citations.

## Research observations and remaining gaps

Van Belzen et al., *BMC Cancer* 23, 618 (2023), [doi:10.1186/s12885-023-11054-3](https://doi.org/10.1186/s12885-023-11054-3), [PMC10318758](https://pmc.ncbi.nlm.nih.gov/articles/PMC10318758/), contributes a separate research inventory: the 222 rows of Additional file 4, Table S1 contain 178 distinct directed pair names. Original diagnoses, high-confidence flags, author clinical flags and row locations are retained. This table includes incidental and reciprocal events, so no new report paragraph is generated from it in this pass. A reported high-confidence structural variant and an author clinical flag are not equivalent to clinical validation of a particular transcript.

The inventories are in [expansion-observations.json](curation/fusions/expansion-observations.json). They contain published fusion names and source locations, with patient/sample identifiers omitted. Multiple samples can come from one patient. The two cohorts can overlap; their counts are not pooled or treated as independent replication. The study's unconfirmed Tier2 candidates, raw prediction sheets and promoter-hijacking candidates are excluded from the runtime additions.

The remaining supplied resources were triaged for their role and access, rather than treated as interchangeable lists of confirmed drivers:

- **TumorFusions / the Cell Reports pan-cancer study:** the article body was retrieved, but the attempted supplementary endpoints returned an error payload or 404. Obtaining the exact driver and event tables remains a priority for adult solid-tumor expansion.
- **Mitelman, ChimerDB, Quiver and FusionHub:** useful discovery resources; no complete release was downloaded and licensed for redistribution in this pass. TumorFusions and FusionHub website access failed.
- **FusionGDB 2.0 / 3.0:** resource descriptions were accessible. FusionGDB 2.0's data-availability statement restricts annotations to academic use; those annotations were not bulk-imported. No complete FusionGDB 3.0 release or redistribution terms were adjudicated.
- **FusionPub:** a route to original therapeutic studies. Abstract drug co-mentions and AI-generated summaries do not clear predictive report claims.
- **Oncofuse / Pegasus:** prediction methods for prioritizing candidates. A computational score does not establish driver status.
- **The supplied reviews:** article bodies or publisher pages were available for discovery. No fusion-specific clinical assertion was automatically imported from a review.

The [resource intake ledger](curation/fusions/resource-review.json) accounts for all 19 supplied URLs, records access/reuse limits, and distinguishes article retrieval from claim adjudication. Full database-release coverage and broad adult solid-tumor supplementation remain incomplete.

## Attribution and reproducibility

The two extracted study supplements are under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Attribution: Liu et al. (2023) and van Belzen et al. (2023), linked above. Changes: fusion names, source locations and diagnostic labels were extracted; names were normalized against the existing frozen HGNC snapshot; patient/sample identifiers were omitted; new occurrence prose was written. No proprietary database summaries were copied.

The checked-in [cohort expansion fragment](curation/fusions/expansion-cohort.json) is consumed by the existing audit pipeline without changing the frozen original corpus. Rebuild the runtime data with:

```sh
python3 "Knowledge Base/scripts/apply-fusion-audit.py"
python3 "Knowledge Base/scripts/draft-fusions.py"
python3 "Knowledge Base/scripts/validate-fusions.py"
node "Knowledge Base/scripts/test-fusion-browser.mjs"
node "Knowledge Base/scripts/validate.mjs"
```

To reproduce the source extraction, obtain the original Liu MOESM4 workbook, van Belzen MOESM4 CSV and the frozen HGNC TSV, then run `scripts/import-fusion-observations.py` with `--pediatric-xlsx`, `--wgs-csv` and `--hgnc-tsv`. Use the bundled Python environment with read-only `openpyxl`. Input checksums, table locations, source URLs, licenses, alias decisions and literature follow-up candidates are retained in the curation JSON. Ordinary rebuilds do not require network access or the original workbooks.

Validation covers exact-hash claims, source rows, corpus/index/export agreement, stable partner identities, disease-filter isolation, historical aliases, reversed-partner searches and exclusion of research-only observations from report generation. Local browser verification confirmed the 382-entry count, MLL/ABI1 search, observation labeling, copy confirmation and evidence-row display, with no recorded browser errors. All entries remain drafts pending specialist review. No Git push or hosted deployment was performed.
