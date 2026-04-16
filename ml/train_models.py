import numpy as np
import joblib

from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.ensemble import RandomForestRegressor, HistGradientBoostingRegressor

from ml.preprocess import preprocessor
from ml.train import X_train, X_val, X_test, y_train, y_val, y_test


# -------------------------
# EVALUATION FUNCTION
# -------------------------

def eval_model(name, model, X_tr, y_tr, X_ev, y_ev):
    model.fit(X_tr, y_tr)

    pred_tr = model.predict(X_tr)
    pred_ev = model.predict(X_ev)

    return {
        "name": name,
        "train_rmse": np.sqrt(mean_squared_error(y_tr, pred_tr)),
        "val_rmse": np.sqrt(mean_squared_error(y_ev, pred_ev)),
        "val_mse": mean_squared_error(y_ev, pred_ev),
        "train_r2": r2_score(y_tr, pred_tr),
        "val_r2": r2_score(y_ev, pred_ev),
        "model": model
    }


# -------------------------
# MODELS
# -------------------------

rf_pipeline = Pipeline([
    ("preprocessor", preprocessor),
    ("model", RandomForestRegressor(
        n_estimators=400,
        max_depth=8,
        min_samples_leaf=5,
        max_features="sqrt",
        random_state=42,
        n_jobs=-1
    ))
])

hgb_pipeline = Pipeline([
    ("preprocessor", preprocessor),
    ("model", HistGradientBoostingRegressor(
        max_depth=4,
        learning_rate=0.05,
        max_iter=300,
        min_samples_leaf=10,
        random_state=42
    ))
])


# -------------------------
# TRAIN + VALIDATE
# -------------------------

rf_res = eval_model("RandomForest", rf_pipeline, X_train, y_train, X_val, y_val)
hgb_res = eval_model("HistGradientBoosting", hgb_pipeline, X_train, y_train, X_val, y_val)


# -------------------------
# SELECT BEST MODEL (VAL SET ONLY)
# -------------------------

results = [rf_res, hgb_res]

best = min(results, key=lambda x: x["val_rmse"])

best_model = best["model"]

print("\nMODEL COMPARISON")
print("-" * 60)

for r in results:
    print(f"{r['name']:<22} "
          f"Train RMSE: {r['train_rmse']:.0f} | "
          f"Val RMSE: {r['val_rmse']:.0f} | "
          f"Val MSE: {r['val_mse']:.0f} | "
          f"Val R2: {r['val_r2']:.3f}")

print("\n🏆 BEST MODEL:", best["name"])


# -------------------------
# FINAL TEST EVALUATION (IMPORTANT)
# -------------------------

best_model.fit(X_train, y_train)

test_pred = best_model.predict(X_test)

test_rmse = np.sqrt(mean_squared_error(y_test, test_pred))
test_mse = mean_squared_error(y_test, test_pred)
test_r2 = r2_score(y_test, test_pred)

print("\nFINAL TEST RESULTS")
print("-" * 60)
print(f"Test RMSE: {test_rmse:.0f}")
print(f"Test MSE: {test_mse:.0f}")
print(f"Test R2:   {test_r2:.3f}")


# -------------------------
# SAVE MODEL
# -------------------------

joblib.dump(best_model, "ml/best_model.pkl")

print("\n✅ Saved best model to ml/best_model.pkl")