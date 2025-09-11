# AI-Powered Data Storyteller & Cleaner

An open-source toolkit that combines automated data cleaning, AI-generated insights, and storytelling for data science workflows. Built with Python, FastAPI, and Gradio, this project aims to accelerate and simplify the process of preparing, analyzing, and presenting data.

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
