import yfinance as yf
import pandas as pd
from typing import Dict, Any
from src.models.financial_analysis_state import FinancialAnalysisState

class DataIngestionService:
    @staticmethod
    def fetch_stock_data(ticker: str, start_date: str, end_date: str) -> Dict[str, Any]:
        """
        Fetch stock data from Yahoo Finance
        
        Args:
            ticker (str): Stock ticker symbol
            start_date (str): Start date for data retrieval
            end_date (str): End date for data retrieval
        
        Returns:
            Dict containing raw and preprocessed data
        """
        try:
            # Download stock data
            df = yf.download(
                ticker, 
                start=start_date, 
                end=end_date
            )

            if df.empty:
                raise ValueError("No data found for the given ticker and date range")
            
            # Preprocess data
            df_cleaned = DataIngestionService._preprocess_data(df)
            
            return {
                'raw_data': df,
                'preprocessed_data': df_cleaned
            }
        except Exception as e:
            raise ValueError(f"Data ingestion error: {str(e)}")
    
    @staticmethod
    def _preprocess_data(df: pd.DataFrame) -> pd.DataFrame:
        """
        Preprocess financial data
        
        Args:
            df (pd.DataFrame): Raw stock data
        
        Returns:
            Cleaned and feature-engineered DataFrame
        """
        # Remove any rows with missing values
        df_cleaned = df.dropna()
        
        # Calculate additional features
        df_cleaned['Returns'] = df_cleaned['Close'].pct_change()
        df_cleaned['Rolling_Mean'] = df_cleaned['Close'].rolling(window=20).mean()
        df_cleaned['Rolling_Std'] = df_cleaned['Close'].rolling(window=20).std()
        
        return df_cleaned.dropna()