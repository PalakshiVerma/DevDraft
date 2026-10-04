# DevDraft: The Standup & PR Polish Agent

[![Hacktoberfest 2026](https://img.shields.io/badge/Hacktoberfest-2026-blueviolet.svg)](https://hacktoberfest.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Turn raw, messy developer notes into crisp, confident daily standups and high-impact Pull Request descriptions in seconds — powered by open-weight LLMs.**

**Live Demo:** [https://devdraft.onrender.com/](https://devdraft.onrender.com/)

---

## The Problem

Interns and junior developers often experience imposter syndrome when communicating in professional engineering channels. Drafting a daily standup update or a GitHub Pull Request description can take 30–45 minutes. The primary bottleneck is not the engineering work itself, but the anxiety associated with achieving the appropriate tone, structure, and technical phrasing.

## The Solution

DevDraft serves as an AI-powered partner designed to function like an experienced senior developer. It accepts raw, unstructured notes and transforms them into clear, professional, and ready-to-publish updates.

* **Daily Standup:** Converts unstructured notes into *Completed*, *Planned*, and *Blockers / Risks* sections using confident, objective language.
* **Pull Request Description:** Formats code summaries and informal notes into a standardized PR template: *Title*, *Summary*, *Why*, *Changes*, *How to Test*, and a *Checklist*.
* **Analyze Mode:** A free-form utility that extracts key insights, technical risks, and action items from any unformatted block of developer notes.

---

## Architecture

```text
hactoberP1/
├── backend/                  # FastAPI REST service
│   ├── app/
│   │   ├── main.py           # CORS, health check & /api/polish
│   │   ├── schemas.py        # Pydantic request / response models
│   │   ├── prompts.py        # System prompts for each mode
│   │   └── services.py       # OpenAI-compatible async LLM client
│   ├── test_main.py          # Pytest async test suite
│   ├── Procfile              # Render deployment entry point
│   └── requirements.txt
├── frontend/                 # Streamlit web UI
│   ├── app.py                # Reactive UI with tabs & diff view
│   ├── api_client.py         # HTTP client for the FastAPI backend
│   ├── styles.py             # Custom CSS
│   └── requirements.txt
├── PLANNER.md                # Master phase planner
└── README.md



```
### Data flow

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


## 📄 License

[MIT](LICENSE)
