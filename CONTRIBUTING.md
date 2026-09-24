# Contribution guide

## One task, one owner, one branch

- Claim an issue before starting. State your scope and acceptance criteria.
- Suggested branch names: `feat/12-animal-search`, `fix/23-mobile-layout`, or `docs/7-animal-sources`.
- Use your own local clone; do not share a working directory.
- Merge changes into `main` through PRs. This is a team convention; repository initialization does not imply enforced branch protection.
- Keep PRs small and ask at least one teammate to review them. After merging, the integration owner should let the team know to update their branches.
- Coordinate changes to shared configuration, dependencies, route entry points, and data structures with the integration owner.
- Discuss data format changes with affected teammates and update both the contract and its consumers.
- Write documentation, issues, PR descriptions, and user-facing copy in English.

## Daily workflow

Start a task:

```sh
git switch main
git pull --ff-only
git switch -c feat/12-animal-search
```

When ready, stage the specific files you changed, then commit and push:

```sh
git add path/to/changed-file
git commit -m "feat: add animal search"
git push -u origin HEAD
```

Open a PR on GitHub describing the change and how you verified it. Use `Closes #12` to link the issue. Inspect your diff before submitting to avoid unrelated files or secrets.

## Verification and content

- Check the issue's acceptance criteria. Never report a test as passing unless you ran it.
- Include desktop or mobile screenshots for page changes.
- Treat AI-generated animal facts as unverified until checked against reliable sources.
- Prefer traceable museum, zoo, and research institution material. Keep source links and access dates.
- Record image sources, creators, licenses, and required attribution, and confirm that the images can be used.
- Never commit `.env` files, API keys, credentials, or private user data.

## Team rhythm

At each check-in, share what is done, what comes next, and any blockers. Merge the smallest usable flow first, then add content and visual improvements.
