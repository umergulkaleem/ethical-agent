# compliance_checks/bias_checker.py
import json, re, time
from typing import Dict, Any
from core.aiml_client import chat_completion

BIAS_PROMPT = """
You are an assistant that detects biased or unfair statements in a passage.
Given the input text, produce a JSON object with keys:
- issues: array of {sentence, labels:[], explanation, severity: "low|medium|high"}
- score: 0.0-1.0 overall bias score (higher means more biased)
Only output valid JSON.

Text:
\"\"\"{text}\"\"\" 
"""

def check_bias(text: str) -> Dict[str, Any]:
    try:
        raw = chat_completion(BIAS_PROMPT.format(text=text))
        m = re.search(r'(\{.*\})', raw, re.S)
        payload = raw if not m else m.group(1)
        parsed = json.loads(payload)
        parsed.setdefault("raw", raw)
        parsed.setdefault("checked_at", int(time.time()))
        return {"check": "bias", "engine": "aiml-gpt", **parsed}
    except Exception as e:
        return {"check": "bias", "engine": "fallback", "error": str(e), "score": 0.0}
