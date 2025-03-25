# test_preprocessing.py (corrected)
import unittest
import pandas as pd
import numpy as np
from src.core.preprocessing import PreprocessingService

class TestPreprocessing(unittest.TestCase):
    def setUp(self):
        """Create sample data for testing"""
        self.sample_data = pd.DataFrame({
            'Close': [100, 105, 110, 115, 120, 125, 130, 135, 140, 145, 150]
        })
    
    def test_feature_engineering(self):
        """Test feature engineering methods"""
        # Process data using the actual method
        processed_data = PreprocessingService.engineer_financial_features(self.sample_data)
        
        # Check if 'Returns' exists and has no NaNs
        self.assertIn('Returns', processed_data.columns)
        self.assertFalse(processed_data['Returns'].isnull().any())

if __name__ == '__main__':
    unittest.main()