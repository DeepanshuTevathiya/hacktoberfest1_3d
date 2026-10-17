import asyncio
import base64
from time import perf_counter
from uuid import uuid4
import httpx
from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from .cache import BlueprintCache
from .config import get_settings
from .pipeline import Pipeline

settings = get_settings(); cache = BlueprintCache(); pipeline = Pipeline(cache, settings.gemini_api_key, settings.gemma_model, settings.gemma_attempt_timeout_seconds)
app = FastAPI(title="Tiny Wonders API")
app.add_middleware(CORSMiddleware, allow_origins=[settings.frontend_origin, "http://localhost:5173", "http://127.0.0.1:5173"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])


@app.get("/api/health")
def health(): return {"status": "ok", "provider": "gemini", "model": settings.gemma_model, "gemini_configured": bool(settings.gemini_api_key)}


@app.get("/api/blueprint/{slug}")
def get_blueprint(slug: str):
    blueprint = pipeline.demo(slug) or cache.get(slug)
    if not blueprint: raise HTTPException(404, detail={"error": {"code": "not_found", "message": "That demo is not available yet."}})
    return {"blueprint": blueprint, "cached": True, "low_confidence": blueprint.confidence < .6}


class PandaExplainRequest(BaseModel):
    object_name: str
    part_name: str
    role: str
    description: str
    fact: str


@app.post("/api/explain")
async def explain_with_panda(request: PandaExplainRequest):
    try:
        explanation = await asyncio.wait_for(
            asyncio.to_thread(pipeline.explain_part, **request.model_dump()),
            timeout=settings.gemma_attempt_timeout_seconds + 10,
        )
        audio_base64 = None
        audio_error = None
        if settings.elevenlabs_api_key:
            try:
                print(f"[panda] creating ElevenLabs audio | voice={settings.elevenlabs_voice_id!r}", flush=True)
                async with httpx.AsyncClient(timeout=25) as client:
                    response = await client.post(
                        f"https://api.elevenlabs.io/v1/text-to-speech/{settings.elevenlabs_voice_id}/stream",
                        params={"output_format": "mp3_22050_32"},
                        headers={"xi-api-key": settings.elevenlabs_api_key, "Content-Type": "application/json"},
                        json={"text": explanation, "model_id": "eleven_flash_v2_5"},
                    )
                    response.raise_for_status()
                audio_base64 = base64.b64encode(response.content).decode("ascii")
                print(f"[panda] ElevenLabs audio ready | bytes={len(response.content)}", flush=True)
            except Exception as audio_exc:
                audio_error = "Panda's voice is unavailable right now."
                print(f"[panda] ElevenLabs failed: {type(audio_exc).__name__}: {audio_exc}", flush=True)
        else:
            audio_error = "Add ELEVENLABS_API_KEY to enable Panda's voice."
        return {"explanation": explanation, "audio_base64": audio_base64, "audio_error": audio_error}
    except Exception as exc:
        print(f"[panda] explanation failed: {type(exc).__name__}: {exc}", flush=True)
        raise HTTPException(503, detail={"error": {"message": "Panda is taking a break. Please try again."}})


@app.post("/api/analyze")
async def analyze(file: UploadFile = File(...), object_name_override: str | None = Form(default=None)):
    request_id = uuid4().hex[:8]
    started_at = perf_counter()
    print(f"[analyze:{request_id}] 1/7 request received | filename={file.filename!r} | type={file.content_type}", flush=True)
    allowed = {"image/jpeg", "image/png", "image/webp"}
    if file.content_type not in allowed:
        print(f"[analyze:{request_id}] rejected: unsupported image type", flush=True)
        raise HTTPException(400, detail={"error": {"code":"invalid_file", "message":"Please choose a JPEG, PNG, or WebP image."}})
    raw = await file.read()
    print(f"[analyze:{request_id}] 2/7 image read | {len(raw) / 1024 / 1024:.2f} MB", flush=True)
    if len(raw) > settings.max_upload_mb * 1024 * 1024:
        print(f"[analyze:{request_id}] rejected: image exceeds {settings.max_upload_mb} MB limit", flush=True)
        raise HTTPException(413, detail={"error": {"code":"file_too_large", "message":f"Photos must be under {settings.max_upload_mb} MB."}})
    try:
        print(f"[analyze:{request_id}] 3/7 starting Gemma analysis | model={settings.gemma_model!r} | object override={object_name_override!r}", flush=True)
        blueprint = await asyncio.wait_for(
            asyncio.to_thread(pipeline.analyze_image, raw, file.content_type, object_name_override),
            timeout=(settings.gemma_attempt_timeout_seconds * 2) + 10,
        )
    except Exception as exc:
        # Never expose API keys or provider internals to the browser; keep the demo usable with a friendly fallback.
        print(f"[analyze:{request_id}] provider failed: {type(exc).__name__}: {exc}. Using local fallback.", flush=True)
        blueprint = pipeline.analyze_offline(object_name_override)
    print(f"[analyze:{request_id}] 6/7 blueprint ready | object={blueprint.object_name!r} | parts={len(blueprint.parts)} | confidence={blueprint.confidence}", flush=True)
    cache.put(blueprint)
    print(f"[analyze:{request_id}] 7/7 response sent | elapsed={perf_counter() - started_at:.1f}s", flush=True)
    return {"blueprint": blueprint, "cached": False, "low_confidence": blueprint.confidence < .6}
