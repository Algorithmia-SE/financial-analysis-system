import unittest
import pandas as pd
import numpy as np
from src.core.prediction import PredictionService

class TestPredictionService(unittest.TestCase):
    def setUp(self):
        """Create sample time series data for testing"""
        np.random.seed(42)
        dates = pd.date_range(start='2023-01-01', end='2023-12-31', freq='D')
        self.sample_data = pd.Series(
            np.cumsum(np.random.normal(0.001, 0.01, len(dates))),
            index=dates
        )

    def test_forecast_prices(self):
        """Test price forecasting method"""
        forecast_result = PredictionService.forecast_prices(self.sample_data)
        
        # Check result structure
        self.assertIn('prediction_model', forecast_result)
        self.assertIn('prediction_results', forecast_result)
        
        prediction_results = forecast_result['prediction_results']
        
        # Check forecast contents
        self.assertIn('forecast', prediction_results)
        self.assertIn('confidence_interval', prediction_results)
        
        # Verify forecast length
        self.assertEqual(len(prediction_results['forecast']), 7)
        self.assertEqual(len(prediction_results['confidence_interval']), 7)

    def test_forecast_periods(self):
        """Test custom forecast periods"""
        custom_periods = 14
        forecast_result = PredictionService.forecast_prices(
            self.sample_data, 
            periods=custom_periods
        )
        
        prediction_results = forecast_result['prediction_results']
        
        # Verify custom period length
        self.assertEqual(len(prediction_results['forecast']), custom_periods)
        self.assertEqual(len(prediction_results['confidence_interval']), custom_periods)

    def test_forecast_error_handling(self):
        """Test error handling for insufficient data"""
        # Create very short time series
        short_data = pd.Series([100, 101, 102])
        
        with self.assertRaises(ValueError):
            PredictionService.forecast_prices(short_data)

    def test_forecast_result_types(self):
        """Verify forecast result data types"""
        forecast_result = PredictionService.forecast_prices(self.sample_data)
        prediction_results = forecast_result['prediction_results']
        
        # Check forecast types
        self.assertIsInstance(prediction_results['forecast'], list)
        self.assertIsInstance(prediction_results['confidence_interval'], list)
        
        # Check numeric values
        self.assertTrue(all(isinstance(x, (int, float)) for x in prediction_results['forecast']))

if __name__ == '__main__':
    unittest.main()