# Fusion evidence audit and integration

2026-11-27 · Pathologist review needed — LLM-generated summary/review.

**186 corrected draft entries are integrated into the knowledge base.** The follow-up pass covered the 49 previously reference-supported entries and the held ETV6::NTRK2 entry. All 50 now retain at least one fusion-specific finding supported by inspected primary body material. This entry-level status does not certify every assertion or tumor association in its paragraph as primary-supported. All 305 original fusion-specific sections across the 186 drafted entries have an explicit source-review decision. This is a completed disposition pass with documented access limits, not certification that every assertion was verified against a primary full text.

[Browse fusions](index.html?mode=fusions) · [Read the corrected blurbs](FUSION-DRAFTS.md) · [Machine-readable audit](data/fusion-audit.json)

## What was reviewed

| Measure | Result |
| --- | ---: |
| Original fusion-specific sections assessed | 305 |
| Retained unchanged | 74 |
| Narrowed, corrected or re-sourced | 224 |
| Removed without replacement | 7 |
| Unique normal partner descriptions reviewed separately | 210 |
| Partner descriptions narrowed | 79 |
| Integrated draft entries | 186 |
| Entries with retained primary-body fusion evidence | 186 |
| Entries with authoritative-reference support only | 0 |
| Previously drafted entry held from runtime | 0 |
| Retained therapeutic sections | 79 |
| Retained prognostic sections | 32 |

The integrated corpus has 165 named pairs (161 chimeric fusions, three promoter-substitution pairs and one other regulatory fusion) plus 21 regulatory-event categories. Some categories group locus rearrangements rather than specifying a sequenced chimeric transcript. It covers 151 original pair-roster candidates and 14 additional pairs.

## Evidence boundaries

Review decisions cite an inspected primary Results section, figure, table or indexed body passage when available. Publisher/PMC access failures and abstract-only evidence are not counted as primary-body confirmation. Official drug labels and authoritative classifications/guidance are explicitly typed as such. Some individual claims remain supported by classifications, guidance or regulatory sources. The section evidence identifies these separately even when another finding gives the entry a primary-evidence status. FUS::ATF1 illustrates this distinction: its peritoneal mesothelioma observation is primary-supported, while its angiomatoid fibrous histiocytoma association remains classification-supported.

There are 671 retained source-linked section placements in the runtime corpus: 230 supported by inspected primary-body material, 54 by official regulatory evidence, and 387 by gene/identity or other authoritative references. The latter includes 373 repeated partner-description placements. These counts are placements, not distinct studies or independently validated patient observations.

Normal partner descriptions were separately checked against the existing cached NCBI/RefSeq/Alliance summaries and frozen HGNC identities. Unsubstantiated functional detail was narrowed, sometimes to the encoded protein identity. This is a reference/identity check, not a primary full-text functional audit of 210 genes.

Full-text review here is LLM source review. Molecular-pathologist review remains pending, and no entry has been promoted to approved status. US regulatory claims retain source dates; the audit does not establish that every historical label is the newest revision or constitute an exhaustive treatment guideline.

## Material corrections

- **Detection versus function:** cohort detection is no longer presented as direct transforming evidence for every partner. Rare EWSR1::ETS, SS18::SSX and kinase-fusion partners retain only the architecture or disease association supported by their sources.
- **MEF2D prognosis:** the poor-outcome observation is bounded to the analyzed cohort and distinguished from a nonsignificant adjusted risk estimate.
- **KMT2A:** blanket menin/HOXA/MEIS1 mechanism language was removed where the inspected partner cohort established occurrence rather than the entire functional mechanism. Official revumenib eligibility remains explicitly regulatory evidence.
- **BCAN::NTRK1:** the experimental glioma statement now identifies the cooperating p53 loss in the reviewed model.
- **ZFTA::RELA:** the mechanism no longer asserts that the RELA NF-kappaB-binding domain is required for tumorigenicity.
- **RAF1:** dual-pathway findings are bounded to the studied cell systems.
- **EWSR1::PATZ1:** the broad epithelial-marker generalization was removed; the source series did not support it.
- **PHF1 and BCOR-associated tumors:** speculative pathway language was narrowed. Directly documented ossifying fibromyxoid tumor associations were added where supported.
- **Prognosis:** inaccessible GRACefUl wording was replaced with the directly inspected BCOR::CCNB3 retrospective cohort and historical CIC comparator. The unconfirmed RANBP2::ALK comparative-prognosis statement remains removed. Infantile VGLL2 observations are bounded to a small cohort.
- **IGH/CCND2 and IGH/CCND3:** exact IGH partner findings are now supported by primary results; light-chain partner findings are not substituted for them.
- **TCR loci:** the four retained descriptions specify the documented TRD rearrangements rather than implying that every TCR locus was demonstrated.
- **ETV6::NTRK2:** restored with AML discovery, experimental transformation and transient patient-response evidence. The pulmonary atypical carcinoid case remains an access gap and is excluded from the paragraph.
- **NPM1::RARA:** the treatment observation is bounded to a patient receiving combination therapy; it does not establish sensitivity to tretinoin alone.
- **ETV6::RUNX1 and TCF3::PBX1:** outcomes now identify the treatment cohorts; favorable results are not generalized across historical regimens, and the TCF3::PBX1 CNS-relapse observation is explicit.
- **Clinical eligibility:** drug statements retain actual tumor, age and prior-treatment restrictions. Experimental/case-level inhibitor findings do not become FDA indications.

## Remaining access gaps and deferred candidates

| Candidate | Disposition |
| --- | --- |
| ETV6::NTRK2 pulmonary case | PMID 38584068 full text remains inaccessible. Its pulmonary disease/entrectinib claims are excluded. The fusion itself is integrated with independently reviewed AML evidence. |
| FUS::ATF1 in AFH | Original AFH case full texts remain inaccessible; this association remains explicitly classification-supported. A peritoneal mesothelioma observation is directly primary-supported. |
| TPR::NTRK3 | Never drafted. Exact-pair primary evidence remains unconfirmed; TPR::NTRK1 must not be substituted. |
| ETV6::MET | Never drafted. Assay-list inclusion alone did not establish a driver or tumor association. |

An unavailable paper is an access gap, not a finding that a fusion is false or non-oncogenic. Removed original wording and decision rationales remain in the curation audit and pre-audit snapshot.

## Knowledge-base integration

The main browser now has **Genes & variants** and **Fusions & rearrangements** views. The fusion view supports either partner order, canonical pair names, legacy aliases, tumor category and assigned tumor type. Existing gene entries link to shared canonical fusion records through a Fusions tab; partners without a standalone gene record still have an identity in their fusion entry.

Each fusion entry shows its report paragraph, adjacent citations, partner links, draft status and an expandable evidence audit with source locations. Copying includes retained text, citations, source links, audit date and the specialist-review disclaimer. No previously drafted entry remains held after this follow-up. Deferred discovery candidates remain outside the browser and report export.

New disease labels use explicitly local unmapped IDs, with no invented OncoTree/NCIt codes. Fusion bibliography and disease additions are loaded through separate manifest paths, preserving the existing gene/source registries. No hosted deployment or Git push was performed.

## Traceability and reproduction

- `curation/fusions/pre-audit-content.json`: frozen original fusion prose.
- `curation/fusions/pre-audit-partners.json`: original partner sentences.
- `curation/fusions/audit-heme.json`, `audit-sarcoma.json`, `audit-solid-cns.json`: claim decisions and inspected evidence locations.
- `curation/fusions/followup-baseline.json`: frozen 50-entry starting state for this follow-up.
- `curation/fusions/audit-followup-heme.json`, `audit-followup-sarcoma.json`, `audit-followup-regulatory.json`: subsequent full-text decisions applied as reproducible overlays; original first-pass artifacts are preserved.
- `curation/fusions/audit-partners.json`: normal-description reference decisions.
- `curation/fusions/audit-decisions.json`: merged decisions, original text hashes and access limits.
- `data/fusion-audit.json`: generated audit export.
- `data/fusions/`, `fusion-index.json`, `fusion-browser.json`, `fusion-sources.json`, `fusion-diseases.json`: runtime corpus.

```sh
python3 "Knowledge Base/scripts/apply-fusion-audit.py"
python3 "Knowledge Base/scripts/draft-fusions.py"
python3 "Knowledge Base/scripts/validate-fusions.py"
node "Knowledge Base/scripts/test-fusion-browser.mjs"
node "Knowledge Base/scripts/validate.mjs"
```

Changing reviewed text invalidates its exact audit hash. The builder and validator require a matching retained decision and inspected-evidence location; retrieval or gene-name matching cannot clear a claim.

Validation passed for corpus structure, audit/source hashes, index/export consistency, held-record exclusion, disease links, legacy/reversed-partner queries, category/tumor isolation and deep links. Local-browser checks passed for gene/fusion navigation, citation copying, empty results and readable layout at the available 559-pixel viewport, with no horizontal overflow or console errors.

## Entry-level disposition

Each primary status below means at least one retained fusion-specific finding has inspected primary-body support. Consult section evidence for guidance, regulatory and remaining reference-only claims.

| Entry | Integration | Evidence for retained fusion claims | Original-section decisions |
| --- | --- | --- | --- |
| EML4::ALK | Integrated draft | Primary body/results retained | 1 narrow, 1 retain |
| KIF5B::ALK | Integrated draft | Primary body/results retained | 1 narrow, 1 retain |
| STRN::ALK | Integrated draft | Primary body/results retained | 1 narrow, 1 retain |
| KIF5B::RET | Integrated draft | Primary body/results retained | 2 retain |
| CCDC6::RET | Integrated draft | Primary body/results retained | 1 narrow, 1 retain |
| NCOA4::RET | Integrated draft | Primary body/results retained | 1 narrow, 1 retain |
| ETV6::RET | Integrated draft | Primary body/results retained | 1 narrow, 1 retain |
| CD74::ROS1 | Integrated draft | Primary body/results retained | 1 narrow, 1 retain |
| SLC34A2::ROS1 | Integrated draft | Primary body/results retained | 1 narrow, 1 retain |
| SDC4::ROS1 | Integrated draft | Primary body/results retained | 1 narrow, 1 retain |
| EZR::ROS1 | Integrated draft | Primary body/results retained | 1 narrow, 1 retain |
| TPM3::ROS1 | Integrated draft | Primary body/results retained | 1 narrow, 1 retain |
| GOPC::ROS1 | Integrated draft | Primary body/results retained | 1 narrow, 1 retain |
| TPM3::NTRK1 | Integrated draft | Primary body/results retained | 1 narrow, 1 retain |
| LMNA::NTRK1 | Integrated draft | Primary body/results retained | 1 narrow, 1 retain |
| TPR::NTRK1 | Integrated draft | Primary body/results retained | 1 narrow, 1 retain |
| SQSTM1::NTRK1 | Integrated draft | Primary body/results retained | 1 narrow, 1 retain |
| EML4::NTRK3 | Integrated draft | Primary body/results retained | 1 narrow, 1 retain |
| SQSTM1::NTRK3 | Integrated draft | Primary body/results retained | 1 narrow, 1 retain |
| ETV6::NTRK3 | Integrated draft | Primary body/results retained | 1 narrow, 1 retain |
| ETV6::NTRK2 | Integrated draft | Primary body/results retained | 2 narrow |
| FGFR2::BICC1 | Integrated draft | Primary body/results retained | 1 narrow, 1 retain |
| FGFR2::AHCYL1 | Integrated draft | Primary body/results retained | 1 narrow, 1 retain |
| FGFR2::ETV6 | Integrated draft | Primary body/results retained | 1 narrow, 1 retain |
| FGFR2::INA | Integrated draft | Primary body/results retained | 1 narrow, 1 retain |
| FGFR3::TACC3 | Integrated draft | Primary body/results retained | 3 retain |
| FGFR1::TACC1 | Integrated draft | Primary body/results retained | 2 retain |
| CD74::NRG1 | Integrated draft | Primary body/results retained | 1 narrow, 1 retain |
| SLC3A2::NRG1 | Integrated draft | Primary body/results retained | 1 narrow, 1 retain |
| ATP1B1::NRG1 | Integrated draft | Primary body/results retained | 1 narrow, 1 retain |
| TPM3::ALK | Integrated draft | Primary body/results retained | 1 narrow, 1 retain |
| TPM4::ALK | Integrated draft | Primary body/results retained | 1 narrow, 1 retain |
| CLTC::ALK | Integrated draft | Primary body/results retained | 1 narrow, 1 retain |
| RANBP2::ALK | Integrated draft | Primary body/results retained | 1 narrow, 1 retain, 1 remove |
| CARS1::ALK | Integrated draft | Primary body/results retained | 1 narrow, 1 retain |
| NPM1::ALK | Integrated draft | Primary body/results retained | 2 narrow |
| BCR::ABL1 | Integrated draft | Primary body/results retained | 2 narrow |
| PML::RARA | Integrated draft | Primary body/results retained | 2 narrow |
| RUNX1::RUNX1T1 | Integrated draft | Primary body/results retained | 1 narrow, 1 retain |
| CBFB::MYH11 | Integrated draft | Primary body/results retained | 1 narrow, 1 retain |
| DEK::NUP214 | Integrated draft | Primary body/results retained | 1 narrow, 1 retain |
| RBM15::MRTFA | Integrated draft | Primary body/results retained | 1 narrow |
| KMT2A::MLLT3 | Integrated draft | Primary body/results retained | 2 narrow, 1 retain |
| KMT2A::AFF1 | Integrated draft | Primary body/results retained | 2 narrow |
| KMT2A::MLLT10 | Integrated draft | Primary body/results retained | 3 narrow |
| KMT2A::ELL | Integrated draft | Primary body/results retained | 2 narrow, 1 retain |
| KMT2A::AFDN | Integrated draft | Primary body/results retained | 2 narrow, 1 remove |
| KMT2A::MLLT1 | Integrated draft | Primary body/results retained | 2 narrow, 1 retain |
| KMT2A::MLLT6 | Integrated draft | Primary body/results retained | 2 narrow, 1 retain |
| NUP98::NSD1 | Integrated draft | Primary body/results retained | 2 narrow |
| NUP98::KDM5A | Integrated draft | Primary body/results retained | 2 narrow |
| NUP98::HOXA9 | Integrated draft | Primary body/results retained | 1 narrow |
| NUP98::HOXD13 | Integrated draft | Primary body/results retained | 1 narrow |
| NUP98::DDX10 | Integrated draft | Primary body/results retained | 1 narrow |
| NUP98::TOP1 | Integrated draft | Primary body/results retained | 1 narrow |
| CBFA2T3::GLIS2 | Integrated draft | Primary body/results retained | 1 narrow, 1 remove |
| FUS::ERG | Integrated draft | Primary body/results retained | 2 narrow, 1 retain |
| RUNX1::CBFA2T3 | Integrated draft | Primary body/results retained | 1 narrow, 1 retain |
| PICALM::MLLT10 | Integrated draft | Primary body/results retained | 1 narrow |
| SET::NUP214 | Integrated draft | Primary body/results retained | 1 narrow |
| KAT6A::CREBBP | Integrated draft | Primary body/results retained | 2 narrow |
| KAT6A::EP300 | Integrated draft | Primary body/results retained | 1 narrow |
| ZBTB16::RARA | Integrated draft | Primary body/results retained | 2 narrow |
| NPM1::RARA | Integrated draft | Primary body/results retained | 2 narrow |
| STAT5B::RARA | Integrated draft | Primary body/results retained | 1 narrow, 1 remove |
| FIP1L1::PDGFRA | Integrated draft | Primary body/results retained | 2 narrow |
| ETV6::PDGFRB | Integrated draft | Primary body/results retained | 2 narrow |
| ZMYM2::FGFR1 | Integrated draft | Primary body/results retained | 2 narrow |
| BCR::FGFR1 | Integrated draft | Primary body/results retained | 2 narrow |
| PCM1::JAK2 | Integrated draft | Primary body/results retained | 2 narrow |
| ETV6::JAK2 | Integrated draft | Primary body/results retained | 1 narrow |
| BCR::JAK2 | Integrated draft | Primary body/results retained | 2 narrow |
| PAX5::JAK2 | Integrated draft | Primary body/results retained | 2 narrow |
| ETV6::FLT3 | Integrated draft | Primary body/results retained | 1 narrow, 1 retain |
| ETV6::ABL1 | Integrated draft | Primary body/results retained | 2 narrow |
| RCSD1::ABL1 | Integrated draft | Primary body/results retained | 2 narrow |
| NUP214::ABL1 | Integrated draft | Primary body/results retained | 2 narrow |
| EBF1::PDGFRB | Integrated draft | Primary body/results retained | 2 narrow |
| SSBP2::CSF1R | Integrated draft | Primary body/results retained | 2 narrow |
| ETV6::RUNX1 | Integrated draft | Primary body/results retained | 2 narrow |
| TCF3::PBX1 | Integrated draft | Primary body/results retained | 2 narrow |
| TCF3::HLF | Integrated draft | Primary body/results retained | 3 narrow |
| MEF2D::BCL9 | Integrated draft | Primary body/results retained | 1 narrow, 1 retain |
| MEF2D::HNRNPUL1 | Integrated draft | Primary body/results retained | 1 narrow, 1 retain |
| EP300::ZNF384 | Integrated draft | Primary body/results retained | 1 narrow |
| TCF3::ZNF384 | Integrated draft | Primary body/results retained | 1 narrow |
| TAF15::ZNF384 | Integrated draft | Primary body/results retained | 1 narrow |
| PAX5::ETV6 | Integrated draft | Primary body/results retained | 1 narrow |
| BIRC3::MALT1 | Integrated draft | Primary body/results retained | 2 narrow |
| EWSR1::FLI1 | Integrated draft | Primary body/results retained | 1 retain |
| EWSR1::ERG | Integrated draft | Primary body/results retained | 1 narrow |
| EWSR1::ETV1 | Integrated draft | Primary body/results retained | 1 narrow |
| EWSR1::ETV4 | Integrated draft | Primary body/results retained | 1 narrow |
| EWSR1::FEV | Integrated draft | Primary body/results retained | 1 narrow |
| SS18::SSX1 | Integrated draft | Primary body/results retained | 1 narrow, 1 retain |
| SS18::SSX2 | Integrated draft | Primary body/results retained | 1 narrow, 1 retain |
| SS18::SSX4 | Integrated draft | Primary body/results retained | 1 narrow, 1 retain |
| PAX3::FOXO1 | Integrated draft | Primary body/results retained | 2 narrow |
| PAX7::FOXO1 | Integrated draft | Primary body/results retained | 2 narrow |
| EWSR1::WT1 | Integrated draft | Primary body/results retained | 1 narrow |
| FUS::DDIT3 | Integrated draft | Primary body/results retained | 1 narrow, 1 retain |
| EWSR1::DDIT3 | Integrated draft | Primary body/results retained | 1 narrow, 1 retain |
| COL1A1::PDGFB | Integrated draft | Primary body/results retained | 2 narrow |
| NAB2::STAT6 | Integrated draft | Primary body/results retained | 1 narrow |
| ASPSCR1::TFE3 | Integrated draft | Primary body/results retained | 1 narrow, 1 retain |
| EWSR1::ATF1 | Integrated draft | Primary body/results retained | 1 narrow |
| EWSR1::CREB1 | Integrated draft | Primary body/results retained | 1 narrow |
| FUS::ATF1 | Integrated draft | Primary body/results retained | 1 narrow |
| FUS::CREB3L2 | Integrated draft | Primary body/results retained | 1 narrow |
| FUS::CREB3L1 | Integrated draft | Primary body/results retained | 1 narrow |
| EWSR1::CREB3L1 | Integrated draft | Primary body/results retained | 1 narrow |
| CIC::DUX4 | Integrated draft | Primary body/results retained | 2 narrow |
| BCOR::CCNB3 | Integrated draft | Primary body/results retained | 2 narrow |
| EWSR1::NFATC2 | Integrated draft | Primary body/results retained | 1 narrow |
| EWSR1::PATZ1 | Integrated draft | Primary body/results retained | 1 narrow |
| HEY1::NCOA2 | Integrated draft | Primary body/results retained | 1 narrow |
| EWSR1::NR4A3 | Integrated draft | Primary body/results retained | 1 narrow |
| TAF15::NR4A3 | Integrated draft | Primary body/results retained | 1 narrow |
| WWTR1::CAMTA1 | Integrated draft | Primary body/results retained | 1 narrow |
| YAP1::TFE3 | Integrated draft | Primary body/results retained | 1 narrow |
| JAZF1::SUZ12 | Integrated draft | Primary body/results retained | 1 narrow |
| YWHAE::NUTM2A | Integrated draft | Primary body/results retained | 1 narrow |
| YWHAE::NUTM2B | Integrated draft | Primary body/results retained | 1 narrow |
| ZC3H7B::BCOR | Integrated draft | Primary body/results retained | 1 narrow |
| PAX3::MAML3 | Integrated draft | Primary body/results retained | 1 narrow, 1 remove |
| VGLL2::NCOA2 | Integrated draft | Primary body/results retained | 2 narrow |
| VGLL2::CITED2 | Integrated draft | Primary body/results retained | 2 narrow |
| KIAA1549::BRAF | Integrated draft | Primary body/results retained | 2 narrow |
| FAM131B::BRAF | Integrated draft | Primary body/results retained | 2 narrow |
| SRGAP3::RAF1 | Integrated draft | Primary body/results retained | 1 narrow, 1 retain |
| QKI::RAF1 | Integrated draft | Primary body/results retained | 1 narrow, 1 retain |
| ZFTA::RELA | Integrated draft | Primary body/results retained | 1 narrow |
| YAP1::MAMLD1 | Integrated draft | Primary body/results retained | 1 retain |
| MYB::QKI | Integrated draft | Primary body/results retained | 1 narrow |
| MN1::BEND2 | Integrated draft | Primary body/results retained | 1 narrow |
| MN1::CXXC5 | Integrated draft | Primary body/results retained | 1 narrow |
| SLC44A1::PRKCA | Integrated draft | Primary body/results retained | 1 narrow |
| CRTC1::MAML2 | Integrated draft | Primary body/results retained | 1 narrow, 1 retain |
| CRTC3::MAML2 | Integrated draft | Primary body/results retained | 2 narrow |
| MYB::NFIB | Integrated draft | Primary body/results retained | 1 narrow |
| MYBL1::NFIB | Integrated draft | Primary body/results retained | 1 narrow |
| BRD4::NUTM1 | Integrated draft | Primary body/results retained | 1 narrow, 1 retain |
| BRD3::NUTM1 | Integrated draft | Primary body/results retained | 1 narrow, 1 retain |
| NSD3::NUTM1 | Integrated draft | Primary body/results retained | 1 narrow, 1 retain |
| DNAJB1::PRKACA | Integrated draft | Primary body/results retained | 1 narrow |
| TMPRSS2::ERG | Integrated draft | Primary body/results retained | 1 narrow |
| CTNNB1::PLAG1 | Integrated draft | Primary body/results retained | 1 narrow |
| LIFR::PLAG1 | Integrated draft | Primary body/results retained | 1 narrow |
| TFG::ALK | Integrated draft | Primary body/results retained | 1 narrow, 1 retain |
| FN1::ALK | Integrated draft | Primary body/results retained | 1 narrow, 1 retain |
| JAZF1::PHF1 | Integrated draft | Primary body/results retained | 1 narrow |
| EPC1::PHF1 | Integrated draft | Primary body/results retained | 1 narrow |
| MEAF6::PHF1 | Integrated draft | Primary body/results retained | 1 narrow |
| RUNX1::MECOM | Integrated draft | Primary body/results retained | 1 narrow, 1 retain |
| NPM1::MLF1 | Integrated draft | Primary body/results retained | 1 narrow |
| PTPRZ1::MET | Integrated draft | Primary body/results retained | 2 narrow |
| BCAN::NTRK1 | Integrated draft | Primary body/results retained | 1 narrow, 1 retain |
| QKI::NTRK2 | Integrated draft | Primary body/results retained | 1 narrow, 1 retain |
| NACC2::NTRK2 | Integrated draft | Primary body/results retained | 1 narrow, 1 retain |
| IGH / MYC | Integrated draft | Primary body/results retained | 1 narrow |
| IGK / MYC | Integrated draft | Primary body/results retained | 1 narrow |
| IGL / MYC | Integrated draft | Primary body/results retained | 1 narrow |
| IGH / BCL2 | Integrated draft | Primary body/results retained | 1 narrow, 1 remove |
| IGH / BCL6 | Integrated draft | Primary body/results retained | 1 narrow |
| IGH / CCND1 | Integrated draft | Primary body/results retained | 1 narrow |
| IGH / CCND2 | Integrated draft | Primary body/results retained | 1 narrow |
| IGH / CCND3 | Integrated draft | Primary body/results retained | 1 narrow |
| IGH / MALT1 | Integrated draft | Primary body/results retained | 1 narrow |
| IGH / BCL10 | Integrated draft | Primary body/results retained | 1 narrow |
| IGH / CRLF2 | Integrated draft | Primary body/results retained | 1 retain |
| P2RY8::CRLF2 | Integrated draft | Primary body/results retained | 1 retain |
| IGH / DUX4 | Integrated draft | Primary body/results retained | 1 narrow, 1 remove |
| TCR loci / TAL1 | Integrated draft | Primary body/results retained | 1 narrow |
| TCR loci / TLX1 | Integrated draft | Primary body/results retained | 1 narrow |
| TCR loci / TLX3 | Integrated draft | Primary body/results retained | 1 narrow |
| TCR loci / LMO2 | Integrated draft | Primary body/results retained | 1 narrow |
| GATA2 enhancer / MECOM | Integrated draft | Primary body/results retained | 2 retain |
| IGH / FGFR3 and NSD2 | Integrated draft | Primary body/results retained | 1 narrow |
| IGH / MAF | Integrated draft | Primary body/results retained | 1 narrow |
| IGH / MAFB | Integrated draft | Primary body/results retained | 1 narrow |
| PRCC::TFE3 | Integrated draft | Primary body/results retained | 1 narrow |
| SFPQ::TFE3 | Integrated draft | Primary body/results retained | 1 narrow |
| NONO::TFE3 | Integrated draft | Primary body/results retained | 1 narrow |
| RBM10::TFE3 | Integrated draft | Primary body/results retained | 1 narrow |
| CLTC::TFE3 | Integrated draft | Primary body/results retained | 1 narrow |
| MALAT1::TFEB | Integrated draft | Primary body/results retained | 1 narrow |
