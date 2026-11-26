import { readFile } from "node:fs/promises";
import assert from "node:assert/strict";
// Upstream 3.8.10 has no downsample:false switch in AlignmentContainer.
// Add a real bypass, rather than relying on a large finite sampling threshold.
export function igvPlugin({ internals = false } = {}) {
  return {
    name: "bam-seek-igv-no-sampling",
    setup(build) {
      build.onLoad({ filter: /igv\/dist\/igv\.esm\.js$/ }, async (args) => {
        let contents = await readFile(args.path, "utf8");
        const before = "this.samplingDepth = samplingDepth || 1000;";
        assert.equal(
          contents.split(before).length,
          2,
          "IGV sampling implementation changed; review patch",
        );
        contents = contents
          .replace(
            "                    samplingWindowSize,\n                    samplingDepth,",
            "                    downsample,\n                    samplingWindowSize,\n                    samplingDepth,",
          )
          .replace(
            before,
            "this.samplingDepth = downsample === false ? Infinity : (samplingDepth || 1000);",
          );
        assert.match(contents, /downsample,\n\s+samplingWindowSize/);
        if (internals)
          contents += "\nexport { AlignmentContainer, BamReader };\n";
        return {
          contents,
          loader: "js",
          resolveDir: new URL("./node_modules/igv/dist/", import.meta.url)
            .pathname,
        };
      });
    },
  };
}

export function inflaterPlugin() {
  return {
    name: "local-javascript-bgzf",
    setup(build) {
      build.onResolve({ filter: /^@gmod\/bgzf-filehandle$/ }, () => ({
        path: new URL("./bgzf.js", import.meta.url).pathname,
      }));
    },
  };
}
