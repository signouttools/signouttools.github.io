export function hgvsg(v) {
  const chr = v.chr.replace(/^chr/i, ""),
    n = v.pos + 1;
  if (v.ref.length === 1 && v.alt.length === 1)
    return `${chr}:g.${n}${v.ref}>${v.alt}`;
  let p = 0,
    s = 0;
  while (p < v.ref.length && p < v.alt.length && v.ref[p] === v.alt[p]) p++;
  while (
    s < v.ref.length - p &&
    s < v.alt.length - p &&
    v.ref.at(-s - 1) === v.alt.at(-s - 1)
  )
    s++;
  const removed = v.ref.slice(p, v.ref.length - s),
    inserted = v.alt.slice(p, v.alt.length - s),
    start = n + p,
    end = start + removed.length - 1,
    coord = removed.length <= 1 ? start : start + "_" + end;
  return (
    `${chr}:g.` +
    (!removed
      ? `${start - 1}_${start}ins${inserted}`
      : !inserted
        ? `${coord}del`
        : `${coord}delins${inserted}`)
  );
}
const aa = {
  Ala: "A",
  Arg: "R",
  Asn: "N",
  Asp: "D",
  Cys: "C",
  Gln: "Q",
  Glu: "E",
  Gly: "G",
  His: "H",
  Ile: "I",
  Leu: "L",
  Lys: "K",
  Met: "M",
  Phe: "F",
  Pro: "P",
  Ser: "S",
  Thr: "T",
  Trp: "W",
  Tyr: "Y",
  Val: "V",
  Ter: "*",
};
const one = (x) => (x.length === 1 ? x.toUpperCase() : aa[x]);
export function links(v, build = "hg19") {
  const chr = v.chr.replace(/^chr/i, ""),
    n = v.pos + 1,
    g = hgvsg(v),
    colon = `chr${chr}:${n}:${v.ref}:${v.alt}`,
    dash = `chr${chr}-${n}-${v.ref}-${v.alt}`,
    e = encodeURIComponent;
  const protein = v.protein || "",
    missense =
      /MISSENSE/i.test(v.type || "") &&
      v.gene &&
      /^p\.([A-Za-z*]|[A-Z][a-z]{2})[1-9]\d*([A-Za-z*]|[A-Z][a-z]{2})$/.test(
        protein,
      );
  let cb = null,
    codon = false;
  const change = protein.replace(/^p\./, "").replace(/^\((.*)\)$/, "$1");
  let m = change.match(
    /^([A-Z][a-z]{2}|[A-Za-z*])([1-9]\d*)([A-Z][a-z]{2}|[A-Za-z*])$/,
  );
  if (m && one(m[1]) && one(m[3])) cb = one(m[1]) + m[2] + one(m[3]);
  else {
    m = change.match(
      /^([A-Z][a-z]{2}|[A-Za-z*])([1-9]\d*)(fs(?:Ter|\*)?\d*|del|dup|ins[A-Za-z*]+)$/,
    );
    if (m && one(m[1])) cb = one(m[1]) + m[2] + m[3];
    else {
      m = change.match(/^([A-Z][a-z]{2}|[A-Za-z*])([1-9]\d*)/);
      if (m && one(m[1])) {
        cb = one(m[1]) + m[2];
        codon = true;
      }
    }
  }
  const a = (name, id, url, note = "", enabled = true) => ({
    name,
    id,
    url,
    enabled,
    note,
  });
  const oql = v.gene && cb ? v.gene + ":MUT=" + cb : "",
    literature = v.gene && protein ? v.gene + " " + protein : g;
  return [
    a("VarSome", colon, "https://varsome.com/variant/hg19/" + e(colon)),
    a("Genome Nexus", g, "https://www.genomenexus.org/variant/" + e(g)),
    a(
      "OncoKB",
      g,
      "https://www.oncokb.org/hgvsg/" + e(g) + "?refGenome=GRCh37",
      "No tumor-specific actionability supplied.",
    ),
    a(
      "SpliceAI Lookup",
      dash,
      "https://spliceailookup.broadinstitute.org/#variant=" +
        e(dash) +
        "&hg=37&bc=basic&distance=500&mask=0&ra=0",
    ),
    a(
      "Franklin",
      dash,
      "https://franklin.genoox.com/clinical-db/variant/snp/" + e(dash),
    ),
    a(
      "ProtVar / AlphaMissense",
      v.gene + ":" + protein,
      "https://www.ebi.ac.uk/ProtVar/search?q=" + e(v.gene + ":" + protein),
      "Requires an explicit missense type, gene and usable protein change.",
      !!missense,
    ),
    a(
      "gnomAD",
      `${chr}-${n}-${v.ref}-${v.alt}`,
      "https://gnomad.broadinstitute.org/variant/" +
        e(`${chr}-${n}-${v.ref}-${v.alt}`) +
        "?dataset=gnomad_r2_1",
    ),
    a(
      "ClinVar",
      `${chr}:${n}:${v.ref}:${v.alt}(GRCh37)`,
      "https://www.ncbi.nlm.nih.gov/clinvar/?term=" +
        e(`${chr}:${n}:${v.ref}:${v.alt}(GRCh37)`),
    ),
    a(
      "cBioPortal",
      oql,
      "https://www.cbioportal.org/ln?q=" + e(oql),
      codon
        ? "Codon fallback; no tumor type supplied."
        : "Requires gene and an explicit amino-acid position.",
      !!oql,
    ),
    a(
      "PubMed literature search",
      literature,
      "https://pubmed.ncbi.nlm.nih.gov/?term=" + e(literature),
      "Literature search, not curated variant evidence.",
    ),
  ].map((x) =>
    build === "hg19"
      ? x
      : {
          ...x,
          enabled: false,
          note: "These provider links are restricted to hg19/GRCh37.",
        },
  );
}
