// Experimental tumor-context helper-marker phasing, ported from the native engine.
import {
  allowed,
  layout,
  call,
  consensus,
  chooseTag,
  moleculeKey,
  recordKey,
  key,
} from "./core.js";
function group(records, s) {
  const tag = chooseTag(records, s),
    groups = new Map();
  let missing = 0,
    fallback = false;
  for (const r of records) {
    let id = tag ? moleculeKey(r, tag) : "";
    if (!id) {
      if (tag) missing++;
      fallback = true;
      id = r.name && (r.flags & 3) === 3 ? "pair|" + r.name : recordKey(r);
    }
    if (!groups.has(id)) groups.set(id, []);
    groups.get(id).push(r);
  }
  return {
    groups: [...groups.values()],
    tag:
      (tag || "paired fragments by read name") +
      (tag && fallback ? " + pair fallback" : ""),
    missing,
  };
}
function observations(groups, variants, s) {
  return groups.map((rs) => {
    const targets = variants.map((v) =>
        consensus(
          rs.map((r) => call(r, v, s)).filter((c) => c !== "N" && c !== "Q"),
        ),
      ),
      votes = new Map();
    for (const r of rs) {
      if (r.mq < Math.max(30, s.mapq)) continue;
      for (const [p, [b, q]] of layout(r).bases) {
        if (q < Math.max(30, s.baseq) || !/[ACGT]/.test(b)) continue;
        if (!votes.has(p)) votes.set(p, new Map());
        const site = votes.get(p),
          vote = site.get(b) || { count: 0, strand: 0 };
        vote.count++;
        vote.strand |= r.flags & 16 ? 2 : 1;
        site.set(b, vote);
      }
    }
    const bases = new Map(),
      strands = new Map();
    for (const [p, site] of votes) {
      const sorted = [...site].sort((a, b) => b[1].count - a[1].count);
      if (sorted[0][1].count > (sorted[1]?.[1].count || 0)) {
        bases.set(p, sorted[0][0]);
        strands.set(p, sorted[0][1].strand);
      }
    }
    return { targets, bases, strands };
  });
}
function markers(molecules, variants, s, exclude = true) {
  const sites = new Map(),
    support = Math.max(3, s.support);
  for (const m of molecules)
    for (const [p, b] of m.bases) {
      if (
        exclude &&
        variants.some(
          (v) => p >= v.pos && p < v.pos + Math.max(v.ref.length, v.alt.length),
        )
      )
        continue;
      if (!sites.has(p)) sites.set(p, new Map());
      const site = sites.get(p),
        x = site.get(b) || { count: 0, strand: 0 };
      x.count++;
      x.strand |= m.strands.get(p);
      site.set(b, x);
    }
  const rare = [],
    common = [];
  for (const [pos, site] of [...sites].sort((a, b) => a[0] - b[0])) {
    const total = [...site.values()].reduce((n, x) => n + x.count, 0),
      alleles = [...site]
        .filter(([, x]) => x.count >= support)
        .sort((a, b) => b[1].count - a[1].count || a[0].localeCompare(b[0]));
    if (alleles.length !== 2) continue;
    const fraction = alleles[1][1].count / total,
      m = { pos, alleles: alleles.map((x) => x[0]), fraction };
    if (fraction >= 0.02 && fraction <= 0.2 && alleles[1][1].strand === 3)
      rare.push(m);
    if (fraction >= 0.3 && alleles.every((x) => x[1].strand === 3))
      common.push(m);
  }
  return { rare, common };
}
function path(graph, start, end) {
  const parent = new Map([[start, start]]),
    parity = new Map([[start, 0]]),
    pending = [start];
  let conflicted = false;
  for (let i = 0; i < pending.length; i++) {
    const p = pending[i];
    for (const e of graph[p]) {
      const expected = parity.get(p) ^ e.parity;
      if (parity.has(e.to)) {
        if (parity.get(e.to) !== expected) conflicted = true;
        continue;
      }
      parent.set(e.to, p);
      parity.set(e.to, expected);
      pending.push(e.to);
    }
  }
  if (!parent.has(end)) return null;
  const chain = [end];
  while (chain.at(-1) !== start) chain.push(parent.get(chain.at(-1)));
  return { chain: chain.reverse(), parity: parity.get(end), conflicted };
}
export async function localPhase(variants, query, s, check = () => {}) {
  const vs = [...new Map(variants.map((v) => [key(v), v])).values()].sort(
    (a, b) => a.chr.localeCompare(b.chr) || a.pos - b.pos,
  );
  if (vs.length < 2) return [];
  const records = new Map(),
    queried = new Set(vs.map((v) => v.pos)),
    mates = new Set();
  const add = (rs) => {
    let added = false;
    for (const r of rs) {
      if (allowed(r, s) && !records.has(recordKey(r))) {
        records.set(recordKey(r), r);
        added = true;
      }
    }
    return added;
  };
  for (const v of vs) add(await query(v.chr, v.pos, v.pos + v.ref.length));
  let limited = false;
  const start = vs[0].pos,
    end = vs.at(-1).pos + Math.max(vs.at(-1).ref.length, vs.at(-1).alt.length);
  if (vs.every((v) => v.chr === vs[0].chr))
    for (let round = 0; round < 32; round++) {
      check();
      for (const r of [...records.values()]) {
        if (
          !r.name ||
          (r.flags & 3) !== 3 ||
          r.next_refid !== r.ref_id ||
          r.next_pos < start ||
          r.next_pos >= end
        )
          continue;
        const mk = r.name + "|" + r.next_pos;
        if (mates.has(mk)) continue;
        mates.add(mk);
        add(
          (await query(vs[0].chr, r.next_pos, r.next_pos + 1)).filter(
            (m) =>
              m.name === r.name &&
              ((r.flags & 64 && m.flags & 128) ||
                (r.flags & 128 && m.flags & 64)),
          ),
        );
      }
      const grouped = group([...records.values()], s),
        ms = observations(grouped.groups, vs, s);
      for (const m of ms)
        for (const p of [...m.bases.keys()])
          if (p < start || p >= end) {
            m.bases.delete(p);
            m.strands.delete(p);
          }
      const discovered = markers(ms, vs, s, false),
        frontier = [...discovered.rare, ...discovered.common]
          .map((x) => x.pos)
          .filter((p) => !queried.has(p))
          .sort((a, b) => a - b);
      if (!frontier.length) break;
      let added = false;
      for (const pos of frontier) {
        if (queried.size >= 2000 || records.size >= 100000) {
          limited = true;
          break;
        }
        queried.add(pos);
        added = add(await query(vs[0].chr, pos, pos + 1)) || added;
      }
      if (!added || limited) break;
      if (round === 31) limited = true;
    }
  const grouped = group([...records.values()], s),
    molecules = observations(grouped.groups, vs, s),
    { rare, common } = markers(molecules, vs, s),
    support = Math.max(3, s.support);
  const present = (m, i) => m.bases.get(rare[i].pos) === rare[i].alleles[1],
    commonAllele = (m, i) =>
      common[i].alleles.indexOf(m.bases.get(common[i].pos));
  const rareAnchors = vs.map((v, t) =>
    rare.flatMap((m, i) =>
      molecules.filter((x) => x.targets[t] === "A" && present(x, i)).length >=
      support
        ? [{ marker: i }]
        : [],
    ),
  );
  const rareGraph = rare.map(() => []);
  for (let i = 0; i < rare.length; i++)
    for (let j = i + 1; j < rare.length; j++)
      if (
        molecules.filter((m) => present(m, i) && present(m, j)).length >=
        support
      ) {
        rareGraph[i].push({ to: j, parity: 0 });
        rareGraph[j].push({ to: i, parity: 0 });
      }
  const commonAnchors = vs.map((v, t) =>
    common.flatMap((m, i) => {
      const counts = [0, 0];
      for (const x of molecules)
        if (x.targets[t] === "A") {
          const a = commonAllele(x, i);
          if (a >= 0) counts[a]++;
        }
      const allele = counts[1] > counts[0] ? 1 : 0;
      return counts[allele] >= support &&
        counts[1 - allele] / (counts[0] + counts[1]) <= s.conflict
        ? [{ marker: i, allele }]
        : [];
    }),
  );
  const commonGraph = common.map(() => []);
  for (let i = 0; i < common.length; i++)
    for (let j = i + 1; j < common.length; j++) {
      const n = [
        [0, 0],
        [0, 0],
      ];
      for (const m of molecules) {
        const a = commonAllele(m, i),
          b = commonAllele(m, j);
        if (a >= 0 && b >= 0) n[a][b]++;
      }
      const diagonal = n[0][0] + n[1][1],
        off = n[0][1] + n[1][0],
        total = diagonal + off;
      let parity = -1;
      if (
        total &&
        n[0][0] >= support &&
        n[1][1] >= support &&
        off / total <= s.conflict
      )
        parity = 0;
      if (
        total &&
        n[0][1] >= support &&
        n[1][0] >= support &&
        diagonal / total <= s.conflict
      )
        parity = parity < 0 ? 1 : -1;
      if (parity >= 0) {
        commonGraph[i].push({ to: j, parity });
        commonGraph[j].push({ to: i, parity });
      }
    }
  const results = [];
  for (let i = 0; i < vs.length; i++)
    for (let j = i + 1; j < vs.length; j++) {
      check();
      let cis = 0,
        trans = 0,
        same = 0,
        conflicted = 0,
        rarePath = null,
        commonPath = null,
        firstAllele = 0;
      for (const a of rareAnchors[i])
        for (const b of rareAnchors[j]) {
          const p = path(rareGraph, a.marker, b.marker);
          if (p) {
            cis++;
            if (!rarePath || p.chain.length < rarePath.length)
              rarePath = p.chain;
          }
        }
      for (const a of commonAnchors[i])
        for (const b of commonAnchors[j]) {
          const p = path(commonGraph, a.marker, b.marker);
          if (!p) continue;
          if (p.conflicted) {
            conflicted++;
            continue;
          }
          if ((a.allele ^ p.parity) !== b.allele) trans++;
          else same++;
          if (!commonPath || p.chain.length < commonPath.length) {
            commonPath = p.chain;
            firstAllele = a.allele;
          }
        }
      const status =
        vs[i].chr !== vs[j].chr
          ? "Unresolved"
          : cis && !trans
            ? "Cis"
            : trans && !cis && !same && !conflicted
              ? "Trans"
              : "Unresolved";
      let chain = [];
      if (status === "Cis")
        chain = rarePath.map(
          (n) => `${vs[i].chr}:${rare[n].pos + 1}${rare[n].alleles[1]}`,
        );
      if (status === "Trans") {
        let allele = firstAllele;
        chain = commonPath.map((n, k) => {
          if (k)
            allele ^= commonGraph[commonPath[k - 1]].find(
              (e) => e.to === n,
            ).parity;
          return `${vs[i].chr}:${common[n].pos + 1}${common[n].alleles[allele]}`;
        });
      }
      const reason =
        status === "Cis"
          ? "Repeated positive ALT co-occurrence connects both targets through rare markers."
          : status === "Trans"
            ? "ALT groups anchor to opposite alleles of a supported common-marker haplotype chain."
            : cis && trans
              ? "Rare-marker cis evidence conflicts with common-marker trans evidence."
              : trans && (same || conflicted)
                ? "Common-marker haplotype evidence is internally inconsistent."
                : "No supported marker chain establishes cis or trans; missing coverage is not a reference observation.";
      results.push({
        a: vs[i],
        b: vs[j],
        status,
        rare: rare.length,
        common: common.length,
        chains:
          status === "Cis"
            ? cis
            : status === "Trans"
              ? trans
              : Math.max(cis, trans),
        chain: chain.join(" → "),
        tag: grouped.tag,
        missing: grouped.missing,
        limited,
        reason:
          reason +
          (limited
            ? " Recruitment limit reached; results use the bounded evidence."
            : ""),
      });
    }
  return results;
}
