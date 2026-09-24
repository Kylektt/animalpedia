# Animalpedia contributor instructions

- Write all project documentation, issues, PR descriptions, and user-facing copy in English. The initial MVP uses English animal names and content.
- Read README.md, CONTRIBUTING.md, and the assigned issue before changing files.
- Keep changes scoped to the assigned task. Coordinate shared configuration, dependencies, routes, and data contracts with the integration owner.
- The 3D prototype is a buildless static site in `dist/` using a vendored model-viewer module. Preserve this simple setup unless the assigned task requires a framework. The full encyclopedia application's stack is not selected yet.
- Use a task branch and propose changes through a pull request after the initial repository bootstrap.
- Preserve teammates' uncommitted changes. Never reset or overwrite unrelated work.
- Keep animal facts traceable to sources and image credits traceable to their licenses. Label unverified content explicitly.
- Run checks appropriate to the change and report what actually ran. For UI changes, verify the relevant page and responsive layout when a runnable app exists.
- Never commit secrets or local environment files. Do not publish a deployment unless the user or assigned task authorizes it.
