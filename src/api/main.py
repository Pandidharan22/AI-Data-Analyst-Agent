from fastapi import FastAPI, UploadFile, File, Body
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from src.cleaning.detector import analyze_issues
from src.storytelling.hf_client import (
    get_cleaning_suggestions_hf,
    get_data_story_hf,
    get_visualization_suggestion_hf,
    get_chat_response_hf,
)

app = FastAPI(title="AI Data Analyst Agent")

# Allow CORS for local Gradio UI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/ping")
def ping():
    return {"message": "API is running"}

# Data cleaning: upload and analyze CSV
@app.post("/analyze-csv")
async def analyze_csv(file: UploadFile = File(...)):
    df = pd.read_csv(file.file)
    issues = analyze_issues(df)
    return {"issues": issues, "columns": list(df.columns)}

# Hugging Face-powered cleaning suggestions
@app.post("/suggest-cleaning")
async def suggest_cleaning(
    issues: dict = Body(...),
    columns: list = Body(...)
):
    suggestions_md = get_cleaning_suggestions_hf(issues, columns)
    return {"suggestions": suggestions_md}

@app.post("/generate-story")
async def generate_story(
    df_head: str = Body(...),
    df_describe: str = Body(...),
    columns: list = Body(...)
):
    """
    Receives dataframe summaries and generates a data story.
    """
    story = get_data_story_hf(df_head, df_describe, columns)
    return {"story": story}

@app.post("/suggest-visualization")
async def suggest_visualization(
    columns: list = Body(...),
    df_head: str = Body(...)
):
    """
    Receives dataframe info and generates a visualization suggestion.
    """
    code = get_visualization_suggestion_hf(columns, df_head)
    return {"visualization_code": code}

@app.post("/chat")
async def chat(
    message: str = Body(...),
    history: list = Body(...),
    columns: list = Body(...),
    df_head: str = Body(...)
):
    """
    Handles chatbot conversation.
    """
    response = get_chat_response_hf(message, history, columns, df_head)
    return {"response": response}

