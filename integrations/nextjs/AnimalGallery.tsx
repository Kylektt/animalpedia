'use client';

import { useState } from 'react';
import { AnimalCard } from '../components/animalpedia/AnimalCard';
import { animals } from '../components/animalpedia/animals';

export default function AnimalGallery() {
  const [selected, setSelected] = useState('australian-sea-lion');
  return <main style={{ maxWidth: 1000, margin: '40px auto', padding: '0 20px' }}>
    <label style={{ display: 'block', marginBottom: 16 }}>
      Choose an animal{' '}
      <select value={selected} onChange={(event) => setSelected(event.target.value)} style={{ font: 'inherit', padding: 8 }}>
        {Object.values(animals).map((animal) => <option key={animal.id} value={animal.id}>{animal.name}</option>)}
      </select>
    </label>
    <AnimalCard animal={animals[selected]} />
  </main>;
}
