import {
  parseDetailed,
  classifyVariants,
  defaults,
  key,
  identifier,
  validateSettings,
} from "./core.js";
import { comparison, phasingNarrative } from "./comparison.js";
import { links } from "./resources.js";
import { panel } from "./panel.js";
import { launchViewer } from "./launch-viewer.js";
import workerCode from "./worker-bundle.js";
const $ = (id) => document.getElementById(id),
  sources = [],
  pending = [];
let serial = 0,
  run = 0,
  busy = false,
  rows = [],
  phases = [],
  localPhases = [],
  settings = { ...defaults },
  lastBuild = "hg19",
  pendingBuild = "hg19",
  pendingSettings = { ...defaults };
const workerURL = URL.createObjectURL(
    new Blob([workerCode], { type: "text/javascript" }),
  ),
  worker = new Worker(workerURL);
worker.addEventListener("error", (e) => {
  status("Worker error: " + e.message);
  setBusy(false);
});
const pct = (a, b) => (b ? ((100 * a) / b).toFixed(2) + "%" : "—");
function node(tag, text, parent, cls) {
  const n = document.createElement(tag);
  n.textContent = text;
  if (cls) n.className = cls;
  parent?.append(n);
  return n;
}
function button(text, fn, parent) {
  const b = node("button", text, parent);
  b.type = "button";
  b.onclick = () => {
    try {
      const p = fn();
      if (p?.catch) p.catch((e) => status(e.message));
    } catch (e) {
      status(e.message);
    }
  };
  return b;
}
function status(text) {
  $("status").textContent = text;
}
function setBusy(b) {
  busy = b;
  for (const id of ["run", "files", "clear", "build"]) $(id).disabled = b;
  $("cancel").disabled = !b;
  document
    .querySelectorAll("[data-source-action]")
    .forEach((n) => (n.disabled = b));
}
async function copy(text) {
  try {
    await navigator.clipboard.writeText(text);
    status("Copied to clipboard.");
  } catch {
    $("copy-fallback").value = text;
    $("copy-dialog").showModal();
    $("copy-fallback").focus();
    $("copy-fallback").select();
  }
}
worker.onmessage = ({ data: d }) => {
  if (d.type === "prepared") {
    const s = sources.find((s) => s.id === d.id);
    if (!s) return;
    s.ready = true;
    s.refs = d.refs;
    renderSources();
    status(s.name + " prepared; calculation starts only when requested.");
  }
  if (d.type === "error") {
    if (d.id) {
      const s = sources.find((s) => s.id === d.id);
      if (s) {
        s.error = d.text;
        renderSources();
      }
    }
    if (d.run && d.run !== run) return;
    status(
      d.cancelled
        ? "Calculation cancelled. Previous completed results retained."
        : d.text,
    );
    if (d.run) setBusy(false);
  }
  if (d.type === "progress" && d.run === run)
    status(
      `${d.done} / ${d.total} VAF results · ${d.reused} reused · ${d.calculated} calculated; phasing follows.`,
    );
  if (d.type === "results" && d.run === run) {
    rows = d.rows;
    phases = d.phases;
    localPhases = d.localPhases;
    lastBuild = pendingBuild;
    settings = pendingSettings;
    render();
    setBusy(false);
    status(
      `${rows.length} VAF results · ${phases.length} direct phase pairs · ${localPhases.length} experimental pairs · ${d.reused} reused · ${d.calculated} calculated · ${rows.filter((r) => r.error).length} VAF issues.`,
    );
  }
};
function remove(s) {
  worker.postMessage({ type: "remove", id: s.id });
  sources.splice(sources.indexOf(s), 1);
  rows = rows.filter((r) => r.id !== s.id);
  phases = phases.filter((r) => r.id !== s.id);
  localPhases = localPhases.filter((r) => r.id !== s.id);
  renderSources();
  render();
}
function renderSources() {
  $("sources").replaceChildren();
  for (const s of sources) {
    const row = node("div", "", $("sources"), "source");
    const label = node("label", "", row);
    const r = node("input", "", label);
    r.type = "radio";
    r.name = "current-bam";
    r.checked = s.current;
    r.disabled = busy;
    r.dataset.sourceAction = "";
    r.onchange = () => {
      sources.forEach((x) => (x.current = x === s));
      renderSources();
      render();
    };
    node("strong", s.name, label);
    node(
      "span",
      s.error
        ? "Error: " + s.error
        : s.ready
          ? "Ready · " + s.index.name
          : "Preparing header and index…",
      row,
      "muted",
    );
    const b = button("Remove", () => remove(s), row);
    b.disabled = busy;
    b.dataset.sourceAction = "";
  }
  const b = button(
    "All BAMs historical",
    () => {
      sources.forEach((s) => (s.current = false));
      renderSources();
      render();
    },
    $("sources"),
  );
  b.disabled = busy;
  b.dataset.sourceAction = "";
}
function prepare(bam, index) {
  const s = {
    id: String(++serial),
    name: bam.name,
    bam,
    index,
    current: false,
    ready: false,
  };
  sources.push(s);
  worker.postMessage({ type: "prepare", id: s.id, bam, index });
  renderSources();
}
function renderPending() {
  $("pairing").replaceChildren();
  for (const p of pending) {
    const row = node("div", "", $("pairing"), "source");
    node("label", "Index for " + p.bam.name, row);
    const select = node("select", "", row);
    node("option", "Choose an index…", select).value = "";
    p.indexes.forEach(
      (f, i) => (node("option", f.name, select).value = String(i)),
    );
    button(
      "Pair files",
      () => {
        if (select.value === "") throw Error("Select the matching index.");
        prepare(p.bam, p.indexes[+select.value]);
        pending.splice(pending.indexOf(p), 1);
        renderPending();
      },
      row,
    );
    button(
      "Dismiss",
      () => {
        pending.splice(pending.indexOf(p), 1);
        renderPending();
      },
      row,
    );
  }
}
$("files").onchange = () => {
  const files = [...$("files").files],
    indexes = files.filter((f) => /\.(bai|csi)$/i.test(f.name)),
    bams = files.filter((f) => /\.bam$/i.test(f.name));
  if (!bams.length)
    status("Select BAM files together with their matching indexes.");
  for (const bam of bams) {
    const names = [
        bam.name + ".bai",
        bam.name + ".csi",
        bam.name.replace(/\.bam$/i, ".bai"),
        bam.name.replace(/\.bam$/i, ".csi"),
      ].map((x) => x.toLowerCase()),
      candidates = indexes.filter((f) => names.includes(f.name.toLowerCase()));
    if (candidates.length === 1) prepare(bam, candidates[0]);
    else if (indexes.length) {
      pending.push({ bam, indexes });
      status("Choose the matching indexes below.");
    } else
      status(
        "Missing BAI/CSI for " + bam.name + "; select both files together.",
      );
  }
  renderPending();
  $("files").value = "";
};
$("clear").onclick = () => {
  worker.postMessage({ type: "clear" });
  sources.length = 0;
  pending.length = 0;
  rows = [];
  phases = [];
  localPhases = [];
  renderSources();
  renderPending();
  render();
  status("Sources, results and evidence cache cleared.");
};
function readSettings() {
  const s = {
    ...defaults,
    mapq: +$("mapq").value,
    baseq: +$("baseq").value,
    support: +$("support").value,
    conflict: +$("conflict").value / 100,
    mode: $("mode").value,
    tag: $("tag").value,
    minVaf: +$("min-vaf").value / 100,
    minReads: +$("min-reads").value,
    minMolecules: +$("min-molecules").value,
    duplicates: $("duplicates").checked,
    secondary: $("secondary").checked,
    supplementary: $("supplementary").checked,
  };
  validateSettings(s);
  return s;
}
$("build").onchange = () => {
  $("panel-note").textContent =
    $("build").value === "hg19"
      ? "The fixed hg19 disease panel is always included."
      : "The hg19 disease panel and hg19 provider links are disabled for hg38.";
  if (rows.length)
    status(
      "Genome selection changed. Recalculate before reviewing results for this build.",
    );
};
$("run").onclick = () => {
  try {
    if (!sources.length || sources.some((s) => !s.ready))
      throw Error("Add valid BAMs and wait for preparation to finish.");
    if (pending.length) throw Error("Pair or dismiss the pending BAMs first.");
    if (!$("assembly-confirm").checked)
      throw Error("Confirm the selected assembly matches the BAMs.");
    const a = parseDetailed($("current").value),
      b = parseDetailed($("historical").value);
    if (a.errors.length || b.errors.length)
      throw Error(
        [
          ...a.errors.map((e) => "Current " + e),
          ...b.errors.map((e) => "Historical " + e),
        ].join("\n"),
      );
    const variants = classifyVariants(a.variants, b.variants);
    pendingBuild = $("build").value;
    pendingSettings = readSettings();
    if (pendingBuild === "hg19") {
      const genomic = new Set(variants.map(key));
      for (const g of panel)
        for (const v of g.variants)
          if (!genomic.has(key(v))) {
            genomic.add(key(v));
            variants.push({ ...v, role: "Disease panel" });
          }
    }
    if (!variants.length)
      throw Error("Enter at least one variant for this assembly.");
    run++;
    setBusy(true);
    status("Calculating evidence…");
    worker.postMessage({
      type: "calculate",
      run,
      ids: sources.map((s) => s.id),
      variants,
      settings: pendingSettings,
      local: $("local-phase").checked,
    });
  } catch (e) {
    status(e.message);
  }
};
$("cancel").onclick = () => {
  worker.postMessage({ type: "cancel" });
  status("Cancelling…");
};
function reference() {
  const fs = [...$("reference").files],
    twoBit = fs.find((f) => /\.2bit$/i.test(f.name));
  return twoBit
    ? { twoBit }
    : {
        fasta: fs.find((f) => /\.(fa|fasta|fna)$/i.test(f.name)),
        fai: fs.find((f) => /\.fai$/i.test(f.name)),
      };
}
function review(s, v) {
  if ($("build").value !== lastBuild)
    throw Error("Recalculate after changing genome build.");
  launchViewer(s, v, settings, reference(), lastBuild, $("viewer"));
}
function resourceDialog(v) {
  $("resource-title").textContent = identifier(v);
  const body = $("resource-list");
  body.replaceChildren();
  for (const l of links(v, lastBuild)) {
    const tr = node("tr", "", body);
    node("td", l.name, tr);
    node("td", l.id, tr);
    node("td", l.note, tr);
    const cell = node("td", "", tr);
    if (l.enabled) {
      const a = node("a", "Open", cell);
      a.href = l.url;
      a.target = "_blank";
      a.rel = "noopener noreferrer";
    } else node("span", "Unavailable", cell);
  }
  $("resources-dialog").showModal();
}
function actions(cell, s, v) {
  button("Open IGV", () => review(s, v), cell);
  button("Copy identifier", () => copy(identifier(v)), cell);
  button("External resources", () => resourceDialog(v), cell);
}
function table(parent, headers) {
  const t = node("table", "", parent),
    head = node("tr", "", node("thead", "", t));
  headers.forEach((x) => node("th", x, head));
  return node("tbody", "", t);
}
function variantName(v) {
  return (
    [v.gene, v.coding, v.protein].filter(Boolean).join(" ") || identifier(v)
  );
}
function drawRows(parent, rs, s) {
  const body = table(parent, [
    "Variant",
    "Origin",
    "ALT / informative reads",
    "Read VAF",
    "ALT / informative molecules",
    "Molecule VAF",
    "Detection / review",
  ]);
  for (const r of rs) {
    const tr = node("tr", "", body),
      label = node("td", variantName(r.v), tr);
    node("small", identifier(r.v), label);
    node("td", r.v.role, tr);
    if (r.error) {
      const cell = node("td", r.error, tr, "error");
      cell.colSpan = 5;
      continue;
    }
    const c = r.counts;
    node("td", `${c.A} / ${c.A + c.R}`, tr);
    node("td", pct(c.A, c.A + c.R), tr);
    node("td", `${c.mA} / ${c.mA + c.mR}`, tr);
    node("td", pct(c.mA, c.mA + c.mR), tr);
    const cell = node(
      "td",
      !c.A && !c.R
        ? "No informative coverage"
        : c.detected
          ? "Detected"
          : "Below threshold",
      tr,
    );
    actions(cell, s, r.v);
    const detail = node("details", "", label);
    node("summary", "Evidence details", detail);
    node(
      "p",
      `OTHER reads ${c.O}; ambiguous/OTHER molecules ${c.mO}; filtered ${c.filtered}; uncallable ${c.N}; low baseQ ${c.Q}; total queried alignments ${c.overlapping}; molecule grouping ${c.tag}; missing tags ${c.missing}; REF forward/reverse ${c.RF}/${c.RR}; ALT forward/reverse ${c.AF}/${c.AR}.`,
      detail,
    );
  }
}
function render() {
  const sorted = [...sources].sort(
    (a, b) =>
      Number(b.current) - Number(a.current) || a.name.localeCompare(b.name),
  );
  $("results").replaceChildren();
  $("disease-results").replaceChildren();
  for (const s of sorted) {
    const rs = rows
      .filter((r) => r.id === s.id && r.v.role !== "Disease panel")
      .sort((a, b) => variantName(a.v).localeCompare(variantName(b.v)));
    if (rs.length) {
      node(
        "h3",
        s.name + (s.current ? " · Current" : " · Historical"),
        $("results"),
      );
      drawRows($("results"), rs, s);
    }
    if (lastBuild === "hg19" && rows.length) {
      node(
        "h3",
        s.name + (s.current ? " · Current" : " · Historical"),
        $("disease-results"),
      );
      for (const g of panel) {
        const section = node("details", "", $("disease-results"));
        node("summary", g.name, section);
        if (g.note) node("p", g.note, section);
        const rs = g.variants
          .map((v) => rows.find((r) => r.id === s.id && key(r.v) === key(v)))
          .filter(Boolean);
        drawRows(section, rs, s);
      }
    }
  }
  $("phase-results").replaceChildren();
  const stats = {
    Cis: 0,
    Trans: 0,
    Indeterminate: 0,
    "Too far apart to phase": 0,
  };
  phases.forEach((p) => {
    if (p.status) stats[p.status]++;
  });
  if (phases.length)
    node(
      "p",
      Object.entries(stats)
        .map(([k, n]) => `${n} ${k.toLowerCase()}`)
        .join(" · "),
      $("phase-results"),
    );
  for (const p of [...phases].sort(
    (a, b) =>
      (a.status === "Cis" || a.status === "Trans" ? 0 : 1) -
      (b.status === "Cis" || b.status === "Trans" ? 0 : 1),
  )) {
    const s = sources.find((s) => s.id === p.id);
    const row = node("div", "", $("phase-results"), "finding");
    node(
      "strong",
      `${s.name} · ${p.a.gene} · ${variantName(p.a)} / ${variantName(p.b)} · ${p.error ? "Error" : p.status}`,
      row,
    );
    node(
      "p",
      p.error ||
        `${p.distance} bp · AB ${p.AB} · Ab ${p.Ab} · aB ${p.aB} · ab ${p.ab} · noninformative ${p.noninformative}. ${p.reason}`,
      row,
    );
    if (!p.error) {
      button("Open first variant in IGV", () => review(s, p.a), row);
      button("Open second variant in IGV", () => review(s, p.b), row);
    }
  }
  $("local-results").replaceChildren();
  for (const p of localPhases) {
    const row = node("div", "", $("local-results"), "finding");
    node(
      "strong",
      `${sources.find((s) => s.id === p.id).name} · ${variantName(p.a)} / ${variantName(p.b)} · ${p.status || "Error"}`,
      row,
    );
    node(
      "p",
      p.error ||
        `${p.rare} rare markers · ${p.common} common markers · ${p.chains} supported chains. ${p.reason} ${p.chain}`,
      row,
    );
  }
  $("narrative").value = [
    comparison(rows, sources),
    phasingNarrative(phases, sources),
  ]
    .filter(Boolean)
    .join("\n\n");
  $("evidence-text").value = rows
    .filter((r) => !r.error)
    .map((r) => {
      const c = r.counts,
        s = sources.find((s) => s.id === r.id);
      return `${s.name} (${s.current ? "Current" : "Historical"}) · ${identifier(r.v)} · ALT reads ${c.A}/${c.A + c.R} (${pct(c.A, c.A + c.R)}) · ALT molecules ${c.mA}/${c.mA + c.mR} (${pct(c.mA, c.mA + c.mR)})`;
    })
    .join("\n");
}
$("theme").onclick = () => document.documentElement.classList.toggle("dark");
$("copy").onclick = () => copy($("narrative").value);
$("copy-evidence").onclick = () => copy($("evidence-text").value);
document
  .querySelectorAll("[data-close]")
  .forEach((b) => (b.onclick = () => b.closest("dialog").close()));
$("about-button").onclick = () => $("about-dialog").showModal();
