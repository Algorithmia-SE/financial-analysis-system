import matplotlib.pyplot as plt
import pandas as pd
from typing import List, Dict, Any

class VisualizationService:
    def create_visualizations(
        self, 
        preprocessed_data: pd.DataFrame, 
        prediction_results: Dict[str, Any],
        ticker: str
    ) -> List[str]:
        """
        Create visualizations for market analysis
        
        Args:
            preprocessed_data (pd.DataFrame): Preprocessed stock data
            prediction_results (Dict): Prediction results
            ticker (str): Stock ticker symbol
        
        Returns:
            List of visualization file paths
        """
        visualization_paths = []
        
        # Price trend visualization
        plt.figure(figsize=(12, 6))
        plt.plot(preprocessed_data['Close'], label='Historical Price')
        plt.plot(
            pd.date_range(
                start=preprocessed_data.index[-1], 
                periods=8, 
                freq='D'
            )[1:], 
            prediction_results['forecast'], 
            color='red', 
            label='Predicted Price'
        )
        plt.title(f"{ticker} Price Trend and Forecast")
        plt.xlabel("Date")
        plt.ylabel("Price")
        plt.legend()
        plt.tight_layout()
        
        # Save price trend plot
        price_trend_path = f"{ticker}_price_trend.png"
        plt.savefig(price_trend_path)
        plt.close()
        visualization_paths.append(price_trend_path)
        
        # Confidence interval visualization
        plt.figure(figsize=(12, 6))
        conf_int = prediction_results['confidence_interval']
        plt.fill_between(
            pd.date_range(
                start=preprocessed_data.index[-1], 
                periods=8, 
                freq='D'
            )[1:], 
            [ci[0] for ci in conf_int],
            [ci[1] for ci in conf_int],
            alpha=0.3, 
            label='Confidence Interval'
        )
        plt.title(f"{ticker} Forecast Confidence Interval")
        plt.xlabel("Date")
        plt.ylabel("Price")
        plt.legend()
        plt.tight_layout()
        
        # Save confidence interval plot
        confidence_path = f"{ticker}_confidence_interval.png"
        plt.savefig(confidence_path)
        plt.close()
        visualization_paths.append(confidence_path)
        
        return visualization_paths