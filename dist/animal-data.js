export const animal = {
  id: 'koala',
  name: 'Koala',
  scientificName: 'Phascolarctos cinereus',
  model: './assets/koala.glb',
  poster: './assets/koala-poster.png',
  cameraOrbit: '60deg 78deg 115%',
  source: 'https://australian.museum/learn/animals/mammals/koala/',
  topics: [
    {
      id: 'diet', label: 'Diet', title: 'A specialist leaf-eater.',
      body: 'Koalas mainly eat leaves from selected eucalypt species. Their food provides both nutrients and moisture.',
      position: [3.15, 6.65, 0], normal: [1, 0, 0],
    },
    {
      id: 'habitat', label: 'Habitat', title: 'At home in the canopy.',
      body: 'Koalas live in eucalypt forests. Their patchy range extends from northern Queensland to southern Victoria and south-eastern South Australia.',
      position: [1.0, 3.8, 2.9], normal: [0.5, 0, 1],
    },
    {
      id: 'adaptations', label: 'Adaptations', title: 'Built for a leafy diet.',
      body: 'Eucalypt leaves are high in fibre. A long caecum, part of the large intestine, helps koalas digest this food.',
      position: [2.65, 2.4, 0.2], normal: [1, 0, 0],
    },
  ],
};

// Topic markers are editorial anchors, not anatomical annotations.
export function nearestTopic(position, topics = animal.topics) {
  return topics.reduce((best, topic) => {
    const distance = (candidate) => candidate.position.reduce(
      (sum, value, index) => sum + (value - position[index]) ** 2, 0,
    );
    return distance(topic) < distance(best) ? topic : best;
  }, topics[0]);
}
