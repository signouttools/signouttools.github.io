import { test } from "node:test";
import assert from "node:assert/strict";
import { parse, count, defaults, phase } from "./core.js";
const r = (seq, name = "x", flags = 0) => ({
  seq,
  name,
  flags,
  start: 0,
  mq: 60,
  CIGAR: seq.length + "M",
  qual: new Uint8Array(seq.length).fill(40),
  tags: {},
});
test("parse genomic and annotated coordinates", () => {
  assert.equal(parse("chr7:140453136 A>T")[0].pos, 140453135);
  assert.equal(
    parse("BRAF c.1799T>A p.V600E chr7:140453136 A>T")[0].gene,
    "BRAF",
  );
});
test("read and fragment counts exclude filtered reads", () => {
  const v = { chr: "chr1", pos: 0, ref: "A", alt: "T" };
  const c = count(
    [r("A", "a"), r("T", "b"), r("T", "b"), r("T", "c", 1024)],
    v,
    defaults,
  );
  assert.equal(c.A, 2);
  assert.equal(c.mA, 1);
  assert.equal(c.R, 1);
  assert.equal(c.filtered, 1);
});
test("ambiguous fragments excluded", () => {
  const c = count(
    [r("A"), r("T")],
    { chr: "chr1", pos: 0, ref: "A", alt: "T" },
    defaults,
  );
  assert.equal(c.mO, 1);
  assert.equal(c.mA + c.mR, 0);
});
test("direct cis phase", () => {
  const a = { chr: "chr1", pos: 0, ref: "A", alt: "T" },
    b = { chr: "chr1", pos: 1, ref: "A", alt: "T" };
  assert.equal(
    phase([r("TT", "a"), r("TT", "b")], a, b, defaults).status,
    "Cis",
  );
});
