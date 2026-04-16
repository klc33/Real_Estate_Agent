from pydantic import BaseModel
from typing import Optional


class PropertyQuery(BaseModel):
    text: str


class ExtractedFeatures(BaseModel):
    LotFrontage: Optional[float]
    LotArea: Optional[float]
    OverallQual: Optional[int]
    YearBuilt: Optional[int]
    GrLivArea: Optional[float]
    FullBath: Optional[int]
    BedroomAbvGr: Optional[int]
    GarageCars: Optional[int]

    Neighborhood: Optional[str]
    HouseStyle: Optional[str]
    Street: Optional[str]


class PredictionResponse(BaseModel):
    price: float
    explanation: str
    missing_fields: list[str]
    features: dict