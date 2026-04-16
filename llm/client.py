import os
import requests
import logging
from typing import List, Dict, Any
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

API_KEY = os.getenv("GROQ_API_KEY")
BASE_URL = "https://api.groq.com/openai/v1/chat/completions"
DEFAULT_MODEL = "llama-3.1-8b-instant"


def call_llm(messages: List[Dict[str, str]], 
             model: str = DEFAULT_MODEL,
             temperature: float = 0.0,
             max_tokens: int = 1000) -> str:
    """
    Call the Groq LLM API with error handling and retries.
    """
    if not API_KEY:
        raise ValueError("GROQ_API_KEY environment variable not set")
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens
    }
    
    try:
        logger.debug(f"Calling LLM with {len(messages)} messages")
        response = requests.post(
            BASE_URL,
            headers=headers,
            json=payload,
            timeout=30
        )
        response.raise_for_status()
        
        data = response.json()
        content = data["choices"][0]["message"]["content"]
        logger.debug(f"LLM response received: {len(content)} chars")
        
        return content
        
    except requests.exceptions.Timeout:
        logger.error("LLM API timeout")
        raise Exception("LLM API request timed out")
        
    except requests.exceptions.RequestException as e:
        logger.error(f"LLM API request failed: {e}")
        raise Exception(f"LLM API error: {str(e)}")
        
    except (KeyError, IndexError) as e:
        logger.error(f"Unexpected LLM response format: {e}")
        raise Exception("Invalid response format from LLM API")