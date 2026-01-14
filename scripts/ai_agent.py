# AI Powered Data Cleaning and preprocessing Agent

import pandas as pd
from openai import OpenAI
from dotenv import load_dotenv
import os
from langchain_openai import OpenAI 
from langgraph.graph import StateGraph, END
from pydantic import BaseModel


# Load API Key from Environment 
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

if not openai_api_key:
    raise ValueError("OpenAI API key not found. Please set the OPENAI_API_KEY environment variable.")

# Define AI Model
llm = OpenAI(openai_api_key=openai_api_key, model_name="gpt-4", temperature=0)

class CleaningState(BaseModel):
    """State Schema defining Input and Output for the LangGraph Agent"""
    input_text: str
    structured_response: str = ""

    
class AIAgent:
    def __init__(self):
        self.graph = self.create_graph()
        
    def create_graph(self):
        """Creates and returns a langgraph agent graph with state management."""
        graph = StateGraph(CleaningState, llm=llm)
        
        # Ensure output structured response
        def agent_logic(state: CleaningState) -> CleaningState:
            """Processes input and returns structured response."""
            response = llm.invoke(state.input_text)
            return CleaningState(input_text=state.input_text, structured_response=response)

        graph.add_node("cleaning_agent", agent_logic)
        graph.add_edge("cleaning_agent", END)
        graph.set_entry_point("cleaning_agent")
        return graph.compile()
    
    def process_data(self, df, batch_size=20):
        """Processes Data in batches to avoid OpenAI's token limit."""
        cleaned_responses = []
        for i in range(0, len(df), batch_size):
            df_batch = df.iloc[i:i+batch_size]
            promt = f"""
            You are an AI Data Cleaning Agent. Analyze the dataset:
            {df_batch.to_string()}
            Identify missing values, choose the best imputation strategy (mean, mode, median),
            remove duplicates, and format text correctly.
            
            return the cleaned data as a structured format.
            """
            
            state = CleaningState(input_text=promt, structured_response="")
            response = self.graph.invoke(state)

            if isinstance(response, dict):
                response = CleaningState(**response)
                
            cleaned_responses.append(response.structured_response) # store results
            
        return "\n".join(cleaned_responses)  # Combine all batch responses into one