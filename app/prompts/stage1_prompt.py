def build_stage1_prompt_v1(user_query: str):
    """Version 1: More structured output request"""
    return [
        {
            "role": "system",
            "content": """You are a real estate data extraction assistant.
Extract property features from user descriptions into structured JSON.
Only extract what is explicitly mentioned or strongly implied.
Return null for missing features. DO NOT guess or use defaults.

Return format:
{
    "LotFrontage": number or null,
    "LotArea": number or null,
    "OverallQual": number (1-10) or null,
    "YearBuilt": number or null,
    "GrLivArea": number or null,
    "FullBath": number or null,
    "BedroomAbvGr": number or null,
    "GarageCars": number or null,
    "Neighborhood": string or null,
    "HouseStyle": string or null,
    "Street": string or null,
    "completeness": {
        "extracted_count": number,
        "total_features": 11,
        "confidence": "high|medium|low"
    }
}"""
        },
        {
            "role": "user",
            "content": user_query
        }
    ]


def build_stage1_prompt_v2(user_query: str):
    """Version 2: More conversational approach"""
    return [
        {
            "role": "system",
            "content": """You are a helpful real estate assistant. 
Given a user's property description, extract the following information as JSON.
Only include features that are clearly stated. Use null for missing information.

Features to extract:
- LotFrontage (feet)
- LotArea (square feet)
- OverallQual (1-10 rating)
- YearBuilt
- GrLivArea (above ground living area in sq ft)
- FullBath (number)
- BedroomAbvGr (bedrooms above grade)
- GarageCars (capacity)
- Neighborhood (name)
- HouseStyle (e.g., 1Story, 2Story, Ranch)
- Street (e.g., Paved, Gravel)

Also include a completeness object with extracted_count and confidence level."""
        },
        {
            "role": "user",
            "content": user_query
        }
    ]


# Default to v1 as it's more structured
build_stage1_prompt = build_stage1_prompt_v1