from langchain_groq import ChatGroq
import pandas as pd
from typing import Dict, Any

class MarketInsightsService:
    def __init__(self, model: str = "llama3-8b-8192", temperature: float = 0.3):
        """
        Initialize Market Insights Service with LLM
        
        Args:
            model (str): LLM model to use
            temperature (float): Creativity/randomness of responses
        """
        self.llm = ChatGroq(
            model=model,
            temperature=temperature,
            max_tokens=None
        )
    
    def generate_insights(self, recent_data: pd.DataFrame, predictions: list) -> Dict[str, str]:
        """
        Generate market insights using LLM
        
        Args:
            recent_data (pd.DataFrame): Recent stock performance data
            predictions (list): Price predictions
        
        Returns:
            Dict with market insights
        """
        try:
            prompt = f"""
            Analyze the following financial data:
            Recent Stock Performance:
            {recent_data.to_string()}
            
            Price Predictions for Next Week:
            {predictions}
            
            Provide a comprehensive market insight including:
            1. Current market trend
            2. Potential investment risks
            3. Short-term price movement prediction
            4. Recommendation for investors
            """
            
            response = self.llm.invoke(prompt)
            
            return {
                'market_insights': response.content
            }
        except Exception as e:
            raise ValueError(f"Market insights generation error: {str(e)}")