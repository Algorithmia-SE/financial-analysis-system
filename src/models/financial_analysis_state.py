from typing import List, Dict, Any
from typing_extensions import TypedDict
import pandas as pd

class FinancialAnalysisState(TypedDict):
    """
    State management for the financial analysis workflow
    """
    ticker: str
    start_date: str
    end_date: str
    raw_data: pd.DataFrame
    preprocessed_data: pd.DataFrame
    prediction_model: Any
    prediction_results: Dict[str, Any]
    market_insights: str
    visualization_paths: List[str]
    analyst_feedback: str