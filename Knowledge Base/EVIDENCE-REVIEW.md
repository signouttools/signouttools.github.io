# Stage-one evidence review — 2026-11-26

Pathologist review needed — LLM-generated summary/review.

**145 previously missing somatic contexts have been assigned. 528 remain pending targeted literature review.** Stage two stays on hold. All 1,133 gene records remain unreviewed drafts.

## What changed

- Common-gene primary-literature updates include DDX41 in myeloid neoplasms, H3-3B in chondroblastoma, MGMT methylation in glioblastoma, CCND2 rearrangements in mantle cell lymphoma, and USP6/CDH11 rearrangements in aneurysmal bone cyst. Further additions cover CDK8, MCL1, BCL2L1, BRIP1, RAD51C, MRE11, EZHIP, IGF2, TERC and broad FGF3/FGF4 amplification context.
- BTK acquired mutations are described in the treatment-associated CLL context, separately from constitutional BTK immunodeficiency. No allele-specific therapy recommendation or new stage-two comment was written.
- The filtered IntOGen compendium supplies additional cohort-level gene–tumor relationships. Every imported row must have IS_DRIVER=True, a combined q-value <0.1, and at least three mutated samples. Gene-level statistical driver evidence does not classify an individual variant. The unfiltered file is not imported; no prevalence estimates are synthesized.
- The IntOGen download is named 20240920, but its archive directory says 2024-06-18 and the README retains a 20230531 header. This version inconsistency is preserved, with SHA256 receipts, rather than silently relabeled.
- Germline assertions were reviewed by condition and inheritance pattern. Breast-cancer naming aliases were reconciled for this review. A disputed claim for one disorder no longer flags every disease association of the gene as contradictory.
- The 59 previously flagged genes have **79 relationship-level editorial decisions**. The source-level decisions withhold expert-disputed/refuted/limited claims and retain separately supported disorders. Four reviewed gene–condition clusters had opposing strong submitter assertions (BRIP1, BTK, COL6A3 and FANCM); the selected condition-specific ClinGen curation controls draft inclusion. These decisions are LLM-assisted source adjudications requiring pathologist review, not new expert-panel verdicts.
- NPM1 now distinguishes published rare constitutional variants from ClinGen's limited marrow-failure classification. TERC describes inherited telomere disease and its associated myeloid risk, rather than presenting AML as a separate Mendelian syndrome. CMMRD labels are normalized for the four mismatch-repair genes.
- The disclaimer is in every gene record, visible entries, document compilations, and clipboard exports. Inline references use PMID links when available and named curation/database references otherwise. No PMID is inferred for a database record.

## What remains open

- **528 genes still need targeted somatic literature review.** They were screened against the qualifying sequence-driver compendium, but absence there does not rule out rare mutations, fusions, copy-number changes, epigenetic mechanisms, or marker-only use. These are still gaps; they are not declared negative associations.
- 632 genes have no retained constitutional association under the current rules. This category includes limited/disputed evidence and genes with no qualifying assertion; absence in the snapshot is not a comprehensive negative literature conclusion.
- The 79 relationship decisions still require a pathologist to review the selected source, phenotype boundaries, and allele mechanism. The original evidence remains in data/evidence.json; the source-selection reasoning is in data/evidence-curation.json.
- No new stage-two comments were generated. The two original examples remain unchanged. data/evidence-curation.json explicitly sets stage_two_ready=false.

## Source receipts and reproduction

data/somatic-cohort-evidence.json retains cohort IDs, original tumor codes and names, q-values, sample counts, research role, sample type, age group, and original cohort publication references. A cohort PMID is sample provenance; the driver analysis is attributed to IntOGen, avoiding a claim that every underlying publication made the same driver call.

Reapply this pass after draft-genes.py with `python3 scripts/curate-evidence.py <draft-input-cache>`. The cache needs gencc.csv, intogen-drivers.zip and intogen-cohorts.zip. The source snapshot hashes are in data/evidence-curation.json. Run `node scripts/validate.mjs` and `python3 scripts/validate-curation.py` afterward. The checked-in individual gene files remain authoritative; gene-index.json must match them.

## Relationship-level decisions

| Gene | Relationship | Selected source classification | Draft decision | Source |
| --- | --- | --- | --- | --- |
| BARD1 | familial ovarian cancer (autosomal dominant) | Disputed Evidence | withhold relationship expert disputed evidence | [ClinGen SGC-106785.2](https://search.clinicalgenome.org/kb/gene-validity/CGGV:assertion_02af8326-360e-4f42-a378-fefff7387d97-2024-08-29T17:00:00.000Z) |
| BLM | breast cancer (autosomal dominant) | Disputed Evidence | withhold unestablished relationship | [Ambry Genetics SGC-102650.1](https://thegencc.org/submissions/SGC-102650.1) |
| BLM | hereditary nonpolyposis colon cancer (autosomal dominant) | Disputed Evidence | withhold unestablished relationship | [Ambry Genetics SGC-103219.1](https://thegencc.org/submissions/SGC-103219.1) |
| BLM | familial colorectal cancer (unknown) | Limited | withhold relationship expert limited | [ClinGen SGC-107206.4](https://search.clinicalgenome.org/kb/gene-validity/CGGV:assertion_37bc882f-34c6-4aea-afea-7b6f037ed9a7-2024-11-22T18:00:00.000Z) |
| BMPR1A | pulmonary arterial hypertension (unknown) | Disputed Evidence | withhold relationship expert disputed evidence | [ClinGen SGC-106241.2](https://search.clinicalgenome.org/kb/gene-validity/CGGV:assertion_e810879d-f635-4851-b20e-86998b000fcc-2022-10-18T16:00:00.000Z) |
| BRAF | Costello syndrome (autosomal dominant) | Disputed Evidence | withhold relationship expert disputed evidence | [ClinGen SGC-104429.4](https://search.clinicalgenome.org/kb/gene-validity/CGGV:assertion_f229eceb-8f5e-4ecb-a484-7863b8dc7d19-2018-07-24T16:00:00.000Z) |
| BRIP1 | hereditary breast carcinoma (autosomal dominant) | Refuted Evidence | withhold relationship expert refuted evidence | [ClinGen SGC-105114.2](https://search.clinicalgenome.org/kb/gene-validity/CGGV:assertion_87aa8181-721b-4583-98cf-0dead1827e27-2023-12-21T18:00:00.000Z) |
| BTK | isolated growth hormone deficiency type III (x-linked) | Disputed Evidence | withhold relationship expert disputed evidence | [ClinGen SGC-106671.2](https://search.clinicalgenome.org/kb/gene-validity/CGGV:assertion_6341781b-9ba9-41b1-889a-8d65a9b3ebb7-2020-11-17T17:00:00.000Z) |
| CHEK2 | familial ovarian cancer (autosomal dominant) | Refuted Evidence | withhold relationship expert refuted evidence | [ClinGen SGC-106787.4](https://search.clinicalgenome.org/kb/gene-validity/CGGV:assertion_9e1071da-cc4a-4bbc-b3fa-4cc07393e74a-2024-11-04T18:00:00.000Z) |
| COL1A2 | congenital heart disease (unknown) | Disputed Evidence | withhold relationship expert disputed evidence | [ClinGen SGC-106926.2](https://search.clinicalgenome.org/kb/gene-validity/CGGV:assertion_b4e87080-7e90-4e19-a3dc-e986bfd01e0f-2024-09-09T16:00:00.000Z) |
| COL6A3 | dystonia 27 (autosomal recessive) | Limited | withhold relationship expert limited | [ClinGen SGC-105205.2](https://search.clinicalgenome.org/kb/gene-validity/CGGV:assertion_8a109763-6fff-4da9-b826-7c2544d3f878-2025-08-25T16:00:00.000Z) |
| EPCAM | hereditary breast carcinoma (autosomal dominant) | Refuted Evidence | withhold relationship expert refuted evidence | [ClinGen SGC-104797.4](https://search.clinicalgenome.org/kb/gene-validity/CGGV:assertion_efe1b152-d818-49bd-9f6f-cebe944b3404-2023-12-21T18:00:00.000Z) |
| ERCC3 | hereditary breast carcinoma (autosomal dominant) | Disputed Evidence | withhold unestablished relationship | [Ambry Genetics SGC-104045.1](https://thegencc.org/submissions/SGC-104045.1) |
| EWSR1 | amyotrophic lateral sclerosis (unknown) | Disputed Evidence | withhold relationship expert disputed evidence | [ClinGen SGC-105469.4](https://search.clinicalgenome.org/kb/gene-validity/CGGV:assertion_4e210cfa-3eb4-4f9b-ad0c-67cfae624029-2022-10-11T16:00:00.000Z) |
| EXO1 | Lynch syndrome (autosomal dominant) | Refuted Evidence | withhold relationship expert refuted evidence | [ClinGen SGC-104861.4](https://search.clinicalgenome.org/kb/gene-validity/CGGV:assertion_3981895c-65e4-4553-9e06-234162704eb4-2023-12-20T18:00:00.000Z) |
| FAAP24 | lymphoproliferative syndrome (autosomal recessive) | Disputed Evidence | withhold relationship expert disputed evidence | [ClinGen SGC-106873.4](https://search.clinicalgenome.org/kb/gene-validity/CGGV:assertion_640890b8-ed2f-46bd-bf07-74e59da80cc2-2024-06-07T16:00:00.000Z) |
| FANCC | breast cancer (autosomal dominant) | Disputed Evidence | withhold unestablished relationship | [Ambry Genetics SGC-102739.1](https://thegencc.org/submissions/SGC-102739.1) |
| FANCC | hereditary breast carcinoma (unknown) | Disputed Evidence | withhold unestablished relationship | [Natera SGC-179950.1](https://thegencc.org/submissions/SGC-179950.1) |
| FANCM | breast cancer (autosomal dominant) | Limited | withhold relationship expert limited | [ClinGen SGC-107119.2](https://search.clinicalgenome.org/kb/gene-validity/CGGV:assertion_25744c57-8e53-403b-a2ec-fb405ad452cc-2024-11-22T18:00:00.000Z) |
| FANCM | Fanconi anemia (autosomal recessive) | Refuted Evidence | withhold relationship expert refuted evidence | [ClinGen SGC-107144.2](https://search.clinicalgenome.org/kb/gene-validity/CGGV:assertion_28865445-bea0-42c1-8f50-fae94e93f1d8-2024-12-10T17:00:00.000Z) |
| FOXI1 | enlarged vestibular aqueduct syndrome (autosomal recessive) | Disputed Evidence | withhold relationship expert disputed evidence | [ClinGen SGC-104692.2](https://search.clinicalgenome.org/kb/gene-validity/CGGV:assertion_d3a6b8fa-01d1-4f32-a45e-9c9582e14280-2018-02-27T17:00:00.000Z) |
| FOXP1 | congenital heart disease (autosomal dominant) | Disputed Evidence | withhold relationship expert disputed evidence | [ClinGen SGC-105507.4](https://search.clinicalgenome.org/kb/gene-validity/CGGV:assertion_e0d2a272-afc2-49df-aa73-0b2f82ce11d6-2023-12-11T17:00:00.000Z) |
| GEN1 | hereditary breast carcinoma (autosomal dominant) | Refuted Evidence | withhold relationship expert refuted evidence | [ClinGen SGC-105283.2](https://search.clinicalgenome.org/kb/gene-validity/CGGV:assertion_b8a2aec0-413b-41f2-ba51-e8a71e52cf1a-2023-12-21T18:00:00.000Z) |
| HDAC1 | congenital heart disease (autosomal dominant) | Disputed Evidence | withhold relationship expert disputed evidence | [ClinGen SGC-105833.2](https://search.clinicalgenome.org/kb/gene-validity/CGGV:assertion_736390a5-ec08-4a25-b6ce-0d70dae98811-2024-01-08T17:00:00.000Z) |
| HEY1 | congenital heart disease (autosomal dominant) | Disputed Evidence | withhold relationship expert disputed evidence | [ClinGen SGC-107303.4](https://search.clinicalgenome.org/kb/gene-validity/CGGV:assertion_634df453-b9c6-4b52-afc0-516603ef90d0-2024-08-06T16:00:00.000Z) |
| HRAS | Noonan syndrome-like disorder with loose anagen hair (autosomal dominant) | Disputed Evidence | withhold relationship expert disputed evidence | [ClinGen SGC-104877.4](https://search.clinicalgenome.org/kb/gene-validity/CGGV:assertion_94630309-c540-48b3-a27f-0ee1891091c1-2018-07-25T16:00:00.000Z) |
| KAT6B | RASopathy (autosomal dominant) | Disputed Evidence | withhold relationship expert disputed evidence | [ClinGen SGC-105885.2](https://search.clinicalgenome.org/kb/gene-validity/CGGV:assertion_fb3c40d8-3aea-45bf-949e-c3ba7d96a6b4-2019-02-04T17:00:00.000Z) |
| KCNQ1 | hypertrophic cardiomyopathy (autosomal dominant) | Disputed Evidence | withhold relationship expert disputed evidence | [ClinGen SGC-105449.4](https://search.clinicalgenome.org/kb/gene-validity/CGGV:assertion_5b44eee3-56ea-4596-8d3e-e4d5c0ad8d60-2022-05-09T16:00:00.000Z) |
| KCNQ1 | familial hypertrophic cardiomyopathy (autosomal dominant) | Disputed Evidence | withhold unestablished relationship | [G2P SGC-180440.1](https://www.ebi.ac.uk/gene2phenotype/lgd/G2P03882) |
| KIF1B | Charcot-Marie-Tooth disease type 2A1 (autosomal dominant) | Disputed Evidence | withhold relationship expert disputed evidence | [ClinGen SGC-106632.4](https://search.clinicalgenome.org/kb/gene-validity/CGGV:assertion_ae6ffeae-9609-47bf-89a9-4863cf6ef05c-2026-10-19T16:00:00.000Z) |
| KRAS | Costello syndrome (autosomal dominant) | Disputed Evidence | withhold relationship expert disputed evidence | [ClinGen SGC-104941.4](https://search.clinicalgenome.org/kb/gene-validity/CGGV:assertion_bc9a82d0-8447-454c-8d54-def792d20e1d-2018-07-24T16:00:00.000Z) |
| MAGI2 | epilepsy (autosomal dominant) | Refuted Evidence | withhold relationship expert refuted evidence | [ClinGen SGC-104666.4](https://search.clinicalgenome.org/kb/gene-validity/CGGV:assertion_7d622b88-9c77-47f8-93b1-808517da0cff-2023-10-17T19:00:00.000Z) |
| MAP2K1 | Costello syndrome (autosomal dominant) | Disputed Evidence | withhold relationship expert disputed evidence | [ClinGen SGC-104469.2](https://search.clinicalgenome.org/kb/gene-validity/CGGV:assertion_8d28301c-df25-4c10-9edb-34be26f2838d-2018-07-24T16:00:00.000Z) |
| MET | complex neurodevelopmental disorder (autosomal dominant) | Disputed Evidence | withhold relationship expert disputed evidence | [ClinGen SGC-106628.4](https://search.clinicalgenome.org/kb/gene-validity/CGGV:assertion_d55c61af-ef8e-475d-9ff7-454496cb6462-2021-01-19T17:00:00.000Z) |
| MLH1 | breast cancer (autosomal dominant) | Refuted Evidence | withhold relationship expert refuted evidence | [ClinGen SGC-105554.2](https://search.clinicalgenome.org/kb/gene-validity/CGGV:assertion_c27a22e4-fc45-4888-8b1d-625bc649697c-2023-12-21T18:00:00.000Z) |
| MRE11 | prostate cancer (autosomal dominant) | Disputed Evidence | withhold unestablished relationship | [Ambry Genetics SGC-103475.1](https://thegencc.org/submissions/SGC-103475.1) |
| MRE11 | breast cancer (autosomal dominant) | Refuted Evidence | withhold relationship expert refuted evidence | [ClinGen SGC-105247.4](https://search.clinicalgenome.org/kb/gene-validity/CGGV:assertion_e720d1f7-62b3-4a0f-97de-e1144d0475a9-2023-03-14T17:00:00.000Z) |
| MRE11 | familial ovarian cancer (autosomal dominant) | Refuted Evidence | withhold relationship expert refuted evidence | [ClinGen SGC-104981.4](https://search.clinicalgenome.org/kb/gene-validity/CGGV:assertion_f5b721c7-52ab-4475-a87e-cb0fa3be198f-2023-12-15T18:00:00.000Z) |
| MSH2 | breast cancer (autosomal dominant) | Refuted Evidence | withhold relationship expert refuted evidence | [ClinGen SGC-104946.4](https://search.clinicalgenome.org/kb/gene-validity/CGGV:assertion_9cb3ff3b-3e0e-42f2-85d5-3ffb1506a255-2023-03-14T17:00:00.000Z) |
| MSH3 | Lynch syndrome (autosomal dominant) | Disputed Evidence | withhold relationship expert disputed evidence | [ClinGen SGC-105598.2](https://search.clinicalgenome.org/kb/gene-validity/CGGV:assertion_e9216399-2779-43fa-8b95-b10020753f43-2024-08-29T17:00:00.000Z) |
| MSH6 | hereditary breast carcinoma (autosomal dominant) | Disputed Evidence | withhold relationship expert disputed evidence | [ClinGen SGC-106606.4](https://search.clinicalgenome.org/kb/gene-validity/CGGV:assertion_d3c3cce5-7d58-4800-a956-e83c092071de-2023-12-21T18:00:00.000Z) |
| MUTYH | hereditary breast carcinoma (autosomal recessive) | Disputed Evidence | withhold relationship expert disputed evidence | [ClinGen SGC-104323.2](https://search.clinicalgenome.org/kb/gene-validity/CGGV:assertion_73e67e8c-0d12-44b1-a0d7-9fcc459b6773-2023-12-21T18:00:00.000Z) |
| MUTYH | familial ovarian cancer (autosomal dominant) | Disputed Evidence | withhold relationship expert disputed evidence | [ClinGen SGC-105521.2](https://search.clinicalgenome.org/kb/gene-validity/CGGV:assertion_2c329a2e-94fd-4719-a47b-a71cc9b39eec-2023-12-20T18:00:00.000Z) |
| MUTYH | hereditary breast carcinoma (autosomal dominant) | Refuted Evidence | withhold relationship expert refuted evidence | [ClinGen SGC-105964.2](https://search.clinicalgenome.org/kb/gene-validity/CGGV:assertion_b818b8fc-7453-46be-8636-08644fd7a1d4-2023-12-21T18:00:00.000Z) |
| MUTYH | colorectal cancer (autosomal dominant) | Disputed Evidence | withhold relationship expert disputed evidence | [ClinGen SGC-106189.4](https://search.clinicalgenome.org/kb/gene-validity/CGGV:assertion_b646b303-fb30-427c-9590-242a131624bf-2023-03-24T05:00:00.000Z) |
| MUTYH | familial ovarian cancer (autosomal recessive) | Disputed Evidence | withhold relationship expert disputed evidence | [ClinGen SGC-106686.4](https://search.clinicalgenome.org/kb/gene-validity/CGGV:assertion_2842036e-4a06-4d05-bce0-846f0f3c1678-2023-12-20T18:00:00.000Z) |
| NBN | hereditary breast carcinoma (autosomal dominant) | Refuted Evidence | withhold relationship expert refuted evidence | [ClinGen SGC-105618.4](https://search.clinicalgenome.org/kb/gene-validity/CGGV:assertion_fc101ed8-f6ae-49b8-8850-384da62eb9b9-2023-03-14T17:00:00.000Z) |
| NBN | hereditary breast carcinoma (unknown) | Refuted Evidence | withhold relationship expert refuted evidence | [ClinGen SGC-105618.4](https://search.clinicalgenome.org/kb/gene-validity/CGGV:assertion_fc101ed8-f6ae-49b8-8850-384da62eb9b9-2023-03-14T17:00:00.000Z) |
| NEIL3 | autoimmune disease (autosomal recessive) | Disputed Evidence | withhold relationship expert disputed evidence | [ClinGen SGC-179649.1](https://search.clinicalgenome.org/kb/gene-validity/CGGV:assertion_619e35d5-2e3a-4d83-8f0d-e8a6a696b9cf-2025-12-17T17:00:00.000Z) |
| NFATC2 | congenital heart disease (autosomal dominant) | Disputed Evidence | withhold relationship expert disputed evidence | [ClinGen SGC-104715.3](https://search.clinicalgenome.org/kb/gene-validity/CGGV:assertion_6f22ef84-1ac1-412a-a134-bbe7617cf47f-2024-03-11T05:00:00.000Z) |
| NOTCH3 | pulmonary arterial hypertension (autosomal dominant) | Disputed Evidence | withhold relationship expert disputed evidence | [ClinGen SGC-104296.4](https://search.clinicalgenome.org/kb/gene-validity/CGGV:assertion_d59e2823-a923-4c3e-8976-c3451eaa8666-2022-11-03T16:00:00.000Z) |
| NTRK3 | congenital heart disease (autosomal dominant) | Disputed Evidence | withhold relationship expert disputed evidence | [ClinGen SGC-105811.2](https://search.clinicalgenome.org/kb/gene-validity/CGGV:assertion_7ec69048-b11f-41f5-b160-c184ae1d65e6-2024-02-06T17:00:00.000Z) |
| PIK3CA | hereditary breast carcinoma (autosomal dominant) | Refuted Evidence | withhold relationship expert refuted evidence | [ClinGen SGC-104409.4](https://search.clinicalgenome.org/kb/gene-validity/CGGV:assertion_7ce3540a-5a7f-4f47-aeb3-520767016539-2023-12-21T18:00:00.000Z) |
| PLAGL1 | congenital heart disease (autosomal dominant) | Disputed Evidence | withhold relationship expert disputed evidence | [ClinGen SGC-190020.1](https://search.clinicalgenome.org/kb/gene-validity/CGGV:assertion_87f9f6f7-be31-4f75-a3d5-0d0d82b7f481-2026-08-04T16:00:00.000Z) |
| PMS1 | Lynch syndrome (autosomal dominant) | Refuted Evidence | withhold relationship expert refuted evidence | [ClinGen SGC-106101.4](https://search.clinicalgenome.org/kb/gene-validity/CGGV:assertion_7aa5e58f-5778-4b62-9279-a3da77ca79c0-2023-12-20T18:00:00.000Z) |
| PMS2 | hereditary breast carcinoma (autosomal dominant) | Disputed Evidence | withhold relationship expert disputed evidence | [ClinGen SGC-106365.4](https://search.clinicalgenome.org/kb/gene-validity/CGGV:assertion_308d8362-7bd9-46a7-b2fa-ab8f671a44c9-2023-12-21T18:00:00.000Z) |
| PPM1D | hereditary breast carcinoma (autosomal dominant) | Disputed Evidence | withhold unestablished relationship | [Ambry Genetics SGC-101746.1](https://thegencc.org/submissions/SGC-101746.1) |
| PTPN11 | cardiofaciocutaneous syndrome (autosomal dominant) | Disputed Evidence | withhold relationship expert disputed evidence | [ClinGen SGC-104968.4](https://search.clinicalgenome.org/kb/gene-validity/CGGV:assertion_a1a2133e-4ce8-45b7-87da-1c52990d3890-2018-05-30T16:00:00.000Z) |
| PTPN11 | Costello syndrome (autosomal dominant) | Disputed Evidence | withhold relationship expert disputed evidence | [ClinGen SGC-106504.2](https://search.clinicalgenome.org/kb/gene-validity/CGGV:assertion_72fca24b-243b-49de-9ceb-ae76e12f60a8-2018-05-31T16:00:00.000Z) |
| RAD50 | hereditary breast carcinoma (autosomal dominant) | Refuted Evidence | withhold relationship expert refuted evidence | [ClinGen SGC-104250.2](https://search.clinicalgenome.org/kb/gene-validity/CGGV:assertion_1f16b58f-c6b5-45ef-bb4a-a9fa5fe8ac35-2023-03-14T17:00:00.000Z) |
| RAD50 | familial ovarian cancer (autosomal dominant) | Refuted Evidence | withhold relationship expert refuted evidence | [ClinGen SGC-105228.4](https://search.clinicalgenome.org/kb/gene-validity/CGGV:assertion_ef809b24-cdc2-4d5c-a1ab-5a9c2f35da54-2024-02-23T18:00:00.000Z) |
| RAF1 | cardiofaciocutaneous syndrome (autosomal dominant) | Disputed Evidence | withhold relationship expert disputed evidence | [ClinGen SGC-104394.4](https://search.clinicalgenome.org/kb/gene-validity/CGGV:assertion_b1e7c802-14d7-435c-b396-637b728a3ae2-2018-05-31T16:00:00.000Z) |
| RAF1 | Costello syndrome (autosomal dominant) | Disputed Evidence | withhold relationship expert disputed evidence | [ClinGen SGC-105929.4](https://search.clinicalgenome.org/kb/gene-validity/CGGV:assertion_67081421-a4a3-4b62-88e0-4a78d19859ba-2018-07-24T16:00:00.000Z) |
| RASA1 | Noonan syndrome (autosomal dominant) | Disputed Evidence | withhold relationship expert disputed evidence | [ClinGen SGC-105893.4](https://search.clinicalgenome.org/kb/gene-validity/CGGV:assertion_a957c2df-eeec-4bdf-b423-6f1667f66abd-2018-06-07T16:00:00.000Z) |
| RECQL | breast cancer (autosomal dominant) | Disputed Evidence | withhold relationship expert disputed evidence | [ClinGen SGC-106679.4](https://search.clinicalgenome.org/kb/gene-validity/CGGV:assertion_777b2a5c-459f-4eee-8a6d-e8bf15b88aca-2023-03-13T17:00:00.000Z) |
| RINT1 | breast cancer (autosomal dominant) | Refuted Evidence | withhold relationship expert refuted evidence | [ClinGen SGC-105032.2](https://search.clinicalgenome.org/kb/gene-validity/CGGV:assertion_d523910c-67e4-4cec-82a2-d7803957ec02-2023-03-14T17:00:00.000Z) |
| SAMHD1 | chilblain lupus (autosomal dominant) | Disputed Evidence | withhold unestablished relationship | [Illumina SGC-109045.1](https://thegencc.org/submissions/SGC-109045.1) |
| SHOC2 | Noonan syndrome (autosomal dominant) | Disputed Evidence | withhold relationship expert disputed evidence | [ClinGen SGC-105690.4](https://search.clinicalgenome.org/kb/gene-validity/CGGV:assertion_185c93c8-e875-46a2-83af-a8575b19a228-2018-05-31T16:00:00.000Z) |
| SHOC2 | cardiofaciocutaneous syndrome (autosomal dominant) | Disputed Evidence | withhold relationship expert disputed evidence | [ClinGen SGC-106377.4](https://search.clinicalgenome.org/kb/gene-validity/CGGV:assertion_fd8e5069-4023-4763-9b41-03350b03ee7f-2018-06-01T16:00:00.000Z) |
| SHOC2 | Costello syndrome (autosomal dominant) | Disputed Evidence | withhold relationship expert disputed evidence | [ClinGen SGC-106626.4](https://search.clinicalgenome.org/kb/gene-validity/CGGV:assertion_a7035ea3-d556-4aa4-b525-5ed6c02866df-2018-07-24T16:00:00.000Z) |
| SLMAP | Brugada syndrome (autosomal dominant) | Refuted Evidence | withhold relationship expert refuted evidence | [ClinGen SGC-106708.2](https://search.clinicalgenome.org/kb/gene-validity/CGGV:assertion_3adfefec-eda0-4991-a0dc-8b83f274ccdf-2026-01-15T01:00:00.000Z) |
| SLX4 | hereditary breast carcinoma (autosomal dominant) | Refuted Evidence | withhold relationship expert refuted evidence | [ClinGen SGC-105707.4](https://search.clinicalgenome.org/kb/gene-validity/CGGV:assertion_4acc26ec-2174-4b21-bb02-965ae3539062-2023-12-21T18:00:00.000Z) |
| SMAD4 | pulmonary arterial hypertension (autosomal dominant) | Disputed Evidence | withhold relationship expert disputed evidence | [ClinGen SGC-105392.4](https://search.clinicalgenome.org/kb/gene-validity/CGGV:assertion_12d82f9f-8ab2-4012-a5d5-20de99f23c07-2022-11-21T17:00:00.000Z) |
| SOS1 | cardiofaciocutaneous syndrome (autosomal dominant) | Disputed Evidence | withhold relationship expert disputed evidence | [ClinGen SGC-105048.4](https://search.clinicalgenome.org/kb/gene-validity/CGGV:assertion_ee5b916f-82ef-4738-82c8-46ee2fad131b-2018-06-01T16:00:00.000Z) |
| SOS1 | Costello syndrome (autosomal dominant) | Disputed Evidence | withhold relationship expert disputed evidence | [ClinGen SGC-106556.4](https://search.clinicalgenome.org/kb/gene-validity/CGGV:assertion_cf0ea291-849a-4bd9-a12a-cd9daad7e214-2018-07-24T16:00:00.000Z) |
| VCL | hypertrophic cardiomyopathy (autosomal dominant) | Disputed Evidence | withhold relationship expert disputed evidence | [ClinGen SGC-104283.4](https://search.clinicalgenome.org/kb/gene-validity/CGGV:assertion_27365fd2-1203-4e2b-8830-3277e965d8bc-2023-05-10T16:00:00.000Z) |
| VCL | hypertrophic cardiomyopathy 15 (autosomal dominant) | Disputed Evidence | withhold unestablished relationship | [PanelApp Australia SGC-178029.1](https://panelapp-aus.org) |
| VCL | familial hypertrophic cardiomyopathy (autosomal dominant) | Disputed Evidence | withhold unestablished relationship | [G2P SGC-180423.1](https://www.ebi.ac.uk/gene2phenotype/lgd/G2P03864) |
| XRCC2 | breast cancer (autosomal dominant) | Refuted Evidence | withhold relationship expert refuted evidence | [ClinGen SGC-105346.2](https://search.clinicalgenome.org/kb/gene-validity/CGGV:assertion_f7f253e9-bb78-44c5-bab1-6e8017eeb69c-2023-03-14T17:00:00.000Z) |

## Remaining somatic review queue

Sorted by panel-family recurrence and educational coverage so common candidates are reviewed first. This priority is editorial, not a clinical evidence grade.

| Gene | Panel families | Review status |
| --- | ---: | --- |
| BLM | 4 | Targeted literature review pending |
| BARD1 | 4 | Targeted literature review pending |
| CHEK1 | 4 | Targeted literature review pending |
| ETV4 | 4 | Targeted literature review pending |
| FANCA | 4 | Targeted literature review pending |
| FANCC | 4 | Targeted literature review pending |
| FANCG | 4 | Targeted literature review pending |
| FANCL | 4 | Targeted literature review pending |
| NOTCH3 | 4 | Targeted literature review pending |
| AKT2 | 4 | Targeted literature review pending |
| AURKB | 4 | Targeted literature review pending |
| AXL | 4 | Targeted literature review pending |
| CRKL | 4 | Targeted literature review pending |
| DDR2 | 4 | Targeted literature review pending |
| ETV5 | 4 | Targeted literature review pending |
| FANCD2 | 4 | Targeted literature review pending |
| FANCE | 4 | Targeted literature review pending |
| FANCF | 4 | Targeted literature review pending |
| FLT1 | 4 | Targeted literature review pending |
| IGF1R | 4 | Targeted literature review pending |
| KDM5A | 4 | Targeted literature review pending |
| MAP2K2 | 4 | Targeted literature review pending |
| MITF | 4 | Targeted literature review pending |
| PRKCI | 4 | Targeted literature review pending |
| PRKN | 4 | Targeted literature review pending |
| RAD51 | 4 | Targeted literature review pending |
| RICTOR | 4 | Targeted literature review pending |
| RPTOR | 4 | Targeted literature review pending |
| VEGFA | 4 | Targeted literature review pending |
| EPCAM | 3 | Targeted literature review pending |
| GSK3B | 3 | Targeted literature review pending |
| H3C3 | 3 | Targeted literature review pending |
| HOXB13 | 3 | Targeted literature review pending |
| NBN | 3 | Targeted literature review pending |
| RAD51D | 3 | Targeted literature review pending |
| RHEB | 3 | Targeted literature review pending |
| ABRAXAS1 | 3 | Targeted literature review pending |
| CD79A | 3 | Targeted literature review pending |
| CTNNA1 | 3 | Targeted literature review pending |
| EPHA5 | 3 | Targeted literature review pending |
| EPHB1 | 3 | Targeted literature review pending |
| ERCC4 | 3 | Targeted literature review pending |
| ERCC5 | 3 | Targeted literature review pending |
| ERRFI1 | 3 | Targeted literature review pending |
| FANCI | 3 | Targeted literature review pending |
| GREM1 | 3 | Targeted literature review pending |
| INHBA | 3 | Targeted literature review pending |
| INPP4B | 3 | Targeted literature review pending |
| IRS2 | 3 | Targeted literature review pending |
| JUN | 3 | Targeted literature review pending |
| NKX3-1 | 3 | Targeted literature review pending |
| NUP93 | 3 | Targeted literature review pending |
| PHOX2B | 3 | Targeted literature review pending |
| PIK3C2B | 3 | Targeted literature review pending |
| PIK3CG | 3 | Targeted literature review pending |
| PIK3R2 | 3 | Targeted literature review pending |
| PLCG2 | 3 | Targeted literature review pending |
| PMS1 | 3 | Targeted literature review pending |
| PRKDC | 3 | Targeted literature review pending |
| RAD52 | 3 | Targeted literature review pending |
| RECQL4 | 3 | Targeted literature review pending |
| SH2D1A | 3 | Targeted literature review pending |
| SLX4 | 3 | Targeted literature review pending |
| SMC3 | 3 | Targeted literature review pending |
| SRC | 3 | Targeted literature review pending |
| XRCC2 | 3 | Targeted literature review pending |
| ZNF217 | 3 | Targeted literature review pending |
| ANKRD26 | 2 | Targeted literature review pending |
| RAD51B | 2 | Targeted literature review pending |
| SOX10 | 2 | Targeted literature review pending |
| FGF23 | 2 | Targeted literature review pending |
| FYN | 2 | Targeted literature review pending |
| RAD54L | 2 | Targeted literature review pending |
| SBDS | 2 | Targeted literature review pending |
| SMARCE1 | 2 | Targeted literature review pending |
| STAT5A | 2 | Targeted literature review pending |
| ADGRA2 | 2 | Targeted literature review pending |
| ALOX12B | 2 | Targeted literature review pending |
| ARFRP1 | 2 | Targeted literature review pending |
| ARID5B | 2 | Targeted literature review pending |
| BABAM1 | 2 | Targeted literature review pending |
| BBC3 | 2 | Targeted literature review pending |
| BCL2L11 | 2 | Targeted literature review pending |
| BCL2L2 | 2 | Targeted literature review pending |
| CCN6 | 2 | Targeted literature review pending |
| CD276 | 2 | Targeted literature review pending |
| CENPA | 2 | Targeted literature review pending |
| COP1 | 2 | Targeted literature review pending |
| DCUN1D1 | 2 | Targeted literature review pending |
| DNMT1 | 2 | Targeted literature review pending |
| DNMT3B | 2 | Targeted literature review pending |
| EGFL7 | 2 | Targeted literature review pending |
| EIF4E | 2 | Targeted literature review pending |
| EMSY | 2 | Targeted literature review pending |
| ERCC1 | 2 | Targeted literature review pending |
| FANCM | 2 | Targeted literature review pending |
| FGF10 | 2 | Targeted literature review pending |
| FGF14 | 2 | Targeted literature review pending |
| FGF6 | 2 | Targeted literature review pending |
| FRS2 | 2 | Targeted literature review pending |
| GABRA6 | 2 | Targeted literature review pending |
| GEN1 | 2 | Targeted literature review pending |
| GID4 | 2 | Targeted literature review pending |
| GPS2 | 2 | Targeted literature review pending |
| H1-2 | 2 | Targeted literature review pending |
| H2BC5 | 2 | Targeted literature review pending |
| H3-4 | 2 | Targeted literature review pending |
| H3-5 | 2 | Targeted literature review pending |
| H3C1 | 2 | Targeted literature review pending |
| H3C10 | 2 | Targeted literature review pending |
| H3C11 | 2 | Targeted literature review pending |
| H3C12 | 2 | Targeted literature review pending |
| H3C13 | 2 | Targeted literature review pending |
| H3C14 | 2 | Targeted literature review pending |
| H3C4 | 2 | Targeted literature review pending |
| H3C6 | 2 | Targeted literature review pending |
| H3C7 | 2 | Targeted literature review pending |
| H3C8 | 2 | Targeted literature review pending |
| HSD3B1 | 2 | Targeted literature review pending |
| HSP90AA1 | 2 | Targeted literature review pending |
| ICOSLG | 2 | Targeted literature review pending |
| IFNGR1 | 2 | Targeted literature review pending |
| IGF1 | 2 | Targeted literature review pending |
| IL10 | 2 | Targeted literature review pending |
| INHA | 2 | Targeted literature review pending |
| INPP4A | 2 | Targeted literature review pending |
| INSR | 2 | Targeted literature review pending |
| IRF2 | 2 | Targeted literature review pending |
| IRS1 | 2 | Targeted literature review pending |
| KEL | 2 | Targeted literature review pending |
| MAGI2 | 2 | Targeted literature review pending |
| MAP3K13 | 2 | Targeted literature review pending |
| MAP3K14 | 2 | Targeted literature review pending |
| MAPK3 | 2 | Targeted literature review pending |
| MDC1 | 2 | Targeted literature review pending |
| MSH3 | 2 | Targeted literature review pending |
| MST1 | 2 | Targeted literature review pending |
| MST1R | 2 | Targeted literature review pending |
| NEGR1 | 2 | Targeted literature review pending |
| NOTCH4 | 2 | Targeted literature review pending |
| NT5C2 | 2 | Targeted literature review pending |
| NTHL1 | 2 | Targeted literature review pending |
| PAK1 | 2 | Targeted literature review pending |
| PAK3 | 2 | Targeted literature review pending |
| PAK5 | 2 | Targeted literature review pending |
| PARP1 | 2 | Targeted literature review pending |
| PDCD1 | 2 | Targeted literature review pending |
| PDK1 | 2 | Targeted literature review pending |
| PDPK1 | 2 | Targeted literature review pending |
| PGR | 2 | Targeted literature review pending |
| PIK3C2G | 2 | Targeted literature review pending |
| PIK3C3 | 2 | Targeted literature review pending |
| PIK3CD | 2 | Targeted literature review pending |
| PIK3R3 | 2 | Targeted literature review pending |
| PLK2 | 2 | Targeted literature review pending |
| PMAIP1 | 2 | Targeted literature review pending |
| PNRC1 | 2 | Targeted literature review pending |
| PRSS8 | 2 | Targeted literature review pending |
| PTPRS | 2 | Targeted literature review pending |
| RAB35 | 2 | Targeted literature review pending |
| RPS6KA4 | 2 | Targeted literature review pending |
| RPS6KB2 | 2 | Targeted literature review pending |
| RYBP | 2 | Targeted literature review pending |
| SHQ1 | 2 | Targeted literature review pending |
| SLIT2 | 2 | Targeted literature review pending |
| SMARCD1 | 2 | Targeted literature review pending |
| SNCAIP | 2 | Targeted literature review pending |
| SPTA1 | 2 | Targeted literature review pending |
| STAG1 | 2 | Targeted literature review pending |
| STAT4 | 2 | Targeted literature review pending |
| STK40 | 2 | Targeted literature review pending |
| TAF1 | 2 | Targeted literature review pending |
| TP53BP1 | 2 | Targeted literature review pending |
| TRAF2 | 2 | Targeted literature review pending |
| VTCN1 | 2 | Targeted literature review pending |
| XIAP | 2 | Targeted literature review pending |
| YES1 | 2 | Targeted literature review pending |
| ZBTB2 | 2 | Targeted literature review pending |
| ZNF703 | 2 | Targeted literature review pending |
| ATP6AP1 | 1 | Targeted literature review pending |
| EGR1 | 1 | Targeted literature review pending |
| FANCB | 1 | Targeted literature review pending |
| FGF8 | 1 | Targeted literature review pending |
| MBD4 | 1 | Targeted literature review pending |
| MLLT1 | 1 | Targeted literature review pending |
| MYBBP1A | 1 | Targeted literature review pending |
| NFE2 | 1 | Targeted literature review pending |
| PPP2R2A | 1 | Targeted literature review pending |
| ROBO1 | 1 | Targeted literature review pending |
| RTEL1 | 1 | Targeted literature review pending |
| SRP72 | 1 | Targeted literature review pending |
| ABCB11 | 1 | Targeted literature review pending |
| ACTG1 | 1 | Targeted literature review pending |
| AGO1 | 1 | Targeted literature review pending |
| AGO2 | 1 | Targeted literature review pending |
| ALB | 1 | Targeted literature review pending |
| APLNR | 1 | Targeted literature review pending |
| ARHGEF28 | 1 | Targeted literature review pending |
| ARID3A | 1 | Targeted literature review pending |
| ARID3B | 1 | Targeted literature review pending |
| ARID3C | 1 | Targeted literature review pending |
| ARID4A | 1 | Targeted literature review pending |
| ARID4B | 1 | Targeted literature review pending |
| ARID5A | 1 | Targeted literature review pending |
| ATP6V1B2 | 1 | Targeted literature review pending |
| ATXN2 | 1 | Targeted literature review pending |
| ATXN7 | 1 | Targeted literature review pending |
| BABAM2 | 1 | Targeted literature review pending |
| BACH2 | 1 | Targeted literature review pending |
| BCL2L12 | 1 | Targeted literature review pending |
| BRCC3 | 1 | Targeted literature review pending |
| BUB1B | 1 | Targeted literature review pending |
| CARM1 | 1 | Targeted literature review pending |
| CCNQ | 1 | Targeted literature review pending |
| CD70 | 1 | Targeted literature review pending |
| CDC42 | 1 | Targeted literature review pending |
| CDH4 | 1 | Targeted literature review pending |
| CDKN1C | 1 | Targeted literature review pending |
| CDKN2B-AS1 | 1 | Targeted literature review pending |
| COL7A1 | 1 | Targeted literature review pending |
| CRBN | 1 | Targeted literature review pending |
| CSDE1 | 1 | Targeted literature review pending |
| CSNK1A1 | 1 | Targeted literature review pending |
| CTR9 | 1 | Targeted literature review pending |
| CYP19A1 | 1 | Targeted literature review pending |
| DCLRE1C | 1 | Targeted literature review pending |
| DDB1 | 1 | Targeted literature review pending |
| DHX15 | 1 | Targeted literature review pending |
| DIS3L2 | 1 | Targeted literature review pending |
| DKC1 | 1 | Targeted literature review pending |
| DMC1 | 1 | Targeted literature review pending |
| DOCK8 | 1 | Targeted literature review pending |
| DUSP4 | 1 | Targeted literature review pending |
| EGLN1 | 1 | Targeted literature review pending |
| ELANE | 1 | Targeted literature review pending |
| EME1 | 1 | Targeted literature review pending |
| ENG | 1 | Targeted literature review pending |
| ERCC6 | 1 | Targeted literature review pending |
| ERF | 1 | Targeted literature review pending |
| ESCO2 | 1 | Targeted literature review pending |
| ETAA1 | 1 | Targeted literature review pending |
| ETS1 | 1 | Targeted literature review pending |
| EXO1 | 1 | Targeted literature review pending |
| EXOSC6 | 1 | Targeted literature review pending |
| EZH1 | 1 | Targeted literature review pending |
| FAAP100 | 1 | Targeted literature review pending |
| FAAP20 | 1 | Targeted literature review pending |
| FAAP24 | 1 | Targeted literature review pending |
| FAF1 | 1 | Targeted literature review pending |
| FAH | 1 | Targeted literature review pending |
| FAN1 | 1 | Targeted literature review pending |
| FGF2 | 1 | Targeted literature review pending |
| FGF5 | 1 | Targeted literature review pending |
| FGF7 | 1 | Targeted literature review pending |
| FGF9 | 1 | Targeted literature review pending |
| FOXF1 | 1 | Targeted literature review pending |
| FURIN | 1 | Targeted literature review pending |
| GAB1 | 1 | Targeted literature review pending |
| GAB2 | 1 | Targeted literature review pending |
| GALNT12 | 1 | Targeted literature review pending |
| GBA1 | 1 | Targeted literature review pending |
| GNA12 | 1 | Targeted literature review pending |
| GNB1 | 1 | Targeted literature review pending |
| GPC3 | 1 | Targeted literature review pending |
| H1-3 | 1 | Targeted literature review pending |
| H1-4 | 1 | Targeted literature review pending |
| H1-5 | 1 | Targeted literature review pending |
| H2AC11 | 1 | Targeted literature review pending |
| H2AC16 | 1 | Targeted literature review pending |
| H2AC17 | 1 | Targeted literature review pending |
| H2AC6 | 1 | Targeted literature review pending |
| H2BC11 | 1 | Targeted literature review pending |
| H2BC12 | 1 | Targeted literature review pending |
| H2BC17 | 1 | Targeted literature review pending |
| H2BC4 | 1 | Targeted literature review pending |
| H2BC8 | 1 | Targeted literature review pending |
| H3C15 | 1 | Targeted literature review pending |
| HABP2 | 1 | Targeted literature review pending |
| HDAC1 | 1 | Targeted literature review pending |
| HDAC7 | 1 | Targeted literature review pending |
| HELQ | 1 | Targeted literature review pending |
| HFE | 1 | Targeted literature review pending |
| HIF1A | 1 | Targeted literature review pending |
| HMBS | 1 | Targeted literature review pending |
| HNRNPK | 1 | Targeted literature review pending |
| ID4 | 1 | Targeted literature review pending |
| ITPKB | 1 | Targeted literature review pending |
| JARID2 | 1 | Targeted literature review pending |
| KCNQ1 | 1 | Targeted literature review pending |
| KIF1B | 1 | Targeted literature review pending |
| KLLN | 1 | Targeted literature review pending |
| KSR2 | 1 | Targeted literature review pending |
| LAMP1 | 1 | Targeted literature review pending |
| LCK | 1 | Targeted literature review pending |
| LIG4 | 1 | Targeted literature review pending |
| LTB | 1 | Targeted literature review pending |
| MAD2L2 | 1 | Targeted literature review pending |
| MAP3K4 | 1 | Targeted literature review pending |
| MAP3K6 | 1 | Targeted literature review pending |
| MAP3K7 | 1 | Targeted literature review pending |
| MAPKAP1 | 1 | Targeted literature review pending |
| MCM8 | 1 | Targeted literature review pending |
| MGAM | 1 | Targeted literature review pending |
| MIB1 | 1 | Targeted literature review pending |
| MKI67 | 1 | Targeted literature review pending |
| MLH3 | 1 | Targeted literature review pending |
| MOB3B | 1 | Targeted literature review pending |
| MPEG1 | 1 | Targeted literature review pending |
| MSI1 | 1 | Targeted literature review pending |
| MTA1 | 1 | Targeted literature review pending |
| MUS81 | 1 | Targeted literature review pending |
| MYO18A | 1 | Targeted literature review pending |
| NADK | 1 | Targeted literature review pending |
| NCSTN | 1 | Targeted literature review pending |
| NECTIN4 | 1 | Targeted literature review pending |
| NEIL1 | 1 | Targeted literature review pending |
| NEIL2 | 1 | Targeted literature review pending |
| NEIL3 | 1 | Targeted literature review pending |
| NFKBIZ | 1 | Targeted literature review pending |
| NR0B1 | 1 | Targeted literature review pending |
| NUF2 | 1 | Targeted literature review pending |
| OGG1 | 1 | Targeted literature review pending |
| PAXIP1 | 1 | Targeted literature review pending |
| PDS5B | 1 | Targeted literature review pending |
| PGBD5 | 1 | Targeted literature review pending |
| PHIP | 1 | Targeted literature review pending |
| PIGA | 1 | Targeted literature review pending |
| PNKP | 1 | Targeted literature review pending |
| POLB | 1 | Targeted literature review pending |
| POLH | 1 | Targeted literature review pending |
| PPP4R2 | 1 | Targeted literature review pending |
| PRDM14 | 1 | Targeted literature review pending |
| PRF1 | 1 | Targeted literature review pending |
| PRSS1 | 1 | Targeted literature review pending |
| PTK2B | 1 | Targeted literature review pending |
| PTP4A1 | 1 | Targeted literature review pending |
| PTPN1 | 1 | Targeted literature review pending |
| PTPN2 | 1 | Targeted literature review pending |
| RAC2 | 1 | Targeted literature review pending |
| RBBP8 | 1 | Targeted literature review pending |
| RECQL | 1 | Targeted literature review pending |
| REST | 1 | Targeted literature review pending |
| RHBDF2 | 1 | Targeted literature review pending |
| RHOT1 | 1 | Targeted literature review pending |
| RIF1 | 1 | Targeted literature review pending |
| RINT1 | 1 | Targeted literature review pending |
| RNF8 | 1 | Targeted literature review pending |
| RPA1 | 1 | Targeted literature review pending |
| RPS15 | 1 | Targeted literature review pending |
| RPS19 | 1 | Targeted literature review pending |
| RPS26 | 1 | Targeted literature review pending |
| RPS6KB1 | 1 | Targeted literature review pending |
| RRAS | 1 | Targeted literature review pending |
| RSPO2 | 1 | Targeted literature review pending |
| RSPO3 | 1 | Targeted literature review pending |
| SCG5 | 1 | Targeted literature review pending |
| SERP2 | 1 | Targeted literature review pending |
| SERPINA1 | 1 | Targeted literature review pending |
| SERPINB3 | 1 | Targeted literature review pending |
| SERPINB4 | 1 | Targeted literature review pending |
| SESN1 | 1 | Targeted literature review pending |
| SESN2 | 1 | Targeted literature review pending |
| SESN3 | 1 | Targeted literature review pending |
| SETD1A | 1 | Targeted literature review pending |
| SETD3 | 1 | Targeted literature review pending |
| SETD4 | 1 | Targeted literature review pending |
| SETD5 | 1 | Targeted literature review pending |
| SETD6 | 1 | Targeted literature review pending |
| SETD7 | 1 | Targeted literature review pending |
| SETDB2 | 1 | Targeted literature review pending |
| SHOC2 | 1 | Targeted literature review pending |
| SLC25A13 | 1 | Targeted literature review pending |
| SLFN11 | 1 | Targeted literature review pending |
| SLX1A | 1 | Targeted literature review pending |
| SLX1B | 1 | Targeted literature review pending |
| SMARCA1 | 1 | Targeted literature review pending |
| SMG1 | 1 | Targeted literature review pending |
| SMYD3 | 1 | Targeted literature review pending |
| SOCS2 | 1 | Targeted literature review pending |
| SOCS3 | 1 | Targeted literature review pending |
| SPRED1 | 1 | Targeted literature review pending |
| SPRTN | 1 | Targeted literature review pending |
| SRCAP | 1 | Targeted literature review pending |
| SRP19 | 1 | Targeted literature review pending |
| SRY | 1 | Targeted literature review pending |
| TAFAZZIN | 1 | Targeted literature review pending |
| TAP1 | 1 | Targeted literature review pending |
| TAP2 | 1 | Targeted literature review pending |
| TDG | 1 | Targeted literature review pending |
| TEK | 1 | Targeted literature review pending |
| TET3 | 1 | Targeted literature review pending |
| TEX12 | 1 | Targeted literature review pending |
| TFRC | 1 | Targeted literature review pending |
| TNFRSF1B | 1 | Targeted literature review pending |
| TOPBP1 | 1 | Targeted literature review pending |
| TRAF5 | 1 | Targeted literature review pending |
| TRIM37 | 1 | Targeted literature review pending |
| TRIP13 | 1 | Targeted literature review pending |
| TYK2 | 1 | Targeted literature review pending |
| UBE2T | 1 | Targeted literature review pending |
| UIMC1 | 1 | Targeted literature review pending |
| UPF1 | 1 | Targeted literature review pending |
| UROD | 1 | Targeted literature review pending |
| USP28 | 1 | Targeted literature review pending |
| VAV2 | 1 | Targeted literature review pending |
| WAS | 1 | Targeted literature review pending |
| WHR1 | 1 | Targeted literature review pending |
| WRN | 1 | Targeted literature review pending |
| XBP1 | 1 | Targeted literature review pending |
| XPA | 1 | Targeted literature review pending |
| XPC | 1 | Targeted literature review pending |
| XRCC1 | 1 | Targeted literature review pending |
| XRCC3 | 1 | Targeted literature review pending |
| XRCC4 | 1 | Targeted literature review pending |
| XRCC5 | 1 | Targeted literature review pending |
| XRCC6 | 1 | Targeted literature review pending |
| YLPM1 | 1 | Targeted literature review pending |
| ZBTB7A | 1 | Targeted literature review pending |
| ZEB2 | 1 | Targeted literature review pending |
| ZFHX4 | 1 | Targeted literature review pending |
| ZNF292 | 1 | Targeted literature review pending |
| ZNF318 | 1 | Targeted literature review pending |
| SAMD9L | 0 | Targeted literature review pending |
| SAMD9 | 0 | Targeted literature review pending |
| FOS | 0 | Targeted literature review pending |
| FOSB | 0 | Targeted literature review pending |
| BMF | 0 | Targeted literature review pending |
| CA9 | 0 | Targeted literature review pending |
| CITED2 | 0 | Targeted literature review pending |
| MUC4 | 0 | Targeted literature review pending |
| SMARCC1 | 0 | Targeted literature review pending |
| SMARCC2 | 0 | Targeted literature review pending |
| TRG | 0 | Targeted literature review pending |
| AHRR | 0 | Targeted literature review pending |
| AIP | 0 | Targeted literature review pending |
| AMACR | 0 | Targeted literature review pending |
| ATG2B | 0 | Targeted literature review pending |
| ATP6AP2 | 0 | Targeted literature review pending |
| CAPN1 | 0 | Targeted literature review pending |
| CD34 | 0 | Targeted literature review pending |
| CD7 | 0 | Targeted literature review pending |
| CDCA7L | 0 | Targeted literature review pending |
| CEP43 | 0 | Targeted literature review pending |
| CHIC2 | 0 | Targeted literature review pending |
| CKS1B | 0 | Targeted literature review pending |
| CLIP1 | 0 | Targeted literature review pending |
| COL12A1 | 0 | Targeted literature review pending |
| COL21A1 | 0 | Targeted literature review pending |
| CSF1 | 0 | Targeted literature review pending |
| CYP2A6 | 0 | Targeted literature review pending |
| DES | 0 | Targeted literature review pending |
| DLK1 | 0 | Targeted literature review pending |
| DNAH11 | 0 | Targeted literature review pending |
| DNAJC21 | 0 | Targeted literature review pending |
| EFL1 | 0 | Targeted literature review pending |
| EGF | 0 | Targeted literature review pending |
| ELL | 0 | Targeted literature review pending |
| ELP1 | 0 | Targeted literature review pending |
| EPOR | 0 | Targeted literature review pending |
| FHL2 | 0 | Targeted literature review pending |
| FOLR1 | 0 | Targeted literature review pending |
| FOSL1 | 0 | Targeted literature review pending |
| FOXI1 | 0 | Targeted literature review pending |
| GNA14 | 0 | Targeted literature review pending |
| GOPC | 0 | Targeted literature review pending |
| GPNMB | 0 | Targeted literature review pending |
| GRIPAP1 | 0 | Targeted literature review pending |
| GRM1 | 0 | Targeted literature review pending |
| GSKIP | 0 | Targeted literature review pending |
| GTF3C2 | 0 | Targeted literature review pending |
| HAVCR2 | 0 | Targeted literature review pending |
| HMGA1 | 0 | Targeted literature review pending |
| HOOK1 | 0 | Targeted literature review pending |
| HOXA9 | 0 | Targeted literature review pending |
| HTRA1 | 0 | Targeted literature review pending |
| IGHV4-34 | 0 | Targeted literature review pending |
| IGLL5 | 0 | Targeted literature review pending |
| IL17RB | 0 | Targeted literature review pending |
| IL3 | 0 | Targeted literature review pending |
| INHBE | 0 | Targeted literature review pending |
| IRF2BP2 | 0 | Targeted literature review pending |
| IRS4 | 0 | Targeted literature review pending |
| KHDRBS2 | 0 | Targeted literature review pending |
| L1CAM | 0 | Targeted literature review pending |
| LINC01187 | 0 | Targeted literature review pending |
| LPL | 0 | Targeted literature review pending |
| LYST | 0 | Targeted literature review pending |
| MAFA | 0 | Targeted literature review pending |
| MMP16 | 0 | Targeted literature review pending |
| MPO | 0 | Targeted literature review pending |
| MRTFB | 0 | Targeted literature review pending |
| NEAT1 | 0 | Targeted literature review pending |
| NPM3 | 0 | Targeted literature review pending |
| OGA | 0 | Targeted literature review pending |
| OTX2 | 0 | Targeted literature review pending |
| PARN | 0 | Targeted literature review pending |
| PCDHGA1 | 0 | Targeted literature review pending |
| PKD1 | 0 | Targeted literature review pending |
| PKD2 | 0 | Targeted literature review pending |
| PKHD1 | 0 | Targeted literature review pending |
| PPP1R10 | 0 | Targeted literature review pending |
| PRDM10 | 0 | Targeted literature review pending |
| PRKCA | 0 | Targeted literature review pending |
| RBMX | 0 | Targeted literature review pending |
| RHCG | 0 | Targeted literature review pending |
| RREB1 | 0 | Targeted literature review pending |
| SBDSP1 | 0 | Targeted literature review pending |
| SERPINE1 | 0 | Targeted literature review pending |
| SH3PXD2A | 0 | Targeted literature review pending |
| SLAMF1 | 0 | Targeted literature review pending |
| SLC3A2 | 0 | Targeted literature review pending |
| SLC44A1 | 0 | Targeted literature review pending |
| SMAD9 | 0 | Targeted literature review pending |
| SOX11 | 0 | Targeted literature review pending |
| SRF | 0 | Targeted literature review pending |
| SRP54 | 0 | Targeted literature review pending |
| SS18L1 | 0 | Targeted literature review pending |
| TACC1 | 0 | Targeted literature review pending |
| TBX21 | 0 | Targeted literature review pending |
| TEAD1 | 0 | Targeted literature review pending |
| TGFBR3 | 0 | Targeted literature review pending |
| TRA | 0 | Targeted literature review pending |
| TRAK1 | 0 | Targeted literature review pending |
| TRB | 0 | Targeted literature review pending |
| TRIM11 | 0 | Targeted literature review pending |
| TRPS1 | 0 | Targeted literature review pending |
| ULK4 | 0 | Targeted literature review pending |
| VSTM2A | 0 | Targeted literature review pending |
