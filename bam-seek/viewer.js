import igv from "igv/dist/igv.esm.js";
let browser, payload;
const status = document.getElementById("viewer-status"),
  container = document.getElementById("igv");
const token = window.name;
const origin = location.origin === "null" ? "*" : location.origin;
function report(type, extra = {}) {
  window.dispatchEvent(
    new CustomEvent("bamseek-viewer", { detail: { type, ...extra } }),
  );
  if (payload?.testPort) payload.testPort.postMessage({ type, ...extra });
}
function retained() {
  const tracks = browser?.findTracks("type", "alignment") || [];
  return tracks.map((t) => {
    const containers = (t.trackView?.viewports || [])
      .map((v) => v.cachedFeatures)
      .filter(Boolean);
    return {
      colorBy: t.colorBy,
      viewAsPairs: t.viewAsPairs,
      sort: t.sortObject || t.config.sort,
      containers: containers.map((c) => ({
        samplingDepth: c.samplingDepth,
        downsampled: c.downsampledIntervals?.length || 0,
        alignments: c
          .allAlignments?.()
          .reduce(
            (n, a) =>
              n + (a.firstAlignment ? 1 + (a.secondAlignment ? 1 : 0) : 1),
            0,
          ),
        rows: [...(c.packedGroups?.values() || [])].reduce(
          (n, g) => n + g.rows.filter((r) => r.alignments.length).length,
          0,
        ),
      })),
    };
  });
}
async function init(p) {
  payload = p;
  document.title = "BAM Seek · " + p.name;
  document.getElementById("viewer-title").textContent =
    p.name +
    " · " +
    p.build +
    " · " +
    p.chr +
    ":" +
    (p.v.pos + 1) +
    " " +
    p.v.ref +
    ">" +
    p.v.alt;
  document.getElementById("filter-note").textContent =
    `Paired by read name · first-of-pair strand colors · sort at ${p.v.pos + 1} · no downsampling · mapQ ≥ ${p.settings.mapq} · duplicates ${p.settings.duplicates ? "included" : "excluded"}, secondary ${p.settings.secondary ? "included" : "excluded"}, supplementary ${p.settings.supplementary ? "included" : "excluded"}. IGV coverage is not the informative VAF denominator.`;
  try {
    status.textContent = "Reading local reference and alignments…";
    const reference = p.reference.twoBit
      ? { id: p.build, name: p.build, twoBitURL: p.reference.twoBit }
      : {
          id: p.build,
          name: p.build,
          fastaURL: p.reference.fasta,
          indexURL: p.reference.fai,
        };
    browser = await igv.createBrowser(container, {
      reference,
      loadDefaultGenomes: false,
      search: false,
      locus: `${p.chr}:${Math.max(1, p.v.pos - 49)}-${Math.min(p.length, p.v.pos + Math.max(51, p.v.ref.length + 26))}`,
      showCenterGuide: true,
      showRuler: true,
      showIdeogram: false,
      tracks: [
        {
          type: "alignment",
          format: "bam",
          name: p.name,
          url: p.bam,
          indexURL: p.index,
          colorBy: "firstOfPairStrand",
          viewAsPairs: true,
          showCoverage: true,
          showAlignments: true,
          showSoftClips: true,
          showMismatches: true,
          downsample: false,
          displayMode: "EXPANDED",
          height: 550,
          visibilityWindow: 1000,
          sort: {
            chr: p.chr,
            position: p.v.pos + 1,
            option: "BASE",
            direction: "ASC",
          },
          filter: {
            duplicates: !p.settings.duplicates,
            vendorFailed: true,
            secondary: !p.settings.secondary,
            supplementary: !p.settings.supplementary,
            mq: p.settings.mapq,
          },
        },
      ],
    });
    const refChr = browser.genome.getChromosome(p.chr);
    if (!refChr || refChr.bpLength !== p.length) {
      igv.removeBrowser(browser);
      throw Error(
        "BAM/reference contig lengths differ. Select the matching reference.",
      );
    }
    const referenceBases = await browser.genome.getSequence(
      p.chr,
      p.v.pos,
      p.v.pos + p.v.ref.length,
    );
    if (referenceBases?.toUpperCase() !== p.v.ref) {
      igv.removeBrowser(browser);
      throw Error("Variant REF does not match the selected reference.");
    }
    document.getElementById("resort").disabled = false;
    document.getElementById("resort").onclick = () => {
      for (const t of browser.findTracks("type", "alignment"))
        t.sort({
          chr: p.chr,
          position: p.v.pos + 1,
          option: "BASE",
          direction: "ASC",
        });
    };
    document.getElementById("recenter").onclick = () =>
      browser.search(
        `${p.chr}:${Math.max(1, p.v.pos - 49)}-${Math.min(p.length, p.v.pos + 51)}`,
      );
    status.textContent =
      "Ready · no downsampling · zoom in before viewing intervals wider than 1 kb";
    report("ready", { diagnostics: retained() });
    if (p.testPort)
      p.testPort.onmessage = async ({ data: d }) => {
        if (d.type === "inspect")
          p.testPort.postMessage({
            type: "inspection",
            diagnostics: retained(),
          });
        if (d.type === "navigate") {
          await browser.search(d.locus);
          p.testPort.postMessage({
            type: "navigated",
            diagnostics: retained(),
          });
        }
      };
  } catch (e) {
    status.textContent = "Unable to open IGV: " + e.message;
    report("error", { text: e.message });
  }
}
const expected = window.opener || window.parent;
window.addEventListener("message", function receive(e) {
  if (
    e.source !== expected ||
    e.data?.type !== "bamseek-init" ||
    e.data.token !== token ||
    !e.ports[0]
  )
    return;
  window.removeEventListener("message", receive);
  const port = e.ports[0];
  port.onmessage = ({ data, ports }) => {
    if (data.type === "payload") {
      init({ ...data.payload, testPort: ports[0] });
      port.close();
      try {
        window.opener = null;
      } catch {}
    }
  };
  port.start();
  port.postMessage({ type: "connected" });
});
expected?.postMessage({ type: "bamseek-viewer-ready", token }, origin);
setTimeout(() => {
  if (!payload)
    status.textContent =
      "This temporary viewer cannot restore file selections after reload. Reopen it from a BAM Seek result.";
}, 10000);

window.addEventListener("message", async (e) => {
  if (
    e.source === expected &&
    e.data?.type === "bamseek-recenter" &&
    browser &&
    payload
  ) {
    await browser.search(
      `${payload.chr}:${Math.max(1, payload.v.pos - 49)}-${Math.min(payload.length, payload.v.pos + 51)}`,
    );
    document.getElementById("resort").click();
  }
});
