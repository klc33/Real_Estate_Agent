from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import traceback

from app.schemas import PropertyQuery, PredictionResponse
from llm.extractor_llm import extract_features
from llm.explainer_llm import explain
from app.model_loader import predict
from app.utils import get_missing_features

app = FastAPI(title="AI Real Estate Agent")

# Add CORS for Streamlit
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health_check():
    """Health check endpoint for Railway"""
    return {"status": "healthy"}


@app.post("/predict", response_model=PredictionResponse)
def predict_price(query: PropertyQuery):
    """
    Main prediction endpoint.
    Chain: Extract → Predict → Explain
    """
    try:
        # Stage 1: Extract features with completeness
        features_obj = extract_features(query.text)
        features = features_obj.model_dump()
        
        # Identify missing fields
        missing = get_missing_features(features)
        completeness = features.get("completeness", {})
        
        # Validate minimum features for prediction
        extracted = completeness.get("extracted_count", 0)
        if extracted < 3:
            # Too few features for meaningful prediction
            return PredictionResponse(
                price=0.0,
                explanation="I need more information to provide an accurate estimate. "
                          f"Currently I only know about {extracted} feature(s). "
                          "Could you provide details about square footage, bedrooms, "
                          "bathrooms, or neighborhood?",
                missing_fields=missing,
                features=features,
                completeness=completeness
            )
        
        # Stage 2: ML Prediction
        try:
            price = predict(features)
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Prediction failed: {str(e)}"
            )
        
        # Stage 3: LLM Explanation
        explanation = explain(price, features)
        
        return PredictionResponse(
            price=price,
            explanation=explanation,
            missing_fields=missing,
            features=features,
            completeness=completeness
        )
        
    except Exception as e:
        error_detail = {
            "error": str(e),
            "traceback": traceback.format_exc()
        }
        print(f"Error in prediction: {error_detail}")
        raise HTTPException(
            status_code=500,
            detail=f"Prediction pipeline error: {str(e)}"
        )