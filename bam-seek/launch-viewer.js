import viewerHtml from "./viewer-bundle.js";
import { resolveContig, identifier, key } from "./core.js";
const sessions = new Map();
const opaqueOrigin =
  location.protocol === "file:" || location.origin === "null";
window.addEventListener("message", (e) => {
  if (e.data?.type !== "bamseek-viewer-ready") return;
  const session = sessions.get(e.data.token);
  if (!session || !session.payload || e.source !== session.window) return;
  if (!opaqueOrigin && e.origin !== location.origin) return;
  const channel = new MessageChannel();
  channel.port1.onmessage = ({ data }) => {
    if (data.type !== "connected") return;
    const ports = session.testPort ? [session.testPort] : [];
    channel.port1.postMessage(
      { type: "payload", payload: session.payload },
      ports,
    );
    channel.port1.close();
    session.payload = null;
    session.testPort = null;
  };
  session.window.postMessage(
    { type: "bamseek-init", token: e.data.token },
    e.origin === "null" ? "*" : e.origin,
    [channel.port2],
  );
});
export function launchViewer(
  source,
  v,
  settings,
  reference,
  build,
  fallback,
  { testPort } = {},
) {
  if (!reference?.twoBit && (!reference?.fasta || !reference?.fai))
    throw Error(
      "Select a local .2bit reference, or uncompressed FASTA and its FAI, before opening IGV.",
    );
  const ref = resolveContig(source.refs, v.chr);
  for (const [token, session] of sessions)
    if (session.window.closed) {
      URL.revokeObjectURL(session.url);
      sessions.delete(token);
    }
  const referenceKey = Object.values(reference)
    .map((f) => [f.name, f.size, f.lastModified].join(":"))
    .join("|");
  const identity =
    source.id +
    "|" +
    key(v) +
    "|" +
    build +
    "|" +
    JSON.stringify(settings) +
    "|" +
    referenceKey;
  for (const s of sessions.values())
    if (s.identity === identity && !s.window.closed && !s.fallback) {
      s.window.postMessage(
        { type: "bamseek-recenter" },
        opaqueOrigin ? "*" : location.origin,
      );
      s.window.focus();
      return s.window;
    }
  const token = "bamseek-" + crypto.randomUUID();
  const url = URL.createObjectURL(
    new Blob([viewerHtml], { type: "text/html" }),
  );
  let w = window.open("about:blank", token);
  let isFallback = false;
  if (!w) {
    isFallback = true;
    const frame = document.createElement("iframe");
    frame.name = token;
    frame.title = "IGV · " + identifier(v);
    frame.style.cssText = "width:100%;height:850px;border:1px solid #ccd8e4";
    fallback.replaceChildren(frame);
    w = frame.contentWindow;
    frame.srcdoc = viewerHtml;
    URL.revokeObjectURL(url);
    fallback.scrollIntoView({ behavior: "smooth" });
  } else w.location.replace(url);
  sessions.set(token, {
    identity,
    url,
    window: w,
    fallback: isFallback,
    testPort,
    payload: {
      name: source.name,
      bam: source.bam,
      index: source.index,
      chr: ref.refName,
      length: ref.length,
      v,
      settings,
      reference,
      build,
    },
  });
  return w;
}
