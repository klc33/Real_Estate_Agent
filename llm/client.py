import os
import requests
import logging
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

API_KEY = os.getenv("GROQ_API_KEY")
BASE_URL = "https://api.groq.com/openai/v1/chat/completions"
DEFAULT_MODEL = "llama-3.1-8b-instant"


def call_llm(messages: List[Dict[str, str]], 
             model: str = DEFAULT_MODEL,
             temperature: float = 0.0,
             max_tokens: int = 500) -> str:
    """
    Call the Groq LLM API with error handling and retries.
    """
    if not API_KEY:
        logger.error("GROQ_API_KEY environment variable not set")
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
    
    logger.info(f"Calling Groq API with model: {model}")
    
    try:
        response = requests.post(
            BASE_URL,
            headers=headers,
            json=payload,
            timeout=30
        )
        
        # Log response status
        logger.info(f"Groq API response status: {response.status_code}")
        
        if response.status_code != 200:
            logger.error(f"Groq API error: {response.text}")
            raise Exception(f"Groq API error: {response.status_code}")
        
        response.raise_for_status()
        
        data = response.json()
        
        # Check if we got a valid response
        if "choices" not in data or len(data["choices"]) == 0:
            logger.error(f"Invalid response structure: {data}")
            raise Exception("No choices in API response")
        
        content = data["choices"][0]["message"]["content"]
        logger.debug(f"LLM response: {content[:200]}...")
        
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