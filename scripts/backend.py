# For Backend we are using FastAPI framework

import os
import sys
import pandas as pd
import io
import aiohttp
from fastapi import FastAPI, File, UploadFile, HTTPException, Query
from sqlalchemy import create_engine
from pydantic import BaseModel
import requests


# Ensure the scripts folder is in Python's path
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from scripts.ai_agent import AIAgent
from scripts.data_cleaning import DataCleaning

app = FastAPI()

# Initialize AI agent and rule-based data cleaner
ai_agent = AIAgent()
cleaner = DataCleaning()

# ------------------CSV/Excel Data cleaning endpoint------------------
@app.post("/clean-data/")
async def clean_data(file: UploadFile = File(...)):
    """Receives file from UI, cleans it using rule-based & AI methods, and returns cleaned JSON."""
    try:
        contents = await file.read()
        file_extension = file.filename.split('.')[-1]
        
        # Load file into DataFrame
        if file_extension == 'csv':
            df = pd.read_csv(io.StringIO(contents.decode('utf-8')))
        elif file_extension in ['xls', 'xlsx']:
            df = pd.read_excel(io.BytesIO(contents))
        else:
            raise HTTPException(status_code=400, detail="Unsupported file type, use CSV or Excel.")

        # Step 1: Rule-Based Cleaning
        df_cleaned = cleaner.clean_data(df)

        # Step 2: AI-Powered Cleaning
        df_ai_cleaned = ai_agent.process_data(df_cleaned)
        
        # Ensure AI Output is DataFrame
        if isinstance(df_ai_cleaned, str):
            from io import StringIO
            df_ai_cleaned = pd.read_csv(StringIO(df_ai_cleaned))

        return {"cleaned_data": df_ai_cleaned.to_dict(orient='records')}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error Processing File: {e}")