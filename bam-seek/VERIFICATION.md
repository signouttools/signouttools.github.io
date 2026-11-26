# BAM Seek verification — 2026-11-26

## Automated checks

- `npm test --prefix bam-seek`: bundled engine, parser, annotation deduplication,
  molecule grouping, report rows/blank protein fields, provider identifiers,
  comparison narratives, no-coverage/error handling, direct and experimental
  phasing, cancellation/recovery, source-cache removal and exact CSP hashes.
- Both BAI and CSI fixtures retain 24,100 alignments and 12,050 independent pairs.
- Native CTest: all five non-GUI suites pass. Native BAM Seek revision
  `98990915e521c89c683a31e3e5485f8e11940756`; igv-cpp revision
  `ebb4ad91b5b2fb9c8cf63e95de68777b8dd33319`.
- Native oracle comparison: all 66 evidence and direct/local phase checks pass,
  covering SNVs, indels, raw fragments, selected MI tags, cis, trans, insufficient
  support, unsequenced gaps and experimental rare/common marker chains.
- The directory refresh rebuilds BAM Seek and leaves the other shipped tool
  files unchanged.

## Browser checks

Observed in the available in-app browser using the actual packaged HTML served
on a loopback-only static preview:

- Worker prepares local File objects under the release CSP, then calculates
  the expected read/molecule results with BAI and CSI. No CSP violations.
- Both-origin annotation deduplication excludes those variants from the narrative.
- Current designation relabels results, repeated runs reuse cached evidence,
  source removal clears displayed results, and ambiguous indexes are explicitly
  paired. The disease-panel groups render with per-site errors where synthetic
  contigs lack hg19 hotspots.
- The Open IGV action on the actual packaged result opens a working embedded
  fallback under inherited CSP.
- Independent BAI and CSI windows each report 24,100 retained alignments, 12,050
  nonempty pair rows, samplingDepth=Infinity, and zero sampled intervals.
- Paired display and firstOfPairStrand coloring are enabled; BASE sorting uses
  zero-based coordinate 149 for the one-based variant at 150.
- A local 2bit reference also opens with the same full-depth evidence.
- An initialized viewer survives removal of its opener iframe, navigates again,
  and retains all 24,100 alignments.
- The embedded fallback visibly renders coverage and paired alignments, and the
  Re-sort at variant action works.

The browser tooling did not support direct `file://` navigation, and its native
file chooser stalled. Tests therefore populate File inputs with synthetic File
objects through the repository harness and exercise the identical standalone HTML
via HTTP. Direct downloaded-file behavior has explicit opaque-origin messaging
and a classic Blob worker, but manual Chrome/Edge file-opening remains a browser
compatibility check outside the available automation. This is not a server
requirement: the release has no external script/style assets or runtime network
requests. These tests establish behavior for their fixtures, not validation as a
diagnostic device or a guarantee for arbitrary BAM/reference combinations.
