# 🚀 The Standup & PR Polish Agent

> Turn raw, messy thoughts into crisp, confident daily standups and high-impact Pull Request descriptions in seconds.

[![Built with FastAPI](https://img.shields.io/badge/FastAPI-005571?style=flat&logo=fastapi)](https://fastapi.tiangolo.com)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat&logo=streamlit&logoColor=white)](https://streamlit.io)
[![Gemini 2.5 Flash](https://img.shields.io/badge/Google%20Gemini-2.5%20Flash-4285F4?style=flat&logo=google)](https://aistudio.google.com/)

---

## 💡 The Problem
Interns and junior developers often suffer from imposter syndrome when communicating in professional engineering channels. Drafting daily standup updates or GitHub PR descriptions can take 30–45 minutes due to anxiety about tone, phrasing, and structure.

## ✨ The Solution
An AI-powered "Senior Developer" partner that takes raw, unfiltered notes and transforms them into:
1. **Daily Standup Updates:** Strictly structured into `Yesterday`, `Today`, and `Blockers` with confident, non-apologetic phrasing.
2. **GitHub Pull Request Descriptions:** Structured into `Summary of Changes`, `Impact / Key Changes`, and `Testing Steps`.

---

## 🛠️ Architecture

```
hactoberP1/
├── backend/                  # FastAPI REST Service
│   ├── app/
│   │   ├── main.py          # CORS, health check & /api/polish
│   │   ├── schemas.py       # Pydantic validation models
│   │   ├── prompts.py       # Senior Dev persona prompts
│   │   └── services.py      # Google GenAI (gemini-2.5-flash) integration
│   ├── test_main.py         # Pytest test suite
│   ├── Procfile             # Render/Railway deployment
│   └── requirements.txt
├── frontend/                 # Streamlit Web UI
│   ├── app.py               # Reactive UI with Tabs & Diff view
│   ├── api_client.py        # API client for FastAPI
│   ├── styles.py            # Glassmorphic CSS & demo samples
│   └── requirements.txt
└── PLANNER.md               # Master phase planner
```

---

## 🚀 Quickstart Guide

### 1. Prerequisites
- Python 3.10+
- A Google Gemini API Key ([Get one free from Google AI Studio](https://aistudio.google.com/))

### 2. Setup Backend
```bash
# In project root
python -m venv venv
.\venv\Scripts\activate   # On Windows (or source venv/bin/activate on Mac/Linux)

pip install -r backend/requirements.txt
```

Create `backend/.env`:
```env
GEMINI_API_KEY=your_gemini_api_key_here
PORT=8000
```

Run FastAPI:
```bash
$env:PYTHONPATH="backend"
uvicorn app.main:app --reload --port 8000
```
Swagger UI will be accessible at: `http://localhost:8000/docs`

### 3. Setup Frontend
```bash
pip install -r frontend/requirements.txt
```

Create `frontend/.env`:
```env
BACKEND_API_URL=http://localhost:8000
```

Run Streamlit:
```bash
streamlit run frontend/app.py
```
Open `http://localhost:8501` in your browser!

---

## 🧪 Running Tests
```bash
$env:PYTHONPATH="backend"
pytest backend/test_main.py
```
