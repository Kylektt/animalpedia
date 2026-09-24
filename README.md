# Animalpedia 🐾

A collaborative animal encyclopedia inspired by Wikipedia, built for the Codex Hackathon.

Our goal: help people discover animals, read reliable information, and explore the sources behind it.

## Current status

A simple [interactive koala prototype](docs/koala-3d.md) is available on this branch: a locally served 3D model, rotation controls, and three source-linked knowledge topics. The full encyclopedia application has not been implemented yet.

The [model study](docs/model-lab.md) compares existing online candidates with an original Australian sea lion experiment. Open `http://127.0.0.1:4173/model-lab.html` after starting the server. These are review assets, not approved realistic encyclopedia models; see the [sourcing report](docs/realistic-animal-assets.md) for species and quality gaps.

Run the prototype with `python3 -m http.server 4173 --bind 127.0.0.1 --directory dist`, then open `http://127.0.0.1:4173/`. No package installation is required. Run `npm run check` for source and asset validation.

The separate [animal media pack](https://github.com/Kylektt/animalpedia/releases/tag/media-pack-2026-09-24) contains 18 photos and 4 videos for the team, with source records and an English handoff on the release page. Download the ZIP from the release assets; it is not stored in Git history.

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

The current prototype uses static HTML, CSS, JavaScript, and a pinned local copy of model-viewer. The full application's stack remains a team decision.

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
