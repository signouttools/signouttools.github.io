import { BamFile } from "@gmod/bam";
import { BlobFile } from "generic-filehandle2";
import {
  count,
  phase,
  key,
  resolveContig,
  validateSettings,
  validateVariant,
} from "./core.js";
import { localPhase } from "./local-phase.js";
export class Engine {
  constructor() {
    this.sources = new Map();
    this.cache = new Map();
  }
  async prepare(id, bam, index) {
    const reader = new BamFile({
      bamFilehandle: new BlobFile(bam),
      [index.name.toLowerCase().endsWith(".csi")
        ? "csiFilehandle"
        : "baiFilehandle"]: new BlobFile(index),
    });
    await reader.getHeader();
    if (!reader.indexToChr?.length)
      throw Error("BAM header has no reference sequences");
    await reader.index.parse();
    this.sources.set(id, reader);
    return reader.indexToChr;
  }
  remove(id) {
    this.sources.delete(id);
    this.cache.delete(id);
  }
  clear() {
    this.sources.clear();
    this.cache.clear();
  }
  async run(
    ids,
    variants,
    s,
    { signal, progress = () => {}, local = true } = {},
  ) {
    validateSettings(s);
    const rows = [],
      phases = [],
      localPhases = [];
    let reused = 0,
      calculated = 0;
    const check = () => {
      if (signal?.aborted)
        throw new DOMException("Calculation cancelled", "AbortError");
    };
    check();
    const genes = new Map();
    for (const v of variants) {
      validateVariant(v);
      if (v.gene && v.role !== "Disease panel") {
        const g = v.gene.toUpperCase();
        if (!genes.has(g)) genes.set(g, []);
        if (!genes.get(g).some((x) => key(x) === key(v))) genes.get(g).push(v);
      }
    }
    for (const id of ids) {
      check();
      const bam = this.sources.get(id);
      if (!bam) continue;
      if (!this.cache.has(id)) this.cache.set(id, new Map());
      const cache = this.cache.get(id);
      const query = async (chr, start, end) => {
        check();
        const ref = resolveContig(bam.indexToChr, chr);
        if (start < 0 || start >= ref.length || end > ref.length)
          throw Error(`Query exceeds ${ref.refName} bounds`);
        const records = await bam.getRecordsForRange(ref.refName, start, end, {
          signal,
        });
        return records;
      };
      for (const v of variants) {
        check();
        const ck = "v|" + key(v) + "|" + JSON.stringify(s);
        try {
          let counts = cache.get(ck);
          if (counts) {
            reused++;
          } else {
            const ref = resolveContig(bam.indexToChr, v.chr);
            if (v.pos + v.ref.length > ref.length)
              throw Error("Variant exceeds contig bounds");
            const rs = await query(
              v.chr,
              Math.max(0, v.pos - 8),
              Math.min(ref.length, v.pos + v.ref.length + 8),
            );
            counts = count(rs, v, s);
            cache.set(ck, counts);
            calculated++;
          }
          rows.push({ id, v, counts });
        } catch (e) {
          if (e.name === "AbortError") throw e;
          rows.push({ id, v, error: e.message });
        }
        progress({
          done: rows.length,
          total: ids.length * variants.length,
          reused,
          calculated,
        });
        await new Promise((r) => setTimeout(r, 0));
      }
      for (const vs of genes.values()) {
        for (let i = 0; i < vs.length; i++)
          for (let j = i + 1; j < vs.length; j++) {
            check();
            const a = vs[i],
              b = vs[j],
              ck = "p|" + key(a) + "|" + key(b) + "|" + JSON.stringify(s);
            try {
              let p = cache.get(ck);
              if (!p) {
                const records = [
                  ...(await query(a.chr, a.pos, a.pos + a.ref.length)),
                  ...(await query(b.chr, b.pos, b.pos + b.ref.length)),
                ];
                p = phase(
                  [...new Map(records.map((r) => [r.fileOffset, r])).values()],
                  a,
                  b,
                  s,
                );
                cache.set(ck, p);
              }
              phases.push({ id, a, b, ...p });
            } catch (e) {
              if (e.name === "AbortError") throw e;
              phases.push({ id, a, b, error: e.message });
            }
            await new Promise((r) => setTimeout(r, 0));
          }
        if (local && vs.length > 1) {
          const ck = "l|" + vs.map(key).sort().join("|") + JSON.stringify(s);
          try {
            let lp = cache.get(ck);
            if (!lp) {
              lp = await localPhase(
                vs.map((v) => ({
                  ...v,
                  chr: resolveContig(bam.indexToChr, v.chr).refName,
                })),
                query,
                s,
                check,
              );
              cache.set(ck, lp);
            }
            const labels = new Map(vs.map((v) => [key(v), v]));
            localPhases.push(
              ...lp.map((p) => ({
                ...p,
                a: labels.get(key(p.a)) || p.a,
                b: labels.get(key(p.b)) || p.b,
                id,
              })),
            );
          } catch (e) {
            if (e.name === "AbortError") throw e;
            localPhases.push({ id, a: vs[0], b: vs.at(-1), error: e.message });
          }
        }
      }
    }
    check();
    return { rows, phases, localPhases, reused, calculated };
  }
}
