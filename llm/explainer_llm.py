from app.llm.client import call_llm


def explain(price, features):

    messages = [
        {
            "role": "system",
            "content": """
You are a real estate expert.

Explain why the predicted price makes sense.
Be simple and clear.
"""
        },
        {
            "role": "user",
            "content": f"""
Price: {price}

Features:
{features}

Explain the pricing.
"""
        }
    ]

    return call_llm(messages)