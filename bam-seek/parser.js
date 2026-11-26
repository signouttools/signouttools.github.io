import { validateVariant, contigKey } from "./core.js";
const blank = () => ({
  gene: "",
  transcript: "",
  coding: "",
  protein: "",
  type: "",
});
const position = (x) => {
  if (!/^[\d,]+$/.test(x)) throw Error("Invalid genomic position");
  const n = Number(x.replaceAll(",", ""));
  if (!Number.isSafeInteger(n) || n < 1 || n > Number.MAX_SAFE_INTEGER - 20000)
    throw Error("Invalid genomic position");
  return n - 1;
};
function variant(chr, pos, ref, alt, extra = {}) {
  const v = {
    ...blank(),
    chr,
    pos: position(pos),
    ref: ref.toUpperCase(),
    alt: alt.toUpperCase(),
    ...extra,
  };
  validateVariant(v);
  return v;
}
function parseLine(line) {
  let cols = line.split(/\s+/),
    report = line.includes("\t") ? line.split("\t").map((x) => x.trim()) : cols;
  if (/^IGV /i.test(report[0]))
    report = ["IGV", report[0].slice(4).trim(), ...report.slice(1)];
  const off = report[0].toUpperCase() === "IGV" ? 1 : 0;
  if (report.length > off + 1 && /^[\d,]+$/.test(report[off + 1])) {
    const ci = report.findIndex((x, i) => i >= off + 3 && /^c\./i.test(x));
    if (ci >= 0) {
      let ai = ci + 1,
        protein = "";
      if (/^p\./i.test(report[ai])) protein = report[ai++];
      else if (report[ai] === "") ai++;
      let ti = off + 3,
        transcript = "";
      if (/^(ENST|ENSMUST|[NX][MR]_|LRG_)/i.test(report[ti]))
        transcript = report[ti++];
      if (ci <= ti || report.length <= ai + 1)
        throw Error("Report row requires gene, type, c. notation, REF and ALT");
      return variant(report[off], report[off + 1], report[ai], report[ai + 1], {
        gene: report[off + 2],
        type: report.slice(ti, ci).join(" "),
        transcript,
        coding: report[ci],
        protein,
      });
    }
  }
  const clin = line.match(
    /^(\S+)\s+(?:(\S+?)(?::|\s+))?(c\.\S+)(?:\s+(p\.\S+))?(?:\s+(.+))?$/,
  );
  if (clin) {
    if (!clin[5])
      throw Error(
        "Clinical-only notation requires a genomic coordinate and REF/ALT",
      );
    return {
      ...parseLine(clin[5]),
      gene: clin[1],
      transcript: clin[2] || "",
      coding: clin[3],
      protein: clin[4] || "",
    };
  }
  let m = line.match(
    /^([^\s:]+):(?:g\.)?([\d,]+)\s*([ACGTN]+)\s*>\s*([ACGTN]+)$/i,
  );
  if (m) return variant(m[1], m[2], m[3], m[4]);
  if (cols.length >= 4)
    return variant(
      cols[0],
      cols[1],
      cols[cols.length >= 5 ? 3 : 2],
      cols[cols.length >= 5 ? 4 : 3],
    );
  throw Error(
    "Expected chr:position REF>ALT, genomic HGVS, VCF columns, or a report row",
  );
}
export function parseDetailed(text) {
  const variants = [],
    errors = [];
  const lines = text.split(/\r?\n/);
  for (let i = 0; i < lines.length; i++) {
    const line = lines[i].trim();
    if (!line || line.startsWith("#") || /^IGV$/i.test(line)) continue;
    if (variants.length + errors.length >= 10000) {
      errors.push("Input is limited to 10,000 query lines");
      break;
    }
    try {
      variants.push({ ...parseLine(line), label: line });
    } catch (e) {
      errors.push(`Line ${i + 1}: ${e.message}`);
    }
  }
  return { variants, errors };
}
export function parse(text) {
  const p = parseDetailed(text);
  if (p.errors.length) throw Error(p.errors.join("\n"));
  return p.variants;
}
const same = (a, b) => !!a && !!b && a.toUpperCase() === b.toUpperCase();
export function sameVariant(a, b) {
  if (
    same(a.gene, b.gene) &&
    (same(a.coding, b.coding) || same(a.protein, b.protein))
  )
    return true;
  if (a.gene || b.gene) return false;
  return (
    contigKey(a.chr) === contigKey(b.chr) &&
    a.pos === b.pos &&
    a.ref === b.ref &&
    a.alt === b.alt
  );
}
export function classifyVariants(current, historical) {
  const result = [];
  for (const [list, role] of [
    [current, "Current"],
    [historical, "Historical"],
  ])
    for (const v of list) {
      const old = result.find((x) => sameVariant(x, v));
      if (!old) {
        result.push({ ...v, role });
        continue;
      }
      for (const k of ["gene", "transcript", "coding", "protein", "type"])
        if (!old[k]) old[k] = v[k];
      if (old.role !== role) old.role = "Both";
    }
  return result;
}
