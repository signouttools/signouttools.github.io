# BAM Seek for SignoutTools

A client-only browser implementation of BAM Seek. The shipped tool is
`../tools/bam-seek.html`; the directory's Open and Download links use that same
standalone file. HTML, CSS, the analysis worker, igv.js, About content and notices
are embedded. No application server, runtime CDN, uploads or persistent browser
storage are required. The desktop localhost receiver/relay is not part of the
web version.

## Use

1. Select coordinate-sorted BAMs together with their BAI/CSI indexes. Conventional
   filenames pair automatically; ambiguous or renamed indexes can be selected
   explicitly. Prepare reads only headers and indexes. Choose at most one Current
   BAM, or leave every BAM historical.
2. Select and confirm the BAM assembly. Paste Current/Historical variants with
   one-based genomic coordinates and REF/ALT, then Calculate VAFs. The hg19 panel
   always runs for hg19, including when both input boxes are empty. It is disabled
   for hg38. Both-origin variants are excluded from comparison narratives.
3. Review separate read and molecule numerators/denominators, exclusion details,
   detection thresholds, direct phasing and experimental local-marker phasing.
   Failed/no-coverage queries suppress unsupported comparison claims.
4. For Open IGV, select the matching local `.2bit`, or uncompressed FASTA + FAI.
   Each result opens an independent temporary viewer. Both mates use the first
   mate's strand color, paired display is enabled, BASE sorting uses the variant
   position, and alignment sampling is disabled. Coverage, mismatches, soft clips,
   ruler and center guide are visible. The selected BAM/reference contig lengths
   and variant REF are checked. IGV display filters are printed in the viewer;
   its coverage need not equal the informative VAF denominator.

An initialized popup owns its selected File objects and bundled code and survives
closure of the analysis page. Reloaded/bookmarked temporary viewers must be
reopened from the results. If popup creation is blocked, an embedded viewer uses
the same bundle. Reopening the same configured result focuses/recenters its
existing popup. A changed reference or filter configuration opens a new viewer.
Wide views require zooming in (1 kb visibility window); depth is never silently
sampled to fit. Browser memory is still finite and resource errors remain errors.

Settings and evidence caches are memory-only. Source removal discards that
source's evidence cache; Clear discards all sources and caches. Current-sample
changes reuse the displayed evidence. Cancellation retains the last completed
result set. External-resource links send only their displayed structured variant
identifier, when clicked. Ten hg19 providers are included; hg38 links are disabled
rather than accidentally querying hg19. Equivalent shifted indels are not
normalized. Clinical-only inputs need genomic coordinates.

Experimental local phasing preserves the native rules: rare 2–20% markers can
support cis through positive co-occurrence, while common ≥30% minor-allele markers
can support trans through opposite haplotypes. Each required allele needs at
least three molecules (or the higher phase threshold), mapQ/baseQ ≥30 and strand
support. Independently supported third alleles, weak/conflicting links and
coverage gaps remain unresolved. Recruitment retains the native bounds of 32
rounds, 2,000 queried marker positions and 100,000 recruited records; reaching a
bound is reported.

## Build and test

Use Node.js 22+ and samtools for generated test fixtures:

```sh
npm ci --prefix bam-seek
npm test --prefix bam-seek
npm run build --prefix bam-seek
node scripts/bundle-tools.mjs
```

The refresh script preserves the existing tools and also rebuilds BAM Seek.
`package-lock.json` pins dependencies. `igv-build.mjs` applies an asserted patch to
igv.js 3.8.10: upstream `AlignmentContainer` ignores `downsample:false`, so the
patch explicitly uses an infinite sampling threshold for that setting. The packed
alignment rows have no imposed finite row cap. A JavaScript-only BGZF adapter
reused from Phase avoids the GMOD package's optional WASM data-URL fetch and works
under `connect-src 'none'`. Its decompression budgets produce explicit errors,
not sampled counts.

`npm test` tests the same bundled JavaScript engine/adapter used in the worker,
including deterministic BAM/BAI/CSI fixtures generated from tracked SAM. It also
checks exact CSP script hashes and packaged script syntax. No absolute fixture
paths are required.

For independent native comparisons, place the native BAM Seek checkout beside
SignoutTools and provide the igv-cpp checkout:

```sh
IGVCPP_SOURCE_DIR=/path/to/igv-cpp npm run test:native --prefix bam-seek
```

Override `BAM_SEEK_NATIVE_SOURCE` and `BAM_SEEK_NATIVE_BUILD` if needed. The script
configures/builds the non-GUI native core, generates JAK2 BAMs, restores the missing
clinical-mapping fixture only if absent, runs CTest, compiles a small native
oracle and compares 66 evidence/direct-phase/local-phase outputs. The supplied
mapping fixture is solely for native parser tests and is not loaded by the tool.

For browser checks:

```sh
npm run fixtures --prefix bam-seek
npm run test:browser:build --prefix bam-seek
python3 -m http.server 8765 --bind 127.0.0.1
```

Open `/bam-seek/tests/browser.html` in the local preview. Run the packaged-page
checks and each viewer button. The harness uses synthetic files only and checks
BAI/CSI, popup fallback, inherited CSP, reference handling, and viewer lifetime
through messages from the actual igv.js instance. High-depth checks require all
24,100 reads and all 12,050 nonempty paired rows, zero sampled intervals, paired
strand coloring and BASE sorting at the correct coordinate. See `VERIFICATION.md`.

No service worker or local HTTP service is installed. The preview server above is
a development/test command, not a deployment dependency. GitHub Pages serves the
same static release. Automatically intercepting desktop port calls or opening a
local pathname received in a URL would require a separate native helper and is
not possible in this client-only architecture.
