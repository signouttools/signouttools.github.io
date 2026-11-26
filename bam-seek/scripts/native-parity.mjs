import { execFileSync } from "node:child_process";
import { resolve, dirname } from "node:path";
import { readFile, copyFile, access, mkdir } from "node:fs/promises";
import { fileURLToPath } from "node:url";
import assert from "node:assert/strict";
import { Engine } from "../engine.js";
import { defaults, parse } from "../core.js";
import { fixtures, fixtureDir } from "./fixtures.mjs";
const root = resolve(dirname(fileURLToPath(import.meta.url)), ".."),
  native = resolve(
    process.env.BAM_SEEK_NATIVE_SOURCE || resolve(root, "../../bam-seek"),
  ),
  igv = process.env.IGVCPP_SOURCE_DIR;
if (!igv) throw Error("Set IGVCPP_SOURCE_DIR to the native igv-cpp checkout");
const build = resolve(
  process.env.BAM_SEEK_NATIVE_BUILD || "/private/tmp/bam-seek-web-native",
);
const run = (cmd, args, opts = {}) =>
  execFileSync(cmd, args, { stdio: "pipe", ...opts });
try {
  await access(resolve(native, "tests/data/clinical_mappings.tsv"));
} catch {
  await mkdir(resolve(native, "tests/data"), { recursive: true });
  await copyFile(
    resolve(fixtureDir, "clinical_mappings.tsv"),
    resolve(native, "tests/data/clinical_mappings.tsv"),
  );
}
run("cmake", [
  "-S",
  native,
  "-B",
  build,
  "-DBAM_SEEK_BUILD_GUI=OFF",
  "-DIGVCPP_SOURCE_DIR=" + igv,
]);
run("cmake", ["--build", build, "-j", "4"]);
run("sh", [resolve(native, "tests/generate_jak2_bams.sh")]);
console.log(
  run("ctest", ["--test-dir", build, "--output-on-failure"]).toString(),
);
const flags = run("pkg-config", ["--cflags", "--libs", "htslib"])
  .toString()
  .trim()
  .split(/\s+/);
const oracle = resolve(build, "web-parity-oracle");
run("c++", [
  "-std=c++20",
  "-I" + resolve(native, "include"),
  "-I" + resolve(igv, "include"),
  resolve(root, "tests/native-oracle.cpp"),
  resolve(build, "libbam_seek_core.a"),
  resolve(build, "igv-cpp/libigv_cpp.a"),
  ...flags,
  "-lz",
  "-o",
  oracle,
]);
await fixtures();
const file = async (n) => new File([await readFile(resolve(fixtureDir, n))], n),
  engine = new Engine();
await engine.prepare(
  "1",
  await file("evidence.bam"),
  await file("evidence.bam.bai"),
);
const cases = [
  "chr1:15 A>T",
  "chr1:35 A>AT",
  "chr1:55 AAA>A",
  "chr1:75 A>T",
  "chr1:85 A>AT",
  "chr1:2 A>C\nchr1:7 A>G",
  "chr1:46 A>C\nchr1:51 A>G",
  "chr1:62 A>C\nchr1:67 A>G",
  "chr1:5 A>T\nchr1:7 A>G",
  "chr1:102 A>C\nchr1:126 A>C",
  "chr1:142 A>C\nchr1:166 A>C",
  "chr1:69 A>T\nchr1:96 A>C",
];
let checks = 0;
for (const mode of ["name", "tag"])
  for (const input of cases) {
    const expected = run(
      oracle,
      [resolve(fixtureDir, "evidence.bam"), ...(mode === "tag" ? ["MI"] : [])],
      { input },
    )
      .toString()
      .trim()
      .split("\n")
      .map((x) => x.split("\t"));
    const vs = parse(input).map((v) => ({
        ...v,
        gene: "TEST",
        role: "Current",
      })),
      s = { ...defaults, mode, tag: "MI" },
      r = await engine.run(["1"], vs, s);
    r.rows.forEach((row, i) => {
      assert.ifError(row.error);
      const c = row.counts;
      assert.deepEqual(
        [c.R, c.A, c.O, c.mR, c.mA, c.mO, c.filtered, c.N, c.Q, c.missing],
        expected[i].slice(1).map(Number),
        input + " " + mode,
      );
      checks++;
    });
    if (vs.length === 2) {
      const p = r.phases[0],
        native = expected[2];
      assert.deepEqual(
        [p.status.toLowerCase(), p.AB, p.Ab, p.aB, p.ab],
        [native[1], ...native.slice(2).map(Number)],
        input + " direct " + mode,
      );
      const l = r.localPhases[0],
        nl = expected[3];
      assert.deepEqual(
        [l.status.toLowerCase(), l.rare, l.common, l.chains],
        [nl[1], ...nl.slice(2).map(Number)],
        input + " local " + mode,
      );
      checks += 2;
    }
  }
console.log(`PASS ${checks} native/browser evidence and phase comparisons`);
