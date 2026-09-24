'use client';

import { useEffect, useId, useRef, useState } from 'react';
import type { AnimalCardProps, AnimalTopic } from './types';
import styles from './AnimalCard.module.css';

type ModelViewer = HTMLElement & {
  autoRotate: boolean;
  cameraOrbit: string;
  cameraTarget: string;
  resetTurntableRotation(): void;
  jumpCameraToGoal(): void;
};

const rendererLoads = new Map<string, Promise<void>>();

function loadRenderer(src: string): Promise<void> {
  if (customElements.get('model-viewer')) return Promise.resolve();
  const pending = rendererLoads.get(src);
  if (pending) return pending;
  const script = document.createElement('script');
  script.type = 'module'; script.src = src;
  const promise = new Promise<void>((resolve, reject) => {
    const timer = window.setTimeout(() => reject(new Error('Renderer load timed out.')), 20000);
    script.onerror = () => { window.clearTimeout(timer); reject(new Error('Renderer could not load.')); };
    script.onload = () => {
      if (customElements.get('model-viewer')) { window.clearTimeout(timer); resolve(); }
      else { window.clearTimeout(timer); reject(new Error('Renderer did not register.')); }
    };
    document.head.append(script);
  }).catch((error) => { script.remove(); rendererLoads.delete(src); throw error; });
  rendererLoads.set(src, promise);
  return promise;
}

/** A self-contained client boundary; safe to render from an App Router server page. */
export function AnimalCard(props: AnimalCardProps) {
  return <AnimalCardContent key={`${props.animal.id}:${props.assetBasePath ?? ''}`} {...props} />;
}

function AnimalCardContent({ animal, assetBasePath = '/animalpedia', className = '' }: AnimalCardProps) {
  const host = useRef<HTMLDivElement>(null);
  const model = useRef<ModelViewer | null>(null);
  const headingId = useId();
  const factId = useId();
  const [status, setStatus] = useState<'loading' | 'ready' | 'error'>('loading');
  const [rotating, setRotating] = useState(false);
  const [selectedId, setSelectedId] = useState(animal.topics[0]?.id);
  const [attempt, setAttempt] = useState(0);
  const base = assetBasePath.replace(/\/$/, '');
  const selected = animal.topics.find((topic) => topic.id === selectedId) ?? animal.topics[0];

  function pause() { if (model.current) model.current.autoRotate = false; setRotating(false); }

  function selectTopic(topic: AnimalTopic) { pause(); setSelectedId(topic.id); }

  useEffect(() => {
    const container = host.current;
    if (!container) return;
    let disposed = false;
    let ready = false;
    let timeout: ReturnType<typeof setTimeout>;
    const motion = window.matchMedia('(prefers-reduced-motion: reduce)');
    const viewer = document.createElement('model-viewer') as ModelViewer;
    model.current = viewer;
    setStatus('loading'); setRotating(false); setSelectedId(animal.topics[0]?.id);
    const attributes: Record<string, string> = {
      src: `${base}/${animal.model}`, poster: `${base}/${animal.poster}`, alt: animal.description,
      'camera-controls': '', 'disable-pan': '', 'disable-tap': '', 'touch-action': 'pan-y',
      'camera-orbit': animal.cameraOrbit, 'camera-target': animal.cameraTarget,
      'field-of-view': '30deg', 'min-camera-orbit': 'auto 25deg 60%', 'max-camera-orbit': 'auto 110deg 200%',
      'environment-image': 'neutral', 'shadow-intensity': '0.8', 'shadow-softness': '1',
      exposure: '1', 'interaction-prompt': 'none', 'rotation-per-second': '12deg', loading: 'eager', reveal: 'auto',
    };
    Object.entries(attributes).forEach(([name, value]) => viewer.setAttribute(name, value));
    viewer.className = styles.viewer;
    const stop = () => { viewer.autoRotate = false; if (!disposed) setRotating(false); };
    const failed = () => {
      if (disposed) return;
      ready = false; clearTimeout(timeout); stop(); setStatus('error');
      viewer.querySelectorAll<HTMLButtonElement>('[data-topic]').forEach((button) => { button.hidden = true; });
    };
    const loaded = () => {
      if (disposed) return;
      ready = true; clearTimeout(timeout); setStatus('ready');
      viewer.querySelectorAll<HTMLButtonElement>('[data-topic]').forEach((button) => { button.hidden = false; });
      viewer.autoRotate = !motion.matches && !document.hidden;
      setRotating(viewer.autoRotate);
    };
    viewer.addEventListener('load', loaded); viewer.addEventListener('error', failed);
    viewer.addEventListener('pointerdown', stop); viewer.addEventListener('keydown', stop);
    animal.topics.forEach((topic, index) => {
      const button = document.createElement('button'); button.type = 'button'; button.className = styles.hotspot;
      button.slot = `hotspot-${topic.id}`; button.dataset.topic = topic.id;
      button.dataset.position = topic.position.map((value) => `${value}m`).join(' ');
      button.dataset.normal = topic.normal.join(' '); button.dataset.visibilityAttribute = 'visible';
      button.textContent = String(index + 1).padStart(2, '0'); button.hidden = true;
      button.setAttribute('aria-label', `Learn about ${topic.label.toLowerCase()}`);
      button.setAttribute('aria-controls', factId);
      button.setAttribute('aria-pressed', String(index === 0));
      button.addEventListener('click', (event) => { event.stopPropagation(); stop(); setSelectedId(topic.id); });
      viewer.append(button);
    });
    container.append(viewer);
    const onMotion = () => { if (motion.matches) stop(); };
    const onVisibility = () => { if (document.hidden) stop(); };
    motion.addEventListener('change', onMotion); document.addEventListener('visibilitychange', onVisibility);
    timeout = setTimeout(() => { if (!ready) failed(); }, 30000);
    loadRenderer(`${base}/vendor/model-viewer.min.js`).catch(failed);
    return () => {
      disposed = true; clearTimeout(timeout); viewer.autoRotate = false;
      motion.removeEventListener('change', onMotion); document.removeEventListener('visibilitychange', onVisibility);
      viewer.remove(); if (model.current === viewer) model.current = null;
    };
  }, [animal, base, attempt, factId]);

  useEffect(() => {
    model.current?.querySelectorAll<HTMLButtonElement>('[data-topic]').forEach((button) => {
      button.setAttribute('aria-pressed', String(button.dataset.topic === selected?.id));
    });
  }, [selected?.id, status]);

  return (
    <section className={`${styles.card} ${className}`} aria-labelledby={headingId}>
      <div className={styles.stage}>
        <div className={styles.stageHeading}><span>EXPLORE IN 3D</span><span>Original animal model</span></div>
        <div className={styles.frame}>
          <div ref={host} className={styles.host} />
          {/* Plain img intentionally preserves a useful server-rendered, dependency-free poster. */}
          {status !== 'ready' && <img className={styles.poster} src={`${base}/${animal.poster}`} alt={animal.description} />}
        </div>
        <p className={styles.status} role="status">
          {status === 'loading' ? 'Loading the 3D model…' : status === 'error' ? 'Showing a still image. The 3D model could not load.' : 'Drag to rotate · Select a marker to explore'}
        </p>
        <div className={styles.controls}>
          {status === 'error' && <button type="button" onClick={() => setAttempt((n) => n + 1)}>Try again</button>}
          <button type="button" disabled={status !== 'ready'} aria-pressed={rotating} onClick={() => {
            if (!model.current) return;
            model.current.autoRotate = !rotating; setRotating(!rotating);
          }}>{rotating ? 'Pause rotation' : 'Start rotation'}</button>
          <button type="button" disabled={status !== 'ready'} onClick={() => {
            const viewer = model.current; if (!viewer) return;
            pause(); viewer.resetTurntableRotation(); viewer.cameraOrbit = animal.cameraOrbit; viewer.cameraTarget = animal.cameraTarget;
            if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) viewer.jumpCameraToGoal();
          }}>Reset view</button>
        </div>
      </div>
      <div className={styles.notes}>
        <p className={styles.eyebrow}>AUSTRALIAN WILDLIFE</p>
        <h2 id={headingId} className={styles.title}>{animal.name}</h2>
        <p className={styles.scientific}>{animal.scientificName}</p>
        <div className={styles.topics} role="group" aria-label={`${animal.name} topics`}>
          {animal.topics.map((topic) => <button key={topic.id} type="button" aria-pressed={topic.id === selected?.id} aria-controls={factId} onClick={() => selectTopic(topic)}>{topic.label}</button>)}
        </div>
        {selected && <article id={factId} className={styles.fact} aria-live="polite" aria-atomic="true">
          <h3>{selected.title}</h3><p>{selected.body}</p>
          <a href={selected.source} target="_blank" rel="noopener noreferrer">Read the source ↗</a>
        </article>}
        <p className={styles.credit}>{animal.credit}</p>
      </div>
    </section>
  );
}
