import joblib
import pandas as pd

MODEL_PATH = "ml/best_model.pkl"

model = joblib.load(MODEL_PATH)


def predict(features: dict):

    df = pd.DataFrame([features])

    # safety: ensure column order matches training
    return model.predict(df)[0]