# compliance_checks/safety_checker.py
import json, re
from typing import Dict, Any
from core.aiml_client import chat_completion

SAFETY_PROMPT = """
You are a safety classifier. Analyze the following text for unsafe, toxic, or harmful content.
Return JSON with:
- category: "safe" | "unsafe"
- severity: "low" | "medium" | "high"
- issues: array of {token, explanation}
- summary: short explanation

Text:
\"\"\"{text}\"\"\" 
"""

def check_safety(text: str) -> Dict[str, Any]:
    try:
        raw = chat_completion(SAFETY_PROMPT.format(text=text))
        m = re.search(r'(\{.*\})', raw, re.S)
        payload = raw if not m else m.group(1)
        parsed = json.loads(payload)
        parsed.setdefault("raw", raw)
        return {"check": "safety", "engine": "aiml-gpt", **parsed}
    except Exception as e:
        return {"check": "safety", "engine": "regex-fallback", "error": str(e)}
