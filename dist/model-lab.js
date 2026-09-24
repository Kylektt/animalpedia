import { candidates, embedUrl } from './model-candidates.js';

const $ = (id) => document.getElementById(id);
const motion = window.matchMedia('(prefers-reduced-motion: reduce)');
let viewer = null;
let current = null;
let ready = false;
let loadVersion = 0;
let timer;
let rendererPromise;

function rotate(value) {
  const running = Boolean(value && ready && viewer);
  if (viewer) viewer.autoRotate = running;
  $('lab-rotation').textContent = running ? 'Pause rotation' : 'Start rotation';
  $('lab-rotation').setAttribute('aria-pressed', String(running));
}

function fact(topic) {
  rotate(false);
  $('lab-fact-title').textContent = topic.title;
  $('lab-fact-body').textContent = topic.body;
  $('lab-fact-source').href = topic.source;
  document.querySelectorAll('[data-topic]').forEach((button) => {
    button.setAttribute('aria-pressed', String(button.dataset.topic === topic.id));
  });
}

function topicControls(model) {
  $('lab-topics').replaceChildren();
  $('lab-topics').hidden = !model.topics?.length;
  $('lab-fact').hidden = !model.topics?.length;
  for (const [index, topic] of (model.topics ?? []).entries()) {
    const button = document.createElement('button');
    button.type = 'button'; button.className = 'topic'; button.dataset.topic = topic.id;
    button.textContent = topic.label; button.setAttribute('aria-controls', 'lab-fact');
    button.addEventListener('click', () => fact(topic));
    $('lab-topics').append(button);
    if (viewer && topic.position) {
      const hotspot = document.createElement('button');
      hotspot.type = 'button'; hotspot.className = 'hotspot'; hotspot.dataset.topic = topic.id;
      hotspot.slot = `hotspot-${topic.id}`;
      hotspot.dataset.position = topic.position.map((v) => `${v}m`).join(' ');
      hotspot.dataset.normal = topic.normal.join(' '); hotspot.dataset.visibilityAttribute = 'visible';
      hotspot.textContent = String(index + 1).padStart(2, '0'); hotspot.hidden = true;
      hotspot.setAttribute('aria-label', `Learn about ${topic.label.toLowerCase()}`);
      hotspot.setAttribute('aria-controls', 'lab-fact');
      hotspot.addEventListener('click', (event) => { event.stopPropagation(); fact(topic); });
      viewer.append(hotspot);
    }
  }
  if (model.topics?.length) fact(model.topics[0]);
}

function renderLocal(model, version) {
  viewer = document.createElement('model-viewer');
  const activeViewer = viewer;
  const attrs = {
    src: model.model, poster: model.poster, alt: model.description,
    'camera-controls': '', 'disable-pan': '', 'disable-tap': '', 'touch-action': 'pan-y',
    'camera-orbit': model.cameraOrbit, 'camera-target': model.cameraTarget ?? 'auto auto auto', 'field-of-view': '30deg',
    'min-camera-orbit': 'auto 25deg 60%', 'max-camera-orbit': 'auto 110deg 200%',
    'shadow-intensity': '0.8', 'shadow-softness': '1', exposure: '1',
    'environment-image': 'neutral', 'interaction-prompt': 'none',
    'rotation-per-second': '12deg', loading: 'eager', reveal: 'auto',
  };
  for (const [key, value] of Object.entries(attrs)) activeViewer.setAttribute(key, value);
  const fail = () => {
    if (version !== loadVersion) return;
    clearTimeout(timer); ready = false; rotate(false);
    $('lab-rotation').disabled = true; $('lab-reset').disabled = true;
    activeViewer.querySelectorAll('.hotspot').forEach((h) => { h.hidden = true; });
    $('viewer-status').textContent = 'The interactive model could not load. Inspect the rendered views below, or select this model again to retry.';
  };
  activeViewer.addEventListener('load', () => {
    if (version !== loadVersion) return;
    clearTimeout(timer); ready = true;
    $('viewer-status').textContent = 'Original model loaded. Select a numbered marker to explore.';
    $('lab-rotation').disabled = false; $('lab-reset').disabled = false;
    activeViewer.querySelectorAll('.hotspot').forEach((h) => { h.hidden = false; });
    rotate(!motion.matches);
  });
  activeViewer.addEventListener('error', fail);
  activeViewer.addEventListener('pointerdown', () => rotate(false));
  activeViewer.addEventListener('keydown', () => rotate(false));
  $('viewer-host').append(activeViewer);
  $('viewer-status').textContent = 'Loading the original sea lion model…';
  timer = setTimeout(fail, 30000);
  rendererPromise ??= import('./vendor/model-viewer.min.js');
  rendererPromise.catch(fail);
}

function selectModel(model) {
  loadVersion += 1; clearTimeout(timer); rotate(false); ready = false; viewer = null; current = model;
  $('viewer-host').replaceChildren();
  $('lab-rotation').disabled = true; $('lab-reset').disabled = true;
  $('model-name').textContent = model.name; $('model-species').textContent = model.scientificName;
  $('model-status').textContent = model.status; $('model-description').textContent = model.description;
  $('model-caveat').textContent = model.caveat; $('model-detail').textContent = model.detail;
  $('model-creator').textContent = model.creator;
  $('model-license').replaceChildren();
  if (model.licenseUrl) {
    const link = document.createElement('a'); link.href = model.licenseUrl; link.textContent = model.license;
    link.target = '_blank'; link.rel = 'noopener noreferrer'; $('model-license').append(link);
  } else $('model-license').textContent = model.license;
  $('model-source').href = model.source;
  $('model-source').textContent = model.type === 'embed' ? 'Open the original model ↗' : 'Download the experimental GLB ↗';
  $('viewer-kind').textContent = model.type === 'embed' ? 'Creator’s online viewer' : 'Original · Local model';
  $('local-controls').hidden = model.type !== 'local';
  document.querySelectorAll('[data-model]').forEach((button) => button.setAttribute('aria-pressed', String(button.dataset.model === model.id)));
  if (model.type === 'embed') {
    const frame = document.createElement('iframe'); frame.src = embedUrl(model);
    frame.title = `${model.name} — interactive model by ${model.creator}`;
    frame.allow = 'autoplay; fullscreen; xr-spatial-tracking'; frame.allowFullscreen = true;
    $('viewer-host').append(frame);
    $('viewer-status').textContent = 'Use the viewer’s controls to explore. If the preview is blocked or stays blank, open the original model using the link beside it.';
  } else renderLocal(model, loadVersion);
  topicControls(model);
  $('inspection').hidden = !model.views?.length;
  $('inspection-images').replaceChildren();
  for (const view of model.views ?? []) {
    const figure = document.createElement('figure'); const img = document.createElement('img');
    img.src = view.src; img.alt = view.label; img.loading = 'lazy';
    const caption = document.createElement('figcaption'); caption.textContent = view.label;
    figure.append(img, caption); $('inspection-images').append(figure);
  }
  history.replaceState(null, '', `#${model.id}`);
}

for (const model of candidates) {
  const button = document.createElement('button'); button.type = 'button'; button.className = 'model-choice';
  button.dataset.model = model.id; button.setAttribute('aria-controls', 'viewer-host');
  const label = document.createElement('span'); label.textContent = model.type === 'embed' ? 'Existing model' : 'Original experiment';
  button.append(label, document.createTextNode(model.name));
  button.addEventListener('click', () => selectModel(model)); $('model-choices').append(button);
}
$('lab-rotation').addEventListener('click', () => rotate(!viewer?.autoRotate));
$('lab-reset').addEventListener('click', () => {
  if (!viewer || !ready) return;
  rotate(false); viewer.resetTurntableRotation(); viewer.cameraOrbit = current.cameraOrbit;
  viewer.cameraTarget = current.cameraTarget ?? 'auto auto auto'; if (motion.matches) viewer.jumpCameraToGoal();
});
motion.addEventListener('change', () => { if (motion.matches) rotate(false); });
document.addEventListener('visibilitychange', () => { if (document.hidden) rotate(false); });
selectModel(candidates.find((m) => `#${m.id}` === location.hash) ?? candidates[0]);
