export type AnimalTopic = {
  id: string;
  label: string;
  title: string;
  body: string;
  source: string;
  position: [number, number, number];
  normal: [number, number, number];
};

export type AnimalCardData = {
  id: string;
  name: string;
  scientificName: string;
  description: string;
  model: string;
  poster: string;
  cameraOrbit: string;
  cameraTarget: string;
  topics: AnimalTopic[];
  credit: string;
};

export type AnimalCardProps = {
  animal: AnimalCardData;
  /** Public asset root, including your Next.js basePath if applicable. */
  assetBasePath?: string;
  className?: string;
};
