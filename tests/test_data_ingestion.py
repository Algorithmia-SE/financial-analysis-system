import unittest
import pandas as pd
import yfinance as yf
from src.core.data_ingestion import DataIngestionService

class TestDataIngestionService(unittest.TestCase):
    def setUp(self):
        """Set up test parameters"""
        self.ticker = 'AAPL'
        self.start_date = '2023-01-01'
        self.end_date = '2023-12-31'

    def test_fetch_stock_data_success(self):
        """Test successful stock data retrieval"""
        result = DataIngestionService.fetch_stock_data(
            self.ticker, 
            self.start_date, 
            self.end_date
        )
        
        # Check keys
        self.assertIn('raw_data', result)
        self.assertIn('preprocessed_data', result)
        
        # Validate raw data
        self.assertIsInstance(result['raw_data'], pd.DataFrame)
        self.assertFalse(result['raw_data'].empty)
        
        # Validate preprocessed data
        self.assertIsInstance(result['preprocessed_data'], pd.DataFrame)
        self.assertFalse(result['preprocessed_data'].empty)

    def test_preprocess_data(self):
        """Test data preprocessing methods"""
        # Create sample dataframe
        sample_data = pd.DataFrame({
            'Open': [100, 102, 105, 103],
            'High': [105, 107, 110, 108],
            'Low': [98, 100, 103, 101],
            'Close': [102, 104, 107, 105]
        })
        
        preprocessed_data = DataIngestionService._preprocess_data(sample_data)
        
        # Check additional columns
        self.assertIn('Returns', preprocessed_data.columns)
        self.assertIn('Rolling_Mean', preprocessed_data.columns)
        self.assertIn('Rolling_Std', preprocessed_data.columns)
        
        # Verify no NaN values
        self.assertFalse(preprocessed_data.isnull().any().any())

    def test_fetch_stock_data_invalid_ticker(self):
        """Test error handling for invalid ticker"""
        with self.assertRaises(ValueError):
            DataIngestionService.fetch_stock_data(
                'INVALIDTICKER', 
                self.start_date, 
                self.end_date
            )

if __name__ == '__main__':
    unittest.main()