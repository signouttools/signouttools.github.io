# Gene inventory review — 2026-11-26

**848 genes are proposed for the writing roster; 285 remain in reserve.** The complete evidence union contains 1,133 HGNC-normalized candidates. The five explicit panel definitions contribute 850 distinct genes. This is an inventory for review, not approved clinical content. No new blurbs were written.

Open `review.html` directly in a browser for a searchable review table; it works without a server. `GENE-LIST.md` contains the complete alphabetical lists. `roster.json` is authoritative and retains each submitted symbol, HGNC mapping method, panel membership, education-reference context/page, and source receipt. Educational mentions are selection leads, not validated somatic associations; they have not been imported into the pilot's tumor filters.

## Selection rule

Propose genes appearing in at least two independent panel families, or having an explicit HGNC-matched mention in the specialty educational references. Group MSK solid and Heme panels as one family for this calculation. Place panel-only genes from one family in reserve. Also reserve a manually identified set of ancillary expression/IHC markers and the SBDS pseudogene confounder, unless a molecular inclusion rationale is confirmed. This yields 519 recurrent-panel genes, 68 single-family genes with educational support, and 261 specialty supplements in the proposed list. The reserve is retained so that the user can broaden the scope without repeating extraction.

## Source versions and observed discrepancies

- MSK IMPACT505: 505 submitted symbols, all normalized.
- MSK HEME468: the downloaded public definition has **467** submitted symbols. This discrepancy is retained; no missing gene was invented.
- DFCI glioma OncoPanel3 (2020 cohort definition): 447 symbols. This is a historical cohort panel, not a claim about the current clinical OncoPanel product.
- FoundationOne: 317 submitted symbols from a **legacy cBioPortal panel definition**. It is not FoundationOne CDx. An exact current CDx list remains an optional source upgrade before freezing the roster.
- Illumina TSO500: 523 normalized genes. Membership includes per-row small-variant, focal-CNV, and RNA-fusion flags. `TERTa` is normalized to TERT because the workbook's footnote marker is flattened into the cell text.
- cBioPortal panel lists are versioned research definitions, not manufacturer assay-validation claims. SHA256 digests identify the downloaded files; they should not be silently replaced by a newer definition.
- Twenty-one AMP oncology cards were retrieved, including Heme Predisposition, AML/MPN, plasma cell, kidney, hereditary/sporadic solid tumors, sarcoma, breast, adult and pediatric CNS, colorectal, melanoma, lung, pediatric solid/soft tissue, ovary and thyroid.
- The supplied tumor-driver atlas was read as structured embedded data. Individual entity names and alteration categories are retained as coverage pointers; its report prose is not redistributed.

## Critical coverage checks and non-gene features

Retain rearrangement partners and noncoding genes when relevant, rather than considering only drug-target genes. Examples to review include KIAA1549, ZFTA (C11orf95), MN1, BEND2, FOXR2, NUTM1, CIC, DUX4, BCOR, SS18, SSX1/2, EWSR1, FUS, DDIT3, CREB3L1/2, YWHAE, NUTM2A/B, NAB2, STAT6, NCOA2, and VGLL2. Histone symbols are normalized to current HGNC names with old names retained, including H3-3A/H3-3B and H3C genes. Hematologic predisposition coverage includes DDX41, GATA2, RUNX1, ETV6, ANKRD26, CEBPA, SAMD9, SAMD9L, and telomere/bone-marrow-failure genes.

The following require a separate biomarker layer in stage two and must not be converted into fictitious gene entries: MSI/MMR phenotype, TMB, HRD/genomic scarring, MGMT promoter methylation, MLH1 promoter methylation, 1p/19q codeletion, chromosome 7 gain/10 loss, MYCN or MDM2 amplification context, DNA methylation class, EBV/HPV status, and immunoglobulin/T-cell receptor clonality. Fusion partners, promoter alterations and exon skipping must keep their alteration class.

## Mapping and extraction limits

Approved symbols take precedence over historical aliases. A unique historical symbol is accepted for explicit panel membership. Educational text uses approved symbols, longer previous symbols, and a limited protein-name alias allowlist; unrestricted HGNC alias matching was deliberately avoided because disease acronyms can be gene aliases. FAP (familial adenomatous polyposis), MPI (breast prognostic index), SDS and HR were excluded as acronym collisions in this corpus.

`unresolved_terms` retains ambiguous terms such as H3, TRK, ER, PR, NRF2 and FIG with candidate mappings and source context. These do not create extra genes automatically. `unmatched-educational-tokens.json` retains the rest of the token audit, including non-gene acronyms and potential OCR/shorthand omissions. Protein families and fused OCR tokens still require manual inspection before claiming exhaustive educational coverage. Negative/pitfall mentions and expression markers may be present: educational support alone is not proof of a driver relationship. Every education-only entry needs inclusion review before prose. This list intentionally separates that decision from clinical interpretation.

No bulk source prose or PDFs are committed. Source links, symbol facts, context labels, hashes and original selection notes are supplied. Access to a source does not confer redistribution rights for its original text. HGNC identity data is CC0.

## Reproduction and review gate

Run `python3 'Knowledge Base/scripts/fetch-roster-sources.py' /private/tmp/kb-roster-new`, then `python3 'Knowledge Base/scripts/compile-roster.py' /private/tmp/kb-roster-new`. The fetcher verifies the frozen SHA256 receipts, resolves the public panel payloads rather than Git LFS pointer files, and extracts AMP text with Poppler `pdftotext -layout`. Source updates require deliberate receipt refresh and count review. The compiler writes the JSON and compact browser data; regenerate the alphabetical list and review counts if selection rules change.

Before approving bulk writing: review the 848 proposed symbols, promote any desired reserve genes, resolve meaningful ambiguous terms, confirm the source-version discrepancies, and obtain an independent specialty coverage review. Existing gene blurbs remain the three draft examples.

## Sources and normalized mention counts

Counts are per source, with overlap; educational counts are mentions mapped to genes, not assay targets.

| Source | Normalized genes | Link |
| --- | ---: | --- |
| tso500 | 523 | [Source](https://www.illumina.com/content/dam/illumina-marketing/documents/products/gene_lists/gene_list_trusight_oncology_500.xlsx) |
| impact505 | 505 | [Source](https://media.githubusercontent.com/media/cBioPortal/datahub/master/reference_data/gene_panels/data_gene_panel_impact505.txt) |
| heme468 | 467 | [Source](https://media.githubusercontent.com/media/cBioPortal/datahub/master/reference_data/gene_panels/data_gene_panel_heme468.txt) |
| glioma_dfci_2020_dfci_oncopanel3 | 447 | [Source](https://media.githubusercontent.com/media/cBioPortal/datahub/master/reference_data/gene_panels/data_gene_panel_glioma_dfci_2020_dfci_oncopanel3.txt) |
| FoundationOne | 317 | [Source](https://media.githubusercontent.com/media/cBioPortal/datahub/master/reference_data/gene_panels/data_gene_panel_FoundationOne.txt) |
| amp-HemePredisposition | 35 | [Source](https://www.amp.org/AMP/assets/File/education/MIMP/HemePredisposition.pdf) |
| amp-Hematopathology | 131 | [Source](https://www.amp.org/AMP/assets/File/education/MIMP/Hematopathology.pdf) |
| amp-AML | 74 | [Source](https://www.amp.org/AMP/assets/File/education/MIMP/AML.pdf) |
| amp-MPN | 31 | [Source](https://www.amp.org/AMP/assets/File/education/MIMP/MPN.pdf) |
| amp-PlasmaCellNeoplasms | 37 | [Source](https://www.amp.org/AMP/assets/File/education/MIMP/PlasmaCellNeoplasms.pdf) |
| amp-AdultTumorsKidney | 63 | [Source](https://www.amp.org/AMP/assets/File/education/MIMP/AdultTumorsKidney.pdf) |
| amp-SolidTumors_Hereditary | 43 | [Source](https://www.amp.org/AMP/assets/File/education/MIMP/SolidTumors_Hereditary.pdf) |
| amp-SolidTumors_Sporadic | 44 | [Source](https://www.amp.org/AMP/assets/File/education/MIMP/SolidTumors_Sporadic.pdf) |
| amp-Bone_Soft_Tissue_1 | 95 | [Source](https://www.amp.org/AMP/assets/File/education/MIMP/Bone_Soft_Tissue_1.pdf) |
| amp-Bone_Soft_Tissue_2 | 76 | [Source](https://www.amp.org/AMP/assets/File/education/MIMP/Bone_Soft_Tissue_2.pdf) |
| amp-BreastCancer | 42 | [Source](https://www.amp.org/AMP/assets/File/education/MIMP/BreastCancer.pdf) |
| amp-CentralNervousSystem | 11 | [Source](https://www.amp.org/AMP/assets/File/education/MIMP/CentralNervousSystem.pdf) |
| amp-Neuropathology | 132 | [Source](https://www.amp.org/AMP/assets/File/education/MIMP/Neuropathology.pdf) |
| amp-Colorectal | 14 | [Source](https://www.amp.org/AMP/assets/File/education/MIMP/Colorectal.pdf) |
| amp-CutaneousMelanomas | 23 | [Source](https://www.amp.org/AMP/assets/File/education/MIMP/CutaneousMelanomas.pdf) |
| amp-LungCancer | 20 | [Source](https://www.amp.org/AMP/assets/File/education/MIMP/LungCancer.pdf) |
| amp-Pediatric_Brain | 41 | [Source](https://www.amp.org/AMP/assets/File/education/MIMP/Pediatric_Brain.pdf) |
| amp-Pediatric_SolidTumors | 48 | [Source](https://www.amp.org/AMP/assets/File/education/MIMP/Pediatric_SolidTumors.pdf) |
| amp-Pediatric_SoftTissue | 74 | [Source](https://www.amp.org/AMP/assets/File/education/MIMP/Pediatric_SoftTissue.pdf) |
| amp-OvarianCancer | 54 | [Source](https://www.amp.org/AMP/assets/File/education/MIMP/OvarianCancer.pdf) |
| amp-Thyroid | 19 | [Source](https://www.amp.org/AMP/assets/File/education/MIMP/Thyroid.pdf) |
| driver-atlas | 455 | [Source](https://mikexiong2.github.io/molecular-tumor-drivers/) |
