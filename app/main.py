from pydantic import BaseModel, Field
from typing import Optional, Literal, Dict, Any


class PropertyQuery(BaseModel):
    text: str = Field(..., description="Natural language property description")
    
    class Config:
        json_schema_extra = {
            "example": {
                "text": "3 bedroom ranch with large garage in nice neighborhood"
            }
        }


class CompletenessInfo(BaseModel):
    extracted_count: int = Field(0, description="Number of features successfully extracted")
    total_features: int = Field(11, description="Total features needed for prediction")
    confidence: Literal["high", "medium", "low"] = Field("low", description="Confidence in extraction quality")


class ExtractedFeatures(BaseModel):
    LotFrontage: Optional[float] = Field(None, description="Linear feet of street connected to property")
    LotArea: Optional[float] = Field(None, description="Lot size in square feet")
    OverallQual: Optional[int] = Field(None, ge=1, le=10, description="Overall material and finish quality")
    YearBuilt: Optional[int] = Field(None, description="Original construction date")
    GrLivArea: Optional[float] = Field(None, description="Above grade living area in square feet")
    FullBath: Optional[int] = Field(None, description="Full bathrooms above grade")
    BedroomAbvGr: Optional[int] = Field(None, description="Bedrooms above grade")
    GarageCars: Optional[int] = Field(None, description="Garage capacity in cars")
    Neighborhood: Optional[str] = Field(None, description="Neighborhood name")
    HouseStyle: Optional[str] = Field(None, description="Style of dwelling")
    Street: Optional[str] = Field(None, description="Type of road access")
    completeness: Optional[CompletenessInfo] = Field(None, description="Extraction completeness metadata")
    
    class Config:
        json_schema_extra = {
            "example": {
                "LotFrontage": 60.0,
                "LotArea": 8450.0,
                "OverallQual": 7,
                "YearBuilt": 1995,
                "GrLivArea": 1850.0,
                "FullBath": 2,
                "BedroomAbvGr": 3,
                "GarageCars": 2,
                "Neighborhood": "Northridge",
                "HouseStyle": "1Story",
                "Street": "Paved",
                "completeness": {
                    "extracted_count": 11,
                    "total_features": 11,
                    "confidence": "high"
                }
            }
        }


class PredictionResponse(BaseModel):
    price: float = Field(..., description="Predicted sale price in dollars")
    explanation: str = Field(..., description="LLM-generated explanation of the prediction")
    missing_fields: list[str] = Field(default_factory=list, description="Features not found in query")
    features: Dict[str, Any] = Field(..., description="Extracted feature values")
    completeness: Optional[Dict[str, Any]] = Field(None, description="Completeness metadata")
    
    class Config:
        json_schema_extra = {
            "example": {
                "price": 285000.0,
                "explanation": "This 3-bedroom ranch is valued at $285,000, which is above the market median of $180,000...",
                "missing_fields": ["LotFrontage", "Street"],
                "features": {
                    "BedroomAbvGr": 3,
                    "HouseStyle": "Ranch",
                    "GarageCars": 2
                },
                "completeness": {
                    "extracted_count": 3,
                    "total_features": 11,
                    "confidence": "low"
                }
            }
        }