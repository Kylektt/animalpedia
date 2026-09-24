# Animalia: South Australian content handover

Prepared and sources checked: **24 September 2026**. Original editorial summaries for an independent concept for Tourism SA; no official partnership is claimed.

## Integration notes

Scope: three animal profiles and their evidence, for the journey discover an animal → understand its environment → explore a relevant place → choose responsible behaviour. These cover mainland mallee, inland desert and island coast; Seal Bay should not stand for all of South Australia.

The repository currently contains planning documents only. [The draft contract](data-contract.md) proposes one JSON file per animal, but category values have not been agreed. This document is the content source for review, not a new runtime schema. No shared contract or README has been changed.

- Copy `id`, `nameEn`, `scientificName`, `summary`, `habitat` and `diet` into their matching contract fields after review. Use `image: null`; media sourcing is outside this handover.
- `category` is pending team agreement. All three are mammals biologically; do not invent a filter enum.
- Each source below supplies `id`, `title`, `url`, `accessedAt` and `supports`. Inline source IDs identify the evidence for each passage; they are editorial markers, not part of the final prose.
- Headline, ecological connection, memorable fact, threats, destination, visitor action, visitor link and caveats are editorial sections pending an agreed schema extension. Keep them together when integrating; do not silently discard the access caveats.
- No issue was supplied or claimed remotely. Before a PR, link this scoped content task to the team's issue. Nothing has been pushed or merged.

## Western grey kangaroo

**id:** `western-grey-kangaroo`

**nameEn:** Western grey kangaroo

**scientificName:** *Macropus fuliginosus*

**Headline:** Meet a grazer of the southern landscapes

**summary:** A western grey kangaroo brings southern Australia's plant life into focus. This herbivore feeds on grasses and shrubs; watching quietly offers a chance to notice the animal and the landscape that supports it. [K1]

**habitat:** Found across southern Australia in habitats including forests and grasslands. [K1]

**diet:** Coarse grasses and some shrubs. [K1]

**Ecological connection:** Its feeding connects it directly to the vegetation around it: grasses and shrubs are food, not just scenery. [K1; editorial interpretation of diet, not a measured ecosystem effect]

**Memorable fact:** A newborn joey climbs to its mother's pouch while still tiny, hairless and with its eyes closed. [K1]

**Threats and visitor pressure:** Feeding wildlife can cause illness and disrupt natural behaviour. This is a practical visitor-related risk, not evidence that western grey kangaroos are nationally threatened. [K3]

**South Australian destination:** Ngarkat Conservation Park, in the state's south-east, protects mallee and heath landscapes. The park authority explicitly records western grey kangaroos there. A visit is an opportunity to explore their environment; sightings are not guaranteed. [K2]

**Responsible visitor action:** Watch quietly from a distance. Do not approach or feed kangaroos, and remain on designated tracks. [V1; observing at a distance is our practical application of the no-disturbance advice]

**Official visitor link:** [Plan a visit to Ngarkat Conservation Park](https://www.parks.sa.gov.au/parks/ngarkat-conservation-park).

**Editorial caveats:** The park currently specifies 4WD-only access. Check its current alerts and access requirements before travel or publication. Its suggested visiting months describe park conditions, not a verified kangaroo-viewing season. No species-wide threat ranking or conservation-status badge is supplied: the reviewed kangaroo sources do not establish a current, jurisdiction-specific assessment. The feeding warning is general wildlife guidance, not a species-specific population study. [K2, K3]

### Sources

All `accessedAt`: `2026-09-24`.

| id | title / url | supports |
| --- | --- | --- |
| K1 | [Perth Zoo — Western Grey Kangaroo](https://perthzoo.wa.gov.au/animal/western-grey-kangaroo) | nameEn, scientificName, summary, habitat, diet, ecological connection (interpretation), memorable fact |
| K2 | [NPWS SA — Ngarkat Conservation Park](https://www.parks.sa.gov.au/parks/ngarkat-conservation-park) | destination, visitor link, access caveats; see Plants and animals and Getting there |
| K3 | [NPWS SA — Baudin Conservation Park](https://www.parks.sa.gov.au/parks/baudin-conservation-park) | visitor-related threats; see Keep wildlife wild; not used as this profile's destination |
| V1 | [NPWS SA — Leave no trace](https://www.parks.sa.gov.au/know-before-you-go/leave-no-trace) | responsible visitor action |

## Spinifex hopping-mouse

**id:** `spinifex-hopping-mouse`

**nameEn:** Spinifex hopping-mouse

**scientificName:** *Notomys alexis*

**Headline:** Discover desert life after dark

**summary:** Much of this small native rodent's day happens out of sight. Spinifex hopping-mice shelter together in deep, humid burrows during hot days, emerging above ground at night. They are rodents, not marsupials. [M1, M2]

**habitat:** Sandy desert environments and spinifex grasslands provide places to shelter and forage. Underground burrows offer refuge during the heat of the day. [M1, M3]

**diet:** Seeds form the core of the diet, supplemented by green plant material, roots, insects and other invertebrates when available. [M3]

**Ecological connection:** Desert grasses provide both food and cover. Spinifex tussocks offer seeds and shelter, linking the mouse's daily life to the plants around its burrow. [M3]

**Memorable fact:** Its tunnels reach down into damp sand, where shared burrows provide a humid daytime refuge. [M1]

**Threats:** Cats, foxes and habitat loss are identified threats to the spinifex hopping-mouse. [M2]

**South Australian connection — occurrence only:** Bush Heritage records this species at Bon Bon Station Reserve, and identifies the reserve as being in South Australia. This supports a connection to the state's inland environments. It does not establish a public wildlife-viewing experience or permission to enter. [M2, M4]

**Responsible visitor action:** When visiting permitted natural areas, stay on designated tracks and leave wildlife and burrows undisturbed. [V1; leaving burrows alone is our practical application of the no-disturbance advice]

**Official visitor-information link:** [Read South Australia's leave-no-trace guidance](https://www.parks.sa.gov.au/know-before-you-go/leave-no-trace). This is general visitor guidance, not a destination or booking link.

**Editorial caveats:** No accessible viewing experience, public access permission or best viewing season has been verified. Keep this as a discovery-and-habitat profile; do not add a “see it here” map pin or booking call to action. Bon Bon is additional occurrence evidence, not a replacement tourism destination. Bush Heritage discusses several hopping-mouse species: only its explicitly species-specific threat and occurrence statements are used here. No formal conservation-status badge is supplied.

The previously supplied [Maralinga Tjarutja biological survey](https://data.environment.sa.gov.au/Content/Publications/Maralinga-Tjuratja_BioSurvey.pdf) could not be retrieved during this check. Its reported occurrence evidence is carried forward from the user's prior research only, and is not relied upon in the publishable copy above. Reopen it and record the page/table before using the Maralinga claim; a survey record would still not imply access permission.

### Sources

All entries below successfully retrieved; `accessedAt`: `2026-09-24`. The inaccessible survey above is excluded from this checked source list.

| id | title / url | supports |
| --- | --- | --- |
| M1 | [Australian Museum — The Red Centre](https://australian.museum/publications/surviving-australia/red-centre/) | nameEn, scientificName, summary, habitat, memorable fact; Spinifex Hopping Mouse section |
| M2 | [Bush Heritage — Hopping mice](https://www.bushheritage.org.au/species/hopping-mice) | summary (rodent classification), threats, SA occurrence; species-specific status paragraph and reserve list |
| M3 | [Australian Reptile Park — Spinifex Hopping Mouse](https://www.reptilepark.com.au/about/meet-our-animals/spinifex-hopping-mouse) | habitat, diet, ecological connection |
| M4 | [Bush Heritage — Bon Bon Station Reserve](https://www.bushheritage.org.au/places/bon-bon) | SA location of occurrence record; not public access |
| V1 | [NPWS SA — Leave no trace](https://www.parks.sa.gov.au/know-before-you-go/leave-no-trace) | responsible visitor action, visitor-information link |

## Australian sea lion

**id:** `australian-sea-lion`

**nameEn:** Australian sea lion

**scientificName:** *Neophoca cinerea*

**Headline:** Follow a life between sea and shore

**summary:** An Australian sea lion resting ashore is only showing part of its story. At sea, it dives for prey; on land, coastal colonies provide places to rest and breed. [S1, S2]

**habitat:** Coastal and marine environments of South Australia and Western Australia. Breeding sites include island shores and some mainland beaches and rocky bays. [S2]

**diet:** Squid, octopus, fish and crustaceans. [S1]

**Ecological connection:** As a marine predator that also rests on land, its life connects feeding grounds at sea with coastal colony sites. [S1, S2; editorial synthesis, not a quantified ecosystem-service claim]

**Memorable fact:** Females generally return to the beach where they were born to breed and produce pups. [S1]

**Threats:** Interactions with fishing gear and entanglement in marine debris, including discarded nets and rope, can harm Australian sea lions. [S1, S2]

**Conservation status:** Endangered — Australian national EPBC listing, checked 24 September 2026. This is a national classification; no state or global classification is asserted here. [S2]

**South Australian destination:** Seal Bay on Kangaroo Island offers a managed setting to learn about an Australian sea lion colony and its coastal environment. [S3]

**Responsible visitor action:** View and photograph from permitted areas, give animals space, follow guide instructions and restrictions, and take your rubbish home. [S3, V1]

**Official visitor link:** [Check current viewing access at Seal Bay](https://www.parks.sa.gov.au/experiences/seal-bay).

**Editorial caveats:** On 24 September 2026 the official page still advertised temporarily paused beach access, with boardwalk viewing available. Recheck immediately before publication and before a visit. Do not advertise beach tours or imply beach access has resumed. Do not promise sightings, use unverified seasonal advice, or freeze prices and opening hours into this copy. [S3]

Use the current species-specific federal page for national status. Older Seal Bay FAQ and recovery materials can retain the former national “Vulnerable” classification. Neither visitor clicks nor bookings demonstrate a conservation outcome.

### Sources

All `accessedAt`: `2026-09-24`.

| id | title / url | supports |
| --- | --- | --- |
| S1 | [AFMA — Australian sea lions](https://www.afma.gov.au/protected-species/australian-sea-lions) | summary, diet, ecological connection, memorable fact, fishing threats |
| S2 | [DCCEEW — Australian sea-lion](https://www.dcceew.gov.au/environment/biodiversity/threatened/action-plan/australian-sea-lion) | nameEn, scientificName, summary, habitat, ecological connection, threats, national conservation status |
| S3 | [NPWS SA — Seal Bay](https://www.parks.sa.gov.au/experiences/seal-bay) | destination, viewing action, visitor link, temporary access caveat |
| V1 | [NPWS SA — Leave no trace](https://www.parks.sa.gov.au/know-before-you-go/leave-no-trace) | responsible visitor action |

## Review and release checklist

- Agree category values and how the extra editorial sections will enter the shared data contract before producing runtime JSON. Retain the stable IDs above.
- Keep the hopping-mouse encounter gap visible. A complete destination journey is currently supported for kangaroo and sea lion, not for hopping-mouse.
- The kangaroo threat paragraph addresses visitor pressure only. Broader species-level threats need additional targeted evidence if required for the interface.
- Recheck destination alerts before release. Sources were retrieved through web browsing; a checked date is not a promise that visitor conditions will remain unchanged.
- If optional interactions are later approved, label them “Illustrative scenario”. A day/night reveal or responsible-choice response must not claim scientific prediction or measured conservation benefit. No interaction or organisation-account scope is approved by this document.
- Review the original prose and evidence links with a teammate before integration. No media, population estimates, guaranteed encounters or climate-attribution claims are included.
