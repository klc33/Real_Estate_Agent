"""
Model training and evaluation script.
"""

import numpy as np
import joblib
import json
import logging
from datetime import datetime

from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
from sklearn.ensemble import RandomForestRegressor, HistGradientBoostingRegressor
from sklearn.linear_model import Ridge

from ml.preprocess import preprocessor
from ml.train import X_train, X_val, X_test, y_train, y_val, y_test

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def evaluate_model(name: str, model: Pipeline, X_tr, y_tr, X_ev, y_ev) -> dict:
    """
    Train and evaluate a model.
    Returns dictionary with metrics and trained model.
    """
    logger.info(f"Training {name}...")
    model.fit(X_tr, y_tr)
    
    # Make predictions (in original dollar space)
    pred_tr = model.predict(X_tr)
    pred_ev = model.predict(X_ev)
    
    # Calculate metrics
    results = {
        "name": name,
        "train_rmse": np.sqrt(mean_squared_error(y_tr, pred_tr)),
        "val_rmse": np.sqrt(mean_squared_error(y_ev, pred_ev)),
        "train_mae": mean_absolute_error(y_tr, pred_tr),
        "val_mae": mean_absolute_error(y_ev, pred_ev),
        "train_r2": r2_score(y_tr, pred_tr),
        "val_r2": r2_score(y_ev, pred_ev),
        "model": model
    }
    
    logger.info(f"{name} - Val RMSE: ${results['val_rmse']:,.0f}, Val R²: {results['val_r2']:.3f}")
    
    return results


# Define models to test
models = {
    "Ridge": Pipeline([
        ("preprocessor", preprocessor),
        ("model", Ridge(alpha=1.0, random_state=42))
    ]),
    
    "RandomForest": Pipeline([
        ("preprocessor", preprocessor),
        ("model", RandomForestRegressor(
            n_estimators=300,
            max_depth=10,
            min_samples_split=10,
            min_samples_leaf=5,
            max_features="sqrt",
            random_state=42,
            n_jobs=-1
        ))
    ]),
    
    "HistGradientBoosting": Pipeline([
        ("preprocessor", preprocessor),
        ("model", HistGradientBoostingRegressor(
            max_depth=5,
            learning_rate=0.05,
            max_iter=300,
            min_samples_leaf=10,
            random_state=42
        ))
    ])
}


def main():
    """Main training workflow"""
    logger.info("=" * 60)
    logger.info("STARTING MODEL TRAINING")
    logger.info("=" * 60)
    
    # Train and evaluate all models
    results = []
    for name, model_pipeline in models.items():
        try:
            result = evaluate_model(
                name, model_pipeline, 
                X_train, y_train, 
                X_val, y_val
            )
            results.append(result)
        except Exception as e:
            logger.error(f"Failed to train {name}: {e}")
    
    # Select best model based on validation RMSE
    best = min(results, key=lambda x: x["val_rmse"])
    best_model = best["model"]
    
    # Print comparison
    print("\n" + "=" * 80)
    print("MODEL COMPARISON (Validation Set)")
    print("=" * 80)
    print(f"{'Model':<20} {'Train RMSE':>12} {'Val RMSE':>12} {'Val MAE':>12} {'Val R²':>10}")
    print("-" * 80)
    
    for r in results:
        print(f"{r['name']:<20} "
              f"${r['train_rmse']:>10,.0f} "
              f"${r['val_rmse']:>10,.0f} "
              f"${r['val_mae']:>10,.0f} "
              f"{r['val_r2']:>9.3f}")
    
    print("-" * 80)
    print(f"🏆 BEST MODEL: {best['name']}")
    print("=" * 80)
    
    # Final evaluation on test set
    logger.info("\nEvaluating best model on test set...")
    
    best_model.fit(X_train, y_train)
    test_pred = best_model.predict(X_test)
    
    test_rmse = np.sqrt(mean_squared_error(y_test, test_pred))
    test_mae = mean_absolute_error(y_test, test_pred)
    test_r2 = r2_score(y_test, test_pred)
    
    print("\n" + "=" * 80)
    print("FINAL TEST RESULTS")
    print("=" * 80)
    print(f"Test RMSE: ${test_rmse:,.0f}")
    print(f"Test MAE:  ${test_mae:,.0f}")
    print(f"Test R²:   {test_r2:.3f}")
    print("=" * 80)
    
    # Save training statistics
    train_stats = {
        "median_price": float(y_train.median()),
        "mean_price": float(y_train.mean()),
        "price_std": float(y_train.std()),
        "price_range": [float(y_train.min()), float(y_train.max())],
        "sample_count": len(y_train),
        "best_model": best["name"],
        "test_rmse": float(test_rmse),
        "test_r2": float(test_r2),
        "training_date": datetime.now().isoformat(),
        "features_used": X_train.columns.tolist()
    }
    
    with open("ml/training_stats.json", "w") as f:
        json.dump(train_stats, f, indent=2)
    
    logger.info("✅ Saved training stats to ml/training_stats.json")
    
    # Save the best model
    joblib.dump(best_model, "ml/best_model.pkl")
    logger.info("✅ Saved best model to ml/best_model.pkl")
    
    return best_model, test_rmse, test_r2


if __name__ == "__main__":
    best_model, test_rmse, test_r2 = main()