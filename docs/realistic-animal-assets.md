# Realistic Australian animal assets

Research date: 2026-09-24. Branch: `feat/realistic-australian-animals`.

## Scope and current result

Use free assets only, with realistic anatomy and surface detail. The agreed species are spinifex hopping mouse (*Notomys alexis*), Australian sea lion (*Neophoca cinerea*), and red kangaroo (*Osphranter rufus*). Keep the existing local, buildless model-viewer setup and English interface.

**No model has passed the final realism acceptance requirements.** The subsequent [model study](model-lab.md) integrates the existing candidates through official online embeds and an original experimental Australian sea lion as a local GLB. The original has been rendered and inspected but remains stylized. This sourcing record is not a completed three-species realistic demo. No purchase or new deployment was performed.

## Candidates reviewed

| Candidate | Evidence checked | Decision |
| --- | --- | --- |
| [Kangaroo — rinaskylark](https://sketchfab.com/3d-models/kangaroo-31236db25afe445e8444b0ce8e22d53d) | Public API reports downloadable, CC BY 4.0. Preview shows a textured full-body animal with fur detail. Description only says “Kangaroo model”; red kangaroo identity is unconfirmed. Official download endpoint returned HTTP 401 without authentication. | Promising visual candidate, pending species confirmation and an authorized download. Preview inspection does not establish mesh quality or performance. |
| [Hopping Mouse prototype — Jack.Schiller](https://sketchfab.com/3d-models/hopping-mouse-prototype-13e27b8b7ca84fde9e99baa3be07ef14) | Public API reports not downloadable and provides no license. Preview is stylized. Author describes an early sculpt and rig with deformation problems. | Reject: unavailable for reuse, insufficient realism, and exact species unconfirmed. |
| [Spinifex hopping mouse base mesh — 3PDMedia](https://www.turbosquid.com/3d-models/3d-c4d-spinifex-hopping-mouse/1028542) | Paid listing; base mesh rather than a finished textured asset. | Exclude under the free-only constraint. |
| [WAM M3998 Australian sea lion jaw — Western Australian Museum](https://sketchfab.com/3d-models/213a8b6c24a94ac9aeca4c3af157e480) | Museum listing identifies an Australian sea lion jaw. | Reject for this scene: partial skeletal specimen, not a living full-body animal. |
| [Model 85 California sea lion — DigitalLife3D](https://sketchfab.com/3d-models/model-85-california-sea-lion-03b669280cc6464c8ea8ab7b48128259) | Public API reports downloadable, CC BY-NC 4.0. Full-body preview inspected. Description identifies *Zalophus californianus*. | Reject for the agreed species: California sea lion, not Australian sea lion. It also has a noncommercial restriction. |
| [Exotic Wildlife HD red kangaroo — 3DAssets.dev](https://3dassets.dev/assets/exotic-wildlife-hd-red-kangaroo-14d31816) | Listing claims CC0. Candidate GLB downloaded outside the repository; supplied poster inspected. Poster shows obvious primitive-like forms and a smooth toy-like surface. | Reject for visual quality. No application integration. |

The search did not establish that suitable free assets do not exist; it did not find a complete, usable set in the sources reviewed. No alternate species is approved as a replacement.

## Shared rendering specification

Apply this specification after an asset passes review:

- Use one local GLB per species with textures embedded; preserve source units and record any transform applied during export.
- Use the same viewer, pale neutral background, environment lighting, exposure, shadow settings, rotation speed, and interaction controls.
- Fit each animal within the same visual frame while displaying its real-world size separately. Equal screen size must not imply equal physical size.
- Choose a comparable three-quarter default view. Inspect front, side, and rear views before acceptance; the landing view alone is insufficient.
- Retain pause, reset, drag, zoom, reduced-motion behavior, and clickable fact topics.
- Place topic markers separately for each mesh. The koala's coordinates cannot be reused for another animal.
- Start with a static pose and viewer rotation. A rig or walk cycle is not required for the requested turntable interaction.
- Export a matching poster only after the actual GLB has been inspected. A marketplace thumbnail is not evidence of the local renderer's output.

Suggested initial asset budget: up to 100,000 triangles, 2K textures, and 10 MB per GLB. These are project targets, not verified device limits. Measure load time and interaction on the intended devices once the models are available.

## Acceptance and handoff

For each model, record the source URL, creator, license URL, exact species evidence, original file hash, local asset path, and modifications. The license must permit the intended website use and redistribution of the asset in this public repository. Keep credits distinct from the project's code license.

Acceptance requires a recognizable, correctly proportioned animal with plausible fur or skin, usable texture detail, and no conspicuous seams or malformed limbs. Do not approve an asset based on the words “realistic” or “HD” in a listing.

The kangaroo candidate can proceed once its species is confirmed and its files are obtained through the publisher's supported download flow. The mouse and Australian sea lion still need suitable sources or newly authored models. Until then, keep them out of the animal selector rather than attaching unrelated meshes to their names.

After sourcing, adapt the asset validator for multiple animals and per-asset licenses, load each GLB locally, position its topics, render inspection views, and verify the interactive page. Existing koala validation alone cannot certify the new assets.

## Reproducible metadata checks

Public metadata endpoints inspected:

- <https://api.sketchfab.com/v3/models/31236db25afe445e8444b0ce8e22d53d>
- <https://api.sketchfab.com/v3/models/13e27b8b7ca84fde9e99baa3be07ef14>
- <https://api.sketchfab.com/v3/models/03b669280cc6464c8ea8ab7b48128259>

Fields used: `description`, `isDownloadable`, `license`, and `thumbnails`. Availability and licensing may change; recheck at download time. The kangaroo download endpoint `/v3/models/31236db25afe445e8444b0ce8e22d53d/download` returned `401` with `Authentication credentials were not provided.` No authenticated asset download was completed.
