"""
Data loading and splitting for model training.
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
import logging

from ml.features import FEATURES, TARGET

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Load and prepare data
def load_data(filepath: str = "data/raw.csv") -> tuple:
    """
    Load the Ames housing dataset and split into train/val/test.
    
    Returns:
        X_train, X_val, X_test, y_train, y_val, y_test
    """
    logger.info(f"Loading data from {filepath}")
    
    # Load data
    df = pd.read_csv(filepath)
    logger.info(f"Loaded {len(df)} rows")
    
    # Select features and target
    available_features = [f for f in FEATURES if f in df.columns]
    missing_features = set(FEATURES) - set(available_features)
    
    if missing_features:
        logger.warning(f"Missing features: {missing_features}")
    
    df = df[available_features + [TARGET]]
    
    # Remove rows with missing target
    df = df.dropna(subset=[TARGET])
    logger.info(f"After removing missing targets: {len(df)} rows")
    
    # Separate features and target
    X = df[available_features]
    y = df[TARGET]
    
    # NO LOG TRANSFORM - Keep prices in original dollars
    logger.info(f"Target range: ${y.min():,.0f} - ${y.max():,.0f}")
    
    # Split: 60% train, 20% validation, 20% test
    X_train, X_temp, y_train, y_temp = train_test_split(
        X, y, test_size=0.4, random_state=42
    )
    
    X_val, X_test, y_val, y_test = train_test_split(
        X_temp, y_temp, test_size=0.5, random_state=42
    )
    
    logger.info(f"Train: {len(X_train)} rows")
    logger.info(f"Validation: {len(X_val)} rows")
    logger.info(f"Test: {len(X_test)} rows")
    
    return X_train, X_val, X_test, y_train, y_val, y_test


# Load the data
try:
    X_train, X_val, X_test, y_train, y_val, y_test = load_data()
except FileNotFoundError:
    logger.error("data/raw.csv not found. Please download the Ames dataset.")
    logger.info("Download from: https://www.kaggle.com/c/house-prices-advanced-regression-techniques/data")
    raise
except Exception as e:
    logger.error(f"Error loading data: {e}")
    raise