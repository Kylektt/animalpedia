# Original Spinifex hopping mouse model

An original naturalistic model study for Animalpedia, depicting **Notomys alexis**. This is a posed educational illustration, not a photogrammetry scan or an anatomically validated specimen. The target is visual consistency with Animalpedia's approved original Australian sea lion.

## Deliverables

- `spinifex-hopping-mouse-original.glb`: self-contained web asset with embedded PBR textures. No remote URLs or runtime texture downloads.
- `spinifex-hopping-mouse-original.blend`: editable source with the asset only.
- `build_mouse.py`: deterministic, portable Blender generation script. Run with Blender 5.2 or later and `--output-dir`.
- `glb-roundtrip-three-quarter.png`, `glb-roundtrip-side.png`, `glb-roundtrip-front.png`: images rendered after deleting the source mesh and reimporting the exported GLB.
- `asset-metadata.json`: bounds, triangle count, file size, model-viewer camera suggestion, and topic anchors in glTF Y-up coordinates.
- `mouse-basecolor.png`, `mouse-normal.png`: original generated 2048px textures, also embedded in the GLB.

```sh
blender --background --python build_mouse.py -- --output-dir ./mouse-output
```

The exported GLB contains the animal only. Preview floors, camera, lighting and shadows are presentation helpers and are not exported. Blender source uses +X forward / +Z up; glTF uses +X forward / +Y up. Mesh measurements are illustration units and must not be interpreted as real-world animal size.

## Appearance and scope

Distinctive cues include a sandy dorsal coat, pale throat and belly, large lateral dark eyes, thin cupped ears, elongated hind feet, small forepaws, and a long curving tail with a dark tuft. The pose is static. No skeletal rig, morph targets, movement animation, or scientific measurement claims are included. Three numbered hotspots are editorial topic anchors, not anatomy labels.

## Provenance

All geometry and texture pixels were generated specifically for this project from the included script. No marketplace models, paid tools, third-party meshes, or photo-derived texture maps are used. The artifact can follow the Animalpedia project's original-asset license. The following primary sources informed identification and proportions, accessed 2026-09-24:

1. [Northern Territory Government — Spinifex hopping mouse](https://nt.gov.au/environment/animals/wildlife-in-nt/spinifex-hopping-mouse): long hind legs, tail tuft, dark eyes, light brown fur, pale belly, nocturnal desert habitat.
2. [Adelaide Zoo — Spinifex hopping mouse](https://www.adelaidezoo.com.au/animals/spinifex-hopping-mouse/): species identity and reference photograph; reviewed for head, ears, muzzle, eyes and coat proportions.

The local `reference-adelaide-zoo.jpg` is **viewing reference only**. It is not an original project asset, is not included in the model or texture maps, and must not be redistributed with the model delivery package. Preserve source links instead.
