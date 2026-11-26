import { Engine } from "./engine.js";
// No remote I/O, storage, analytics or application backend.
const engine = new Engine();
let active,
  epoch = 0;
const removed = new Set();
self.onmessage = async ({ data: d }) => {
  try {
    if (d.type === "cancel") {
      active?.abort();
      return;
    }
    if (d.type === "remove") {
      removed.add(d.id);
      engine.remove(d.id);
      return;
    }
    if (d.type === "clear") {
      active?.abort();
      epoch++;
      engine.clear();
      return;
    }
    if (d.type === "prepare") {
      const generation = epoch;
      const refs = await engine.prepare(d.id, d.bam, d.index);
      if (generation !== epoch || removed.has(d.id)) {
        engine.remove(d.id);
        return;
      }
      postMessage({ type: "prepared", id: d.id, refs });
      return;
    }
    if (d.type === "calculate") {
      active = new AbortController();
      const result = await engine.run(d.ids, d.variants, d.settings, {
        local: d.local,
        signal: active.signal,
        progress: (p) => postMessage({ type: "progress", run: d.run, ...p }),
      });
      postMessage({ type: "results", run: d.run, ...result });
    }
  } catch (e) {
    postMessage({
      type: "error",
      id: d.id,
      run: d.run,
      cancelled: e.name === "AbortError",
      text: e.message,
    });
  }
};
