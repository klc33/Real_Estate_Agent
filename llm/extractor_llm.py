import json
import logging
from typing import Dict, Any
from llm.client import call_llm
from app.schemas import ExtractedFeatures
from app.prompts.stage1_prompt import build_stage1_prompt_v1, build_stage1_prompt_v2

logger = logging.getLogger(__name__)


def extract_features(text: str, prompt_version: str = "v1") -> ExtractedFeatures:
    """
    Extract features using the specified prompt version.
    Includes fallback handling for malformed LLM responses.
    
    Args:
        text: User's natural language query
        prompt_version: "v1" or "v2" for different prompt strategies
    
    Returns:
        ExtractedFeatures object with parsed values
    """
    
    # Select prompt version
    if prompt_version == "v2":
        prompt = build_stage1_prompt_v2(text)
    else:
        prompt = build_stage1_prompt_v1(text)
    
    try:
        response = call_llm(prompt)
        
        # Parse JSON from response - handle markdown code blocks
        json_str = response.strip()
        
        if "```json" in json_str:
            json_str = json_str.split("```json")[1].split("```")[0].strip()
        elif "```" in json_str:
            json_str = json_str.split("```")[1].split("```")[0].strip()
        
        # Clean up any trailing commas or invalid JSON
        data = json.loads(json_str)
        
        # Ensure completeness field exists
        if "completeness" not in data:
            extracted = sum(1 for k, v in data.items() 
                          if k != "completeness" and v is not None)
            data["completeness"] = {
                "extracted_count": extracted,
                "total_features": 11,
                "confidence": "high" if extracted >= 8 else "medium" if extracted >= 5 else "low"
            }
        
        # Validate and create object
        return ExtractedFeatures(**data)
        
    except json.JSONDecodeError as e:
        logger.error(f"JSON parse error: {e}")
        logger.debug(f"Raw response: {response[:500]}")
        
        # Fallback: return minimal valid object
        return ExtractedFeatures(
            completeness={
                "extracted_count": 0,
                "total_features": 11,
                "confidence": "low"
            }
        )
        
    except Exception as e:
        logger.error(f"Extraction error: {e}")
        
        # Fallback with error info
        return ExtractedFeatures(
            completeness={
                "extracted_count": 0,
                "total_features": 11,
                "confidence": "low"
            }
        )


def compare_prompt_versions(query: str) -> Dict[str, Any]:
    """
    Compare both prompt versions for testing purposes.
    Returns results from both versions for evaluation.
    """
    results = {}
    
    for version in ["v1", "v2"]:
        try:
            features = extract_features(query, prompt_version=version)
            results[version] = {
                "success": True,
                "extracted_count": features.completeness.extracted_count if features.completeness else 0,
                "features": features.model_dump()
            }
        except Exception as e:
            results[version] = {
                "success": False,
                "error": str(e)
            }
    
    return results