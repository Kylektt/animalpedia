# Animal data contract (draft for team agreement)

Agree on this format before building the directory, detail pages, and content in parallel. For the first version, use static JSON with one file per animal: `data/animals/<id>.json`. This proposal is independent of the frontend framework.

| Field | Type | Meaning |
| --- | --- | --- |
| id | string | Stable English slug used by detail routes |
| nameEn | string | English common name |
| scientificName | string | Scientific name |
| category | string | Category filter value agreed by the team |
| summary | string | Short introduction |
| habitat | string | Habitat description |
| diet | string | Diet description |
| sources | Source[] | Supporting references; at least one for real content |
| image | Image or null | Image with licensing records; use a placeholder when null |

`Source`: `id`, `title`, `url`, `accessedAt` (YYYY-MM-DD), and `supports` (an array of field names supported by this source).

`Image`: `url`, `alt`, `sourceUrl`, `creator`, `license`, `licenseUrl`, and `attribution`.

Rules:

- Each `id` is unique and uses lowercase English letters, numbers, and hyphens. Agree on detail URLs during frontend setup.
- Directory and detail pages read the same data. Do not maintain separate copies of names or summaries.
- Confirm the allowed `category` values before collecting content.
- Missing images must not prevent a page from rendering.
- Omit uncertain facts rather than inventing values to fill fields.
- When adding conservation status, weight, lifespan, or other fields, also define relevant units, sources, and time context.
- Use English for content, image descriptions, and interface copy. Additional languages are outside the initial MVP.

This is a working draft. No loader or validator has been implemented yet.
