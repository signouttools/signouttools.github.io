import { identifier } from "./core.js";
import { sameVariant } from "./parser.js";
const name = (v) =>
  [v.gene, v.coding || v.protein].filter(Boolean).join(" ") || identifier(v);
export function natural(a) {
  return a.length < 2
    ? a[0] || ""
    : a.length === 2
      ? a.join(" and ")
      : a.slice(0, -1).join(", ") + ", and " + a.at(-1);
}
const present = (r) => r.counts.available && r.counts.mA > 0;
function item(r) {
  const c = r.counts,
    details = [];
  if (r.v.coding && r.v.protein) details.push(r.v.protein);
  details.push(`${c.A}/${c.A + c.R} consensus reads`);
  const n = c.available ? c.mA : "N/A";
  details.push(`${n} ${n === 1 ? "molecule" : "molecules"}`);
  return `${name(r.v)} (${details.join(", ")})`;
}
export function comparison(rows, sources) {
  const incomplete = rows.filter((r) => {
    const s = sources.find((s) => s.id === r.id);
    const needed =
      s &&
      ((!s.current && r.v.role === "Current") ||
        (s.current && r.v.role === "Historical"));
    return (
      needed && (r.error || !r.counts?.available || !(r.counts.A + r.counts.R))
    );
  });
  if (incomplete.length)
    return (
      "Comparison incomplete — failed queries or no informative coverage prevent a comparison across all required samples. Review: " +
      natural(
        incomplete.map(
          (r) =>
            (sources.find((s) => s.id === r.id)?.name || "Sample") +
            " " +
            identifier(r.v),
        ),
      ) +
      "."
    );
  const paragraphs = [],
    current = [],
    lost = [];
  for (const r of rows) {
    if (r.error || r.v.role === "Both" || r.v.role === "Disease panel")
      continue;
    const s = sources.find((s) => s.id === r.id);
    if (!s) continue;
    if (!s.current && r.v.role === "Current") {
      let g = current.find((g) => sameVariant(g.v, r.v));
      if (!g) {
        g = { v: r.v, rows: [] };
        current.push(g);
      }
      g.rows.push(r);
    } else if (s.current && r.v.role === "Historical") lost.push(r);
  }
  if (lost.length) {
    let p =
      "Historical variants not currently called — A detailed investigation in IGV does NOT identify the previously reported " +
      natural(lost.map(item)) +
      (lost.length > 1 ? " mutations" : " mutation") +
      " above the level of noise of the assay.";
    const low = lost.filter(present).map((r) => name(r.v));
    if (low.length)
      p +=
        " Low-level evidence is present for " +
        natural(low) +
        ", but remains below the applicable calling/detection threshold.";
    paragraphs.push(p);
  }
  const detected = current.filter((g) => g.rows.some(present)),
    absent = current.filter((g) => !g.rows.some(present));
  if (detected.length) {
    const labels = detected.map((g) => {
      const a = g.rows
        .filter(present)
        .map((r) => sources.find((s) => s.id === r.id).name + ": " + item(r));
      return a.length === 1 ? a[0] : name(g.v) + " [" + natural(a) + "]";
    });
    paragraphs.push(
      "Current variants with prior sub-threshold evidence — Targeted manual review of sequence reads from previous samples from this patient shows that the " +
        natural(labels) +
        (detected.length > 1
          ? " variants reported in the current sample were present previously, but at VAFs below the validated threshold for calling variants and, therefore, were not reported at those times. Accordingly, their presence now represents an increase in relative abundance, but not de novo new mutations for this patient."
          : " variant reported in the current sample was present previously, but at a VAF below the validated threshold for calling a variant and, therefore, was not reported at that time. Accordingly, its presence now represents an increase in relative abundance, but not a de novo new mutation for this patient."),
    );
  }
  if (absent.length) {
    const labels = absent.map(
      (g) =>
        name(g.v) +
        ` (0 ALT reads across ${g.rows.length} historical ${g.rows.length === 1 ? "sample" : "samples"}; ${g.rows.reduce((n, r) => n + r.counts.R, 0)} total REF reads)`,
    );
    paragraphs.push(
      "Completely new variants — Targeted manual review of sequence reads from all previous samples from this patient shows that the " +
        natural(labels) +
        (absent.length > 1
          ? " variants reported in the current sample were not present and, therefore, their presence in the current sample represents new mutations for this patient."
          : " variant reported in the current sample was not present and, therefore, its presence in the current sample represents a new mutation for this patient."),
    );
  }
  return paragraphs.join("\n\n");
}
export function phasingNarrative(phases, sources) {
  if (!phases.length) return "";
  return (
    "Read-based phasing:\n" +
    phases
      .filter((p) => !p.error)
      .map((p) => {
        const s = sources.find((s) => s.id === p.id),
          verb = {
            Cis: "are in cis",
            Trans: "are in trans",
            Indeterminate: "have indeterminate phase",
            "Too far apart to phase": "are too far apart to phase",
          }[p.status];
        return `${s.current ? "current" : "historical"} sample ${s.name}: ${p.a.gene || "Unannotated"} ${p.a.coding || p.a.protein || identifier(p.a)} and ${p.b.coding || p.b.protein || identifier(p.b)} ${verb} (${p.distance >= 0 ? p.distance + " bp apart; " : ""}${p.AB + p.Ab + p.aB + p.ab} informative molecule(s); AB=${p.AB}, Ab=${p.Ab}, aB=${p.aB}, ab=${p.ab}). ${p.reason}`;
      })
      .join("\n")
  );
}
