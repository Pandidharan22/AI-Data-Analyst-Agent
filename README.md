# AI Data Analyst Agent

[![Live Demo on Hugging Face Spaces](https://img.shields.io/badge/Live%20Demo-Hugging%20Face%20Spaces-blue?logo=huggingface)](https://huggingface.co/spaces/Pandidharan22/AI-Data-Analyst-Agent)

---
title: AI Data Analyst Agent
emoji: 📊
colorFrom: indigo
colorTo: purple
sdk: gradio
sdk_version: "4.29.0"
app_file: gradio_app.py
pinned: false
---

# AI Data Analyst Agent

Converse with your dataset. Upload a CSV, detect data issues, get a Markdown cleaning playbook with runnable code, generate a narrative data story, request visualizations (auto-rendered), and chat with a context-aware data analyst bot.

Built with FastAPI + Gradio, powered by a Hugging Face LLM.

## Highlights
- Data issue detection (missing values, duplicates, types, outliers, etc.)
- AI cleaning suggestions as Markdown with fenced Python code
- AI data storytelling for stakeholders
- AI visualization suggestions; code is executed to render charts
- Conversational chatbot with dataset context

## Architecture (short)
- Gradio UI (`gradio_app.py`): upload CSV, show Markdown, render charts, chat
- FastAPI (`src/api/main.py`): endpoints for analysis, suggestions, story, viz, chat
- LLM client (`src/storytelling/hf_client.py`): `InferenceClient` (provider: novita, model: meta-llama/Meta-Llama-3-8B-Instruct)
- Pandas/NumPy + matplotlib/seaborn for data and plots

## Requirements
- Python 3.10+
- `requirements.txt` installs: pandas, numpy, scikit-learn, matplotlib, seaborn, plotly, gradio, fastapi, uvicorn, httpx, requests, huggingface_hub, python-dotenv, pytest
- Hugging Face API token in env (`HF_TOKEN` or `HF_API_KEY`)

## Quickstart (Windows / PowerShell)
1) Clone
```powershell
git clone https://github.com/Pandidharan22/AI-Data-Analyst-Agent.git ai-data-analyst-agent
cd ai-data-analyst-agent
```

2) Create venv and install
```powershell
python -m venv venv
venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

3) Configure token (.env in project root)
```
HF_TOKEN=your_hugging_face_api_token_here
```

4) Run (two terminals)
- Terminal A — FastAPI
```powershell
python -m uvicorn src.api.main:app --reload
```
- Terminal B — Gradio UI
```powershell
python gradio_app.py
```
Open the URL shown by Gradio (usually http://127.0.0.1:7860).

## Using the app
1) Upload CSV
2) Analyze Data Issues → get quick diagnostics
3) Get AI Cleaning Suggestions → Markdown manual with fenced Python blocks
4) Generate Data Story → narrative summary
5) Suggest a Visualization → code executes and renders a chart
6) Chat with your Data Analyst → ask questions or request code

## Feature screenshots

Below are screenshots of the five core features in order:

1) Analyze Data Issues

![Analyze Data Issues](docs/Screenshot%202025-09-14%20204905.png)

2) AI Cleaning Suggestions

![AI Cleaning Suggestions](docs/Screenshot%202025-09-14%20204941.png)

3) AI Data Story

![AI Data Story](docs/Screenshot%202025-09-14%20205020.png)

4) AI Visualization Suggestion

![AI Visualization Suggestion](docs/Screenshot%202025-09-14%20205050.png)

5) Data Analyst Chatbot

![Data Analyst Chatbot](docs/Screenshot%202025-09-14%20205233.png)

## Configuration
- Model: `meta-llama/Meta-Llama-3-8B-Instruct` (provider: `novita`)
- Token: `HF_TOKEN` (or `HF_API_KEY`) required in env/.env
- UI connects to FastAPI at `http://127.0.0.1:8000`

## API (FastAPI)
Base: `http://127.0.0.1:8000`
- GET `/ping`
- POST `/analyze-csv` (form: file)
- POST `/suggest-cleaning` (issues, columns)
- POST `/generate-story` (df_head, df_describe, columns)
- POST `/suggest-visualization` (columns, df_head)
- POST `/chat` (message, history, columns, df_head)

## Deploying to Hugging Face Spaces
Spaces run a single process. Simplest path is to keep Gradio as the entry app and ensure LLM calls use the Hugging Face Inference API (already done). If you also need FastAPI endpoints, either:
- Inline the backend logic in Gradio callbacks, or
- Start uvicorn at launch and call `http://localhost:8000` from the UI (advanced)

Add `HF_TOKEN` as a Space Secret. Keep `requirements.txt` up to date. Set the app file to `gradio_app.py`.

## Troubleshooting
- “Hugging Face token not found” → ensure `.env` has `HF_TOKEN=` and the token is valid
- Viz code tries `pd.read_csv()` → remove it; the UI provides a `df` already
- OneDrive path locks/renames → pause syncing or develop outside OneDrive (e.g., `C:\Projects`)
- CORS / localhost issues on remote → host FastAPI publicly and configure CORS; update UI base URL

## License
MIT License
