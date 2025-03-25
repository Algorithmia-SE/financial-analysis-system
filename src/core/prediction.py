import pmdarima as pm
import pandas as pd
from typing import Dict, Any

class PredictionService:
    @staticmethod
    def forecast_prices(data: pd.Series, periods: int = 7) -> Dict[str, Any]:
        """
        Generate price forecasts using Auto ARIMA
        
        Args:
            data (pd.Series): Historical price data
            periods (int): Number of periods to forecast
        
        Returns:
            Dict containing forecast and confidence intervals
        """
        try:
            # Fit Auto ARIMA model
            model = pm.auto_arima(
                data, 
                seasonal=True, 
                m=12,  # Monthly seasonality
                suppress_warnings=True,
                stepwise=True
            )
            
            # Forecast next week's prices
            forecast, conf_int = model.predict(n_periods=periods, return_conf_int=True)
            
            return {
                'prediction_model': model,
                'prediction_results': {
                    'forecast': forecast.tolist(),
                    'confidence_interval': conf_int.tolist()
                }
            }
        except Exception as e:
            raise ValueError(f"Prediction error: {str(e)}")