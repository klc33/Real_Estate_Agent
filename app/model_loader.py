import joblib
import pandas as pd
import os
import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

# Get absolute path for Docker compatibility
MODEL_PATH = os.path.join(os.path.dirname(__file__), "..", "ml", "best_model.pkl")
STATS_PATH = os.path.join(os.path.dirname(__file__), "..", "ml", "training_stats.json")

# Lazy loading pattern - better for API startup
_model = None
_stats = None


def get_model():
    """Lazy load the model on first use"""
    global _model
    if _model is None:
        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError(f"Model not found at {MODEL_PATH}. Please train the model first.")
        logger.info(f"Loading model from {MODEL_PATH}")
        _model = joblib.load(MODEL_PATH)
        logger.info("Model loaded successfully")
    return _model


def get_training_stats() -> Dict[str, Any]:
    """Load training statistics for context"""
    global _stats
    if _stats is None:
        if os.path.exists(STATS_PATH):
            import json
            with open(STATS_PATH, "r") as f:
                _stats = json.load(f)
        else:
            # Fallback stats
            _stats = {
                "median_price": 180000,
                "mean_price": 185000,
                "price_std": 80000,
                "price_range": [50000, 750000],
                "sample_count": 2000
            }
    return _stats


def predict(features: Dict[str, Any]) -> float:
    """
    Make prediction with proper feature handling.
    Handles missing values appropriately.
    """
    model = get_model()
    
    # Remove completeness field if present - not used for prediction
    clean_features = {}
    for k, v in features.items():
        if k != "completeness" and v is not None:
            clean_features[k] = v
    
    # Expected feature columns in correct order
    expected_cols = [
        "LotFrontage", "LotArea", "OverallQual", "YearBuilt", "Street",
        "GrLivArea", "FullBath", "BedroomAbvGr", "GarageCars",
        "Neighborhood", "HouseStyle"
    ]
    
    # Create DataFrame with all expected columns
    df_data = {}
    for col in expected_cols:
        df_data[col] = clean_features.get(col, None)
    
    df = pd.DataFrame([df_data])
    
    # Predict and return scalar value
    try:
        prediction = model.predict(df)[0]
        return float(prediction)
    except Exception as e:
        logger.error(f"Prediction error: {e}")
        raise ValueError(f"Model prediction failed: {e}")