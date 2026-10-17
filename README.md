# Tiny Wonders

Tiny Wonders is an interactive 3D learning MVP. Upload a photo or open a TV/microwave demo to explore its parts and learn how they work.

Website: [Tiny Wonders](https://frontend-amber-six-70.vercel.app/)

## Requirements

- Python 3.11+
- Node.js 18+
- A Gemini API key with access to the configured Gemma model

## Backend

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
```

Add your `GEMINI_API_KEY` to `backend/.env`, then start the API:

```powershell
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8001
```

The health check is available at `http://127.0.0.1:8001/api/health`.

## Frontend

Open a second terminal:

```powershell
cd frontend
npm install
npm run dev
```

Open the URL printed by Vite (normally `http://localhost:5173`). The frontend tries the local backend at port `8001` automatically.

## MVP features

- Interactive exploded 3D demos for a microwave and TV
- Image upload and visual object identification through Gemma
- Layer details, fun facts, and safety notes
- Backend logging checkpoints for debugging API requests

## Notes

- Keep API keys only in `backend/.env`; never commit that file.
- If the model provider is slow or unavailable, the backend returns a local fallback blueprint so the app remains usable.
