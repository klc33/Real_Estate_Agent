import os
from dotenv import load_dotenv
import requests

load_dotenv()

API_KEY = os.getenv("GROQ_API_KEY")
print(f"API Key exists: {bool(API_KEY)}")
print(f"API Key starts with: {API_KEY[:10]}..." if API_KEY else "No key found")

# Test the API
headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

payload = {
    "model": "llama-3.1-8b-instant",
    "messages": [
        {"role": "user", "content": "Say 'API is working!' if you can hear me."}
    ],
    "temperature": 0,
    "max_tokens": 50
}

try:
    response = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers=headers,
        json=payload,
        timeout=10
    )
    
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        content = data["choices"][0]["message"]["content"]
        print(f"Response: {content}")
        print("✅ Groq API is working!")
    else:
        print(f"❌ Error: {response.text}")
        
except Exception as e:
    print(f"❌ Error: {e}")