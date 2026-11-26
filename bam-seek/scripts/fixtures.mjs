import { readFile, writeFile, mkdir } from "node:fs/promises";
import { execFileSync } from "node:child_process";
import { fileURLToPath } from "node:url";
import { dirname, resolve } from "node:path";
export const fixtureDir = resolve(
  dirname(fileURLToPath(import.meta.url)),
  "../tests/fixtures",
);
export async function fixtures() {
  await mkdir(fixtureDir, { recursive: true });
  const samtools = process.env.SAMTOOLS || "samtools";
  const run = (args) => execFileSync(samtools, args, { stdio: "pipe" });
  run([
    "sort",
    "-o",
    resolve(fixtureDir, "evidence.bam"),
    resolve(fixtureDir, "evidence.sam"),
  ]);
  run(["index", resolve(fixtureDir, "evidence.bam")]);
  run([
    "index",
    "-c",
    resolve(fixtureDir, "evidence.bam"),
    resolve(fixtureDir, "evidence.bam.csi"),
  ]);
  await writeFile(
    resolve(fixtureDir, "evidence.fa"),
    await readFile(resolve(fixtureDir, "evidence_reference.txt")),
  );
  run(["faidx", resolve(fixtureDir, "evidence.fa")]);
  await writeFile(
    resolve(fixtureDir, "deep.fa"),
    ">chr1\n" + "A".repeat(1000) + "\n",
  );
  run(["faidx", resolve(fixtureDir, "deep.fa")]);
  const twoBit = new Uint8Array(291),
    view = new DataView(twoBit.buffer);
  view.setUint32(0, 0x1a412743);
  view.setUint32(8, 1);
  twoBit[16] = 4;
  twoBit.set(new TextEncoder().encode("chr1"), 17);
  view.setUint32(21, 25);
  view.setUint32(25, 1000);
  twoBit.fill(0xaa, 41);
  await writeFile(resolve(fixtureDir, "deep.2bit"), twoBit);
}

// spawn input is kept separate for large deterministic high-depth SAM.
export async function deepFixture() {
  const samtools = process.env.SAMTOOLS || "samtools",
    sam = ["@HD\tVN:1.6\tSO:coordinate", "@SQ\tSN:chr1\tLN:1000"];
  for (let i = 0; i < 12050; i++)
    for (const [flag, start, next] of [
      [99, 101, 121],
      [147, 121, 101],
    ]) {
      let seq = "A".repeat(101);
      if (i < 3013)
        seq = seq.slice(0, 150 - start) + "T" + seq.slice(151 - start);
      sam.push(
        [
          `pair_${String(i).padStart(6, "0")}`,
          flag,
          "chr1",
          start,
          60,
          "101M",
          "=",
          next,
          flag === 99 ? 121 : -121,
          seq,
          "I".repeat(101),
        ].join("\t"),
      );
    }
  execFileSync(samtools, ["sort", "-o", resolve(fixtureDir, "deep.bam"), "-"], {
    input: sam.join("\n") + "\n",
    maxBuffer: 16 * 1024 * 1024,
  });
  execFileSync(samtools, ["index", resolve(fixtureDir, "deep.bam")]);
  execFileSync(samtools, [
    "index",
    "-c",
    resolve(fixtureDir, "deep.bam"),
    resolve(fixtureDir, "deep.bam.csi"),
  ]);
}
if (process.argv[1] === fileURLToPath(import.meta.url)) {
  await fixtures();
  await deepFixture();
  console.log("Generated deterministic BAM/BAI/CSI and FASTA/FAI fixtures");
}
