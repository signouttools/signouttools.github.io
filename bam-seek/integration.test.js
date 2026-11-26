import { test } from "node:test";
import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import { resolve } from "node:path";
import { Engine } from "./tests/engine-bundle.js";
import { defaults, parse } from "./core.js";
import { fixtureDir, fixtures, deepFixture } from "./scripts/fixtures.mjs";
await fixtures();
await deepFixture();
const file = async (name) =>
  new File([await readFile(resolve(fixtureDir, name))], name);
for (const index of ["evidence.bam.bai", "evidence.bam.csi"])
  test(`native evidence rules with ${index}`, async () => {
    const e = new Engine();
    await e.prepare("1", await file("evidence.bam"), await file(index));
    const vs = parse(
      "chr1:15 A>T\nchr1:35 A>AT\nchr1:55 AAA>A\n1:75 A>T\n1:85 A>AT",
    );
    const result = await e.run(["1"], vs, defaults);
    assert.deepEqual(
      result.rows.map((r) => [
        r.counts?.R,
        r.counts?.A,
        r.counts?.O,
        r.counts?.mR,
        r.counts?.mA,
      ]),
      [
        [2, 3, 2, 2, 3],
        [1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1],
        [2, 3, 0, 1, 2],
        [0, 2, 0, 0, 1],
      ],
    );
    const selected = await e.run(["1"], [vs[0]], {
      ...defaults,
      mode: "tag",
      tag: "MI",
    });
    assert.equal(selected.rows[0].counts.missing, 1);
    assert.equal(selected.rows[0].counts.tag, "MI + pair fallback");
    const auto = await e.run(["1"], [vs[0]], { ...defaults, mode: "auto" });
    assert.equal(auto.rows[0].counts.tag, "paired fragments by read name");
    const rerun = await e.run(["1"], vs, defaults);
    assert.equal(rerun.reused, 5);
    e.remove("1");
    assert.equal(e.cache.size, 0);
  });
test("native direct and experimental phase cases", async () => {
  const e = new Engine();
  await e.prepare(
    "1",
    await file("evidence.bam"),
    await file("evidence.bam.bai"),
  );
  const pairs = [
    [1, "C", 6, "G", "Cis"],
    [45, "C", 50, "G", "Trans"],
    [61, "C", 66, "G", "Indeterminate"],
    [4, "T", 6, "G", "Too far apart to phase"],
    [101, "C", 125, "C", "Cis"],
    [141, "C", 165, "C", "Trans"],
    [68, "T", 95, "C", "Unresolved"],
  ];
  for (let i = 0; i < pairs.length; i++) {
    const [a, aa, b, bb, expected] = pairs[i],
      vs = [
        {
          chr: "chr1",
          pos: a,
          ref: "A",
          alt: aa,
          gene: "TEST",
          role: "Current",
        },
        {
          chr: "chr1",
          pos: b,
          ref: "A",
          alt: bb,
          gene: "TEST",
          role: "Current",
        },
      ];
    const r = await e.run(["1"], vs, defaults);
    assert.equal(
      i < 4 ? r.phases[0].status : r.localPhases[0].status,
      expected,
      JSON.stringify(r),
    );
    if (i === 4) {
      const strict = await e.run(["1"], vs, { ...defaults, support: 4 });
      assert.equal(strict.localPhases[0].status, "Unresolved");
    }
  }
});
for (const index of ["deep.bam.bai", "deep.bam.csi"])
  test(`high depth retains 24,100 reads with ${index}`, async () => {
    const e = new Engine();
    await e.prepare("deep", await file("deep.bam"), await file(index));
    const r = await e.run(["deep"], parse("chr1:150 A>T"), defaults);
    assert.equal(r.rows[0].counts.A + r.rows[0].counts.R, 24100);
    assert.equal(r.rows[0].counts.mA + r.rows[0].counts.mR, 12050);
    assert.equal(r.rows[0].counts.A, 6026);
  });
test("bad source and cancellation report errors", async () => {
  const e = new Engine();
  await assert.rejects(() =>
    e.prepare(
      "bad",
      new File(["invalid"], "bad.bam"),
      new File(["invalid"], "bad.bai"),
    ),
  );
  const abort = new AbortController();
  abort.abort();
  await assert.rejects(
    () => e.run([], [], defaults, { signal: abort.signal }),
    { name: "AbortError" },
  );
});

test("running cancellation preserves completed cache and a later run recovers", async () => {
  const e = new Engine();
  await e.prepare(
    "1",
    await file("evidence.bam"),
    await file("evidence.bam.bai"),
  );
  const abort = new AbortController();
  await assert.rejects(
    () =>
      e.run(["1"], parse("chr1:15 A>T\nchr1:35 A>AT"), defaults, {
        signal: abort.signal,
        progress: () => abort.abort(),
      }),
    { name: "AbortError" },
  );
  const result = await e.run(
    ["1"],
    parse("chr1:15 A>T\nchr1:35 A>AT"),
    defaults,
  );
  assert.equal(result.rows.length, 2);
  assert.equal(result.reused, 1);
  assert.equal(result.calculated, 1);
});
