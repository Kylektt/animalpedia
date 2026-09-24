# Red kangaroo model experiment

Original static adult male red kangaroo, **Osphranter rufus**, created for Animalpedia in the same textured illustrative style as the accepted original sea lion. This is an experimental modeled interpretation, not a photogrammetric scan or scientifically validated anatomical specimen.

## Files

- `red-kangaroo-experimental.glb`: standalone Y-up GLB with two embedded 2048px PNG textures (base color and tangent normal).
- `red-kangaroo-experimental.blend`: editable imported GLB geometry, material images and neutral studio setup.
- `build_kangaroo.py`: creates original continuous lofts, voxel-blends skin geometry, bakes textures, exports GLB, reimports GLB, and renders all three inspection views.
- `three-quarter.png`, `side.png`, `front.png`: actual renderings of the exported GLB after reimport, not Blender-only procedural materials.
- `asset-metadata.json`, `validation.json`: measured geometry and artifact checks.

Run:

```sh
/Applications/Blender.app/Contents/MacOS/Blender --background --python build_kangaroo.py -- --output-dir /absolute/output/path
```

The output directory is optional and defaults to the script's directory. Source reference photographs are not needed to run the script.

## Provenance

The geometry, procedural texture patterns and scripts were created for this task. No third-party mesh or image texture, purchase or paid generation service was used. This is project-created experimental work; no additional broad license has been assigned.

Three real red-kangaroo photographs credited to Brad Leue/AWC on the Australian Wildlife Conservancy species page were viewed to guide the ears, tapered muzzle, reddish male coat, cream underside, large thighs and small forearms. The photographs were used as visual reference only, not projected or baked into the mesh. They retain their owners' copyright and are **not part of the model deliverable**. Do not copy the local `reference-*.jpg` research files into the repository or downloadable package.

Sources checked on 2026-09-24:

- Australian Wildlife Conservancy, Red Kangaroo: https://www.australianwildlife.org/en-gb/animals/red-kangaroo
- Perth Zoo, Red Kangaroo: https://perthzoo.wa.gov.au/animal/red-kangaroo
- Atlas of Living Australia, accepted species identity: https://bie.ala.org.au/species/https%3A/biodiversity.org.au/afd/taxa/7e6e134b-2bc7-43c4-b23a-6e3f420f57ad

The named species and male coat direction are grounded in these references; individual mesh proportions and the resting pose are estimated.

## Artifact checks

The final GLB is 10,747,172 bytes and contains 106,094 triangles in one mesh with seven material primitives. Its two texture images are embedded; it has no external URI or required glTF extension. All three inspection views are produced only after exporting and reimporting the GLB.

## Integration

Coordinates are meters, +Y up, head facing +X. The floor, lights and camera are not exported. Suggested starting settings:

- `camera-target="-0.42m 0.88m 0m"`
- `camera-orbit="48deg 78deg 3.6m"`
- Face hotspot: `0.46 1.31 0.05`
- Hind leg hotspot: `0.02 0.48 0.30`
- Tail hotspot: `-0.95 0.13 0.04`

Hotspots are editorial anchors, not anatomical segmentation. The integration owner should verify placement and framing in the final viewer.

## Limits

The model is deliberately consistent with the accepted sea-lion illustration style rather than photorealistic. It has no rig or locomotion animation. Short fur is baked surface detail; no strand fur is simulated. Head and limb proportions, paws, claw count/details, and facial anatomy require specialist review before any scientific use. Mesh production and GLB roundtrip render checks do not substitute for browser/mobile testing.
