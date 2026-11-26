import { launchViewer } from "../launch-viewer.js";
let input, port;
window.addEventListener("message", (e) => {
  if (e.source !== parent || e.data?.type !== "test-init") return;
  input = e.data.payload;
  port = e.ports[0];
  document.getElementById("launch").disabled = false;
  document.getElementById("status").textContent =
    "Ready to open independent viewer.";
});
document.getElementById("launch").onclick = () => {
  launchViewer(
    input.source,
    input.v,
    input.settings,
    input.reference,
    "hg19",
    document.getElementById("fallback"),
    { testPort: port },
  );
};
parent.postMessage({ type: "lifecycle-ready" }, location.origin);
