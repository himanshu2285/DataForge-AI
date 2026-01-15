# This script will call all necessary backend functions to run the FastAPI server.

from data_ingestions import DataIngestion
from data_cleaning import DataCleaning
from ai_agent import AIAgent

# Database Configuration

DB_USER = "postgres"
DB_PASSWORD = "Admin"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "demodb"

DB_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


# Initialize all these component (Data Ingestion, Cleaning, and AI Agent)
ingestion = DataIngestion(db_url=DB_URL)
cleaner = DataCleaning()
ai_agent = AIAgent()

## ------------- Load and clean csv data -------------
df_csv = ingestion.load_csv("sample_data.csv")
if df_csv is not None:
    print("\n Cleaning CSV Data...")
    df_csv = cleaner.clean_data(df_csv)
    df_csv = ai_agent.process_data(df_csv)
    print("\n✅ AI-Cleaned CSV Data:\n", df_csv)
    

## ------------- Load and clean excel data -------------
df_excel = ingestion.load_excel("sample_data.xlsx", sheet_name="Sheet1")
if df_excel is not None:
    print("\n Cleaning Excel Data...")
    df_excel = cleaner.clean_data(df_excel)
    df_excel = ai_agent.process_data(df_excel)
    print("\n✅ AI-Cleaned Excel Data:\n", df_excel)


## ------------- Load and clean Database data -------------
df_db = ingestion.load_data_from_db("SELECT * FROM customers;")
if df_db is not None:
    print("\n Cleaning Database Data...")
    df_db = cleaner.clean_data(df_db)
    df_db = ai_agent.process_data(df_db)
    print("\n✅ AI-Cleaned Database Data:\n", df_db)

## ------------- Fetch and clean API data -------------
API_URL = "https://jsonplaceholder.typicode.com/posts"
df_api = ingestion.fetch_from_api(API_URL)

if df_api is not None:
    print("\n Cleaning API Data...")
    # Keep only first 30 rows to avoid token overflow
    df_api = df_api.head(30)
    
    # Reduce long text fields before sending to API
    if "body" in df_api.columns:
        df_api["body"] = df_api["body"].apply(lambda x: x[:100] + "..." if isinstance(x, str) else x) # Limit text length
    
    df_api = cleaner.clean_data(df_api)
    df_api = ai_agent.process_data(df_api)
    print("\n✅ AI-Cleaned API Data:\n", df_api)