"""Extract scoped fusion observations from Liu et al. and van Belzen et al. (2023).

Run with the bundled Python (openpyxl is used read-only). Inputs are original
MOESM4 workbook, MOESM4 CSV and the frozen HGNC TSV. No network requests.
The checked-in extraction is sufficient for ordinary corpus regeneration.
"""
import argparse
import collections
import csv
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CUR = ROOT / 'curation/fusions'
DATE = '2026-11-27'
HGNC_SHA = '46b83736ec351f15e22331575dce2f08416c5233765b26a08c65e6b42e56b651'
SOURCE = 'liu-2023-pediatric-cohort'
URL = 'https://pmc.ncbi.nlm.nih.gov/articles/PMC10076316/'


def sha(data):
    return hashlib.sha256(data).hexdigest()


def load(path):
    return json.loads(path.read_text())


def save(path, data):
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + '\n')


# Explicit mappings preserve pediatric and unspecified/historical qualifiers.
# A cohort's recruitment group is not necessarily the tumor's lineage.
CONTEXTS = {
    'AML': ('Pediatric acute myeloid leukemia', 'hematologic', 'aml'),
    'BALL': ('Pediatric B-lymphoblastic leukemia', 'hematologic', 'atlas-h-ball'),
    'TALL': ('Pediatric T-lymphoblastic leukemia', 'hematologic', 'atlas-h-tall'),
    'LGG': ('Pediatric low-grade glioma', 'cns', 'glioma'),
    'HGG': ('Pediatric high-grade glioma', 'cns', 'glioma'),
    'EPD': ('Pediatric ependymoma', 'cns', None),
    'MB': ('Pediatric medulloblastoma', 'cns', None),
    'BT': ('Pediatric brain tumor, subtype unspecified', 'cns', None),
    'Other': ('Pediatric brain tumor, subtype unspecified', 'cns', None),
    'Not Reported': ('Pediatric brain tumor, subtype unspecified', 'cns', None),
    'ST': ('Pediatric solid tumor, subtype unspecified', 'solid', None),
    'RHB': ('Pediatric rhabdomyosarcoma, subtype unspecified', 'solid', None),
    'EWS': ('Pediatric Ewing sarcoma', 'solid', None),
    "Ewing's Sarcoma": ('Pediatric Ewing sarcoma', 'solid', None),
    'Rhabdomyosarcoma': ('Pediatric rhabdomyosarcoma, subtype unspecified', 'solid', None),
    'Sarcoma': ('Pediatric sarcoma, subtype unspecified', 'solid', None),
    'Ganglioglioma': ('Pediatric ganglioglioma', 'cns', None),
    'Dysembryoplastic neuroepithelial tumor (DNET)': ('Pediatric dysembryoplastic neuroepithelial tumor', 'cns', None),
    'Brainstem glioma- Diffuse intrinsic pontine glioma': ('Pediatric diffuse intrinsic pontine glioma (study diagnosis)', 'cns', 'glioma'),
    'Glial-neuronal tumor NOS': ('Pediatric glioneuronal tumor, NOS', 'cns', None),
    'Supratentorial or Spinal Cord PNET': ('Pediatric supratentorial or spinal PNET (historical study diagnosis)', 'cns', None),
    'Metastatic secondary tumors': ('Pediatric metastatic tumor, primary unspecified', 'solid', None),
    'Meningioma': ('Pediatric meningioma', 'cns', None),
    'Neurocytoma': ('Pediatric neurocytoma', 'cns', None),
    'Cavernoma': ('Pediatric cavernoma (study specimen label)', 'cns', None),
    'Neurofibroma/Plexiform': ('Pediatric neurofibroma/plexiform neurofibroma', 'solid', None),
}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--pediatric-xlsx', type=Path, required=True)
    parser.add_argument('--wgs-csv', type=Path, required=True)
    parser.add_argument('--hgnc-tsv', type=Path, required=True)
    args = parser.parse_args()
    import openpyxl

    if sha(args.hgnc_tsv.read_bytes()) != HGNC_SHA:
        raise ValueError('HGNC snapshot differs; review identity changes before importing')
    with args.hgnc_tsv.open() as stream:
        identity = {r['symbol']: r for r in csv.DictReader(stream, delimiter='\t') if r['status'] == 'Approved'}
    previous = collections.defaultdict(list)
    for r in identity.values():
        for name in r['prev_symbol'].split('|'):
            previous[name].append(r['symbol'])

    def normalize(name):
        if name in identity:
            return name
        candidates = previous.get(name, [])
        if len(candidates) != 1:
            raise ValueError('Unresolved symbol: ' + name)
        return candidates[0]

    workbook = openpyxl.load_workbook(args.pediatric_xlsx, read_only=True, data_only=True)
    sheet = workbook['Supplementary Data 1']
    rows = list(sheet.values)
    if rows[3][:6] != ('Patient', 'Data Source', 'Cancer Type', 'Cancer Subtype', 'Sample', 'Fusion'):
        raise ValueError('Unexpected source table headers')
    grouped = collections.defaultdict(list)
    patients = set()
    all_patients = set()
    for row_number, row in enumerate(rows[4:], 5):
        if row[0]:
            all_patients.add(row[0])
        if row[5] and row[5] != '-':
            patients.add(row[0])
            grouped[row[5]].append({'row': row_number, 'cancer_type': row[2], 'cancer_subtype': row[3]})
    if (len(grouped), len(patients), len(all_patients)) != (272, 2005, 5190):
        raise ValueError('Extraction does not reconcile to published cohort totals')
    literature = {r[0]: {'row': n, 'candidate_reference': r[2], 'comment': r[3]}
                  for n, r in enumerate(workbook['Supplementary Data 25'].values, 1)
                  if r[0] in grouped}
    orientations = {r[4]: {'row': n, 'comment': r[6]}
                    for n, r in enumerate(workbook['Supplementary Data 32'].values, 1)
                    if r[4] in grouped}
    if set(orientations) != set(grouped):
        raise ValueError('Missing author orientation assignment')

    original = load(CUR / 'pre-audit-content.json')
    existing = {e['label'] for e in original['entries']}
    held = {e['label'] for e in original['deferred']}
    partners = load(CUR / 'partners.json')
    dmap = load(CUR / 'disease-mapping.json')
    all_diseases = load(ROOT / 'data/diseases.json') + dmap['new_diseases']
    by_name = {d['name']: d for d in all_diseases}
    new_diseases = []
    mapping = {}
    entries, decisions, observations, new_partners = [], [], [], {}
    for raw_pair, source_rows in sorted(grouped.items()):
        symbols = [normalize(s) for s in raw_pair.split('_')]
        if len(symbols) != 2:
            raise ValueError('Expected directed pair: ' + raw_pair)
        label = '::'.join(symbols)
        # Never clear a pre-existing hold through a bulk observation import.
        if label in held:
            raise ValueError('Held candidate requires a separate explicit review: ' + label)
        context_names = []
        for subtype in sorted({r['cancer_subtype'] for r in source_rows}):
            name, category, parent = CONTEXTS[subtype]
            context_names.append(name)
            if name in dmap['mapping']:
                mapping[name] = dmap['mapping'][name]
            elif name in by_name:
                mapping[name] = by_name[name]['id']
            else:
                disease_id = 'fusion-context-' + sha(name.encode())[:12]
                d = {'id': disease_id, 'name': name, 'category': category, 'parent_id': parent,
                     'synonyms': [], 'ontology_mappings': [], 'mapping_status': 'local_unmapped'}
                new_diseases.append(d)
                by_name[name] = d
                mapping[name] = disease_id
        observation = {'label': label, 'submitted_pair': raw_pair, 'source_id': SOURCE,
                       'table': 'Supplementary Data 1', 'source_rows': source_rows,
                       'tumor_contexts': sorted(set(context_names)),
                       'orientation_review': orientations[raw_pair],
                       'literature_followup': literature.get(raw_pair),
                       'disposition': 'existing_entry_preserved' if label in existing else 'new_cohort_observation_draft'}
        observations.append(observation)
        if label in existing:
            continue
        for symbol in symbols:
            if symbol in partners or symbol in new_partners:
                continue
            gene = identity[symbol]
            description = ('encodes ' + gene['name'] + '.' if gene['locus_type'] == 'gene with protein product'
                           else 'is annotated by HGNC as ' + gene['name'] + ' (' + gene['locus_type'] + ').')
            new_partners[symbol] = {
                'symbol': symbol, 'hgnc_id': gene['hgnc_id'], 'ncbi_gene_id': gene['entrez_id'] or None,
                'description': description, 'source_ids': ['hgnc'], 'identity_source_id': 'hgnc',
                'reference_audit': {'status': 'reference_supported', 'audited_on': DATE,
                                    'basis': 'identity_reference', 'url': 'https://www.genenames.org/data/gene-symbol-report/#!/hgnc_id/' + gene['hgnc_id'],
                                    'location': 'Frozen HGNC TSV: ' + gene['hgnc_id'] + ', approved symbol, name and locus_type columns',
                                    'document_sha256': HGNC_SHA,
                                    'scope': 'Approved gene identity/name only; no additional protein mechanism asserted.'}}
        # Describes occurrence only; no patient frequency, driver, diagnostic,
        # outcome or drug claim is inferred from the selected pair or gene name.
        text = label + ' was reported in specimens labeled as ' + '; '.join(observation['tumor_contexts']) + ' in the RNA-sequencing cohort of Liu et al.'
        row_numbers = [r['row'] for r in source_rows]
        evidence = [{'source_id': SOURCE, 'url': URL + '#MOESM4',
                     'location': 'Supplementary Data 1, columns C–F, rows ' + ', '.join(map(str, row_numbers)),
                     'source_rows': row_numbers, 'table': 'Supplementary Data 1',
                     'document_sha256': sha(args.pediatric_xlsx.read_bytes()),
                     'scope': 'Reported directed fusion and specimen diagnosis only. Not independent functional validation or a treatment indication.',
                     'access_level': 'primary_fulltext'}]
        aliases = {raw_pair.replace('_', '::')} - {label}
        for n, symbol in enumerate(symbols):
            for old in identity[symbol]['prev_symbol'].split('|'):
                if old:
                    alias_symbols = symbols.copy()
                    alias_symbols[n] = old
                    aliases.add('::'.join(alias_symbols))
        entries.append({'label': label, 'partners': symbols, 'aliases': sorted(aliases),
                        'event_class': 'fusion_transcript', 'tumor_contexts': observation['tumor_contexts'],
                        'evidence_scope': 'cohort_observation',
                        'sections': [{'kind': 'tumor_relevance', 'text': text, 'source_ids': [SOURCE]}],
                        'curation_notes': ['Transcript detection only. Functional orientation follows the authors\' Supplementary Data 32; uncommon orientations are not corrected by reversing partners.',
                                           'Literature references in Supplementary Data 25 are candidates for claim-specific review, not verified citations.']})
        decisions.append({'label': label, 'section_kind': 'tumor_relevance', 'original_text': text,
                          'original_text_sha256': sha(text.encode()), 'decision': 'retain',
                          'replacement_text': text, 'evidence': evidence,
                          'rationale': 'Exact directed pair and specimen labels extracted from the final cohort table; report text limited to the tabulated observation.'})

    # Independent RNA/WGS study: preserve observations and flags for follow-up.
    # Its "clinical" flag and tumor SV support do not establish a report claim.
    wgs = collections.defaultdict(list)
    with args.wgs_csv.open(encoding='utf-8-sig') as stream:
        for n, row in enumerate(csv.DictReader(stream), 2):
            wgs[row['fusion_name']].append({'row': n, 'diagnosis': row['tumor_type_label'],
                                           'supergroup': row['supergroup_label'],
                                           'high_confidence': row['high_confidence'] == 'TRUE',
                                           'author_clinical_flag': row['anno_clinically_relevant'] == 'TRUE',
                                           'variant_type': row['variant_type']})
    wgs_queue = []
    for pair, source_rows in sorted(wgs.items()):
        try:
            canonical = '::'.join(normalize(s) for s in pair.split('--'))
        except ValueError:
            canonical = None
        wgs_queue.append({'submitted_pair': pair, 'normalized_label': canonical,
                          'table': 'Additional file 4, Table S1', 'source_rows': source_rows,
                          'disposition': 'existing_or_added_pair_followup' if canonical in existing | {e['label'] for e in entries} else 'research_observation_review_required',
                          'report_eligible': False})
    receipts = {'pediatric_workbook_sha256': sha(args.pediatric_xlsx.read_bytes()),
                'wgs_csv_sha256': sha(args.wgs_csv.read_bytes()), 'hgnc_snapshot_sha256': HGNC_SHA,
                'pediatric_url': URL, 'pediatric_supplement': '41467_2023_37438_MOESM4_ESM.xlsx',
                'wgs_url': 'https://pmc.ncbi.nlm.nih.gov/articles/PMC10318758/',
                'wgs_supplement': '12885_2023_11054_MOESM4_ESM.csv',
                'license': 'CC BY 4.0', 'license_url': 'https://creativecommons.org/licenses/by/4.0/',
                'attribution': 'Liu et al., Nature Communications 14, 1739 (2023); van Belzen et al., BMC Cancer 23, 618 (2023).',
                'changes': 'Extracted fusion names, row locations and diagnostic labels; normalized HGNC names; removed patient/sample identifiers; original occurrence prose.'}
    source = {'id': SOURCE, 'title': 'Etiology of oncogenic fusions in 5,190 childhood cancers and its clinical and therapeutic implication',
              'url': URL, 'kind': 'primary_study', 'pmid': '37019972', 'citation_label': 'Liu et al. (2023)',
              'accessed_on': DATE, 'access_level': 'primary_fulltext',
              'review_scope': 'Results: Landscape of childhood oncogenic fusions; final cohort Supplementary Data 1; orientation Supplementary Data 32. Fusion detection and source diagnostic labels only.',
              'reuse_notes': receipts['attribution'] + ' CC BY 4.0. ' + receipts['changes'], 'license_url': receipts['license_url']}
    save(CUR / 'expansion-cohort.json', {'built_on': DATE, 'receipts': receipts,
         'added_sources': [source], 'added_partners': new_partners, 'entries': entries,
         'decisions': decisions, 'disease_mapping': mapping, 'new_diseases': new_diseases})
    save(CUR / 'expansion-observations.json', {'built_on': DATE, 'receipts': receipts,
         'pediatric': {'published_pairs': 272, 'published_fusion_positive_patients': 2005, 'published_cohort_patients': 5190,
                      'observation_rows': sum(map(len, grouped.values())), 'pairs': observations},
         'wgs': {'distinct_directed_pairs': len(wgs), 'observation_rows': sum(map(len, wgs.values())),
                 'pairs': wgs_queue}, 'new_runtime_entries': len(entries),
         'limits': ['A pair may occur in multiple specimens from one patient. Row counts are not patient counts.',
                    'The two cohorts may overlap; counts are not pooled or treated as independent replication.',
                    'Existing report text and tumor applicability are preserved; new contexts for existing entries require a separate claim review.',
                    'No raw prediction sheets, unconfirmed Tier2 candidates or promoter-hijacking candidates were imported.',
                    'WGS Table S1 contains incidentally detected and reciprocal fusions; none receives new report prose in this pass.']})
    print(f'Extracted {len(grouped)} pediatric pairs; {len(entries)} new observation drafts; {len(wgs)} RNA/WGS pairs queued.')


if __name__ == '__main__':
    main()
