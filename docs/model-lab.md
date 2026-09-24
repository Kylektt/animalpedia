# Animal model study

This local study separates two workflows: reviewing existing models through their publishers' viewers, and building an original Australian sea lion asset. It does not certify that the candidates meet the encyclopedia's species or realism requirements.

## Open locally

Run `npm run dev`, then open <http://127.0.0.1:4173/model-lab.html>. If the existing local server is already running, reuse it. The koala home page links to the study.

The site is buildless. No new package dependencies, account credentials, or paid generation services are required.

## Existing models

Three candidates use official Sketchfab iframe embeds:

- Kangaroo by rinaskylark: textured, but species unconfirmed.
- California sea lion by DigitalLife3D: a visual benchmark, explicitly not an Australian sea lion.
- Hopping Mouse prototype by Jack.Schiller: a stylized comparison, not a realistic or species-verified asset.

The embeds require internet access and retain the publishers' controls, branding, and scene settings. They are not local GLB downloads and do not provide identical lighting across animals. The original model link remains available when third-party content is blocked or unavailable. Cross-origin iframe load events cannot establish successful 3D rendering, so the page does not report them as proof of success.

Animations and automatic spin are disabled in the embed URLs. The official [initialization documentation](https://sketchfab.com/developers/viewer/initialization) describes these parameters. No premium controls or branding removal are requested.

Source availability and license metadata are recorded in `dist/assets/model-lab-sources.json`. Embedding a public viewer does not grant permission to download or redistribute its mesh. See [the sourcing audit](realistic-animal-assets.md) for unresolved species and asset gaps.

## Original experiment

The default selection is now the original adult-female Australian sea lion experiment. Its GLB is 11,241,104 bytes, with 127,274 triangles, one mesh containing five material primitives, and two embedded 2K textures. Three-quarter and side inspection images were rendered after reimporting that exported GLB; the front image comes from the source Blender scene. The inspected exports retain the generated coat texture and facial materials, but the anatomy and overall appearance remain stylized.

The served asset and its provenance are under `dist/assets/sea-lion/`. Reproduction scripts are under `tools/sea-lion/`. To generate a separate output package with the editable `.blend` file:

```sh
/Applications/Blender.app/Contents/MacOS/Blender --background --factory-startup --python tools/sea-lion/build_sea_lion.py -- --output-dir /tmp/animalpedia-sea-lion
/Applications/Blender.app/Contents/MacOS/Blender --background --factory-startup --python tools/sea-lion/verify_glb.py -- --output-dir /tmp/animalpedia-sea-lion
```

The original editable `.blend` and full inspection package also remain locally in `/Users/kt/Temp/codex-build-day-deliverables/sea-lion-build/`. Reference photographs are not included in the repository or embedded in the GLB. The experiment establishes a reproducible modeling and export path; it does not establish photorealistic quality.

The original-model path in the page uses the existing vendored model-viewer renderer. It supports drag, zoom, rotation/pause, reset, clickable topic markers, reduced motion, load errors, and rendered inspection views. Camera orientation and topic coordinates belong to the individual asset.

Generated geometry is an artistic approximation, not a scientific scan. Evaluate the actual exported GLB from multiple directions, including the face, flipper roots, silhouette, and texture seams. A plausible silhouette alone does not establish photorealism or species accuracy.

## Files and checks

- `dist/model-candidates.js`: model identity, provenance links, presentation notes, and local-asset configuration.
- `dist/model-lab.html`, `dist/model-lab.js`, `dist/model-lab.css`: comparison page and viewer lifecycle.
- `tools/koala-3d/validate-model-lab.mjs`: source and asset checks, called by `npm run check`.

Checks cover local references, JavaScript syntax, explicit species labels, safe embed IDs, motion defaults, and (when present) local GLB structure and embedded textures. External embed URLs returned HTTP 200 during integration on 2026-09-24. This verifies endpoint access, not browser rendering. Browser interaction and responsive layout have not been visually tested in this session.

No new deployment is part of this work. All changes remain on the task branch for local review.
