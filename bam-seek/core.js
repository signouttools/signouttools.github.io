// Allele and molecule rules ported from bam-seek evidence_engine.cpp.
export const defaults = {
  mapq: 20,
  baseq: 20,
  duplicates: false,
  secondary: false,
  supplementary: false,
  mode: "name",
  tag: "MI",
  support: 2,
  conflict: 0.1,
  minVaf: 0,
  minReads: 1,
  minMolecules: 1,
};
export const contigKey = (s) =>
  String(s).toLowerCase().replace(/^chr/, "").replace(/^m$/, "mt");
export const key = (v) => [contigKey(v.chr), v.pos, v.ref, v.alt].join(":");
export const identifier = (v) => `${v.chr}:${v.pos + 1} ${v.ref}>${v.alt}`;
export function validateSettings(s) {
  for (const k of ["mapq", "baseq"])
    if (!Number.isInteger(s[k]) || s[k] < 0 || s[k] > 255)
      throw Error(`${k} must be an integer from 0 to 255`);
  for (const k of ["minReads", "minMolecules", "support"])
    if (!Number.isInteger(s[k]) || s[k] < 1)
      throw Error(`${k} must be a positive integer`);
  for (const k of ["minVaf", "conflict"])
    if (!Number.isFinite(s[k]) || s[k] < 0 || s[k] > 1)
      throw Error(`${k} must be between 0 and 1`);
  if (
    !["name", "auto", "tag"].includes(s.mode) ||
    (s.mode === "tag" && !/^[A-Za-z][A-Za-z0-9]$/.test(s.tag))
  )
    throw Error("Choose a valid molecule mode and two-character BAM tag");
}
export function resolveContig(refs, chr) {
  const exact = refs.find((r) => r.refName === chr);
  if (exact) return exact;
  const matches = refs.filter((r) => contigKey(r.refName) === contigKey(chr));
  if (matches.length !== 1)
    throw Error(`Contig unavailable or ambiguous: ${chr}`);
  return matches[0];
}
export function validateVariant(v) {
  if (
    !v.chr ||
    !Number.isSafeInteger(v.pos) ||
    v.pos < 0 ||
    !v.ref ||
    !v.alt ||
    v.ref.length > 10000 ||
    v.alt.length > 10000 ||
    !/^([ACGTN]+)$/.test(v.ref) ||
    !/^([ACGTN]+)$/.test(v.alt) ||
    v.ref === v.alt ||
    (v.ref.length !== v.alt.length &&
      !v.ref.startsWith(v.alt) &&
      !v.alt.startsWith(v.ref))
  )
    throw Error("Invalid variant; small indels require a shared left anchor");
}
export function allowed(r, s) {
  return (
    !(r.flags & 4) &&
    r.mq >= s.mapq &&
    (s.duplicates || !(r.flags & 1024)) &&
    (s.secondary || !(r.flags & 256)) &&
    (s.supplementary || !(r.flags & 2048))
  );
}
export function layout(r) {
  const bases = new Map(),
    ins = new Map(),
    del = [];
  let p = r.start,
    q = 0;
  for (const m of r.CIGAR.matchAll(/(\d+)([MIDNSHP=X])/g)) {
    const n = +m[1],
      op = m[2];
    if ("M=X".includes(op)) {
      for (let i = 0; i < n && q + i < r.seq.length; i++)
        bases.set(p + i, [r.seq[q + i].toUpperCase(), r.qual?.[q + i] ?? 0]);
      p += n;
      q += n;
    } else if (op === "I") {
      if (q < r.seq.length && p > r.start) {
        let quality = 255;
        for (let i = 0; i < n; i++)
          quality = Math.min(quality, r.qual?.[q + i] ?? 0);
        ins.set(p - 1, [r.seq.slice(q, q + n).toUpperCase(), quality]);
      }
      q += n;
    } else if (op === "D" || op === "N") {
      del.push([p, p + n, op]);
      p += n;
    } else if (op === "S") q += n;
  }
  return { bases, ins, del };
}
export function allele(r, v) {
  const { bases, ins, del } = layout(r);
  const deleted = (p) => del.some((d) => p >= d[0] && p < d[1]);
  const covered = (seq, match) => {
    let q = 255;
    for (let i = 0; i < seq.length; i++) {
      const b = bases.get(v.pos + i);
      if (!b || deleted(v.pos + i) || (match && b[0] !== seq[i])) return null;
      q = Math.min(q, b[1]);
    }
    return q;
  };
  const insertionQ = (start, end) => {
    const a = [...ins]
      .filter(([p]) => p >= start && p <= end)
      .map(([, x]) => x[1]);
    return a.length ? Math.min(...a) : null;
  };
  if (!bases.has(v.pos) && !deleted(v.pos)) return ["N", 0];
  const R = covered(v.ref, true),
    A = covered(v.alt, true),
    anchor = v.pos + v.ref.length - 1,
    aq = covered("A", false) ?? 0;
  if (v.ref.length === v.alt.length) {
    const q = covered(v.ref, false);
    if (q === null) return ["O", aq];
    const iq = insertionQ(v.pos, anchor);
    if (iq !== null) return ["O", Math.min(q, iq)];
    return A !== null ? ["A", A] : R !== null ? ["R", R] : ["O", q];
  }
  if (v.alt.length > v.ref.length) {
    const i = ins.get(anchor),
      boundary = del.some((d) => d[0] <= anchor + 1 && anchor + 1 < d[1]);
    if (R !== null && i?.[0] === v.alt.slice(v.ref.length))
      return ["A", Math.min(R, i[1])];
    if (R !== null && !i && !boundary) return ["R", R];
    return ["O", i ? Math.min(R ?? aq, i[1]) : (R ?? aq)];
  }
  const ds = v.pos + v.alt.length,
    de = v.pos + v.ref.length,
    expected = del.some((d) => d[2] === "D" && d[0] === ds && d[1] === de),
    iq = insertionQ(v.pos, de - 1);
  if (A !== null && expected && iq === null) return ["A", A];
  if (R !== null && iq === null) return ["R", R];
  return ["O", iq === null ? (R ?? A ?? aq) : Math.min(R ?? A ?? aq, iq)];
}
export function call(r, v, s) {
  const [a, q] = allele(r, v);
  return a === "N" ? "N" : q < s.baseq ? "Q" : a;
}
export function consensus(cs) {
  const n = { A: 0, R: 0, O: 0 };
  for (const c of cs) if (c in n) n[c]++;
  return n.A > n.R && n.A > n.O ? "A" : n.R > n.A && n.R > n.O ? "R" : "O";
}
const tagValue = (r, t) =>
  r.tags?.[t] === undefined || r.tags[t] === "" ? null : String(r.tags[t]);
export function chooseTag(rs, s) {
  if (s.mode === "name") return "";
  if (s.mode === "tag") return s.tag;
  return (
    ["MI", "RX", "UB"].find(
      (t) =>
        rs.length &&
        rs.filter((r) => tagValue(r, t) !== null).length / rs.length >= 0.9,
    ) || ""
  );
}
export function recordKey(r) {
  return [r.name, r.ref_id, r.start, r.end, r.flags, r.CIGAR, r.seq].join("|");
}
export function fragmentKey(r) {
  return r.name
    ? "pair|" + r.name
    : "alignment|" + [r.ref_id, r.start, r.end, r.flags].join("|");
}
export function moleculeKey(r, t) {
  const v = tagValue(r, t);
  if (v === null) return "";
  if (t !== "RX" && t !== "UB") return v;
  const start =
    r.next_refid === r.ref_id && r.next_pos >= 0
      ? Math.min(r.start, r.next_pos)
      : r.start;
  return (
    (t === "UB" ? (tagValue(r, "CB") ?? "no-CB") + "|" : "") +
    v +
    "|" +
    r.ref_id +
    ":" +
    start +
    "|" +
    Math.abs(r.template_length || 0)
  );
}
export function count(records, v, s) {
  validateSettings(s);
  validateVariant(v);
  const out = {
    R: 0,
    A: 0,
    O: 0,
    N: 0,
    Q: 0,
    filtered: 0,
    overlapping: records.length,
    mR: 0,
    mA: 0,
    mO: 0,
    missing: 0,
    RF: 0,
    RR: 0,
    AF: 0,
    AR: 0,
  };
  const called = [];
  for (const r of records) {
    if (!allowed(r, s)) {
      out.filtered++;
      continue;
    }
    const c = call(r, v, s);
    if (c === "N" || c === "Q") {
      out[c]++;
      continue;
    }
    called.push({ r, c });
  }
  const tag = chooseTag(
      called.map((x) => x.r),
      s,
    ),
    groups = new Map();
  let fallback = false;
  for (const { r, c } of called) {
    out[c]++;
    if (c === "A" || c === "R") out[c + (r.flags & 16 ? "R" : "F")]++;
    let id = tag ? moleculeKey(r, tag) : "";
    if (!id) {
      if (tag) out.missing++;
      id = fragmentKey(r);
      fallback = true;
    }
    if (!groups.has(id)) groups.set(id, []);
    groups.get(id).push(c);
  }
  for (const cs of groups.values()) out["m" + consensus(cs)]++;
  out.available = groups.size > 0;
  out.tag =
    (tag || "paired fragments by read name") +
    (tag && fallback ? " + pair fallback" : "");
  out.detected =
    out.A >= s.minReads &&
    out.A / (out.A + out.R) >= s.minVaf &&
    out.available &&
    out.mA >= s.minMolecules;
  return out;
}
export function phase(records, a, b, s) {
  const c = {
    AB: 0,
    Ab: 0,
    aB: 0,
    ab: 0,
    noninformative: 0,
    missing: 0,
    distance: Math.abs(a.pos - b.pos),
    reason: "",
    status: "Indeterminate",
  };
  if (contigKey(a.chr) !== contigKey(b.chr))
    return {
      ...c,
      distance: -1,
      status: "Too far apart to phase",
      reason: "The variants are on different contigs.",
    };
  const called = [];
  for (const r of records) {
    if (!allowed(r, s)) continue;
    for (const [l, v] of [
      [0, a],
      [1, b],
    ]) {
      const x = call(r, v, s);
      if (x !== "N" && x !== "Q") called.push({ r, l, x });
    }
  }
  const tag = chooseTag(
      called.map((x) => x.r),
      s,
    ),
    groups = new Map();
  let fallback = false;
  for (const x of called) {
    let id = tag ? moleculeKey(x.r, tag) : "",
      tagged = !!id;
    if (!id) {
      if (tag) c.missing++;
      id = fragmentKey(x.r);
      fallback = true;
    }
    if (!groups.has(id)) groups.set(id, { calls: [[], []], tagged: false });
    const g = groups.get(id);
    g.tagged ||= tagged;
    g.calls[x.l].push(x);
  }
  c.tag =
    (tag || "paired fragments by read name") +
    (tag && fallback ? " + pair fallback" : "");
  for (const g of groups.values()) {
    const [left, right] = g.calls,
      linked =
        g.tagged ||
        left.some((x) =>
          right.some(
            (y) =>
              recordKey(x.r) === recordKey(y.r) ||
              ((x.r.flags & 3) === 3 &&
                (y.r.flags & 3) === 3 &&
                ((x.r.flags & 64 && y.r.flags & 128) ||
                  (x.r.flags & 128 && y.r.flags & 64))),
          ),
        );
    const x = consensus(left.map((x) => x.x)),
      y = consensus(right.map((x) => x.x));
    if (!linked || ![x, y].every((x) => x === "A" || x === "R")) {
      c.noninformative++;
      continue;
    }
    c[(x === "A" ? "A" : "a") + (y === "A" ? "B" : "b")]++;
  }
  const total = c.AB + c.Ab + c.aB;
  if (!total && !c.ab)
    return {
      ...c,
      status: "Too far apart to phase",
      reason:
        "No high-quality molecule directly observed both variant positions.",
    };
  if (!total)
    return {
      ...c,
      reason:
        "Molecules span both positions, but none contains either alternate allele.",
    };
  const cis = c.AB >= s.support && (c.Ab + c.aB) / total <= s.conflict,
    trans =
      c.Ab >= s.support && c.aB >= s.support && c.AB / total <= s.conflict;
  if (cis && !trans)
    return {
      ...c,
      status: "Cis",
      reason:
        "ALT/ALT molecules meet the configured support and conflict thresholds.",
    };
  if (trans && !cis)
    return {
      ...c,
      status: "Trans",
      reason:
        "Reciprocal ALT/REF and REF/ALT molecules meet the configured support and conflict thresholds.",
    };
  return {
    ...c,
    reason:
      c.AB && c.Ab + c.aB
        ? "Conflicting cis- and trans-supporting molecules exceed the configured conflict threshold."
        : "Direct linkage was observed, but the configured molecule-support threshold was not met.",
  };
}
export { parse, parseDetailed, classifyVariants } from "./parser.js";
