

from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from src.cleaning.detector import analyze_issues


app = FastAPI()

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



