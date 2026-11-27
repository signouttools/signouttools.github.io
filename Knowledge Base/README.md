# Knowledge Base — plan and draft implementation

Hotspot library v0.4 · 2026-11-26 · Pathologist review needed — LLM-generated summary/review.

## Purpose and current boundary

Build a searchable molecular pathology reference that helps a sign-out professional draft a report. Stage one is a dictionary of approximately 500–1,000 cancer-panel genes, each with one concise paragraph covering normal function, germline disease associations, and somatic cancer associations. Stage two adds alteration-specific comments in explicitly defined disease contexts.

The dictionary has **1,305 source-linked gene drafts**: the original 848 proposed + 285 reserve genes, plus **172 additional genes** from the Cancer Hotspots workbooks. All **432 distinct hotspot genes** are represented. The three releases yield **1,633 site drafts and 4,468 observed-allele drafts**, with **112 conditional disruption comments**. The original two disease-specific pilot files remain unchanged. See [HOTSPOT-REVIEW.md](HOTSPOT-REVIEW.md) for provenance, added genes, licensing, and the incomplete FDA label-adjudication queue. See [EVIDENCE-REVIEW.md](EVIDENCE-REVIEW.md) for the original 528 unresolved somatic-association gaps. All entries remain unreviewed drafts.

The user authorized stage-two drafting and US FDA evidence indexing on 2026-11-26 while stage-one review remains open. This supersedes the original proposed sequencing below. The FDA index contains 788 official-source reference rows; it is **not yet an exhaustive, current-label-verified targeted-therapy database**.

Open `index.html` through an HTTP server. From the repository root:

```sh
python3 -m http.server 8765 --bind 127.0.0.1
```

Then visit <http://127.0.0.1:8765/Knowledge%20Base/>. This is a static GitHub Pages-compatible prototype. It reads bundled JSON; it has no database service, analytics, patient entry, or external runtime lookup. Source links open only when selected. Direct `file://` opening is unsupported because browsers restrict local JSON fetching.

## Report-language standard

Copyable comments use concise, self-contained, third-person language suitable for a molecular report. Gene paragraphs describe normal function and supported germline, mosaic, and somatic disease associations. Hotspot comments describe the observed alteration, established biological effect where supported, and relevant cancer contexts. Disruption comments describe the conditional loss-of-function mechanism and gene-specific exceptions. Citations accompany biological claims. Omit generic interpretation reminders (for example, that clinical significance depends on context, effects vary by allele, or tumor-only findings do not establish germline origin). Retain concrete gene-specific mechanisms and disease associations.

Panel membership, selection rationale, dataset versions, extraction methods, source-assertion grading, and curation notes remain outside report paragraphs. Selection provenance is available in the interface’s About section and the original inventory. Unresolved associations are omitted from the report projection and flagged separately; missing evidence is not converted into a negative clinical claim. All report comments retain draft status and the pathologist-review disclaimer.

`report_summary` in each gene and `report_comment` in hotspot/disruption records provide the report-language projections. The underlying evidence summaries and assertions remain available for audit. The two original pilot files use report projections in `data/report-comment-overrides.json`. After regenerating evidence, run `prepare-report-comments.py` before building browser shards and the draft export.

## Stage one: selecting the gene inventory

**Recommendation:** target 600–800 genes for the first release, allowing 500–1,000 after the source union and gap review. This is a planning range, not a measured union. Avoid adding weakly relevant genes solely to reach a number.

1. Obtain dated, version-specific *complete gene lists* from at least three independent broad oncology assays. Proposed anchors are MSK-IMPACT (the institutional page currently describes 505 genes), Illumina TruSight Oncology 500 (523 DNA genes), and FoundationOne CDx (324 genes). A marketing gene count alone cannot establish membership.
2. Add a hematologic source such as MSK-IMPACT Heme, and institution/provider lists covering myeloid, lymphoid, CNS, pediatric, and sarcoma testing. The current MSK clinical overview describes a 468-gene Heme assay; an older 400-gene list must remain a distinct panel version. Record the exact list actually acquired.
3. Normalize all symbols to HGNC IDs, retain submitted and historical symbols, resolve withdrawn/ambiguous symbols manually, and deduplicate by HGNC ID. Histone renaming and aliases such as MLL/KMT2A require special attention. CDKN2A transcript products remain one gene, with transcript-specific discussion when needed.
4. Classify selection as **recurrent panel member** (at least two independently sourced assay families), **specialty supplement** (a documented heme/CNS/pediatric/sarcoma gap), or **manual addition** (explicit rationale and evidence). Versions of one assay family do not count as independent panels. Inclusion priority is an editorial property, not a clinical evidence tier.
5. Audit coverage across solid tumors, myeloid and lymphoid neoplasms, CNS tumors, pediatric tumors, and mesenchymal tumors. Include genes chiefly relevant to fusions, copy-number changes, or promoter alterations; don't limit the dictionary to SNVs. Do not treat panel inclusion as proof of a cancer association or drug response.
6. Deliver the candidate roster **before bulk prose**: HGNC ID, approved symbol, aliases, panel memberships/versions, assay family, tested alteration classes, selection reason, priority, and coverage flags. Report raw and normalized counts, overlaps, exclusions, unresolved mappings, and source-license restrictions. Freeze a versioned roster for approval.

The five acquired panel definitions and versioned memberships are recorded in `data/panels.json` and each gene record. The original inventory review remains a historical selection artifact; the live gene dictionary also includes the hotspot supplement.

## Information architecture

| Object | Authoritative file | Main responsibility |
| --- | --- | --- |
| Gene | `data/genes/<HGNC-number>.json` | Stable identity; function, germline and somatic statements; typed disease links; panel provenance; editorial state |
| Variant comment | `data/variants/<stable-id>.json` | One alteration selector plus one disease context and a scoped, cited comment |
| Disease | `data/diseases.json` | Stable local ID, preferred name, synonyms, parent, broad category, optional validated ontology mappings |
| Source | `data/sources.json` | Title, publisher, URL, source type, access date, optional version/PMID, reuse notes |
| Panel | `data/panels.json` | Provider, family, version, exact-list URL and acquisition state |
| Release | `data/manifest.json` | Schema/data version, release state, record file paths and build date |
| Contract | `schemas/knowledge-base.schema.json` | JSON Schema 2020-12 with entity definitions |

Keep one gene per file so edits and review diffs remain manageable. Store paragraph components separately (`function`, `germline`, `somatic`) and join them in that order for the short report paragraph. Do not maintain a second manually edited copy of the same paragraph. Each component carries source IDs. Disease links also carry sources, association type, and mechanism; the browser's tumor filters use **somatic links only**.

Use stable HGNC-based IDs even when symbols change. Clinical variants use a versioned RefSeq transcript, HGVS c. and p. description, and familiar aliases. The pilot's transcripts are examples, not a blanket commitment to a canonical transcript policy. In stage two, add assembly and normalized genomic coordinates when available, preserve the original submitted representation, and document the validation tool/version.

## Disease navigation and search

The UI supports keyword search, an A–Z selector, broad tumor category, and tumor type. Search spans symbols, names, aliases, paragraphs, pathway terms, linked disease names/synonyms, and hotspot aliases. Multiple words must all match; gene-symbol matches sort first. Filters combine with AND. A broad disease selection includes descendants; a specific tumor selection does not automatically include generic pan-cancer associations. Show a clear empty state with reset controls.

Use a local disease hierarchy now; adopt a pinned OncoTree release and NCIt mappings after scope approval. The pilot explicitly contains **unmapped local disease IDs**, not invented OncoTree codes. Maintain preferred names, synonyms (e.g. AML), parent-child relationships, taxonomy release, and mapping review status. Distinguish an organ (brain), a family (diffuse glioma), and an integrated diagnosis. Preserve age or lineage qualifiers when they change interpretation. Allow multiple parents in a future ontology migration if required; the initial local hierarchy has a single parent.

Broad pan-cancer genes remain discoverable through their actual curated disease links and a separate pan-cancer category. Do not propagate germline syndrome-associated cancers into somatic search results. Stage two must filter individual comments by disease applicability independently of gene-level associations; a BRAF melanoma comment must not be presented as a colorectal comment.

## Editorial guidelines

### Gene paragraph

Aim for **80–140 words**, usually three to five sentences; allow up to 180 for complex genes with an explicit editorial reason. Follow this fixed order:

1. **Normal function:** state the encoded protein or RNA, its principal biological role, and the relevant pathway in plain language. Use NCBI Gene/RefSeq as the default functional source; verify specialized mechanisms against primary literature or an authoritative protein resource.
2. **Germline disease:** describe established pathogenic/likely pathogenic variant associations, including non-neoplastic syndromes when relevant. State inheritance and allele/mechanism restrictions where supported. A susceptibility association, Mendelian syndrome, and postzygotic mosaic disorder are different assertions. Put mosaic disease in a separate structured field, and explicitly identify it in the prose if mentioned. For a gene with no established inherited association found in the reviewed sources, use a qualified statement and record the search scope/date; absence of a curated association is not proof that none exists.
3. **Somatic cancer:** state the principal alteration mechanism and a few representative tumor associations. For broadly altered genes, say they are altered across many cancer types. Use “mutated” for sequence mutations and “altered” when also discussing copy number, rearrangements, or expression. Avoid exhaustive tumor lists, unsourced frequencies, and implications that every variant is pathogenic.

Write original synthesis, with citations attached to the claims they support. Avoid copying database paragraphs. Do not conflate detection with causality, prognostic value, diagnostic specificity, or treatment benefit. Avoid drug or prognosis statements in the stage-one paragraph unless separately reviewed and explicitly in scope. Do not infer inherited status from a tumor result or VAF alone.

### Source hierarchy and reuse

- **Identity:** HGNC; retain the source release/date and identifiers. HGNC data is CC0.
- **Function:** NCBI Gene/RefSeq first; UniProt or primary mechanistic studies when additional detail is needed.
- **Germline:** GeneReviews and ClinGen expert curation, then relevant primary studies; ClinVar assertions require review status, disease, date and conflicts to be assessed. A single submission is not an established gene–disease relationship.
- **Somatic:** primary disease cohorts and functional studies, supported by curated cancer resources where licensing permits. Record study population, assay and denominator before quoting mutation prevalence. Distinguish any mutation from an established driver.
- **Interpretation:** authoritative disease classification, professional guidance, and regulatory labels for any future diagnostic/prognostic/predictive statement, with edition, jurisdiction and date.

GeneCards, OMIM, COSMIC, OncoKB, CIViC, and similar resources may help discovery, but public accessibility does not imply unrestricted bulk reuse. Review terms before ingestion or redistribution, including any commercial-use restriction. Prefer public, linkable evidence and original prose; record per-source reuse notes. No scraping or bulk redistribution of licensed summaries is authorized by this plan. The sample ClinVar records support nomenclature only; their germline assertions are not used to classify the pilot's somatic variants.

### Review and versioning

Use `draft → in_review → approved → retired`. Automated drafts stay `draft`. Record author, reviewer, review date, source-check date, revision, and change note. `approved` requires a named specialist and completed review date, not just successful schema validation. This pilot uses no fictitious reviewer and does not claim clinical approval.

Recommended future cadence: quarterly source and symbol checks, annual substantive gene review, and event-triggered review for major changes in classification or clinical evidence. Treatment comments may need a shorter interval. This is a recommendation only; no automation is scheduled. Keep released snapshots immutable, maintain a changelog, and distinguish source access from medical review. Retire records without breaking stable links.

## Stage two: alteration- and disease-specific comments

Keep these as separate records referencing gene and disease IDs. The schema reserves selectors for exact variants, codons, exon events, loss of function, amplification, deletion, and fusions. The preview exercises exact variants only. A future loss-of-function record must define qualifying alteration classes and exclude VUS, terminal truncations, and non-disruptive splice changes where inappropriate; a sequence call alone does not establish biallelic loss. Capture fusion partner/orientation and domain retention when relevant.

Each comment needs: normalized alteration and aliases; tumor context; mechanism; short report text; applicability restrictions; evidence references; editorial status; and an explicit interpretation scope (`biological` in this pilot). Later add separate diagnostic/prognostic/predictive assertions with evidence framework/version, level, jurisdiction, therapy, indication, line of therapy, resistance/sensitivity direction, and review date. Germline ACMG/AMP categories, somatic oncogenicity, and AMP/ASCO/CAP clinical significance are separate concepts and must never share one ambiguous “pathogenic” field.

Do not apply a gene-wide comment to every missense variant, transfer a hotspot comment to a different substitution, or copy clinical implications between tumors. Require exact selector and disease matching, documented inheritance rules for parent contexts, and explicit exceptions. An exact protein hotspot can arise from more than one nucleotide event; future matching should normalize equivalent representations without silently expanding biological scope.

The two pilot comments are **BRAF p.Val600Glu in melanoma** and **IDH1 p.Arg132His in diffuse glioma**, both limited to biological context. They make no treatment recommendation or integrated diagnostic assignment.

## Implementation sequence and acceptance criteria

| Milestone | Deliverable | Gate |
| --- | --- | --- |
| Current pilot | Plan, schema, three gene paragraphs, two hotspot comments, searchable preview | User reviews scope, format and interface |
| Inventory | Reproducible versioned panel union plus specialty gap report | User approves roster and priorities |
| Editorial calibration | 15–20 diverse genes from the approved roster | Specialist agrees on depth and wording |
| Stage-one batches | Groups of 25–50 genes; sources and disease tags reviewed together | Validate every file and review every clinical assertion |
| Stage-one release | Approved dictionary, search index, release manifest, review log | No unresolved identity/citation errors; required coverage audit passes |
| Stage-two pilot | Agree evidence framework; test exact hotspots and tumor-suppressor mechanisms across diseases | Specialist confirms applicability rules before expanding |

Stage one is complete only when every included gene has the required paragraph, verified identity, explicit germline status, source-backed somatic tags, and specialist approval. Counts reflect records actually present; never show 600 placeholders as completed entries. Every record remains labeled as a draft; the preview reads its counts from the bundled data.

The validator checks required structure, duplicate IDs, source and disease references, hierarchy cycles, panel version references, gene links, exact-variant selector requirements, URL schemes, and approval metadata. Build a compact generated search index after the inventory grows; avoid fetching 800 individual files at page load. Preserve source records as the authority and verify the generated index against them. Current loading is intentionally simple for the three-record pilot. Add automated browser interaction coverage when the pilot becomes production functionality.

## Questions to settle before expansion

1. Which assays should anchor the inventory? Default proposal: MSK-IMPACT, TSO500, FoundationOne CDx, plus heme/CNS/pediatric/sarcoma supplements. A local laboratory panel can take priority if supplied.
2. Should germline coverage include **all established Mendelian diseases**, or focus on cancer predisposition with brief mention of other major syndromes? The pilot uses the broader option.
3. Is a single **80–140-word paragraph**, with optional structured details and citations below it, the desired report-writing format?
4. Who will provide specialist approval before entries can be marked approved? Until a reviewer is designated and reviews content, all entries remain drafts.
5. US FDA regulatory indexing is now authorized. Exact allele/disease eligibility, current labels, and withdrawals still need adjudication before therapeutic report language can be approved.

## Source anchors consulted for this plan

- [MSK-IMPACT overview](https://www.mskcc.org/msk-impact)
- [MSK testing overview, including Heme](https://www.mskcc.org/cancer-care/diagnosis-treatment/diagnosing/next-generation-tumor-genetic-testing)
- [Illumina TSO500 product and gene-list links](https://www.illumina.com/products/by-type/clinical-research-products/trusight-oncology-500.html)
- [FoundationOne CDx product features](https://www.foundationmedicine.com/sites/default/files/document/F1CDx_Product_Features.pdf)
- [HGNC data license](https://www.genenames.org/about/license/)
- [OncoTree source and documentation](https://github.com/cBioPortal/oncotree)

Per-claim pilot sources are in `data/sources.json` and linked in the preview.

## Validation

```sh
node 'Knowledge Base/scripts/validate.mjs'
node --check 'Knowledge Base/app.js'
python3 'Knowledge Base/scripts/validate-curation.py'
python3 'Knowledge Base/scripts/validate-hotspots.py'
python3 'Knowledge Base/scripts/validate-report-comments.py'
```

The dependency-free validator covers the executable subset of this schema used by the pilot, plus cross-record rules. It is not a general JSON Schema engine. Use a full Draft 2020-12 validator in production CI before accepting external submissions.

## Applying the evidence review

After regenerating base drafts, run `python3 scripts/curate-evidence.py <draft-input-cache>` to reapply the source decisions, named citations and disclaimers. That historical script records the stage-one review boundary; stage-two drafting was subsequently authorized. It expects the original roster, so do not run it directly against the expanded dictionary. Rebuild the original base, apply the historical review, then apply the hotspot supplement and derived-index pipeline documented in [HOTSPOT-REVIEW.md](HOTSPOT-REVIEW.md). Evidence-review receipts and remaining gaps are in `data/evidence-curation.json`.

## Primary literature supplementation

Report comments retain database provenance and add primary-study PMID references where a retained gene–disease/inheritance assertion or original tumor-cohort record provides a matching publication. Common examples also have targeted literature links. Reviews, guidelines, editorials, and retracted articles are excluded. Automatically linked articles have metadata/abstract screening; detailed full-text and supplementary-data claim review remains open. `data/primary-citation-review.json` records each claim link, its assertion/cohort provenance, input receipts, and limitations. These citation links are reapplied when report prose is regenerated.

To extend the pass, retrieve PubMed XML for candidate references and run `scripts/supplement-primary-citations.py <pubmed-xml-cache> <gencc-csv>`, followed by the browser-index build, draft export, and validation commands. Do not cite a compendium's methods paper as proof of every contained gene–disease assertion.

## Claim-specific citation audit (supersedes automatic supplementation)

The automatic supplementation pass is superseded by the [report citation audit](CITATION-AUDIT.md). Unconfirmed PMID placements have been removed from report comments, while historical candidates remain archived. Retained PMIDs require an explicit reviewed support scope and exact statement binding, or original study-release observation evidence. `prepare-report-comments.py` reapplies the citation gate automatically. Run `python3 "Knowledge Base/scripts/validate-citation-audit.py"` after regeneration. The legacy automatic PMID importer is disabled; gene-name/abstract matching is insufficient to reinsert a citation.

## Continuing full-text reviews

[FULLTEXT-REVIEW.md](FULLTEXT-REVIEW.md) separates retrieved papers, explicit claim decisions, and unresolved work. The queue is in `data/fulltext-review-queue.json`; manual statement-specific decisions, with document hashes and Results/table locations, are in `curation/fulltext-review-decisions.json`. Retrieval never counts as verification. Reviewed support is restored only to the exact matching report statement; function, germline, mosaic and somatic claims are distinct. `validate-fulltext-review.py` checks these distinctions and the restored placements. The full-text review remains in progress.
