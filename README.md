# Signout Tools

This repository serves the Signout Tools directory through GitHub Pages. The root
page links to CARA, SARA, FIQ, Phase, SAGE, and BAM Seek. Each **Open tool** link and its
**Download stand-alone HTML** counterpart use the same file in `tools/`. Open a downloaded
file directly in desktop Chrome or Edge.

## Local processing

The site is static. Tools process selected files in the browser, keep working data
in memory, and use no application-managed persistent storage. The tool documents
deny runtime connections with Content Security Policy and allow bundled scripts by
hash. Tools that support explicit exports still let the user save those exports.
SARA retains its user-initiated external variant lookup links.

## Refreshing the tools

With the source checkouts next to this repository, run:

```sh
node scripts/bundle-tools.mjs
```

You can also pass the path to the parent directory containing the source checkouts.
The script uses the current release HTML from SARA and the four documented Phase
workflows. Phase workflow links live in the directory so each download opens
independently. All nine releases include an offline About dialog. Edit the
copy in `scripts/about-content.mjs`, then rerun the bundler. The script embeds
the local JavaScript and CSS from CARA, FIQ, and SAGE and updates CSP hashes.
For SARA, FIQ, and Phase, rebuild in the source
checkout first if the published source artifacts are stale. Review and commit the
updated HTML files to publish them through GitHub Pages. Refresh the bundled
third-party notices in `scripts/third-party-notices/` when FIQ or Phase updates
its dependencies. The site itself needs no build step.

## BAM Seek

BAM Seek source and tests live in `bam-seek/`. Run `npm ci --prefix bam-seek`
once before refreshing the tool directory. The directory bundler rebuilds its
standalone `tools/bam-seek.html`, including its worker, patched igv.js viewer,
About dialog and third-party notices. See `bam-seek/README.md` for testing.
BAMs, indexes and optional IGV reference files are explicitly selected locally.
The browser version has no localhost command receiver or desktop relay.
