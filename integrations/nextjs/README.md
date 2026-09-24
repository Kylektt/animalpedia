# Animalpedia cards for Next.js

Copy-in React components and original animal assets. The existing site stays buildless; this adapter is for the teammate's Next.js application.

## Integrate

1. Copy this kit's `components/animalpedia/` into your project's `components/` (or `src/components/`).
2. Copy `public/animalpedia/` into your project's `public/`.
3. Render a card from an App Router page:

```tsx
import { AnimalCard } from '@/components/animalpedia/AnimalCard';
import { animals } from '@/components/animalpedia/animals';

export default function Page() {
  return <AnimalCard animal={animals['australian-sea-lion']} />;
}
```

Available records are `australian-sea-lion`, `red-kangaroo`, and `spinifex-hopping-mouse`. The generated `animals.ts` file is the source of truth for the packaged records. If your project has no `@/` alias, use a relative import instead.

`AnimalCard` owns the `'use client'` boundary. Your page can remain a Server Component. The renderer loads only after mount; no WebGL, `window`, or custom-element registration runs on the server. No React Three Fiber, Tailwind, backend, API key, remote model host, or new npm dependency is required. The included Google model-viewer 4.3.1 bundle and its Apache-2.0 license live in `public/animalpedia/vendor/`.

## Configure

```tsx
<AnimalCard
  animal={animals['red-kangaroo']}
  assetBasePath="/animalpedia"
  className="my-card"
/>
```

`assetBasePath` is the public URL prefix, not a filesystem path. For a Next.js `basePath` of `/guide`, pass `/guide/animalpedia`. For CDN hosting, use the complete asset URL prefix and configure that server's CORS headers. Next.js `assetPrefix` does not automatically rewrite files in `public/`.

The scoped CSS module uses a bounded model stage (up to 420px; 330px on small screens), independent of fact text height. Keep the parent container at least 280px wide. Avoid overriding its model height to `100vh` or stretching the stage to an unrelated sidebar's height.

## Change content

The serializable `AnimalCardData` type includes model and poster paths relative to `assetBasePath`, scientific name, camera framing, and source-linked topics. You may edit topic text and source URLs in `animals.ts`; position and normal coordinates belong to the individual GLB and should not be copied between animals. Keep names consistent with the supplied species.

Each card has rotation/pause, reset, drag/zoom, numbered hotspots, topic buttons, reduced-motion support, a server-rendered poster, retry on load failure, and source attribution. A single card can change animals by receiving another data record. Multiple cards can coexist: the renderer loads once, IDs are instance-specific, and viewers clean up on unmount. The example `examples/AnimalGallery.tsx` shows a single viewer with an animal selector to avoid loading every GLB at once.

## Assets and provenance

These are original project-created 3D illustrations accepted as a visual direction by the project owner. They are not scans or expert-validated anatomical references. No third-party animal mesh or photograph texture is included. Keep the per-animal provenance records with redistributed assets. Reference photographs used during modeling are excluded. The renderer's license is separate from the animal assets; this handoff does not assign a new blanket license to the project.

## Generate and validate the handoff

From the Animalpedia source repository:

```sh
npm run check
node tools/package-nextjs-kit.mjs /absolute/path/to/animalpedia-nextjs-kit
```

This writes a ready-to-copy folder and adjacent ZIP, including checksums. It does not deploy or modify the teammate's application. See `VALIDATION.md` in the release kit for the exact checks and tested versions.

Official references: [Next.js client components](https://nextjs.org/docs/app/getting-started/server-and-client-components), [public static files](https://nextjs.org/docs/app/getting-started/installation), [assetPrefix behavior](https://nextjs.org/docs/app/api-reference/config/next-config-js/assetPrefix).
