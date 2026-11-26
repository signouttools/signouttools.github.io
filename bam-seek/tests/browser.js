import { Engine } from "../engine.js";
import { defaults, parse } from "../core.js";
import { launchViewer } from "../launch-viewer.js";
const out = document.getElementById("report"),
  files = {};
function log(s) {
  out.textContent += s + "\n";
}
const eq = (a, b, message) => {
  if (a !== b) throw Error(message + `: got ${a}, expected ${b}`);
};
async function wait(fn, label) {
  const end = Date.now() + 30000;
  while (Date.now() < end) {
    const v = fn();
    if (v) return v;
    await new Promise((r) => setTimeout(r, 50));
  }
  throw Error("Timed out: " + label);
}
window.addEventListener("error", (e) => log("ERROR " + e.message));
window.addEventListener("unhandledrejection", (e) => log("ERROR " + e.reason));
async function start() {
  for (const name of [
    "evidence.bam",
    "evidence.bam.bai",
    "evidence.bam.csi",
    "deep.bam",
    "deep.bam.bai",
    "deep.bam.csi",
    "deep.fa",
    "deep.fa.fai",
    "deep.2bit",
  ]) {
    const r = await fetch("./fixtures/" + name);
    if (!r.ok) throw Error(name + " unavailable");
    files[name] = new File([await r.arrayBuffer()], name);
  }
  document.querySelectorAll("button").forEach((b) => (b.disabled = false));
  log("Fixtures loaded. Ready.");
}
start().catch((e) => log("FAIL " + e.message));
function inputFiles(doc, id, fs) {
  const dt = new doc.defaultView.DataTransfer();
  fs.forEach((f) => dt.items.add(f));
  const el = doc.getElementById(id);
  el.files = dt.files;
  el.dispatchEvent(new Event("change", { bubbles: true }));
}
document.getElementById("run-tests").onclick = async () => {
  try {
    log("Starting packaged application checks…");
    const frame = document.getElementById("app");
    await wait(
      () => frame.contentDocument?.getElementById("files"),
      "app loaded",
    );
    const d = frame.contentDocument;
    const violations = [];
    d.addEventListener("securitypolicyviolation", (e) =>
      violations.push(e.violatedDirective),
    );
    inputFiles(d, "files", [files["deep.bam"], files["deep.bam.bai"]]);
    await wait(
      () => d.getElementById("sources").textContent.includes("Ready"),
      "source ready",
    );
    d.getElementById("build").value = "hg38";
    d.getElementById("build").dispatchEvent(new Event("change"));
    d.getElementById("assembly-confirm").checked = true;
    d.getElementById("current").value = "TEST c.150A>T p.K50N chr1:150 A>T";
    d.getElementById("historical").value = "TEST c.150A>T p.K50N chr1:150 A>T";
    d.getElementById("run").click();
    await wait(
      () => d.getElementById("status").textContent.includes("results ·"),
      "results",
    );
    const text = d.getElementById("results").textContent;
    if (
      !text.includes("6026 / 24100") ||
      !text.includes("3013 / 12050") ||
      !text.includes("Both")
    )
      throw Error("Incorrect packaged result: " + text);
    eq(d.getElementById("narrative").value, "", "Both excluded from narrative");
    log(
      "PASS packaged worker/CSP/BAI results: 24,100 reads, 12,050 molecules; Both excluded from narrative.",
    );
    d.querySelector('input[name="current-bam"]').click();
    if (!d.getElementById("results").textContent.includes("Current"))
      throw Error("Current relabel failed");
    log("PASS Current sample relabel without recalculation.");
    d.getElementById("run").click();
    await wait(
      () => d.getElementById("status").textContent.includes("1 reused"),
      "cache reuse",
    );
    log("PASS evidence cache reuse.");
    inputFiles(d, "reference", [files["deep.fa"], files["deep.fa.fai"]]);
    const oldOpen = frame.contentWindow.open;
    frame.contentWindow.open = () => null;
    try {
      d.querySelector("#results button").click();
    } finally {
      frame.contentWindow.open = oldOpen;
    }
    await wait(
      () =>
        d
          .querySelector("#viewer iframe")
          ?.contentDocument?.getElementById("viewer-status")
          ?.textContent.includes("Ready ·"),
      "packaged IGV fallback ready",
    );
    log("PASS IGV launched from actual packaged result under inherited CSP.");
    d.querySelector("#sources button").click();
    eq(d.getElementById("results").textContent, "", "remove result");
    log("PASS source removal clears results/cache.");
    inputFiles(d, "files", [
      files["deep.bam"],
      files["deep.bam.bai"],
      files["deep.bam.csi"],
    ]);
    await wait(
      () => d.getElementById("pairing").textContent.includes("Index for"),
      "ambiguous pairing",
    );
    d.querySelector("#pairing select").value = "1";
    d.querySelector("#pairing button").click();
    await wait(
      () => d.getElementById("sources").textContent.includes("Ready"),
      "CSI prepare",
    );
    d.getElementById("run").click();
    await wait(
      () => d.getElementById("status").textContent.includes("results ·"),
      "CSI results",
    );
    if (!d.getElementById("results").textContent.includes("6026 / 24100"))
      throw Error("CSI incorrect");
    log("PASS explicit ambiguous-index pairing and CSI calculation.");
    d.getElementById("build").value = "hg19";
    d.getElementById("build").dispatchEvent(new Event("change"));
    d.getElementById("run").click();
    await wait(
      () => d.getElementById("status").textContent.includes("VAF issues"),
      "panel run",
    );
    if (!d.getElementById("disease-results").textContent.includes("CLL or MCL"))
      throw Error("Panel groups absent");
    log(
      "PASS disease-panel groups and per-site errors (synthetic reference lacks real hg19 hotspots).",
    );
    eq(violations.length, 0, "CSP violations");
    log("PASS no CSP violations.");
    log("PACKAGED APPLICATION CHECKS PASSED");
  } catch (e) {
    log("FAIL " + e.message);
  }
};
function source(index) {
  return {
    id: index,
    name: "deep " + index,
    bam: files["deep.bam"],
    index: files[index],
    refs: [{ refName: "chr1", length: 1000 }],
  };
}
const reference = () => ({
  fasta: files["deep.fa"],
  fai: files["deep.fa.fai"],
});
function inspect(port, label) {
  port.onmessage = ({ data: d }) => {
    if (d.type === "error") {
      log("FAIL " + label + " " + d.text);
      return;
    }
    if (d.type !== "ready" && d.type !== "inspection" && d.type !== "navigated")
      return;
    try {
      const t = d.diagnostics[0],
        c = t?.containers[0];
      if (!c) throw Error("No alignment container: " + JSON.stringify(d));
      eq(t.colorBy, "firstOfPairStrand", "strand coloring");
      eq(t.viewAsPairs, true, "paired display");
      eq(t.sort.option, "BASE", "base sorting");
      eq(t.sort.position, 149, "sort coordinate");
      eq(c.samplingDepth, Infinity, "sampling disabled");
      eq(c.downsampled, 0, "no sampled intervals");
      eq(c.alignments, 24100, "retained reads");
      eq(c.rows, 12050, "all pairs packed");
      log(
        "PASS " +
          label +
          " " +
          d.type +
          ": 24,100 retained reads, 12,050 packed pair rows; sampling disabled; strand/pairs/base sort correct.",
      );
    } catch (e) {
      log("FAIL " + label + " " + e.message);
    }
  };
  port.start();
}
for (const [button, index] of [
  ["open-bai", "deep.bam.bai"],
  ["open-csi", "deep.bam.csi"],
])
  document.getElementById(button).onclick = () => {
    const channel = new MessageChannel();
    inspect(channel.port1, index);
    launchViewer(
      source(index),
      parse("1:150 A>T")[0],
      defaults,
      reference(),
      "hg19",
      document.getElementById("fallback"),
      { testPort: channel.port2 },
    );
  };
document.getElementById("fallback-test").onclick = () => {
  const old = window.open;
  window.open = () => null;
  try {
    const channel = new MessageChannel();
    inspect(channel.port1, "popup fallback");
    launchViewer(
      { ...source("deep.bam.bai"), id: "fallback" },
      parse("1:150 A>T")[0],
      defaults,
      reference(),
      "hg19",
      document.getElementById("fallback"),
      { testPort: channel.port2 },
    );
  } finally {
    window.open = old;
  }
};
window.addEventListener("message", (e) => {
  const frame = document.getElementById("lifecycle");
  if (e.source !== frame?.contentWindow || e.data?.type !== "lifecycle-ready")
    return;
  const channel = new MessageChannel();
  let removed = false;
  channel.port1.onmessage = ({ data: d }) => {
    if (d.type === "ready" && !removed) {
      removed = true;
      frame.remove();
      log("Opener iframe removed; requesting independent navigation…");
      channel.port1.postMessage({ type: "navigate", locus: "chr1:130-180" });
    } else if (d.type === "navigated") {
      const c = d.diagnostics[0]?.containers[0];
      try {
        eq(c?.alignments, 24100, "independent viewer retained reads");
        eq(c?.downsampled, 0, "independent sampling");
        log(
          "PASS independent IGV survives opener closure and navigates with all 24,100 reads.",
        );
      } catch (e) {
        log("FAIL " + e.message);
      }
    } else if (d.type === "error") log("FAIL independent viewer " + d.text);
  };
  channel.port1.start();
  frame.contentWindow.postMessage(
    {
      type: "test-init",
      payload: {
        source: { ...source("deep.bam.bai"), id: "lifecycle" },
        v: parse("1:150 A>T")[0],
        settings: defaults,
        reference: reference(),
      },
    },
    location.origin,
    [channel.port2],
  );
});
document.getElementById("lifecycle-test").onclick = () => {
  const frame = document.createElement("iframe");
  frame.id = "lifecycle";
  frame.title = "Independent viewer opener";
  frame.style.height = "130px";
  frame.src = "lifecycle.html";
  document.getElementById("lifecycle-host").replaceChildren(frame);
};

document.getElementById("open-twobit").onclick = () => {
  const channel = new MessageChannel();
  inspect(channel.port1, "2bit reference");
  launchViewer(
    { ...source("deep.bam.bai"), id: "twobit" },
    parse("1:150 A>T")[0],
    defaults,
    { twoBit: files["deep.2bit"] },
    "hg19",
    document.getElementById("fallback"),
    { testPort: channel.port2 },
  );
};
