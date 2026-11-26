import { test } from "node:test";
import assert from "node:assert/strict";
import {
  parse,
  parseDetailed,
  classifyVariants,
  count,
  defaults,
  phase,
} from "./core.js";
import { links, hgvsg } from "./resources.js";
import { comparison } from "./comparison.js";
import { panel } from "./panel.js";
test("report metadata and blank protein columns remain aligned", () => {
  const v = parse(
    "IGV X\t53448856\tSMC1A\tENST00000322213.4\tINTRON\tc.109+582_109+585delACCGinsCCCC\t\tCGGT\tGGGG\tCATAGXGGGGG\t22.8",
  )[0];
  assert.deepEqual(
    [v.chr, v.pos, v.ref, v.alt, v.protein, v.type, v.transcript],
    ["X", 53448855, "CGGT", "GGGG", "", "INTRON", "ENST00000322213.4"],
  );
  const d = parse(
    "5 176943930 DDX41 ENST00000507955.1 MISSENSE c.17C>T p.P6L G A GTTCGXGTTCC 4.4 19 45",
  )[0];
  assert.equal(d.gene, "DDX41");
  assert.equal(d.ref, "G");
});
test("clinical labels require exact complete genomic alleles", () => {
  for (const line of [
    "BRAF c.1799T>A p.V600E",
    "chr1:10 A>A",
    "chr1:10 A><script>",
    "chr1:0 A>T",
    "chr1:5 A>TC",
    "chr1:1 A>T trailing",
  ])
    assert.equal(parseDetailed(line).errors.length, 1, line);
  assert.equal(parse("chr7:g.140453136A>T")[0].pos, 140453135);
  assert.equal(parse("7 140453136 . A T")[0].ref, "A");
  assert.equal(parse("#comment\nIGV\n").length, 0);
});
test("annotation dedup merges metadata and tracks Both", () => {
  const a = parse("JAK2 c.1849G>T p.V617F chr9:5073770 G>T"),
    b = parse("jak2 c.999G>A p.V617F 9:5073770 G>T");
  const c = classifyVariants([...a, ...a], b);
  assert.equal(c.length, 1);
  assert.equal(c[0].role, "Both");
  assert.equal(
    classifyVariants(parse("chr9:5073770 G>T"), parse("9:5073770 G>T"))[0].role,
    "Both",
  );
});
test("RX grouping distinguishes genomic templates and UB includes cell barcode", () => {
  const v = parse("1:1 A>T")[0],
    r = (name, start, tag) => ({
      name,
      start,
      end: 2,
      ref_id: 0,
      next_refid: 0,
      next_pos: start,
      template_length: 50,
      mq: 60,
      flags: 0,
      seq: "T",
      qual: new Uint8Array([40]),
      CIGAR: "1M",
      tags: tag,
    });
  const rs = [
    r("a", 0, { RX: "AAA" }),
    r("b", 0, { RX: "AAA" }),
    r("c", 0, { RX: "BBB" }),
    r("d", 0, {}),
  ];
  assert.equal(count(rs, v, { ...defaults, mode: "tag", tag: "RX" }).mA, 3);
  assert.equal(
    count(rs, v, { ...defaults, mode: "auto" }).tag,
    "paired fragments by read name",
  );
  const cells = [
    r("a", 0, { UB: "AAA", CB: "one" }),
    r("b", 0, { UB: "AAA", CB: "two" }),
  ];
  assert.equal(count(cells, v, { ...defaults, mode: "tag", tag: "UB" }).mA, 2);
});
test("same-name improper mates do not establish phase", () => {
  const a = parse("1:1 A>T")[0],
    b = parse("1:20 A>T")[0],
    r = (start, flags) => ({
      name: "x",
      start,
      end: start + 1,
      seq: "T",
      qual: new Uint8Array([40]),
      CIGAR: "1M",
      mq: 60,
      flags,
      tags: {},
    });
  assert.equal(
    phase([r(0, 65), r(19, 129)], a, b, defaults).status,
    "Too far apart to phase",
  );
});
test("provider identifiers never contain original text or sample metadata", () => {
  const v = {
    ...parse("BRAF c.1799T>A p.V600E chr7:140453136 A>T")[0],
    label: "SECRET_patient/path.bam",
    type: "missense",
  };
  const ls = links(v);
  assert.equal(ls.length, 10);
  assert.ok(ls.every((l) => !JSON.stringify(l).includes("SECRET")));
  assert.ok(ls.find((l) => l.name === "ProtVar / AlphaMissense").enabled);
  assert.equal(ls.find((l) => l.name === "cBioPortal").id, "BRAF:MUT=V600E");
  assert.ok(
    links({ ...v, protein: "p.600?" }).find((l) => l.name === "cBioPortal")
      .enabled === false,
  );
  assert.ok(links(v, "hg38").every((l) => !l.enabled));
  assert.equal(hgvsg(parse("1:10 AT>A")[0]), "1:g.11del");
  assert.equal(hgvsg(parse("1:10 A>AT")[0]), "1:g.10_11insT");
});
test("comparison includes detected, absent and lost, excludes Both", () => {
  const sources = [
      { id: "a", name: "old-A.bam" },
      { id: "b", name: "old-B.bam" },
      { id: "c", name: "current.bam", current: true },
    ],
    v = (gene, coding, protein, role) => ({
      ...parse("1:1 A>T")[0],
      gene,
      coding,
      protein,
      role,
    }),
    a = v("JAK2", "c.1849G>T", "p.V617F", "Current"),
    b = v("NOTCH1", "c.7330C>T", "p.Q2444*", "Current"),
    lost = v("TET2", "c.5162T>G", "p.L1721W", "Historical"),
    both = v("TP53", "c.743G>A", "p.R248Q", "Both"),
    r = (id, v, A, R, mA) => ({ id, v, counts: { A, R, mA, available: true } });
  const text = comparison(
    [
      r("a", a, 2, 98, 1),
      r("b", a, 0, 80, 0),
      r("a", b, 0, 75, 0),
      r("c", lost, 0, 120, 0),
      r("a", both, 10, 90, 5),
    ],
    sources,
  );
  assert.ok(
    text.includes(
      "old-A.bam: JAK2 c.1849G>T (p.V617F, 2/100 consensus reads, 1 molecule)",
    ),
  );
  assert.ok(
    text.includes(
      "NOTCH1 c.7330C>T (0 ALT reads across 1 historical sample; 75 total REF reads)",
    ),
  );
  assert.ok(text.includes("previously reported TET2"));
  assert.ok(!text.includes("TP53"));
});
test("fixed panel has all disease groups and unique site reuse", () => {
  assert.equal(panel.length, 11);
  assert.equal(
    new Set(
      panel.flatMap((g) =>
        g.variants.map((v) => [v.chr, v.pos, v.ref, v.alt].join(":")),
      ),
    ).size,
    15,
  );
  assert.match(
    panel.find((g) => g.name === "CLL or MCL").note,
    /pipeline-managed/,
  );
});

test("failed and zero-coverage retrospective queries do not imply absence", () => {
  const v = { ...parse("1:1 A>T")[0], role: "Current" },
    sources = [{ id: "a", name: "old.bam" }];
  assert.match(
    comparison([{ id: "a", v, error: "Contig unavailable" }], sources),
    /Comparison incomplete/,
  );
  assert.match(
    comparison(
      [{ id: "a", v, counts: { R: 0, A: 0, available: false } }],
      sources,
    ),
    /Comparison incomplete/,
  );
});
