# Handoff validation

Checked on 2026-09-24:

- Standalone App Router integration: Next.js **16.3.6**, React **19.3.0**, Node.js **22.23.2**. Production build and TypeScript checks pass, including server prerendering of the Client Component.
- Original assets: three standalone GLB 2.0 files, each with embedded base-color and normal textures. No external mesh/texture URLs or required decoder extensions.
- Asset sizes: sea lion 11,241,104 bytes; red kangaroo 10,747,172 bytes; spinifex hopping mouse 12,670,200 bytes.
- Triangle counts: sea lion 127,274; kangaroo 106,094; mouse 128,432.
- The exported animal GLBs were reimported into Blender and actual renders were inspected. Modeling scripts and provenance are preserved in the source repository.
- Local HTTP serving, required component files, package-relative paths, and SHA-256 archive records are checked. These checks establish the packaged data and build integration, not visual equivalence between every browser/GPU.
- Card spacing is bounded in CSS and the model stage no longer stretches to the length of the details column. The included component scopes its CSS and includes mobile/narrow-container layouts.

Browser interaction and responsive screenshots have not been captured during this handoff. Before merging into the final app, check drag/zoom, topic selection, repeated animal switching, mobile scrolling, and the error/retry state in the team's target browser. The original sea-lion appearance was approved by the project owner; the new animals follow that illustrative direction and await their visual review.
