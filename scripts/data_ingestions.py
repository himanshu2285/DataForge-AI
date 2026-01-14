import os
import pandas as pd
import requests
from sqlalchemy import create_engine

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../data')

class DataIngestion:
    def __init__(self, db_url=None):
        """Initialize data ingestion with an optional database connection."""
        self.engine = create_engine(db_url) if db_url else None
        
    def load_csv(self, file_name):
        """Load data from a CSV file."""
        file_path = os.path.join(DATA_DIR, file_name)
        try:
            df = pd.read_csv(file_path)
            print(f"CSV Loaded Successfully: {file_path}")
            return df
        except Exception as e:
            print(f"Error loading CSV file {file_name}: {e}")
            return None
        
    def load_excel(self, file_name, sheet_name=0):
        """Load an Excel file into a DataFrame."""
        file_path = os.path.join(DATA_DIR, file_name)
        try:
            df = pd.read_excel(file_path, sheet_name=sheet_name)
            print(f"Excel Loaded Successfully: {file_path}")
            return df
        except Exception as e:
            print(f"Error loading Excel file {file_name}: {e}")
            return None
        
    def connect_database(self, db_url):
        """Establishes a database connection."""
        try:
            self.engine = create_engine(db_url)
            print("Database connection established.")
        except Exception as e:
            print(f"Error connecting to database: {e}")
        
    def load_data_from_db(self, query):
        """Fetches data from a database using a SQL query."""
        if not self.engine:
            print("No Database connection. Call connect_database() first.")
            return None
        try: 
            df = pd.read_sql(query, self.engine)
            print("Data fetched from database successfully.")
            return df
        except Exception as e:
            print(f"Error fetching data from database: {e}")
            return None
    
    def fetch_from_api(self, api_url, params=None):
        """Fetch data from a REST API and return as DataFrame."""
        try:
            response = requests.get(api_url, params=params)
            if response.status_code == 200:
                data = response.json()
                df = pd.DataFrame(data)
                print("Data fetched from API successfully.")
                return df
            else:
                print(f"API request failed: {response.status_code}")
                return None
        except Exception as e:
            print(f"Error fetching data from API: {e}")
            return None