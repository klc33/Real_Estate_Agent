import json
from app.llm_client import call_llm
from app.schemas import ExtractedFeatures
from app.prompts.stage1_prompt import build_stage1_prompt


def extract_features(text: str):

    prompt = build_stage1_prompt(text)

    response = call_llm(prompt)

    try:
        data = json.loads(response)
    except:
        raise ValueError("LLM returned invalid JSON")

    return ExtractedFeatures(**data)