# Oncogenic fusion expansion plan

2026-11-27 · Planning only · No fusion blurbs drafted or authorized by this document.

Historical planning boundary: the user subsequently authorized drafting on 2026-11-27. See [fusion draft review](FUSION-REVIEW.md) and the [draft library](FUSION-DRAFTS.md) for the resulting work. The planning-only language below describes the earlier phase.

## Proposed scope

Add a dedicated fusion catalog to the molecular pathology knowledge base, connected to both partner genes and explicitly reviewed disease contexts. Start with established recurrent pairs and expand to less common partners after the identity and evidence model works. Include kinase, transcription-factor, chromatin-regulator, and ligand fusions. Maintain a separate regulatory-rearrangement track for enhancer hijacking and promoter substitution.

The deliverable for this phase is the plan and proposed inventory. No runtime data, schemas, browser code, report projections, gene paragraphs, or existing comments are changed. Blurb drafting remains a later, separately authorized task.

## Inventory and rollout

The [readable fusion list](inventory/FUSION-LIST.md) and [structured roster](inventory/fusion-roster.json) contain **152 unique ordered pairs** and **21 separately counted regulatory-event candidates**. This is a curated starting proposal, not an exhaustive census or a clinically adjudicated driver list. Each row has proposed contexts and discovery leads; those are inputs to evidence review. Clinical validity is not implied by inventory inclusion.

| Wave | Pairs | Purpose |
| --- | ---: | --- |
| 1 | 71 | Core recurrent fusions across solid tumors, hematologic neoplasia, sarcoma, and CNS disease |
| 2 | 70 | Extend partner coverage and specialty tumor coverage; exercise disease and mechanism distinctions |
| 3 | 11 | Less common partners and boundary cases requiring focused review |
| Separate regulatory track | 21 events | Immunoglobulin/TCR rearrangements, promoter substitution, and enhancer relocation |

Wave numbers indicate proposed work order, not oncogenicity, diagnostic specificity, prevalence, or therapeutic evidence. Multiple disease contexts for the same pair count once in the roster; future pair-by-disease assertions will increase the number of evidence records. Transcript isoforms and exon junctions do not automatically become separate pair records. Reciprocal products require their own supporting evidence.

Nineteen proposed partner symbols are absent from the current gene dictionary: AHCYL1, BCL9, CARS1, DDX10, EBF1, EZR, FAM131B, HNRNPUL1, HOXD13, INA, LIFR, MLLT6, RCSD1, SDC4, SET, SQSTM1, SRGAP3, SSBP2, and TPM4. Revalidate against a dated HGNC release, including aliases, before adding identity-only stubs. This audit does not establish that the genes are absent under every historical name.

## Fit with the existing application

The current knowledge base has 1,305 gene records, a gene index, disease hierarchy, shared sources, two pilot variant comments, and hotspot/disruption libraries. `schemas/knowledge-base.schema.json` permits `selector.kind = fusion`, but the selector lacks structured partners and breakpoint/domain fields. Variant comments have a single `gene_id`; the browser loads them from `manifest.variant_files`. That structure needs extension to support a fusion shared by two genes without duplicating the underlying record.

Proposed future files:

- `data/fusions/<stable-id>.json`: categorical pair identity and mechanism constraints.
- `data/fusion-assertions/<stable-id>.json`: one fusion, disease context, claim type, and evidence set; report text added only in the later drafting phase.
- `data/fusion-index.json`: generated compact search and navigation index.
- A dedicated fusion schema, manifest entries, validator, and browser build step, following the repository's existing static JSON pattern.

Keep this planning roster outside the runtime manifest. Use the existing disease/source registries after their entries are reviewed. Do not silently make up ontology codes or import the candidate roster as approved content.

## Identity and representation

Use approved HGNC symbols with stable HGNC IDs. Display chimeric gene pairs in 5′ to 3′ order using `GENE1::GENE2`, consistent with [HGNC guidance](https://www.genenames.org/about/guidelines/). Preserve source spelling and aliases such as MLL/KMT2A, MKL1/MRTFA, C11orf95/ZFTA, and API2/BIRC3. Searching either partner or a historical fusion name should find the canonical record.

Use the [Gene Fusion Specification](https://fusions.cancervariants.org/en/latest/) as the modeling reference for categorical versus assayed fusions and regulatory versus chimeric events. The consulted specification identifies itself as pre-release; pin a version or commit before implementation.

The categorical catalog should support:

- Ordered partner IDs, canonical label, aliases, stable internal ID, and identity provenance.
- Product/mechanism class: chimeric protein, promoter substitution, enhancer hijacking, other, or unresolved. Some events need more than one mechanism annotation.
- Necessary retained domains, relevant loss of regulatory domains, and known breakpoint-dependent exceptions, each with evidence.
- Disease-independent biological assertions separated from disease-specific assertions.
- Family membership, such as ALK or NTRK fusion, without treating every possible partner as equivalent.

A later assay-level representation can add versioned transcripts, exon junctions, assembly/coordinates, breakpoint precision, orientation, predicted reading frame, assay type, and expression confirmation. Unknown values remain unknown. Do not invent a single canonical junction for a pair, require coding exons for every regulatory event, or equate an in-frame call with an oncogenic product. An observed DNA rearrangement, a break-apart FISH result, an RNA transcript, and an inferred protein fusion are distinct evidence types.

Use locus-aware regulatory records for immunoglobulin/TCR events. A slash-separated label in this planning list is shorthand for loci to investigate, not an asserted transcript or formal regulatory nomenclature. Preserve derivative structure and affected regulatory elements when supported. Keep KMT2A partial tandem duplication, BCOR internal tandem duplication, FGFR tandem duplication, MET exon 14 skipping, gene amplification, and incidental read-through transcripts outside the fusion-pair catalog; link relevant alteration records later.

## Evidence work before prose

1. **Normalize and freeze the inventory.** Resolve partner identities and aliases against a dated HGNC release; verify 5′/3′ order from original reports; document duplicate pairs, ambiguous loci, exclusions, and missing dictionary entries. Finalize waves after evidence triage.
2. **Acquire pair-specific sources.** Follow classification, PDQ, and cohort leads to original discovery, functional, and disease-cohort papers. Record DOI/PMID, accessible full-text URL, access date, exact figure/table/passage, study population, assay, and relevant breakpoint/product. Database listing or assay coverage alone does not establish oncogenicity.
3. **Adjudicate each assertion.** Track `not_reviewed`, `supports`, `partial`, `does_not_support`, `conflicting`, and `unavailable`. Record the reviewer and rationale. Separate detection, recurrence, transforming activity, disease association, diagnostic value, prognosis, and treatment response. A cohort occurrence may support detection without proving a driver mechanism.
4. **Review each disease context.** Create stable local disease links, document ontology release/mappings, and specify descendant applicability. Preserve important lineage, age, and histologic distinctions. A family-level or pan-cancer association must not automatically supply a comment for a specific diagnosis.
5. **Resolve mechanism exceptions.** Review retained functional domains, breakpoint restrictions, reciprocal products, and unusual partners. Separate fusions arising as acquired resistance from initiating drivers. Keep benign/intermediate tumor associations explicit; fusion status alone must not establish malignancy.
6. **Freeze an evidence-ready subset.** Produce a row-level evidence matrix and unresolved queue. Only supported biological assertions become eligible for later prose. Diagnostic/prognostic/predictive claims require their own review; therapy claims additionally require dated jurisdiction-specific regulatory/guideline evidence.

Sources in the roster are discovery leads, not a completed claim-to-citation audit. In particular, a broad pan-cancer source is not presumed to validate a specialty fusion absent from its cohort. Keep unsupported candidates in the review queue or exclude them with a reason. Use original synthesis later and retain source-specific reuse terms; this plan does not authorize bulk redistribution of licensed summaries.

## Implementation sequence after planning

1. Define and validate the fusion identity and assertion schemas using a small representative set: BCR::ABL1, EML4::ALK, ETV6::NTRK3, FGFR2::BICC1, EWSR1::ATF1, KIAA1549::BRAF, and one regulatory event. These exercise multiple contexts, domain dependence, partner order, and regulatory representation without requiring prose.
2. Add missing partner identities and disease terms with source provenance. Build the reviewed pair index and assertion records. Draft fields remain absent until drafting is authorized.
3. Add a fusion browse/search mode and links from both gene pages to the same canonical pair. Show filters for partner, family, disease, mechanism, and review status. Match canonical and legacy names, hyphenated input, and reversed partner queries; reversed queries may retrieve a record without asserting that the reciprocal product is equivalent.
4. Apply disease filtering to individual assertions. For example, EWSR1::ATF1 can require distinct histologic contexts; a shared pair is not a unique diagnosis. Keep family-level evidence distinguishable from pair-specific and junction-specific evidence.
5. Add fusion counts to the appropriate UI locations without inflating gene or hotspot counts. Keep draft status visible. Enable copying only when reviewed report text exists; candidate records carry no placeholder report paragraph.
6. After separate authorization to draft, create concise biological comments from approved assertions, run the existing citation/report-language review workflow with fusion support, then perform pathologist review and release versioning.

## Acceptance checks for later implementation

- Unique stable IDs; no duplicate ordered pairs; valid partner/source/disease references; explicit review states.
- Family-level evidence cannot silently establish pair-level or junction-level evidence. A reported reciprocal does not inherit support automatically.
- Aliases resolve to a canonical pair; both gene pages link to it. Unknown partners and regulatory loci do not receive fabricated HGNC IDs.
- Supported assertions cite exact evidence. Missing full text and contradictory evidence remain visible to curators.
- Disease filtering respects assertion scope and descendant flags. BCR::ABL1 contexts and EWSR1::ATF1 histologies remain separable.
- Regulatory events render without invented chimeric proteins; DNA/FISH evidence does not silently become RNA confirmation.
- Existing gene, hotspot, disruption, source-link, search, and report-copy behavior passes regression checks. Check the static site over HTTP and inspect narrow-screen layouts.
- Release audit reports pair count, assertion count, source coverage, identity/disease mapping gaps, unsupported candidates, exclusions, and review completion independently.

## Completion boundary for this request

The plan and proposed inventory are saved. No blurbs, report comments, runtime integration, or publication are part of this completed planning step. The next substantive step is pair-specific identity and full-text evidence review, followed by a revised inclusion list before drafting.
