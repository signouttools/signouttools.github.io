# Tumor type dropdown review

Reviewed 2026-11-27. All **606** selectable somatic tumor/source-context entries were reviewed across gene associations, hotspot cohorts, fusion contexts, and their ancestors. **70 redundant options** were consolidated into **57 groups**, leaving **536 options** in the combined gene browser. The fusion browser uses the same registry.

The reviewed registry is `data/tumor-type-aliases.json`. It explicitly lists source IDs for each group. The application resolves these IDs to a shared category before building the dropdown, applying filters, or restoring a bookmarked tumor filter. Original JSON evidence, source cohort labels/counts, and source IDs are retained. Search includes the original names and synonyms. No source cohort counts are added together.

## Review decisions

- Merge identical names and differences limited to case, punctuation, spacing, possessives, or the “(hotspot cohort)” suffix.
- Merge clear equivalent wording and word order, including cervical adenocarcinoma / adenocarcinoma of cervix, renal clear cell carcinoma / clear cell renal cell carcinoma, and salivary secretory carcinoma / secretory carcinoma of salivary gland.
- Merge explicitly readable site-code formatting variants, such as `adrenalgland` / `adrenal_gland`, `softtissue` / `soft_tissue`, and `headandneck` / `head_neck`. The source code records remain unchanged.
- The user explicitly approved combining glioblastoma / glioblastoma multiforme / glioblastoma, IDH-wildtype; B- and T-lymphoblastic leukemia with their respective leukemia/lymphoma groups; and myelodysplastic syndrome / neoplasm / neoplasia. “Glioblastoma” is the combined display label; grouping legacy evidence does not reclassify its original cases as IDH-wildtype.
- Equivalent lymphoid neoplasm entries use the hematologic category; the IntOGen entry had previously been assigned to solid tumors. The readable CNS cohort also supplies the category for its `cnsbrain` alias.

## Distinctions retained

Broad organ cohorts and narrower histologies remain separate: lung tumors / lung carcinoma / lung adenocarcinoma; breast tumors / breast carcinoma / invasive breast carcinoma; colon / rectal / colorectal adenocarcinoma; pancreatic carcinoma / adenocarcinoma / ductal adenocarcinoma. Molecular, anatomic, age-specific, grade-specific, and malignant-only qualifiers are retained, including TFEB-altered versus TFEB-rearranged renal carcinoma, solitary fibrous tumor versus malignant/high-risk solitary fibrous tumor, and specific leukemia fusion subtypes.

Unknown or ambiguous source abbreviations (including `acyc`, `lusm`, `lymbc`, `pias`) are retained as source-code categories. Similar-looking names and existing broad synonyms are not sufficient to merge them automatically. Future additions should receive explicit reviewed membership in the registry.

## Merged groups

| Shared option | Original dropdown names |
| --- | --- |
| Acute lymphoblastic leukemia | Acute lymphoblastic leukemia; Acute lymphoblastic leukemia (hotspot cohort) |
| Acute myeloid leukemia | Acute myeloid leukemia; Acute myeloid leukemia (hotspot cohort) |
| Acute promyelocytic leukemia | Acute promyelocytic leukemia |
| Adenocarcinoma of cervix | Adenocarcinoma of cervix; Cervical Adenocarcinoma |
| Adrenal gland tumors | Adrenal gland tumors (hotspot cohort); Cancer Hotspots source tumor code: adrenalgland (hotspot cohort) |
| Adrenocortical carcinoma | Adrenocortical carcinoma; Adrenocortical carcinoma (hotspot cohort) |
| Atypical teratoid/rhabdoid tumor | Atypical teratoid/rhabdoid tumor; Atypical Teratoid/Rhabdoid Tumor |
| B-lymphoblastic leukemia/lymphoma | B-lymphoblastic leukemia/lymphoma; B-lymphoblastic leukemia |
| Biliary tract tumors | Biliary tract tumors (hotspot cohort); Cancer Hotspots source tumor code: biliarytract (hotspot cohort) |
| Bladder Urothelial Carcinoma | Bladder Urothelial Carcinoma; Bladder urothelial carcinoma (hotspot cohort) |
| Breast carcinoma | Breast carcinoma; Breast carcinoma (hotspot cohort) |
| Cancer Hotspots source tumor code: ampulla_of_vater | Cancer Hotspots source tumor code: ampulla_of_vater (hotspot cohort); Cancer Hotspots source tumor code: ampullaofvater (hotspot cohort) |
| Cervical carcinoma | Cervical carcinoma; Cervical carcinoma (hotspot cohort) |
| Chromophobe renal cell carcinoma | Chromophobe renal cell carcinoma; Chromophobe renal cell carcinoma (hotspot cohort) |
| Chronic lymphocytic leukemia | Chronic lymphocytic leukemia; Chronic lymphocytic leukemia (hotspot cohort) |
| Chronic lymphocytic leukemia / small lymphocytic lymphoma | Chronic lymphocytic leukemia / small lymphocytic lymphoma; Chronic Lymphocytic Leukemia/Small Lymphocytic Lymphoma |
| Clear cell renal cell carcinoma | Clear cell renal cell carcinoma; Renal Clear Cell Carcinoma; Clear cell renal cell carcinoma (hotspot cohort) |
| CNS tumors | CNS tumors (hotspot cohort); Cancer Hotspots source tumor code: cnsbrain (hotspot cohort) |
| Colorectal carcinoma | Colorectal carcinoma; Colorectal carcinoma (hotspot cohort) |
| Cutaneous melanoma | Cutaneous melanoma; Cutaneous melanoma (hotspot cohort) |
| Endometrial carcinoma | Endometrial carcinoma; Endometrial carcinoma (hotspot cohort) |
| Esophagus / stomach tumors | Cancer Hotspots source tumor code: esophagusstomach (hotspot cohort); Esophagus/Stomach |
| Ewing sarcoma | Ewing sarcoma |
| Gastric adenocarcinoma | Gastric adenocarcinoma; Stomach Adenocarcinoma; Gastric adenocarcinoma (hotspot cohort) |
| Glioblastoma | Glioblastoma; Glioblastoma, IDH-wildtype; Glioblastoma Multiforme; Glioblastoma (hotspot cohort) |
| Head and Neck Squamous Cell Carcinoma | Head and Neck Squamous Cell Carcinoma; Head and neck squamous cell carcinoma (hotspot cohort) |
| Head and neck tumors | Head and neck tumors (hotspot cohort); Cancer Hotspots source tumor code: headandneck (hotspot cohort) |
| Hepatocellular carcinoma | Hepatocellular carcinoma; Hepatocellular carcinoma (hotspot cohort) |
| High-grade glioma | High-grade glioma; High-grade glioma (hotspot cohort) |
| Hyalinizing clear cell carcinoma of salivary gland | Hyalinizing clear cell carcinoma of salivary gland; Salivary hyalinizing clear cell carcinoma |
| Lung adenocarcinoma | Lung adenocarcinoma; Lung adenocarcinoma (hotspot cohort) |
| Lung squamous cell carcinoma | Lung squamous cell carcinoma; Lung squamous cell carcinoma (hotspot cohort) |
| Lung tumors | Lung tumors (hotspot cohort); Lung |
| Lymphoid neoplasms | Lymphoid neoplasms (hotspot cohort); Lymphoid Neoplasm |
| Medulloblastoma | Medulloblastoma; Medulloblastoma (hotspot cohort) |
| Myelodysplastic neoplasm | Myelodysplastic neoplasm; Myelodysplastic Syndromes; Myelodysplastic neoplasia; Myelodysplastic neoplasm (hotspot cohort) |
| Nasopharyngeal carcinoma | Nasopharyngeal carcinoma; Nasopharyngeal carcinoma (hotspot cohort) |
| Ovarian carcinoma | Ovarian carcinoma; Ovarian carcinoma (hotspot cohort) |
| Pancreatic Adenocarcinoma | Pancreatic Adenocarcinoma; Pancreatic adenocarcinoma (hotspot cohort) |
| Pancreatic tumors | Pancreatic tumors (hotspot cohort); Pancreas |
| Papillary renal cell carcinoma | Papillary renal cell carcinoma; Papillary renal cell carcinoma (hotspot cohort) |
| Paraganglioma | Paraganglioma |
| Ph-like B-lymphoblastic leukemia | Ph-like B-lymphoblastic leukemia; Ph-like B-ALL |
| Plasma cell myeloma | Plasma cell myeloma; Multiple myeloma (hotspot cohort) |
| Prostate adenocarcinoma | Prostate adenocarcinoma; Prostate adenocarcinoma (hotspot cohort) |
| Prostate tumors | Prostate tumors (hotspot cohort); Prostate |
| Secretory carcinoma of salivary gland | Secretory carcinoma of salivary gland; Salivary secretory carcinoma |
| Skin tumors | Skin tumors (hotspot cohort); Skin |
| Small cell lung carcinoma | Small cell lung carcinoma; Small Cell Lung Cancer |
| Soft tissue tumors | Soft tissue tumors (hotspot cohort); Soft Tissue; Cancer Hotspots source tumor code: softtissue (hotspot cohort) |
| Squamous cell carcinoma of cervix | Squamous cell carcinoma of cervix; Cervical Squamous Cell Carcinoma |
| Squamous cell carcinoma of skin | Squamous cell carcinoma of skin; Cutaneous Squamous Cell Carcinoma |
| T-lymphoblastic leukemia/lymphoma | T-lymphoblastic leukemia/lymphoma; T-ALL; T-lymphoblastic leukemia; T-cell acute lymphoblastic leukemia |
| Thyroid carcinoma | Thyroid carcinoma; Thyroid carcinoma (hotspot cohort) |
| Uterine carcinosarcoma | Uterine carcinosarcoma (hotspot cohort); Uterine Carcinosarcoma/Uterine Malignant Mixed Mullerian Tumor |
| Vulva / vagina tumors | Cancer Hotspots source tumor code: vulvavagina (hotspot cohort); Vulva/Vagina |
| Wilms tumor | Wilms tumor; Wilms' Tumor |

## Validation

`node "Knowledge Base/scripts/test-tumor-types.mjs"` checks the full selectable corpus for remaining normalized-name duplicates, all registry IDs, merged filter membership across genes/hotspots/fusions/variants, canonical parent cycles, category assignment, and legacy IDs.

Terminology references: [NCBI cervical adenocarcinoma](https://www.ncbi.nlm.nih.gov/medgen/79024), [NCBI small cell lung carcinoma](https://www.ncbi.nlm.nih.gov/medgen/57450), [SEER plasma cell myeloma](https://seer.cancer.gov/seertools/hemelymph/51f6cf5ae3e27c3994bd54aa/), and [NCBI uterine carcinosarcoma](https://ncbi.nlm.nih.gov/medgen/83678).
