import { mkdir, copyFile, readFile, writeFile, readdir } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { createHash } from 'node:crypto';
import { execFileSync } from 'node:child_process';
import { candidates } from '../dist/model-candidates.js';

const root = fileURLToPath(new URL('../', import.meta.url));
const output = path.resolve(process.argv[2] ?? path.join(root, '../codex-build-day-deliverables/animalpedia-nextjs-kit'));
const components = path.join(output, 'components/animalpedia');
const publicRoot = path.join(output, 'public/animalpedia');
await mkdir(components, { recursive: true });
await mkdir(path.join(publicRoot, 'vendor'), { recursive: true });
await mkdir(path.join(output, 'examples'), { recursive: true });
const packaged = [];
async function copy(from, to) { await copyFile(from, to); packaged.push(path.relative(output, to)); }
async function write(to, text) { await writeFile(to, text); packaged.push(path.relative(output, to)); }
for (const file of ['AnimalCard.tsx', 'AnimalCard.module.css', 'types.ts']) {
  await copy(path.join(root, 'integrations/nextjs', file), path.join(components, file));
}
await copy(path.join(root, 'integrations/nextjs/README.md'), path.join(output, 'README.md'));
await copy(path.join(root, 'integrations/nextjs/AnimalGallery.tsx'), path.join(output, 'examples/AnimalGallery.tsx'));
for (const file of ['model-viewer.min.js', 'model-viewer.LICENSE']) {
  await copy(path.join(root, 'dist/vendor', file), path.join(publicRoot, 'vendor', file));
}
const records = {};
for (const animal of candidates.filter((entry) => entry.type === 'local')) {
  const id = animal.id.replace(/-original$/, '');
  const relative = `models/${id}`;
  const dir = path.join(publicRoot, relative);
  await mkdir(dir, { recursive: true });
  await copy(path.join(root, 'dist', animal.model), path.join(dir, 'model.glb'));
  await copy(path.join(root, 'dist', animal.poster), path.join(dir, 'poster.png'));
  const sourceDir = path.dirname(path.join(root, 'dist', animal.model));
  for (const file of (await readdir(sourceDir)).filter((file) => /^(README\.md|.*\.json)$/.test(file))) {
    await copy(path.join(sourceDir, file), path.join(dir, file));
  }
  records[id] = {
    id, name: animal.name, scientificName: animal.scientificName, description: animal.description,
    model: `${relative}/model.glb`, poster: `${relative}/poster.png`, cameraOrbit: animal.cameraOrbit,
    cameraTarget: animal.cameraTarget ?? 'auto auto auto', topics: animal.topics,
    credit: 'Original Animalpedia 3D illustration. Topic markers are editorial anchors, not anatomical measurements.',
  };
}
await write(path.join(components, 'animals.ts'), `import type { AnimalCardData } from './types';\n\nexport const animals: Record<string, AnimalCardData> = ${JSON.stringify(records, null, 2)};\n`);
await write(path.join(output, 'manifest.json'), JSON.stringify({ formatVersion: 1, renderer: '@google/model-viewer 4.3.1', animals: Object.keys(records) }, null, 2) + '\n');
const validationPath = path.join(root, 'integrations/nextjs/VALIDATION.md');
await copy(validationPath, path.join(output, 'VALIDATION.md'));
const hashes = [];
for (const file of [...packaged].sort()) hashes.push(`${createHash('sha256').update(await readFile(path.join(output, file))).digest('hex')}  ${file}`);
await write(path.join(output, 'SHA256SUMS'), hashes.join('\n') + '\n');
const zipPath = `${output}.zip`;
execFileSync('python3', ['-c', 'import sys,zipfile,pathlib,json; root=pathlib.Path(sys.argv[1]); z=zipfile.ZipFile(sys.argv[2],"w",zipfile.ZIP_DEFLATED); [z.write(root/p,root.name+"/"+p) for p in json.loads(sys.argv[3])]; z.close()', output, zipPath, JSON.stringify(packaged)]);
console.log(JSON.stringify({ directory: output, zip: zipPath, models: Object.keys(records), files: packaged.length }, null, 2));
