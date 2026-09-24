# Animalpedia 🐾

A collaborative animal encyclopedia inspired by Wikipedia, built for the Codex Hackathon.

Our goal: help people discover animals, read reliable information, and explore the sources behind it.

## Current status

A simple [interactive koala prototype](docs/koala-3d.md) is available on this branch: a locally served 3D model, rotation controls, and three source-linked knowledge topics. The full encyclopedia application has not been implemented yet.

The [animal cards](docs/model-lab.md) now include original models of an Australian sea lion, red kangaroo and spinifex hopping mouse, following the project owner's accepted sea-lion style. Open `http://127.0.0.1:4173/model-lab.html` after starting the server. They are textured 3D illustrations, not scientific scans.

For the teammate's Next.js application, use the [copy-in component guide](integrations/nextjs/README.md). Generate the component and asset ZIP with `node tools/package-nextjs-kit.mjs /absolute/output/animalpedia-nextjs-kit`. The current sandbox stays buildless; the adapter includes a Client Component, scoped CSS, typed animal records, and local public assets.

Run the prototype with `python3 -m http.server 4173 --bind 127.0.0.1 --directory dist`, then open `http://127.0.0.1:4173/`. No package installation is required. Run `npm run check` for source and asset validation.

The separate [animal media pack](https://github.com/Kylektt/animalpedia/releases/tag/media-pack-2026-09-24) contains 18 photos and 4 videos for the team, with source records and an English handoff on the release page. Download the ZIP from the release assets; it is not stored in Git history.

## Next.js handoff

**Deliverable: three reusable, interactive animal cards for the website.** Place an `AnimalCard` in an animal detail page or a featured-animal section. It includes the 3D animal, camera controls, numbered information markers, source-linked facts, and the compact card layout.

Recommended integration: download [animalpedia-nextjs-kit.zip](https://github.com/Kylektt/animalpedia/releases/download/animal-cards-v0.1.0/animalpedia-nextjs-kit.zip), then follow the included English README. Copy `components/animalpedia/` and `public/animalpedia/` into the Next.js application. The ZIP is a ready-to-copy snapshot of the component and assets on this branch; the website owner keeps control of routes, page layout, navigation and branding.

```tsx
import { AnimalCard } from '@/components/animalpedia/AnimalCard';
import { animals } from '@/components/animalpedia/animals';

export default function AnimalPage() {
  return <AnimalCard animal={animals['red-kangaroo']} />;
}
```

Animal IDs: `australian-sea-lion`, `red-kangaroo`, `spinifex-hopping-mouse`. The component also accepts another animal record to switch the displayed animal; the kit includes a selector example.

For a custom presentation, the individual `.glb` files and posters can be reused with the website's own viewer. Using the supplied component preserves the demonstrated interactions and framing. `dist/model-lab.html` is the local preview; the Next.js integration entry point is `AnimalCard.tsx` in the kit. The separate photo/video media pack linked above serves editorial media needs.

Source is on [`feat/realistic-australian-animals`](https://github.com/Kylektt/animalpedia/tree/feat/realistic-australian-animals). Changes are committed and pushed to that feature branch; integration into the website and any merge into `main` remain with the website owner.

## Proposed Hackathon MVP

- Animal directory with images, names, and categories.
- Search and category filters.
- Animal detail pages with common and scientific names, a summary, habitat, diet, and source links.
- Start with well-researched content for 10 animals before expanding.
- Cite important facts and record image creators, sources, and licenses.

Optional highlights: animal comparisons, map exploration, or a quiz. Choose one after the core flow works.

## Getting started

1. Join the repository as a collaborator. Public visibility alone does not grant write access.
2. Claim a task in [Issues](https://github.com/Kylektt/animalpedia/issues) and agree on its owner.
3. Read the [contribution guide](CONTRIBUTING.md) and [draft data contract](docs/data-contract.md).
4. Create a task branch from the latest `main`, then open a pull request when ready.
5. Ask your teammate to review it before the integration owner merges it.

```sh
git clone https://github.com/Kylektt/animalpedia.git
cd animalpedia
git switch -c feat/your-task
```

The current prototype uses static HTML, CSS, JavaScript, and a pinned local copy of model-viewer. The teammate plans to build the full application in Next.js; use the provided adapter to integrate these cards.

## Suggested responsibilities

| Owner | Responsibilities | Coordination boundary |
| --- | --- | --- |
| Kyle: 3D assets and media | Animal models, consistent presentation, posters, topic markers, and asset provenance | Deliver models and metadata that the site can reuse |
| Teammate: application and integration | Pages, directory, search, shared components, and integration | Coordinate dependencies, shared configuration, and routes |

The current team has two members. Agree on the data format and visual direction together, then each own a complete feature area and review each other's PRs. Each person can use Codex on their task branch and should inspect the result before submitting it.

Spend the first 20 minutes agreeing on the stack, data format, and routes. Get one animal working from directory to detail page, then expand in parallel. Merge small, working changes every 45–60 minutes. Reserve roughly the final 20% of the event for integration and the demo.

## Demo acceptance criteria

- A user can find an animal and open its detail page.
- Empty search results, missing images, and unknown animal URLs have useful fallback states.
- Pages work on mobile and desktop.
- Facts and images can be traced to their sources.
- The README includes verified setup instructions and the demo URL when available.

This is an independent Hackathon project with no affiliation to Wikipedia or Wikimedia.
