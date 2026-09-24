# Australian sea lion: original model experiment

An original static adult-female Australian sea lion (Neophoca cinerea) prototype for Animalpedia. This is a procedural sculpting experiment for visual evaluation, not a photogrammetric scan or scientifically validated anatomical model. It has not reached photorealistic asset quality.

## Deliverables

This served folder contains a subset of the full modeling handoff: the GLB, metadata, validation record, and three inspection PNGs. Here `three-quarter.png` and `side.png` are the exported-GLB roundtrip renders; `front.png` is the source-scene render. Reproduction scripts live at `tools/sea-lion/` in the repository. The editable `.blend` and all original filenames below remain in the local full handoff directory, `/Users/kt/Temp/codex-build-day-deliverables/sea-lion-build/`.

- `australian-sea-lion-experimental.glb`: embedded base-color and tangent normal textures, Y-up, no external image dependencies, static pose.
- `australian-sea-lion-experimental.blend`: editable mesh, baked materials and presentation studio.
- `build_sea_lion.py`: reproducible original geometry, material baking, export and four-view rendering in Blender 5.2.2.
- `verify_glb.py`: reimports the delivered GLB for material/export verification.
- `three-quarter.png`, `side.png`, `front.png`, `rear.png`: source Blender renders.
- `glb-roundtrip-three-quarter.png`, `glb-roundtrip-side.png`: actual renders of the exported GLB after reimport.
- `asset-metadata.json`: bounds, triangle count and file size.

The asset is project-created experimental work with no third-party mesh; no additional broad license has been assigned.

Final geometry: 127,274 triangles, one mesh with five material primitives, 11,241,104-byte GLB. Two embedded 2048px textures, no external URIs and no required glTF extensions. Structural checks and GLB roundtrip render inspection passed; browser/WebGL validation remains with the integration owner.

Run with `/Applications/Blender.app/Contents/MacOS/Blender --background --python build_sea_lion.py`, then the same command with `verify_glb.py`. Either script accepts `-- --output-dir /absolute/output/path` after the Blender arguments.

## Provenance and reference use

The geometry, texture pattern and Python scripts were created for this task. No third-party mesh, image texture, paid generation service or purchase was used. The downloaded reference photos were viewed for shape and color only; they are **not baked into the model or included in its GLB**. Reference photographs have their own copyright and are not part of the generated asset license. Do not redistribute the local reference copies as project assets.

Reference observations:

- DCCEEW describes a blunt muzzle, small rolled external ears, and adult-female ash-grey upper coat with cream underside: https://www.dcceew.gov.au/environment/biodiversity/threatened/action-plan/australian-sea-lion
- Australian Museum describes stocky bodies, short narrow flippers and female silver-grey/fawn backs with cream underside: https://australian.museum/learn/animals/mammals/australian-sea-lion/
- Actual photograph viewed on the Australian Museum page: Kasia-aus, CC BY-SA 4.0, beach group at Seal Bay. Reference-only file `reference-museum.jpg`. https://media.australian.museum/media/dd/thumbnails/images/Sea_lions_on_the_beach.048e7b7.width-1200.97a2b82.jpg
- Actual DCCEEW photograph viewed, seated sea lion: reference-only file `reference-dcceew.jpg`. https://www.dcceew.gov.au/sites/default/files/images/australian-sea-lion-card-image.jpg

The two sources were checked on 2026-09-24. Their descriptive facts inform the visual direction; proportions are estimated rather than measured from a specimen.

## Known limitations

This is a seated static animal with no rig, movement, LOD or full fur simulation. The coat is baked microtexture, not individual short hairs. The forehead, eye sockets, flipper digits, mouth and skin folds remain approximations. The base is a continuous lofted surface with voxel-blended appendages rather than an expert hand-sculpted anatomical surface. A realistic species-specific final asset would need expert anatomical refinement, stronger photographic texture references and additional sculpting. The render is a practical quality checkpoint, not a claim that realism is solved.

## Integration

The GLB uses meters, +Y up and the head facing +X. Use `camera-orbit="45deg 76deg 2.9m"` and `camera-target="-0.25m 0.6m 0m"` as a starting angle. The original model's studio floor, cameras and lights are excluded from the GLB.

Suggested editorial hotspot anchors (GLB x/y/z): face `0.68 1.02 0.05`, front flipper `0.04 0.12 0.40`, body `-0.23 0.55 0.24`. These are content anchors, not anatomical classifications; check label occlusion in the actual viewer.
