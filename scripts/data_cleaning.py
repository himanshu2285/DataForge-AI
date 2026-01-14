# Here we are going to handle missing values, duplicates, and inconsistent data formats

import pandas as pd
import numpy as np

class DataCleaning:
    def handle_missing_values(self, df, strategy='mean'):
        """Handles missing values by filling with mean, median, mode or dropping."""
        if strategy == 'mean':
            return df.fillna(df.mean(numeric_only=True), inplace=True)
        elif strategy == 'median':
            return df.fillna(df.median(numeric_only=True), inplace=True)
        elif strategy == 'mode':
            return df.fillna(df.mode().iloc[0], inplace=True)
        elif strategy == 'drop':
            return df.dropna()
        return df
    
    def remove_duplicates(self, df):
        """Remove duplicate rows from the DataFrame."""
        return df.drop_duplicates()
    
    def fix_data_types(self, df):
        """Attempts to convert columns to appropriate data types."""
        for col in df.columns:
            try:
                df[col] = pd.to_numeric(df[col])
            except ValueError:
                pass
        return df
    
    def clean_data(self, df):
        """Applies all cleaning steps."""
        df = self.handle_missing_values(df)
        df = self.remove_duplicates(df)
        df = self.fix_data_types(df)
        return df
    
                