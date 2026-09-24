import { animal, nearestTopic } from './animal-data.js';

const viewer = document.querySelector('#animal');
const rotationButton = document.querySelector('#rotation');
const resetButton = document.querySelector('#reset');
const loading = document.querySelector('#loading');
const error = document.querySelector('#model-error');
const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
let ready = false;
let rotating = false;
let pointerStart = null;
let loadTimer;
const buttons = [];

function setRotation(value) {
  rotating = value && ready;
  viewer.autoRotate = rotating;
  rotationButton.textContent = rotating ? 'Pause rotation' : 'Start rotation';
  rotationButton.setAttribute('aria-pressed', String(rotating));
}

function selectTopic(id, pause = true) {
  const topic = animal.topics.find((entry) => entry.id === id);
  if (!topic) return;
  if (pause) setRotation(false);
  document.querySelector('#fact-category').textContent = topic.label.toUpperCase();
  document.querySelector('#fact-title').textContent = topic.title;
  document.querySelector('#fact-body').textContent = topic.body;
  document.querySelector('#fact-source').href = animal.source;
  buttons.forEach((button) => button.setAttribute('aria-pressed', String(button.dataset.topic === id)));
}

animal.topics.forEach((topic, index) => {
  const button = document.createElement('button');
  button.type = 'button';
  button.className = 'topic';
  button.dataset.topic = topic.id;
  button.setAttribute('aria-controls', 'fact');
  const number = document.createElement('span');
  number.textContent = String(index + 1).padStart(2, '0');
  number.setAttribute('aria-hidden', 'true');
  button.append(number, document.createTextNode(topic.label));
  button.addEventListener('click', () => selectTopic(topic.id));
  document.querySelector('#topics').append(button);

  const hotspot = document.createElement('button');
  hotspot.type = 'button';
  hotspot.className = 'hotspot';
  hotspot.slot = `hotspot-${topic.id}`;
  hotspot.dataset.position = topic.position.map((value) => `${value}m`).join(' ');
  hotspot.dataset.normal = topic.normal.join(' ');
  hotspot.dataset.visibilityAttribute = 'visible';
  hotspot.dataset.topic = topic.id;
  hotspot.textContent = String(index + 1).padStart(2, '0');
  hotspot.setAttribute('aria-label', `Learn about koala ${topic.label.toLowerCase()}`);
  hotspot.setAttribute('aria-controls', 'fact');
  hotspot.hidden = true;
  hotspot.addEventListener('click', (event) => {
    event.stopPropagation();
    selectTopic(topic.id);
  });
  viewer.append(hotspot);
  buttons.push(button, hotspot);
});
selectTopic(animal.topics[0].id, false);

function showError() {
  if (ready) return;
  clearTimeout(loadTimer);
  loading.hidden = true;
  error.hidden = false;
  viewer.hidden = true;
  document.querySelector('#fallback-poster').hidden = false;
  setRotation(false);
}

viewer.addEventListener('load', () => {
  ready = true;
  clearTimeout(loadTimer);
  loading.hidden = true;
  error.hidden = true;
  viewer.hidden = false;
  document.querySelector('#fallback-poster').hidden = true;
  rotationButton.disabled = false;
  resetButton.disabled = false;
  viewer.querySelectorAll('.hotspot').forEach((button) => { button.hidden = false; });
  setRotation(!reducedMotion.matches);
});
viewer.addEventListener('error', () => {
  ready = false;
  rotationButton.disabled = true;
  resetButton.disabled = true;
  viewer.querySelectorAll('.hotspot').forEach((button) => { button.hidden = true; });
  showError();
});
rotationButton.addEventListener('click', () => setRotation(!rotating));
resetButton.addEventListener('click', () => {
  setRotation(false);
  viewer.resetTurntableRotation();
  viewer.cameraOrbit = animal.cameraOrbit;
  viewer.cameraTarget = 'auto auto auto';
  if (reducedMotion.matches) viewer.jumpCameraToGoal();
});
viewer.addEventListener('pointerdown', (event) => {
  setRotation(false);
  pointerStart = { x: event.clientX, y: event.clientY, id: event.pointerId };
});
viewer.addEventListener('pointercancel', () => { pointerStart = null; });
viewer.addEventListener('pointerup', (event) => {
  const start = pointerStart;
  pointerStart = null;
  if (!ready || !start || start.id !== event.pointerId) return;
  if (event.composedPath().some((element) => element.classList?.contains('hotspot'))) return;
  if (Math.hypot(event.clientX - start.x, event.clientY - start.y) > 8) return;
  const rect = viewer.getBoundingClientRect();
  const hit = viewer.positionAndNormalFromPoint(event.clientX - rect.left, event.clientY - rect.top);
  if (hit) selectTopic(nearestTopic([hit.position.x, hit.position.y, hit.position.z]).id);
});
viewer.addEventListener('keydown', () => setRotation(false));
reducedMotion.addEventListener('change', () => { if (reducedMotion.matches) setRotation(false); });
document.addEventListener('visibilitychange', () => { if (document.hidden) setRotation(false); });
document.querySelector('#retry').addEventListener('click', () => window.location.reload());

// Load the renderer after the independent fact controls are available.
loadTimer = setTimeout(showError, 20000);
import('./vendor/model-viewer.min.js').catch(showError);
