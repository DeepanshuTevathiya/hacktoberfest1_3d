import type { Blueprint } from '../types/blueprint';
import { localDemos } from '../demoBlueprints';
const base = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';
const apiBases = [...new Set(['', base, 'http://127.0.0.1:8001', 'http://localhost:8001'])];
export async function loadDemo(slug:string): Promise<Blueprint> {
  try {
    const r=await fetch(`${base}/api/blueprint/${slug}`);
    if (r.ok) return (await r.json()).blueprint;
  } catch { /* The local demo below keeps the first experience independent of a backend. */ }
  const demo = localDemos[slug];
  if (demo) return demo;
  throw new Error('Demo unavailable');
}
export async function analyze(file:File, name?:string): Promise<Blueprint> {
  let lastError: unknown;
  for (const apiBase of apiBases) {
    try {
      const body = new FormData(); body.append('file', file); if (name) body.append('object_name_override', name);
      const response = await fetch(`${apiBase}/api/analyze`, { method: 'POST', body });
      const payload = await response.json();
      if (!response.ok) throw new Error(payload.detail?.error?.message || 'Could not analyse this photo');
      return payload.blueprint;
    } catch (error) { lastError = error; }
  }
  throw new Error(lastError instanceof Error ? lastError.message : 'Cannot connect to the Tiny Wonders backend. Start it on port 8001.');
}

export type PandaExplanation = { explanation: string; audio_base64: string | null; audio_error: string | null };

export async function explainWithPanda(part: {object_name:string; part_name:string; role:string; description:string; fact:string}): Promise<PandaExplanation> {
  let lastError: unknown;
  for (const apiBase of apiBases) {
    try {
      const response = await fetch(`${apiBase}/api/explain`, {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify(part)});
      const payload = await response.json();
      if (!response.ok) throw new Error(payload.detail?.error?.message || 'Panda could not explain this part');
      return payload;
    } catch (error) { lastError = error; }
  }
  throw new Error(lastError instanceof Error ? lastError.message : 'Cannot connect to the backend.');
}
