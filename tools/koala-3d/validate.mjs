import assert from 'node:assert/strict';
import { readFile, stat } from 'node:fs/promises';
import { execFileSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import path from 'node:path';
import { animal } from '../../dist/animal-data.js';

const root = fileURLToPath(new URL('../../', import.meta.url));
const dist = path.join(root, 'dist');
const html = await readFile(path.join(dist, 'index.html'), 'utf8');
const css = await readFile(path.join(dist, 'styles.css'), 'utf8');
assert(html.includes('<html lang="en">'));
assert(!/@import/.test(css), 'Styles must not depend on remote imports.');
for (const [, reference] of html.matchAll(/(?:src|href|poster)="(\.\/[^"#]*)"/g)) {
  assert((await stat(path.join(dist, reference))).isFile() || reference === './', reference);
}
for (const file of ['app.js', 'animal-data.js', 'vendor/model-viewer.min.js']) {
  execFileSync(process.execPath, ['--check', path.join(dist, file)]);
}
const bytes = await readFile(path.join(dist, animal.model));
assert.equal(bytes.toString('ascii', 0, 4), 'glTF');
assert.equal(bytes.readUInt32LE(4), 2);
assert.equal(bytes.readUInt32LE(8), bytes.length);
const jsonLength = bytes.readUInt32LE(12);
const gltf = JSON.parse(bytes.toString('utf8', 20, 20 + jsonLength));
assert.equal(gltf.asset.version, '2.0');
assert(gltf.meshes.length > 0);
assert(!gltf.extensionsRequired?.length, 'No external decoder should be required.');
assert(gltf.buffers.every((buffer) => !buffer.uri), 'GLB buffers should be embedded.');
assert((gltf.images ?? []).every((image) => !image.uri), 'Images should be embedded.');
const positionAccessors = gltf.meshes.flatMap((mesh) => mesh.primitives.map((p) => gltf.accessors[p.attributes.POSITION]));
const min = [0, 1, 2].map((i) => Math.min(...positionAccessors.map((a) => a.min[i])));
const max = [0, 1, 2].map((i) => Math.max(...positionAccessors.map((a) => a.max[i])));
const ids = new Set();
for (const topic of animal.topics) {
  assert(!ids.has(topic.id)); ids.add(topic.id);
  assert(topic.label && topic.title && topic.body);
  assert.equal(topic.position.length, 3);
  assert.equal(topic.normal.length, 3);
  assert(topic.normal.some((value) => value !== 0));
  topic.position.forEach((value, i) => assert(value >= min[i] - 0.5 && value <= max[i] + 0.5, `Hotspot ${topic.id} outside model bounds`));
}
const credits = JSON.parse(await readFile(path.join(dist, 'assets/credits.json'), 'utf8'));
assert.equal(credits.model.license, 'CC-BY-3.0');
assert(credits.model.creator && credits.model.sourceUrl);
console.log(`PASS: entrypoint, local assets, JavaScript syntax, embedded GLB (${bytes.length} bytes), ${ids.size} hotspot records, and attribution.`);
console.log('Browser rendering and interaction have not been tested by this check.');
