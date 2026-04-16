import numpy as np
import joblib

from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.ensemble import RandomForestRegressor, HistGradientBoostingRegressor

from ml.preprocess import preprocessor
from ml.train import X_train, X_val, y_train, y_val


# -------------------------
# EVALUATION FUNCTION (FIXED)
# -------------------------

def eval_pipeline(name, pipeline, X_tr, y_tr, X_ev, y_ev):
    pipeline.fit(X_tr, y_tr)

    train_pred = pipeline.predict(X_tr)
    val_pred = pipeline.predict(X_ev)

    return {
        "model": name,

        "train_mae": mean_absolute_error(y_tr, train_pred),
        "train_rmse": np.sqrt(mean_squared_error(y_tr, train_pred)),
        "train_r2": r2_score(y_tr, train_pred),

        "val_mae": mean_absolute_error(y_ev, val_pred),
        "val_rmse": np.sqrt(mean_squared_error(y_ev, val_pred)),
        "val_r2": r2_score(y_ev, val_pred),

        "pipeline": pipeline
    }


# -------------------------
# RANDOM FOREST (REGULARIZED)
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


# -------------------------
# HIST GRADIENT BOOSTING (BEST PRACTICE MODEL)
# -------------------------

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
# TRAIN MODELS
# -------------------------

rf_results = eval_pipeline(
    "RandomForest",
    rf_pipeline,
    X_train, y_train,
    X_val, y_val
)

hgb_results = eval_pipeline(
    "HistGradientBoosting",
    hgb_pipeline,
    X_train, y_train,
    X_val, y_val
)


# -------------------------
# COMPARE MODELS
# -------------------------

all_results = [rf_results, hgb_results]

print(f'{"Model":<25} {"Train RMSE":>12} {"Val RMSE":>12} {"Gap":>12} {"Train R2":>10} {"Val R2":>10}')
print("-" * 85)

best_score = float("inf")
best_model = None
best_pipeline = None

for r in all_results:
    gap = r["val_rmse"] - r["train_rmse"]

    print(f'{r["model"]:<25} '
          f'{r["train_rmse"]:>12,.0f} '
          f'{r["val_rmse"]:>12,.0f} '
          f'{gap:>+12,.0f} '
          f'{r["train_r2"]:>10.3f} '
          f'{r["val_r2"]:>10.3f}')

    if r["val_rmse"] < best_score:
        best_score = r["val_rmse"]
        best_model = r["model"]
        best_pipeline = r["pipeline"]


# -------------------------
# FINAL RESULT
# -------------------------

print("\n" + "-" * 85)
print(f"🏆 BEST MODEL: {best_model}")
print(f"📉 BEST VAL RMSE: {best_score:,.0f}")


# -------------------------
# SAVE MODEL
# -------------------------

joblib.dump(best_pipeline, "ml/best_model.pkl")

print("\n✅ Model saved to ml/best_model.pkl")