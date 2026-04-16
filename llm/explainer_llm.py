import json
import os
import logging
from typing import Dict, Any
from llm.client import call_llm

logger = logging.getLogger(__name__)


def load_training_stats() -> Dict[str, Any]:
    """Load training statistics for context in explanations"""
    stats_path = os.path.join(os.path.dirname(__file__), "..", "ml", "training_stats.json")
    
    try:
        if os.path.exists(stats_path):
            with open(stats_path, "r") as f:
                return json.load(f)
    except Exception as e:
        logger.warning(f"Could not load training stats: {e}")
    
    # Fallback stats
    return {
        "median_price": 180000,
        "mean_price": 185000,
        "price_std": 80000,
        "price_range": [50000, 750000],
        "sample_count": 2000
    }


def explain(price: float, features: Dict[str, Any]) -> str:
    """
    Generate contextual explanation for the predicted price.
    Includes market context and feature importance reasoning.
    
    Args:
        price: Predicted price in dollars
        features: Dictionary of extracted features
    
    Returns:
        Natural language explanation string
    """
    
    # Load training stats for context
    stats = load_training_stats()
    
    # Clean features for display (remove completeness metadata)
    clean_features = {k: v for k, v in features.items() 
                     if k != "completeness" and v is not None}
    
    # Determine price category
    median = stats.get("median_price", 180000)
    if price > median * 1.2:
        price_category = "above market average"
    elif price < median * 0.8:
        price_category = "below market average"
    else:
        price_category = "near market average"
    
    system_prompt = f"""You are a knowledgeable real estate pricing expert.
Explain predictions clearly, conversationally, and helpfully.

Market context from training data:
- Median home price: ${stats['median_price']:,.0f}
- Average home price: ${stats['mean_price']:,.0f}
- Typical price range: ${stats['price_range'][0]:,.0f} - ${stats['price_range'][1]:,.0f}
- Based on {stats['sample_count']} home sales

Guidelines for your explanation:
1. State if the price is above, below, or near market average
2. Mention 2-3 key features that likely influenced the price
3. Note any missing features that could affect accuracy
4. Keep it concise (2-4 sentences)
5. Be helpful but acknowledge limitations
"""

    user_prompt = f"""Predicted price: ${price:,.2f} (This is {price_category})

Features provided:
{json.dumps(clean_features, indent=2)}

Number of features provided: {len(clean_features)} out of 11 total

Please explain this valuation in 2-4 sentences. What features likely influenced 
the price most? If many features are missing, acknowledge the uncertainty."""

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]
    
    try:
        response = call_llm(messages, temperature=0.3, max_tokens=300)
        explanation = response.strip()
        
        if not explanation:
            # Fallback explanation
            if len(clean_features) < 5:
                explanation = (f"This home is valued at approximately ${price:,.0f} "
                             f"based on limited information. Providing more details about "
                             f"square footage, bedrooms, or neighborhood would improve accuracy.")
            else:
                explanation = (f"This home is valued at ${price:,.0f}, which is {price_category}. "
                             f"This estimate is based on the {len(clean_features)} features provided.")
        
        return explanation
        
    except Exception as e:
        logger.error(f"Explanation generation failed: {e}")
        
        # Final fallback
        if len(clean_features) < 5:
            return (f"Estimated value: ${price:,.0f} based on limited information. "
                   f"More details would help provide a more accurate estimate.")
        else:
            return f"Estimated value: ${price:,.0f} based on the provided features."