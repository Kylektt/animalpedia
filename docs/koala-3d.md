# Koala 3D explorer

A deliberately small, static prototype on `feat/koala-3d-explorer`.

## Run locally

Requires Python 3. Node.js 20+ is needed only for the optional npm shortcuts and source checks.

```sh
python3 -m http.server 4173 --bind 127.0.0.1 --directory dist
```

Open `http://127.0.0.1:4173/`. No dependency installation or build is required: the browser module is vendored at a pinned version.

```sh
npm run check
```

## Structure

- `dist/index.html`: page structure and loading/error fallbacks.
- `dist/styles.css`: responsive presentation.
- `dist/app.js`: model interaction and topic selection.
- `dist/animal-data.js`: model paths, camera setup, knowledge, and hotspot coordinates.
- `dist/assets/koala.glb`: locally served model, with all geometry/material data embedded.
- `dist/assets/credits.json`: asset provenance, source links, and license information.
- `dist/vendor/model-viewer.min.js`: Google model-viewer 4.3.1; Apache-2.0 license is included alongside it.
- `.openai/hosting.json`: Sites static deployment configuration. This does not deploy GitHub branches automatically.

`dist/` contains authored source in this buildless prototype; it is intentionally tracked. There is no app backend, API key, database, or third-party model request at runtime. The included model does not require external decoders. The external museum and attribution URLs are ordinary links.

## Interactions

- Rotate or zoom using mouse, touch, or keyboard camera controls.
- Automatic rotation stops when the user interacts, opens a topic, or leaves the tab.
- A button explicitly restarts rotation. Reduced-motion preferences disable initial auto-rotation.
- Numbered model markers and matching topic buttons show the same fact panel.
- A short click on the mesh selects the nearest topic anchor; dragging does not select a fact.
- Reset restores the initial camera and turntable orientation.
- Loading errors retain the poster and independently usable fact controls, with a retry button.

The model is a stylized illustration. Hotspots are editorial topic anchors, not anatomical labels. Facts are summarized from the Australian Museum and link to the original source.

## Add the next animal

1. Choose a model with compatible visual style and a license permitting distribution in this public source repository.
2. Store its GLB and poster under `dist/assets/`, with author, source, and license records.
3. Update the data record, camera orientation, and model-space hotspot coordinates. The current page's name, scientific name, attribution, and fallback copy must also be updated. This is a single-animal prototype, not yet a multi-animal router.
4. Verify rotation, marker positions, keyboard access, mobile scrolling, and failure states in the target browser.

## Validation boundary

The source checker validates syntax, local file references, embedded GLB data, hotspot bounds, and attribution. The model was also imported in Blender to render the local poster. These checks do not establish browser rendering or touch behavior. A browser smoke test remains necessary before merging the prototype into the main application.

To reproduce the poster, run `tools/koala-3d/render-poster.py` with Blender in background mode from any working directory. The model is unchanged; only the poster is a new rendered derivative.
