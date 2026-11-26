export const about = {
  'bam-seek': {
    title: 'BAM Seek',
    sections: [
      ['Use', 'Select coordinate-sorted BAM files and their matching BAI or CSI indexes. Designate at most one current sample, choose the alignment assembly, and enter current and historical variants with genomic coordinates and REF/ALT. The fixed hg19 disease panel runs alongside the entered variants.'],
      ['Evidence and phase', 'Read VAF uses ALT/(ALT+REF). Molecule VAF uses independent read-name fragments or the selected MI/RX/UB grouping. OTHER calls and ambiguous molecules are excluded from the denominators. Direct phasing requires actual observations of both sites. Experimental local phasing uses repeated rare-marker co-occurrence for cis and opposite common-marker haplotypes for trans.'],
      ['IGV review', 'Select a local 2bit reference or uncompressed FASTA with FAI. Each result opens a temporary igv.js window with paired alignments, first-of-pair strand coloring, base sorting at the variant and sampling disabled. Files are read locally and the bundled viewer requires no network. Wide views may require zooming in. Reloading a temporary window requires reopening it from the results.'],
      ['Privacy and interpretation', 'Files, settings and caches are held in memory. External resource links open only when selected and contain structured variant identifiers. Review draft narratives against assay thresholds and coverage before use. No desktop command relay is required.'],
    ],
  },
  sara: {
    title: 'SARA',
    sections: [
      ['Use', 'Open an hg19 somatic variant TSV or compact CSV. Use the Variants tab to filter and review calls. Add the matching hg19 .2bit file for SBS-96 sequence contexts, homopolymer checks, and indel anchoring.'],
      ['Hotspots and review flags', 'SARA checks reported protein positions against bundled Core, Broad, or Maximal gene-and-residue lists, using the selected distance window. The source datasets for those lists are undocumented in this release. A separate NCBI ClinVar pathogenic/likely pathogenic snapshot flags exact hg19 alleles after trimming shared bases. Truncating variants in the selected tumor suppressor gene tier also get a review flag.'],
      ['Signatures and TMB', 'SBS-96 and DBS-78 profiles are compared with COSMIC v3.4 by cosine similarity, with an optional non-negative mixture fit. TMB divides qualifying variants by the configured assay size (default 42.964144 Mb). The UCSC chain maps hg19 alleles to hg38 when the full allele maps continuously.'],
    ],
  },
  cara: {
    title: 'CARA',
    sections: [
      ['Use', 'Load four hg19 TSVs together: copy ratios and allelic counts for tumor and matched normal. Confirm the file assignments, open a chromosome, and drag across a region in Annotate mode to record a label. Save review writes a file you can reopen later.'],
      ['Tracks and suggestions', 'CARA plots log₂ copy ratios and allele fractions for tumor and normal. Running means summarize the tracks. The paired imbalance track compares tumor and normal at matching alleles. Threshold labeling applies editable ranges to smoothed copy ratios after a baseline adjustment. Review proposed labels before accepting them.'],
      ['Gene annotation', 'The bundled UCSC hg19 RefSeq gene spans supply interval overlaps, including introns. An overlap indicates that the interval touches the gene span.'],
    ],
  },
  fiq: {
    title: 'FIQ',
    sections: [
      ['Use', 'Open a coordinate-sorted hg19/GRCh37 BAM and its matching BAI or CSI. Enter two gene names or two 1-based coordinates with a search window. Run the search and inspect the supporting read groups and mapping qualities.'],
      ['Evidence', 'FIQ queries the two loci through the BAM index. It groups split, supplementary, and mate-linked alignments by read name and reports the evidence for each group. For coordinate searches, skipped regions and deletions do not count as aligned overlap. A linked read group is evidence for review. Breakpoint and transcript assignments are approximate.'],
      ['Gene annotation', 'The bundled GENCODE v50 annotation mapped to GRCh37 supplies gene and exon intervals. Transcript-pair summaries prefer MANE transcripts where available.'],
    ],
  },
  sage: {
    title: 'SAGE',
    sections: [
      ['Use', 'Upload a gel image and adjust the Enhance controls. Import reference overlay images and align them using position, scale, rotation, skew, and opacity. The export button saves the working project as JSON for reopening.'],
      ['Image processing', 'SAGE applies brightness, contrast, gamma, and other adjustments to a working copy on the canvas. The source image is left intact. Overlay crops and transforms affect how the layers are drawn.'],
      ['Reference overlays', 'Overlay images come from files you select. Compare band positions by eye after alignment.'],
    ],
  },
  phase: {
    title: 'Phase · Manual',
    sections: [
      ['Use', 'Open a coordinate-sorted BAM, its BAI or CSI, and the alignment reference as .2bit or uncompressed FASTA with FAI. Load a 1-based interval or choose a transcript. Select read pairs in the pileup and choose Merge selected.'],
      ['Evidence', 'Phase reads the selected locus through the BAM index and pairs records by read name and read group. Conflicting callable bases or indels block a merge. Uncovered sites stay unknown. Site VAF counts alternate-supporting fragments among callable fragments and counts overlapping mates once. Group share uses all included fragments in the loaded interval.'],
      ['Transcript catalog', 'Gene search uses bundled NCBI RefSeq transcript coordinates from UCSC for hg19 and hg38. Choose the assembly used to align the BAM.'],
    ],
  },
  'phase-automatic': {
    title: 'Phase · Automatic grouping',
    sections: [
      ['Use', 'Open a coordinate-sorted BAM, its BAI or CSI, and the alignment reference as .2bit or uncompressed FASTA with FAI. Choose a gene or 1-based interval, then select Analyze. Expand a group to inspect its original read pairs.'],
      ['Grouping', 'Phase calls local SNPs and CIGAR indels and builds phase blocks from alleles observed together on fragments. Within a block it groups compatible allele patterns. Reads that fit multiple patterns can remain ambiguous, and overlapping mates count once. Disconnected blocks are reported separately. Group counts describe the observed fragments in each block.'],
      ['Transcript catalog', 'Gene and transcript lookup uses bundled NCBI RefSeq coordinates from UCSC for hg19 and hg38.'],
    ],
  },
  'phase-assembly': {
    title: 'Phase · Assembly',
    sections: [
      ['Use', 'Open a coordinate-sorted BAM and its BAI or CSI. Add the matching reference for sequence annotation, then select an interval and assemble. Select a graph segment or pattern to inspect its supporting fragments.'],
      ['Assembly', 'Phase builds a de Bruijn graph from local read sequences using k-mers (default 31) and condenses unbranched paths. Read paths define alternative sequences at graph branches. Paired fragments link these alternatives into local patterns. Ambiguous fragments can remain shared across patterns.'],
      ['Reference and counts', 'Bundled NCBI RefSeq coordinates from UCSC support hg19/hg38 gene lookup. The optional genome reference labels assembled sequence. Pattern share and allele fraction are calculated from supporting fragments.'],
    ],
  },
  'phase-specific': {
    title: 'Phase · Specific variants',
    sections: [
      ['Use', 'Open a coordinate-sorted BAM and its BAI or CSI. Select the BAM assembly, paste 1-based variants, and choose Check variant list. Fix flagged entries, then select Phase specific variants. No separate genome file is required.'],
      ['Evidence', 'Phase queries each site through the BAM index. Read pairs count once, including when each mate covers a different site. Together and separate frequencies use fragments carrying at least one requested alternate and a callable REF or ALT at both sites. Optional helper SNPs report indirect links separately from direct fragment counts.'],
      ['Transcript mapping', 'Coding HGVS uses bundled hg19/hg38 NCBI RefSeq coordinates from UCSC. Indels are evaluated at the stated coordinates. Equivalent shifted indels in repeats can be missed.'],
    ],
  },
};
