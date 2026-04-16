from pydantic import BaseModel, Field
from typing import Optional, Literal


class PropertyQuery(BaseModel):
    text: str


class CompletenessInfo(BaseModel):
    extracted_count: int = 0
    total_features: int = 11
    confidence: Literal["high", "medium", "low"] = "low"


class ExtractedFeatures(BaseModel):
    LotFrontage: Optional[float] = None
    LotArea: Optional[float] = None
    OverallQual: Optional[int] = None
    YearBuilt: Optional[int] = None
    GrLivArea: Optional[float] = None
    FullBath: Optional[int] = None
    BedroomAbvGr: Optional[int] = None
    GarageCars: Optional[int] = None
    Neighborhood: Optional[str] = None
    HouseStyle: Optional[str] = None
    Street: Optional[str] = None
    completeness: Optional[CompletenessInfo] = None


class PredictionResponse(BaseModel):
    price: float
    explanation: str
    missing_fields: list[str]
    features: dict
    completeness: Optional[dict] = None