# AI Data Analyst Agent

This project is an interactive, AI-powered toolkit for automated data cleaning, analysis, and storytelling. Built with Python, FastAPI, and Gradio, it allows users to upload a CSV file and receive intelligent data quality assessments, cleaning suggestions, narrative summaries, and engage in a conversation with a data analyst chatbot.

## Features


## Tech Stack


## Setup and Installation

1.  **Clone the repository:**
  ```bash
  git clone https://github.com/Pandidharan22/AI-Data-Analyst-Agent.git ai-data-analyst-agent
  cd ai-data-analyst-agent
  ```

2.  **Create a virtual environment and install dependencies:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    pip install -r requirements.txt
    ```

3.  **Set up your Hugging Face API Token:**
    - Create a `.env` file in the root of the project.
    - Add your Hugging Face token to the file. This is required to communicate with the LLM.
      ```
      HF_TOKEN="your_hugging_face_api_token_here"
      ```

4.  **Run the application:**
    - Start the FastAPI backend:
      ```bash
  python -m uvicorn src.api.main:app --reload
      ```
    - In a separate terminal, run the Gradio frontend:
      ```bash
  python gradio_app.py
      ```

5.  **Open the application:**
    - Navigate to the local URL provided by Gradio (usually `http://127.0.0.1:7860`) in your web browser.

## Deploying to Hugging Face Spaces

This application is designed to be easily deployed on Hugging Face Spaces.

1.  **Create a new Space:** Go to [Hugging Face Spaces](https://huggingface.co/new-space) and create a new "Gradio SDK" space.
2.  **Upload your files:** Upload all the project files (`.py`, `requirements.txt`, `.env` etc.) to your Space repository.
3.  **Add your HF_TOKEN to Secrets:** In your Space settings, go to "Secrets" and add your `HF_TOKEN`. This is crucial for the application to authenticate with the Hugging Face Inference API.
4.  **Set the Application File:** Ensure the `app.py` or `gradio_app.py` is set as the main application file in the Space configuration.
5.  The Space will automatically install the dependencies from `requirements.txt` and run the application.


## License

MIT License
# AI Data Analyst Agent

Converse with your dataset. This app pairs a Gradio UI with a FastAPI backend and a Hugging Face LLM to:
- detect issues in CSVs (missing values, duplicates, outliers, types, etc.)
- generate Markdown-formatted cleaning playbooks with runnable Python code
- write human-friendly data stories
- suggest and render visualizations with executable code
- chat like a data analyst to answer questions and produce code on demand

Built for clarity, reproducibility, and cloud-readiness.

## Table of Contents
- Overview
- Architecture & Workflow
- Features
- Requirements
- Setup (Windows/PowerShell friendly)
- Running Locally
- Using the App (Step-by-step)
- Configuration (Models, tokens, URLs)
- API Reference
- Deployment Options (incl. Hugging Face Spaces)
- Troubleshooting & FAQ
- Roadmap
- License

## Overview
AI Data Analyst Agent is a full-stack data analysis assistant. Upload a CSV, click to detect issues, get a structured cleaning manual (with fenced Python code), have the AI write a narrative story, ask for visualization code and see the plot rendered, and converse with a context-aware data analyst chatbot.

## Architecture & Workflow

High level:

1) Gradio UI (`gradio_app.py`)
- Upload CSV and trigger actions via buttons
- Renders cleaning suggestions and data story as Markdown (scrollable)
- Executes AI-generated plotting code to display charts
- Chatbot interface for conversational analysis

2) FastAPI backend (`src/api/main.py`)
- Endpoints: `/ping`, `/analyze-csv`, `/suggest-cleaning`, `/generate-story`, `/suggest-visualization`, `/chat`
- Reads CSV, analyzes issues, calls LLM functions

3) LLM client (`src/storytelling/hf_client.py`)
- Uses `huggingface_hub.InferenceClient` with provider "novita" and model `meta-llama/Meta-Llama-3-8B-Instruct`
- Requires `HF_TOKEN` in environment or `.env`
- Returns Markdown for cleaning suggestions (with fenced code)

4) Data & Viz
- Pandas/NumPy for data handling
- AI returns plotting code (matplotlib/seaborn); UI executes code to produce a matplotlib figure

Data flow:
- UI -> FastAPI via `httpx` -> LLM -> back to UI
- Visualization code is executed in a sandboxed local scope with `df` defined

## Features
- Data issue detection: missing values, duplicates, dtype issues, outliers, high cardinality, constants, imbalanced categoricals, etc.
- AI cleaning suggestions: Markdown manual with headings and fenced `python` blocks.
- AI data storytelling: formatted Markdown story for non-technical stakeholders.
- AI visualization suggestions: single-plot Python code; executed to display the chart.
- Conversational chatbot: context-aware Q&A about the dataset; can emit plotting code.
- Clean UI: scrollable Markdown for long outputs; copy-friendly formatting.

## Requirements
- Python 3.10+ (3.11/3.12/3.13 supported)
- Packages (from `requirements.txt`):
  - pandas, numpy, scikit-learn, matplotlib, seaborn, plotly
  - gradio, fastapi, uvicorn, httpx, requests
  - huggingface_hub, python-dotenv, pytest
- A Hugging Face API token with access to the chosen model (`HF_TOKEN`)

## Setup (Windows/PowerShell)

1) Clone
```powershell
git clone https://github.com/Pandidharan22/AI-Data-Analyst-Agent.git ai-data-analyst-agent
cd ai-data-analyst-agent
```

2) Virtual env & install
```powershell
python -m venv venv
venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

3) Configure HF token
Create a `.env` in the project root:
```
HF_TOKEN=your_hugging_face_api_token_here
```

## Running Locally

Use two terminals.

Terminal A — start FastAPI
```powershell
python -m uvicorn src.api.main:app --reload
```

Terminal B — start the Gradio UI
```powershell
python gradio_app.py
```

Open the Gradio URL shown (usually http://127.0.0.1:7860).

## Using the App (Step-by-step)
1) Upload CSV (left top)
2) Click “Analyze Data Issues”
   - See a quick summary of detected issues
3) Click “Get AI Cleaning Suggestions (Meta Llama 3)”
   - Receive a Markdown manual:
     - `### Issue N: …`
     - `**Why this needs to be fixed:** …`
     - ```python fenced code ```
4) Click “Generate Data Story”
   - Read a structured narrative based on head() and describe()
5) Click “Suggest a Visualization”
   - Code is returned and executed to render a matplotlib figure
6) Use “Chat with your Data Analyst”
   - Ask questions; request plots; get code inline

## Configuration

Model & LLM
- Default model: `meta-llama/Meta-Llama-3-8B-Instruct`
- Provider: `novita` (via `InferenceClient`)
- Tuning: temperature, max_tokens per function (see `src/storytelling/hf_client.py`)

Environment
- HF token required: `HF_TOKEN` or `HF_API_KEY`

Frontend/Backend URLs
- `gradio_app.py` calls FastAPI at `http://127.0.0.1:8000`

UI Styling
- Scrollable containers: `.scroll-suggestions`, `.scroll-story` defined in `gradio_app.py`
- Adjust height via CSS if desired

## API Reference (FastAPI)

Base URL: `http://127.0.0.1:8000`

- GET `/ping`
  - Response: `{ "message": "API is running" }`

- POST `/analyze-csv` (multipart form)
  - Body: `file` (CSV)
  - Response: `{ issues: { ... }, columns: [ ... ] }`

- POST `/suggest-cleaning`
  - Body: `{ issues: <object>, columns: <array> }`
  - Response: `{ suggestions: <markdown_string> }`

- POST `/generate-story`
  - Body: `{ df_head: <string>, df_describe: <string>, columns: <array> }`
  - Response: `{ story: <markdown_or_text> }`

- POST `/suggest-visualization`
  - Body: `{ columns: <array>, df_head: <string> }`
  - Response: `{ visualization_code: <python_code_string> }`

- POST `/chat`
  - Body: `{ message: <string>, history: <[[user,assistant],...]>, columns: <array>, df_head: <string> }`
  - Response: `{ response: <string_markdown_or_text> }`

## Deployment Options

Option A — Self-host (recommended for production)
- Run FastAPI on a server (VM/container)
- Expose it over HTTPS (e.g., behind Nginx)
- Update `gradio_app.py` API base URLs to your public backend URL

Option B — Hugging Face Spaces (single runtime)
- Spaces run one process; you’ll need both UI and API in one app.
- Easiest path: host only the Gradio UI and call the Hugging Face Inference API directly (already done for LLM), but your FastAPI endpoints must also be available. You can:
  - Merge backend logic into Gradio callbacks, or
  - Start uvicorn inside the Space at launch (advanced), then call `http://localhost:8000`
- Add `HF_TOKEN` in Spaces Secrets and keep `requirements.txt` up to date.

## Troubleshooting & FAQ

Q: I get “Hugging Face token not found”.
- Ensure `.env` exists with `HF_TOKEN=` and the token is valid.

Q: Visualization code tries to `pd.read_csv()` and fails.
- The prompt forbids it; if it appears, just remove that line. The UI provides `df` already.

Q: OneDrive blocks renames/moves.
- Pause OneDrive syncing temporarily and close VS Code/Python before renaming. Consider working outside OneDrive (e.g., `C:\Projects`).

Q: CORS or 127.0.0.1 unreachable on cloud.
- For remote deployments, update the API base URL to a public endpoint and configure CORS in FastAPI accordingly.

Q: Large CSVs are slow.
- Consider sampling before analysis; extend the backend to stream or chunk if needed.

## Roadmap
- Export cleaning playbook to file (Markdown/HTML)
- Add “Copy code” buttons per block
- Merge backend into a single-process app for easy Spaces deploy
- Add auth and request quotas

## License
MIT License
