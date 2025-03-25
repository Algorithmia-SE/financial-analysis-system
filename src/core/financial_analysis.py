import matplotlib.pyplot as plt
import pandas as pd
from typing import Dict, Any

from src.core.data_ingestion import DataIngestionService
from src.core.prediction import PredictionService
from src.core.insights import MarketInsightsService
from src.utils.visualization import VisualizationService

class FinancialAnalysisSystem:
    def __init__(self):
        self.data_service = DataIngestionService()
        self.prediction_service = PredictionService()
        self.insights_service = MarketInsightsService()
        self.visualization_service = VisualizationService()
    
    def run_analysis(self, ticker: str, start_date: str, end_date: str) -> Dict[str, Any]:
        """
        Execute complete financial analysis workflow
        
        Args:
            ticker (str): Stock ticker symbol
            start_date (str): Analysis start date
            end_date (str): Analysis end date
        
        Returns:
            Dict containing analysis results
        """
        try:
            # 1. Data Ingestion
            data_result = self.data_service.fetch_stock_data(ticker, start_date, end_date)
            preprocessed_data = data_result['preprocessed_data']
            
            # 2. Predictive Modeling
            prediction_result = self.prediction_service.forecast_prices(
                preprocessed_data['Close']
            )
            
            # 3. Market Insights
            market_insights = self.insights_service.generate_insights(
                preprocessed_data.tail(10), 
                prediction_result['prediction_results']['forecast']
            )
            
            # 4. Visualization
            visualization_paths = self.visualization_service.create_visualizations(
                preprocessed_data, 
                prediction_result['prediction_results'],
                ticker
            )
            
            # Combine results
            return {
                'ticker': ticker,
                **data_result,
                **prediction_result,
                **market_insights,
                'visualization_paths': visualization_paths
            }
        
        except Exception as e:
            raise ValueError(f"Financial analysis error: {str(e)}")