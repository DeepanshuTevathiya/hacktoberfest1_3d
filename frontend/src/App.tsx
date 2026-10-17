import { useEffect, useRef, useState } from 'react';
import { analyze, explainWithPanda, loadDemo } from './api/client';
import { useStore } from './store/useStore';
import { Viewer } from './scene/Viewer';
import './demo-highlight.css';

const samples = [['microwave_oven', 'Microwave'], ['television', 'TV']];

function Navigation({ onHome }: { onHome: () => void }) {
  return <header className="site-nav"><button className="wordmark" onClick={onHome}><b>›</b> Tiny Wonders</button><nav><a href="#how-it-works">How it works</a><a href="#demos">Demos</a><button className="nav-action" onClick={onHome}>Explore inside</button></nav></header>;
}

export default function App() {
  const input = useRef<HTMLInputElement>(null);
  const s = useStore();
  const part = s.blueprint?.parts.find(p => p.id === s.selectedPartId);
  const [pandaText, setPandaText] = useState('');
  const [pandaError, setPandaError] = useState('');
  const [askingPanda, setAskingPanda] = useState(false);
  const [pandaAudioUrl, setPandaAudioUrl] = useState('');
  const pandaAudio = useRef<HTMLAudioElement | null>(null);
  useEffect(() => { pandaAudio.current?.pause(); setPandaText(''); setPandaError(''); setPandaAudioUrl(''); }, [part?.id]);

  async function demo(slug: string) { try { s.set({ status: 'loading' }); s.set({ blueprint: await loadDemo(slug), status: 'viewer' }); } catch { s.set({ status: 'error', error: 'Could not load that demo.' }); } }
  async function upload(file?: File) { if (!file) return; try { input.current && (input.current.value = ''); s.set({ status: 'loading', blueprint: undefined, selectedPartId: undefined, hoveredPartId: undefined }); const [blueprint] = await Promise.all([analyze(file), new Promise(resolve => setTimeout(resolve, 180000))]); s.set({ blueprint, status: 'viewer' }); } catch (e) { s.set({ status: 'error', error: e instanceof Error ? e.message : 'Something went wrong' }); } }
  async function askPanda() {
    if (!part || !s.blueprint) return;
    setAskingPanda(true); setPandaText(''); setPandaError('');
    try {
      const result = await explainWithPanda({ object_name: s.blueprint.object_name, part_name: part.name, role: part.role, description: part.hover_text, fact: part.fun_fact });
      setPandaText(result.explanation);
      if (result.audio_base64) {
        pandaAudio.current?.pause();
        const audioUrl = `data:audio/mpeg;base64,${result.audio_base64}`;
        setPandaAudioUrl(audioUrl);
        pandaAudio.current = new Audio(audioUrl);
        await pandaAudio.current.play();
      } else if (result.audio_error) setPandaError(result.audio_error);
    }
    catch (e) { setPandaError(e instanceof Error ? e.message : 'Panda could not answer right now.'); }
    finally { setAskingPanda(false); }
  }

  if (s.status === 'loading') return <main className="center"><Navigation onHome={s.reset}/><div className="panda">✦</div><h1>Peeking inside...</h1><p>Studying your image and building the 3D view. This can take up to 3 minutes.</p></main>;
  if (s.status === 'error') return <main className="center"><Navigation onHome={s.reset}/><h1>Oops!</h1><p>{s.error}</p><button className="nav-action" onClick={s.reset}>Try again</button></main>;
  if (s.status === 'upload') return <main className="upload"><Navigation onHome={s.reset}/><span className="sticker left-sticker">✦ See inside</span><span className="sticker right-sticker">⚡ tiny tech</span><section className="hero"><span className="announcement"><b>NEW</b> Made for curious minds</span><h1><mark>Peek inside</mark> everyday<br/>things you use</h1><p>Turn a photo into a playful 3D map of the tiny parts that make it work.</p><button className="drop" onClick={() => input.current?.click()}><span>↑</span> Upload a photo <small>JPEG, PNG, or WebP</small></button><input ref={input} type="file" accept="image/jpeg,image/png,image/webp" hidden onChange={e => upload(e.target.files?.[0])}/><p className="hint">Your photo is processed in memory and never stored.</p><div className="samples" id="demos"><span>Try a demo:</span>{samples.map(([slug, label]) => <button key={slug} onClick={() => demo(slug)}>{label} →</button>)}</div></section><span className="corner-spark">✦</span></main>;
  return <main className="viewer"><header><button className="brand" onClick={s.reset}>TINY WONDERS</button><span>{s.blueprint?.object_name}</span><button onClick={s.reset}>New photo</button></header><Viewer blueprint={s.blueprint!}/><section className="controls"><label>Explode view <input aria-label="Explode view" type="range" min="0" max="1" step=".01" value={s.explodeValue} onChange={e => s.set({ explodeValue: +e.target.value })}/></label></section>{s.hoveredPartId && <aside className="tooltip">{s.blueprint?.parts.find(p => p.id === s.hoveredPartId)?.name}</aside>}{part && <aside className="panel"><button className="close" onClick={() => s.set({ selectedPartId: undefined })}>×</button><span className="eyebrow">{part.role}</span><h2>{part.name}</h2><p>{part.hover_text}</p><div className="fact">✨ {part.fun_fact}</div>{pandaText && <p className="panda-answer">🐼 {pandaText}</p>}{pandaError && <p className="panda-error">{pandaError}</p>}<button onClick={askPanda} disabled={askingPanda}>{askingPanda ? 'Panda is thinking…' : 'Explain with Panda 🐼'}</button>{pandaAudioUrl && <button onClick={() => pandaAudio.current?.play()}>🔊 Hear Panda again</button>}</aside>}{s.blueprint?.safety_note && <aside className="safety">⚠ {s.blueprint.safety_note}</aside>}</main>;
}
