# Fusion draft review and coverage

2026-11-27 · Pathologist review needed — LLM-generated summary/review.

The user authorized fusion blurbs on 2026-11-27, superseding the planning-only boundary in the historical expansion plan. The requested order is a short sentence for each partner, fusion mechanism/oncogenicity, specific tumor associations, then supported prognosis and therapeutics. Generic interpretation reminders are excluded from report prose.

## Written content

Read the complete [fusion draft library](FUSION-DRAFTS.md).

| Content | Count |
| --- | ---: |
| Named fusion-pair entries | 165 |
| Chimeric fusion entries within that set | 161 |
| Regulatory fusion / promoter-substitution pairs within that set | 4 |
| Additional regulatory-event entries | 21 |
| Total draft entries | 186 |
| Entries with therapeutic sections | 80 |
| Entries with prognostic sections | 38 |
| Exact claim placements queued for citation adjudication | 678 |

The set covers 151 of the original 152 proposed pairs and adds 14 pairs: BCAN::NTRK1, EPC1::PHF1, ETV6::RET, FN1::ALK, JAZF1::PHF1, MEAF6::PHF1, MN1::CXXC5, NACC2::NTRK2, NPM1::MLF1, PTPRZ1::MET, QKI::NTRK2, RUNX1::MECOM, SQSTM1::NTRK3 and TFG::ALK. This is a broad initial library, not an exhaustive census of every published partner or breakpoint.

Every entry has brief partner descriptions, fusion biology, named tumor scope and sentence/section-level source links. Prognosis and treatment are included where a sufficiently specific statement could be drafted. Their absence is an omission from this draft, not a negative assertion that no prognostic or therapeutic literature exists. No numerical survival or response estimates were inserted without a dedicated cohort-level analysis.

The regulatory track includes locus-level categories. In particular, the four TCR-locus records are groups of enhancer rearrangements, not four sequenced fusion products. The IGH/FGFR3/NSD2 record describes a rearrangement affecting two oncogenes and has three partner descriptions. Benign/intermediate tumor associations, including pleomorphic adenoma and stromal nodules, are retained explicitly; an oncogenic event does not automatically establish malignant behavior.

## Source and review status

The dedicated registry contains **331 source records**, including normal-function gene references, primary studies, classifications, guidance and US regulatory sources. This is not a count of independently reviewed papers. Normal-function citations support partner biology and cannot establish fusion oncogenicity.

Sources were checked through abstracts, retrieved excerpts and selected full-text passages. Several clinical statements were checked against official prescribing information or approval notices. **A complete claim-by-claim primary full-text audit has not been performed. All 678 claim placements remain pending in the fusion-specific adjudication queue.** The review labels and source access levels preserve that distinction. No source or fusion has been promoted to specialist-approved status.

Primary evidence, classification statements, case reports, preclinical experiments and regulatory indications are described at their actual scope. Examples include:

- KMT2A translocations: revumenib's relapsed/refractory acute leukemia indication, including its age restriction; a class indication does not certify equal efficacy for every rare partner.
- BRAF fusions: tovorafenib's pediatric low-grade glioma indication and the mechanistic difference from BRAF V600-selective inhibition. RAF1 fusions do not inherit the BRAF label.
- FGFR3::TACC3: separate glioma preclinical evidence and urothelial carcinoma erdafitinib eligibility, including prior-treatment requirements.
- NRG1 fusions: ligand-driven HER2/HER3 signaling and dated US zenocutuzumab tumor indications.
- ETV6::FLT3: a reported gilteritinib response is case-level off-label evidence, not a fusion-specific approval.
- SS18::SSX: afamitresgene autoleucel eligibility requires the specified HLA alleles and MAGE-A4 expression in addition to the synovial sarcoma treatment setting.
- ASPSCR1::TFE3: the atezolizumab ASPS indication is not transferred to renal cell carcinoma.
- RARA variants: ZBTB16/STAT5B resistance and NPM1-associated retinoid responsiveness are kept distinct from conventional PML::RARA APL.

Regulatory sources carry dates and the relevant US indication scope. The library is not an exhaustive current drug-label compendium. Older label documents remain explicitly dated; no assertion is made that every cited label is the latest revision. Current-label verification is part of the remaining clinical review.

## Held candidates

| Candidate | Reason no blurb was written |
| --- | --- |
| TPR::NTRK3 | A pair-specific primary report was not confirmed. Retrieved TPR evidence supported NTRK1; substituting a paralog would be unsafe. This is the only original roster pair held. |
| ETV6::MET | Located on assay lists during expansion, but primary clinical/functional evidence was not confirmed in this pass. Assay coverage does not establish an oncogenic driver. |

Further expansion should prioritize supported recurrent pairs and avoid promoting every observed or assay-listed chimera. Follow the pair-level notes for unresolved biological, diagnostic and clinical assertions. Additional tumor contexts were omitted where dedicated citations were not yet available.

## Artifacts and regeneration

The hand-curated source of prose is `curation/fusions/draft-content.json`. Partner sentences/identities are in `curation/fusions/partners.json`; the dedicated bibliography is `curation/fusions/sources.json`. Identity matching uses the existing frozen HGNC inventory snapshot with a recorded SHA-256 receipt, not a newly downloaded HGNC release. The generic TCR-locus group deliberately has no invented gene identifier.

Generated files:

- `data/fusions/<stable-id>.json`: one entry with partner records, tumor scopes, source-linked sections, draft report projection and hashes.
- `data/fusion-index.json`: compact index and file manifest for this separate corpus.
- `data/fusion-sources.json`: bibliography for the fusion corpus.
- `data/fusion-drafting-review.json`: counts, coverage and held candidates.
- `data/fusion-evidence-review-queue.json`: every exact claim/source placement for subsequent adjudication.
- `FUSION-DRAFTS.md`: complete readable export with adjacent citations.

From the repository root:

```sh
python3 'Knowledge Base/scripts/draft-fusions.py'
python3 'Knowledge Base/scripts/validate-fusions.py'
```

The validator checks unique records, partner identity/sentence alignment, complete source references, non-gene evidence for fusion assertions, exact claim hashes, queue coverage, roster accounting and export/index consistency. These checks verify the data contract and editorial state; they do not adjudicate medical accuracy or replace specialist review.

The fusion corpus is not connected to the live browser, runtime manifest, original citation-audit policy or approved-content pipeline. Existing gene/hotspot/disruption records are not rebuilt by the fusion commands. Browser integration and publication were not performed in this drafting task.
