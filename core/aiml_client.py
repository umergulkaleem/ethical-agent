# core/aiml_client.py
import os
from openai import OpenAI

# Wrapper for AIML API (OpenAI-compatible endpoint)
def get_client():
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY not set")

    return OpenAI(
        base_url="https://api.aimlapi.com/v1",
        api_key=api_key,
    )

def chat_completion(prompt: str, model: str = None, max_tokens: int = 400) -> str:
    client = get_client()
    model = model or os.environ.get("MODEL", "gpt-4")
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a compliance analysis assistant."},
            {"role": "user", "content": prompt},
        ],
        max_tokens=max_tokens,
    )
    return response.choices[0].message.content
