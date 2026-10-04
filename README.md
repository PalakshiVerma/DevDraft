# 🚀 The Standup & PR Polish Agent

> Turn raw, messy developer notes into crisp, confident daily standups and high-impact Pull Request descriptions in seconds — powered by open-weight LLMs.

[![Built with FastAPI](https://img.shields.io/badge/FastAPI-005571?style=flat&logo=fastapi)](https://fastapi.tiangolo.com)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat&logo=streamlit&logoColor=white)](https://streamlit.io)
[![Powered by Llama](https://img.shields.io/badge/Llama%203.1-open--weight-blueviolet?style=flat&logo=meta)](https://groq.com)
[![OpenAI-compatible](https://img.shields.io/badge/OpenAI--compatible-API-412991?style=flat&logo=openai)](https://platform.openai.com/docs/api-reference)

---

## 💡 The Problem

Interns and junior developers often suffer from imposter syndrome when communicating in professional engineering channels. Drafting a daily standup or a GitHub PR description can take 30–45 minutes — not because the work is hard, but because getting the tone and structure right causes anxiety.

## ✨ The Solution

An AI-powered "Senior Developer" partner that takes raw, unfiltered notes and transforms them into:

1. **Daily Standup** — structured into `Completed`, `Planned`, and `Blockers / Risks` with confident, non-apologetic phrasing.
2. **Pull Request Description** — structured into `Title`, `Summary`, `Why`, `Changes`, `How to test`, and a `Checklist`.
3. **Analyze** — a free-form mode that extracts insights, risks, and action items from any blob of developer notes.

---

## 🔓 Why Open Models?

- **Swap models with one env var.** Point `LLM_MODEL` at any model on Groq, OpenRouter, Hugging Face, or your local Ollama — no code changes.
- **Runs fully local.** Set `LLM_BASE_URL=http://localhost:11434/v1` and your notes never leave your machine.
- **No vendor lock-in.** The backend speaks the OpenAI-compatible chat completions API, which every major open-model provider supports.

---

## 🛠️ Architecture

```
hactoberP1/
├── backend/                  # FastAPI REST service
│   ├── app/
│   │   ├── main.py          # CORS, health check & /api/polish
│   │   ├── schemas.py       # Pydantic request / response models
│   │   ├── prompts.py       # System prompts for each mode
│   │   └── services.py      # OpenAI-compatible async LLM client
│   ├── test_main.py         # Pytest async test suite
│   ├── Procfile             # Render deployment entry point
│   └── requirements.txt
├── frontend/                 # Streamlit web UI
│   ├── app.py               # Reactive UI with tabs & diff view
│   ├── api_client.py        # HTTP client for the FastAPI backend
│   ├── styles.py            # Custom CSS
│   └── requirements.txt
├── PLANNER.md               # Master phase planner
└── README.md
```

### Data flow

```
User → Streamlit → POST /api/polish → AsyncOpenAI client
     ← polished_text ←────────────── Groq / OpenRouter / Ollama
```

---

## ⚙️ Environment Variables

All three variables live in `backend/.env`. No code changes are needed to switch providers.

| Variable | Default | Description |
|---|---|---|
| `LLM_BASE_URL` | `https://api.groq.com/openai/v1` | Base URL of any OpenAI-compatible endpoint |
| `LLM_API_KEY` | *(required)* | API key for the chosen provider |
| `LLM_MODEL` | `llama-3.1-8b-instant` | Model ID as recognised by the provider |
| `LLM_FALLBACK_MODEL` | *(optional)* | Tried automatically if the primary model fails all retries |
| `PORT` | `8000` | Port the FastAPI server listens on |

---

## 🚀 Quickstart (Local)

### 1. Prerequisites

- Python 3.10+
- A Groq API key — free at [console.groq.com](https://console.groq.com) (no credit card needed)

### 2. Clone & create a virtual environment

```bash
git clone https://github.com/your-username/hactoberP1.git
cd hactoberP1
python -m venv venv

# Windows
.\venv\Scripts\activate
# macOS / Linux
source venv/bin/activate
```

### 3. Backend

```bash
pip install -r backend/requirements.txt
```

Copy the example env file and fill in your key:

```bash
cp backend/.env.example backend/.env
# Open backend/.env and set LLM_API_KEY=<your_groq_key>
```

Start the API:

```bash
# From the project root
cd backend
uvicorn app.main:app --reload --port 8000
```

Swagger docs: [http://localhost:8000/docs](http://localhost:8000/docs)

### 4. Frontend

```bash
pip install -r frontend/requirements.txt
```

```bash
cd frontend
streamlit run app.py
```

Open [http://localhost:8501](http://localhost:8501).

---

## 🦙 Local Mode with Ollama (fully offline, notes never leave your machine)

1. Install [Ollama](https://ollama.com) and pull a model:

```bash
ollama pull llama3.1
```

2. Set these vars in `backend/.env`:

```env
LLM_BASE_URL=http://localhost:11434/v1
LLM_API_KEY=ollama
LLM_MODEL=llama3.1
```

3. Start Ollama, then start the backend as normal. No internet connection required.

---

## 🌐 Deployment

### Backend → Render (free tier)

1. Push the repo to GitHub.
2. Create a new **Web Service** on [render.com](https://render.com), point it at your repo.
3. Set **Root Directory** to `backend`.
4. Render auto-detects the `Procfile`:
   ```
   web: uvicorn app.main:app --host 0.0.0.0 --port $PORT
   ```
5. Add environment variables in the Render dashboard:
   - `LLM_API_KEY` — your Groq key
   - `LLM_BASE_URL` — `https://api.groq.com/openai/v1`
   - `LLM_MODEL` — `llama-3.1-8b-instant`

> **⚠️ Free tier cold start:** Render spins down free services after ~15 minutes of inactivity. The first request after idle may take 30–60 seconds to respond while the container wakes up. Subsequent requests are fast.

### Frontend → Streamlit Community Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io) and connect your GitHub repo.
2. Set **Main file path** to `frontend/app.py`.
3. Add a secret in the app settings:
   ```
   BACKEND_API_URL=https://your-render-service.onrender.com
   ```
4. Deploy — Streamlit Community Cloud handles the rest.

---

## 🧪 Running Tests

```bash
cd backend
pytest test_main.py -v
```

---

## 📁 .env files

Neither `.env` file is committed (both are in `.gitignore`). Use the provided `.env.example` files as templates:

- `backend/.env.example` — LLM provider config
- `frontend/.env.example` — backend URL for the Streamlit client

---

## 📄 License

[MIT](LICENSE)
