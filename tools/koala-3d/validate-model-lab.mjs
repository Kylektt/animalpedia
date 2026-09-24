import assert from 'node:assert/strict';
import { readFile, stat } from 'node:fs/promises';
import { execFileSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import { candidates, embedUrl } from '../../dist/model-candidates.js';

const dist = new URL('../../dist/', import.meta.url);
const html = await readFile(new URL('model-lab.html', dist), 'utf8');
assert(html.includes('<html lang="en">'));
for (const [, reference] of html.matchAll(/(?:src|href|poster)="(\.\/[^"#]*)"/g)) {
  assert((await stat(new URL(reference, dist))).isFile() || reference === './', reference);
}
for (const file of ['model-candidates.js', 'model-lab.js']) {
  execFileSync(process.execPath, ['--check', fileURLToPath(new URL(file, dist))]);
}
assert.equal(new Set(candidates.map((m) => m.id)).size, candidates.length);
let localCount = 0;
for (const model of candidates) {
  assert(model.name && model.scientificName && model.creator && model.license && model.source && model.caveat);
  if (model.type === 'embed') {
    const url = new URL(embedUrl(model));
    assert.equal(url.origin, 'https://sketchfab.com');
    assert.equal(url.searchParams.get('autospin'), '0', 'Embedded viewers must not rotate automatically.');
    assert.equal(url.searchParams.get('animation_autoplay'), '0');
    assert.equal(url.searchParams.get('dnt'), '1');
    assert.equal(model.model, undefined, 'Embedded candidates must not imply a locally downloaded mesh.');
    continue;
  }
  assert.equal(model.type, 'local'); localCount += 1;
  assert(model.model && model.poster && model.cameraOrbit && model.views?.length >= 3);
  for (const file of [model.model, model.poster, ...model.views.map((view) => view.src)]) {
    assert((await stat(new URL(file, dist))).size > 0, file);
  }
  const bytes = await readFile(new URL(model.model, dist));
  assert.equal(bytes.toString('ascii', 0, 4), 'glTF');
  assert.equal(bytes.readUInt32LE(4), 2);
  assert.equal(bytes.readUInt32LE(8), bytes.length);
  const gltf = JSON.parse(bytes.toString('utf8', 20, 20 + bytes.readUInt32LE(12)));
  assert(gltf.meshes?.length > 0);
  assert(!gltf.extensionsRequired?.length, 'Local GLB must not require an external decoder.');
  assert(gltf.buffers.every((buffer) => !buffer.uri));
  assert(gltf.images?.length > 0, 'The original model must contain its baked surface textures.');
  assert(gltf.images.every((image) => Number.isInteger(image.bufferView) && !image.uri));
  const primitives = gltf.meshes.flatMap((mesh) => mesh.primitives);
  for (const p of primitives) {
    const a = gltf.accessors[p.attributes.POSITION];
    assert(a.min.every(Number.isFinite) && a.max.every(Number.isFinite));
    assert.equal(p.mode ?? 4, 4, 'Expected triangulated meshes.');
  }
  const triangleCount = primitives.reduce((n, p) => n + gltf.accessors[p.indices ?? p.attributes.POSITION].count / 3, 0);
  console.log(`${model.name}: ${bytes.length} bytes, ${triangleCount} triangles, ${gltf.images.length} embedded images.`);
  for (const topic of model.topics ?? []) {
    assert(topic.id && topic.label && topic.title && topic.body && new URL(topic.source).protocol === 'https:');
    assert.equal(topic.position.length, 3); assert.equal(topic.normal.length, 3);
    assert(topic.position.every(Number.isFinite) && topic.normal.every(Number.isFinite));
    assert(topic.normal.some((v) => v !== 0));
  }
}
assert.equal(candidates.find((m) => m.id === 'california-sea-lion').scientificName, 'Zalophus californianus');
assert.match(candidates.find((m) => m.id === 'hopping-mouse').caveat, /not a realistic spinifex/);
assert.throws(() => embedUrl({ type: 'embed', uid: '../bad-id' }));
console.log(`PASS: model lab sources, references, species labels, ${candidates.length - localCount} embeds and ${localCount} local models.`);
console.log('This check does not establish browser rendering or external viewer availability.');
