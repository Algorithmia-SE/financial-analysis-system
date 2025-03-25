import pandas as pd
import numpy as np
from typing import Dict, Any

class PreprocessingService:
    @staticmethod
    def normalize_data(data: pd.DataFrame) -> pd.DataFrame:
        """
        Normalize numerical columns using min-max scaling
        
        Args:
            data (pd.DataFrame): Input DataFrame
        
        Returns:
            pd.DataFrame: Normalized DataFrame
        """
        numeric_columns = data.select_dtypes(include=[np.number]).columns
        data_normalized = data.copy()
        
        for col in numeric_columns:
            data_normalized[f'{col}_normalized'] = (data[col] - data[col].min()) / \
                (data[col].max() - data[col].min())
        
        return data_normalized
    
    @staticmethod
    def handle_missing_values(data: pd.DataFrame, strategy: str = 'mean') -> pd.DataFrame:
        """
        Handle missing values in the DataFrame
        
        Args:
            data (pd.DataFrame): Input DataFrame
            strategy (str): Imputation strategy
        
        Returns:
            pd.DataFrame: DataFrame with imputed values
        """
        data_imputed = data.copy()
        
        if strategy == 'mean':
            data_imputed = data_imputed.fillna(data_imputed.mean())
        elif strategy == 'median':
            data_imputed = data_imputed.fillna(data_imputed.median())
        elif strategy == 'forward_fill':
            data_imputed = data_imputed.fillna(method='ffill')
        elif strategy == 'backward_fill':
            data_imputed = data_imputed.fillna(method='bfill')
        
        return data_imputed
    
    @staticmethod
    def engineer_financial_features(data: pd.DataFrame) -> pd.DataFrame:
        """
        Create additional financial features
        
        Args:
            data (pd.DataFrame): Input financial data
        
        Returns:
            pd.DataFrame: DataFrame with engineered features
        """
        data_features = data.copy()
        
        # Price change percentage
        data_features['Returns'] = data_features['Close'].pct_change()
        
        # Moving averages
        data_features['MA_20'] = data_features['Close'].rolling(window=20).mean()
        data_features['MA_50'] = data_features['Close'].rolling(window=50).mean()
        
        # Standard deviation of returns
        data_features['Returns_Volatility'] = data_features['Returns'].rolling(window=20).std()
        
        # Relative Strength Index (RSI) - simplified
        delta = data_features['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        
        rs = gain / loss
        data_features['RSI'] = 100 - (100 / (1 + rs))
        
        return data_features.dropna()