# Animalpedia 🐾

A collaborative animal encyclopedia inspired by Wikipedia, built for the Codex Hackathon.

Our goal: help people discover animals, read reliable information, and explore the sources behind it.

## Current status

The collaboration repository is ready. The application has not been implemented yet. The team will select the technology stack in the first task.

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

Installation, development, and build commands will be added when the stack is initialized.

## Suggested responsibilities

| Owner | Responsibilities | Coordination boundary |
| --- | --- | --- |
| Kyle: browsing and integration | Setup, home page, directory, search, filters, builds, and demo | Coordinate dependencies, shared configuration, and route scaffolding |
| Teammate: details and content | Detail pages, 10 animal entries, image licenses, and sources | One data file per animal; shared IDs across directory and detail pages |

The current team has two members. Agree on the data format and visual direction together, then each own a complete feature area and review each other's PRs. Each person can use Codex on their task branch and should inspect the result before submitting it.

Spend the first 20 minutes agreeing on the stack, data format, and routes. Get one animal working from directory to detail page, then expand in parallel. Merge small, working changes every 45–60 minutes. Reserve roughly the final 20% of the event for integration and the demo.

## Demo acceptance criteria

- A user can find an animal and open its detail page.
- Empty search results, missing images, and unknown animal URLs have useful fallback states.
- Pages work on mobile and desktop.
- Facts and images can be traced to their sources.
- The README includes verified setup instructions and the demo URL when available.

This is an independent Hackathon project with no affiliation to Wikipedia or Wikimedia.
