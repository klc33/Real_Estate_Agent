import json
import logging
import re
from typing import Dict, Any
from llm.client import call_llm
from app.schemas import ExtractedFeatures

logger = logging.getLogger(__name__)


def extract_features(text: str, prompt_version: str = "v1") -> ExtractedFeatures:
    """
    Extract features from natural language query.
    Includes robust error handling and fallback extraction.
    """
    
    # Improved prompt that forces better extraction
    messages = [
        {
            "role": "system",
            "content": """You are a real estate data extraction expert. Extract property features from user descriptions.

CRITICAL RULES:
1. Extract EXACTLY what is stated - do not guess
2. Use these quality mappings:
   - "poor condition", "fixer", "needs work" → OverallQual 3
   - "average", "decent" → OverallQual 5
   - "nice", "good" → OverallQual 7
   - "luxury", "high-end", "top quality" → OverallQual 9
3. Convert all numbers to integers where appropriate
4. Return ONLY valid JSON, no markdown, no extra text

FEATURE DEFINITIONS:
- LotFrontage: street frontage in feet (number or null)
- LotArea: lot size in sq ft (number or null)
- OverallQual: 1-10 rating (integer or null)
- YearBuilt: construction year (integer or null)
- GrLivArea: living area in sq ft (number or null)
- FullBath: number of full bathrooms (integer or null)
- BedroomAbvGr: number of bedrooms (integer or null)
- GarageCars: garage capacity (integer or null)
- Neighborhood: neighborhood name (string or null)
- HouseStyle: architectural style (string or null)
- Street: road type - "Paved" or "Gravel" (string or null)

Example: "2 bedroom fixer from 1950 with 1200 sq ft"
{
    "LotFrontage": null,
    "LotArea": null,
    "OverallQual": 3,
    "YearBuilt": 1950,
    "GrLivArea": 1200,
    "FullBath": null,
    "BedroomAbvGr": 2,
    "GarageCars": null,
    "Neighborhood": null,
    "HouseStyle": null,
    "Street": null,
    "completeness": {
        "extracted_count": 4,
        "total_features": 11,
        "confidence": "medium"
    }
}

Return JSON now for: """
        },
        {
            "role": "user",
            "content": text
        }
    ]
    
    try:
        logger.info(f"Extracting features from: {text[:100]}...")
        response = call_llm(messages, temperature=0.0)
        logger.info(f"LLM Response received: {response[:200]}...")
        
        # Clean the response - handle various formats
        json_str = response.strip()
        
        # Remove markdown code blocks if present
        if "```json" in json_str:
            json_str = json_str.split("```json")[1].split("```")[0].strip()
        elif "```" in json_str:
            json_str = json_str.split("```")[1].split("```")[0].strip()
        
        # Remove any text before the first { and after the last }
        start_idx = json_str.find('{')
        end_idx = json_str.rfind('}') + 1
        if start_idx != -1 and end_idx > start_idx:
            json_str = json_str[start_idx:end_idx]
        
        # Parse JSON
        data = json.loads(json_str)
        logger.info(f"Parsed JSON: {data}")
        
        # Ensure all expected fields exist
        expected_fields = [
            "LotFrontage", "LotArea", "OverallQual", "YearBuilt", 
            "GrLivArea", "FullBath", "BedroomAbvGr", "GarageCars",
            "Neighborhood", "HouseStyle", "Street"
        ]
        
        for field in expected_fields:
            if field not in data:
                data[field] = None
        
        # Calculate completeness
        extracted = sum(1 for k, v in data.items() 
                       if k in expected_fields and v is not None)
        
        data["completeness"] = {
            "extracted_count": extracted,
            "total_features": 11,
            "confidence": "high" if extracted >= 8 else "medium" if extracted >= 5 else "low"
        }
        
        logger.info(f"Extracted {extracted} features")
        return ExtractedFeatures(**data)
        
    except json.JSONDecodeError as e:
        logger.error(f"JSON parse error: {e}")
        logger.error(f"Raw response: {response}")
        
        # Fallback: Try to manually extract using regex
        return manual_extraction(text)
        
    except Exception as e:
        logger.error(f"Extraction error: {e}")
        return manual_extraction(text)


def manual_extraction(text: str) -> ExtractedFeatures:
    """
    Fallback manual extraction using regex patterns.
    """
    text_lower = text.lower()
    features = {}
    
    # Extract bedrooms
    bedroom_match = re.search(r'(\d+)\s*bedroom', text_lower)
    features['BedroomAbvGr'] = int(bedroom_match.group(1)) if bedroom_match else None
    
    # Extract bathrooms
    bath_match = re.search(r'(\d+\.?\d*)\s*bath', text_lower)
    if bath_match:
        bath_val = float(bath_match.group(1))
        features['FullBath'] = int(bath_val) if bath_val >= 1 else None
    else:
        features['FullBath'] = None
    
    # Extract year
    year_match = re.search(r'\b(19\d{2}|20\d{2})\b', text)
    features['YearBuilt'] = int(year_match.group(1)) if year_match else None
    
    # Extract square footage
    sqft_match = re.search(r'(\d+)\s*(?:sq\.?\s*ft|square\s*feet)', text_lower)
    features['GrLivArea'] = float(sqft_match.group(1)) if sqft_match else None
    
    # Extract quality
    if any(word in text_lower for word in ['poor', 'fixer', 'needs work', 'renovation']):
        features['OverallQual'] = 3
    elif any(word in text_lower for word in ['average', 'decent']):
        features['OverallQual'] = 5
    elif any(word in text_lower for word in ['nice', 'good']):
        features['OverallQual'] = 7
    elif any(word in text_lower for word in ['luxury', 'high-end', 'excellent', 'top']):
        features['OverallQual'] = 9
    else:
        features['OverallQual'] = None
    
    # Extract garage
    garage_match = re.search(r'(\d+)\s*(?:car\s*)?garage', text_lower)
    features['GarageCars'] = int(garage_match.group(1)) if garage_match else None
    
    # Extract house style
    if 'ranch' in text_lower:
        features['HouseStyle'] = 'Ranch'
    elif '2-story' in text_lower or 'two story' in text_lower:
        features['HouseStyle'] = '2Story'
    elif '1-story' in text_lower or 'one story' in text_lower:
        features['HouseStyle'] = '1Story'
    else:
        features['HouseStyle'] = None
    
    # Set defaults for missing
    for field in ['LotFrontage', 'LotArea', 'Neighborhood', 'Street']:
        features[field] = None
    
    # Calculate completeness
    extracted = sum(1 for v in features.values() if v is not None)
    features['completeness'] = {
        "extracted_count": extracted,
        "total_features": 11,
        "confidence": "medium" if extracted >= 5 else "low"
    }
    
    logger.info(f"Manual extraction found {extracted} features")
    return ExtractedFeatures(**features)