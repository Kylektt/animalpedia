export const candidates = [
  {
    id: 'australian-sea-lion-original', name: 'Australian sea lion', scientificName: 'Neophoca cinerea',
    type: 'local', model: './assets/sea-lion/australian-sea-lion-experimental.glb',
    poster: './assets/sea-lion/three-quarter.png', cameraOrbit: '45deg 76deg 2.9m',
    cameraTarget: '-0.25m 0.6m 0m',
    creator: 'Animalpedia · Codex modeling experiment',
    license: 'Project-created experiment; no third-party mesh', licenseUrl: null,
    source: './assets/sea-lion/australian-sea-lion-experimental.glb',
    status: 'Original model · Experimental',
    description: 'An original static model intended to depict an adult female Australian sea lion, with embedded coat textures, flippers and whiskers. Rotate it and select a numbered topic marker.',
    caveat: 'A procedural modeling experiment, not a scan. It remains stylized and has not reached photorealistic or anatomically validated quality.',
    detail: 'Built in Blender using original geometry and generated surface detail. Photographs informed the shape and coat colors; they are not used as textures. The first two inspection views were rendered from the exported GLB reimported into Blender.',
    views: [
      { src: './assets/sea-lion/three-quarter.png', label: 'Three-quarter view · exported GLB' },
      { src: './assets/sea-lion/side.png', label: 'Side view · exported GLB' },
      { src: './assets/sea-lion/front.png', label: 'Front view · source Blender model' },
    ],
    topics: [
      { id: 'coat', label: 'Coat', title: 'A lighter coat for females.', body: 'Adult females have silver-grey to fawn backs and creamy undersides. Males have darker coats with yellowish areas around the neck and head.', position: [0.60, 0.97, 0.12], normal: [1, 0.4, 0.4], source: 'https://australian.museum/learn/animals/mammals/australian-sea-lion/' },
      { id: 'habitat', label: 'Habitat', title: 'Sheltered Australian shores.', body: 'Australian sea lions favor sandy beaches in sheltered bays. The species is native to Australian waters, with breeding islands off Western Australia and South Australia.', position: [-0.23, 0.55, 0.24], normal: [0, 0.3, 1], source: 'https://australian.museum/learn/animals/mammals/australian-sea-lion/' },
      { id: 'form', label: 'Form', title: 'Stocky bodies, narrow flippers.', body: 'The Australian Museum describes a large head, a stocky body and short, narrow flippers. This experimental model approximates these features; its proportions are not specimen measurements.', position: [0.04, 0.12, 0.40], normal: [0, 1, 1], source: 'https://australian.museum/learn/animals/mammals/australian-sea-lion/' },
    ],
  },
  {
    id: 'kangaroo', name: 'Kangaroo', scientificName: 'Species unconfirmed',
    type: 'embed', uid: '31236db25afe445e8444b0ce8e22d53d',
    creator: 'rinaskylark', license: 'CC BY 4.0',
    licenseUrl: 'https://creativecommons.org/licenses/by/4.0/',
    source: 'https://sketchfab.com/3d-models/kangaroo-31236db25afe445e8444b0ce8e22d53d',
    status: 'Existing model · Textured candidate',
    description: 'A full-body kangaroo with textured fur. Explore the shape and surface detail from different angles.',
    caveat: 'The creator has not identified the species. This is not yet verified as a red kangaroo.',
    detail: 'The source marks this model as downloadable. A local copy still requires the supported download flow and species review.',
  },
  {
    id: 'california-sea-lion', name: 'California sea lion', scientificName: 'Zalophus californianus',
    type: 'embed', uid: '03b669280cc6464c8ea8ab7b48128259',
    creator: 'DigitalLife3D', license: 'CC BY-NC 4.0',
    licenseUrl: 'https://creativecommons.org/licenses/by-nc/4.0/',
    source: 'https://sketchfab.com/3d-models/model-85-california-sea-lion-03b669280cc6464c8ea8ab7b48128259',
    status: 'Existing model · Photogrammetry',
    description: 'A full-body model of Ariel, a female California sea lion, published by DigitalLife3D. Use it as a visual benchmark for the original model experiment.',
    caveat: 'This is a California sea lion, not the Australian sea lion requested for the encyclopedia.',
    detail: 'The source carries a noncommercial license. This preview embeds the creator’s viewer; it does not redistribute the mesh.',
  },
  {
    id: 'hopping-mouse', name: 'Hopping mouse prototype', scientificName: 'Species unconfirmed',
    type: 'embed', uid: '13e27b8b7ca84fde9e99baa3be07ef14',
    creator: 'Jack.Schiller', license: 'No download license provided', licenseUrl: null,
    source: 'https://sketchfab.com/3d-models/hopping-mouse-prototype-13e27b8b7ca84fde9e99baa3be07ef14',
    status: 'Existing model · Stylized study',
    description: 'An early sculpt and rig study, shown here to compare the available starting material. The creator notes deformation issues.',
    caveat: 'This is a stylized prototype, not a realistic spinifex hopping mouse. Exact species is unconfirmed.',
    detail: 'The creator has not enabled downloads. This preview uses the public embed only; no local mesh or reuse license is included.',
  },
];

export function embedUrl(candidate) {
  if (candidate.type !== 'embed' || !/^[a-f0-9]{32}$/.test(candidate.uid)) {
    throw new Error('Expected a reviewed Sketchfab model ID.');
  }
  const url = new URL(`https://sketchfab.com/models/${candidate.uid}/embed`);
  url.search = new URLSearchParams({ autostart: '1', autospin: '0', animation_autoplay: '0', camera: '0', dnt: '1' });
  return url.href;
}
