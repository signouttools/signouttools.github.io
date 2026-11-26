# Cancer Hotspots attribution and database license

Contains information from **Cancer Hotspots**, developed by Memorial Sloan Kettering Cancer Center and collaborators: https://www.cancerhotspots.org/. Original release files were downloaded on 2026-11-26 and are retained unmodified in `original/`; their source URLs and SHA-256 hashes are recorded in `../data/hotspot-import.json`.

The Cancer Hotspots-derived database portions, including normalized hotspot/allele records, their recurrence drafts, hotspot search indexes/shards, and hotspot-derived portions of supplemental gene records, are made available under the **Open Database License (ODbL) v1.0**: https://opendatacommons.org/licenses/odbl/1-0/. A copy is retained in `LICENSE-ODbL-1.0.txt`. Retain attribution and comply with the license when publicly using or sharing adapted databases.

This adaptation normalizes submitted gene symbols to HGNC IDs, records release/sheet/row provenance, preserves source observations, and adds LLM-generated draft summaries. It does not imply endorsement by Cancer Hotspots, MSK, the study authors, FDA, HGNC, GenCC, or UniProt. The source database license does not assign a license to independently sourced third-party content or application code. Other source licenses and attributions continue to apply to those materials.

Study references:

- V1: Chang et al. [PMID 26619011](https://pubmed.ncbi.nlm.nih.gov/26619011/).
- V2: Chang et al. [PMID 29247016](https://pubmed.ncbi.nlm.nih.gov/29247016/).
- V3: Bandlamudi et al. [PMID 41895280](https://pubmed.ncbi.nlm.nih.gov/41895280/).

**Pathologist review needed — LLM-generated summary/review.**
