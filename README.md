# AI-Powered Data Storyteller & Cleaner

# AI Data Storyteller & Cleaner

This project is an interactive, AI-powered toolkit for automated data cleaning, analysis, and storytelling. Built with Python, FastAPI, and Gradio, it allows users to upload a CSV file and receive intelligent data quality assessments, cleaning suggestions, and narrative summaries.

## Features

- **Automated Data Issue Detection:** Upload a CSV and instantly get a report on common data quality issues like:
  - Missing Values
  - Duplicate Rows
  - Outliers
  - Data Type Inconsistencies
- **AI-Powered Cleaning Suggestions:** Leveraging the power of Meta's Llama 3 model, the tool provides concrete, actionable Python code snippets to fix the detected issues.
- **AI Data Storytelling:** Generates a high-level narrative summary of the dataset, explaining key insights, trends, and patterns in plain English.
- **AI Visualization Suggestions:** Recommends and generates relevant data visualizations (e.g., histograms, scatter plots) complete with the Python code to create them.
- **Interactive UI:** A simple, user-friendly web interface built with Gradio allows for easy file uploads and interaction.
- **FastAPI Backend:** A robust backend powered by FastAPI handles all the data processing and AI interactions.

## Tech Stack

- **Backend:** FastAPI, Uvicorn
- **Frontend:** Gradio
- **Data Handling:** Pandas, NumPy
- **AI/LLM:** Hugging Face InferenceClient (running Meta Llama 3)
- **Plotting:** Matplotlib, Seaborn

## Setup and Installation

1.  **Clone the repository:**
    ```bash
    git clone <your-repo-url>
    cd ai-data-storyteller
    ```

2.  **Create a virtual environment and install dependencies:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    pip install -r requirements.txt
    ```

3.  **Set up your Hugging Face API Token:**
    - Create a `.env` file in the root of the project.
    - Add your Hugging Face token to the file:
      ```
      HF_TOKEN="your_hugging_face_api_token_here"
      ```

4.  **Run the application:**
    - Start the FastAPI backend:
      ```bash
      uvicorn src.api.main:app --reload
      ```
    - In a separate terminal, run the Gradio frontend:
      ```bash
      python gradio_app.py
      ```

5.  **Open the application:**
    - Navigate to the local URL provided by Gradio (usually `http://127.0.0.1:7860`) in your web browser.


## Project Overview

**AI-Powered Data Storyteller & Cleaner** is designed to help data scientists, analysts, and business users:
- Detect and resolve data quality issues automatically
- Get AI-powered suggestions for cleaning and analysis
- Generate interactive EDA reports and visualizations
- Receive business-friendly narratives and recommendations
- Export reusable cleaning and analysis scripts

---

## Features (Work in Progress)

### 1. Intelligent Data Cleaning Module (Completed)

**Automated Data Issue Detection:**
- Upload a CSV file and instantly receive a comprehensive report of data quality issues, including:
  - Missing values (per column)
  - Duplicate rows
  - Data type inconsistencies (mixed types in columns)
  - Outliers (numeric columns, IQR method)
  - Constant columns (zero variance)
  - High cardinality columns
  - Columns with a single unique value
  - Mixed data types in object columns
  - Columns with high percentage of missing values
  - Highly imbalanced categorical columns
  - All-zero columns
  - All-same-string columns
  - Potential date/time parsing issues

**Interactive Gradio UI:**
- Upload your dataset and view a detailed, human-readable summary of all detected issues.
- Designed for rapid feedback and easy review.

**Backend:**
- FastAPI endpoint `/analyze-csv` processes uploaded CSVs and returns a structured JSON report of all detected issues.
- Modular Python code for easy extension and testing.

---

### Upcoming Features
- GenAI-powered cleaning suggestions (Ollama LLM)
- Interactive approval/modification of cleaning steps
- Export cleaning steps as Python scripts
- Automated EDA and visualization
- AI-generated narratives and business recommendations
- CLI and notebook integration
- RESTful API for integration

---

## Ollama Integration (Coming Soon)

This project will use a local Ollama LLM for GenAI-powered data cleaning suggestions and narratives. Ensure you have Ollama installed and running on your machine. See [Ollama's official site](https://ollama.com/) for setup instructions. No cloud API keys required—your data stays local!

---

## Quickstart

1. Start the FastAPI backend:
  ```
  C:/Python313/python.exe -m uvicorn src.api.main:app --reload
  ```
2. Start the Gradio frontend:
  ```
  C:/Python313/python.exe gradio_app.py
  ```
3. Open the Gradio UI in your browser and upload a CSV to analyze data issues.

---

## License

MIT License
