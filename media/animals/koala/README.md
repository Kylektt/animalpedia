# Koala Feeding

A 15-second, real-time live-action clip of a koala holding a leafy branch and feeding. No AI-generated imagery, narration, music, or text overlays.

## Files

| File | Purpose |
| --- | --- |
| `koala-feeding.mp4` | Landscape close-up, 1280 × 720, H.264, 30 fps, silent |
| `koala-feeding-portrait.mp4` | Full original composition, 720 × 1280, H.264, 30 fps, silent |
| `poster.jpg` | Landscape poster |
| `poster-portrait.jpg` | Portrait poster |
| `metadata.json` | Source, license, edit details, dimensions, and SHA-256 hashes |
| `qa.json` | Media verification results |

The landscape version crops the original portrait footage around the head, leaves, and forelimbs. Use the portrait version when the complete body and surroundings matter.

## Source and license

- Original: [Koala Feeding.webm](https://commons.wikimedia.org/wiki/File:Koala_Feeding.webm)
- Creator credited on the source page: Classy Melissa
- License: [CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/)
- Source description: filmed on Phillip Island, Victoria, on 6 February 2020.
- Edit: source seconds 8–23, normal speed; crop/resize, audio removed, encoded for web playback.

Suggested credit: Footage: Classy Melissa / Wikimedia Commons (CC0 1.0). Edited for Animalpedia.

## Website integration

Copy the chosen video and poster into your application's static asset directory. The following example assumes they are served from `/media/animals/koala/`; configure those paths for your chosen framework.

```html
<figure>
  <video
    controls
    playsinline
    preload="none"
    poster="/media/animals/koala/poster.jpg"
    width="1280"
    height="720"
    style="display: block; width: 100%; height: auto;"
    aria-label="A koala holding a leafy branch and feeding on leaves"
  >
    <source src="/media/animals/koala/koala-feeding.mp4" type="video/mp4" />
    <a href="/media/animals/koala/koala-feeding.mp4">Download the video</a>
  </video>
  <figcaption>
    A koala holds a leafy branch and feeds on leaves.
    Footage: Classy Melissa / Wikimedia Commons (CC0 1.0).
  </figcaption>
</figure>
```

Both MP4s passed complete decode checks and duration/codec/fast-start checks. The landscape version was visually inspected using one frame per second. Playback within the final application still needs to be checked after integration.
