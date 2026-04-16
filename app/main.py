from fastapi import FastAPI
from app.schemas import PropertyQuery, PredictionResponse
from app.llm.extractor_llm import extract_features
from app.llm.explainer_llm import explain
from app.model_loader import predict
from app.utils import get_missing_features

app = FastAPI()


@app.post("/predict", response_model=PredictionResponse)
def predict_price(query: PropertyQuery):

    # 🧠 LLM #1 — Extract features
    features_obj = extract_features(query.text)
    features = features_obj.dict()

    # Missing fields
    missing = get_missing_features(features)

    # ML prediction
    price = predict(features)

    # 🧠 LLM #2 — Explanation
    explanation = explain(price, features)

    return PredictionResponse(
        price=price,
        explanation=explanation,
        missing_fields=missing,
        features=features
    )