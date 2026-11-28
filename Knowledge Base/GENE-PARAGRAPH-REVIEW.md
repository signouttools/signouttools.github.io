# Gene paragraph source review

Completed the source pass for all **1,251 remaining short entries**. **887 paragraphs were expanded or materially clarified**; each remaining entry has an explicit retention decision.

Across the full 1,305-gene library, **411 paragraphs are 80–300 words**, **894 are shorter**, and **0 are longer. The range is a soft editorial target. A short paragraph is not an unfinished source-review task.

## Sources and scope

The pass compared NCBI Gene/RefSeq functional descriptions with reviewed UniProtKB entries matched by HGNC ID. Missing NCBI snapshots were retrieved, and a current reviewed human UniProt functional snapshot was acquired. Source text, selected functional propositions, qualifiers, per-gene URLs, and hashes are preserved in `curation/gene-paragraph-source-review.json`. Curated report projections are stored in `curation/gene-paragraph-expansions.json`.

This was a source-backed molecular-function expansion pass, not new full-text adjudication of every inherited or somatic association. Those sections and their claim-specific publication approvals are preserved. Existing disease-evidence gaps remain explicitly recorded outside report prose.

Entries were retained when the supported concise function was already represented, additional descriptions were uncertain or isoform-dependent, protein identity was not uniquely resolved, or explanatory function remained unknown. Predicted or similarity-based roles are not promoted to established human experimental findings. No minimum word count is enforced.

Targeted editorial checks distinguish AIP from AHR; the CTLH substrate-recognition role of GID4; nicastrin from the catalytic gamma-secretase assembly; Delta ligands from NOTCH receptors in MIB1 signaling; RNA translation from transcription in MSI2; the GDP-to-GTP exchange promoted by SOS1; and the predominant in-vivo reductase role of HSD11B1. Noncoding RNAs, antigen-receptor loci, and pseudogenes are handled separately from protein products.

## Reuse and regeneration

Includes selected, adapted UniProtKB functional descriptions. Attribution: UniProt Consortium, [CC BY 4.0](https://www.uniprot.org/help/license). Changes include selection, condensation, and harmonization with the existing paragraph. Individual UniProt entry links accompany each relevant report section.

Run `python3 "Knowledge Base/scripts/expand-gene-paragraphs.py"`, then `python3 "Knowledge Base/scripts/write-hotspot-review.py"`. The expansion step is also invoked after the citation audit by `prepare-report-comments.py`. It does not require the temporary source-download cache.

## Per-gene decisions

| Gene | Before | After | Source-review decision |
| --- | ---: | ---: | --- |
| ABCB11 | 43 | 82 | expanded from reviewed protein function |
| ABCC10 | 35 | 62 | expanded from reviewed protein function |
| ABL1 | 59 | 124 | expanded from reviewed protein function |
| ABL2 | 43 | 94 | expanded from reviewed protein function |
| ABRAXAS1 | 34 | 73 | expanded from reviewed protein function |
| ABTB3 | 30 | 30 | retained after source review |
| ACADS | 42 | 103 | expanded from reviewed protein function |
| ACP6 | 35 | 64 | expanded from reviewed protein function |
| ACSBG2 | 37 | 77 | expanded from reviewed protein function |
| ACTB | 70 | 97 | expanded from reviewed protein function |
| ACTG1 | 50 | 68 | expanded from reviewed protein function |
| ACVR1 | 64 | 64 | retained after source review |
| ACVR1B | 43 | 93 | expanded from reviewed protein function |
| ACVR2A | 57 | 57 | retained after source review |
| ADGRA2 | 27 | 72 | expanded from reviewed protein function |
| ADGRG1 | 79 | 92 | expanded from reviewed protein function |
| ADGRL4 | 35 | 35 | retained after source review |
| AFDN | 42 | 78 | expanded from reviewed protein function |
| AFF1 | 44 | 44 | retained after source review |
| AFF2 | 58 | 58 | retained after source review |
| AGO1 | 58 | 83 | expanded from reviewed protein function |
| AGO2 | 46 | 76 | expanded from reviewed protein function |
| AHI1 | 47 | 97 | expanded from reviewed protein function |
| AHRR | 42 | 71 | expanded from reviewed protein function |
| AIP | 44 | 63 | expanded targeted editorial synthesis |
| AKT1 | 59 | 108 | expanded from reviewed protein function |
| AKT2 | 43 | 78 | expanded from reviewed protein function |
| AKT3 | 66 | 104 | expanded from reviewed protein function |
| ALB | 36 | 64 | expanded from reviewed protein function |
| ALOX12B | 40 | 87 | expanded from reviewed protein function |
| ALPK1 | 65 | 74 | expanded from reviewed protein function |
| AMACR | 41 | 41 | retained after source review |
| AMER1 | 62 | 103 | expanded from reviewed protein function |
| AMPD1 | 31 | 31 | retained after source review |
| ANKRD11 | 36 | 76 | expanded from reviewed protein function |
| ANKRD26 | 26 | 38 | expanded from reviewed protein function |
| ANKZF1 | 39 | 76 | expanded from reviewed protein function |
| APLNR | 24 | 66 | expanded from reviewed protein function |
| APOBR | 33 | 41 | expanded from reviewed protein function |
| AR | 60 | 93 | expanded from reviewed protein function |
| ARAF | 42 | 42 | retained after source review |
| ARFRP1 | 24 | 49 | expanded from reviewed protein function |
| ARHGAP26 | 43 | 43 | retained after source review |
| ARHGAP28 | 35 | 44 | expanded from reviewed protein function |
| ARHGAP33 | 29 | 63 | expanded from reviewed protein function |
| ARHGAP35 | 61 | 97 | expanded from reviewed protein function |
| ARHGAP6 | 44 | 54 | expanded from reviewed protein function |
| ARHGEF12 | 50 | 78 | expanded from reviewed protein function |
| ARHGEF28 | 33 | 54 | expanded from reviewed protein function |
| ARID1B | 68 | 114 | expanded from reviewed protein function |
| ARID2 | 66 | 76 | expanded from reviewed protein function |
| ARID3A | 26 | 26 | retained after source review |
| ARID3B | 17 | 28 | expanded from reviewed protein function |
| ARID3C | 34 | 49 | expanded from reviewed protein function |
| ARID4A | 34 | 48 | expanded from reviewed protein function |
| ARID4B | 37 | 73 | expanded from reviewed protein function |
| ARID5A | 37 | 72 | expanded from reviewed protein function |
| ARID5B | 35 | 75 | expanded from reviewed protein function |
| ARIH1 | 35 | 90 | expanded from reviewed protein function |
| ARL16 | 24 | 57 | expanded from reviewed protein function |
| ASAP1 | 52 | 95 | expanded from reviewed protein function |
| ASF1B | 26 | 93 | expanded from reviewed protein function |
| ASPSCR1 | 43 | 43 | retained after source review |
| ASXL1 | 43 | 107 | expanded from reviewed protein function |
| ASXL2 | 74 | 110 | expanded from reviewed protein function |
| ATF1 | 64 | 64 | retained after source review |
| ATG2B | 27 | 94 | expanded from reviewed protein function |
| ATL2 | 38 | 38 | retained after source review |
| ATP1B1 | 34 | 61 | expanded from reviewed protein function |
| ATP6AP1 | 41 | 114 | expanded from reviewed protein function |
| ATP6AP2 | 59 | 59 | retained after source review |
| ATP6V1B2 | 35 | 74 | expanded from reviewed protein function |
| ATRX | 50 | 96 | expanded from reviewed protein function |
| ATXN2 | 38 | 38 | retained after source review |
| ATXN7 | 26 | 57 | expanded from reviewed protein function |
| ATXN7L3 | 37 | 69 | expanded from reviewed protein function |
| AURKA | 46 | 96 | expanded from reviewed protein function |
| AURKB | 38 | 81 | expanded from reviewed protein function |
| AXIN1 | 35 | 74 | expanded from reviewed protein function |
| AXIN2 | 47 | 47 | retained after source review |
| AXL | 39 | 107 | expanded from reviewed protein function |
| B2M | 51 | 51 | retained after source review |
| BABAM1 | 20 | 80 | expanded from reviewed protein function |
| BABAM2 | 35 | 80 | expanded from reviewed protein function |
| BACH2 | 57 | 57 | retained after source review |
| BAP1 | 48 | 80 | expanded from reviewed protein function |
| BARD1 | 29 | 90 | expanded from reviewed protein function |
| BBC3 | 26 | 55 | expanded targeted editorial synthesis |
| BCL10 | 65 | 105 | expanded from reviewed protein function |
| BCL11B | 75 | 119 | expanded from reviewed protein function |
| BCL2 | 39 | 75 | expanded from reviewed protein function |
| BCL2L1 | 50 | 50 | retained after source review |
| BCL2L11 | 25 | 25 | retained after source review |
| BCL2L12 | 22 | 47 | expanded targeted editorial synthesis |
| BCL2L2 | 28 | 28 | retained after source review |
| BCL6 | 44 | 128 | expanded from reviewed protein function |
| BCOR | 62 | 62 | retained after source review |
| BCORL1 | 51 | 61 | expanded from reviewed protein function |
| BCR | 49 | 82 | expanded from reviewed protein function |
| BEND2 | 22 | 59 | expanded targeted editorial synthesis |
| BICC1 | 32 | 40 | expanded from reviewed protein function |
| BIRC3 | 55 | 91 | expanded from reviewed protein function |
| BLM | 40 | 63 | expanded from reviewed protein function |
| BMF | 13 | 13 | retained after source review |
| BMP6 | 43 | 76 | expanded from reviewed protein function |
| BMPR1A | 67 | 75 | expanded from reviewed protein function |
| BNC2 | 40 | 54 | expanded from reviewed protein function |
| BRCC3 | 30 | 76 | expanded from reviewed protein function |
| BRD3 | 45 | 96 | expanded from reviewed protein function |
| BRD4 | 67 | 118 | expanded from reviewed protein function |
| BRD7 | 25 | 55 | expanded from reviewed protein function |
| BRINP1 | 29 | 43 | expanded from reviewed protein function |
| BRIP1 | 55 | 82 | expanded from reviewed protein function |
| BTG1 | 40 | 40 | retained after source review |
| BTK | 52 | 105 | expanded from reviewed protein function |
| BUB1B | 48 | 55 | expanded from reviewed protein function |
| C3orf70 | 33 | 33 | retained after source review |
| C6 | 39 | 114 | expanded from reviewed protein function |
| CA9 | 30 | 30 | retained after source review |
| CADM2 | 21 | 21 | retained after source review |
| CALR | 32 | 89 | expanded from reviewed protein function |
| CAMTA1 | 65 | 65 | retained after source review |
| CANT1 | 44 | 65 | expanded from reviewed protein function |
| CAPN1 | 42 | 42 | retained after source review |
| CARD11 | 66 | 105 | expanded from reviewed protein function |
| CARM1 | 35 | 67 | expanded from reviewed protein function |
| CARMN | 25 | 25 | retained after targeted source review |
| CASP8 | 71 | 62 | expanded from reviewed protein function |
| CBFA2T3 | 37 | 82 | expanded from reviewed protein function |
| CBFB | 64 | 64 | retained after source review |
| CBL | 64 | 106 | expanded from reviewed protein function |
| CBLB | 39 | 83 | expanded from reviewed protein function |
| CCDC6 | 50 | 60 | expanded from reviewed protein function |
| CCN6 | 40 | 40 | retained after source review |
| CCNB3 | 39 | 47 | expanded from reviewed protein function |
| CCND1 | 50 | 50 | retained after source review |
| CCND2 | 66 | 66 | retained after source review |
| CCND3 | 62 | 62 | retained after source review |
| CCNE1 | 44 | 44 | retained after source review |
| CCNQ | 46 | 46 | retained after source review |
| CCR4 | 43 | 43 | retained after source review |
| CCT8 | 33 | 59 | expanded from reviewed protein function |
| CD274 | 51 | 51 | retained after source review |
| CD276 | 25 | 55 | expanded from reviewed protein function |
| CD28 | 41 | 63 | expanded from reviewed protein function |
| CD34 | 31 | 31 | retained after source review |
| CD58 | 41 | 49 | expanded from reviewed protein function |
| CD7 | 29 | 29 | retained after source review |
| CD70 | 45 | 45 | retained after source review |
| CD74 | 62 | 75 | expanded from reviewed protein function |
| CD79A | 42 | 59 | expanded from reviewed protein function |
| CD79B | 63 | 63 | retained after source review |
| CDC42 | 38 | 58 | expanded from reviewed protein function |
| CDC73 | 64 | 119 | expanded from reviewed protein function |
| CDCA7L | 21 | 30 | expanded from reviewed protein function |
| CDH11 | 58 | 58 | retained after source review |
| CDH4 | 23 | 23 | retained after source review |
| CDK12 | 44 | 64 | expanded from reviewed protein function |
| CDK4 | 63 | 63 | retained after source review |
| CDK6 | 38 | 70 | expanded from reviewed protein function |
| CDK8 | 77 | 136 | expanded from reviewed protein function |
| CDKN1A | 49 | 68 | expanded from reviewed protein function |
| CDKN1B | 71 | 100 | expanded from reviewed protein function |
| CDKN1C | 61 | 61 | retained after source review |
| CDKN2B | 54 | 54 | retained after source review |
| CDKN2B-AS1 | 24 | 56 | expanded targeted editorial synthesis |
| CDKN2C | 49 | 49 | retained after source review |
| CDX2 | 56 | 71 | expanded from reviewed protein function |
| CEBPA | 41 | 105 | expanded from reviewed protein function |
| CELSR1 | 34 | 34 | retained after source review |
| CENPA | 26 | 79 | expanded from reviewed protein function |
| CEP43 | 29 | 29 | retained after source review |
| CEP63 | 38 | 48 | expanded from reviewed protein function |
| CEP89 | 31 | 31 | retained after source review |
| CFAP20 | 32 | 42 | expanded from reviewed protein function |
| CFAP44 | 30 | 30 | retained after source review |
| CFAP90 | 27 | 27 | retained after source review |
| CHD2 | 65 | 103 | expanded from reviewed protein function |
| CHD3 | 43 | 73 | expanded from reviewed protein function |
| CHD4 | 66 | 94 | expanded from reviewed protein function |
| CHD7 | 56 | 56 | retained after source review |
| CHEK1 | 33 | 70 | expanded from reviewed protein function |
| CHIC2 | 18 | 47 | expanded targeted editorial synthesis |
| CHIT1 | 27 | 36 | expanded from reviewed protein function |
| CHST12 | 32 | 58 | expanded from reviewed protein function |
| CIITA | 71 | 91 | expanded from reviewed protein function |
| CITED2 | 33 | 50 | expanded from reviewed protein function |
| CIZ1 | 34 | 34 | retained after source review |
| CKS1B | 28 | 73 | expanded from reviewed protein function |
| CLDN18 | 32 | 93 | expanded from reviewed protein function |
| CLEC14A | 32 | 68 | expanded targeted editorial synthesis |
| CLECL1 | 26 | 53 | expanded from reviewed protein function |
| CLIP1 | 29 | 46 | expanded from reviewed protein function |
| CLTC | 58 | 93 | expanded from reviewed protein function |
| CMTR2 | 36 | 58 | expanded from reviewed protein function |
| CNOT9 | 33 | 87 | expanded from reviewed protein function |
| COBL | 27 | 48 | expanded from reviewed protein function |
| COL12A1 | 47 | 47 | retained after source review |
| COL1A1 | 65 | 65 | retained after source review |
| COL1A2 | 53 | 53 | retained after source review |
| COL21A1 | 11 | 52 | expanded targeted editorial synthesis |
| COL6A3 | 57 | 57 | retained after source review |
| COL7A1 | 50 | 50 | retained after source review |
| COP1 | 31 | 54 | expanded from reviewed protein function |
| CR1 | 37 | 96 | expanded from reviewed protein function |
| CRB1 | 47 | 58 | expanded from reviewed protein function |
| CRBN | 28 | 87 | expanded from reviewed protein function |
| CREB1 | 58 | 87 | expanded from reviewed protein function |
| CREB3L1 | 72 | 75 | expanded from reviewed protein function |
| CREB3L2 | 72 | 84 | expanded from reviewed protein function |
| CREBBP | 49 | 87 | expanded from reviewed protein function |
| CREM | 57 | 57 | retained after source review |
| CRKL | 33 | 44 | expanded targeted editorial synthesis |
| CRLF2 | 41 | 56 | expanded from reviewed protein function |
| CRNKL1 | 29 | 29 | retained after source review |
| CRTC1 | 54 | 71 | expanded from reviewed protein function |
| CRTC3 | 54 | 66 | expanded from reviewed protein function |
| CSDE1 | 41 | 41 | retained after source review |
| CSF1 | 41 | 48 | expanded from reviewed protein function |
| CSF1R | 52 | 129 | expanded from reviewed protein function |
| CSF3R | 59 | 59 | retained after source review |
| CSNK1A1 | 35 | 35 | retained after source review |
| CSPG5 | 30 | 30 | retained after source review |
| CTCF | 68 | 105 | expanded from reviewed protein function |
| CTLA4 | 51 | 63 | expanded from reviewed protein function |
| CTNNA1 | 46 | 78 | expanded from reviewed protein function |
| CTR9 | 31 | 94 | expanded from reviewed protein function |
| CUL3 | 69 | 112 | expanded from reviewed protein function |
| CXCR4 | 52 | 81 | expanded from reviewed protein function |
| CXXC5 | 56 | 71 | expanded from reviewed protein function |
| CYLD | 67 | 93 | expanded from reviewed protein function |
| CYP19A1 | 36 | 83 | expanded from reviewed protein function |
| CYP2A6 | 29 | 29 | retained after source review |
| CYP2C8 | 30 | 50 | expanded from reviewed protein function |
| CYP4A11 | 33 | 97 | expanded from reviewed protein function |
| CYP7B1 | 52 | 95 | expanded from reviewed protein function |
| CYSLTR2 | 39 | 39 | retained after source review |
| DAXX | 35 | 94 | expanded from reviewed protein function |
| DCAF13 | 35 | 87 | expanded from reviewed protein function |
| DCLRE1C | 41 | 90 | expanded from reviewed protein function |
| DCTN1 | 52 | 90 | expanded from reviewed protein function |
| DCUN1D1 | 32 | 79 | expanded from reviewed protein function |
| DDB1 | 39 | 95 | expanded from reviewed protein function |
| DDB2 | 47 | 109 | expanded from reviewed protein function |
| DDIT3 | 34 | 62 | expanded targeted editorial synthesis |
| DDR2 | 51 | 63 | expanded from reviewed protein function |
| DDX28 | 25 | 52 | expanded from reviewed protein function |
| DDX3X | 69 | 92 | expanded from reviewed protein function |
| DDX41 | 49 | 94 | expanded from reviewed protein function |
| DEK | 39 | 39 | retained after source review |
| DES | 42 | 117 | expanded from reviewed protein function |
| DGCR8 | 71 | 122 | expanded from reviewed protein function |
| DHRS4 | 30 | 46 | expanded from reviewed protein function |
| DHX15 | 29 | 53 | expanded from reviewed protein function |
| DIS3 | 38 | 53 | expanded from reviewed protein function |
| DIS3L2 | 39 | 75 | expanded from reviewed protein function |
| DKC1 | 48 | 68 | expanded from reviewed protein function |
| DLK1 | 31 | 31 | retained after source review |
| DMC1 | 31 | 39 | expanded from reviewed protein function |
| DMRT1 | 72 | 127 | expanded from reviewed protein function |
| DNAH11 | 46 | 60 | expanded from reviewed protein function |
| DNAH9 | 43 | 71 | expanded from reviewed protein function |
| DNAJB1 | 47 | 58 | expanded from reviewed protein function |
| DNAJC21 | 26 | 52 | expanded from reviewed protein function |
| DNMT1 | 56 | 75 | expanded from reviewed protein function |
| DNMT3B | 48 | 100 | expanded from reviewed protein function |
| DOCK8 | 46 | 95 | expanded from reviewed protein function |
| DOT1L | 50 | 50 | retained after source review |
| DROSHA | 75 | 75 | retained after source review |
| DTD2 | 30 | 59 | expanded from reviewed protein function |
| DTX1 | 45 | 88 | expanded from reviewed protein function |
| DUSP16 | 33 | 33 | retained after source review |
| DUSP2 | 47 | 47 | retained after source review |
| DUSP22 | 52 | 70 | expanded from reviewed protein function |
| DUSP4 | 27 | 27 | retained after source review |
| DUX4 | 63 | 71 | expanded from reviewed protein function |
| E2F3 | 52 | 60 | expanded from reviewed protein function |
| EBF2 | 38 | 63 | expanded from reviewed protein function |
| EED | 59 | 107 | expanded from reviewed protein function |
| EFL1 | 36 | 36 | retained after source review |
| EGF | 42 | 42 | retained after source review |
| EGFL7 | 29 | 29 | retained after source review |
| EGLN1 | 53 | 72 | expanded from reviewed protein function |
| EGR1 | 40 | 64 | expanded from reviewed protein function |
| EGR2 | 69 | 110 | expanded from reviewed protein function |
| EHMT1 | 45 | 85 | expanded from reviewed protein function |
| EIF1AX | 50 | 78 | expanded from reviewed protein function |
| EIF4A2 | 43 | 43 | retained after source review |
| EIF4E | 32 | 116 | expanded from reviewed protein function |
| ELANE | 44 | 60 | expanded from reviewed protein function |
| ELF3 | 55 | 64 | expanded from reviewed protein function |
| ELL | 39 | 51 | expanded from reviewed protein function |
| ELOC | 47 | 47 | retained after source review |
| ELP1 | 39 | 57 | expanded targeted editorial synthesis |
| EME1 | 16 | 16 | retained after source review |
| EMILIN2 | 38 | 47 | expanded from reviewed protein function |
| EML4 | 50 | 72 | expanded from reviewed protein function |
| EMSY | 13 | 39 | expanded from reviewed protein function |
| ENG | 40 | 40 | expanded from reviewed protein function |
| EP300 | 56 | 93 | expanded from reviewed protein function |
| EP400 | 41 | 83 | expanded from reviewed protein function |
| EPAS1 | 60 | 92 | expanded from reviewed protein function |
| EPC1 | 41 | 101 | expanded from reviewed protein function |
| EPCAM | 52 | 52 | retained after source review |
| EPHA3 | 42 | 96 | expanded from reviewed protein function |
| EPHA5 | 28 | 87 | expanded from reviewed protein function |
| EPHA7 | 49 | 74 | expanded from reviewed protein function |
| EPHB1 | 22 | 71 | expanded from reviewed protein function |
| EPOR | 39 | 39 | retained after source review |
| ERBB2 | 77 | 77 | retained after source review |
| ERBB3 | 69 | 123 | expanded from reviewed protein function |
| ERBB4 | 53 | 100 | expanded from reviewed protein function |
| ERC1 | 51 | 51 | retained after source review |
| ERCC1 | 43 | 43 | retained after source review |
| ERCC2 | 66 | 66 | retained after source review |
| ERCC3 | 60 | 81 | expanded from reviewed protein function |
| ERCC4 | 47 | 58 | expanded from reviewed protein function |
| ERCC5 | 45 | 62 | expanded from reviewed protein function |
| ERCC6 | 50 | 67 | expanded targeted editorial synthesis |
| ERF | 62 | 62 | retained after source review |
| ERG | 57 | 52 | expanded targeted editorial synthesis |
| ERRFI1 | 35 | 46 | expanded from reviewed protein function |
| ESCO2 | 37 | 37 | retained after source review |
| ESR1 | 53 | 83 | expanded from reviewed protein function |
| ETAA1 | 32 | 32 | retained after source review |
| ETNK1 | 32 | 32 | retained after source review |
| ETS1 | 37 | 37 | retained after source review |
| ETV1 | 56 | 56 | retained after source review |
| ETV4 | 47 | 72 | expanded from reviewed protein function |
| ETV5 | 44 | 44 | retained after source review |
| ETV6 | 71 | 71 | retained after source review |
| EVPL | 27 | 38 | expanded from reviewed protein function |
| EWSR1 | 35 | 57 | expanded from reviewed protein function |
| EXO1 | 25 | 55 | expanded from reviewed protein function |
| EXOSC6 | 14 | 78 | expanded from reviewed protein function |
| EXT1 | 44 | 44 | retained after source review |
| EXT2 | 48 | 48 | retained after source review |
| EYA4 | 52 | 103 | expanded from reviewed protein function |
| EZH1 | 36 | 86 | expanded from reviewed protein function |
| EZH2 | 47 | 141 | expanded from reviewed protein function |
| EZHIP | 43 | 73 | expanded from reviewed protein function |
| FAAP100 | 14 | 43 | expanded from reviewed protein function |
| FAAP20 | 31 | 40 | expanded from reviewed protein function |
| FAAP24 | 23 | 44 | expanded from reviewed protein function |
| FAF1 | 32 | 32 | retained after source review |
| FAH | 33 | 33 | retained after source review |
| FAN1 | 42 | 87 | expanded from reviewed protein function |
| FANCA | 29 | 55 | expanded from reviewed protein function |
| FANCB | 41 | 41 | retained after source review |
| FANCC | 26 | 54 | expanded from reviewed protein function |
| FANCD2 | 41 | 59 | expanded from reviewed protein function |
| FANCE | 26 | 40 | expanded from reviewed protein function |
| FANCF | 30 | 61 | expanded from reviewed protein function |
| FANCG | 38 | 56 | expanded from reviewed protein function |
| FANCI | 40 | 73 | expanded from reviewed protein function |
| FANCL | 42 | 57 | expanded from reviewed protein function |
| FANCM | 47 | 65 | expanded from reviewed protein function |
| FANK1 | 37 | 37 | retained after source review |
| FAS | 72 | 102 | expanded from reviewed protein function |
| FAT1 | 64 | 64 | retained after source review |
| FAT3 | 35 | 35 | retained after source review |
| FBXO11 | 62 | 127 | expanded from reviewed protein function |
| FBXW7 | 63 | 106 | expanded from reviewed protein function |
| FEV | 51 | 51 | retained after source review |
| FGF1 | 43 | 80 | expanded from reviewed protein function |
| FGF10 | 44 | 44 | retained after source review |
| FGF14 | 28 | 28 | retained after source review |
| FGF19 | 40 | 40 | retained after source review |
| FGF2 | 30 | 45 | expanded from reviewed protein function |
| FGF23 | 67 | 67 | retained after source review |
| FGF3 | 53 | 53 | retained after source review |
| FGF4 | 38 | 71 | expanded from reviewed protein function |
| FGF5 | 29 | 59 | expanded from reviewed protein function |
| FGF6 | 31 | 31 | retained after source review |
| FGF7 | 30 | 30 | retained after source review |
| FGF8 | 40 | 62 | expanded from reviewed protein function |
| FGF9 | 46 | 46 | retained after source review |
| FGFR2 | 70 | 112 | expanded from reviewed protein function |
| FGFR3 | 74 | 96 | expanded from reviewed protein function |
| FGFR4 | 45 | 97 | expanded from reviewed protein function |
| FH | 60 | 60 | retained after source review |
| FHL2 | 38 | 59 | expanded from reviewed protein function |
| FIP1L1 | 35 | 83 | expanded from reviewed protein function |
| FLCN | 55 | 115 | expanded from reviewed protein function |
| FLI1 | 74 | 74 | retained after source review |
| FLT1 | 45 | 55 | expanded from reviewed protein function |
| FLT3 | 39 | 87 | expanded from reviewed protein function |
| FLT4 | 65 | 98 | expanded from reviewed protein function |
| FN1 | 70 | 73 | expanded from reviewed protein function |
| FOLR1 | 44 | 72 | expanded from reviewed protein function |
| FOS | 36 | 56 | expanded from reviewed protein function |
| FOSB | 42 | 58 | expanded from reviewed protein function |
| FOSL1 | 39 | 46 | expanded targeted editorial synthesis |
| FOXA1 | 61 | 104 | expanded from reviewed protein function |
| FOXF1 | 60 | 60 | retained after source review |
| FOXI1 | 44 | 63 | expanded from reviewed protein function |
| FOXL2 | 71 | 71 | retained after source review |
| FOXO1 | 53 | 101 | expanded from reviewed protein function |
| FOXO3 | 44 | 116 | expanded from reviewed protein function |
| FOXO4 | 50 | 50 | retained after source review |
| FOXP1 | 73 | 73 | retained after source review |
| FOXR2 | 32 | 32 | retained after targeted source review |
| FRMD4B | 24 | 51 | expanded from reviewed protein function |
| FRMD6 | 33 | 33 | retained after targeted source review |
| FRS2 | 41 | 65 | expanded from reviewed protein function |
| FUBP1 | 58 | 58 | retained after source review |
| FURIN | 23 | 35 | expanded from reviewed protein function |
| FUS | 55 | 96 | expanded from reviewed protein function |
| FYN | 36 | 74 | expanded from reviewed protein function |
| FZD10 | 30 | 60 | expanded from reviewed protein function |
| GAB1 | 24 | 46 | expanded from reviewed protein function |
| GAB2 | 34 | 52 | expanded from reviewed protein function |
| GABRA6 | 33 | 33 | retained after source review |
| GALNT12 | 27 | 69 | expanded from reviewed protein function |
| GATA1 | 64 | 64 | retained after source review |
| GATA2 | 48 | 55 | expanded from reviewed protein function |
| GATA3 | 71 | 68 | expanded from reviewed protein function |
| GATA4 | 72 | 70 | expanded from reviewed protein function |
| GATA6 | 76 | 76 | retained after source review |
| GBA1 | 40 | 64 | expanded from reviewed protein function |
| GEN1 | 30 | 64 | expanded from reviewed protein function |
| GFI1 | 64 | 80 | expanded from reviewed protein function |
| GFI1B | 68 | 84 | expanded from reviewed protein function |
| GID4 | 26 | 50 | expanded targeted editorial synthesis |
| GLI1 | 54 | 66 | expanded from reviewed protein function |
| GLI2 | 75 | 123 | expanded from reviewed protein function |
| GLIS2 | 63 | 63 | retained after source review |
| GNA11 | 63 | 105 | expanded from reviewed protein function |
| GNA12 | 30 | 49 | expanded from reviewed protein function |
| GNA13 | 49 | 71 | expanded from reviewed protein function |
| GNA14 | 28 | 28 | retained after source review |
| GNAQ | 53 | 97 | expanded from reviewed protein function |
| GNAS | 64 | 105 | expanded targeted editorial synthesis |
| GNB1 | 47 | 63 | expanded from reviewed protein function |
| GOPC | 31 | 50 | expanded from reviewed protein function |
| GPC3 | 44 | 84 | expanded from reviewed protein function |
| GPNMB | 39 | 39 | retained after source review |
| GPRIN2 | 31 | 31 | retained after source review |
| GPS2 | 40 | 87 | expanded from reviewed protein function |
| GREB1 | 27 | 27 | retained after source review |
| GREM1 | 35 | 27 | expanded from reviewed protein function |
| GRIN2A | 61 | 88 | expanded from reviewed protein function |
| GRIPAP1 | 42 | 62 | expanded from reviewed protein function |
| GRM1 | 48 | 82 | expanded from reviewed protein function |
| GRM3 | 46 | 46 | retained after source review |
| GSK3B | 34 | 57 | expanded from reviewed protein function |
| GSKIP | 34 | 34 | retained after source review |
| GTF2I | 51 | 95 | expanded from reviewed protein function |
| GTF3C2 | 38 | 55 | expanded from reviewed protein function |
| H1-2 | 32 | 54 | expanded from reviewed protein function |
| H1-3 | 31 | 70 | expanded from reviewed protein function |
| H1-4 | 42 | 80 | expanded from reviewed protein function |
| H1-5 | 33 | 70 | expanded from reviewed protein function |
| H2AC11 | 25 | 62 | expanded from reviewed protein function |
| H2AC16 | 25 | 62 | expanded from reviewed protein function |
| H2AC17 | 25 | 62 | expanded from reviewed protein function |
| H2AC6 | 25 | 62 | expanded from reviewed protein function |
| H2BC11 | 25 | 65 | expanded from reviewed protein function |
| H2BC12 | 26 | 65 | expanded from reviewed protein function |
| H2BC17 | 26 | 62 | expanded from reviewed protein function |
| H2BC4 | 25 | 65 | expanded from reviewed protein function |
| H2BC5 | 26 | 62 | expanded from reviewed protein function |
| H2BC8 | 25 | 65 | expanded from reviewed protein function |
| H3-3A | 61 | 117 | expanded from reviewed protein function |
| H3-3B | 45 | 101 | expanded from reviewed protein function |
| H3-4 | 23 | 60 | expanded from reviewed protein function |
| H3-5 | 25 | 60 | expanded from reviewed protein function |
| H3C1 | 23 | 60 | expanded from reviewed protein function |
| H3C10 | 23 | 60 | expanded from reviewed protein function |
| H3C11 | 23 | 60 | expanded from reviewed protein function |
| H3C12 | 23 | 60 | expanded from reviewed protein function |
| H3C13 | 23 | 60 | expanded from reviewed protein function |
| H3C14 | 23 | 60 | expanded from reviewed protein function |
| H3C15 | 23 | 60 | expanded from reviewed protein function |
| H3C2 | 40 | 77 | expanded from reviewed protein function |
| H3C3 | 23 | 60 | expanded from reviewed protein function |
| H3C4 | 23 | 60 | expanded from reviewed protein function |
| H3C6 | 23 | 60 | expanded from reviewed protein function |
| H3C7 | 23 | 60 | expanded from reviewed protein function |
| H3C8 | 23 | 60 | expanded from reviewed protein function |
| HABP2 | 63 | 63 | retained after source review |
| HAVCR2 | 47 | 66 | expanded from reviewed protein function |
| HDAC1 | 30 | 70 | expanded from reviewed protein function |
| HDAC4 | 63 | 84 | expanded from reviewed protein function |
| HDAC7 | 39 | 63 | expanded from reviewed protein function |
| HELQ | 38 | 64 | expanded from reviewed protein function |
| HEXD | 32 | 32 | retained after source review |
| HEY1 | 54 | 59 | expanded from reviewed protein function |
| HFE | 42 | 42 | retained after source review |
| HGF | 77 | 77 | retained after source review |
| HIF1A | 31 | 46 | expanded from reviewed protein function |
| HLA-A | 46 | 77 | expanded from reviewed protein function |
| HLA-B | 47 | 86 | expanded from reviewed protein function |
| HLA-C | 49 | 85 | expanded from reviewed protein function |
| HLF | 56 | 56 | retained after source review |
| HMBS | 44 | 38 | expanded from reviewed protein function |
| HMGA1 | 32 | 44 | expanded from reviewed protein function |
| HMGA2 | 67 | 67 | retained after source review |
| HNF1A | 71 | 71 | retained after source review |
| HNMT | 41 | 41 | retained after source review |
| HNRNPK | 46 | 56 | expanded from reviewed protein function |
| HOOK1 | 23 | 63 | expanded from reviewed protein function |
| HOOK2 | 31 | 60 | expanded from reviewed protein function |
| HOXA9 | 37 | 83 | expanded from reviewed protein function |
| HOXB13 | 46 | 46 | retained after source review |
| HOXB2 | 37 | 37 | retained after source review |
| HSD11B1 | 33 | 66 | expanded targeted editorial synthesis |
| HSD3B1 | 35 | 35 | retained after source review |
| HSP90AA1 | 36 | 56 | expanded from reviewed protein function |
| HTRA1 | 58 | 77 | expanded from reviewed protein function |
| ICOS | 51 | 75 | expanded from reviewed protein function |
| ICOSLG | 26 | 58 | expanded from reviewed protein function |
| ID3 | 53 | 68 | expanded from reviewed protein function |
| ID4 | 38 | 38 | retained after source review |
| IFNGR1 | 54 | 87 | expanded from reviewed protein function |
| IGF1 | 47 | 90 | expanded from reviewed protein function |
| IGF1R | 78 | 76 | expanded from reviewed protein function |
| IGF2 | 78 | 78 | retained after source review |
| IGH | 36 | 78 | expanded targeted editorial synthesis |
| IGHV4-34 | 25 | 57 | expanded from reviewed protein function |
| IGK | 29 | 29 | retained limited functional evidence |
| IGL | 29 | 74 | expanded targeted editorial synthesis |
| IGLL5 | 22 | 52 | expanded targeted editorial synthesis |
| IKBKE | 48 | 69 | expanded from reviewed protein function |
| IKZF1 | 66 | 66 | retained after source review |
| IKZF3 | 67 | 80 | expanded from reviewed protein function |
| IL10 | 30 | 89 | expanded from reviewed protein function |
| IL17RB | 28 | 28 | retained after source review |
| IL3 | 24 | 54 | expanded from reviewed protein function |
| IL6ST | 62 | 104 | expanded from reviewed protein function |
| IL7R | 52 | 52 | retained after source review |
| ING1 | 33 | 33 | retained after source review |
| INHA | 25 | 70 | expanded from reviewed protein function |
| INHBA | 31 | 97 | expanded from reviewed protein function |
| INHBE | 36 | 79 | expanded from reviewed protein function |
| INMT | 26 | 74 | expanded from reviewed protein function |
| INPP4A | 35 | 50 | expanded from reviewed protein function |
| INPP4B | 35 | 56 | expanded from reviewed protein function |
| INPPL1 | 46 | 76 | expanded from reviewed protein function |
| INSR | 58 | 99 | expanded from reviewed protein function |
| INTS12 | 37 | 91 | expanded from reviewed protein function |
| IRF1 | 50 | 82 | expanded from reviewed protein function |
| IRF2 | 40 | 59 | expanded from reviewed protein function |
| IRF2BP2 | 37 | 37 | retained after source review |
| IRF4 | 67 | 67 | retained after source review |
| IRS1 | 34 | 86 | expanded from reviewed protein function |
| IRS2 | 36 | 86 | expanded from reviewed protein function |
| IRS4 | 47 | 78 | expanded from reviewed protein function |
| ITK | 51 | 79 | expanded from reviewed protein function |
| ITPKB | 30 | 30 | retained after source review |
| JAK1 | 62 | 75 | expanded from reviewed protein function |
| JAK2 | 50 | 100 | expanded from reviewed protein function |
| JAK3 | 65 | 92 | expanded from reviewed protein function |
| JARID2 | 49 | 93 | expanded from reviewed protein function |
| JAZF1 | 41 | 65 | expanded from reviewed protein function |
| JUN | 37 | 37 | retained after source review |
| JUNB | 63 | 72 | expanded from reviewed protein function |
| KANK4 | 29 | 29 | retained after source review |
| KAT6A | 71 | 85 | expanded from reviewed protein function |
| KAT6B | 61 | 61 | retained after source review |
| KAT8 | 37 | 106 | expanded from reviewed protein function |
| KBTBD4 | 33 | 91 | expanded from reviewed protein function |
| KCNH5 | 47 | 92 | expanded from reviewed protein function |
| KCNJ12 | 36 | 78 | expanded from reviewed protein function |
| KCNJ8 | 46 | 87 | expanded from reviewed protein function |
| KCNQ1 | 43 | 66 | expanded from reviewed protein function |
| KCNQ5 | 43 | 83 | expanded from reviewed protein function |
| KDM5A | 34 | 56 | expanded from reviewed protein function |
| KDM5C | 72 | 101 | expanded from reviewed protein function |
| KDM6A | 56 | 86 | expanded from reviewed protein function |
| KDR | 70 | 70 | retained after source review |
| KEAP1 | 60 | 81 | expanded from reviewed protein function |
| KEL | 22 | 22 | retained after source review |
| KHDRBS2 | 31 | 63 | expanded from reviewed protein function |
| KIAA1549 | 34 | 34 | retained after source review |
| KIF1B | 29 | 29 | retained after source review |
| KIF26B | 29 | 81 | expanded from reviewed protein function |
| KIF5B | 46 | 71 | expanded from reviewed protein function |
| KLF17 | 47 | 58 | expanded from reviewed protein function |
| KLF2 | 51 | 51 | retained after source review |
| KLF4 | 49 | 49 | retained after source review |
| KLF5 | 66 | 66 | retained after source review |
| KLHL6 | 37 | 74 | expanded from reviewed protein function |
| KLLN | 9 | 43 | expanded from reviewed protein function |
| KMT2A | 44 | 116 | expanded from reviewed protein function |
| KMT2B | 60 | 110 | expanded from reviewed protein function |
| KMT2C | 58 | 96 | expanded from reviewed protein function |
| KMT2D | 72 | 102 | expanded from reviewed protein function |
| KMT5A | 47 | 47 | retained after source review |
| KNSTRN | 33 | 65 | expanded from reviewed protein function |
| KSR2 | 32 | 32 | retained after source review |
| L1CAM | 49 | 49 | retained after source review |
| LAMC1 | 30 | 30 | retained after source review |
| LAMP1 | 31 | 44 | expanded from reviewed protein function |
| LATS1 | 47 | 83 | expanded from reviewed protein function |
| LATS2 | 48 | 95 | expanded from reviewed protein function |
| LCE1A | 24 | 24 | retained after source review |
| LCE1F | 28 | 28 | retained after source review |
| LCK | 46 | 76 | expanded from reviewed protein function |
| LENG8 | 26 | 26 | retained after targeted source review |
| LEUTX | 51 | 51 | retained after source review |
| LIG4 | 38 | 85 | expanded from reviewed protein function |
| LINC01187 | 13 | 13 | retained limited functional evidence |
| LMNA | 57 | 72 | expanded from reviewed protein function |
| LMO1 | 34 | 34 | retained after source review |
| LMO2 | 41 | 41 | retained after source review |
| LPL | 37 | 77 | expanded from reviewed protein function |
| LRP1 | 34 | 71 | expanded from reviewed protein function |
| LRP1B | 43 | 43 | retained after source review |
| LRP5 | 44 | 93 | expanded from reviewed protein function |
| LRRC71 | 30 | 30 | retained limited functional evidence |
| LSM14A | 31 | 60 | expanded from reviewed protein function |
| LTB | 27 | 27 | retained after source review |
| LTK | 50 | 66 | expanded from reviewed protein function |
| LTN1 | 30 | 53 | expanded from reviewed protein function |
| LYN | 54 | 114 | expanded from reviewed protein function |
| LYST | 21 | 34 | expanded from reviewed protein function |
| LZTR1 | 63 | 82 | expanded from reviewed protein function |
| MAD2L2 | 37 | 72 | expanded from reviewed protein function |
| MAF | 67 | 75 | expanded from reviewed protein function |
| MAFA | 39 | 39 | retained after source review |
| MAFB | 76 | 86 | expanded from reviewed protein function |
| MAGEC1 | 32 | 61 | expanded targeted editorial synthesis |
| MAGI2 | 45 | 71 | expanded from reviewed protein function |
| MAGOH | 37 | 93 | expanded from reviewed protein function |
| MALAT1 | 44 | 81 | expanded targeted editorial synthesis |
| MALT1 | 69 | 97 | expanded from reviewed protein function |
| MAML2 | 47 | 47 | retained after source review |
| MAML3 | 48 | 48 | retained after source review |
| MAMLD1 | 39 | 47 | expanded from reviewed protein function |
| MAP2K1 | 66 | 84 | expanded from reviewed protein function |
| MAP2K2 | 56 | 56 | retained after source review |
| MAP2K4 | 48 | 98 | expanded from reviewed protein function |
| MAP3K1 | 64 | 64 | retained after source review |
| MAP3K13 | 37 | 54 | expanded from reviewed protein function |
| MAP3K14 | 33 | 50 | expanded from reviewed protein function |
| MAP3K4 | 38 | 38 | retained after source review |
| MAP3K6 | 33 | 33 | retained after source review |
| MAP3K7 | 47 | 66 | expanded from reviewed protein function |
| MAP3K8 | 42 | 85 | expanded from reviewed protein function |
| MAPK1 | 51 | 93 | expanded from reviewed protein function |
| MAPK3 | 33 | 72 | expanded from reviewed protein function |
| MAPK7 | 31 | 57 | expanded from reviewed protein function |
| MAPKAP1 | 36 | 101 | expanded from reviewed protein function |
| MARCHF10 | 28 | 42 | expanded from reviewed protein function |
| MAX | 65 | 65 | retained after source review |
| MBD4 | 27 | 40 | expanded from reviewed protein function |
| MCL1 | 50 | 50 | retained after source review |
| MCM8 | 54 | 97 | expanded from reviewed protein function |
| MDC1 | 34 | 88 | expanded from reviewed protein function |
| MDM2 | 30 | 81 | expanded from reviewed protein function |
| MDM4 | 46 | 46 | retained after source review |
| MEAF6 | 37 | 97 | expanded from reviewed protein function |
| MECOM | 65 | 113 | expanded from reviewed protein function |
| MED12 | 71 | 111 | expanded from reviewed protein function |
| MED28 | 45 | 101 | expanded from reviewed protein function |
| MEF2A | 33 | 76 | expanded from reviewed protein function |
| MEF2B | 57 | 57 | retained after source review |
| MEF2C | 71 | 85 | expanded from reviewed protein function |
| MEF2D | 49 | 71 | expanded from reviewed protein function |
| MEIS1 | 55 | 55 | retained after source review |
| METTL14 | 32 | 108 | expanded from reviewed protein function |
| MGA | 53 | 65 | expanded from reviewed protein function |
| MGAM | 25 | 38 | expanded from reviewed protein function |
| MGMT | 41 | 66 | expanded from reviewed protein function |
| MIB1 | 28 | 46 | expanded targeted editorial synthesis |
| MICA | 34 | 34 | retained after source review |
| MIR143 | 33 | 73 | expanded targeted editorial synthesis |
| MIR17HG | 53 | 83 | expanded targeted editorial synthesis |
| MITF | 58 | 93 | expanded from reviewed protein function |
| MKI67 | 27 | 92 | expanded from reviewed protein function |
| MLH3 | 32 | 32 | retained after source review |
| MLLT1 | 21 | 76 | expanded from reviewed protein function |
| MLLT10 | 46 | 46 | retained after source review |
| MLLT3 | 41 | 94 | expanded from reviewed protein function |
| MMP16 | 23 | 23 | retained after source review |
| MN1 | 38 | 59 | expanded from reviewed protein function |
| MOB3B | 27 | 27 | retained after source review |
| MPEG1 | 37 | 61 | expanded from reviewed protein function |
| MPL | 50 | 50 | retained after source review |
| MPO | 45 | 33 | expanded from reviewed protein function |
| MRE11 | 46 | 127 | expanded from reviewed protein function |
| MRTFA | 47 | 87 | expanded from reviewed protein function |
| MRTFB | 36 | 36 | retained after source review |
| MSH2 | 51 | 81 | expanded from reviewed protein function |
| MSH3 | 41 | 41 | retained after source review |
| MSI1 | 28 | 54 | expanded from reviewed protein function |
| MSI2 | 35 | 64 | expanded targeted editorial synthesis |
| MST1 | 42 | 49 | expanded targeted editorial synthesis |
| MST1R | 48 | 56 | expanded from reviewed protein function |
| MTA1 | 30 | 43 | expanded from reviewed protein function |
| MTAP | 50 | 62 | expanded from reviewed protein function |
| MTCP1 | 38 | 38 | retained after source review |
| MTOR | 78 | 116 | expanded from reviewed protein function |
| MUC4 | 38 | 62 | expanded from reviewed protein function |
| MUC6 | 39 | 39 | retained after source review |
| MUS81 | 27 | 65 | expanded from reviewed protein function |
| MUTYH | 48 | 59 | expanded from reviewed protein function |
| MXD1 | 58 | 58 | retained after source review |
| MXD4 | 54 | 54 | retained after source review |
| MXI1 | 53 | 53 | retained after source review |
| MXRA5 | 30 | 30 | retained after source review |
| MYB | 63 | 63 | retained after source review |
| MYBBP1A | 31 | 57 | expanded from reviewed protein function |
| MYBL1 | 61 | 97 | expanded from reviewed protein function |
| MYC | 31 | 66 | expanded from reviewed protein function |
| MYCL | 44 | 44 | retained after targeted source review |
| MYCN | 43 | 43 | retained after source review |
| MYD88 | 55 | 104 | expanded from reviewed protein function |
| MYH11 | 56 | 56 | retained after source review |
| MYH9 | 68 | 89 | expanded from reviewed protein function |
| MYO18A | 20 | 47 | expanded targeted editorial synthesis |
| MYO18B | 41 | 59 | expanded from reviewed protein function |
| MYO9A | 29 | 48 | expanded from reviewed protein function |
| MYOCD | 40 | 63 | expanded from reviewed protein function |
| MYOD1 | 67 | 67 | retained after source review |
| MYT1 | 42 | 72 | expanded from reviewed protein function |
| MYT1L | 54 | 111 | expanded from reviewed protein function |
| NAB2 | 47 | 47 | retained after source review |
| NADK | 24 | 48 | expanded targeted editorial synthesis |
| NAP1L3 | 31 | 31 | retained after source review |
| NBN | 35 | 107 | expanded from reviewed protein function |
| NCOA1 | 59 | 90 | expanded from reviewed protein function |
| NCOA2 | 50 | 62 | expanded from reviewed protein function |
| NCOA3 | 50 | 89 | expanded from reviewed protein function |
| NCOA4 | 40 | 66 | expanded from reviewed protein function |
| NCOR1 | 49 | 69 | expanded from reviewed protein function |
| NCOR2 | 49 | 58 | expanded from reviewed protein function |
| NCR1 | 31 | 31 | retained after source review |
| NCSTN | 35 | 63 | expanded targeted editorial synthesis |
| NEAT1 | 26 | 55 | expanded targeted editorial synthesis |
| NECTIN4 | 47 | 47 | retained after source review |
| NEGR1 | 24 | 32 | expanded from reviewed protein function |
| NEIL1 | 31 | 49 | expanded from reviewed protein function |
| NEIL2 | 30 | 59 | expanded from reviewed protein function |
| NEIL3 | 29 | 91 | expanded from reviewed protein function |
| NFATC2 | 60 | 79 | expanded from reviewed protein function |
| NFE2 | 43 | 60 | expanded from reviewed protein function |
| NFE2L2 | 74 | 147 | expanded from reviewed protein function |
| NFIC | 36 | 36 | retained after source review |
| NFKBIA | 63 | 63 | retained after source review |
| NFKBIE | 40 | 55 | expanded from reviewed protein function |
| NFKBIZ | 28 | 48 | expanded from reviewed protein function |
| NHS | 40 | 59 | expanded from reviewed protein function |
| NKX2-1 | 71 | 91 | expanded from reviewed protein function |
| NKX3-1 | 34 | 34 | retained after source review |
| NOL4 | 24 | 24 | retained after targeted source review |
| NONO | 56 | 77 | expanded from reviewed protein function |
| NOTCH1 | 56 | 99 | expanded from reviewed protein function |
| NOTCH2 | 77 | 82 | expanded from reviewed protein function |
| NOTCH3 | 71 | 71 | retained after source review |
| NOTCH4 | 49 | 49 | expanded from reviewed protein function |
| NPAS1 | 36 | 83 | expanded from reviewed protein function |
| NPM3 | 20 | 35 | expanded from reviewed protein function |
| NR0B1 | 56 | 87 | expanded from reviewed protein function |
| NR4A3 | 64 | 88 | expanded from reviewed protein function |
| NRG1 | 48 | 71 | expanded from reviewed protein function |
| NSD1 | 68 | 68 | retained after source review |
| NSD2 | 66 | 81 | expanded from reviewed protein function |
| NSD3 | 49 | 59 | expanded targeted editorial synthesis |
| NT5C2 | 45 | 45 | retained after source review |
| NT5C3A | 43 | 43 | retained after source review |
| NTHL1 | 45 | 68 | expanded from reviewed protein function |
| NTRK1 | 53 | 110 | expanded from reviewed protein function |
| NTRK2 | 54 | 122 | expanded from reviewed protein function |
| NTRK3 | 34 | 34 | retained after source review |
| NTSR1 | 41 | 41 | retained after source review |
| NUF2 | 22 | 70 | expanded from reviewed protein function |
| NUMA1 | 38 | 66 | expanded from reviewed protein function |
| NUP214 | 65 | 65 | retained after source review |
| NUP93 | 44 | 44 | retained after source review |
| NUP98 | 72 | 72 | retained after source review |
| NUTM1 | 26 | 40 | expanded from reviewed protein function |
| NUTM2A | 27 | 27 | retained limited functional evidence |
| NUTM2B | 25 | 25 | retained limited functional evidence |
| NXF1 | 33 | 84 | expanded from reviewed protein function |
| OBP2B | 29 | 29 | retained after source review |
| OGA | 25 | 25 | retained after source review |
| OGG1 | 43 | 43 | retained after source review |
| OLIG2 | 59 | 79 | expanded from reviewed protein function |
| OTX2 | 55 | 55 | retained after source review |
| OVGP1 | 30 | 30 | retained after source review |
| OXA1L | 34 | 70 | expanded from reviewed protein function |
| P2RY8 | 56 | 56 | retained after source review |
| PACS2 | 52 | 59 | expanded from reviewed protein function |
| PAK1 | 47 | 94 | expanded from reviewed protein function |
| PAK3 | 47 | 80 | expanded from reviewed protein function |
| PAK5 | 31 | 56 | expanded from reviewed protein function |
| PAN3 | 51 | 81 | expanded from reviewed protein function |
| PANK3 | 29 | 40 | expanded from reviewed protein function |
| PARN | 53 | 76 | expanded from reviewed protein function |
| PARP1 | 49 | 92 | expanded from reviewed protein function |
| PASD1 | 29 | 54 | expanded from reviewed protein function |
| PATZ1 | 62 | 72 | expanded from reviewed protein function |
| PAX3 | 70 | 70 | retained after source review |
| PAX5 | 76 | 76 | retained after source review |
| PAX7 | 61 | 61 | retained after source review |
| PAX8 | 59 | 59 | retained after source review |
| PAXIP1 | 27 | 30 | expanded from reviewed protein function |
| PBRM1 | 43 | 61 | expanded from reviewed protein function |
| PBX3 | 56 | 56 | retained after source review |
| PCBP1 | 48 | 48 | retained after source review |
| PCDHA10 | 30 | 30 | retained after source review |
| PCDHGA1 | 28 | 28 | retained after source review |
| PCED1B | 29 | 66 | expanded targeted editorial synthesis |
| PCM1 | 42 | 68 | expanded from reviewed protein function |
| PCMTD1 | 35 | 70 | expanded from reviewed protein function |
| PCSK5 | 29 | 50 | expanded from reviewed protein function |
| PDCD1 | 31 | 31 | retained after source review |
| PDCD1LG2 | 47 | 58 | expanded from reviewed protein function |
| PDGFB | 62 | 104 | expanded from reviewed protein function |
| PDGFD | 65 | 63 | expanded from reviewed protein function |
| PDGFRA | 74 | 99 | expanded from reviewed protein function |
| PDGFRB | 71 | 126 | expanded from reviewed protein function |
| PDHA1 | 44 | 85 | expanded from reviewed protein function |
| PDK1 | 37 | 48 | expanded from reviewed protein function |
| PDPK1 | 35 | 75 | expanded from reviewed protein function |
| PDS5B | 32 | 59 | expanded from reviewed protein function |
| PDZRN3 | 44 | 44 | retained after source review |
| PGBD5 | 22 | 22 | retained after source review |
| PGR | 36 | 36 | retained after source review |
| PHF1 | 49 | 50 | expanded from reviewed protein function |
| PHF6 | 57 | 57 | retained after source review |
| PHIP | 48 | 48 | retained after source review |
| PHOX2B | 70 | 78 | expanded from reviewed protein function |
| PICALM | 49 | 87 | expanded from reviewed protein function |
| PIGA | 42 | 51 | expanded from reviewed protein function |
| PIK3C2B | 34 | 34 | retained after source review |
| PIK3C2G | 33 | 33 | retained after source review |
| PIK3C3 | 32 | 56 | expanded from reviewed protein function |
| PIK3CB | 50 | 89 | expanded from reviewed protein function |
| PIK3CD | 50 | 75 | expanded from reviewed protein function |
| PIK3CG | 38 | 61 | expanded from reviewed protein function |
| PIK3R1 | 70 | 101 | expanded from reviewed protein function |
| PIK3R2 | 60 | 94 | expanded from reviewed protein function |
| PIK3R3 | 32 | 32 | retained after source review |
| PIM1 | 52 | 87 | expanded from reviewed protein function |
| PKD1 | 51 | 82 | expanded from reviewed protein function |
| PKD2 | 51 | 61 | expanded from reviewed protein function |
| PKHD1 | 40 | 128 | expanded from reviewed protein function |
| PLAG1 | 74 | 74 | retained after source review |
| PLAGL1 | 64 | 64 | retained after source review |
| PLAGL2 | 51 | 51 | retained after source review |
| PLCB3 | 28 | 61 | expanded from reviewed protein function |
| PLCB4 | 56 | 56 | retained after source review |
| PLCG1 | 42 | 71 | expanded from reviewed protein function |
| PLCG2 | 53 | 53 | retained after source review |
| PLK2 | 33 | 92 | expanded from reviewed protein function |
| PMAIP1 | 23 | 38 | expanded from reviewed protein function |
| PML | 42 | 71 | expanded from reviewed protein function |
| PMS1 | 32 | 32 | retained after source review |
| PNKP | 56 | 56 | retained after source review |
| PNLIPRP3 | 31 | 31 | retained after source review |
| PNRC1 | 14 | 14 | retained after source review |
| PODXL | 33 | 80 | expanded from reviewed protein function |
| POLB | 28 | 45 | expanded from reviewed protein function |
| POLD1 | 54 | 97 | expanded from reviewed protein function |
| POLE | 56 | 91 | expanded from reviewed protein function |
| POLH | 42 | 66 | expanded from reviewed protein function |
| POLQ | 56 | 94 | expanded from reviewed protein function |
| POM121 | 30 | 47 | expanded from reviewed protein function |
| POT1 | 61 | 110 | expanded from reviewed protein function |
| POU5F1 | 54 | 65 | expanded from reviewed protein function |
| PPARG | 64 | 72 | expanded from reviewed protein function |
| PPM1D | 78 | 93 | expanded from reviewed protein function |
| PPP1R10 | 41 | 103 | expanded from reviewed protein function |
| PPP2R1A | 72 | 106 | expanded from reviewed protein function |
| PPP2R2A | 37 | 77 | expanded from reviewed protein function |
| PPP4R2 | 38 | 67 | expanded from reviewed protein function |
| PPP6C | 52 | 71 | expanded from reviewed protein function |
| PRCC | 24 | 24 | retained after source review |
| PRDM1 | 61 | 106 | expanded from reviewed protein function |
| PRDM10 | 41 | 41 | retained after source review |
| PRDM14 | 38 | 74 | expanded from reviewed protein function |
| PRDM6 | 42 | 59 | expanded from reviewed protein function |
| PREX2 | 54 | 72 | expanded from reviewed protein function |
| PRF1 | 37 | 71 | expanded from reviewed protein function |
| PRKACA | 57 | 94 | expanded from reviewed protein function |
| PRKACB | 53 | 104 | expanded from reviewed protein function |
| PRKCA | 38 | 117 | expanded from reviewed protein function |
| PRKCB | 48 | 96 | expanded from reviewed protein function |
| PRKCI | 30 | 88 | expanded from reviewed protein function |
| PRKD1 | 60 | 129 | expanded from reviewed protein function |
| PRKD2 | 54 | 93 | expanded from reviewed protein function |
| PRKD3 | 44 | 44 | retained after source review |
| PRKDC | 51 | 76 | expanded from reviewed protein function |
| PRKN | 54 | 61 | expanded from reviewed protein function |
| PROCR | 31 | 31 | retained after source review |
| PRSS1 | 42 | 43 | expanded from reviewed protein function |
| PRSS27 | 32 | 68 | expanded targeted editorial synthesis |
| PRSS8 | 37 | 37 | retained after source review |
| PSG4 | 28 | 57 | expanded targeted editorial synthesis |
| PTCH1 | 76 | 76 | retained after source review |
| PTK2B | 36 | 68 | expanded from reviewed protein function |
| PTN | 27 | 73 | expanded from reviewed protein function |
| PTP4A1 | 27 | 35 | expanded from reviewed protein function |
| PTPN1 | 36 | 49 | expanded from reviewed protein function |
| PTPN11 | 73 | 82 | expanded from reviewed protein function |
| PTPN14 | 52 | 71 | expanded from reviewed protein function |
| PTPN2 | 33 | 70 | expanded from reviewed protein function |
| PTPRB | 45 | 45 | retained after source review |
| PTPRD | 48 | 48 | retained after source review |
| PTPRS | 29 | 61 | expanded from reviewed protein function |
| PTPRT | 40 | 40 | retained after source review |
| PUM3 | 32 | 66 | expanded from reviewed protein function |
| PVT1 | 45 | 78 | expanded targeted editorial synthesis |
| QKI | 47 | 86 | expanded from reviewed protein function |
| RAB35 | 28 | 89 | expanded from reviewed protein function |
| RAC1 | 69 | 123 | expanded from reviewed protein function |
| RAC2 | 54 | 54 | retained after source review |
| RAD21 | 69 | 69 | retained after source review |
| RAD50 | 48 | 126 | expanded from reviewed protein function |
| RAD51 | 46 | 77 | expanded from reviewed protein function |
| RAD51B | 38 | 52 | expanded from reviewed protein function |
| RAD52 | 33 | 33 | retained after source review |
| RAD54B | 47 | 60 | expanded from reviewed protein function |
| RAD54L | 34 | 70 | expanded from reviewed protein function |
| RAF1 | 63 | 77 | expanded from reviewed protein function |
| RANBP2 | 65 | 81 | expanded from reviewed protein function |
| RARA | 47 | 73 | expanded from reviewed protein function |
| RASA1 | 57 | 70 | expanded from reviewed protein function |
| RBBP8 | 45 | 106 | expanded from reviewed protein function |
| RBM10 | 41 | 72 | expanded targeted editorial synthesis |
| RBM15 | 38 | 113 | expanded from reviewed protein function |
| RBM39 | 35 | 78 | expanded from reviewed protein function |
| RBMX | 41 | 48 | expanded from reviewed protein function |
| RECQL | 32 | 47 | expanded from reviewed protein function |
| RECQL4 | 41 | 50 | expanded from reviewed protein function |
| REL | 48 | 101 | expanded from reviewed protein function |
| RELA | 64 | 114 | expanded from reviewed protein function |
| RELCH | 33 | 63 | expanded from reviewed protein function |
| REST | 53 | 81 | expanded from reviewed protein function |
| RHBDF2 | 41 | 61 | expanded from reviewed protein function |
| RHCG | 31 | 44 | expanded from reviewed protein function |
| RHEB | 29 | 60 | expanded from reviewed protein function |
| RHOA | 53 | 85 | expanded from reviewed protein function |
| RHOH | 47 | 89 | expanded from reviewed protein function |
| RHOT1 | 29 | 29 | retained after source review |
| RICTOR | 41 | 89 | expanded from reviewed protein function |
| RIF1 | 18 | 72 | expanded from reviewed protein function |
| RIMS1 | 32 | 66 | expanded from reviewed protein function |
| RIMS2 | 47 | 47 | retained after source review |
| RINT1 | 33 | 33 | retained after source review |
| RIPPLY2 | 49 | 49 | retained after source review |
| RIT1 | 53 | 78 | expanded from reviewed protein function |
| RNF43 | 61 | 83 | expanded from reviewed protein function |
| RNF8 | 30 | 91 | expanded from reviewed protein function |
| ROBO1 | 43 | 67 | expanded from reviewed protein function |
| ROS1 | 31 | 86 | expanded from reviewed protein function |
| RPA1 | 58 | 94 | expanded from reviewed protein function |
| RPL10L | 32 | 74 | expanded from reviewed protein function |
| RPS15 | 37 | 37 | retained after source review |
| RPS19 | 45 | 58 | expanded from reviewed protein function |
| RPS26 | 42 | 42 | retained after source review |
| RPS6KA4 | 34 | 89 | expanded from reviewed protein function |
| RPS6KB1 | 32 | 86 | expanded from reviewed protein function |
| RPS6KB2 | 29 | 45 | expanded from reviewed protein function |
| RPTOR | 40 | 62 | expanded from reviewed protein function |
| RRAGC | 37 | 109 | expanded from reviewed protein function |
| RRAS | 34 | 34 | retained after source review |
| RRAS2 | 53 | 53 | retained after source review |
| RRBP1 | 34 | 34 | retained after source review |
| RREB1 | 43 | 43 | retained after source review |
| RSBN1L | 24 | 24 | retained after source review |
| RSPO2 | 40 | 58 | expanded from reviewed protein function |
| RSPO3 | 25 | 70 | expanded from reviewed protein function |
| RTEL1 | 52 | 102 | expanded from reviewed protein function |
| RTKN2 | 26 | 26 | retained after source review |
| RUNX1 | 63 | 105 | expanded from reviewed protein function |
| RUNX1T1 | 45 | 45 | retained after source review |
| RUNX2 | 59 | 59 | retained after source review |
| RXRA | 47 | 86 | expanded from reviewed protein function |
| RYBP | 33 | 89 | expanded from reviewed protein function |
| S100A3 | 32 | 43 | expanded from reviewed protein function |
| S100A8 | 30 | 75 | expanded from reviewed protein function |
| SAMD9 | 32 | 87 | expanded from reviewed protein function |
| SAMD9L | 32 | 56 | expanded from reviewed protein function |
| SAMHD1 | 57 | 100 | expanded from reviewed protein function |
| SBDS | 41 | 52 | expanded from reviewed protein function |
| SBDSP1 | 15 | 15 | retained limited functional evidence |
| SCG5 | 47 | 70 | expanded from reviewed protein function |
| SDHA | 63 | 63 | retained after source review |
| SDHAF2 | 40 | 105 | expanded from reviewed protein function |
| SDHB | 66 | 75 | expanded from reviewed protein function |
| SDHC | 65 | 65 | retained after source review |
| SDHD | 71 | 71 | retained after source review |
| SEMA4B | 22 | 34 | expanded from reviewed protein function |
| SERP2 | 15 | 49 | expanded from reviewed protein function |
| SERPINA1 | 30 | 50 | expanded from reviewed protein function |
| SERPINB3 | 27 | 27 | retained after source review |
| SERPINB4 | 32 | 32 | retained after source review |
| SERPINE1 | 42 | 68 | expanded from reviewed protein function |
| SESN1 | 31 | 67 | expanded from reviewed protein function |
| SESN2 | 33 | 50 | expanded from reviewed protein function |
| SESN3 | 28 | 50 | expanded from reviewed protein function |
| SETBP1 | 56 | 81 | expanded targeted editorial synthesis |
| SETD1A | 47 | 87 | expanded from reviewed protein function |
| SETD1B | 53 | 115 | expanded from reviewed protein function |
| SETD2 | 70 | 104 | expanded from reviewed protein function |
| SETD3 | 30 | 50 | expanded from reviewed protein function |
| SETD4 | 32 | 69 | expanded from reviewed protein function |
| SETD5 | 54 | 80 | expanded from reviewed protein function |
| SETD6 | 28 | 45 | expanded from reviewed protein function |
| SETD7 | 27 | 49 | expanded from reviewed protein function |
| SETDB1 | 47 | 63 | expanded from reviewed protein function |
| SETDB2 | 32 | 48 | expanded from reviewed protein function |
| SF3B1 | 31 | 122 | expanded from reviewed protein function |
| SFPQ | 43 | 79 | expanded from reviewed protein function |
| SGK1 | 55 | 102 | expanded from reviewed protein function |
| SH2B3 | 69 | 69 | retained after source review |
| SH2D1A | 39 | 79 | expanded from reviewed protein function |
| SH3PXD2A | 32 | 32 | retained after source review |
| SHB | 33 | 80 | expanded from reviewed protein function |
| SHH | 59 | 128 | expanded from reviewed protein function |
| SHOC2 | 58 | 83 | expanded from reviewed protein function |
| SHQ1 | 30 | 57 | expanded from reviewed protein function |
| SHROOM1 | 33 | 33 | retained after source review |
| SIX1 | 68 | 88 | expanded from reviewed protein function |
| SIX2 | 47 | 87 | expanded from reviewed protein function |
| SLAMF1 | 28 | 55 | expanded from reviewed protein function |
| SLC16A13 | 31 | 31 | retained after source review |
| SLC25A13 | 50 | 100 | expanded from reviewed protein function |
| SLC27A5 | 38 | 65 | expanded from reviewed protein function |
| SLC34A2 | 64 | 64 | retained after source review |
| SLC3A2 | 16 | 50 | expanded from reviewed protein function |
| SLC44A1 | 48 | 65 | expanded from reviewed protein function |
| SLC4A11 | 54 | 66 | expanded from reviewed protein function |
| SLCO1B7 | 39 | 39 | retained limited functional evidence |
| SLFN11 | 28 | 48 | expanded from reviewed protein function |
| SLIT2 | 42 | 45 | expanded from reviewed protein function |
| SLMAP | 40 | 65 | expanded from reviewed protein function |
| SLX1A | 33 | 64 | expanded from reviewed protein function |
| SLX1B | 33 | 64 | expanded from reviewed protein function |
| SLX4 | 38 | 82 | expanded from reviewed protein function |
| SMAD2 | 63 | 105 | expanded from reviewed protein function |
| SMAD3 | 54 | 94 | expanded from reviewed protein function |
| SMAD9 | 57 | 57 | retained after source review |
| SMARCA1 | 51 | 93 | expanded from reviewed protein function |
| SMARCA2 | 73 | 119 | expanded from reviewed protein function |
| SMARCC1 | 49 | 81 | expanded from reviewed protein function |
| SMARCC2 | 50 | 84 | expanded from reviewed protein function |
| SMARCD1 | 41 | 81 | expanded from reviewed protein function |
| SMARCE1 | 55 | 95 | expanded from reviewed protein function |
| SMC1A | 55 | 78 | expanded from reviewed protein function |
| SMC3 | 51 | 70 | expanded from reviewed protein function |
| SMG1 | 30 | 55 | expanded from reviewed protein function |
| SMO | 77 | 77 | retained after source review |
| SMTNL2 | 24 | 24 | retained after targeted source review |
| SMYD3 | 32 | 32 | retained after source review |
| SNCAIP | 23 | 23 | retained after source review |
| SND1 | 46 | 58 | expanded from reviewed protein function |
| SNRPD3 | 32 | 69 | expanded from reviewed protein function |
| SOCS1 | 64 | 64 | retained after source review |
| SOCS2 | 36 | 81 | expanded from reviewed protein function |
| SOCS3 | 31 | 61 | expanded from reviewed protein function |
| SOS1 | 50 | 72 | expanded targeted editorial synthesis |
| SOX10 | 52 | 68 | expanded from reviewed protein function |
| SOX11 | 77 | 85 | expanded from reviewed protein function |
| SOX17 | 66 | 66 | retained after source review |
| SOX2 | 62 | 97 | expanded from reviewed protein function |
| SOX9 | 62 | 94 | expanded from reviewed protein function |
| SP140 | 44 | 44 | retained after source review |
| SPEN | 63 | 80 | expanded from reviewed protein function |
| SPI1 | 55 | 40 | expanded from reviewed protein function |
| SPOP | 58 | 107 | expanded renewed primary claim review |
| SPRED1 | 54 | 54 | retained after source review |
| SPRTN | 24 | 83 | expanded from reviewed protein function |
| SPTA1 | 48 | 48 | retained after source review |
| SRC | 30 | 102 | expanded from reviewed protein function |
| SRCAP | 51 | 82 | expanded from reviewed protein function |
| SRF | 38 | 78 | expanded from reviewed protein function |
| SRP19 | 36 | 56 | expanded from reviewed protein function |
| SRP54 | 45 | 84 | expanded from reviewed protein function |
| SRP72 | 40 | 95 | expanded from reviewed protein function |
| SRSF2 | 22 | 72 | expanded from reviewed protein function |
| SRY | 45 | 50 | expanded from reviewed protein function |
| SS18 | 46 | 57 | expanded from reviewed protein function |
| SS18L1 | 31 | 47 | expanded from reviewed protein function |
| SSBP3 | 33 | 52 | expanded from reviewed protein function |
| SSX1 | 37 | 37 | retained after source review |
| SSX2 | 21 | 21 | retained after source review |
| SSX4 | 21 | 21 | retained after source review |
| STAG1 | 43 | 73 | expanded from reviewed protein function |
| STAG2 | 50 | 80 | expanded from reviewed protein function |
| STAT3 | 77 | 130 | expanded from reviewed protein function |
| STAT4 | 47 | 70 | expanded from reviewed protein function |
| STAT5A | 47 | 47 | retained after source review |
| STIL | 42 | 72 | expanded from reviewed protein function |
| STK40 | 28 | 28 | retained after source review |
| STRN | 38 | 38 | expanded from reviewed protein function |
| SUFU | 61 | 76 | expanded from reviewed protein function |
| SUZ12 | 63 | 80 | expanded from reviewed protein function |
| SWI5 | 32 | 32 | retained after source review |
| SYK | 58 | 104 | expanded from reviewed protein function |
| SYT13 | 30 | 30 | retained after source review |
| TACC1 | 28 | 43 | expanded from reviewed protein function |
| TACC3 | 27 | 78 | expanded from reviewed protein function |
| TAF1 | 52 | 95 | expanded from reviewed protein function |
| TAF15 | 41 | 63 | expanded from reviewed protein function |
| TAFAZZIN | 35 | 88 | expanded from reviewed protein function |
| TAL1 | 51 | 51 | retained after source review |
| TAL2 | 53 | 53 | retained after targeted source review |
| TAP1 | 43 | 76 | expanded from reviewed protein function |
| TAP2 | 41 | 69 | expanded from reviewed protein function |
| TARBP2 | 32 | 85 | expanded from reviewed protein function |
| TBL1XR1 | 68 | 81 | expanded from reviewed protein function |
| TBX2 | 36 | 68 | expanded from reviewed protein function |
| TBX21 | 42 | 85 | expanded from reviewed protein function |
| TBX3 | 74 | 87 | expanded from reviewed protein function |
| TBXT | 43 | 54 | expanded from reviewed protein function |
| TCF20 | 45 | 45 | retained after source review |
| TCF3 | 59 | 69 | expanded from reviewed protein function |
| TCF4 | 70 | 70 | retained after source review |
| TCF7L2 | 71 | 90 | expanded from reviewed protein function |
| TCL1A | 45 | 45 | retained after source review |
| TDG | 29 | 109 | expanded from reviewed protein function |
| TEAD1 | 51 | 95 | expanded from reviewed protein function |
| TEK | 55 | 90 | expanded from reviewed protein function |
| TENT5C | 40 | 60 | expanded from reviewed protein function |
| TENT5D | 28 | 39 | expanded from reviewed protein function |
| TERC | 71 | 100 | expanded targeted editorial synthesis |
| TERT | 52 | 113 | expanded from reviewed protein function |
| TET1 | 56 | 80 | expanded from reviewed protein function |
| TET3 | 48 | 80 | expanded from reviewed protein function |
| TEX12 | 14 | 41 | expanded from reviewed protein function |
| TFCP2 | 51 | 67 | expanded from reviewed protein function |
| TFEB | 49 | 110 | expanded from reviewed protein function |
| TFG | 61 | 77 | expanded from reviewed protein function |
| TFRC | 49 | 72 | expanded from reviewed protein function |
| TGFBR1 | 55 | 133 | expanded from reviewed protein function |
| TGFBR2 | 60 | 130 | expanded from reviewed protein function |
| TGFBR3 | 37 | 69 | expanded from reviewed protein function |
| TGFBRAP1 | 32 | 71 | expanded from reviewed protein function |
| THBD | 40 | 92 | expanded from reviewed protein function |
| THRA | 45 | 45 | retained after source review |
| THSD7B | 28 | 28 | retained after targeted source review |
| TLX1 | 53 | 53 | retained after source review |
| TLX3 | 50 | 50 | retained after targeted source review |
| TMEM127 | 50 | 50 | retained after source review |
| TMEM131 | 29 | 29 | retained after source review |
| TMEM147 | 48 | 120 | expanded from reviewed protein function |
| TMEM200C | 26 | 26 | retained after targeted source review |
| TMEM68 | 43 | 94 | expanded from reviewed protein function |
| TMPRSS2 | 56 | 56 | retained after source review |
| TNFAIP3 | 71 | 104 | expanded from reviewed protein function |
| TNFRSF14 | 56 | 97 | expanded from reviewed protein function |
| TNFRSF1B | 53 | 58 | expanded from reviewed protein function |
| TOP1 | 43 | 93 | expanded from reviewed protein function |
| TOP2A | 23 | 72 | expanded from reviewed protein function |
| TOP2B | 49 | 78 | expanded from reviewed protein function |
| TOPBP1 | 31 | 72 | expanded from reviewed protein function |
| TP53BP1 | 36 | 90 | expanded from reviewed protein function |
| TP63 | 72 | 72 | retained after source review |
| TPM3 | 58 | 84 | expanded from reviewed protein function |
| TPR | 50 | 101 | expanded from reviewed protein function |
| TPSD1 | 30 | 47 | expanded from reviewed protein function |
| TPTE2 | 35 | 35 | retained after source review |
| TRA | 22 | 50 | expanded targeted editorial synthesis |
| TRAF2 | 32 | 80 | expanded from reviewed protein function |
| TRAF3 | 43 | 91 | expanded from reviewed protein function |
| TRAF5 | 33 | 33 | retained after source review |
| TRAF7 | 61 | 90 | expanded from reviewed protein function |
| TRAK1 | 31 | 48 | expanded from reviewed protein function |
| TRB | 22 | 60 | expanded targeted editorial synthesis |
| TRG | 20 | 59 | expanded targeted editorial synthesis |
| TRIM11 | 31 | 69 | expanded from reviewed protein function |
| TRIM27 | 50 | 86 | expanded from reviewed protein function |
| TRIM33 | 46 | 46 | retained after source review |
| TRIM37 | 40 | 68 | expanded from reviewed protein function |
| TRIM65 | 35 | 82 | expanded from reviewed protein function |
| TRIP13 | 54 | 85 | expanded from reviewed protein function |
| TROAP | 23 | 23 | retained after source review |
| TRPS1 | 63 | 78 | expanded from reviewed protein function |
| TRUB1 | 33 | 70 | expanded from reviewed protein function |
| TSC1 | 62 | 90 | expanded from reviewed protein function |
| TSC2 | 60 | 109 | expanded from reviewed protein function |
| TSC22D2 | 38 | 38 | retained after source review |
| TSHR | 61 | 80 | expanded from reviewed protein function |
| TTYH1 | 43 | 43 | retained after source review |
| TUBGCP4 | 42 | 69 | expanded from reviewed protein function |
| TUBGCP6 | 44 | 73 | expanded from reviewed protein function |
| TYK2 | 43 | 78 | expanded from reviewed protein function |
| U2AF1 | 29 | 90 | expanded from reviewed protein function |
| U2AF2 | 62 | 62 | retained after source review |
| UBE2D3 | 35 | 80 | expanded from reviewed protein function |
| UBE2T | 42 | 74 | expanded from reviewed protein function |
| UBR5 | 61 | 98 | expanded from reviewed protein function |
| UBTF | 73 | 73 | retained after source review |
| UBXN11 | 30 | 48 | expanded from reviewed protein function |
| UCHL1 | 45 | 74 | expanded from reviewed protein function |
| UIMC1 | 32 | 67 | expanded from reviewed protein function |
| ULK4 | 27 | 27 | retained after source review |
| UPF1 | 30 | 99 | expanded from reviewed protein function |
| UROD | 41 | 41 | retained after source review |
| USP28 | 28 | 47 | expanded from reviewed protein function |
| USP6 | 40 | 56 | expanded from reviewed protein function |
| USP8 | 40 | 32 | expanded from reviewed protein function |
| VAV1 | 52 | 52 | retained after source review |
| VAV2 | 32 | 49 | expanded from reviewed protein function |
| VCL | 46 | 46 | retained after source review |
| VEGFA | 41 | 48 | expanded from reviewed protein function |
| VGLL2 | 26 | 37 | expanded from reviewed protein function |
| VIM | 49 | 74 | expanded from reviewed protein function |
| VPS37B | 28 | 54 | expanded from reviewed protein function |
| VSTM2A | 22 | 44 | expanded from reviewed protein function |
| VTCN1 | 31 | 31 | retained after source review |
| WAS | 49 | 49 | retained after source review |
| WDR73 | 40 | 70 | expanded from reviewed protein function |
| WHR1 | 31 | 66 | expanded from reviewed protein function |
| WRN | 43 | 44 | expanded from reviewed protein function |
| WT1 | 66 | 66 | retained after source review |
| WWTR1 | 55 | 97 | expanded from reviewed protein function |
| XBP1 | 51 | 67 | expanded from reviewed protein function |
| XIAP | 49 | 49 | retained after source review |
| XPA | 38 | 74 | expanded from reviewed protein function |
| XPC | 43 | 100 | expanded from reviewed protein function |
| XPO1 | 39 | 96 | expanded from reviewed protein function |
| XPO6 | 31 | 31 | retained after source review |
| XRCC1 | 32 | 57 | expanded from reviewed protein function |
| XRCC2 | 30 | 64 | expanded from reviewed protein function |
| XRCC3 | 28 | 68 | expanded from reviewed protein function |
| XRCC4 | 50 | 97 | expanded from reviewed protein function |
| XRCC5 | 31 | 77 | expanded from reviewed protein function |
| XRCC6 | 32 | 76 | expanded from reviewed protein function |
| YAP1 | 69 | 110 | expanded from reviewed protein function |
| YES1 | 31 | 64 | expanded from reviewed protein function |
| YLPM1 | 13 | 37 | expanded from reviewed protein function |
| YWHAE | 46 | 80 | expanded from reviewed protein function |
| ZBTB16 | 56 | 56 | retained after source review |
| ZBTB2 | 44 | 44 | retained after source review |
| ZBTB46 | 56 | 56 | retained after source review |
| ZBTB7A | 53 | 87 | expanded from reviewed protein function |
| ZC3H7B | 44 | 44 | retained after source review |
| ZEB1 | 71 | 71 | retained after source review |
| ZEB2 | 58 | 58 | retained after source review |
| ZFHX3 | 54 | 72 | expanded from reviewed protein function |
| ZFHX4 | 47 | 47 | retained after source review |
| ZFTA | 23 | 23 | retained after targeted source review |
| ZHX3 | 38 | 38 | retained after source review |
| ZMYM2 | 65 | 65 | retained after source review |
| ZMYM3 | 25 | 25 | retained after source review |
| ZNF217 | 38 | 38 | retained after source review |
| ZNF292 | 57 | 57 | retained after source review |
| ZNF318 | 30 | 30 | retained after source review |
| ZNF384 | 48 | 48 | retained after source review |
| ZNF516 | 42 | 43 | expanded from reviewed protein function |
| ZNF623 | 42 | 42 | retained after source review |
| ZNF649 | 37 | 37 | retained after source review |
| ZNF703 | 30 | 30 | retained after source review |
| ZNRF3 | 39 | 63 | expanded from reviewed protein function |
| ZRSR2 | 26 | 48 | expanded from reviewed protein function |
